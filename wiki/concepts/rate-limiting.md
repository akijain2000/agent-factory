# Rate Limiting

## What it is

**Rate limiting** constrains how fast an agent consumes **external APIs** (provider RPM/TPM), **internal** services, and **your own** budgets: **token budgets per request**, **concurrency** caps across tenants, and **backpressure** signals when downstream systems saturate. For agent loops, limits apply per **iteration**, per **run**, and per **aggregate** (org, API key, deployment). Handling limits gracefully means **retry with jitter**, **exponential backoff**, **degraded modes**, and **user-visible** progress instead of hard failures.

## Why it matters for agents

Loops amplify calls: one user message can trigger dozens of model and tool requests. A single 429 from a provider can stall a run mid-plan; unbounded parallelism can **brown out** databases or bankrupt a quota. Without explicit **token and concurrency** governance, tail latency explodes and incident response lacks levers (who to throttle, which feature to shed).

Provider dashboards show **account-level** limits; your product needs **per-customer** fairness so one noisy neighbor cannot exhaust shared capacity. Rate limiting is also a **product** knob: free tiers get tighter ceilings, enterprise gets **reserved** concurrency where contracts allow.

## How to implement it

1. **Classify limits:** hard (HTTP 429, quota exhausted) vs soft (latency SLO, cost ceiling). Map each to a **handler** in the harness.
2. **Per-request token budget:** pass `max_tokens` / equivalent to the model API; track **prompt + completion** against a ceiling; stop or summarize when approaching the cap.
3. **Concurrency:** use semaphores or worker pools per **tenant** and per **tool class**; separate “cheap” tools from “expensive” ones so one customer cannot starve the pool.
4. **Retries:** on 429 and transient 5xx, retry with **full jitter** and a **max elapsed** time; respect `Retry-After` when present. Never retry non-idempotent tools without **deduplication** keys.
5. **Backpressure:** when queues grow, shed load: delay non-critical runs, route to smaller models, or return **202** with estimated wait. Surface queue depth to operators.
6. **Agent loop integration:** after each iteration, recompute **remaining budget** (tokens, wall time, dollars); if low, switch strategy—shorter plan, fewer tools, human escalation.
7. **Observability:** emit metrics for `rate_limit_events`, `retry_count`, and `budget_remaining`; alert on sustained 429s or budget exhaustion rates.

8. **Circuit breakers:** after repeated failures to a dependency, **trip** open for a cool-down; fail fast with a clear user message instead of hammering a sick endpoint.

**Provider vs self-imposed:** combine both—provider limits are the ceiling; your budgets protect **product economics** and **fairness**.

## Token and cost coupling

Align **RPM/TPM** limits with **dollar** limits per org. When TPM is tight, prefer **smaller context** (summarization, retrieval caps) over blind retries.

Document **limit headers** and provider-specific quirks in runbooks so on-call engineers know whether to backoff, switch **region**, or failover to a **secondary** model.

**Load tests** should include **429 storms** and partial outages—synthetic traffic that only hits 200s misses real-world agent behavior.

## Common mistakes

- **Busy-loop retries** without caps, burning quota and lengthening outages.
- Global concurrency with **no tenant fairness**; one bad job blocks everyone.
- Treating **tool errors** as always retriable (duplicate writes, duplicate charges).
- Hiding throttling from users—**silent** stalls erode trust.
- **Static** concurrency set to “high” in dev and **equal** in prod without load testing.
- Ignoring **downstream** rate limits (search APIs, CRM) while only throttling the LLM.

## References to course modules

These map to the **23-module Agent Factory course** (see [`../../course/README.md`](../../course/README.md) when published).

- **Module 08 — Error Handling and Recovery** — retries, backoff, and overload behavior.
- **Module 20 — Deployment and Scaling** — quotas, capacity, and graceful degradation under load.
- **Module 19 — Observability and Debugging** — attributing throttling and saturation in production.

Full curriculum index: [`../../course/README.md`](../../course/README.md) (when present).

## See also

- [Cost Optimization](cost-optimization.md)
- [Error Recovery](error-recovery.md)
- [Agent Loop](agent-loop.md)
- [Observability](observability.md)
- [Deployment Patterns](deployment-patterns.md)
