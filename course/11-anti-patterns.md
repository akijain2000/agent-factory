# Module 11: Anti-Patterns

**Duration:** approximately 35 minutes  
**Prerequisites:** Modules 03, 05, 09, and 10 (for vocabulary); Module 02 optional.

---

## Learning objectives

By the end of this module, you should be able to:

- **Recognize** common agent anti-patterns from architecture diagrams, prompts, and runtime logs.
- **Diagnose** failures by mapping **symptoms** to likely root causes.
- **Simplify** over-engineered agent stacks when a smaller design meets the same goals with less risk.

---

## God agent: one agent tries to do everything

A **god agent** has a sprawling system prompt (“you are legal, medical, DevOps, and data science”), dozens of tools, and no clear **phase** or **scope**. Symptoms: inconsistent persona, wrong tool choice, long latency, and **no single owner** for errors.

**Fix:** Split by **capability** (read vs write tools) or **workflow phase** (plan, execute, verify). Narrow the default prompt; **escalate** to specialized configs only when needed.

**Review cue:** If your architecture diagram is one box labeled “AI,” you probably have a god agent—or a product decision to make explicit.

---

## Over-tooling: too many tools, LLM can’t choose

**Over-tooling** exposes many similar tools (`search_v1`, `search_v2`, `grep`, `ripgrep`, `file_search`). The model **hesitates**, **hallucinates** parameters, or calls the wrong layer.

**Fix:** **Consolidate** behind one well-documented tool with parameters; use **routing** (supervisor or classifier) to pick families of tools; measure **tool selection accuracy** in evals.

**Metric:** Track **tool-call error rate** (schema violations, 4xx from APIs) weekly. Spikes often precede user-visible regressions.

---

## Premature multi-agent: adding agents when one would suffice

**Premature multi-agent** adds “researcher + writer + editor” for tasks a **single loop** with reflection handles. You pay coordination, duplicated context, and **handoff bugs**.

**Fix:** Start **single agent + tools + optional reflection**; add a second agent only when metrics show **specialization** or **adversarial critique** wins.

**Rule of thumb:** If two agents share the **same tools** and **same success criteria**, merge them until proven otherwise.

---

## Context window abuse: stuffing too much context

**Context stuffing** pastes entire repos, long logs, or full thread history “just in case.” Symptoms: **lost middle** attention failures, high cost, slow turns, and **conflicting** older instructions.

**Fix:** **Retrieve** (RAG), **summarize** with anchors, **sliding windows** with explicit “state so far” blocks, and **priority truncation** (keep tool errors and user goals, drop pleasantries). See Module 12.

**Smell:** Users paste 5k-line logs “for context” and the agent summarizes them poorly—often the harness should **parse** logs into structured events first.

---

## Sycophantic loops: agent agrees with itself endlessly

**Sycophantic loops** occur when reflection or multi-agent critique **rubber-stamps** prior outputs (“looks good”) without new checks. The loop **terminates** without improving quality.

**Fix:** Require **evidence-bound** critique (“cite failing test name”), use **diverse prompts** or a **smaller critic model** with a rubric, and **compare** against baselines (golden outputs, linters).

**Test:** Freeze inputs; run critic with temperature 0. If critique text changes wildly across runs while claiming the same verdict, your loop is performative.

---

## Premature autonomy: full autonomy before guardrails

**Premature autonomy** grants write access, production deploys, or irreversible APIs before **confirmation**, **dry-run**, or **allowlists**. Symptoms: incidents, data loss, and loss of user trust.

**Fix:** **Progressive trust**: read-only default, human-in-the-loop for destructive ops, **sandbox** execution, and **observability** (Module 08 patterns).

Document **blast radius** per tool: if an agent can reach it, assume it eventually will.

---

## Study: AutoGPT’s evolution and context-stuffing pitfalls

Early **AutoGPT-style** agents demonstrated **long-horizon** loops—and **fragility**: goal drift, redundant sub-agents, and **unbounded** context growth. Lessons: **tight objectives**, **checkpointing**, **tool budgets**, and **explicit stop** conditions beat raw autonomy.

Pair with wiki **bad examples** of context-stuffed agents: they are useful **negative templates** for reviews.

---

## Diagnosis checklist: symptoms to likely anti-pattern

| Symptom | Consider |
|--------|----------|
| Wrong tool half the time | Over-tooling; unclear tool docs |
| Great plans, no execution | Planning without harness enforcement |
| Escalating token cost, quality flat | Context window abuse |
| “Team” of agents, same mistakes | Premature multi-agent; no distinct roles |
| Infinite “improvement” with no delta | Sycophantic loops |
| Incidents after “agent shipped” | Premature autonomy |
| Same bug across retries | Missing Reflexion memory or non-idempotent tools |
| Supervisor re-sends full chat each call | Handoff anti-pattern (Module 10) |

---

## When to simplify architecture

Simplify when:

- **Evals flatline** after adding complexity.  
- **P95 latency** grows faster than quality.  
- On-call spends time debugging **coordination**, not domain logic.

A sound simplification path: remove the **last** agent you added; keep tools and checkpoints; re-measure.

---

## Exercises

1. **Audit a design**  
   Take an agent spec (yours or from wiki/examples/bad). List anti-patterns, cite evidence (prompt excerpt, tool list, diagram), and propose **one** minimal change per issue.

2. **Decompose a god agent**  
   Draw a **before** diagram (one box) and **after** (planner, executor, verifier—or single agent with phases). Write one paragraph on **what state** crosses boundaries.

---

## Further reading

- [Anti-patterns research (wiki)](../../wiki/research/anti-patterns.md)
- [Bad examples (wiki)](../../wiki/examples/bad/) — e.g. [god-agent](../../wiki/examples/bad/god-agent.md), [over-tooled-agent](../../wiki/examples/bad/over-tooled-agent.md), [context-stuffing-agent](../../wiki/examples/bad/context-stuffing-agent.md), [premature-autonomy-agent](../../wiki/examples/bad/premature-autonomy-agent.md)
