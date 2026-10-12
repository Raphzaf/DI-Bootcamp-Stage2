"""LLM-driven plan -> act -> observe loop over the MCP hub (OpenAI-compatible API: GroqCloud or Ollama)."""
import json
import re
import time

from openai import OpenAI

from .mcp_hub import MCPHub
from .observability import RunLogger, summarize

SYSTEM_PROMPT = """You are "Research Notebook", an agent that prepares short, sourced research briefs from arXiv.
Tools come from several MCP servers (the prefix is the server):
- arxiv__*        third-party arXiv server: search papers, get one abstract
- paper_intel__*  OUR server: rank_papers (decide which papers are best for the topic),
                  extract_findings (quote key results from abstracts + build a cited Markdown brief)
- fetch__*        third-party fetch server: read a web page as markdown (optional)
- filesystem__*   third-party filesystem server, sandboxed to {workspace}: write/list files

Decide the next action from the previous results. A good plan is usually:
1) arxiv__search_papers for the topic (sort_by "relevance", max_results about 3x the number of papers wanted);
2) paper_intel__rank_papers with the topic, papers = a JSON list of the arXiv ids found, top_k = number wanted
   (if it reports too few on-topic papers, search again as its next_step says);
3) paper_intel__extract_findings with the topic and the ranked paper_ids (keep the ranking order);
4) filesystem__write_file with content = brief_markdown from step 3, unchanged, path = {workspace}/<file name>.
Each tool result may contain "next_step": follow it unless it no longer fits.
Rules: prefer one tool call at a time; only use facts returned by tools; if a tool fails, read the error and
re-plan (fix the arguments, retry later, use another tool such as arxiv__get_abstract or fetch__fetch, or
skip the step). When the file is saved, reply with a short final answer (what you did + the file path)."""


