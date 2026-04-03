# Minimal Function-Calling Agent: Twenty Lines, Full Loop

## Summary

This example is a deliberately tiny agent: a loop that (1) sends the user goal and prior steps to the model, (2) receives either a final answer or a **function call** with JSON arguments, (3) executes the function in code, and (4) appends the result to history until done or a step limit is hit. No frameworks—just the smallest **observe–decide–act** cycle that still qualifies as an agent.

## Pattern

**Bare ReAct with structured tool calls.** The “tools” are plain functions registered in a dict; the model’s tool schema is minimal (one or two operations). The host program owns iteration caps, logging, and error formatting back to the model.

## What makes it good

The entire system fits in one screen of code, which makes it ideal for teaching and for proving integration paths (auth, logging, tracing) before adopting heavier orchestration. Failure modes are obvious: bad JSON, exceptions from tools, or runaway loops—each has a direct fix. Tests can stub the model to emit deterministic tool sequences.

It demonstrates that **agency comes from the loop and the tools**, not from branding or a large prompt file.

### In practice

Wrap tool execution in try/catch and return concise error strings to the model with a reminder of the schema. Log each turn’s tool name, latency, and argument hash for replay. Swap the model client in one place to compare providers without touching business logic.

### Failure modes this design mitigates

Huge frameworks sometimes obscure **iteration limits** and **duplicate tool calls**. Twenty-line hosts make caps impossible to miss. Deterministic tests can feed a fake model that always calls `finish` or always errors on tool 2 to validate recovery.

### When to reconsider

Add orchestration libraries when you need persistence, branching human approval, or multi-agent fan-out. The minimal loop remains the **reference implementation** for mental models and integration tests.

## Key takeaway

**Start with the smallest closed loop**; add frameworks only when you need persistence, branching, or multi-agent coordination.

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

- [Agent loop](../../concepts/agent-loop.md)
- [Tool design](../../concepts/tool-design.md)
- [Structured outputs](../../concepts/structured-outputs.md)
- [Anatomy of a good agent](../../research/anatomy-of-a-good-agent.md)
- [Agent vs workflow](../../research/agent-vs-workflow.md)
