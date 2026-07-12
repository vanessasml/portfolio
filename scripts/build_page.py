#!/usr/bin/env python3
"""
build_page.py — bake the tagged digest + Morning Brief + Strategy + Playbook +
Story Desk into ONE self-contained HTML file (how-ai-you-doing-week.html).

No server, no internet: data is inlined, so it opens on any phone/desktop and can
be emailed or AirDropped. CSS is read from index.html so it always matches the live
dashboard. Run scripts/tag_items.py first so the topic desks are populated.
"""
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"


def read_text(p: Path) -> str:
    return p.read_text(encoding="utf-8") if p.exists() else ""


def main() -> None:
    digest = json.loads((DATA / "latest.json").read_text(encoding="utf-8"))
    docs = {
        "morning": read_text(DATA / "morning.md"),
        "strategy": read_text(DATA / "strategy.md"),
        "playbook": read_text(DATA / "recommendations.md"),
        "podcast": read_text(DATA / "podcast.md"),
    }
    index_html = read_text(ROOT / "index.html")
    m = re.search(r"<style>([\s\S]*?)</style>", index_html)
    css = m.group(1) if m else ""

    payload = {"DIGEST": digest, "DOCS": docs, "WEEK": str(digest.get("week_of", ""))}
    page = TEMPLATE.replace("/*__CSS__*/", css).replace('"__DATA__"', json.dumps(payload, ensure_ascii=False))
    out = ROOT / "how-ai-you-doing-week.html"
    out.write_text(page, encoding="utf-8")
    total = sum(digest.get("counts", {}).values())
    print(f"Wrote {out.name} ({out.stat().st_size} bytes, {total} items, week {payload['WEEK']}).")


TEMPLATE = r"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8" />
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover" />
<title>How AI you doing? — Weekly</title>
<style>/*__CSS__*/</style>
</head>
<body>
<div class="wrap">
  <header class="top">
    <div class="eyebrow">This week in AI</div>
    <h1>HOW AI YOU DOING?</h1>
    <div class="sub">A weekly debrief — retrieval, agents, and production war stories, plus a morning brief and strategy signals. <b id="weeklabel"></b></div>
  </header>
  <div class="tabs" id="tabs"></div>
  <main id="content"><div class="empty">Loading…</div></main>
  <footer>Self-contained weekly edition · <span class="mono">How AI you doing?</span></footer>
