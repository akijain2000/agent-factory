# Agent vs Workflow: A Decision Framework

The core question is not “agents or not” but **where stochastic reasoning earns its place** in a system otherwise implementable as code. Vendors (notably Anthropic) argue for **workflows first**: deterministic structure with explicit branches; add model judgment only where the payoff exceeds cost, latency, and risk.

## When a workflow wins

Choose deterministic workflows when:

- Rules are **stable** and **complete** enough to maintain.
- Correctness requires **certifiable** steps (finance, access control).
- Latency SLOs are tight and **variance** is unacceptable.
- Debugging must be **replayable** without nondeterministic drift.

Workflows excel as **chains, routers, state machines**, and **CRUD automations** with known data shapes.

## When an agent wins

Choose agentic loops when:

- Tool selection depends on **context** that is costly to encode as rules.
- Task decomposition is **data-dependent** and evolves per request.
- The environment is **semi-open** (browsers, tickets, logs) and heuristics rot quickly.

Agents pay for **flexibility** with higher **monitoring** and **evaluation** burdens.

## Anthropic-aligned synthesis

Map your product to **prompt chaining, routing, parallelization, orchestrator–workers, evaluator–optimizer** before adopting a free-form agent. Often a **small agent** sits inside one node of a larger deterministic graph.

## Cost and reliability tradeoffs

Agents increase **tail latency** and **failure diversity** (creative mistakes). Workflows increase **maintenance** when rules churn. Hybrid designs route **easy** paths deterministically and escalate **hard** paths to models.

## Risk framing

Irreversible side effects (payments, deletes, external comms) deserve **human gates** or **two-person rules** regardless of topology. Agents do not remove **accountability**—they shift it to **prompt, tool, and policy** owners.

## Practical decision checklist

1. Can a **junior engineer script** the happy path in a day? If yes, workflow-first.
2. Is failure **expensive** or **ambiguous**? Add **critique**, **tests**, or **HITL**—not more autonomy.
3. Do you have **evals**? Without them, prefer workflows until baselines exist.

## Vignette: refunds vs copywriting

**Refunds** (irreversible, policy-heavy) suit workflows with **explicit** approval and deterministic rules—even if a model **drafts** emails, the send action should be gated. **Marketing copy** variants (reversible, subjective) may tolerate more open-ended **agentic** exploration with human final review.

## Migration path

Start workflow-first; instrument **failure clusters** where rules churn weekly. Promote only those clusters into **tool-rich** agent nodes with budgets. This avoids boiling-the-ocean autonomy projects that stall on compliance review.

## Sources and further reading

- Anthropic, *Building Effective Agents*.
- OpenAI agent guidance on when autonomy helps.

## See also

- [Anthropic agent patterns](anthropic-agent-patterns.md)
- [Anti-patterns](anti-patterns.md)
- [Cost analysis](cost-analysis.md)
- [Multi-agent landscape](multi-agent-landscape.md)
- Concepts: [Progressive Complexity](../concepts/progressive-complexity.md), [Planning Strategies](../concepts/planning-strategies.md), [Guardrails](../concepts/guardrails.md), [Human-in-the-Loop](../concepts/human-in-the-loop.md)
- Course: [Agent Factory course](../../course/README.md)
