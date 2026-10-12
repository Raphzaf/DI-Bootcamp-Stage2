"""paper-intel: our own MCP server (Part 2). It adds a decision step and an enrichment step that the
third-party servers do not provide.

Tools
- rank_papers(topic, papers, top_k, recency_weight)
    Opinionated decision step. It enriches papers from the arXiv API when only ids are given, removes
    duplicates, scores each paper on relevance to the topic (BM25 on title + abstract) and on recency,
    and returns the top_k with a score breakdown and a one-line reason for each.
- extract_findings(topic, paper_ids, per_paper)
    Transformation step. For each paper it picks the abstract sentence(s) that state a result
    ("we show", "outperforms", "reduces ... by 40%", ...). It returns numbered findings that cite
    their source [n], the matching reference list, and a ready-to-save Markdown brief.
    Every finding is copied verbatim from an abstract, so the LLM cannot invent findings.

Both tools return typed (pydantic) results, so MCP clients also receive an output schema.
Run: python paper_intel_server.py   (STDIO transport; logs go to stderr)
"""
import ast
import json
import logging
import math
import re
import sys
import time
import urllib.request
import xml.etree.ElementTree as ET
from datetime import date, datetime

from mcp.server.fastmcp import FastMCP
from pydantic import BaseModel, Field

logging.basicConfig(level=logging.INFO, stream=sys.stderr, format="[paper-intel] %(message)s")
mcp = FastMCP("paper-intel")

ARXIV_ID = re.compile(r"(\d{4}\.\d{4,5})(v\d+)?")
ATOM = "{http://www.w3.org/2005/Atom}"
STOP = set("a an and are as at be by for from has have in into is it its of on or our that the their this to "
           "was we were which with using use via based towards toward new study paper approach method".split())
RESULT_CUES = re.compile(r"\b(we (show|find|demonstrate|observe|achieve|report)|results? (show|indicate)|outperform\w*|"
                         r"improv\w*|reduc\w*|achiev\w*|surpass\w*|faster|fewer|state[- ]of[- ]the[- ]art|"
                         r"significant\w*|comparable|matches|up to|\d+(\.\d+)?\s?(%|x|×))", re.I)
ACRONYMS = {"llm": "large language model", "llms": "large language models", "rag": "retrieval augmented generation",
            "lora": "lora low-rank adaptation", "rl": "reinforcement learning", "nlp": "natural language processing"}
MIN_COVERAGE = 0.5   # a paper must match at least half of the topic terms to be kept
_CACHE: dict[str, dict] = {}   # arXiv metadata, kept for the server's lifetime


# ---------- typed outputs (become the tools' MCP output schemas) ----------
class RankedPaper(BaseModel):
    rank: int
    id: str = Field(description="arXiv id without version")
    title: str
    authors: str
    year: str
    score: float = Field(description="final score in [0, 1]")
    relevance: float = Field(description="BM25 relevance to the topic, normalised to [0, 1] among kept papers")
    coverage: float = Field(description="share of the topic terms found in the title/abstract")
    recency: float = Field(description="1.0 = this year, halves every 2 years")
    why: str


class RankResult(BaseModel):
    topic: str
    considered: int
    duplicates_removed: int
    off_topic_removed: int = Field(description="papers dropped because they match < 50% of the topic terms")
    ranked: list[RankedPaper]
    next_step: str


class Finding(BaseModel):
    cite: int = Field(description="reference number [n]")
    paper_id: str
    text: str = Field(description="sentence quoted verbatim from the abstract")


class FindingsResult(BaseModel):
    topic: str
    findings: list[Finding]
    references: list[str]
    missing_ids: list[str] = Field(description="ids whose abstract could not be found")
    brief_markdown: str = Field(description="complete Markdown brief, ready to be written to a file")
    next_step: str


# ---------- helpers ----------
def _tokens(text: str) -> list[str]:
    out = []
    for w in re.findall(r"[a-z0-9]+(?:-[a-z0-9]+)*", text.lower()):
        if w in STOP or len(w) < 2:
            continue
        w = re.sub(r"(ing|ed|es|s)$", "", w) if len(w) > 4 else w   # light stemming
        out.append(w)
    return out


