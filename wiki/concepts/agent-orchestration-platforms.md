# Agent Orchestration Platforms

## What it is

**Agent orchestration platforms** manage **teams** of agents as operational units: **goal assignment** (queues, prioritization, SLAs), **cost tracking** (per agent, per customer, per tool), **work dashboards** (status, blockers, approvals), and **agent-as-employee** patterns (roles, shift handoffs, performance reviews via evals). They sit above single-run harnesses—coordinating **many** concurrent automations with **human** managers in the loop. Research and products in the **paperclip** and **aperant** line of thinking treat orchestration as **work management** for machine labor, not only as chat endpoints.

## Why it matters for agents

One agent is a script; **fifty** agents are an **organization** problem. Without platforms, work duplicates, **budgets** collide, and nobody knows which agent owns a customer thread. Dashboards and **cost** attribution turn experiments into **services** finance can understand.

Platforms also encode **culture**: how you name agents, tag work, and review outcomes shapes whether machine labor is **legible** to the rest of the company.

## How to implement it

1. **Work model:** represent tasks as **jobs** with priority, deadline, owning **agent profile**, and **dependencies**. Use a queue or workflow engine with **visibility** timeouts.
2. **Goal assignment:** route by **skill tags**, **load**, and **SLA**; support **escalation** to stronger models or humans when stuck.
3. **Cost tracking:** tag every span with `agent_id`, `team`, `customer_id`; roll up **token**, **tool**, and **infra** cost daily.
4. **Dashboards:** show **backlog**, **in progress**, **blocked** (policy, missing input), **done**; drill down to **traces** for audits.
5. **Agent-as-employee:** define **RACI**—which agent **recommends**, which **executes**, which **approves**; align with **HR**-style onboarding (evals, access reviews).
6. **Inter-agent protocols:** message schemas or **A2A**-style contracts for handoffs; avoid **ad hoc** string passing without schemas.

7. **Runbooks for fleets:** define how to **pause** all agents, drain queues, and **fail over** when a shared tool degrades.

**Paperclip**-style systems stress **ops** visibility and **multi-agent** workload management. **Aperant**-style framing emphasizes **governance** and **economic** controls on machine workforces.

## Multi-tenant fairness

Isolate **queues** and **budgets** per tenant; prevent one customer’s agent swarm from starving shared **tool** pools.

Expose **forecast** views when backlog growth correlates with marketing events or product launches—ops should see demand spikes before **SLA** breaches.

Integrate **finance** views: projected monthly **token** spend by team prevents surprise invoices when agent adoption spikes.

Define **SLOs** per queue (time-to-first-action, time-to-resolution) the same way you would for human teams.

## Common mistakes

- **Spawning** agents without **parent** run correlation—impossible to debug.
- Dashboards that show **counts** but not **quality** or **cost**.
- **Flat** org of identical agents instead of **specialized** roles with clear interfaces.
- Omitting **human** escalation when queues age beyond SLA.
- **Anonymized** dashboards that hide which **tenant** is burning budget.

## References to course modules

These map to the **23-module Agent Factory course** (see [`../../course/README.md`](../../course/README.md) when published).

- **Module 10 — Multi-Agent Patterns** — roles, coordination, and handoffs across agents.
- **Module 13 — Framework Selection** — choosing orchestration platforms and runtimes.
- **Module 20 — Deployment and Scaling** — operating agent fleets under load.

Full curriculum index: [`../../course/README.md`](../../course/README.md) (when present).

## See also

- [Multi-Agent Orchestration](multi-agent-orchestration.md)
- [Agent Handoffs](agent-handoffs.md)
- [Cost Optimization](cost-optimization.md)
- [Observability](observability.md)
- [Human-in-the-Loop](human-in-the-loop.md)
