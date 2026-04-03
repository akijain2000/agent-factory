# Observability

## What it is

**Observability** for agents means you can reconstruct *why* a run behaved as it did: inputs, model generations, tool calls, latencies, errors, costs, and user-visible outcomes. Primary mechanisms include **distributed tracing** (spans per step), **structured logging**, **decision logs** (which policy fired), and **cost attribution** (tokens and $ per tenant or feature). Products such as **LangSmith**, **Braintrust**, and vendor consoles provide trace UIs; self-hosted stacks often use OpenTelemetry plus a log store.

## Why it matters for agents

Multi-step runs fail in opaque ways: wrong tool, subtle prompt drift, or retry storms. Without traces, debugging is guesswork. Observability supports **SLOs**, **chargebacks**, **compliance audits**, and **evaluation** (export traces into offline replay). It also enables **on-call** playbooks: correlate incident reports with span ids.

## How to implement it

1. **One trace per user request** (or per scheduled job); child spans for each model call, tool invocation, retrieval, and human-approval wait.
2. **Stable identifiers:** `trace_id`, `span_id`, `tenant_id`, `agent_version`, `prompt_hash` (not raw prompts in logs by default).
3. **Log tool I/O summaries:** argument keys and hashes for large payloads; full bodies only in restricted stores with retention policies.
4. **Cost tracking:** record input/output tokens per span; aggregate by model id and route. Enforce **budgets** in the harness, not only in dashboards.
5. **Decision logging:** when guardrails or routers override the model, log rule id and reason code.
6. **Sampling:** 100% in dev; in prod, sample high-value or high-risk traffic fully and baseline the rest.

## What to log vs not log

**Log:** span names, durations, status, error classes, token counts, tool names, schema validation results, policy outcomes, correlation ids.

**Avoid in default logs:** raw PII, secrets, full prompts with customer data, unredacted third-party API keys, entire document bodies. Put sensitive detail in **tiered storage** with access controls and TTLs.

## LangSmith and Braintrust-style workflows

Export traces after incidents and annotate **root cause** (bad retrieval, wrong tool, policy gap). Use comparison views for **prompt A/B**: diff spans side by side, not only final answers. Define saved filters for **high-risk** tenants or features so on-call starts from a useful subset rather than ad hoc queries.

## Long multi-step debugging

For runs exceeding tens of steps, collapse repetitive spans in the UI but keep **raw** export for replay. Mark **checkpoints** in code (after plan approval, after batch tool completion) so traces align with human mental models. Attach **user-visible message ids** to the trace root for support tooling.

## Metrics beyond traces

Pair traces with **aggregate** dashboards: p95 step latency, tool error rates by name, token growth per turn, guardrail trigger counts. Alerts should fire on **deltas** after deploys, not only static thresholds.

## Common mistakes

- Logging everything the model saw, defeating data-minimization and exploding storage cost.
- No linkage between UI session and backend trace id, so support cannot investigate.
- Traces that omit failed branches or retries, hiding flakiness.
- Dashboards without ownership or alerts on error-rate or latency SLO regressions.

## References to course modules

These map to the **23-module Agent Factory course** (see [`../../course/README.md`](../../course/README.md) when published).

- **Module 17 — Tracing, Spans, and Correlation IDs** — OpenTelemetry-style agent traces.
- **Module 18 — Cost and Token Attribution** — budgets and chargeback patterns.
- **Module 19 — Debugging Multi-Step Runs** — trace-driven incident response.

Full curriculum index: [`../../course/README.md`](../../course/README.md) (when present).

## See also

- [Agent Evaluation](agent-evaluation.md)
- [Error Recovery](error-recovery.md)
- [Cost Optimization](cost-optimization.md)
- [Sandboxing](sandboxing.md)
- [Harness Engineering](harness-engineering.md)