def _topic_terms(topic: str) -> set[str]:
    """Topic terms, with common acronyms expanded (LLMs -> large language models)."""
    words = " ".join(ACRONYMS.get(w.lower(), w) for w in re.findall(r"[\w-]+", topic))
    return set(_tokens(words))


def _parse(papers) -> list[dict]:
    """JSON / Python literal (list, {'papers': [...]}) / list of ids / text with ids -> list of dicts."""
    data = papers
    if isinstance(papers, str):
        data = None
        for loader in (json.loads, ast.literal_eval):
            try:
                data = loader(papers)
                break
            except (ValueError, SyntaxError, TypeError):
                continue
        if not isinstance(data, (list, dict)):   # plain text, or a bare id that JSON reads as a float
            data = [m[0] for m in ARXIV_ID.findall(papers)]
    if isinstance(data, dict):
        data = data.get("papers") or data.get("results") or data.get("ranked") or [data]
    items = []
    for d in data or []:
        if isinstance(d, dict):
            m = ARXIV_ID.search(str(d.get("id") or d.get("arxiv_id") or d.get("paper_id") or ""))
            items.append({**d, "id": m.group(1) if m else str(d.get("id", ""))})
        else:
            m = ARXIV_ID.search(str(d))
            if m:
                items.append({"id": m.group(1)})
    return items


def _fetch_arxiv(ids: list[str]) -> None:
    """Fill _CACHE with title/abstract/authors/date from the public arXiv API (one batched request)."""
    todo = [i for i in dict.fromkeys(ids) if i and i not in _CACHE]
    if not todo:
        return
    url = "https://export.arxiv.org/api/query?max_results=50&id_list=" + ",".join(todo)
    for attempt in range(3):   # the arXiv API is rate-limited (about 1 request / 3 s): retry with backoff
        try:
            with urllib.request.urlopen(url, timeout=25) as r:
                root = ET.fromstring(r.read())
            if root.find(f"{ATOM}entry") is not None:
                break
        except Exception as e:
            logging.warning("arXiv API attempt %d failed: %s", attempt + 1, e)
            if attempt == 2:
                raise
        time.sleep(3 * (attempt + 1))
    for e in root.iter(f"{ATOM}entry"):
        m = ARXIV_ID.search(e.findtext(f"{ATOM}id", ""))
        if not m:
            continue
        _CACHE[m.group(1)] = {
            "id": m.group(1),
            "title": re.sub(r"\s+", " ", e.findtext(f"{ATOM}title", "")).strip(),
            "abstract": re.sub(r"\s+", " ", e.findtext(f"{ATOM}summary", "")).strip(),
            "authors": [a.findtext(f"{ATOM}name", "") for a in e.iter(f"{ATOM}author")],
            "published": e.findtext(f"{ATOM}published", "")}
    logging.info("arXiv API: fetched %d/%d papers", sum(i in _CACHE for i in todo), len(todo))


def _complete(items: list[dict]) -> list[dict]:
    """Merge what the caller gave with cached/API metadata (the caller's abstract snippets are often truncated)."""
    need = [it["id"] for it in items if ARXIV_ID.fullmatch(it.get("id", "")) and
            (len(str(it.get("abstract") or it.get("summary") or "")) < 400 or not it.get("title"))]
    try:
        _fetch_arxiv(need)
    except Exception as e:                      # degrade gracefully: keep what we already have
        logging.warning("arXiv enrichment failed: %s", e)
    out = []
    for it in items:
        meta = _CACHE.get(it.get("id", ""), {})
        abstract = max(str(it.get("abstract") or it.get("summary") or ""), meta.get("abstract", ""), key=len)
        out.append({"id": it.get("id", ""), "title": meta.get("title") or str(it.get("title", "")),
                    "abstract": abstract, "authors": meta.get("authors") or it.get("authors") or [],
                    "published": meta.get("published") or str(it.get("published") or it.get("year") or "")})
    return out


