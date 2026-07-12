#!/usr/bin/env python3
"""
collect.py — weekly source scanner for the "How AI you doing?" podcast.

Scans arXiv, GitHub, Hacker News, and a curated list of engineering blogs
for items from the past N days, then writes a versioned digest to data/.

No API keys required. (GitHub search works unauthenticated but is rate-limited;
inside GitHub Actions the GITHUB_TOKEN env var is used automatically.)

Outputs:
    data/digest-YYYY-MM-DD.json   one file per run (the archive)
    data/latest.json              a copy of the most recent run
    data/index.json               list of all digests, newest first
"""

import datetime as dt
import html as _html
import json
import os
import re
import sys
import time
from pathlib import Path
from urllib.parse import quote
from xml.etree import ElementTree as ET

import requests
import yaml

ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT / "data"
CONFIG_PATH = ROOT / "sources.yml"
USER_AGENT = "how-ai-are-doing-bot/1.0 (+https://github.com)"
TIMEOUT = 30


# --------------------------------------------------------------------------- #
# helpers
# --------------------------------------------------------------------------- #
def load_config() -> dict:
    with open(CONFIG_PATH, "r", encoding="utf-8") as fh:
        return yaml.safe_load(fh)


def http_get(url: str, headers: dict | None = None, params: dict | None = None):
    h = {"User-Agent": USER_AGENT}
    if headers:
        h.update(headers)
    return requests.get(url, headers=h, params=params, timeout=TIMEOUT)


def clean(text: str, limit: int = 400) -> str:
    if not text:
        return ""
    text = re.sub(r"<[^>]+>", " ", text)          # strip HTML tags
    text = re.sub(r"\s+", " ", text).strip()
    return text[:limit] + ("…" if len(text) > limit else "")


def within_window(published: dt.datetime, days: int) -> bool:
    cutoff = dt.datetime.now(dt.timezone.utc) - dt.timedelta(days=days)
    if published.tzinfo is None:
        published = published.replace(tzinfo=dt.timezone.utc)
    return published >= cutoff


def parse_date(value: str) -> dt.datetime | None:
    if not value:
        return None
    fmts = [
        "%Y-%m-%dT%H:%M:%SZ",
        "%Y-%m-%dT%H:%M:%S%z",
        "%a, %d %b %Y %H:%M:%S %z",
        "%a, %d %b %Y %H:%M:%S %Z",
        "%Y-%m-%dT%H:%M:%S.%fZ",
    ]
    for fmt in fmts:
        try:
            return dt.datetime.strptime(value, fmt)
        except ValueError:
            continue
    return None


# --------------------------------------------------------------------------- #
# source: arXiv
# --------------------------------------------------------------------------- #
def fetch_arxiv(cfg: dict, days: int) -> list[dict]:
    cats = cfg.get("arxiv_categories", ["cs.SE", "cs.DC", "cs.AI"])
    max_results = cfg.get("arxiv_max_results", 40)
    cat_query = "+OR+".join(f"cat:{c}" for c in cats)
    url = (
        "http://export.arxiv.org/api/query?"
        f"search_query={cat_query}"
        "&sortBy=submittedDate&sortOrder=descending"
        f"&max_results={max_results}"
    )
    items: list[dict] = []
    try:
        resp = http_get(url)
        resp.raise_for_status()
        ns = {"a": "http://www.w3.org/2005/Atom"}
        root = ET.fromstring(resp.text)
        for entry in root.findall("a:entry", ns):
            published = parse_date((entry.findtext("a:published", "", ns) or "").strip())
            if not published or not within_window(published, days):
                continue
            authors = [
                a.findtext("a:name", "", ns)
                for a in entry.findall("a:author", ns)
            ]
            items.append({
                "title": clean(entry.findtext("a:title", "", ns), 200),
                "url": (entry.findtext("a:id", "", ns) or "").strip(),
                "summary": clean(entry.findtext("a:summary", "", ns)),
                "authors": ", ".join(filter(None, authors[:4])),
                "published": published.date().isoformat(),
            })
    except Exception as exc:  # noqa: BLE001
        print(f"[arxiv] error: {exc}", file=sys.stderr)
    return items


