"""Our own MCP server: research helpers used together with the third-party arXiv/filesystem servers.

Tools
- clean_citations: normalise messy paper metadata (JSON from arXiv search, BibTeX or plain lines) into
  deduplicated, consistently formatted references [1], [2], ...
- assemble_brief: build a Markdown research brief (summary, key findings, references) from structured inputs.
"""
import ast
import json
import logging
import re
import sys
import urllib.request
import xml.etree.ElementTree as ET
from datetime import date

from mcp.server.fastmcp import FastMCP

logging.basicConfig(level=logging.INFO, stream=sys.stderr, format="[research] %(message)s")
mcp = FastMCP("research-tools")


def _norm_authors(authors) -> str:
    if isinstance(authors, str):
        authors = [a.strip() for a in re.split(r",| and ", authors) if a.strip()]
    authors = [re.sub(r"\s+", " ", a) for a in (authors or [])]
    if not authors:
        return "Unknown author"
    if len(authors) > 3:
        return f"{authors[0]} et al."
    return ", ".join(authors[:-1]) + (" & " if len(authors) > 1 else "") + authors[-1]


def _parse_items(papers) -> list[dict]:
    """Accept JSON / Python-literal (list, or {'papers': [...]}), a list of arXiv ids, or plain text lines."""
    data = papers
    if isinstance(papers, str):
        data = None
        for loader in (json.loads, ast.literal_eval):   # small LLMs sometimes send Python-style lists
            try:
                data = loader(papers)
                break
            except (ValueError, SyntaxError, TypeError):
                continue
    if isinstance(data, dict):
        data = data.get("papers") or data.get("results") or [data]
    if isinstance(data, list):
        return [d if isinstance(d, dict) else {"id": str(d), "title": ""} for d in data]
    items = []
    for line in str(papers).splitlines():
        line = line.strip(" -*\t")
        if line:
            m = ARXIV_ID.search(line)
            items.append({"title": line, "id": m.group(1) if m else ""})
    return items


ARXIV_ID = re.compile(r"(\d{4}\.\d{4,5})(v\d+)?")
ATOM = "{http://www.w3.org/2005/Atom}"


def _enrich(items: list[dict]) -> list[dict]:
    """Fill missing titles/authors/years for bare arXiv ids from the public arXiv API (best effort)."""
    ids = [m.group(1) for it in items if not it.get("title") or ARXIV_ID.fullmatch(str(it.get("title")))
           for m in [ARXIV_ID.search(str(it.get("id", "")))] if m]
    if not ids:
        return items
    try:
        url = "https://export.arxiv.org/api/query?max_results=50&id_list=" + ",".join(ids)
        with urllib.request.urlopen(url, timeout=20) as r:
            root = ET.fromstring(r.read())
        meta = {}
        for e in root.iter(f"{ATOM}entry"):
            pid = ARXIV_ID.search(e.findtext(f"{ATOM}id", "")).group(1)
            meta[pid] = {"title": e.findtext(f"{ATOM}title", ""), "published": e.findtext(f"{ATOM}published", ""),
                         "authors": [a.findtext(f"{ATOM}name", "") for a in e.iter(f"{ATOM}author")]}
        logging.info("enriched %d/%d bare ids from the arXiv API", len(meta), len(ids))
        return [{**it, **meta.get(ARXIV_ID.search(str(it.get("id", ""))).group(1), {})}
                if ARXIV_ID.search(str(it.get("id", ""))) else it for it in items]
    except Exception as e:   # fallback: keep the ids as they are
        logging.warning("arXiv enrichment failed (%s); keeping bare ids", e)
        return items


@mcp.tool()
def clean_citations(papers: str, style: str = "short") -> dict:
    """Clean, deduplicate and number references.

    papers: the 'papers' list returned by arxiv search_papers (JSON string), a list of arXiv ids
            (e.g. '["2310.08659", "2502.01378"]', metadata is then looked up on arXiv), or one reference per line.
    style: 'short' (Authors (Year). Title. arXiv:ID) or 'markdown' (with a link).
    Returns {'count', 'references': [...], 'duplicates_removed'}.
    """
    items = _enrich(_parse_items(papers))
    seen, refs = set(), []
    for it in items:
        pid = re.sub(r"v\d+$", "", str(it.get("id") or it.get("arxiv_id") or it.get("versioned_id") or "").strip())
        title = re.sub(r"\s+", " ", str(it.get("title", "")).strip().rstrip("."))
        key = pid or title.lower()
        if not key or key in seen:
            continue
        seen.add(key)
        year = str(it.get("year") or it.get("published") or it.get("date") or "n.d.")[:4]
        ref = f"{_norm_authors(it.get('authors'))} ({year}). {title}."
        if pid:
            url = it.get("url") or f"https://arxiv.org/abs/{pid}"
            ref += f" [arXiv:{pid}]({url})" if style == "markdown" else f" arXiv:{pid}"
        refs.append(ref)
    numbered = [f"[{i}] {r}" for i, r in enumerate(refs, 1)]
    logging.info("clean_citations: %d in -> %d out", len(items), len(numbered))
    return {"count": len(numbered), "references": numbered, "duplicates_removed": len(items) - len(numbered)}


@mcp.tool()
def assemble_brief(topic: str, key_findings: list[str], references: list[str], summary: str = "") -> str:
    """Assemble a Markdown research brief. Cite references in findings with [n] matching the references list.

    summary: 3-5 sentences (optional: a default sentence is used when missing, so a weak LLM still gets a brief).
    Returns the brief as Markdown text (save it with the filesystem server's write_file tool).
    """
    summary = summary or f"This brief collects {len(references)} recent arXiv papers on {topic.strip()}; see the key findings below."
    findings = "\n".join(f"- {f.strip()}" for f in key_findings if f and f.strip()) or "- (no findings provided)"
    refs = "\n".join(r if r.startswith("[") else f"[{i}] {r}" for i, r in enumerate(references, 1)) or "(none)"
    brief = (f"# Research brief: {topic.strip()}\n\n_Generated {date.today().isoformat()} by the Research Notebook agent._\n\n"
             f"## Summary\n{summary.strip()}\n\n## Key findings\n{findings}\n\n## References\n{refs}\n")
    logging.info("assemble_brief: %d findings, %d references", len(key_findings), len(references))
    return brief


if __name__ == "__main__":
    mcp.run()
