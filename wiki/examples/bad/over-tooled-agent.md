# Over-Tooled Agent: When the Toolbox Becomes a Maze

## Summary

This anti-pattern exposes **more than a hundred tools** to a single model, many of which **overlap** in purpose: multiple search variants, several “send email” adapters, legacy and v2 APIs side by side. The intent is flexibility; the outcome is **decision paralysis** and chronic mis-selection.

## Anti-pattern

**Schema sprawl without orthogonality.** Tools differ only in subtle defaults or naming. No router narrows the active set per task phase. Descriptions read like internal API docs pasted into the prompt.

## Why it fails

Large language models are not exhaustive optimizers over huge discrete action spaces. With overlapping tools, **calibration breaks**: the model picks the familiar-sounding name, not the correct integration. Latency grows from parsing enormous schemas; costs rise from retries after failed calls.

Maintenance becomes hazardous: deprecating one tool risks silent breakage because callers (the model) are not version-pinned in a reliable way. Telemetry shows high **tool-error rates** clustered around sibling tools.

### Symptoms in production

Playbooks recommend “try the other search tool if the first fails,” effectively asking humans to finish routing. Automated evals show high variance on identical prompts.

### Root cause

Mistaking **coverage** for **clarity**. Fewer, composable tools with clear contracts beat a catalog of micro-variants.

## Key takeaway

**Merge, wrap, or phase tools** so the model rarely chooses among near duplicates.

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

- [Tool design](../../concepts/tool-design.md)
- [Tool selection](../../concepts/tool-selection.md)
- [Anti-patterns](../../research/anti-patterns.md)
- [God agent](god-agent.md)
- [Framework soup](framework-soup.md)
