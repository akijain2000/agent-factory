# Framework Soup: LangGraph, CrewAI, and AutoGen in One Repo

## Summary

This anti-pattern stitches together **multiple agent frameworks** in one codebase—say LangGraph for one path, CrewAI for another, AutoGen for a third—each with its own **state model**, tracing format, and concurrency primitives. The goal is to use “the best of each”; the result is **three incompatible orchestration layers** maintaining conflicting notions of who is speaking and what happened.

## Anti-pattern

**Conflicting abstractions in a single product.** Teams import whatever tutorial matched last week’s blog post. Shared concepts (memory, handoffs, tools) are re-implemented per framework instead of normalized.

## Why it fails

On-call engineers cannot trace a single user request across components without reading three docs and three log formats. **State divergence** causes duplicate tool calls, lost messages, and race conditions. Dependency upgrades become a nightmare: one framework pins an old HTTP client; another demands a new one.

Testing requires harnesses for each stack; behavior diverges subtly for the same prompt. New hires face weeks of orientation just to run the repo locally.

### Symptoms in production

“Heisenbugs” appear only when paths cross frameworks. Feature requests stall on “which orchestrator owns this?”

### Root cause

Absence of an **architecture decision record** and a mandate to **standardize on one orchestration spine** (or a thin internal adapter).

## Key takeaway

**Pick one primary orchestration model per surface area**; integrate other libraries as utilities, not parallel universes.

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

- [Framework comparison](../../research/framework-comparison.md)
- [State management](../../concepts/state-management.md)
- [Harness engineering](../../concepts/harness-engineering.md)
- [Anti-patterns](../../research/anti-patterns.md)
- [God agent](god-agent.md)
