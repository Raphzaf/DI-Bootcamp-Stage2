"""Command-line runner: python cli.py "your research goal" (prints every tool call as it happens)."""
import asyncio
import json
import sys

from agent.config import load_settings
from agent.orchestrator import Orchestrator

DEFAULT_GOAL = ("Find 3 recent arXiv papers on LoRA fine-tuning of large language models and save a "
                "research brief to lora_brief.md in the workspace.")


def show(e):
    k = e.get("kind")
    if k == "server":
        state = "OK " if e.get("ok") else "FAIL"
        extra = ", ".join(e.get("tools_exposed", [])) if e.get("ok") else e.get("error")
        print(f"[server {state}] {e['server']:<10} {'third-party' if e.get('third_party') else 'ours':<11} {extra}")
    elif k == "tool_call":
        print(f"\n[step {e['step']}] -> {e['tool']}({e['args']})")
    elif k == "tool_result":
        print(f"[step {e['step']}] <- {'ok' if e['ok'] else 'ERROR'} in {e['seconds']}s: {e['result']}")
    elif k == "final":
        print(f"\n=== FINAL ===\n{e['text']}")


async def main():
    goal = " ".join(sys.argv[1:]) or DEFAULT_GOAL
    settings = load_settings()
    print("Config:", json.dumps(settings.public_summary(), indent=1))
    orch = Orchestrator(settings)
    await orch.run(goal, on_event=show)
    print("\n=== OUTCOME ===\n" + json.dumps(orch.outcome, indent=1))
    print(f"Run log: {orch.logger.path}")


if __name__ == "__main__":
    asyncio.run(main())
