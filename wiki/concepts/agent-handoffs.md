# Agent Handoffs

## What it is

An **agent handoff** transfers **control**, **responsibility**, and **state** from one agent (or runtime) to another. Patterns include **OpenAI Swarm**-style routing functions that select the next agent with a structured handoff payload, **CrewAI delegation** from managers to specialists, and custom **context passing** where a serialized `Handoff` object carries goal, constraints, artifacts, and audit metadata. **State transfer** covers not only messages but also tool permits, budget remaining, and open human approvals.

**Clean handoff** means explicit schema, id, and trace continuity; **messy handoff** dumps unstructured chat and loses tool permissions or tenant scope.

## Why it matters for agents

Support triage → billing escalation, coding agent → security reviewer, and locale-specific specialists all require reliable transfer. Poor handoffs drop constraints (“user said no refunds”) or re-expose secrets. Compliance often needs to show *which* agent performed *which* action.

## How to implement it

1. **Handoff schema:** `{ from_agent, to_agent, goal, constraints[], artifacts[], trace_id, budget, pending_hitl }` validated at boundary.
2. **Context package:** summarize prior work; include pointers to large artifacts; avoid re-injecting entire transcripts when tiers allow slimmer digests.
3. **Authority transfer:** update allowlisted tools and credentials to match the receiving agent’s role; revoke prior elevated tokens if required.
4. **Swarm-style routing:** implement as explicit function returns consumed by harness, not model free text alone.
5. **CrewAI-style delegation:** task objects with acceptance criteria; manager verifies `output` schema before closing task.
6. **Resume rules:** receiving agent acknowledges constraints in structured form (checkbox JSON) before acting.

**Clean vs messy:** clean uses versioned payloads and continues one trace; messy concatenates strings and hopes the next model infers policy.

## Handoff lifecycle

1. **Prepare:** freeze authoritative constraints from state; snapshot open questions.  
2. **Validate:** schema check; redact secrets from the visible package while retaining secure handles.  
3. **Transfer:** atomically switch **active agent** pointer and **credential scope** in the harness.  
4. **Acknowledge:** receiving agent emits structured acceptance or rejection with reasons.  
5. **Continue or rollback:** on rejection, route back to sender or human with preserved checkpoints.

Record each transition in an **audit log** row tied to `trace_id`.

## Idempotency across agents

If a handoff retries after a timeout, include a **handoff_id** so downstream work is not duplicated. Align with tool **idempotency keys** when the receiving agent immediately triggers writes.

## Common mistakes

- **String soup handoffs** with no schema validation.
- **Permission leakage** carrying elevated tool access to a generalist agent.
- **Broken trace ids** so operators cannot follow cross-agent flows.
- **Duplicate execution** when both agents believe they own the next step.

## References to course modules

These map to the **23-module Agent Factory course** (see [`../../course/README.md`](../../course/README.md) when published).

- **Module 10 — Multi-Agent Patterns** — roles, routing, and explicit transfer semantics.
- **Module 12 — State Management** — handoff payloads, forbidden transitions, and recovery.
- **Module 19 — Observability and Debugging** — shared trace IDs and cross-agent narratives.

Full curriculum index: [`../../course/README.md`](../../course/README.md) (when present).

## See also

- [Multi-Agent Orchestration](multi-agent-orchestration.md)
- [State Management](state-management.md)
- [Human-in-the-Loop](human-in-the-loop.md)
- [Tool Design](tool-design.md)
- [Observability](observability.md)