# --------------------------------------------------------------------------- #
# source: GitHub (recently created, popular, keyword-matched)
# --------------------------------------------------------------------------- #
def fetch_github(cfg: dict, days: int) -> list[dict]:
    keywords = cfg.get("github_keywords", ["ai", "llm", "agent"])
    min_stars = cfg.get("github_min_stars", 50)
    since = (dt.date.today() - dt.timedelta(days=days)).isoformat()
    query = f"{' OR '.join(keywords)} created:>{since} stars:>{min_stars}"
    url = "https://api.github.com/search/repositories"
    params = {"q": query, "sort": "stars", "order": "desc", "per_page": 25}
    headers = {"Accept": "application/vnd.github+json"}
    token = os.environ.get("GITHUB_TOKEN")
    if token:
        headers["Authorization"] = f"Bearer {token}"
    items: list[dict] = []
    try:
        resp = http_get(url, headers=headers, params=params)
        resp.raise_for_status()
        for repo in resp.json().get("items", []):
            items.append({
                "title": repo.get("full_name", ""),
                "url": repo.get("html_url", ""),
                "summary": clean(repo.get("description", ""), 240),
                "stars": repo.get("stargazers_count", 0),
                "language": repo.get("language") or "—",
                "published": (repo.get("created_at", "") or "")[:10],
            })
    except Exception as exc:  # noqa: BLE001
        print(f"[github] error: {exc}", file=sys.stderr)
    return items


# --------------------------------------------------------------------------- #
# source: Hacker News (via Algolia API)
# --------------------------------------------------------------------------- #
def _hn_comment_text(raw: str, limit: int = 320) -> str:
    """Strip HTML tags + unescape entities from an HN comment."""
    if not raw:
        return ""
    txt = raw.replace("<p>", " ")
    txt = re.sub(r"<[^>]+>", " ", txt)
    txt = _html.unescape(txt)
    txt = re.sub(r"\s+", " ", txt).strip()
    return txt[:limit] + ("…" if len(txt) > limit else "")


def fetch_hn_comments(object_id: str, n: int) -> list[dict]:
    """Fetch the top-scoring comments for one HN story."""
    url = "https://hn.algolia.com/api/v1/search"
    params = {"tags": f"comment,story_{object_id}", "hitsPerPage": n}
    out: list[dict] = []
    try:
        resp = http_get(url, params=params)
        resp.raise_for_status()
        for hit in resp.json().get("hits", []):
            text = _hn_comment_text(hit.get("comment_text", ""))
            if len(text) < 40:            # skip one-liners / noise
                continue
            out.append({"author": hit.get("author", ""), "text": text})
    except Exception as exc:  # noqa: BLE001
        print(f"[hn-comments] error for {object_id}: {exc}", file=sys.stderr)
    return out[:n]


def fetch_hackernews(cfg: dict, days: int) -> list[dict]:
    # Discussion threads stay valuable longer than news, so HN uses its own window.
    window = int(cfg.get("hn_window_days", 30))
    min_points = cfg.get("hn_min_points", 60)
    queries = cfg.get("hn_keywords", ["AI", "LLM", "architecture", "engineering"])
    max_stories = int(cfg.get("hn_max_stories", 8))
    comments_per = int(cfg.get("hn_comments_per_story", 6))
    cutoff_ts = int((dt.datetime.now(dt.timezone.utc) -
                     dt.timedelta(days=window)).timestamp())
    seen: dict[str, dict] = {}
    for q in queries:
        url = "https://hn.algolia.com/api/v1/search"
        params = {
            "query": q,
            "tags": "story",
            "numericFilters": f"points>{min_points},created_at_i>{cutoff_ts}",
            "hitsPerPage": 20,
        }
        try:
            resp = http_get(url, params=params)
            resp.raise_for_status()
            for hit in resp.json().get("hits", []):
                oid = hit.get("objectID")
                if not oid or oid in seen:
                    continue
                seen[oid] = {
                    "title": clean(hit.get("title", ""), 200),
                    "url": hit.get("url") or f"https://news.ycombinator.com/item?id={oid}",
                    "summary": "",
                    "points": hit.get("points", 0),
                    "comments": hit.get("num_comments", 0),
                    "hn_url": f"https://news.ycombinator.com/item?id={oid}",
                    "published": (hit.get("created_at", "") or "")[:10],
                    "_oid": oid,
                }
        except Exception as exc:  # noqa: BLE001
            print(f"[hn] error for '{q}': {exc}", file=sys.stderr)
        time.sleep(0.3)  # be polite

    # keep the most-discussed stories, then pull their top comments
    stories = sorted(seen.values(), key=lambda x: x.get("comments", 0), reverse=True)[:max_stories]
    for s in stories:
        s["top_comments"] = fetch_hn_comments(s.pop("_oid"), comments_per)
        # discussion_summary is filled in later by the Cowork/scheduled task
        s["discussion_summary"] = ""
        time.sleep(0.3)
    return stories


