# Agent Testing Patterns

## What it is

**Agent testing patterns** cover how to verify agents beyond ordinary unit tests: **unit tests for tools** (contracts, timeouts, idempotency), **integration tests for agent flows** (harness + model stub or recorded completions), **behavioral tests** for end-user outcomes and tone, **trace-based testing** (assert ordered spans and tool args), and **snapshot testing** for stable textual outputs where variability is low. The goal is confidence that **prompt, tools, and policy** evolve without silent regressions.

## Why it matters for agents

Nondeterminism and long chains make “it works on my machine” insufficient. Structured tests localize failures: bad schema vs bad routing vs model drift. They are prerequisites for **CI gates**, **model upgrades**, and **refactors** of composition or memory.

## How to implement it

1. **Tool unit tests:** feed representative and malformed inputs; assert error codes; mock upstream HTTP with contract fixtures.
2. **Flow integration:** drive the agent loop with a **fake LLM** that returns scripted tool calls and final messages; verify state transitions and stop conditions.
3. **Behavioral scenarios:** natural-language user turns with rubric checks (regex or LLM judge in CI with pinned prompts); assert final structured output fields.
4. **Trace assertions:** export spans from test runs; assert tool names, ordering, and redaction rules (no secrets in attributes).
5. **Snapshots:** freeze golden responses for deterministic stubs; review diffs intentionally when prompts change.
6. **Flake control:** set temperature to 0 for regression tests; record seeds where the runtime supports them.

## CI strategy

Fast tier: tools + stubbed loop. Nightly: small live-model suite with budget caps. Block deploy on fast tier failures; trend nightly drift.

## Trace-based testing details

Serialize spans to JSON in CI and assert with **stable ordering** keys. Allow optional spans (retries) via flexible matchers. Redact dynamic ids in snapshots while preserving **topology** (tool A before tool B). Fail tests with **diff-friendly** output when traces diverge.

## Snapshot testing boundaries

Use snapshots for **tool arguments** and **structured** final answers, not for exploratory prose. When updating snapshots, require **paired** eval or product review so changes are intentional.

## Property-based angles

Generate random but valid tool inputs (Hypothesis, fast-check) to find edge cases in adapters. Combine with **mutation** of recorded traces to ensure the harness handles out-of-order tool responses defensively.

## Common mistakes

- Only testing tools while the prompt roams untested in production.
- Brittle full-string match on model prose that legitimately varies.
- No negative tests for guardrails (injection, excessive tools, policy bypass attempts).
- Ignoring timing: flaky tests from real network without hermetic mocks.

## Quick checklist

- Tool contract tests run **without** calling a live LLM.
- Stubbed loop tests assert **state** and **trace topology**, not only strings.
- Live-model nightly jobs have **token budgets** and failure artifacts attached.

## References to course modules

These map to the **23-module Agent Factory course** (see [`../../course/README.md`](../../course/README.md) when published).

- **Module 17 — Agent Evaluation and Testing** — scenarios, golden traces, and CI for agents.
- **Module 05 — Tool Design and Integration** — contracts and boundaries under test.
- **Module 19 — Observability and Debugging** — using spans and traces as test artifacts.

Full curriculum index: [`../../course/README.md`](../../course/README.md) (when present).

## See also

- [Agent Evaluation](agent-evaluation.md)
- [Structured Outputs](structured-outputs.md)
- [Tool Design](tool-design.md)
- [Error Recovery](error-recovery.md)
- [Observability](observability.md)
