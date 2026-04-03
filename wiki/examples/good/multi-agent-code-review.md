# Multi-Agent Code Review: Parallel Specialists and a Coordinator

## Summary

A code-review system fans out a pull request to **parallel specialists**: a linter-focused agent (style and static checks), a security agent (dependency and secret patterns), and a style/readability agent (naming, structure, docs). A **coordinator** merges findings into a single report with severities, file paths, and non-duplicated issues.

## Pattern

**Parallel fan-out with structured aggregation.** Each agent receives the same diff or file list but different rubrics and tool access (e.g., security may run grep for keys; linter consumes compiler output). The coordinator normalizes schemas, deduplicates overlapping comments, and resolves contradictions with explicit rules (security outranks nitpicks).

## What makes it good

Specialists can run concurrently, improving wall-clock time versus one omnibus reviewer. Narrow prompts reduce cross-domain confusion and make evaluations targeted (precision on secrets vs style). Structured aggregation prevents the user from reading three redundant essays.

The pattern maps well to CI: each agent is a job; the coordinator is a final step that posts one GitHub comment.

### In practice

Pass each specialist only the files they need (security: lockfiles and network code; style: changed non-generated sources). Feed deterministic signals first (compiler, unit tests) into prompts as facts, not as raw logs over 100KB. The coordinator should sort findings by severity and file path for human scanning.

### Failure modes this design mitigates

Single-reviewer models **blend severities** and miss rare security issues while nitpicking names. Specialists tune temperature and rubrics independently. Deduping prevents developer fatigue from three bots repeating the same comment.

### When to reconsider

On tiny diffs, fan-out overhead may dominate; use a single reviewer below a line-count threshold. Scale parallelism when diffs touch many modules or when security review warrants deeper passes in parallel.

## Key takeaway

**Fan out for breadth, coordinate for clarity**—parallel agents need a deterministic merge layer.

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
- [Agent evaluation](../../concepts/agent-evaluation.md)
- [Structured outputs](../../concepts/structured-outputs.md)
- [Agent testing patterns](../../concepts/agent-testing-patterns.md)
- [Andrew Ng patterns](../../research/andrew-ng-patterns.md)
