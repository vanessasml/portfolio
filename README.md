# Personal site — Vanessa Lopes

A clean personal/portfolio site with a live **"How AI you doing?"** dashboard, hosted free on GitHub Pages.

```
portfolio-site/
├── index.html       # the site (hero, projects, this-week, writing, speaking, contact)
├── dashboard.html   # self-contained weekly dashboard (linked from the site)
└── README.md
```

## Before you publish — edit these
In `index.html`, search for `EDIT` and fill in:
- Your name (nav + footer), headline, and lead sentence.
- Real project links (OpenSearch toolkit, agent eval harness, etc.).
- Writing post links, MLCon talk titles/slides.
- Social links: GitHub, LinkedIn (email is already set to vsofiaml@gmail.com).

## Publish on GitHub Pages (public, free)

**Option A — personal site at `https://vanessasml.github.io/` (recommended):**
1. Create a public repo named exactly **`vanessasml.github.io`**.
2. Put the contents of this folder (index.html, dashboard.html) in the repo root.
   ```
   cd portfolio-site
   git init && git add . && git commit -m "Personal site"
   git branch -M main
   git remote add origin https://github.com/vanessasml/vanessasml.github.io.git
   git push -u origin main
   ```
3. Repo → Settings → Pages → Source: *Deploy from a branch* → Branch `main` / `/ (root)` → Save.
4. Live in ~1 minute at **`https://vanessasml.github.io/`** — dashboard at **`/dashboard.html`**.

**Option B — project repo:** name it anything (e.g. `site`), push, enable Pages → served at `https://vanessasml.github.io/site/`.

## Keeping the dashboard fresh
`dashboard.html` is a copy of `how-ai-you-doing-week.html` from your ai-work folder. Each week, after the Monday build, copy the new file over and push:
```
cp ../how-ai-you-doing-week.html dashboard.html && git commit -am "Weekly update" && git push
```
(Or add a GitHub Action to automate the copy + commit.)

Once the site is live, send me your Pages URL and I'll drop the real link into the weekly email draft and the automated Monday email.
