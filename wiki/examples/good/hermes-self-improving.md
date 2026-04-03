# Hermes-Style Self-Improving Agent: Learn, Skillify, Promote

## Summary

Inspired by Hermes-like systems, this agent maintains an **explicit learning loop**: after tasks, it reflects on failures and successes, distills repeatable procedures into **skills** (prompt fragments, checklists, or small programs), and **promotes** only those that pass quality gates. Knowledge persists outside the raw chat log so future sessions benefit without re-deriving the same lessons.

## Pattern

**Explicit learning cycle with promotion criteria.** Capture traces and outcomes, mine them for stable patterns, draft a skill artifact, validate against a holdout set or human review, then commit to a versioned store. Demotion or deprecation is as important as promotion when models or tools change.

## What makes it good

Without promotion criteria, “self-improving” becomes “self-accumulating sludge.” Hermes-style discipline ties memory growth to measurable utility: fewer retries, higher task success, or shorter paths. Skills are inspectable—unlike opaque weight updates—so teams can audit what the system “learned.”

The loop composes with normal agent tooling: learning is another workflow with its own budget and guardrails.

### In practice

Store skills as files (markdown, JSON, or small scripts) in a repo with PR review. Tag skills with **evidence**: which tasks improved, by how much, and which model version they targeted. Schedule periodic audits to retire skills that no longer help after a model upgrade.

### Failure modes this design mitigates

Uncontrolled self-edit prompts accumulate **contradictions** and unsafe shortcuts (“always disable SSL verification”). Promotion gates and regression tests catch harmful skill drafts before they enter the default bundle.

### When to reconsider

If your task distribution shifts weekly, invest in eval suites before aggressive skill promotion—otherwise you optimize for yesterday’s benchmarks.

## Key takeaway

**Treat learning as a governed pipeline** (capture, distill, verify, promote), not as unbounded append-only context.

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

- [Self-improving agents](../../concepts/self-improving-agents.md)
- [Feedback loops](../../concepts/feedback-loops.md)
- [Memory systems](../../concepts/memory-systems.md)
- [Hermes agent deep dive](../../research/hermes-agent-deep-dive.md)
- [Agent evaluation](../../concepts/agent-evaluation.md)