def _authors(a) -> str:
    a = [x for x in (a if isinstance(a, list) else re.split(r",| and ", str(a))) if str(x).strip()]
    if not a:
        return "Unknown"
    return f"{a[0]} et al." if len(a) > 2 else " & ".join(a)


def _year(p: str) -> str:
    m = re.search(r"(19|20)\d{2}", p or "")
    return m.group(0) if m else "n.d."


def _reference(n: int, p: dict) -> str:
    return f"[{n}] {_authors(p['authors'])} ({_year(p['published'])}). {p['title']}. arXiv:{p['id']} - https://arxiv.org/abs/{p['id']}"


# ---------- tools ----------
@mcp.tool()
def rank_papers(topic: str, papers: str | list[str | dict] | dict, top_k: int = 3, recency_weight: float = 0.3) -> RankResult:
    """Rank candidate papers for a topic and keep the best top_k (decision step).

    topic: the research topic, e.g. "LoRA fine-tuning of LLMs".
    papers: the JSON returned by arxiv search_papers, OR simply a list of arXiv ids
            (e.g. '["2310.08659", "2502.01378"]'): missing titles/abstracts are fetched from the arXiv API.
    top_k: how many papers to keep (1-10).
    recency_weight: 0 = relevance only, 1 = newest first (default 0.3).
    Returns the ranked papers with score, relevance, recency and a reason, plus the suggested next step.
    """
    items = _parse(papers if isinstance(papers, str) else json.dumps(papers))
    if not items:
        raise ValueError("No papers found in 'papers'. Pass the JSON from arxiv search_papers or a list of arXiv ids.")
    seen, uniq = set(), []
    for it in items:
        key = it.get("id") or str(it.get("title", "")).lower()
        if key and key not in seen:
            seen.add(key)
            uniq.append(it)
    docs = [p for p in _complete(uniq) if p["title"] or p["abstract"]]
    if not docs:
        raise ValueError("Could not get any title/abstract for these ids (arXiv API unreachable?). "
                         "Pass the full JSON returned by arxiv search_papers instead.")

    q = _topic_terms(topic)
    toks = [_tokens(p["title"]) * 2 + _tokens(p["abstract"]) for p in docs]   # title counts double
    avg = sum(map(len, toks)) / len(toks) or 1
    df = {t: sum(t in set(d) for d in toks) for t in q}
    raw = []
    for d in toks:
        s = 0.0
        for t in q:
            tf = d.count(t)
            idf = math.log(1 + (len(toks) - df[t] + 0.5) / (df[t] + 0.5))
            s += idf * tf * 2.2 / (tf + 1.2 * (0.25 + 0.75 * len(d) / avg)) if tf else 0
        raw.append(s)
    w = min(max(recency_weight, 0.0), 1.0)
    this_year = date.today().year
    scored, off_topic = [], 0
    for p, r, d in zip(docs, raw, toks):
        matched = sorted(t for t in q if t in d)
        coverage = len(matched) / len(q)
        if coverage < MIN_COVERAGE:   # opinionated: never recommend an off-topic paper, even if it is the "best" one
            off_topic += 1
            continue
        y = _year(p["published"])
        rec = 0.5 ** ((this_year - int(y)) / 2) if y != "n.d." else 0.0
        scored.append([0.0, r, round(rec, 3), p, y, matched, round(coverage, 2)])
    top = max((x[1] for x in scored), default=0) or 1
    for x in scored:
        x[1] = round(x[1] / top, 3)
        x[0] = round((1 - w) * x[1] + w * x[2], 3)
    scored.sort(key=lambda x: x[0], reverse=True)
    k = min(max(int(top_k), 1), 10)
    ranked = [RankedPaper(rank=i, id=p["id"], title=p["title"], authors=_authors(p["authors"]), year=y,
                          score=sc, relevance=rel, recency=rec, coverage=cov,
                          why=f"matches {', '.join(matched[:5])} ({cov:.0%} of topic terms); {y}")
              for i, (sc, rel, rec, p, y, matched, cov) in enumerate(scored[:k], 1)]
    logging.info("rank_papers: %d candidates, %d off-topic -> top %d", len(docs), off_topic, len(ranked))
    if len(ranked) < k:   # tell the planner what to do instead of silently returning weak papers
        nxt = (f"only {len(ranked)} on-topic paper(s) out of {len(docs)}: call arxiv search_papers again with a more "
               "specific query, sort_by='relevance' and more max_results, then call rank_papers again "
               "(you may pass all ids together)." + (f" Or continue with {[p.id for p in ranked]}." if ranked else ""))
    else:
        nxt = f"call extract_findings with topic and paper_ids={json.dumps([p.id for p in ranked])}"
    return RankResult(topic=topic, considered=len(docs), duplicates_removed=len(items) - len(uniq),
                      off_topic_removed=off_topic, ranked=ranked, next_step=nxt)


