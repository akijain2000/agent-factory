# Agent Lifecycle

## What it is

The **agent lifecycle** spans from **prototype** (notebook, single-user harness) through **staging**, **production**, and **continuous iteration**: development practices, **testing gates**, **deployment** checklists, **monitoring**, and feedback-driven improvement. It is the macro view of how an agent product becomes **reliable**, **observable**, and **governed**—not only how the loop works in isolation.

## Why it matters for agents

Prototypes optimize for **demo success**; production optimizes for **tail risk**, **cost**, and **compliance**. Without explicit lifecycle stages, teams ship **prompt changes** without evals, add tools without **security review**, and debug incidents without **reproducible** run artifacts. A disciplined lifecycle turns “it worked in the meeting” into **measurable** quality and rollback.

Lifecycle thinking also bounds **scope**: every stage should have an explicit **exit criterion** so experiments do not linger half-shipped, sharing production credentials without SLOs.

## How to implement it

1. **Prototype stage:** narrow scope, synthetic tasks, manual traces. Establish **success criteria** and a **minimal** tool set. Version prompts and schemas in git.
2. **Alpha:** real users under NDA; enable **full observability**; collect **failure buckets** (tool, model, policy). No unbounded autonomy.
3. **Beta:** load testing, **SLOs**, **cost** dashboards, **on-call** playbooks. Introduce **feature flags** for risky tools.
4. **Production gates:** require **offline eval** pass, **security** review for new tools, **rollback** plan, and **runbook** updates. Tag releases with **model ids** and **policy versions**.
5. **Deployment checklist:** config diff, secret rotation plan, **canary** slice, **metric** dashboards pre-staged, **customer comms** if behavior changes.
6. **Monitoring:** golden signals—success rate, latency, cost per task, **tool error** rate, **human escalation** rate. Alert on drift, not only outages.
7. **Iteration:** close the loop with **eval sets** and **user feedback**; schedule periodic **red-team** and **data retention** reviews.

8. **Ownership:** name a **DRI** for prompts, tools, eval suites, and on-call—ambiguous ownership stalls lifecycle maturity.

**Documentation:** keep `AGENT_SPEC`-level docs in sync with shipped behavior; treat doc drift as a bug.

## Testing gates

Block promotion when **regressions** exceed thresholds on **held-out** tasks or when **safety** scenarios fail. Pair automated tests with **periodic** human spot checks for subjective quality.

Add **release notes** for user-visible behavior changes—even “better” models can alter tone enough to trigger support tickets.

Archive **artifacts** (prompt hashes, eval reports) with each release so compliance and support can reconstruct historical behavior.

## Common mistakes

- **Prompt edits** straight to production without versioned evals.
- Skipping **disaster** drills (provider outage, quota exhaustion).
- No **owner** for tool permissions and data retention.
- Conflating **model upgrades** with harmless config changes.
- **Skipping** post-incident updates to eval sets after real-world failures.
- Letting **staging** drift from prod (different tools enabled, older corpora).

## References to course modules

These map to the **23-module Agent Factory course** (see [`../../course/README.md`](../../course/README.md) when published).

- **Module 01 — Foundations & Lifecycle** — stages, ownership, and definitions of done.
- **Module 16 — Testing & CI for Agents** — gates, fixtures, and regression suites.
- **Module 19 — Deployment & Runtime Topology** — shipping and operating agents.
- **Module 20 — Production Readiness & Reliability** — SLOs, incidents, and rollback.

Full curriculum index: [`../../course/README.md`](../../course/README.md) (when present).

## See also

- [Agent Evaluation](agent-evaluation.md)
- [Agent Testing Patterns](agent-testing-patterns.md)
- [Observability](observability.md)
- [Deployment Patterns](deployment-patterns.md)
- [Feedback Loops](feedback-loops.md)
