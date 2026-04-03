# Planning Strategies

## What it is

**Planning** is any process that decomposes a goal into steps before or during execution. Patterns include **Chain of Thought** (linear intermediate reasoning), **Tree of Thoughts** (branching, scoring, pruning), explicit **task decomposition** (checklists, substeps), **plan-then-execute** (separate planning phase then fixed execution), and **iterative refinement** (draft, critique, revise in multiple passes).

## Why it matters for agents

Complex tasks fail when the model improvises tool order without lookahead. Planning improves dependency ordering, exposes missing tools early, and supports **human-in-the-loop** review of a plan before expensive actions. Over-planning, however, adds latency, tokens, and failure modes (beautiful plans that ignore tool errors).

## How to implement it

1. **CoT:** allow short rationale before tool calls in ReAct-style loops; cap length in system prompt. Consider hiding rationale from end users if policy requires.
2. **ToT:** generate N branches, score with a rubric or second model, prune; use only when task search space is small and value warrants cost; add hard limits on branches and depth.
3. **Task decomposition:** emit structured plan objects (JSON) validated by schema; executor steps through or hands subtasks to workers.
4. **Plan-then-execute:** freeze plan version `v`; if observations invalidate assumptions, bump to `v+1` with a *replan* node rather than silent drift.
5. **Iterative refinement:** single domain (e.g., code or prose) with bounded rounds; stop when diff below threshold or max iterations.

**When planning helps:** multi-tool dependencies, high blast-radius mutations, compliance checkpoints, or novel user goals. **When it hurts:** trivial lookups, latency-sensitive chat, or environments where observations are too noisy for stable plans—prefer tight reactive loops with strong tools.

## Cost and latency controls

Attach **token ceilings** to planning passes: if the planner exceeds budget, fall back to a single-step ReAct policy. For ToT, predefine **beam width** and **depth**; log how often pruning discards all branches (signal the task may be ill-posed). **Plan caching** keyed by normalized goal can help repeated admin tasks—invalidate cache when tool schemas or policies change.

## Evaluation notes

Measure not only final answer quality but **plan adherence** (did execution skip mandatory steps?) and **replan quality** after injected tool failures. Offline suites with perturbed observations reveal whether your planner overfits to happy-path demos.

## Human-visible vs internal planning

If users should see plans (approval UX), render structured steps; if planning is internal, avoid dumping raw CoT to clients—store internal rationale in ops-only logs when permitted by policy. Align with legal/compliance on **retention** of reasoning traces.

## Common mistakes

- **Planning theater:** long plans never synchronized with actual tool capabilities.
- **Unbounded ToT:** exponential branching without scoring discipline.
- **No replan trigger:** executing obsolete plans after tool failure.
- **Leaking internal CoT** to users or logs when it contains sensitive inference.

## References to course modules

These map to the **23-module Agent Factory course** (see [`../../course/README.md`](../../course/README.md) when published).

- **Module 10 — Reasoning Patterns: CoT, ToT, Reflexion** — tradeoffs and controls.
- **Module 14 — Plan–Execute & Replanning** — integrating plans with the harness.
- **Module 19 — Agent Evaluation & Offline Metrics** — plan adherence and replan quality.

Full curriculum index: [`../../course/README.md`](../../course/README.md) (when present).

Prefer **measured** planning: if offline eval shows no lift over reactive ReAct for your domain, delete the planner and reclaim latency.

Pair planners with **simulated tool stubs** in CI so plans do not silently reference retired capabilities.

## See also

- [Agent Loop](agent-loop.md)
- [Multi-Agent Orchestration](multi-agent-orchestration.md)
- [State Management](state-management.md)
- [Human-in-the-Loop](human-in-the-loop.md)
- [Progressive Complexity](progressive-complexity.md)