@mcp.tool()
def extract_findings(topic: str, paper_ids: list[str] | str, per_paper: int = 1) -> FindingsResult:
    """Extract the key result sentence(s) of each paper and build a cited Markdown brief (transformation step).

    topic: the research topic (used to pick topic-relevant sentences and as the brief title).
    paper_ids: arXiv ids in the order they should be cited, e.g. the ids returned by rank_papers.
    per_paper: sentences to keep per paper (1-3).
    Returns findings quoted verbatim from the abstracts with [n] citations, the numbered references,
    and brief_markdown: a complete brief to save as-is with the filesystem write_file tool.
    """
    ids = [it["id"] for it in _parse(paper_ids if isinstance(paper_ids, str) else json.dumps(paper_ids))
           if ARXIV_ID.fullmatch(it.get("id", ""))]
    if not ids:
        raise ValueError("paper_ids must contain arXiv ids such as '2310.08659'.")
    papers = _complete([{"id": i} for i in dict.fromkeys(ids)])
    q = _topic_terms(topic)
    k = min(max(int(per_paper), 1), 3)
    findings, refs, missing = [], [], []
    for p in papers:
        if not p["abstract"]:
            missing.append(p["id"])
            continue
        n = len(refs) + 1
        refs.append(_reference(n, p))
        sents = [s.strip() for s in re.split(r"(?<=[.!?])\s+(?=[A-Z])", p["abstract"]) if 40 <= len(s.strip()) <= 400]

        def score(s, i):
            return (2.0 * len(RESULT_CUES.findall(s)) + 1.0 * len(q & set(_tokens(s)))
                    + (0.5 if i >= len(sents) / 2 else 0))   # results are usually stated late in an abstract
        best = sorted(range(len(sents)), key=lambda i: score(sents[i], i), reverse=True)[:k]
        findings += [Finding(cite=n, paper_id=p["id"], text=sents[i]) for i in sorted(best)]
    if not findings:
        raise ValueError(f"No abstract available for {ids}. Check the ids or run arxiv search_papers again.")

    lead = papers[[p["id"] for p in papers].index(findings[0].paper_id)]
    first = re.split(r"(?<=[.!?])\s+", lead["abstract"])[0]
    summary = (f"This brief covers {len(refs)} arXiv paper(s) on {topic}. "
               f"The top-ranked one, \"{lead['title']}\" [1], frames the problem as follows: {first}")
    md = (f"# Research brief: {topic}\n\n_Generated {datetime.now():%Y-%m-%d} by the Research Notebook agent "
          f"(findings are quoted from the abstracts)._\n\n## Summary\n{summary}\n\n## Key findings\n"
          + "\n".join(f"- {f.text} [{f.cite}]" for f in findings)
          + "\n\n## References\n" + "\n".join(refs) + "\n")
    logging.info("extract_findings: %d papers -> %d findings (%d missing)", len(papers), len(findings), len(missing))
    return FindingsResult(topic=topic, findings=findings, references=refs, missing_ids=missing, brief_markdown=md,
                          next_step="save brief_markdown unchanged with filesystem write_file")


if __name__ == "__main__":
    mcp.run()
