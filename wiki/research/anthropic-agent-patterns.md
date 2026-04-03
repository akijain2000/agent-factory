# Anthropic’s “Building Effective Agents”: Dissection

Anthropic’s *Building Effective Agents* argues for **simple, composable workflows** before reaching for open-ended autonomy. The essay is less a framework than a **design lens**: start with deterministic structure; add model judgment only where it earns its cost and risk.

## Workflows before agents

The headline guidance: many products need **prompt chains**, routers, and parallel workers—not a single agent that “figures everything out.” This reduces failure modes tied to **unbounded loops** and makes debugging **local**: which step failed, with what inputs.

## Prompt chaining

Sequential specialization—summarize, then extract, then classify—keeps each step **narrow** and testable. Chains trade latency for **predictability**; they excel when intermediate representations are **useful artifacts** (citations, tables) rather than throwaway scratchpad.

## Routing

A classifier or rules engine sends tasks to **different downstream prompts or tools**. Routing is the cheapest form of **conditional computation**; it prevents paying frontier-model prices on trivial intents.

## Parallelization

Fan-out subtasks (map) with deterministic merge (reduce) exploits **wall-clock** parallelism without multi-agent drama. Useful for research synthesis, multi-file code edits with independent chunks, or batched evaluations.

## Orchestrator–workers

A central planner delegates subtasks to workers that return **structured results**. Contrast with peer “swarm” chat: orchestrator–workers keeps **a single integration point**—critical for accountability and state consistency.

## Evaluator–optimizer

Generator plus **critic** loop (reflection) with clear stop rules. Strength: improves outputs when critique is **grounded** (tests, rubrics). Weakness: cost and **agreement bias** if critic shares the same blind spots.

## Implications for production

Treat each pattern as a **module** with schemas, timeouts, and observability. Prefer **explicit** failure propagation over conversational concealment. Combine patterns inside **graphs** or plain code—Anthropic’s value is choosing the **minimal** pattern set.

## Pattern selection rubric

| Signal | Lean workflow | Add model judgment |
|--------|----------------|--------------------|
| Branching rules stable | Routing in code | Rare |
| High-variance inputs | Router + specialist prompts | Yes |
| Need creative draft + checks | Chain | Evaluator–optimizer |
| Embarrassingly parallel tasks | Parallelization | Minimal |

Use the table as a **heuristic**, not law—measure with **evals** on your traffic.

## Interaction with multi-agent fashion

Anthropic’s framing is a **counterweight** to default multi-agent demos: orchestrator–workers is multi-agent, but **bounded** and **schema-first**. Prefer that over unconstrained peer dialogue when accountability matters.

## Measuring when you overfit autonomy

If incident postmortems repeatedly cite **unexpected tool paths** or **unbounded retries**, you likely need **more workflow** and **less agent**. If maintenance churns **giant** conditional trees weekly, a **router + specialist** agent may reduce rule entropy—verify with **A/B** cost and defect rates.

## Sources and further reading

- Anthropic, *Building Effective Agents* (official essay).
- Anthropic documentation on tool use and safety with untrusted content.

## See also

- [Agent vs workflow](agent-vs-workflow.md)
- [OpenAI agent patterns](openai-agent-patterns.md)
- [Andrew Ng patterns](andrew-ng-patterns.md)
- [Anti-patterns](anti-patterns.md)
- Concepts: [Progressive Complexity](../concepts/progressive-complexity.md), [Guardrails](../concepts/guardrails.md), [Planning Strategies](../concepts/planning-strategies.md), [Agent Composition](../concepts/agent-composition.md)
- Course: [Agent Factory course](../../course/README.md)
