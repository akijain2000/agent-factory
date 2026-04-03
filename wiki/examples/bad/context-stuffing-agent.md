# Context Stuffing Agent: The Whole Repo Every Turn

## Summary

This anti-pattern feeds the model **the entire codebase**, giant log dumps, or hundreds of retrieved chunks **on every turn**—hundreds of thousands of tokens “so it has full context.” The assumption is that more text means better answers; the reality is **context rot**, distraction, and prohibitive cost.

## Anti-pattern

**Window as database.** No summarization, no retrieval policy, no pointer indirection—just append everything again when anything changes.

## Why it fails

Models attend poorly to mid-context needles; irrelevant code **drowns** the few lines that matter. Latency rises with input size; bills scale with tokens whether or not the model uses them. **Performance** on precise edits degrades because the model chases red herrings from unrelated modules.

CI and reproducibility suffer: runs are non-deterministic when the model fixates on different sections of the blob each time.

### Symptoms in production

Simple one-line fixes take multiple turns. Developers joke that the agent “read the repo but understood nothing.”

### Root cause

Laziness in **context engineering**—treating retrieval and summarization as optional extras.

## Key takeaway

**Retrieve and summarize on demand; keep working sets small and labeled.**

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

- [Context window management](../../concepts/context-window-management.md)
- [Context engineering](../../concepts/context-engineering.md)
- [Memory systems](../../concepts/memory-systems.md)
- [Anti-patterns](../../research/anti-patterns.md)
- [God agent](god-agent.md)
