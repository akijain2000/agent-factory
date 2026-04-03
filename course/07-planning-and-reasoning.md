# Module 07: Planning and Reasoning

**Duration:** approximately 40 minutes  
**Prerequisites:** Module 03 (The Agent Loop); Module 06 (Memory and Context) optional for scratchpad-style plans.

---

## Learning objectives

By the end of this module, you should be able to:

- **Implement** planning strategies inside agent loops using explicit reasoning steps.
- **Apply** Chain of Thought, Tree of Thoughts, and task decomposition where they improve reliability.
- **Use** plan-then-execute versus iterative execution deliberately.
- **Recognize** when planning overhead hurts latency, cost, or accuracy (over-planning, analysis paralysis).

---

## 1. Chain of Thought in agent loops

**Chain of Thought (CoT)** asks the model to expose intermediate reasoning before an action or answer. In agents, CoT is not only for the final reply—it shapes **tool selection** and **argument construction**.

Patterns:

- **Prefix** each assistant turn with a short “Thought:” block (internal or user-visible per your product).
- **Require** the model to state **preconditions** it checked (“I need the file path; I will list the directory first”).
- **Ground** thoughts in tool outputs (“Tool returned 404; hypothesis: wrong branch”).

Example (illustrative):

```text
Thought: User wants migrations applied. I must confirm DB URL and migration directory.
Action: call tool list_dir(path="db/migrations")
```

CoT increases tokens; use **length limits** and discourage repeating unchanged plans every turn.

---

## 2. Tree of Thoughts: exploring multiple strategies

**Tree of Thoughts (ToT)** explores **several branches**—candidate plans or hypotheses—before committing. Useful when:

- The task is **under-specified** and multiple interpretations exist.
- Early mistakes are **expensive** (destructive file ops, financial actions).

Implementation sketch:

1. Generate `k` short candidate approaches (low temperature, structured bullets).  
2. **Score** or critique them (self-critique, second model, or heuristic checks).  
3. **Expand** the best one or two branches into concrete steps.  
4. Execute with checkpoints.

ToT is costly. Default to **single-path CoT**; escalate to ToT when confidence is low or stakes are high.

---

## 3. Task decomposition

**Decomposition** breaks a goal into **ordered or parallelizable** sub-tasks with clear completion criteria.

Good sub-tasks are:

- **Observable** — you can tell when done (`tests pass`, `file exists`).  
- **Sized** for one tool burst or a short model turn.  
- **Dependency-aware** — explicit edges (“after schema migration, run seed script”).

Example decomposition for “migrate API clients to v2”:

```markdown
1. Inventory v1 call sites (static search).
2. Map v1 endpoints to v2 (read OpenAPI diff).
3. Refactor module A; run unit tests.
4. Refactor module B; run integration tests.
5. Update docs and changelog.
```

Feed the **current sub-task id** to the model so it does not drift.

---

## 4. Plan-then-execute pattern

**Plan-then-execute** separates **planning** from **execution**:

1. Produce a plan (steps, tools, risks).  
2. Human or automated **approval** optional.  
3. Execute steps **mechanically**, refreshing the plan only when the world changes.

Benefits: auditable plans, easier HITL gates, less thrashing. Risks: stale plans when environments are dynamic—add **replan triggers** (tool error, unexpected diff, user correction).

---

## 5. Study: AutoAgent’s `program.md` as planning interface

AutoAgent-style harnesses often treat **`program.md`** (or equivalent) as the **living plan**: markdown checklists, step status, and notes the agent updates after each major action. The file is **durable context** outside the sliding chat window.

Patterns to copy:

- **Checklist semantics** — `- [ ]` / `- [x]` for human and model readability.  
- **Timestamped notes** when assumptions change.  
- **Single writer discipline**—merge conflicts avoided by serializing agent writes through the harness.

This turns planning into a **first-class artifact** you can diff, review, and resume.

---

## 6. When planning hurts

**Over-planning**  
The model spends thousands of tokens outlining work it could start immediately. Symptom: long plans with no tool calls. Fix: **step budgets**, “plan max 5 bullets,” or **interleaved** plan-update only after each milestone.

**Analysis paralysis**  
ToT with too many branches or repeated self-critique without action. Fix: cap branches, require **first executable step** within N tokens.

**Brittle plans**  
Static plans in chaotic environments. Fix: **short horizons** (plan two steps, execute, replan).

**Cost and latency**  
Every reasoning pass is billed. CoT/ToT should be **adaptive**, not default-on for trivial tasks.

---

## Exercises

1. **Implement task decomposition** for a file migration agent (e.g., moving `src/legacy/` to `src/modules/`). Write a `program.md` skeleton with at least eight checkboxes, dependencies called out, and explicit verification steps (build, test, grep for stale imports).

2. **Compare plan-then-execute vs iterative** approaches for the same task (e.g., “fix flaky CI”). Write a half-page analysis: when you would choose each, what failure modes differ, and how you would instrument metrics (steps to green, tokens, wall time).

---

## Further reading

- [Planning strategies](../../wiki/concepts/planning-strategies.md)
- [AutoAgent harness patterns](../../wiki/research/autoagent-harness-patterns.md)

---

## Summary

Planning is a **control strategy**, not a personality trait. CoT improves tool use quality; ToT helps under ambiguity; decomposition and `program.md`-style artifacts make long tasks **resumable**. Choose plan-then-execute when auditability matters, and stay ready to **replan** when reality diverges. Skip deep planning when the task is small or the environment is too volatile for static plans.
