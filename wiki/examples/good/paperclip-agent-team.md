# Paperclip-Style Agent Team: Ownership, Costs, and “Employees”

## Summary

Following Paperclip-like orchestration, work is assigned to **named agents with clear ownership**: each has a charter, allowed tools, and budget. A central layer tracks **cost** (tokens, tool calls, wall time) per agent and task, surfacing spend the way a manager would track an employee’s utilization—not as a post-hoc surprise.

## Pattern

**Agent-as-employee with visible economics.** Tasks carry goals, deadlines, and spend caps. Agents pull from a queue or receive delegations; the orchestrator resolves conflicts and prevents duplicate work. Cost and outcome metadata feed dashboards and retrospectives.

## What makes it good

Ownership eliminates ambiguous “everyone owns everything” multi-agent failures. Cost visibility forces product decisions: which steps deserve cheaper models, which need humans, and where caching wins. Modeling agents like roles clarifies hiring metaphors—onboarding a new agent means documenting scope, tools, and success metrics.

### In practice

Instrument per-agent spend and attach it to Jira or Asana tickets. Define SLAs: max wall time before escalation, max dollars per task. Use queues with priorities so high-value work is not starved by chatty low-value jobs.

### Failure modes this design mitigates

Anonymous swarms of agents duplicate work, drift from brand voice, or fight over shared resources. Named ownership plus budgets makes pathologies visible in dashboards rather than in angry finance emails.

### When to reconsider

For prototypes, full economic modeling may be premature—start with **step caps** and add per-agent accounting once spend exceeds a pain threshold.

## Key takeaway

**Multi-agent orchestration is also an operations problem**: align ownership and make costs first-class metrics.

## Review checklist

- [ ] Is the active tool set small enough to name from memory?
- [ ] Are transitions or handoffs explicit in code, not only in prose?
- [ ] Do traces identify phase, tool, and outcome for each step?
- [ ] Are step, cost, and time limits enforced in the host, not the model?
- [ ] Can you replay a failed run with mocks for tools and LLM?
- [ ] Are high-risk actions behind sandbox, schema validation, or human approval?

## Metrics and evaluation

Define SLIs for the loop: success rate per task type, median steps to completion, tool-error ratio, and cost per successful outcome. Store traces with default PII redaction and retain enough detail to replay decisions. Run periodic canaries on pinned prompts and tool versions to catch provider or dependency drift before users do.

## Contrast with common failures

For unstructured alternatives and their failure modes, see [God agent](../bad/god-agent.md), [Over-tooled agent](../bad/over-tooled-agent.md), and the wiki [Anti-patterns](../../research/anti-patterns.md) catalog.

## See also

- [Multi-agent orchestration](../../concepts/multi-agent-orchestration.md)
- [Cost optimization](../../concepts/cost-optimization.md)
- [Observability](../../concepts/observability.md)
- [Paperclip orchestration analysis](../../research/paperclip-orchestration-analysis.md)
- [Agent personas](../../concepts/agent-personas.md)
