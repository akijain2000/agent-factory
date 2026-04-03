# Premature Autonomy Agent: Purchasing Power on Day One

## Summary

This anti-pattern grants **full autonomy** before guardrails exist: the agent can **make purchases**, **send external email**, **modify customer records**, or **create cloud resources** without confirmation, sandboxing, or policy checks. The team wanted speed; they shipped **irreversible side effects** tied to a stochastic planner.

## Anti-pattern

**High-risk actions without human-in-the-loop.** Capabilities are enabled “so the demo looks real.” Audit trails and dual-control are deferred to “phase two.”

## Why it fails

Stochastic failures become **business incidents**: wrong SKU ordered, email sent to the wrong list, data corrupted at scale. **No human-in-the-loop** for high-risk actions means no one with skin in the game approves the final commit. Legal and compliance teams block rollout after the first mistake; rebuilding trust costs more than incremental guardrails would have.

Attackers need only steer the model once to trigger financial or data harm.

### Symptoms in production

Finance finds unexplained charges; support finds mass emails the team did not preview.

### Root cause

**Capability-led roadmap** instead of **controls-first** design.

## Key takeaway

**Ship read-only and draft modes first; add approval gates before money, mail, or master data change.**

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

- [Human-in-the-loop](../../concepts/human-in-the-loop.md)
- [Guardrails](../../concepts/guardrails.md)
- [Agent security](../../concepts/agent-security.md)
- [No guardrails agent](no-guardrails-agent.md)
- [Anti-patterns](../../research/anti-patterns.md)
