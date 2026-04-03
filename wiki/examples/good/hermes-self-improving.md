# Hermes-Style Self-Improving Agent: Learn, Skillify, Promote

## Summary

Inspired by Hermes-like systems, this agent maintains an **explicit learning loop**: after tasks, it reflects on failures and successes, distills repeatable procedures into **skills** (prompt fragments, checklists, or small programs), and **promotes** only those that pass quality gates. Knowledge persists outside the raw chat log so future sessions benefit without re-deriving the same lessons.

## Pattern

**Explicit learning cycle with promotion criteria.** Capture traces and outcomes, mine them for stable patterns, draft a skill artifact, validate against a holdout set or human review, then commit to a versioned store. Demotion or deprecation is as important as promotion when models or tools change.

## What makes it good

Without promotion criteria, “self-improving” becomes “self-accumulating sludge.” Hermes-style discipline ties memory growth to measurable utility: fewer retries, higher task success, or shorter paths. Skills are inspectable—unlike opaque weight updates—so teams can audit what the system “learned.”

The loop composes with normal agent tooling: learning is another workflow with its own budget and guardrails.

### Concrete skill stub

A promoted skill lives as a versioned file with evidence metadata:

```markdown
# skills/summarize-pr.md
---
version: 1.2
promoted: 2025-11-03
evidence: reduced review-prep time by 40% across 23 tasks (gpt-4o)
model_target: gpt-4o
regression_suite: tests/skills/summarize-pr.yaml
---

## When to use
User asks for a PR summary, diff explanation, or changelog draft.

## Procedure
1. Read the full diff via `gh pr diff`.
2. Group changes by file type (src, test, config, docs).
3. For each group, emit: what changed, why it likely changed, risk level.
4. Produce a 3-bullet summary suitable for a Slack message.

## Constraints
- Never include raw secrets even if they appear in the diff.
- If diff > 2000 lines, summarize by directory instead of file.
```

### Promotion gate checklist

Before a candidate skill enters the default bundle:

1. **Evidence threshold**: task success improved by ≥15% on ≥10 runs.
2. **Regression pass**: existing skills still pass their test suites.
3. **Human review**: at least one maintainer approved the diff.
4. **Model-version tag**: skill specifies which model it was validated against.
5. **Rollback hook**: the skill can be disabled by deleting its file without side effects.
6. **Safety scan**: no credential patterns, no instructions to bypass guardrails.

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
