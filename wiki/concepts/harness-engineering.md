# Harness Engineering

## What it is

**Harness engineering** is the discipline of building **meta-agent control structures** around the model: **evaluation loops** that score intermediate work, **failure classifiers** that route errors to recovery strategies, **goal trackers** that align multi-step plans with terminal criteria, and **memory tiers** (working, episodic, semantic) with explicit read/write policies. The harness—not the prompt alone—makes capabilities **scalable** and **reliable**. Research and open systems such as **autoagent**, **autocontext**, and **HarnessOS** explore composable control graphs, automated context shaping, and operating-system-like runtimes for long-horizon agents.

## Why it matters for agents

Models are **stochastic** and **myopic** without scaffolding. Harness code enforces **invariants** (no tool without validation), **stops** runaway depth, and **standardizes** telemetry. Teams that only tweak prompts hit a ceiling; teams that engineer harnesses can swap models, add tools, and meet **SLOs** without redesigning the product each time.

Treat the harness as **product code**: it deserves the same **review bar** as payment services—tests, types, and architectural decision records when patterns change.

## How to implement it

1. **Evaluation loops:** after critical steps, run **checkers** (schema validators, unit tests on outputs, LLM-as-judge only with **human** baselines). Fail closed or repair with bounded retries.
2. **Failure classifiers:** map exceptions to `Transient`, `UserInput`, `Policy`, `ToolBug`; each maps to a **strategy** (retry, ask user, halt, escalate).
3. **Goal trackers:** maintain explicit **subgoals** with completion predicates; detect **stagnation** (repeated tool/args) and **scope creep** (new goals without authorization).
4. **Memory tiers:** working context in the window; **episodic** summaries in a store; **semantic** retrieval with ACLs. Define **promotion** rules (what gets remembered and when).
5. **Hooks:** `before_model`, `after_model`, `on_tool_result`, `should_stop`—keep side effects in tools, **policy** in hooks.
6. **Composable graphs:** represent branches (plan vs execute vs verify) explicitly; avoid **hidden** recursion through tools calling models without depth counters.

7. **Checkpoints:** persist minimal **resumable** state at stable boundaries so workers can restart after deploys without replaying expensive steps.

**Sources to study:** autoagent-style **orchestration** patterns, autocontext-style **automatic** context assembly, HarnessOS-style **process** abstractions for durable agents.

## Testing harnesses

Golden **traces** for hook ordering; property tests that **max depth** and **max spend** cannot be exceeded; fuzz **tool errors** to verify classifiers.

Property-based tests help prove **idempotency** of `on_tool_result` handlers when providers retry deliveries. Snapshot **policy bundles** when debugging “why did step 5 differ in prod?”

Document **invariants** the harness guarantees (e.g., “no HTTP tool without URL allow-list check”) and test them explicitly.

## Common mistakes

- **Fat tools** that embed planning inside a single call—bypasses observability.
- Unbounded **judge** loops burning budget without convergence criteria.
- Memory tiers without **GC**—stale beliefs persist forever.
- **Tight coupling** to one framework so harness logic cannot be unit tested.
- **Implicit** state in globals or thread-locals that breaks under async workers.
- Skipping **versioning** on harness **policy** JSON—impossible to replay old runs.

## References to course modules

These map to the **23-module Agent Factory course** (see [`../../course/README.md`](../../course/README.md) when published).

- **Module 03 — The Agent Loop** — wiring plan–act–observe control flow around the model.
- **Module 05 — Tool Design and Integration** — boundaries between model, tools, and runtime.
- **Module 22 — Self-Improvement and Harness Engineering** — graphs, checkpoints, and evolving harness behavior.

Full curriculum index: [`../../course/README.md`](../../course/README.md) (when present).

## See also

- [Agent Loop](agent-loop.md)
- [State Management](state-management.md)
- [Agent Evaluation](agent-evaluation.md)
- [Error Recovery](error-recovery.md)
- [Context Engineering](context-engineering.md)
- [Autonomous Loops](autonomous-loops.md)
