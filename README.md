# Personal site

A static personal site with a live weekly AI-engineering dashboard, hosted on GitHub Pages.

## Structure

```
├── index.html        # the site
├── dashboard.html    # self-contained weekly dashboard
├── writing/          # article pages
└── README.md
```

## Publish (GitHub Pages)

1. Create a public repo named `portfolio` (do **not** add a README — an auto-README causes push conflicts).
2. Push this folder:
   ```
   git init
   git add . && git commit -m "site"
   git branch -M main
   git remote add origin https://github.com/<you>/portfolio.git
   git push -u origin main
   ```
3. Settings → Pages → *Deploy from a branch* → `main` / `/ (root)`.
   Live at `https://<you>.github.io/portfolio/`.

> Push rejected ("remote contains work…")? The repo wasn't empty — recreate it without a README, or run `git pull origin main --allow-unrelated-histories` then push.

## Updating the dashboard

Replace `dashboard.html` with the newest build and push. (A GitHub Action can automate this.)
