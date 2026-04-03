# CrewAI Research Team: Role-Specialized Sequential Pipeline

## Summary

This example describes a three-role CrewAI crew: a **Researcher** gathers sources and facts, a **Writer** drafts a structured brief from those notes, and an **Editor** checks claims, tone, and completeness before output is returned. Tasks are chained in order; each role receives only the artifacts it needs from the previous step.

## Pattern

**Clean role separation with a sequential pipeline.** Each agent has a short system identity, a small tool allowlist (e.g., search vs drafting vs citation check), and a task definition with explicit inputs and outputs. The crew orchestrator passes structured handoffs rather than dumping the full conversation history into every prompt.

## What makes it good

Specialization reduces cognitive load per model call: the Researcher is not simultaneously optimizing prose; the Writer is not re-implementing search strategy. Sequential ordering matches the dependency graph of the work (facts before narrative before polish). Cost and latency remain predictable because parallelism is not introduced until the workflow is stable.

The pattern scales to human review gates by inserting a pause between Editor approval and external publish, without rewriting the core crew.

### In practice

Define each task output as a schema: Researcher returns `sources[]` with URLs and quotes; Writer returns `sections[]`; Editor returns `issues[]` and `approved: bool`. Passing structured objects between agents avoids re-explaining the entire narrative each time and keeps token use sublinear in document length when summaries are allowed.

### Failure modes this design mitigates

When every agent sees the full chat, later roles **overfit** to early mistakes (e.g., citing a retracted source). Narrow handoffs force the Writer to treat Researcher output as data, which you can validate (minimum sources, required fields) before drafting proceeds.

### When to reconsider

If tasks require tight back-and-forth clarification with the user, pure sequential crews can feel rigid. Add a **short feedback loop** only around the Researcher or insert a human approval step before expensive drafting.

## Key takeaway

Multi-agent setups work best when **roles map to real phases of work** and **information flows in one clear direction**, not when every agent can do everything.

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

- [Multi-agent orchestration](../../concepts/multi-agent-orchestration.md)
- [Agent personas](../../concepts/agent-personas.md)
- [Context window management](../../concepts/context-window-management.md)
- [Multi-agent landscape](../../research/multi-agent-landscape.md)
- [Cost optimization](../../concepts/cost-optimization.md)
