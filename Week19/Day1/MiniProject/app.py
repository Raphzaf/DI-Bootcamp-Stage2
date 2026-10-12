"""Streamlit UI for the Research Notebook agent: streamlit run app.py"""
import asyncio
import json
from pathlib import Path

import streamlit as st

from agent.config import load_settings
from agent.orchestrator import Orchestrator

st.set_page_config(page_title="Research Notebook - MCP agent", page_icon="📚", layout="wide")
st.title("📚 Research Notebook")
st.caption("Part 2: an LLM plans multi-step calls across third-party MCP servers (arXiv, filesystem, fetch) and "
           "our own paper-intel server (rank_papers, extract_findings), then saves a sourced Markdown brief.")

try:
    settings = load_settings()
except RuntimeError as e:   # e.g. LLM_BACKEND=groq without a key
    st.error(f"Configuration error: {e}")
    st.stop()

with st.sidebar:
    st.header("Configuration")
    st.caption("Read from `.env` (secrets are never displayed).")
    st.json(settings.public_summary(), expanded=False)
    if "status" in st.session_state:
        st.header("MCP servers")
        for name, s in st.session_state.status.items():
            icon = "🟢" if s.get("ok") else "🔴"
            kind = "third-party" if s.get("third_party") else "ours"
            detail = ", ".join(s.get("tools_exposed", [])) if s.get("ok") else s.get("error", "")
            st.markdown(f"{icon} **{name}** ({kind})  \n<small>{detail}</small>", unsafe_allow_html=True)

topic = st.text_input("Research topic", "LoRA fine-tuning of large language models")
c1, c2 = st.columns(2)
n_papers = c1.slider("Number of papers", 2, 6, 3)
filename = c2.text_input("Output file (in the workspace)", "brief.md")
goal = st.text_area("Goal sent to the agent (editable)",
                    f"Find {n_papers} recent arXiv papers on {topic} and save a research brief to {filename} in the workspace.")

if st.button("Run agent", type="primary"):
    st.session_state.status, st.session_state.timeline = {}, []
    timeline = st.container(border=True)
    timeline.subheader("Tool calls (live)")

    def on_event(e):
        k = e.get("kind")
        if k == "server":
            st.session_state.status[e["server"]] = e
        elif k == "tool_call":
            timeline.markdown(f"**Step {e['step']} →** `{e['tool']}`")
            timeline.code(e["args"], language="json")
        elif k == "tool_result":
            (timeline.success if e["ok"] else timeline.error)(f"← {'ok' if e['ok'] else 'error'} in {e['seconds']}s: {e['result']}")
        if k in ("tool_call", "tool_result"):
            st.session_state.timeline.append(e)

    orch = Orchestrator(settings)
    with st.spinner("Agent working (starting MCP servers, planning, calling tools)..."):
        try:
            final, events = asyncio.run(orch.run(goal, on_event=on_event))
        except Exception as e:
            st.error(f"Run failed: {type(e).__name__}: {e}")
            st.stop()
    st.session_state.result = {"final": final, "outcome": orch.outcome, "log": str(orch.logger.path), "file": filename,
                               "events": [e for e in events if e["kind"] in ("tool_retry", "fallback_used",
                                                                              "fallback_enabled", "server_failed",
                                                                              "tool_blocked_repeat", "completion_check",
                                                                              "fault_injected")]}
    st.rerun()   # refresh the sidebar with the server status

if res := st.session_state.get("result"):
    with st.expander(f"Tool calls of the last run ({len(st.session_state.timeline) // 2})", expanded=True):
        for e in st.session_state.timeline:
            if e["kind"] == "tool_call":
                st.markdown(f"**Step {e['step']} →** `{e['tool']}`  `{e['args'][:200]}`")
            else:
                (st.success if e["ok"] else st.error)(f"← {'ok' if e['ok'] else 'error'} in {e['seconds']}s: {e['result'][:220]}")
    st.subheader("Outcome")
    o = res["outcome"]
    m1, m2, m3 = st.columns(3)
    m1.metric("Status", o.get("status", "?"))
    m2.metric("Tool calls", o.get("tool_calls", 0), f"-{o.get('failed_calls', 0)} failed" if o.get("failed_calls") else None)
    m3.metric("Servers used", len(o.get("servers_used", [])))
    st.caption(" → ".join(o.get("sequence", [])))
    st.markdown("**LLM final answer:** " + (res["final"] or "(empty)"))
    if res["events"]:
        with st.expander(f"Resilience events ({len(res['events'])}): retries / fallbacks"):
            for e in res["events"]:
                st.write(e)
    brief = settings.workspace / Path(res["file"]).name
    if brief.exists():
        st.subheader(f"Brief: {brief.name}")
        st.markdown(brief.read_text(encoding="utf-8"))
        st.download_button("Download the brief", brief.read_bytes(), file_name=brief.name, mime="text/markdown")
    with st.expander("Run log (JSONL, secret-free)"):
        st.code("\n".join(json.dumps(json.loads(l), ensure_ascii=False)
                          for l in Path(res["log"]).read_text(encoding="utf-8").splitlines()), language="json")