# --------------------------------------------------------------------------- #
# source: engineering blogs (RSS / Atom)
# --------------------------------------------------------------------------- #
def fetch_blogs(cfg: dict, days: int) -> list[dict]:
    feeds = cfg.get("blog_feeds", [])
    items: list[dict] = []
    for feed in feeds:
        name = feed.get("name", "blog")
        url = feed.get("url")
        if not url:
            continue
        try:
            resp = http_get(url)
            resp.raise_for_status()
            root = ET.fromstring(resp.content)
            # RSS 2.0
            channel_items = root.findall(".//item")
            if channel_items:
                for it in channel_items:
                    published = parse_date((it.findtext("pubDate") or "").strip())
                    if published and not within_window(published, days):
                        continue
                    items.append({
                        "title": clean(it.findtext("title", ""), 200),
                        "url": (it.findtext("link") or "").strip(),
                        "summary": clean(it.findtext("description", "")),
                        "blog": name,
                        "published": published.date().isoformat() if published else "",
                    })
                continue
            # Atom
            ns = {"a": "http://www.w3.org/2005/Atom"}
            for entry in root.findall("a:entry", ns):
                published = parse_date(
                    (entry.findtext("a:updated", "", ns)
                     or entry.findtext("a:published", "", ns) or "").strip()
                )
                if published and not within_window(published, days):
                    continue
                link_el = entry.find("a:link", ns)
                link = link_el.get("href") if link_el is not None else ""
                items.append({
                    "title": clean(entry.findtext("a:title", "", ns), 200),
                    "url": link,
                    "summary": clean(entry.findtext("a:summary", "", ns)
                                     or entry.findtext("a:content", "", ns)),
                    "blog": name,
                    "published": published.date().isoformat() if published else "",
                })
        except Exception as exc:  # noqa: BLE001
            print(f"[blog:{name}] error: {exc}", file=sys.stderr)
    return items


# --------------------------------------------------------------------------- #
# main
# --------------------------------------------------------------------------- #
def main() -> None:
    cfg = load_config()
    days = int(cfg.get("window_days", 7))

    print(f"Collecting items from the past {days} days…")
    sources = {
        "arxiv": fetch_arxiv(cfg, days),
        "github": fetch_github(cfg, days),
        "hackernews": fetch_hackernews(cfg, days),
        "blogs": fetch_blogs(cfg, days),
    }

    # Tag every item with topic categories for the dashboard's desks.
    try:
        from tag_items import tags_for
        for src_key, arr in sources.items():
            for it in arr:
                extra = f"{it.get('summary','')} {it.get('discussion_summary','')}"
                it["tags"] = tags_for(it.get("title", ""), extra, src_key)
    except Exception as exc:  # noqa: BLE001
        print(f"[tag] skipped: {exc}", file=sys.stderr)

    now = dt.datetime.now(dt.timezone.utc)
    digest = {
        "generated_at": now.isoformat(),
        "week_of": now.date().isoformat(),
        "window_days": days,
        "counts": {k: len(v) for k, v in sources.items()},
        "sources": sources,
    }

    DATA_DIR.mkdir(parents=True, exist_ok=True)
    stamp = now.date().isoformat()
    digest_file = DATA_DIR / f"digest-{stamp}.json"
    with open(digest_file, "w", encoding="utf-8") as fh:
        json.dump(digest, fh, indent=2, ensure_ascii=False)
    with open(DATA_DIR / "latest.json", "w", encoding="utf-8") as fh:
        json.dump(digest, fh, indent=2, ensure_ascii=False)

    # maintain archive index
    archive = sorted(
        {p.name for p in DATA_DIR.glob("digest-*.json")},
        reverse=True,
    )
    index = [
        {"file": name, "week_of": name.replace("digest-", "").replace(".json", "")}
        for name in archive
    ]
    with open(DATA_DIR / "index.json", "w", encoding="utf-8") as fh:
        json.dump(index, fh, indent=2, ensure_ascii=False)

    total = sum(digest["counts"].values())
    print(f"Done. {total} items written to {digest_file.name}")
    print(f"Counts: {digest['counts']}")


if __name__ == "__main__":
    main()
