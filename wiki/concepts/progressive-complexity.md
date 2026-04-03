# Progressive Complexity

## What it is

**Progressive complexity** is an engineering strategy: ship the **simplest system that solves the problem**, then add autonomy, tools, and multi-step reasoning only when measured need appears. A common ladder is **augmented LLM** (single call with retrieval or a function) → **single agent loop** (plan, act, observe) → **multi-agent** or hierarchical orchestration. This aligns with practitioner guidance (including **Anthropic**’s emphasis on **workflows before agents**): deterministic pipelines and human-visible steps often beat opaque agent graphs for reliability.

## Why it matters for agents

Jumping straight to multi-agent or long autonomous loops maximizes **failure modes**, cost, and debug surface area. Incremental rollout ties each layer to **evaluations** and **observability** you actually use. Teams that skip the ladder struggle to attribute regressions: was it routing, a sub-agent, or a tool?

## How to implement it

1. **Start augmented:** one model call with strict output schema, optional retrieval, optional single tool—no loop until you have failing cases that need iteration.
2. **Introduce a bounded loop:** cap steps, time, and tools; log traces; add recovery policies before adding branching planners.
3. **Split workflows vs agents:** if transitions are fixed, encode a state machine or DAG; reserve agents for variable decomposition you cannot enumerate.
4. **Add tools narrowly:** each tool should earn its place via real tasks; avoid exposing the whole API at once.
5. **Escalate to multi-agent** when roles are genuinely distinct (e.g., coder vs reviewer), communication bandwidth is bounded, and handoff contracts are clear.
6. **Gate promotions:** require offline evals and shadow traffic before granting broader autonomy.

## Anthropic-style workflow-first framing

Prefer **explicit steps** (retrieve → classify → draft → verify) with checkpoints over a free-form “figure it out” loop. Insert **human approval** at expensive or irreversible transitions early; automate only after metrics justify it.

## Signals you need more complexity

Repeated failures that a single pass cannot fix; need for parallel exploration; distinct expertise domains with low crosstalk. Absent those, complexity is likely negative value.

## Migration path

Start with **feature flags** that enable the loop or a second agent for a slice of traffic. Keep **rollback** one toggle away. Document **parity** requirements: the simple path and complex path should agree on safety invariants even if capability differs.

## Measuring each layer

Instrument **success rate**, **cost per task**, and **time to resolution** at each complexity tier. If the augmented path hits product goals, defer the loop until a metric gap appears. Use **holdout** groups to prevent org-wide complexity creep without evidence.

## Documentation and onboarding

New engineers should read the **simplest** path first. Architecture diagrams should show optional layers as add-ons, not the default mental model. This reduces accidental coupling to advanced features during routine fixes.

## Common mistakes

- Multi-agent theater: several models chatting without clear division of responsibility.
- Unbounded loops before basic logging and budgets exist.
- Automating a messy manual process without first simplifying the process.
- Treating “agent” as a requirement from day one instead of an optimization.

## References to course modules

These map to the **23-module Agent Factory course** (see [`../../course/README.md`](../../course/README.md) when published).

- **Module 01 — From Prompt to Product** — when a single call suffices.
- **Module 02 — Workflows, State Machines, and DAGs** — structured automation before agents.
- **Module 10 — Multi-Agent Roles & Specialization** — justified decomposition.

Full curriculum index: [`../../course/README.md`](../../course/README.md) (when present).

## See also

- [Agent Composition](agent-composition.md)
- [Planning Strategies](planning-strategies.md)
- [Agent Loop](agent-loop.md)
- [Cost Optimization](cost-optimization.md)
- [Agent Evaluation](agent-evaluation.md)
