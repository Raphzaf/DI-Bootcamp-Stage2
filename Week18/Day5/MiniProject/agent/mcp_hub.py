"""Connect to several MCP servers over STDIO, expose their tools as namespaced LLM function specs,
and call them with timeouts and retries."""
import asyncio
import json
import os
import re
import urllib.parse
from contextlib import AsyncExitStack

from mcp import ClientSession, StdioServerParameters, types
from mcp.client.stdio import stdio_client

SEP = "__"   # LLM-visible tool name = "<server>__<tool>"
FALLBACK_SEARCH = types.Tool(
    name="search_papers",
    description="Search arXiv papers by keywords (fallback served via the fetch server + Semantic Scholar API because the arXiv MCP server is unavailable).",
    inputSchema={"type": "object", "properties": {"query": {"type": "string"}, "max_results": {"type": "integer"}},
                 "required": ["query"]})


class MCPHub:
    def __init__(self, settings, logger):
        self.settings, self.logger = settings, logger
        self.stack = AsyncExitStack()
        self.sessions, self.tools, self.status = {}, {}, {}

    async def __aenter__(self):
        errlog = self.stack.enter_context(open(self.settings.log_dir / "servers_stderr.log", "a"))
        for spec in self.settings.servers:
            try:
                # pass the full environment: proxies, CA bundles and PATH are needed by uvx/npx
                params = StdioServerParameters(command=spec.command[0], args=spec.command[1:], env=dict(os.environ),
                                               cwd=str(self.settings.workspace.parent))
                read, write = await self.stack.enter_async_context(stdio_client(params, errlog=errlog))
                session = await self.stack.enter_async_context(ClientSession(read, write))
                await asyncio.wait_for(session.initialize(), timeout=180)
                listed = (await session.list_tools()).tools
                exposed = [t for t in listed if not spec.allow or t.name in spec.allow]
                self.sessions[spec.name] = session
                for t in exposed:
                    self.tools[f"{spec.name}{SEP}{t.name}"] = (spec.name, t)
                self.status[spec.name] = {"ok": True, "third_party": spec.third_party,
                                          "tools_total": len(listed), "tools_exposed": [t.name for t in exposed]}
                self.logger.log("server_connected", server=spec.name, tools=[t.name for t in exposed], tools_total=len(listed))
            except Exception as e:   # one failing server must not kill the app: continue with the others
                self.status[spec.name] = {"ok": False, "third_party": spec.third_party, "error": f"{type(e).__name__}: {e}"[:300]}
                self.logger.log("server_failed", server=spec.name, error=f"{type(e).__name__}: {e}")
        # provider fallback: keep arxiv__search_papers available through the fetch server if arXiv's server is down
        if f"arxiv{SEP}search_papers" not in self.tools and "fetch" in self.sessions:
            self.tools[f"arxiv{SEP}search_papers"] = ("fetch-fallback", FALLBACK_SEARCH)
            self.logger.log("fallback_enabled", tool=f"arxiv{SEP}search_papers", via="fetch")
        return self

    async def __aexit__(self, *exc):
        try:
            await self.stack.aclose()
        except Exception:
            pass

    def function_specs(self):
        specs = []
        for full, (server, t) in self.tools.items():
            schema = t.inputSchema or {"type": "object", "properties": {}}
            specs.append({"type": "function", "function": {
                "name": full,
                "description": f"[{server}] {(t.description or t.name)[:400]}",
                "parameters": {"type": "object", "properties": schema.get("properties", {}),
                               "required": schema.get("required", [])}}})
        return specs

    async def call(self, full_name: str, args: dict):
        """Returns (ok, text). Retries timeouts/transient errors; returns a readable error otherwise."""
        if full_name not in self.tools:
            return False, f"Unknown tool '{full_name}'. Available: {sorted(self.tools)}"
        server, tool = self.tools[full_name]
        if server == "fetch-fallback":
            return await self._search_via_fetch(args)
        last_err = ""
        for attempt in range(1, self.settings.tool_retries + 2):
            try:
                res = await asyncio.wait_for(self.sessions[server].call_tool(tool.name, arguments=args),
                                             timeout=self.settings.tool_timeout_s)
                if res.structuredContent and "result" in res.structuredContent:
                    val = res.structuredContent["result"]
                    text = val if isinstance(val, str) else json.dumps(val, ensure_ascii=False)
                else:
                    text = "\n".join(getattr(c, "text", "") for c in res.content)
                if res.isError:
                    return False, text or "tool returned an error"
                return True, text
            except asyncio.TimeoutError:
                last_err = f"timeout after {self.settings.tool_timeout_s:g}s"
            except Exception as e:
                last_err = f"{type(e).__name__}: {e}"
            self.logger.log("tool_retry", tool=full_name, attempt=attempt, error=last_err)
            await asyncio.sleep(2 * attempt)
        if full_name == f"arxiv{SEP}search_papers" and "fetch" in self.sessions:   # runtime fallback
            self.logger.log("fallback_used", tool=full_name, via="fetch", error=last_err)
            return await self._search_via_fetch(args)
        return False, f"Tool failed after {self.settings.tool_retries + 1} attempts: {last_err}"

    async def _search_via_fetch(self, args: dict):
        """Paper search through the third-party fetch server and the Semantic Scholar API (its robots.txt allows it;
        arXiv's export API does not allow autonomous fetching). Same output shape as arxiv-mcp-server."""
        q = urllib.parse.quote_plus(str(args.get("query", "")))
        url = (f"https://api.semanticscholar.org/graph/v1/paper/search?query={q}&limit={int(args.get('max_results') or 5)}"
               f"&fields=title,year,authors,externalIds,abstract")
        last = ""
        for attempt in range(1, self.settings.tool_retries + 2):   # the public API is rate-limited: retry with backoff
            self.logger.log("tool_call", tool="fetch__fetch (fallback)", attempt=attempt, args={"url": url})
            try:
                res = await asyncio.wait_for(self.sessions["fetch"].call_tool(
                    "fetch", arguments={"url": url, "raw": True, "max_length": 50000}), timeout=self.settings.tool_timeout_s)
                text = "\n".join(getattr(c, "text", "") for c in res.content)
                body = json.loads(text[text.index("{"):]) if "{" in text else {}
                if "data" not in body:
                    raise ValueError(text[:200])
                papers = [{"id": (p.get("externalIds") or {}).get("ArXiv") or p.get("paperId"),
                           "title": p.get("title", ""), "authors": [a["name"] for a in p.get("authors") or []],
                           "published": str(p.get("year") or ""), "abstract": (p.get("abstract") or "")[:400]}
                          for p in body["data"]]
                return True, json.dumps({"returned": len(papers), "source": "fallback: fetch + Semantic Scholar",
                                         "papers": papers}, ensure_ascii=False)
            except Exception as e:
                last = f"{type(e).__name__}: {e}"
                self.logger.log("tool_retry", tool="fetch__fetch (fallback)", attempt=attempt, error=last)
                await asyncio.sleep(3 * attempt)
        return False, f"Paper search unavailable (arxiv server and fetch fallback failed): {last}"