class Orchestrator:
    def __init__(self, settings, logger: RunLogger | None = None):
        self.s = settings
        self.logger = logger or RunLogger(settings.log_dir)
        self.outcome = {}
        self.client = OpenAI(base_url=settings.base_url, api_key=settings.api_key, timeout=180, max_retries=2)

    def _llm(self, messages, tools):
        for attempt in range(3):
            try:
                return self.client.chat.completions.create(model=self.s.model, messages=messages, tools=tools,
                                                           tool_choice="auto", temperature=0)
            except Exception as e:
                self.logger.log("llm_retry", attempt=attempt + 1, error=f"{type(e).__name__}: {e}")
                time.sleep(3 * (attempt + 1))
        raise RuntimeError("LLM backend unreachable after 3 attempts")

    @staticmethod
    def _normalize_args(name, args):
        """Input normalisation before a call: small LLMs often wrap file content in ``` fences."""
        if name == "filesystem__write_file" and isinstance(args.get("content"), str):
            args["content"] = re.sub(r"^\s*```[a-z]*\s*\n|\n?```\s*$", "", args["content"]).strip() + "\n"
        return args

    @staticmethod
    def _parse_args(raw):
        if isinstance(raw, dict):
            return raw
        try:
            return json.loads(raw or "{}")
        except json.JSONDecodeError:
            m = re.search(r"\{.*\}", raw or "", re.S)   # small models sometimes wrap JSON in text
            return json.loads(m.group(0)) if m else None

    async def run(self, goal: str, on_event=None):
        """Yields nothing; reports progress through on_event(event_dict). Returns (final_text, events)."""
        emit = (lambda e: on_event(e) if on_event else None)
        async with MCPHub(self.s, self.logger) as hub:
            for name, st in hub.status.items():
                emit({"kind": "server", "server": name, **st})
            tools = hub.function_specs()
            if not tools:
                raise RuntimeError("No MCP server could be started: check the server commands in .env and logs/servers_stderr.log")
            emit(self.logger.log("plan_start", goal=goal, tools=[t["function"]["name"] for t in tools]))
            down = [n for n, st in hub.status.items() if not st["ok"]]
            status_note = f"Note: servers unavailable right now: {', '.join(down)}.\n" if down else ""
            messages = [{"role": "system", "content": SYSTEM_PROMPT.replace("{workspace}", str(self.s.workspace))},
                        {"role": "user", "content": f"{status_note}Workspace folder (absolute path for filesystem tools): "
                                                    f"{self.s.workspace}\n\nGoal: {goal}"}]
            consecutive_failures, empty_replies, final, failed_calls = 0, 0, None, {}
            calls, saved = [], None
            wants_file, wrote_file, completion_nudges = bool(re.search(r"\bsave|\bwrite|\.md\b", goal, re.I)), False, 0
            for step in range(1, self.s.max_steps + 1):
                resp = self._llm(messages, tools)
                msg = resp.choices[0].message
                if not msg.tool_calls and not (msg.content or "").strip() and empty_replies < 2:
                    empty_replies += 1   # small local models sometimes return nothing: nudge them once or twice
                    self.logger.log("llm_empty_reply", step=step)
                    messages.append({"role": "user", "content": "Your reply was empty. Call the next tool needed for the goal."})
                    continue
                if not msg.tool_calls and wants_file and not wrote_file and completion_nudges < 2:
                    completion_nudges += 1   # verify the goal before accepting the final answer
                    self.logger.log("completion_check", step=step, text="goal asks for a file but none was written")
                    messages.append({"role": "assistant", "content": msg.content or ""})
                    messages.append({"role": "user", "content": "The goal is not complete: nothing has been saved yet. "
                                     f"Continue with the next tool call (build the brief with paper_intel__extract_findings if needed, then filesystem__write_file "
                                     f"with a path inside {self.s.workspace})."})
                    continue
                if not msg.tool_calls:
                    final = (msg.content or "").strip()
                    emit(self.logger.log("final", step=step, text=final))
                    break
                messages.append({"role": "assistant", "content": msg.content or "",
                                 "tool_calls": [tc.model_dump() for tc in msg.tool_calls]})
                for tc in msg.tool_calls:   # parallel calls are executed one after the other, in order
                    name, args = tc.function.name, self._parse_args(tc.function.arguments)
                    args = self._normalize_args(name, args) if isinstance(args, dict) else args
                    key = f"{name}:{json.dumps(args, sort_keys=True)}" if args is not None else None
                    if args is None:
                        ok, out = False, f"Arguments were not valid JSON: {tc.function.arguments[:200]}"
                    elif failed_calls.get(key, 0) >= 2:   # loop guard: do not replay a call that already failed twice
                        ok, out = False, "This exact call already failed twice. Do not repeat it: change the arguments or the tool."
                        emit(self.logger.log("tool_blocked_repeat", step=step, tool=name))
                    else:
                        emit(self.logger.log("tool_call", step=step, tool=name, args=args))
                        t0 = time.time()
                        ok, out = await hub.call(name, args)
                        emit(self.logger.log("tool_result", step=step, tool=name, ok=ok, seconds=round(time.time() - t0, 1), result=out))
                    consecutive_failures = 0 if ok else consecutive_failures + 1
                    if not ok and key:
                        failed_calls[key] = failed_calls.get(key, 0) + 1
                    wrote_file = wrote_file or (ok and name == "filesystem__write_file")
                    calls.append({"tool": name, "ok": ok})
                    if ok and name == "filesystem__write_file":
                        saved = (args or {}).get("path")
                    content = out if ok else f"ERROR: {out}\nAdapt: fix the arguments, use another tool, or continue without this step."
                    messages.append({"role": "tool", "tool_call_id": tc.id, "content": content[:6000]})
                if consecutive_failures >= 3:   # fallback: stop hammering a broken path
                    messages.append({"role": "user", "content": "Several tool calls failed in a row. Read the error, change the "
                                     "arguments or use a different tool (e.g. write the file directly) - do not give up on the goal."})
                    consecutive_failures = 0
            if final is None:                 # step budget exhausted: ask for a final answer without tools
                messages.append({"role": "user", "content": "Step limit reached. Give your final answer now, without tools."})
                resp = self.client.chat.completions.create(model=self.s.model, messages=messages, temperature=0)
                final = (resp.choices[0].message.content or "").strip()
                emit(self.logger.log("final", step="limit", text=final))
            # output normalisation: one structured outcome for the UI/CLI, whatever the LLM wrote
            self.outcome = {"status": "done" if (wrote_file or not wants_file) else "incomplete", "file": saved,
                            "tool_calls": len(calls), "failed_calls": sum(not c["ok"] for c in calls),
                            "servers_used": sorted({c["tool"].split("__")[0] for c in calls if c["ok"]}),
                            "sequence": [c["tool"] + ("" if c["ok"] else " (failed)") for c in calls]}
            self.logger.log("outcome", **self.outcome)
            return final, self.logger.events
