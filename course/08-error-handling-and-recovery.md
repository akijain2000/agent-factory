# Module 08: Error Handling and Recovery

**Duration:** approximately 30 minutes  
**Prerequisites:** Module 03 (The Agent Loop); Module 05 (Tool Design) strongly recommended.

---

## Learning objectives

By the end of this module, you should be able to:

- **Classify** failures in agent systems (tool, LLM, logic, external dependency) and map them to responses.
- **Implement** retries with exponential backoff, jitter, and bounded attempts.
- **Design** fallback chains and circuit breakers to prevent cascading outages.
- **Use** dead letter queues or equivalent patterns for unrecoverable failures while preserving debuggability.
- **Explain** Hermes-style multi-provider fallback ideas at a high level.

---

## 1. Types of failures in agents

**Tool errors**  
Timeouts, 4xx/5xx from APIs, validation failures, permission denials. Often **transient** or **user-fixable**; return structured codes to the model.

**LLM errors**  
Rate limits, context length exceeded, malformed output, refusals. May require **backoff**, **truncation**, **smaller model**, or **prompt repair**.

**Logic errors**  
Wrong tool chosen, incorrect parsing of tool JSON, infinite loops repeating the same call. Mitigate with **validators**, **deduplication**, and **max step** guards in the harness.

**External service failures**  
Third-party outages, DNS, network partitions. Treat as **degraded mode**; surface status to the user when user-visible features break.

---

## 2. Retry strategies

**Exponential backoff**  
Wait `base * 2^attempt` between retries (cap the delay). Prevents hammering a struggling dependency.

**Jitter**  
Add random noise to wait times so synchronized clients do not retry in lockstep.

**Max attempts**  
Hard stop after `N` tries; return a final structured error to the agent with `retryable: false`.

```python
import random
import time

def backoff_sleep(attempt, base=0.5, cap=30.0):
    exp = min(cap, base * (2 ** attempt))
    time.sleep(exp + random.uniform(0, 0.25 * exp))
```

Retry **only** when safe: GETs, idempotent writes, or operations with **idempotency keys**. Never blindly retry a non-idempotent tool without deduplication.

---

## 3. Fallback chains

A **fallback chain** tries alternatives when the primary path fails:

1. Primary model → smaller/faster model for shallow tasks.  
2. Primary search index → secondary web search.  
3. Live API → cached snapshot with explicit “stale as of” metadata.

Each step should **record** which tier served the response for observability. Instruct the model **not** to hide degradation—users should know when answers are stale or approximate.

---

## 4. Circuit breakers

A **circuit breaker** stops calling a failing dependency after a threshold, failing fast for a cooldown period. This protects the rest of the stack and avoids burning tokens on hopeless tool loops.

States (simplified):

- **Closed** — normal traffic.  
- **Open** — reject calls immediately; return `CIRCUIT_OPEN` to the agent.  
- **Half-open** — occasional probe to detect recovery.

Wire breaker metrics to dashboards: trips per hour, time in open state, error taxonomy.

---

## 5. Dead letter queues

When a task cannot complete after retries and fallbacks, **dead letter** it:

- Persist payload, correlation id, last error, and stack/tool trace (scrub secrets).  
- Alert operators or surface in an internal UI.  
- Do **not** drop silently—silent loss erodes trust.

Agents should receive a concise `UNRECOVERABLE` object so they can apologize, suggest next steps, or request human takeover.

---

## 6. Study: Hermes Agent’s fallback provider chains

Hermes-style architectures emphasize **resilient model routing**: if the primary provider errors or rate-limits, **fail over** to another model or provider with compatible capabilities, adjusting prompts or output parsers as needed. The pattern pairs well with **unified telemetry** so you can see **which provider actually served** each step.

Lessons:

- Keep **capability matrices** (context length, tool support, vision).  
- Normalize outputs so **downstream** code does not branch on vendor quirks.  
- Test fallbacks in CI—unused chains rot.

---

## Exercises

1. **Add error handling** to a given agent loop (use your project’s harness or the pseudocode below). Identify where to catch tool exceptions, map them to `{ code, retryable, message }`, and enforce `max_steps`. Write the diff or annotated pseudocode.

```python
# Pseudocode for improvement
while steps < max_steps:
    action = model.next(messages, tools)
    if action.is_tool:
        try:
            result = tools.run(action)
        except Exception as e:
            result = ???  # your structured error here
        messages.append(tool_message(result))
    else:
        return action.text
```

2. **Design a fallback chain** for a multi-model agent that: answers user questions, calls tools, and must stay up during a provider outage. Specify order of providers, triggers for failover, what happens to in-flight tool calls, and how you log decisions.

---

## Further reading

- [Error recovery](../../wiki/concepts/error-recovery.md)
- [Hermes agent deep dive](../../wiki/research/hermes-agent-deep-dive.md)

---

## Summary

Resilient agents **classify** failures, **retry** safely, **degrade** with transparency, and **stop** before cascading damage. Circuit breakers protect dependencies; dead letter queues protect operational integrity. Multi-provider fallback, as in Hermes-style systems, is a **tested policy**, not a config toggle—validate it before you need it in production.
