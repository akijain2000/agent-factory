# Cost Analysis: The Economics of Running Agents

Agent economics are dominated by **token volume**, **model tier**, **tool latency**, and **retry behavior**. Treat cost as a **first-class SLO**: measure per-task distributions, not averages alone.

## Token drivers

Long system prompts, retrieved context, and **multi-turn self-dialog** inflate input tokens. **Output tokens** grow with chain-of-thought-style verbosity. **Caching** (prompt prefix caching where supported) can slash repeated system+tool-schema costs—ROI is highest for **stable** prefixes.

## Model selection impact

Using a frontier model for **triage** is a common anti-pattern. Route **classification, summarization, and formatting** to smaller models; reserve large models for **integration** under uncertainty. The savings compound across high-QPS agents.

## Per-task cost distributions

Report **p50/p95** cost per successful task and per **failure**. Agents with weak stop policies have **fat tails**—a few runs dominate spend. **Step caps** and **duplicate-action detection** trim tails dramatically.

## Tool and infrastructure costs

HTTP tools, VM sandboxes, and browser daemons add **compute** and **egress** charges orthogonal to LLM bills. Parallel fan-out improves wall-clock but can **multiply** tool spend; gate parallelism with **budgets**.

## Framework comparison (economic lens)

Heavier frameworks do not inherently cost more—**topology** does. Multi-agent chat without termination can exceed single-agent graphs. **Graph-based** workflows with explicit merge points often **predict** cost better than emergent dialog.

## Caching ROI

Cache **embeddings** for static corpora, **tool results** where safe (respect freshness), and **prompt prefixes** for stable instructions. Invalidate on **schema** or **policy** changes—stale cache equals subtle quality drift.

## Governance metrics

Finance and procurement teams need **per-tenant** cost attribution: correlate spend to **features** (which skill, which tool). This requires **trace-level** accounting, not monthly invoice totals.

## Sensitivity: a toy scenario

Consider a support bot handling **50k** tickets monthly. Cutting average **output tokens** per resolution by **30%** via summarization discipline may dominate savings versus swapping a mid-tier model for a smaller one—especially if input context (KB + history) is the bulk spend. Conversely, a coding agent with **unbounded** self-dialog can erase model savings in a handful of **runaway** sessions. **Tail risk** management (hard caps) often beats incremental per-token tuning.

## Hidden costs beyond tokens

**Egress** from verbose logs, **embedding** recomputation on every doc tweak, and **duplicate retrieval** across retries inflate bills quietly. Instrument **per-stage** costs to find the true hotspots—often tool I/O, not the LLM.

## FinOps integration

Export daily **cost per feature flag** and **per skill** into existing FinOps dashboards. Finance teams model agents as **microservices** with variable COGS; without attribution, agents get blanket budget cuts that harm high-ROI workflows alongside runaway ones.

## Summary

Agent economics are **tail-heavy**: caps and backoff matter as much as model choice. Combine token discipline with **infra** telemetry and **per-tenant** attribution to avoid silent margin erosion.

## Sources and further reading

- Provider pricing pages (token tiers, caching policies).
- OpenAI/Anthropic docs on batching and caching features (as available).
- Internal dashboards combining LLM + infra spend.

## See also

- [Agent evaluation methods](agent-evaluation-methods.md)
- [Agent vs workflow](agent-vs-workflow.md)
- [Anti-patterns](anti-patterns.md)
- Concepts: [Cost Optimization](../concepts/cost-optimization.md), [Model Selection](../concepts/model-selection.md), [Observability](../concepts/observability.md), [Rate Limiting](../concepts/rate-limiting.md)
- Course: [Agent Factory course](../../course/README.md)
