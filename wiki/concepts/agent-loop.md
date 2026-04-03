# Agent Loop

## What it is

The **agent loop** is the control cycle that turns a language model into an autonomous system: read state and user goal, decide the next action (often a tool call or structured plan step), execute through a **harness**, observe results, and repeat until a **stop condition** fires. The **ReAct** (reasoning + acting) pattern makes this explicit in the transcript: short natural-language rationale, then a tool invocation, then observation, in alternation. Every production agent is a loop wrapped in timeouts, budgets, and policy—not a single completion.

## Why it matters for agents

Chat-style single-shot generation cannot reliably complete multi-step tasks with side effects. The loop is where **tool use**, **error recovery**, **memory injection**, and **guardrails** attach. Without a clearly implemented loop, behavior fragments across callbacks, retries duplicate work, and operators cannot trace *why* step *n* happened. The loop is also the natural place to enforce **max steps**, **max wall time**, and **max spend** per run.

## How to implement it

1. **Define stop conditions** in code and mirror them in `system-prompt.md`: task complete, user message received, unrecoverable error, budget exhausted, or explicit halt tool.
2. **Single-step loop:** one model call per iteration; parse tool calls; execute; append assistant + tool messages; continue. Simplest to test and trace.
3. **Multi-step / planner loop:** an outer loop for high-level goals and an inner loop for execution, or a graph (e.g., LangGraph) where nodes are model or tool steps. Keep *who advances the counter* unambiguous.
4. **Observation channel:** normalize tool results into messages the model can parse (structured JSON plus short human-readable summary).
5. **Reflection:** optional final pass where the model checks outputs against constraints before returning to the user; keep it bounded (one extra call or a classifier).

**Single vs multi-step:** a single loop with one model call per iteration is easier to debug. Multi-step inner loops reduce round-trips but increase the chance of coherent-looking wrong plans; compensate with stricter schemas and tests.

**When to break the loop:** on success, on fatal errors, when no progress is detected (same tool/args repeated), or when escalation to human is required. Never rely on the model alone to “know” when to stop.

## Instrumentation and testing

Emit a **span per iteration** with fields: `iteration_index`, `tool_names`, `token_delta`, and `stop_reason` (null until terminal). Golden tests should assert invariants: no tool call without a preceding model generation, max steps never exceeded, and terminal states map to documented enums. For ReAct transcripts, snapshot tests help catch harness regressions when upgrading SDKs. If you support **streaming**, still parse the final assistant message and tool calls from the completed turn before executing tools—partial JSON is not an action.

## Anti-patterns in loop design

Mixing **business logic inside prompt-only branches** (“if the user sounds angry, call refund”) without code-level policy creates audit gaps. Prefer explicit classifiers or rules engines for sensitive branches, with the loop recording which branch fired. Another failure mode is **double execution**: the harness and the model both “helpfully” repeating a tool call after a timeout; dedupe using idempotency keys and stable request ids per iteration.

## Mapping to production harness code

Your orchestrator should expose: `run_loop(initial_state) -> TerminalState`, with hooks `before_model`, `after_model`, `on_tool_result`, and `should_stop`. Keep **side effects** inside tool implementations, not inside the model wrapper—this preserves testability when you swap models. For synchronous HTTP APIs, return **202 + run id** for long loops and stream events; avoid holding a request open unbounded.

## Common mistakes

- **Unbounded runs:** no max steps or wall clock; tab close is the only kill switch.
- **Hidden loops:** tools that internally call the model again without depth limits (**recursive self-spawn**).
- **Soup observations:** pasting raw HTML or stack traces into context without structured error types.
- **Treating reflection as free:** unbounded self-critique chains that burn tokens without measurable quality gain.

## References to course modules

These map to the **23-module Agent Factory course** (see [`../../course/README.md`](../../course/README.md) when published).

- **Module 03 — The Agent Loop & Control Flow** — lifecycle of a run, iteration boundaries, stop conditions.
- **Module 04 — ReAct, Tool Calling, and the Harness** — wiring plan-act-observe into your runtime.
- **Module 21 — Observability & Tracing** — correlating spans across loop iterations.

Full curriculum index: [`../../course/README.md`](../../course/README.md) (when present).

Treat the loop as the **product surface** for reliability: if iteration boundaries are fuzzy, every other pattern (memory, tools, safety) becomes harder to reason about.

## See also

- [State Management](state-management.md)
- [Error Recovery](error-recovery.md)
- [Planning Strategies](planning-strategies.md)
- [Context Window Management](context-window-management.md)
- [Autonomous Loops](autonomous-loops.md)
- [Harness Engineering](harness-engineering.md)