</div>
<script>
const BUNDLE = "__DATA__";
const DIGEST = BUNDLE.DIGEST, DOCS = BUNDLE.DOCS;
const VIEWS = [
  { key: "morning",   label: "◉ Morning Brief",    type: "md",   doc: "morning" },
  { key: "retrieval", label: "⌕ Retrieval Desk",   type: "desk", tag: "retrieval" },
  { key: "agents",    label: "⛓ Agents in Prod",   type: "desk", tag: "agents" },
  { key: "warstory",  label: "⚠ War Stories",      type: "desk", tag: "warstory" },
  { key: "strategy",  label: "↗ Strategy Signals", type: "md",   doc: "strategy" },
  { key: "playbook",  label: "⚙ Playbook",         type: "md",   doc: "playbook" },
  { key: "podcast",   label: "◇ Story Desk",       type: "md",   doc: "podcast" },
];
const SRC_LABEL = { arxiv: "arXiv", blogs: "Blog", github: "GitHub", hackernews: "HN" };
let tab = "morning";
const esc = s => (s || "").replace(/[&<>]/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;' }[c]));

function itemsByTag(tag) {
  const src = DIGEST.sources || {}; const out = [];
  for (const k of Object.keys(src)) for (const it of (src[k] || [])) if ((it.tags || []).includes(tag)) out.push({ it, src: k });
  return out;
}
function tabButton(v, count) {
  const div = document.createElement("div");
  div.className = "tab" + (v.key === tab ? " active" : "");
  div.innerHTML = v.label + (count != null ? ` <span class="count">${count}</span>` : "");
  div.onclick = () => { tab = v.key; renderTabs(); renderItems(); };
  return div;
}
function renderTabs() {
  const el = document.getElementById("tabs"); el.innerHTML = "";
  for (const v of VIEWS) {
    if (v.type === "desk") { const c = itemsByTag(v.tag).length; if (!c) continue; el.appendChild(tabButton(v, c)); }
    else el.appendChild(tabButton(v, null));
  }
}
function mdToHtml(md) {
  const lines = (md || "").replace(/\r/g, "").split("\n"); let html = "", inList = false;
  const inline = s => esc(s).replace(/\*\*(.+?)\*\*/g, "<strong>$1</strong>")
    .replace(/\[([^\]]+)\]\(([^)]+)\)/g, '<a href="$2" target="_blank" rel="noopener">$1</a>')
    .replace(/\*(.+?)\*/g, "<em>$1</em>");
  const cl = () => { if (inList) { html += "</ul>"; inList = false; } };
  for (const raw of lines) { const line = raw.trimEnd();
    if (/^#{1,6}\s/.test(line)) { cl(); const lvl = line.match(/^#+/)[0].length; html += `<h${lvl} class="md-h">${inline(line.replace(/^#+\s/, ""))}</h${lvl}>`; }
    else if (/^---+$/.test(line)) { cl(); html += "<hr>"; }
    else if (/^[-*]\s/.test(line)) { if (!inList) { html += '<ul class="md-ul">'; inList = true; } html += `<li>${inline(line.replace(/^[-*]\s/, ""))}</li>`; }
    else if (line === "") { cl(); } else { cl(); html += `<p class="md-p">${inline(line)}</p>`; } }
  cl(); return html;
}
function badge(t) { return `<span class="badge">${esc(String(t))}</span>`; }
function deskCard(it, srcKey) {
  const title = `<a class="title" href="${esc(it.url)}" target="_blank" rel="noopener">${esc(it.title)}</a>`;
  let meta = [`<span class="badge src">${esc(SRC_LABEL[srcKey] || srcKey)}</span>`];
  if (srcKey === "arxiv")  meta.push(badge(it.authors || "—"), badge(it.published));
  if (srcKey === "blogs")  meta.push(badge(it.blog || "blog"), badge(it.published || ""));
  if (srcKey === "github") meta.push(badge("★ " + (it.stars ?? 0)), badge(it.language || "—"));
  let extra = "";
  if (srcKey === "hackernews") {
    meta.push(badge((it.comments ?? 0) + " comments"), `<a class="badge" href="${esc(it.hn_url)}" target="_blank" rel="noopener">HN thread</a>`);
    if (it.discussion_summary) {
      const quotes = (it.top_comments || []).map(c => `<div class="quote">“${esc(c.text)}”<span class="who"> — ${esc(c.author)}</span></div>`).join("");
      extra = `<div class="disc"><div class="disc-h">💬 What people are saying</div><div class="disc-body">${esc(it.discussion_summary)}</div>${quotes}</div>`;
    }
  }
  const summary = it.summary ? `<div class="summary">${esc(it.summary)}</div>` : "";
  return `<div class="card">${title}${summary}${extra}<div class="meta">${meta.join("")}</div></div>`;
}
function renderItems() {
  const root = document.getElementById("content");
  const view = VIEWS.find(v => v.key === tab) || VIEWS[0];
  if (view.type === "md") {
    const md = DOCS[view.doc];
    root.innerHTML = md ? `<div class="brief">${mdToHtml(md)}</div>` : `<div class="empty">Not in this edition.</div>`;
    return;
  }
  const rows = itemsByTag(view.tag);
  root.innerHTML = rows.length ? rows.map(r => deskCard(r.it, r.src)).join("") : `<div class="empty">No items on this desk this week.</div>`;
}
document.getElementById("weeklabel").textContent = BUNDLE.WEEK ? "Week of " + BUNDLE.WEEK : "";
renderTabs(); renderItems();
</script>
</body>
</html>
"""

if __name__ == "__main__":
    main()
