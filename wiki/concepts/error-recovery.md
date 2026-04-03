# Error Recovery

## What it is

**Error recovery** is how an agent harness responds when models, tools, or dependencies fail: **retries with exponential backoff** for transient faults, **fallbacks** to alternate models or simpler tools, **circuit breakers** that stop hammering sick dependencies, **graceful degradation** (partial answers with clear limits), and **dead letter queues** for work that cannot complete after policy limits.

The goal is **resilience without infinite loops**: recover when safe, surface when not.

## Why it matters for agents

Models will retry mentally if you paste “try again” without structure; combined with tool retries, that doubles cost and risk. Production agents need deterministic policies that distinguish **retryable** (`429`, `503`, timeout) from **fatal** (validation, auth). Operators need visibility into poison messages and stuck runs.

## How to implement it

1. **Classify errors** at the tool boundary; normalize into `{ code, retryable, detail }` for logs and harness logic.
2. **Backoff:** jittered exponential caps; per-tool and per-run limits; never retry non-idempotent writes without dedupe keys.
3. **Circuit breaker:** after N failures in window T, fail fast for M seconds; surface degraded mode message to user.
4. **Fallbacks:** cheaper model for summarization; read-only cache for stale-but-usable data; escalate to human for policy violations.
5. **DLQ:** enqueue failed jobs with payload + failure reason + trace id; alert and allow manual replay.
6. **Loop guards:** detect repeated identical tool calls or no state delta across iterations; break and escalate.

**Infinite loop prevention:** max steps, max wall time, max spend, stagnation detection, and circuit breakers together—not any single layer.

## Policy matrix (example)

| Error class        | Retry? | Backoff | User-visible message        | Ops action        |
|--------------------|--------|---------|-----------------------------|-------------------|
| Rate limit / 429   | Yes    | Jitter  | “Temporary limit—retrying”  | Alert if sustained |
| Validation / 400   | No     | —       | “Bad request—fix input”     | Log + metric      |
| Upstream timeout   | Yes    | Exp     | “Still working…”            | Breaker if flappy |
| Auth / 403         | No     | —       | “Permission denied”         | Page on-call      |

Tune the matrix per tool and tenant; store it as config, not scattered `if` statements.

## Testing failure paths

Chaos tests: inject latency, 500s, and malformed payloads into tool stubs. Assert the harness **stops** under stagnation and **preserves** partial state for human resume. Property tests on idempotency keys help ensure retries do not double-charge.

## Common mistakes

- **Retry everything** including `400` and business rule violations.
- **Silent error swallowing:** empty catch blocks or “Sorry” with no trace.
- **Feeding raw HTML/500 bodies** into the model as the only observation.
- **Recursive self-retry** at multiple layers without shared attempt budgets.

## References to course modules

These map to the **23-module Agent Factory course** (see [`../../course/README.md`](../../course/README.md) when published).

- **Module 08 — Error Handling and Recovery** — retries, idempotency, circuit breakers, and DLQs.
- **Module 05 — Tool Design and Integration** — surfacing errors the model can act on safely.
- **Module 19 — Observability and Debugging** — correlating failures and retries in traces.

Full curriculum index: [`../../course/README.md`](../../course/README.md) (when present).

## See also

- [Agent Loop](agent-loop.md)
- [Tool Design](tool-design.md)
- [Guardrails](guardrails.md)
- [State Management](state-management.md)
- [Rate Limiting](rate-limiting.md)
