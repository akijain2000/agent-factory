# God Agent: One Prompt to Rule Them All

## Summary

This anti-pattern is a single “super agent” entrusted with **every** responsibility: research, coding, email, calendar, billing analysis, incident response, and creative writing. It carries **fifty or more tools**, a **five-thousand-token system prompt** packed with policies and examples, and no real delegation. Marketing still calls it an “autonomous agent.”

## Anti-pattern

**Monolithic agency.** One model instance, one context, one flat tool registry, one prompt that tries to encode the entire company handbook. Specialization exists only in prose (“when doing X, remember Y”), not in architecture.

## Why it fails

Tool confusion dominates: similar tool names and overlapping descriptions cause **wrong-tool selection** and accidental side effects. The context window fills with policy text, few-shot chatter, and accumulated history, leaving little capacity for the actual task (**context overflow**). The system is **untestable** in practice—too many interaction paths, too much coupling to prompt wording, and no seams for unit tests beyond end-to-end roulette.

Operators cannot reason about blast radius: any bug or injection affects the full capability surface. Cost and latency spike because every turn pays for the entire prompt and tool schema.

### Symptoms in production

Users report “it used the wrong integration,” retries make things worse, and incident reviews find no single owner for behavior. Prompt edits fix one scenario and break three others.

### Root cause

Conflating **flexibility** with **lack of structure**. Useful agents are constrained; god agents are only constrained by model politeness.

## Key takeaway

**Decompose by responsibility and shrink each context**—or accept that you have a brittle demo, not a maintainable system.

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

- [Anti-patterns](../../research/anti-patterns.md)
- [Tool selection](../../concepts/tool-selection.md)
- [Context window management](../../concepts/context-window-management.md)
- [Multi-agent orchestration](../../concepts/multi-agent-orchestration.md)
- [Over-tooled agent](over-tooled-agent.md)
