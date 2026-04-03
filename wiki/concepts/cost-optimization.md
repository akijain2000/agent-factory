# Cost Optimization

## What it is

**Cost optimization** for agents reduces spend while preserving quality: managing **token usage** (prompt size, completion length), **model selection** (frontier vs economical tiers per subtask), **caching** (prompt or result caches with stable keys), **batching** (grouping similar requests), and **budgets** (per tenant, per session, per tool class). It pairs technical tactics with **observability** so savings are measurable, not guessed.

## Why it matters for agents

Loops multiply tokens: each tool round trip re-sends context. Unbounded history and verbose tools inflate bills and latency. Cost discipline keeps products viable at scale and prevents runaway spend from retries or runaway autonomy.

## How to implement it

1. **Measure first:** per-span token counts and $ estimates; tag by feature, customer, and model id.
2. **Right-size models:** route classification, summarization, or extraction to smaller models; reserve large models for planning or ambiguous reasoning. Validate with **offline eval** before broad rollout.
3. **Trim context:** summaries, retrieval caps, structured tool returns instead of prose dumps; avoid repeating static instructions—cache or prefix-cache where supported.
4. **Caching:** cache idempotent tool results and deterministic sub-queries; include schema version and args in keys; respect TTL and privacy (no cross-tenant cache bleed).
5. **Batching:** aggregate embeddings or independent scoring calls where APIs allow; avoid batching user-visible latency-sensitive paths without SLAs.
6. **Budgets:** hard caps on tokens, steps, and dollars per request; graceful degradation (shorter answer, escalate to human) when approaching limits.

## Model selection heuristic

Use cheap models for **high-volume, low-risk** subtasks with automatic validation (schema checks, unit tests on outputs). Use expensive models where error cost dominates API cost (legal, financial, safety-critical planning).

## Token usage tactics

Shorten **system** prompts by moving reference docs to retrieval. Collapse verbose tool outputs server-side before returning to the model. Prefer **structured** tool responses over narrative. Use **stop sequences** or max tokens where appropriate to prevent runaway completions on simple intents.

## Budgets and chargeback

Define **per-request**, **per-user**, and **per-org** limits. Expose remaining budget to the orchestrator so it can switch strategy (shorter plan, escalate to human). Attribute shared platform costs back to product lines using trace tags.

## Caching pitfalls to engineer around

Include **locale**, **model version**, and **tool schema hash** in cache keys when outputs might change. Invalidate on **knowledge base** updates if cached answers embed facts. For LLM response caches, respect **data use** policies—some contracts forbid caching certain inputs.

## Common mistakes

- Caching responses that embed user-specific PII without tenant-scoped keys.
- Aggressive summarization that drops safety constraints or tool rules.
- Optimizing average cost while tail latency or failure rate spikes.
- No kill switch when upstream pricing or usage anomalies occur.

## Quick checklist

- Token and dollar dashboards exist per feature **before** optimizing prompts.
- Routing to cheaper models is gated by **offline** parity checks.
- Cache keys include tenant, schema version, and locale where relevant.

## References to course modules

These map to the **23-module Agent Factory course** (see [`../../course/README.md`](../../course/README.md) when published).

- **Module 04 — Model Selection & Routing** — when to use which model.
- **Module 18 — Cost and Token Attribution** — measurement and chargeback.
- **Module 22 — Caching, Batching, and Context Pruning** — engineering levers.

Full curriculum index: [`../../course/README.md`](../../course/README.md) (when present).

## See also

- [Observability](observability.md)
- [Context Window Management](context-window-management.md)
- [Context Engineering](context-engineering.md)
- [Agent Evaluation](agent-evaluation.md)
- [Progressive Complexity](progressive-complexity.md)
