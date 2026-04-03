# No Guardrails Agent: Root Shell and a Dream

## Summary

This anti-pattern gives the model **broad system access**: full shell, raw database clients, unrestricted file I/O, and production credentials—**without** sandboxing, approval gates, or read-only defaults. A single successful prompt injection or mistaken plan can **delete a production database** or exfiltrate secrets.

## Anti-pattern

**Trust boundary collapse.** The same process that parses user text also executes arbitrary commands. There is no separation between “planning” and “execution,” no policy engine, and no human checkpoint for destructive operations.

## Why it fails

Models are **not security kernels**. They follow persuasive text, including malicious instructions embedded in web pages or tickets. Without guardrails, social engineering becomes remote code execution. Even “benign” mistakes scale: a wrong `DROP` or `rm -rf` is one tool call away.

Regulatory and customer trust evaporates after the first incident. Forensics are hard because actions were not logged with intent and approval metadata.

### Symptoms in production

Postmortems cite “the agent thought the user wanted a reset.” There is no record of who authorized the reset.

### Root cause

Shipping **capabilities** before **controls**, often to win a demo timeline.

## Key takeaway

**Default deny, sandbox execution, and require explicit approval for irreversible or exfiltration-capable actions.**

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

- [Guardrails](../../concepts/guardrails.md)
- [Sandboxing](../../concepts/sandboxing.md)
- [Agent security](../../concepts/agent-security.md)
- [Human-in-the-loop](../../concepts/human-in-the-loop.md)
- [Premature autonomy agent](premature-autonomy-agent.md)
