# Chatbot Pretending to Be an Agent

## Summary

The product is labeled an “AI agent,” but under the hood it is a **single-turn or lightly stateful chatbot**: no tool loop, no durable plan, no external actions, no verification step. The system prompt uses agent-flavored language (“I will autonomously…”) while the implementation is **plain completion**.

## Anti-pattern

**Agency theater.** Marketing and UX promise delegation and outcomes; engineering ships a chat wrapper. There is no **observe–decide–act** cycle, no error recovery, and no grounding in executable checks.

## Why it fails

Without tools, the model cannot **commit** actions—only describe them—so users must copy-paste into other systems. Without state beyond the transcript, long tasks **fragment** across sessions. Without a loop, there is **no agency** in the engineering sense: nothing persists, nothing is retried, nothing is verified.

Stakeholders assume safeguards exist because the word “agent” implies them; security review may be skipped. When something goes wrong, blame lands on “the model” instead of missing harness code.

### Symptoms in production

Users ask “did it actually file the ticket?” and the answer is no. Demos work on cherry-picked scripts; real workflows stall at the first exception.

### Root cause

Confusing **autonomous-sounding prose** with **autonomous architecture**.

## Key takeaway

**Reserve “agent” for systems with loops, tools, and explicit outcomes**—or rename the product honestly.

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

- [Agent loop](../../concepts/agent-loop.md)
- [Agent vs workflow](../../research/agent-vs-workflow.md)
- [Anatomy of a good agent](../../research/anatomy-of-a-good-agent.md)
- [Premature autonomy agent](premature-autonomy-agent.md)
- [Infinite loop agent](infinite-loop-agent.md)
