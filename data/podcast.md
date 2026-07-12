# ◇ Story Desk — This Week's Angles

Angles worth developing from this week's items — for a talk, a post, or a deep-dive. Each has a hook, an angle type, talking points, who to talk to, and a source. Biased toward retrieval, agents, and production reality.

## 1. Seconds → milliseconds: Netflix's Cassandra latency fix  *(War Story · LEAD)*
Hook: a classic read-latency nightmare at scale — and the partitioning change that fixed it.
- What caused seconds-long reads, and how they diagnosed it.
- The partition/data-model change and its trade-offs.
- What transfers to any large-index or vector store you run.
- When to fix the data model vs. throw hardware at it.
Who to talk to: an engineer who's run large stateful data stores. [InfoQ](https://www.infoq.com/news/2026/07/netflix-cassandra-partition/)

## 2. Memory that survives the session: semantic persistence for LLM workflows  *(Tool/Workflow)*
Hook: RAG isn't just retrieval — it's persisting *workflow knowledge* so agents don't start cold.
- "Workflow as Knowledge": what to persist and how to index it.
- Where hybrid/semantic retrieval helps vs. hurts in agent memory.
- Cost and staleness trade-offs of long-lived indexes.
Who to talk to: a retrieval/RAG practitioner (your wheelhouse). [arXiv](http://arxiv.org/abs/2607.08740v1)

## 3. Serving agents at scale: scheduling when every turn hits an LLM  *(War Story)*
Hook: agentic chat in production lives or dies on scheduling and tail latency.
- SMetric's session-centric scheduling for serving agents.
- Throughput vs. per-session fairness; what breaks under load.
- Guardrails for cost blowups when agents loop.
Who to talk to: an infra/serving engineer. [arXiv](http://arxiv.org/abs/2607.08565v1)

## 4. Postgres → ClickHouse: when your database stops keeping up  *(War Story)*
Hook: the honest version of a migration story — why they switched and what it cost.
- Signals it was time to move off Postgres.
- What ClickHouse bought them, and the sharp edges.
- How they de-risked the cutover.
Who to talk to: an engineer who's led a datastore migration. [InfoQ](https://www.infoq.com/news/2026/07/momentic-postgres-clickhouse/)

## 5. TDD with AI, for real: Datadog's test-driven production migration  *(Tool/Workflow)*
Hook: a concrete, reviewable way to use AI coding tools without "vibe coding" in prod.
- The test-first loop that kept the migration safe.
- Where human review stayed non-negotiable.
- What made it repeatable vs. a one-off.
Who to talk to: someone shipping AI-assisted migrations. [InfoQ](https://www.infoq.com/news/2026/07/datadog-ai-production-migration/)

## 6. Latency vs. cost: the multi-region architecture trade-off  *(Architecture)*
Hook: the decision every scaling team faces, laid out with the real trade-offs.
- What actually drives the latency/cost curve.
- Patterns that fail quietly at multi-region scale.
- A decision framework you can reuse Monday.
Who to talk to: an architect who's run multi-region systems. [InfoQ](https://www.infoq.com/articles/multi-region-latency-cost-tradeoffs/)

---
**Lead with #1** — a concrete, high-stakes latency war story hooks engineers instantly and frames the whole "production reality" theme. #2 and #3 are your retrieval/agents depth plays.
