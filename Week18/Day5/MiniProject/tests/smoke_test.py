"""Offline-friendly checks (no LLM needed): python tests/smoke_test.py
1) secrets are redacted from logs  2) our MCP server works over STDIO  3) retries + readable errors on timeouts."""
import asyncio
import json
import sys
from dataclasses import replace
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from agent.config import load_settings          # noqa: E402
from agent.mcp_hub import MCPHub                # noqa: E402
from agent.observability import RunLogger, redact  # noqa: E402


async def main():
    assert "gsk_" not in redact("key gsk_abcdefghijklmnopqrstuvwxyz"), "Groq key not redacted"
    assert "hunter2" not in redact('{"api_key": "hunter2"}'), "api_key not redacted"
    print("ok  redaction")

    s = load_settings()
    research_only = [sp for sp in s.servers if sp.name == "research"]
    logger = RunLogger(s.log_dir)
    async with MCPHub(replace(s, servers=research_only), logger) as hub:
        ok, out = await hub.call("research__clean_citations", {"papers": json.dumps(
            [{"id": "2106.09685v2", "title": "LoRA: Low-Rank Adaptation of Large Language Models",
              "authors": ["Edward J. Hu", "Yelong Shen", "Phillip Wallis", "Zeyuan Allen-Zhu"], "published": "2021-06-17"},
             {"id": "2106.09685", "title": "LoRA (duplicate)"}])})
        res = json.loads(out)
        assert ok and res["count"] == 1 and res["duplicates_removed"] == 1, out
        print("ok  research__clean_citations ->", res["references"][0])

        ok, out = await hub.call("research__nope", {})
        assert not ok and "Unknown tool" in out
        print("ok  unknown tool -> readable error")

    # a tiny timeout forces the retry path: every attempt is logged, then a clean error is returned
    async with MCPHub(replace(s, servers=research_only, tool_timeout_s=0.0001, tool_retries=1), logger) as hub:
        ok, out = await hub.call("research__assemble_brief", {"topic": "t", "key_findings": ["a"], "references": ["r"]})
        retries = [e for e in logger.events if e["kind"] == "tool_retry"]
        assert not ok and len(retries) == 2, (ok, out, retries)
        print(f"ok  timeout -> {len(retries)} logged attempts, then: {out}")
    print("all smoke tests passed; log:", logger.path)


if __name__ == "__main__":
    asyncio.run(main())
