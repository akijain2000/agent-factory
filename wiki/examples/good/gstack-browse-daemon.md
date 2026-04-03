# gstack Browse Daemon: Headless Browser Agent

## Summary

gstack’s browse agent drives a headless browser through a **small, focused tool surface**: navigate, click, type, scroll, snapshot the accessibility tree, take screenshots, and assert state. The agent is optimized for QA and dogfooding: fast command round-trips, structured page snapshots, and optional before/after diffs for verification.

## Pattern

**Focused tool set, structured observations, diff-based verification.** Instead of exposing the entire DOM API, tools return normalized snapshots (e.g., YAML or JSON summaries) that models can reason over reliably. Screenshots supplement structure for layout regressions. Verification steps compare snapshots or hashes across actions.

## What makes it good

A narrow API keeps the model’s decision space manageable and makes failures interpretable (“element ref X not found” vs opaque script errors). Structured output at each step supports automated assertions in harnesses. Diff-based checks turn flaky “does it look right?” into repeatable comparisons, which is critical for CI and regression suites.

Latency-aware design (batched operations, minimal round-trips) prevents the agent loop from becoming prohibitively expensive for tight inner loops.

### In practice

Drive flows as **short scripts of commands** (navigate, wait for selector, snapshot) rather than one giant natural-language plan per page. Cache stable element refs only within a page generation; refresh after navigation. Pair every critical path with an assertion node in CI so failures block merges.

### Failure modes this design mitigates

Raw HTML dumps overwhelm models and leak noise; accessibility snapshots prioritize actionable nodes. Screenshot-only agents hallucinate clicks; combining structure + pixels catches layout-only bugs without losing interactability.

### When to reconsider

For static marketing pages with no auth flows, traditional visual regression (Percy-style) may be cheaper than a full browser agent. Use gstack-style agents when **interaction** and **state** matter, not just pixels.

## Key takeaway

**Browser agents win on ergonomics and observability**: constrain the surface area, return machine-friendly state, and verify with diffs—not with unbounded visual prose.

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

- [Tool design](../../concepts/tool-design.md)
- [Structured outputs](../../concepts/structured-outputs.md)
- [Agent testing patterns](../../concepts/agent-testing-patterns.md)
- [Observability](../../concepts/observability.md)
- [Gstack agent analysis](../../research/gstack-agent-analysis.md)
