# OpenAI Agents SDK: Customer Service with Handoffs

## Summary

A customer-service stack built with the OpenAI Agents SDK uses a **triage** agent as the front door, then **hands off** to domain specialists: billing, technical support, or account changes. Each specialist has tools appropriate to its domain; triage has only classification and routing tools. Guardrails validate outbound messages and sensitive actions before they reach the customer or back office.

## Pattern

**Hierarchical handoffs with scoped tools and policy layers.** Triage produces a structured intent and confidence; the runtime selects the next agent or asks a clarifying question. Specialists run under tighter prompts and tool sets. Guardrails (schema checks, policy text, optional human review) sit at boundaries where harm or compliance risk is highest.

## What makes it good

Handoffs are first-class: the framework models delegation explicitly, so traces show which agent owned which turn. Narrowing tools per stage reduces wrong-tool errors and makes it harder for prompt injection in one channel to trigger unrelated tools in another. Guardrails turn “we hope the model is safe” into enforceable checks.

Operations teams can tune triage without rewriting billing logic, and billing can add tools without expanding triage’s surface area.

### In practice

Log each handoff with correlation IDs tied to CRM tickets. Store the structured intent object alongside the transcript so supervisors can audit why a case landed in technical vs billing. For PII-heavy sectors, redact transcripts before model training or analytics while retaining structured metadata.

### Failure modes this design mitigates

Monolithic support bots conflate refund policy with debug steps, producing dangerous mixed advice. Scoped specialists reduce **cross-domain leakage**. Guardrails at send-time catch disallowed promises (SLAs, legal language) even if an inner agent drafts them.

### When to reconsider

If your volume is low and cases are rarely ambiguous, a single agent with a decision tree prompt may suffice until metrics show misrouting cost. Measure **containment versus escalation** before investing in multi-agent complexity.

## Key takeaway

**Route first, specialize second, and validate at the edges**—especially before messages and transactions leave the system.

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

- [Agent handoffs](../../concepts/agent-handoffs.md)
- [Guardrails](../../concepts/guardrails.md)
- [Human-in-the-loop](../../concepts/human-in-the-loop.md)
- [OpenAI agent patterns](../../research/openai-agent-patterns.md)
- [Agent security](../../concepts/agent-security.md)
