# Multi-Agent Landscape (2024–2026): What Works, What Does Not

Multi-agent systems promise **parallelism** and **specialization**; they also multiply **coordination cost**. This survey maps dominant topologies—supervisor, swarm, sequential pipelines, parallel map—against observed strengths and failure modes in research and product practice.

## Supervisor (orchestrator–workers)

A central agent **decomposes**, assigns, and **integrates**. Strengths: clear accountability, simpler global state policy (single planner). Weaknesses: supervisor becomes a **bottleneck** and single point of misconvergence if its world model drifts.

**Works when** subtasks have crisp interfaces and the orchestrator has **good observability** into worker outputs (schemas, tests).

## Swarm / peer mesh

Agents negotiate peer-to-peer or via a shared channel. Strengths: flexible, academically interesting for open-ended exploration. Weaknesses: ambiguous **ownership**, duplicate work, hard-to-debug **message storms**.

**Works when** tasks are **embarrassingly parallel** with merge functions, or in research sandboxes—not as default for regulated production without heavy guardrails.

## Sequential specialization

Pipeline of roles (triage → specialist → reviewer) without dynamic topology. Strengths: predictable cost and latency profiles; easy to test each stage. Weaknesses: error **propagation** requires explicit contracts; early-stage mistakes compound.

**Works when** stage inputs/outputs are **typed** and you can **short-circuit** the pipeline on low-confidence classifications.

## Parallel map–reduce

Fan-out identical operations over shards (files, tickets, documents) then deterministic reduce. Strengths: excellent **wall-clock** scaling; minimal agent chatter. Weaknesses: reduce step can be **subtle** if conflicts arise across shards.

**Works when** merge logic is **code**, not model improvisation.

## Hybrid industrial pattern

Production systems often combine **routing** (cheap) with **small fixed teams** (e.g., builder + critic) and **human gates** on irreversible tools. Pure “emergent collaboration” is rare where **SLOs and audit** matter.

## What does not work (reliably)

- **Unbounded peer debate** without termination proofs.
- **Shared scratchpads** without single-writer rules.
- **Recursive delegation** without depth limits (cost explosions).
- **Homogeneous multi-agent** (same prompt copy) expecting diversity—better to vary **temperature, tools, or rubrics**.

## Evaluation takeaway

Measure **end-to-end task success**, cost, and latency—not conversational plausibility. Multi-agent wins show up in **parallel speedups** or **separation of concerns**; losses show up as integration bugs invisible to each agent locally.

## Topology cheat sheet

- **Need strict audit trail?** Prefer supervisor or sequential pipelines.  
- **Need max throughput on independent shards?** Parallel map–reduce.  
- **Exploring novel research?** Swarm with lab-only guardrails.  
- **Production customer impact?** Avoid swarm unless tightly capped.

## Industry anecdotes (pattern-level)

Teams reporting success often had **small** fixed topologies (2–3 agents) with **schema-first** handoffs. Teams reporting pain often had **dynamic** role spawning without centralized **task IDs**—debugging became forensic chat archaeology.

## Sources and further reading

- Anthropic, *Building Effective Agents* (orchestrator–workers, parallelization).
- Andrew Ng’s multi-agent pattern framing.
- A2A protocol discussions for cross-framework delegation.

## See also

- [A2A deep dive](a2a-deep-dive.md)
- [Anti-patterns](anti-patterns.md)
- [Andrew Ng patterns](andrew-ng-patterns.md)
- [Agent evaluation methods](agent-evaluation-methods.md)
- Concepts: [Multi-Agent Orchestration](../concepts/multi-agent-orchestration.md), [Agent Handoffs](../concepts/agent-handoffs.md), [State Management](../concepts/state-management.md)
- Course: [Agent Factory course](../../course/README.md)
