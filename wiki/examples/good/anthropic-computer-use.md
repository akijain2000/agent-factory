# Anthropic Computer Use: Progressive Capability and Safety Gates

## Summary

Anthropic’s computer-use style agents combine **screen understanding** (screenshots and/or accessibility-derived structure) with **low-level actions**: mouse movement, clicks, and keyboard input. The product narrative emphasizes **progressive capability**: the model gains desktop-like affordances only when the harness enables them, paired with **safety gates** before irreversible or high-risk operations.

## Pattern

**Progressive capability with explicit gates.** The agent loop alternates between perception (what is on screen?), planning (what is the next atomic action?), and actuation. High-risk classes of actions—installing software, deleting files, sending mail—require additional confirmation, policy checks, or human approval rather than being bundled into a single “do anything” tool.

## What makes it good

Treating the desktop as a hazardous environment mirrors how security teams treat shells: default-deny, scoped permissions, and audit logs. Progressive rollout lets teams validate reliability on read-only or single-app sandboxes before enabling broader control. Safety gates convert “the model tried” into “the system allowed,” which is essential for enterprise adoption.

Structured action formats (coordinates, keys, delays) make automation more testable than free-form shell one-liners.

### In practice

Start in VMs or containers with snapshots so runs are reproducible. Record action traces (mouse path, keys) for replay and forensics. Map “sensitive applications” to explicit allowlists so the agent cannot pivot from a browser task into unrelated admin panels without a new approval.

### Failure modes this design mitigates

Unsandboxed desktop agents turn prompt injection into **data exfiltration** via email clients and file managers. Progressive capability limits blast radius. Gates add a place to attach enterprise policy (MFA, DLP) that models cannot bypass with clever wording.

### When to reconsider

If your automation targets a single SaaS with a good API, **prefer APIs** over pixels and mouse coordinates. Computer use shines when UIs lack APIs or when you must validate what humans actually see.

## Key takeaway

**Computer use is a privilege, not a default**: scale autonomy in stages and put hard stops before irreversible effects.

## Review checklist

- [ ] Is the active tool set small enough to name from memory?
- [ ] Are transitions or handoffs explicit in code, not only in prose?
- [ ] Do traces identify phase, tool, and outcome for each step?
- [ ] Are step, cost, and time limits enforced in the host, not the model?
- [ ] Can you replay a failed run with mocks for tools and LLM?
- [ ] Are high-risk actions behind sandbox, schema validation, or human approval?

## Metrics and evaluation

Define SLIs for the loop: success rate per task type, median steps to completion, tool-error ratio, and cost per successful outcome. Store traces with default PII redaction and retain enough detail to replay decisions. Run periodic canaries on pinned prompts and tool versions to catch provider or dependency drift before users do.

## Contrast with common failures

For unstructured alternatives and their failure modes, see [God agent](../bad/god-agent.md), [Over-tooled agent](../bad/over-tooled-agent.md), and the wiki [Anti-patterns](../../research/anti-patterns.md) catalog.

## See also

- [Sandboxing](../../concepts/sandboxing.md)
- [Guardrails](../../concepts/guardrails.md)
- [Progressive complexity](../../concepts/progressive-complexity.md)
- [Anthropic agent patterns](../../research/anthropic-agent-patterns.md)
- [Agent security](../../concepts/agent-security.md)
