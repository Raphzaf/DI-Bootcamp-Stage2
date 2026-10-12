"""Checks that need no LLM: python tests/smoke_test.py
1) secrets are redacted  2) our paper-intel server works over STDIO with typed outputs
3) unknown tool -> readable error  4) injected fault -> error without retry  5) timeout -> logged retries."""
import asyncio
import json
import sys
from dataclasses import replace
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from agent.config import load_settings             # noqa: E402
from agent.mcp_hub import MCPHub                   # noqa: E402
from agent.observability import RunLogger, redact  # noqa: E402

PAPERS = json.dumps({"papers": [
    {"id": "2106.09685v2", "title": "LoRA: Low-Rank Adaptation of Large Language Models", "published": "2021-06-17",
     "authors": ["Edward J. Hu", "Yelong Shen", "Phillip Wallis"],
     "abstract": "We propose Low-Rank Adaptation, or LoRA, which freezes the pre-trained model weights and injects "
                 "trainable rank decomposition matrices. LoRA reduces the number of trainable parameters by 10,000 "
                 "times and the GPU memory requirement by 3 times compared to GPT-3 175B fine-tuned with Adam."},
    {"id": "2106.09685", "title": "duplicate"},
    {"id": "1706.03762", "title": "Attention Is All You Need", "published": "2017-06-12", "authors": ["Ashish Vaswani"],
     "abstract": "We propose a new simple network architecture, the Transformer, based solely on attention mechanisms. "
                 "Experiments on two machine translation tasks show these models to be superior in quality."}]})


async def main():
    assert "gsk_" not in redact("key gsk_abcdefghijklmnopqrstuvwxyz") and "hunter2" not in redact('{"api_key": "hunter2"}')
    print("ok  redaction")

    s = load_settings()
    ours = [sp for sp in s.servers if sp.name == "paper_intel"]
    logger = RunLogger(s.log_dir)
    async with MCPHub(replace(s, servers=ours, fault_inject={"paper_intel__extract_findings": 1}), logger) as hub:
        specs = {f["function"]["name"] for f in hub.function_specs()}
        assert specs == {"paper_intel__rank_papers", "paper_intel__extract_findings"}, specs
        ok, out = await hub.call("paper_intel__rank_papers", {"topic": "LoRA low-rank adaptation", "papers": PAPERS, "top_k": 2})
        res = json.loads(out)
        assert ok and res["duplicates_removed"] == 1 and res["off_topic_removed"] == 1 and res["ranked"][0]["id"] == "2106.09685", out
        print("ok  rank_papers ->", [(p["rank"], p["id"], p["score"]) for p in res["ranked"]])

        ok, out = await hub.call("paper_intel__extract_findings", {"topic": "LoRA", "paper_ids": ["2106.09685"]})
        assert not ok and "simulated outage" in out
        print("ok  injected fault ->", out)
        ok, out = await hub.call("paper_intel__extract_findings", {"topic": "LoRA", "paper_ids": ["2106.09685"]})
        res = json.loads(out)
        assert ok and res["findings"][0]["cite"] == 1 and "## References" in res["brief_markdown"], out
        print("ok  extract_findings ->", res["findings"][0]["text"][:90], "...")

        ok, out = await hub.call("paper_intel__rank_papers", {"topic": "x", "papers": "nothing here"})
        assert not ok and "No papers found" in out
        print("ok  bad input -> tool error the LLM can act on:", out[:80])
        ok, out = await hub.call("paper_intel__nope", {})
        assert not ok and "Unknown tool" in out
        print("ok  unknown tool -> readable error")

    async with MCPHub(replace(s, servers=ours, tool_timeout_s=0.0001, tool_retries=1, fault_inject={}), logger) as hub:
        ok, out = await hub.call("paper_intel__rank_papers", {"topic": "t", "papers": PAPERS})
        retries = [e for e in logger.events if e["kind"] == "tool_retry"]
        assert not ok and len(retries) == 2, (ok, out, retries)
        print(f"ok  timeout -> {len(retries)} logged attempts, then: {out}")
    print("all smoke tests passed")


if __name__ == "__main__":
    asyncio.run(main())
