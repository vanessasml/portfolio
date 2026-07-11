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

Hosted as its own repo so your existing pages stay untouched — served at
**`https://vanessasml.github.io/portfolio/`**.

1. On GitHub, create a new **public** repo named **`portfolio`** — do NOT add a README (an auto-README causes push conflicts).
2. From this folder, point at the new repo and push:
   ```
   cd portfolio-site
   git init                                   # skip if already a repo
   git add . && git commit -m "Portfolio site"
   git branch -M main
   git remote set-url origin https://github.com/vanessasml/portfolio.git  # or 'git remote add origin ...' if none
   git push -u origin main
   ```
3. Repo → Settings → Pages → Source: *Deploy from a branch* → Branch `main` / `/ (root)` → Save.
4. Live in ~1 minute at **`https://vanessasml.github.io/portfolio/`** — dashboard at **`/portfolio/dashboard.html`**.

> If the push is rejected ("remote contains work…"), the repo wasn't empty. Either recreate it without a README, or run `git pull origin main --allow-unrelated-histories` then push.

## Keeping the dashboard fresh
`dashboard.html` is a copy of `how-ai-you-doing-week.html` from your ai-work folder. Each week, after the Monday build, copy the new file over and push:
```
cp ../how-ai-you-doing-week.html dashboard.html && git commit -am "Weekly update" && git push
```
(Or add a GitHub Action to automate the copy + commit.)

Once the site is live, send me your Pages URL and I'll drop the real link into the weekly email draft and the automated Monday email.
