# Human-in-the-Loop

## What it is

**Human-in-the-loop (HITL)** inserts explicit **approval gates**, **review points**, and **escalation paths** where a person confirms, edits, or rejects before the agent continues—especially before irreversible or high-risk actions. **Confidence thresholds** from classifiers or calibrated model self-scores can route borderline cases to humans. The **interface** should show diff, impact, and rollback options, not raw model prose alone.

## Why it matters for agents

Full autonomy is rarely acceptable for finance, healthcare, infra, or privacy-impacting workflows. HITL converts “the model did it” into “a human authorized step *k*.” It also improves quality: experts correct plans early, reducing compound errors downstream.

## How to implement it

1. **Gate inventory:** list operations requiring approval (refunds, prod writes, external email); encode as graph interrupts or state machine transitions.
2. **Payload for review:** structured proposal `{ intent, args_hash, preview, blast_radius }`; avoid burying parameters in chat.
3. **Timeouts and fallbacks:** if human does not respond, default to safe path (hold, cancel, or degraded response)—documented per gate.
4. **Confidence routing:** if `P(high_risk) > τ`, require approval; tune τ with offline eval and incident review.
5. **Audit trail:** who approved, when, and with what diff; link to trace id.
6. **UX:** optimistic loading, clear primary/secondary actions, escalation to on-call for SLA breaches.

**When to require approval:** irreversible mutations, regulatory triggers, first-time use of a high-privilege tool, or anomaly detection hits. **When not to:** low-risk read-only steps that would make the product unusably slow—use logging instead.

## SLAs and operations

Define **response time targets** per gate class (e.g., P95 under five minutes for refunds). If SLA is missed, auto-escalate to a secondary queue or safe default (hold transaction). Runbooks should include how to **replay** a stuck run after approval without re-executing prior side effects—usually via idempotent step ids stored in state.

## Accessibility and clarity

Review UIs should work with keyboard navigation and screen readers where customer-facing; show **numeric impact** (amounts, row counts) and **blast radius** in plain language. Provide a “why this needs approval” string generated from policy code, not only model prose.

## Metrics

Track **time-in-queue** per gate, **approval vs rejection** rates, and **override frequency** (if operators can force-through). Sudden spikes often indicate model drift or ambiguous policy text. Pair metrics with **trace samples** for qualitative review.

## Common mistakes

- **Missing human escalation** on failures; infinite auto-retry instead.
- **Rubber-stamp UI** where humans cannot see actual args or side effects.
- **Blocking everything** so humans become the bottleneck; no tiered risk model.
- **No audit** of overrides or edits to model proposals.

## References to course modules

These map to the **23-module Agent Factory course** (see [`../../course/README.md`](../../course/README.md) when published).

- **Module 20 — Human-in-the-Loop UX & Policy** — gate design and interfaces.
- **Module 14 — Plan–Execute & Replanning** — approving plans before execution.
- **Module 17 — Safety Architecture & Threat Modeling** — aligning gates to threats.

Full curriculum index: [`../../course/README.md`](../../course/README.md) (when present).

Design gates so **defaults are safe**: if the UI is confusing, operators will approve to unblock—assume that failure mode.

Record **training snippets** for reviewers when policies change; otherwise approvals become guesswork.

## See also

- [Guardrails](guardrails.md)
- [State Management](state-management.md)
- [Agent Handoffs](agent-handoffs.md)
- [Multi-Agent Orchestration](multi-agent-orchestration.md)
- [Agent UX](agent-ux.md)
