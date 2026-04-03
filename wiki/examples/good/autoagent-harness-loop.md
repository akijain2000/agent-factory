# AutoAgent Harness: program.md and Optimization Loop

## Summary

AutoAgent-style harnesses treat agent behavior as **code plus data**: a `program.md` (or equivalent) holds the evolving system prompt, tool policies, and evaluation hooks. A **meta-agent** or offline job edits that program, runs benchmarks, and **hill-climbs** toward higher scores—always against fixed tasks so improvement is measurable.

## Pattern

**Explicit optimization loop over a versioned program artifact.** Changes are proposed as diffs to prompts or structured config, scored by an eval suite (accuracy, tool efficiency, safety violations), and kept or rolled back. Human review gates can sit between “candidate program” and “deployed program.”

## What makes it good

Tying optimization to **concrete benchmarks** avoids vibes-driven prompt twiddling. Versioning `program.md` in git gives auditability: you know which prompt produced which behavior. Hill-climbing with guardrails (no unbounded autonomy for the meta-agent) keeps the outer loop from melting production policies.

This pattern shines in research and internal tooling where tasks are repeatable.

### In practice

Keep benchmarks **small but representative**; guard against overfitting to a dozen trivia questions. Require the meta-agent to cite which eval regressed before merging a prompt change. Use separate holdout sets updated monthly to detect drift.

### Failure modes this design mitigates

Manual prompt editing in chat lacks reproducibility and blame assignment. Automated hill-climbing without rollback risks **reward hacking** (shorter answers that score well but harm users). Versioned programs plus eval gates cap that damage.

### When to reconsider

If tasks are mostly one-off creative work, heavy benchmark loops mislead—invest in human preference sampling instead of pure autograding.

## Key takeaway

**Improve agents by iterating on a tracked artifact under eval pressure**, not by one-off chat tweaks.

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

- [Harness engineering](../../concepts/harness-engineering.md)
- [Autonomous loops](../../concepts/autonomous-loops.md)
- [Agent evaluation](../../concepts/agent-evaluation.md)
- [Autoagent harness patterns](../../research/autoagent-harness-patterns.md)
- [Feedback loops](../../concepts/feedback-loops.md)
