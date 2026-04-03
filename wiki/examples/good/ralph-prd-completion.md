# Ralph-Style PRD Completion: Git as Memory and Done Means Tested

## Summary

Ralph-like autonomous builders treat a product requirement document (PRD) as the **source of truth** for scope. The agent iterates in a loop: pick the next unchecked requirement, implement, **run tests or checks**, commit, and update the PRD or task list. **Git** holds history, branches, and diffs—serving as durable memory beyond the model context window.

## Pattern

**Git-based state plus explicit completion criteria.** Each increment ends with a verifiable artifact (code, test output, screenshot). The PRD or checklist tracks what “done” means; the agent is not finished until those gates pass. Rollbacks and bisects use normal version control.

## What makes it good

Context windows lie; git does not. Storing progress in the repo makes handoffs between sessions and humans trivial. Test verification reduces theater: the agent cannot mark a story complete without executable proof. The loop naturally supports CI: every commit can run the same checks humans trust.

### In practice

Break PRDs into **testable slices** (“API returns 404 for missing id”) rather than vague goals (“make it robust”). After each slice, run unit tests, linters, or smoke scripts; commit with messages that reference the requirement ID. Use branches so failed experiments do not contaminate main.

### Failure modes this design mitigates

Pure chat transcripts as “memory” are lossy and unreviewable. Git gives diffs, blame, and revert. Without tests, agents mark tasks done based on narrative confidence—executable checks keep them honest.

### When to reconsider

Exploratory spikes without clear acceptance criteria should not use full Ralph discipline; park them in scratch branches until the PRD hardens.

## Key takeaway

**Anchor autonomous building in version control and executable definitions of done.**

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
- [Agent testing patterns](../../concepts/agent-testing-patterns.md)
- [State management](../../concepts/state-management.md)
- [Harness engineering](../../concepts/harness-engineering.md)
- [Anatomy of a good agent](../../research/anatomy-of-a-good-agent.md)
