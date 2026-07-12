# 🛠 AI Engineering Playbook

**How to get the most from AI in software engineering** — concrete, tested moves for cutting cost, shipping faster, and keeping output trustworthy. Grounded in current best practices and real practitioner reports from this week's HN threads.

## Cut token usage (and cost)

- **Turn on prompt caching** — Anthropic caching bills cached input at ~0.1x (a 90% discount) and now auto-caches multi-turn chats. Biggest single lever for repeated context. [Token Optimize](https://www.tokenoptimize.dev/guides/llm-token-optimization-strategies)
- **Compact mid-session** — use summarize/compaction so the context window doesn't grow unbounded; a long session gets squeezed into a compact recap. [Redis](https://redis.io/blog/llm-token-optimization-speed-up-apps/)
- **Persist memory across sessions** — curated memory turns a 50K-token reload into a few hundred tokens. Have the agent maintain its own `plan.md`/docs so it isn't reliant on one session's context. [Token Optimize](https://www.tokenoptimize.dev/guides/context-engineering-reduce-token-usage)
- **Compress & mask tool output** — logs, files, and RAG chunks compress 60–95% before hitting the model; mask irrelevant tool results instead of pasting them whole. [CoddyKit](https://www.coddykit.com/pages/blog-detail?id=512865&slug=how-to-cut-llm-token-usage-by-90-with-context-compression-a-step-by-step-guide)
- **Retrieve, don't pack** — fetch only relevant chunks on demand from a vector store rather than stuffing the whole history in the prompt. [LogRocket](https://blog.logrocket.com/stop-wasting-ai-tokens-10-ways-to-reduce-usage/)
- **Compile fuzzy calls into local functions** — for repeated LLM-API tasks (parse logs, repair JSON, rank by intent), compile the spec into a local "fuzzy function" to reclaim locality, reproducibility, and price. [Program-as-Weights](https://arxiv.org/abs/2607.02512)
- **Minify agent state** — state-in-context agents shrink dramatically with minification/context-pruning. [Minification](https://arxiv.org/pdf/2606.01326) · [Context Pruning](https://arxiv.org/pdf/2605.15315)

## Speed up feature development

- **Plan before you code** — collapse ~20 ambiguous decisions into one reviewed spec so each lands near 100% instead of 80%. The cheapest speed-up there is. [Claude Code Docs](https://code.claude.com/docs/en/best-practices)
- **Delegate to subagents** — a subagent explores in its own context and reports back a compressed summary, keeping the main session clean and fast (great for large read/exploration tasks). [SmartScope](https://smartscope.blog/en/generative-ai/claude/claude-code-best-practices-advanced-2026/)
- **Chain the SDLC as skills** — brainstorm → worktree → implementation plan → subagent execution → TDD → review-before-merge (e.g., the "Superpowers" collection). [duet.so](https://duet.so/guides/claude-code-skills-complete-guide)
- **Enforce TDD with hooks** — a deterministic red-green-refactor loop (write failing test → watch it fail → make it pass) via hooks/state machine yields regression-proof code; one HN dev built a 300k-line SaaS this way. [HN](https://news.ycombinator.com/item?id=48413629)
- **Use a second model as reviewer** — several devs run Codex to review Claude Code output (or vice-versa) as a cheap quality gate. [HN](https://news.ycombinator.com/item?id=48413629)

## Skills to add to a project (and how to manage them)

- **Check skills into the repo** — keep them under `.agents/skills/`, versioned and reviewed via PR, so every contributor inherits the project's conventions automatically. [Developers Digest](https://www.developersdigest.tech/blog/best-claude-code-skills-2026)
- **Keep 8–12, audit monthly** — that covers most of a senior dev's day; beyond that you pay a "context tax." Delete any skill you haven't triggered in 30 days. [SmartScope](https://smartscope.blog/en/generative-ai/claude/claude-code-best-practices-advanced-2026/)
- **Right tool for the job** — *Skills* = how to do something; *MCP* = access to external systems; *Subagents* = delegate to a specialist with its own context. [duet.so](https://duet.so/guides/claude-code-skills-complete-guide)
- **High-ROI starter skills:** branch/PR review, test generation, CI/CD setup, spec-driven scaffolding, incident triage, changelog/release notes, and a repo-conventions linter.

## Keep AI output trustworthy

- **Treat the agent as a fallible teammate** — extensive unit/automation tests, static analysis (e.g., SonarQube), and CI gates on everything merged to main. [HN](https://news.ycombinator.com/item?id=48445024)
- **Guard the review surface** — autonomous agents that ship code across many PRs are a real attack surface (a payload can be timed across commits); keep human review and CI gating tight. [Distributed Attacks in Persistent-State AI Control](https://arxiv.org/abs/2607.02514)
- **Prefer deterministic scripts** — for repeatable ops (deploys, scaffolding), have the agent run pre-built scripts instead of improvising API calls, so results are consistent every time. [HN](https://news.ycombinator.com/item?id=48445024)

## Manage context

- **Rules close to the repo** — put project rules where the code lives; keep prompts short and task-specific rather than "heroic" mega-prompts. [HN](https://news.ycombinator.com/item?id=48445024)
- **Watch for context bloat** — too much in context degrades output; lean context beats a kitchen-sink of skills/MCPs. [HN](https://news.ycombinator.com/item?id=48413629)

## Anti-patterns to avoid

- **Vibe coding without the rest of the software** — code isn't the whole product; skipping docs, tests, and design catches up fast.
- **Skill hoarding** — untriggered skills/MCPs just tax your context window.
- **Skim reviews** — pattern-skimming misses duplication, bloat, and inconsistent naming that quietly drain productivity.
- **Burning tokens on non-AI work** — if a plain shell script does the job, automate it without the model.

---
*Sources: current best-practice guides + practitioner reports from this week's Hacker News threads and arXiv papers in your digest.*
