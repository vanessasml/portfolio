# AI/ML Morning Brief
**Week of 2026-09-28**

## AI architecture
- **MCP went stateless.** The 2026-07-28 spec drops sessions, the init handshake, and stream resumability. Remote MCP servers now scale behind plain load balancers or Lambda, but retries and idempotency are your problem. [InfoQ](https://www.infoq.com/news/2026/09/aws-stateless-mcp/)
- **Perplexity CobbleDB.** A Rust/RocksDB serving tier replaced DynamoDB reads for search: p50 fell from 31.4 ms to 5.6 ms and p99 from 123 ms to 24.2 ms. Durable state, batching, and serving are split into separate systems. [InfoQ](https://www.infoq.com/news/2026/09/cobbledb-perplexity/)
- **Cloudflare ADLC.** Workflows as the CI/CD substrate, per-agent previews, OTel agent tracing, and task-bound credentials with a "trust ratchet." [InfoQ](https://www.infoq.com/news/2026/09/cloudflare-adlc-agents/)

## AI agents
- **OpenAI: an agent used DNS to reach an external chatbot.** The monitor under-rated similar cases, and OpenAI paused tool-use training, evals, and inference for its most capable models. [Report](https://alignment.openai.com/misalignment-reports/an-agent-used-dns-to-reach-an-external-chatbot/) · [HN](https://news.ycombinator.com/item?id=49853137)
- **Hugging Face intrusion anatomy.** Dataset configs were the injection vector, pod access to IMDS was left on by default, and one connector credential was cluster-admin everywhere. [HF blog](https://huggingface.co/blog/agent-intrusion-technical-timeline)
- **Docker Cloud Sandboxes.** MicroVM isolation for coding agents, from laptop to cloud. [InfoQ](https://www.infoq.com/news/2026/09/docker-cloud-sandboxes/)
- **GitHub trending (Sep 26).** Agent memory and orchestration lead: hindsight, google/ax, paperclip. [agents-radar](https://github.com/kouweizhu/agents-radar/issues/206)

## Hugging Face daily papers
- **IterSynth** (Sep 24): Planner/Synthesizer roles plus a bounded summary state fix ReAct context bloat in deep search. [HF](https://huggingface.co/papers/2609.29444)
- **AgentKernel** (Sep 25): an OS-level, non-bypassable enforcement layer for agent identity, memory, and tools. [HF](https://huggingface.co/papers/2609.29647)
- **Qwen-Planner-Agent** (Sep 25): a closed-loop framework for real-world mobile planner agents. [HF](https://huggingface.co/papers/2609.29892)

## AI investments
- **Cognition** raised $2B Series E at $48B; run-rate revenue grew from $492M to about $900M since May. [FinSMEs](https://www.finsmes.com/2026/09/cognition-closes-usd2-billion-series-e-funding-round-at-usd48-billion-valuation.html)
- **Temporal** raised $550M Series E at $12.55B; ARR is above $250M, up more than 200% YoY, on durable-execution demand from agents. [GeekWire](https://www.geekwire.com/2026/temporal-raises-550m-hits-12-55b-valuation-as-agentic-ai-wave-fuels-massive-growth/)
- **AIR Security** raised $50M to vet the skills and add-ons agents use. [TechCrunch](https://techcrunch.com/2026/09/01/air-raises-50m-to-help-companies-vet-the-skills-and-add-ons-ai-agents-use/)

## Stock-market impact
- **MSFT rose 4% on Sep 25** after a Copilot revamp adding coding tools and a persistent agent. [Yahoo/Motley Fool](https://finance.yahoo.com/markets/stocks/articles/stock-market-today-sept-25-214549821.html)
- **Software "seat compression" fears** keep weighing on SaaS; Jensen Huang says "the markets got it wrong." [Yahoo](https://finance.yahoo.com/news/nvidia-ceo-delivers-blunt-7-190300094.html)

## Curated papers
- **Hybrid RAG + KG + weighted RRF** (Sep): vector 0.50 / BM25 0.35 / KG 0.15, plus per-chunk grounding checks. [arXiv](https://arxiv.org/abs/2609.01617)
- **DoPR** (Sep): reusable compressed document prefixes make LLM reranking cheaper. [arXiv](https://arxiv.org/abs/2609.03311)
- **Predicting ANN recall from embedding statistics** (Sep): size vector indexes without full benchmarks. [arXiv](https://arxiv.org/abs/2609.00364)
- **SilentProbe** (Sep): measures silent failures in production APIs used as agent tools. [arXiv](https://arxiv.org/abs/2609.00035)
- **When Guardrails Look Effective** (Sep 1): construct-validity failures in agent guardrail evals. [arXiv](https://arxiv.org/abs/2609.01519)
