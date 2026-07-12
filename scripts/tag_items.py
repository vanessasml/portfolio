#!/usr/bin/env python3
"""
tag_items.py — assign topic tags to digest items for the dashboard desks.

Precision over recall: a desk should only contain items that genuinely belong,
and it's fine for a desk to be empty (the dashboard hides empty desks).

Desks
-----
retrieval : search / RAG / vector / OpenSearch work (any source).
agents    : agentic systems *with a production angle* — from blogs/HN freely,
            from arXiv only when it also signals production/serving/deployment.
warstory  : real experience reports — postmortems, incidents, "how we built/
            scaled/broke X", migrations. Engineering blogs + Hacker News only
            (research papers are not war stories).

Re-run anytime; idempotent.
"""
import json
from pathlib import Path

DATA = Path(__file__).resolve().parent.parent / "data"

RETRIEVAL = [
    "retrieval", "rag ", " rag", "retrieval-augmented", "vector search",
    "vector database", "vector db", "re-rank", "rerank", "reranking",
    "opensearch", "elasticsearch", "lucene", "semantic search", "hybrid search",
    "bm25", "dense retrieval", "nearest neighbor", "approximate nearest",
    "knn", "ann index", "faiss", "similarity search", "retriever",
]

AGENT_TERMS = [
    "agent", "agentic", "tool use", "tool-use", "function calling",
    "multi-agent", "agent orchestration", "llm agent", "mcp server", " mcp ",
]
# An arXiv item joins the agents desk only if it ALSO carries a production signal.
PROD_SIGNAL = [
    "production", "deploy", "serving", "in prod", "real-world", "real world",
    "enterprise", "incident", "latency", "throughput", "guardrail",
    "at scale", "reliab", "sla", "on-call",
]

WARSTORY = [
    "outage", "postmortem", "post-mortem", "incident", "root cause",
    "lessons", "how we", "what we learned", "retrospective", "migrat",
    "cut latency", "reduced latency", "reduced", "scaling", "scaled",
    "downtime", "rollback", "failure", "broke", "reliability", "at scale",
    "milliseconds", "what worked", "what failed", "we built", "we moved",
]


def tags_for(title: str, summary: str, source: str) -> list[str]:
    text = f"{title} {summary}".lower()
    tags = []

    if any(k in text for k in RETRIEVAL):
        tags.append("retrieval")

    has_agent = any(k in text for k in AGENT_TERMS)
    if has_agent and (source in ("blogs", "hackernews") or any(k in text for k in PROD_SIGNAL)):
        tags.append("agents")

    if source in ("blogs", "hackernews") and any(k in text for k in WARSTORY):
        tags.append("warstory")

    return tags


def tag_file(path: Path) -> dict:
    d = json.loads(path.read_text(encoding="utf-8"))
    counts = {"retrieval": 0, "agents": 0, "warstory": 0}
    for source, arr in d.get("sources", {}).items():
        for it in arr:
            extra = f"{it.get('summary','')} {it.get('discussion_summary','')}"
            it["tags"] = tags_for(it.get("title", ""), extra, source)
            for tg in it["tags"]:
                counts[tg] += 1
    path.write_text(json.dumps(d, indent=2, ensure_ascii=False), encoding="utf-8")
    return counts


if __name__ == "__main__":
    for p in sorted(DATA.glob("digest-*.json")) + [DATA / "latest.json"]:
        if p.exists():
            print(f"{p.name}: {tag_file(p)}")
