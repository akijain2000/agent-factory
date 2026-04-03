# Multi-Agent Orchestration

## What it is

**Multi-agent orchestration** coordinates multiple LLM-driven actors to complete work: **supervisor pattern** (a lead delegates and reviews), **sequential pipeline** (stages hand off artifacts), **parallel fan-out** (subtasks concurrently, then aggregate), **debate** (adversarial or diverse roles challenge drafts), and **consensus** (voting or judge model picks a winner). Frameworks (CrewAI, LangGraph, custom) provide structure; the principles are routing, aggregation, and **bounded autonomy** per worker.

## Why it matters for agents

Specialized prompts and tools per role can beat one general agent on complex workflows—if coordination overhead stays below value gained. Orchestration is also a **governance** tool: supervisors enforce style, policy, and tool allowlists before workers act.

## How to implement it

1. **Supervisor:** maintain shared state or message bus; workers return structured results; supervisor decides continue, retry, or escalate.
2. **Sequential pipeline:** strict interfaces between stages (`StageOutput` schema); fail fast on schema violations.
3. **Parallel fan-out:** idempotent tasks; aggregate with deterministic merge; cap concurrency; handle partial failures explicitly.
4. **Debate/consensus:** limit rounds; define scoring rubric or judge instructions; avoid infinite argument loops.
5. **Shared context policy:** what each agent may read (PII partitions, tenant scoping).

**When multi-agent helps:** diverse expertise, parallelizable research, high-stakes verification, or clear role boundaries. **When it is premature:** simple FAQ bots, tight latency budgets, or teams lacking observability for multi-actor traces—start single-loop with good tools.

## Topology selection

| Pattern        | Best when                          | Watchouts                          |
|----------------|-------------------------------------|------------------------------------|
| Supervisor     | Need central policy enforcement     | Supervisor becomes bottleneck      |
| Pipeline       | Stable stage ordering               | Brittle if mid-stage often fails   |
| Fan-out        | Embarrassingly parallel subtasks    | Partial failure aggregation        |
| Debate/judge   | High-stakes correctness           | Costly; define stop criteria       |

Start with the **smallest** topology that meets governance needs; add agents when traces show repeated rework or policy violations a supervisor could catch earlier.

## Observability requirements

Every sub-agent run should inherit the **root trace id** and add a **child span** with `agent_role`, `parent_span_id`, and `delegation_reason`. Metrics: fan-out **concurrency**, **merge latency**, and **supervisor revision rate** (how often outputs are sent back for fixes). Dashboards without these become blind during incidents.

## Common mistakes

- **Agent explosion** without shared trace id across actors.
- **Messy handoffs** (opaque string blobs) between workers.
- **Duplicate work** because no central task ledger.
- **Supervisor as god model** re-solving everything instead of gating.

## References to course modules

These map to the **23-module Agent Factory course** (see [`../../course/README.md`](../../course/README.md) when published).

- **Module 10 — Multi-Agent Patterns** — supervisors, workers, and coordination topologies.
- **Module 07 — Planning and Reasoning** — staged execution and explicit replan triggers.
- **Module 19 — Observability and Debugging** — shared trace IDs, spans, and coordination signals.

Full curriculum index: [`../../course/README.md`](../../course/README.md) (when present).

## See also

- [Agent Handoffs](agent-handoffs.md)
- [Planning Strategies](planning-strategies.md)
- [State Management](state-management.md)
- [Observability](observability.md)
- [Agent Orchestration Platforms](agent-orchestration-platforms.md)
