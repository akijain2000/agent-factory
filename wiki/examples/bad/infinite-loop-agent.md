# Infinite Loop Agent: Retry Until the Heat Death of the Wallet

## Summary

This anti-pattern implements an agent that **retries failed actions indefinitely**: the same failing tool call, the same bad parameters, the same hallucinated file path—driven by “keep trying until it works.” There is **no circuit breaker**, **no maximum iterations**, and **no fallback** to a human or a simpler workflow.

## Anti-pattern

**Unbounded control flow.** The loop condition is implicit optimism. Errors are fed back verbatim without backoff, categorization, or escalation.

## Why it fails

Costs **explode** linearly or worse with each retry; provider rate limits amplify outages. Users wait forever with spinning UI. Logs fill with identical stack traces, hiding the original root cause. **No recovery** path exists: the system never admits defeat, so operators are not alerted until finance notices the bill.

In multi-step flows, one stuck subtask blocks the entire run with no partial result or checkpoint strategy.

### Symptoms in production

Dashboards show flat error rates but soaring token use. PagerDuty stays quiet while budgets burn.

### Root cause

Confusing **persistence** with **lack of limits**. Healthy agents fail fast, classify errors, and escalate.

## Key takeaway

**Cap steps, cap cost, and require monotonic progress or human handoff.**

## Review checklist (red flags)

- [ ] Single prompt or flat registry trying to cover unrelated domains.
- [ ] No max iterations, no circuit breaker, no escalation path.
- [ ] Tools overlap in name or description; deprecation is unmanaged.
- [ ] Production credentials or shells available without scoped sandboxes.
- [ ] Entire repositories or logs pasted every turn “for context.”
- [ ] Multiple orchestration frameworks each owning state for the same user journey.
- [ ] “Agent” branding without tools, loop, or verifiable outcomes.

## How teams slide into this

Pressure to ship a unified “copilot” across teams, demos that must look unrestricted, and copy-paste from tutorials that emphasize power over safety. Without design review, the path of least resistance is one agent, one prompt, one tool dump.

## Redesign direction

Factor responsibilities, shrink active tools per step, add caps and approvals, and instrument traces. Cross-link each anti-pattern article to a matching [good example](../good/) once you know your target shape (e.g., handoffs, MCP, or explicit graphs).

## See also

- [Error recovery](../../concepts/error-recovery.md)
- [Autonomous loops](../../concepts/autonomous-loops.md)
- [Cost optimization](../../concepts/cost-optimization.md)
- [Anti-patterns](../../research/anti-patterns.md)
- [Context stuffing agent](context-stuffing-agent.md)
