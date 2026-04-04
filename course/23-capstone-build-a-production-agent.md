# Module 23: Capstone — Build a Production Agent

**Duration:** approximately 60 minutes (planning and implementation time beyond this lesson is expected)  
**Prerequisites:** Completion of Modules 01–22 or equivalent experience; Module 17 (Evaluation) and Module 18 (Safety) are mandatory baselines before shipping.

---

## Learning objectives

By the end of this capstone, you should be able to:

- **Integrate** architecture, tools, memory, safety, testing, and deployment into one coherent agent system.
- **Use** the **Agent Maker** meta-skill as a structured path from intent to shippable artifacts.
- **Ship** an agent with **documentation**, **tests**, and **operational** hooks (logging, metrics, rollback).
- **Validate** your work against **[AGENT_SPEC.md](../AGENT_SPEC.md)** as the project quality standard.

---

## Capstone overview: from idea to deployed agent

This capstone is intentionally **end-to-end**: you are not proving you can call an API once—you are proving you can own a **lifecycle** (design, implement, verify, deploy, observe). Expect to iterate: production agents are **systems**, not prompts.

Deliverables (adjust to your employer’s norms, but do not skip categories):

- **AGENT_SPEC alignment:** explicit checklist mapping (see rubric below).
- **Runnable code** or configuration plus **README** for operators.
- **Behavioral tests** or eval harness covering success and representative failures.
- **Safety notes:** data handling, tool scopes, escalation, and known limitations.

---

## Three tracks

### Track A: Single-agent coding assistant

Focus: **tool use**, **memory**, **error handling**. Suitable if you want depth in one loop and tight control over UX.

Typical scope: repository-aware edits, test runs, lint, structured handoff to human review. Emphasize **idempotent** tools and **clear** stop conditions.

### Track B: Multi-agent research team

Focus: **orchestration**, **handoffs**, **cost tracking**. Suitable if you already built single agents and need coordination patterns.

Typical scope: planner plus specialist workers, shared artifact store (e.g., brief, sources), explicit merge step. Emphasize **message schemas** and **deduplication** of work.

### Track C: Self-improving agent with harness optimization

Focus: **learning loops**, **benchmarks**, constrained self-edit. Suitable if you completed Module 22 and want meta-control.

Typical scope: outer harness that scores an inner agent on a fixed task set; gated updates to a `program.md` or equivalent. Emphasize **anti-Goodhart** design and **rollback**.

---

## Step-by-step guide (all tracks)

Apply these steps to **your** track; depth varies, but order matters.

### 1. Define the agent’s purpose and constraints

Write a one-paragraph **mission**, non-goals, **SLAs** (latency, cost), and **compliance** constraints (PII, secrets, regions). If you cannot state failure modes, you are not ready to implement.

### 2. Choose architecture and framework

Pick a graph, SDK, or minimal loop—justify **one** primary orchestration mechanism. Note what you are **not** building (avoid framework soup).

### 3. Design system prompt and tools

Prompt carries **policy**; tools carry **capabilities**. Specify JSON schemas, side effects, and authentication. Split tools before the prompt becomes a branching novel.

### 4. Implement the agent loop

Implement observe → plan → act → verify with **budgets** (steps, tokens, wall clock). Log structured traces for debugging.

### 5. Add safety and guardrails

Input validation, tool allowlists, secrets hygiene, human gates for irreversible actions, and **content** policy where relevant. Document **residual risk**.

### 6. Write behavioral tests

Minimum: golden paths, tool failure injection, timeout behavior, and a **regression** case tied to a real bug you found. Prefer repeatable fixtures over one-off demos.

### 7. Deploy and monitor

Choose an environment appropriate to Track A/B/C. Ship **health checks**, **alerts** on error rate and cost anomalies, and a **rollback** path for prompt or config changes.

### 8. Validate against AGENT_SPEC.md

Walk the spec line by line; file gaps as issues, not footnotes. If something is intentionally out of scope, say so in the README with **risk acceptance**.

---

## Evaluation rubric aligned with AGENT_SPEC.md

Use **[AGENT_SPEC.md](../AGENT_SPEC.md)** as source of truth. For self-grading, include evidence (links to tests, logs, config) for each major area:

| Area | Evidence you should produce |
|------|-----------------------------|
| Clarity of purpose | Mission, non-goals, user-facing limits |
| Tooling | Schemas, auth, least privilege |
| Reliability | Retries, timeouts, idempotency notes |
| Safety | Guardrails, escalation, data handling |
| Observability | Traces, metrics, debug playbook |
| Quality assurance | Evals or tests, baseline scores |
| Operations | Deploy steps, rollback, ownership |

A **pass** is not “it ran once”; it is **repeatable** acceptable behavior on your declared task set.

---

### Autoresearch-validated quality bar

The Factory Showcase autoresearch loop empirically validated what separates a 7/10 agent from a 9/10 agent across 20 production agent designs. Use these as your capstone quality targets:

- **Source code**: Typed state machine enum + transition table + circuit breakers (not stubs)
- **System prompt**: Refusal paths + HITL gates + memory strategy + cost awareness (not just persona)
- **Tool design**: Error taxonomy with retryable flags per tool + idempotency for mutations (not just schemas)
- **Testing**: 4 scenario types — happy path, error recovery, adversarial, regression (not just happy path)
- **Observability**: SLOs with domain-specific numbers + tracing + cost tracking (not just logs)
- **Safety**: SECURITY.md with domain threat model + HITL with timeout behavior (not just "be safe")
- **Documentation**: Mermaid diagram + env matrix + honest limitations (not just a README)

See the full ranked breakdown: [Factory Showcase LEARNINGS.md](https://github.com/akijain2000/factory-showcase/blob/main/grading/autoresearch-logs/LEARNINGS.md).

---

## Graduation checklist

Before you call the capstone done:

- [ ] README explains **how to run**, **how to test**, and **what not to use it for**.
- [ ] At least **one** automated check runs in CI or a local script developers can execute.
- [ ] **AGENT_SPEC.md** review completed; gaps documented with owners or deferrals.
- [ ] **Cost** and **latency** observed on a realistic workload; surprises explained.
- [ ] **Incident** playbook: who to page, how to disable tools, how to revert config.

---

## Exercises

**Complete one of the three tracks** end-to-end at a scope you can finish: a thin vertical slice beats a sprawling unfinished system. Submit (or archive) artifacts: code, README, test/eval output, and AGENT_SPEC mapping.

Optional stretch: implement a second track’s **handoff interface** only (schema + stub) to practice interoperability without doubling implementation time.

---

## Further reading

- [AGENT_SPEC.md — quality standard for this repository](../AGENT_SPEC.md)
- [Agent Maker meta-skill](../agent-maker/SKILL.md)
- [Agent evaluation methods (wiki)](../wiki/research/agent-evaluation-methods.md)
- [Harness engineering (wiki)](../wiki/concepts/harness-engineering.md)
- [Production case studies (wiki)](../wiki/research/production-case-studies.md)
