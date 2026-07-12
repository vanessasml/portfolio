#!/usr/bin/env python3
"""
build_dashboard.py — portfolio-repo build: inline the digest + curated sections
into dashboard.html, using the bundled dashboard.css (dark theme).

Reuses the page TEMPLATE from build_page.py but takes CSS from scripts/dashboard.css
(the site's index.html is the light homepage, so we can't read CSS from it here).
Run by the weekly GitHub Action after collect.py + tag_items.py.
"""
import json
from pathlib import Path

from build_page import TEMPLATE   # same HTML/JS shell as the local builder

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"


def read(p: Path) -> str:
    return p.read_text(encoding="utf-8") if p.exists() else ""


def main() -> None:
    digest = json.loads((DATA / "latest.json").read_text(encoding="utf-8"))
    docs = {
        "morning": read(DATA / "morning.md"),
        "strategy": read(DATA / "strategy.md"),
        "playbook": read(DATA / "recommendations.md"),
        "podcast": read(DATA / "podcast.md"),
    }
    css = read(Path(__file__).resolve().parent / "dashboard.css")
    payload = {"DIGEST": digest, "DOCS": docs, "WEEK": str(digest.get("week_of", ""))}
    page = TEMPLATE.replace("/*__CSS__*/", css).replace('"__DATA__"', json.dumps(payload, ensure_ascii=False))
    (ROOT / "dashboard.html").write_text(page, encoding="utf-8")
    total = sum(digest.get("counts", {}).values())
    print(f"Wrote dashboard.html ({total} items, week {payload['WEEK']}).")


if __name__ == "__main__":
    main()
