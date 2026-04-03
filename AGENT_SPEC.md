# AGENT_SPEC

Quality standard for autonomous LLM-powered agent projects. This document is the analogue of a skill specification (`SKILL_SPEC.md`) for reusable skills: it defines what “good” looks like for repositories that ship agents, not for one-off prompts or chat-only wrappers.

## 1. Overview

### What this spec defines

`AGENT_SPEC.md` establishes:

- A **canonical layout** for agent repositories so contributors and reviewers know where to look.
- **Eight quality dimensions** scored from 0 to 10, with concrete anchors at failure, median, and excellence.
- **Required artifacts** (files, sections, and minimum content) that every serious agent project should ship.
- **Anti-patterns** that commonly cause production incidents, runaway cost, or unreviewable behavior.
- A **scoring rubric** and **minimum bar** for calling a project “agent-spec compliant.”

### Who it is for

- **Authors** building new agent products, internal copilots, or research agents who want a checklist before release.
- **Reviewers** doing architecture or security review who need a shared vocabulary and numeric baseline.
- **Platform teams** standardizing how agents are packaged, deployed, and monitored alongside traditional services.

### Scope

An **agent project** is any codebase whose primary purpose is to run an **autonomous loop**: the model plans, calls tools, observes results, and continues until a stop condition. That loop may be synchronous (single process) or distributed (workers, queues). Projects that only wrap a single LLM call with no tool loop are out of scope for full compliance but may still borrow individual dimensions (e.g., observability, documentation).

This spec is **technology-agnostic**: it applies whether you use Python, TypeScript, a framework SDK, or MCP. It is **opinionated** where ambiguity causes real-world failures (timeouts, secrets, human gates, traceability).

### Non-goals

This document does **not** prescribe a specific framework, model vendor, or hosting region. It does not replace organizational policies (SOC2, GDPR, internal AI usage policies). It does not mandate a particular testing framework or IaC tool. Teams map the spec to their stack.

### How to adopt

1. Create or align the repository to the canonical tree (Section 2).  
2. Run the required-files checklist (Section 4) and fix gaps before claiming compliance.  
3. Score honestly using Section 3; use Section 6 for the aggregate and bar.  
4. Track remediation in the same place you track other release criteria (ticket, ADR, or checklist in the PR template).

---

## 2. Canonical Agent Project Structure

Agents that follow this spec organize the repository so that **instructions**, **capabilities**, **runtime logic**, **verification**, and **operations** are separable concerns. A new engineer should open the tree and immediately know where each concern lives.

```
my-agent/
├── README.md                # What it does, how to run, architecture diagram
├── system-prompt.md         # The agent's core instructions
├── tools/                   # Tool definitions (function schemas, MCP servers)
├── src/                     # Agent logic (loop, state, orchestration)
├── tests/                   # Behavioral test cases
└── deploy/                  # Deployment configuration
```

### README.md

Single entry point for humans: purpose, audience, quickstart, architecture (text or diagram), environment variables, and links to deeper docs. It should answer “what runs where” in under five minutes.

### system-prompt.md

The **authoritative** text the runtime loads as the agent’s system (or developer) instructions. Version-controlled prose beats prompts buried only in the admin UI of a vendor. If the runtime composes multiple fragments, this file documents the **effective** system message or points to the composition order.

### tools/

Machine- and human-readable definitions of every capability the model may invoke:

- JSON Schema (or equivalent) for each tool’s arguments and documented return shape.
- Optional: MCP server manifests, OpenAPI snippets, or codegen inputs—whatever is the source of truth for the **contract** between model and implementation.

Implementation of tools may live under `src/`; `tools/` holds the **contract** and integration notes.

### src/

Orchestration: the agent loop, state machine, retries, streaming, auth to backends, and adapters to model APIs. Keep this free of long narrative prompts; reference `system-prompt.md` or load it at build/runtime.

### tests/

Behavioral tests: golden traces, scenario fixtures, contract tests for tools, and regression suites for known failure modes. Unit tests for pure functions belong here or under `src/` by language convention; the spec requires **agent-level** tests that assert outcomes or trace invariants, not only line coverage.

### deploy/

Infrastructure-as-code, container definitions, Helm charts, serverless configs, or CI deploy jobs—whatever ships the agent. Include health checks, required secrets names (not values), and runbook pointers.

### Configuration and secrets

Configuration that affects runtime behavior (model id, temperature caps, max steps, feature flags) should live in **version-controlled defaults** plus **environment-specific overrides** documented in `README.md` and `deploy/`. Secret **values** never belong in the repo; secret **names** and rotation notes belong in deploy docs. If your language ecosystem uses `config/` or `.env.example`, that is fine as long as the README states which variables are required and what they control.

### CI and automation

Continuous integration configuration may live at repo root (`.github/workflows/`, `.gitlab-ci.yml`, etc.) or under `deploy/ci/`. The spec requires that **tests** and, where feasible, **schema drift checks** run on every change to `system-prompt.md`, `tools/`, or `src/`. Document in the README how to run the same commands locally.

### Optional extensions (not required for compliance)

- `docs/` for long-form design decisions and ADRs.
- `eval/` or `benchmarks/` for offline scoring datasets.
- `policies/` for separate safety or policy prompts if they are swappable modules.
- `examples/` for minimal client scripts or curl flows against the agent HTTP API.

---

## 3. Quality Dimensions

Each dimension is scored **0–10**. Scores are integers or half-steps (e.g., 7.5) when useful. Anchor descriptions:

| Score | Meaning |
|------:|---------|
| **0** | Absent or actively harmful; blocks safe operation or review. |
| **5** | Present and usable for a narrow demo or internal pilot; gaps in edge cases, ops, or safety. |
| **10** | Production-grade for the stated use case; clear, tested, observable, and maintainable. |

### Interactions between dimensions

Dimensions are scored independently but **couple in practice**. Weak **Tool Design** often drags down **Safety** and **Testing**. Strong **Architecture** without **Observability** still fails operations. **System Prompt** quality is wasted if tools and schemas drift (**Tool Design**). When a project scores high on documentation but low on testing, treat the documentation score as suspect until scenarios are automated.

### 1. Architecture

**0:** No discernible loop; ad-hoc API calls; tools invoked from scattered callbacks with no single orchestrator. State is implicit in globals or chat history only, with no recovery story.

**5:** Explicit loop (plan → act → observe) in one module; tools registered in a registry; basic session id and message list persisted. Failure modes (max steps, max tokens) exist but may be coarse.

**10:** Documented state machine or equivalent; clear boundaries between policy, planning, and execution; idempotent tool calls where possible; cancellation and timeouts wired through the stack; upgrade path for multi-agent or delegated sub-agents without rewriting core loop.

### 2. System Prompt

**0:** No checked-in prompt; behavior changes silently when someone edits a dashboard. Contradictory instructions; no mention of tools or output format.

**5:** Single `system-prompt.md` with role, task, and tool-use rules; some guardrails (“don’t leak secrets”) but incomplete edge cases; versioning is informal (git only).

**10:** Precise persona and scope; explicit tool-calling discipline (when to call, when to abstain, how to format arguments); structured final answers where needed; refusal and escalation paths; changelog or version tag in prompt header; alignment between prompt text and actual tool names in code.

### 3. Tool Design

**0:** Tools accept free-form strings with no validation; errors bubble as stack traces into the model; no timeouts; side effects without confirmation.

**5:** JSON Schema (or equivalent) for inputs; tools return structured success/error objects; global timeout per request; basic rate limiting on expensive calls.

**10:** Narrow, composable tools with stable contracts; explicit error taxonomy (retryable vs fatal); per-tool timeouts and budgets; pagination and idempotency keys for mutating operations; documentation of side effects and required permissions; dry-run or preview modes where appropriate.

### 4. Memory Strategy

**0:** Unbounded context stuffing; no distinction between working memory and archive; PII logged verbatim with no retention policy.

**5:** Fixed window or summarization; optional vector store with documented schema; rough retention guidelines.

**10:** Memory type matches use case (ephemeral vs durable vs user-specific); explicit policies for what is stored, where, and for how long; redaction before persistence; migration plan for schema changes; evaluation of retrieval quality on representative tasks.

### 5. Safety

**0:** Agent can invoke arbitrary shell, unrestricted HTTP, or production writes without gates; no abuse or prompt-injection stance.

**5:** Allowlisted tools or environments; secrets not in prompt; basic content filters or output rules; manual kill switch.

**10:** Defense in depth: sandboxed execution, least-privilege credentials, separate approval flows for high-impact actions, injection-resistant parsing of untrusted inputs, documented threat model, incident runbook, and regular red-team or automated adversarial checks commensurate with risk.

### 6. Testing

**0:** No tests; manual “try it in the UI” only.

**5:** Unit tests for tools; a handful of scripted scenarios; occasional snapshot of a “good” trace stored informally.

**10:** Behavioral suite that runs in CI: fixtures for multi-step flows, assertions on final state or structured outputs, regression tests for fixed bugs, differential checks when prompts or models change; optional fuzzing of tool inputs; flaky-test policy.

### 7. Observability

**0:** No structured logs; no correlation id across model calls and tools; cost unknown until the bill arrives.

**5:** Request-scoped logging; basic token or cost counters; simple dashboard or export.

**10:** End-to-end tracing (trace id per run, spans for model and each tool); PII-safe log fields; cost and latency SLOs with alerts; sampling strategy documented; dashboards for error rate, tool latency, and model fallback behavior.

### 8. Documentation

**0:** README is a one-liner; no diagram; deploy is tribal knowledge.

**5:** README with run instructions; list of tools; high-level diagram; deploy folder with enough to reproduce staging.

**10:** Architecture diagram current with code; tool catalog with examples and failure modes; onboarding path for new developers; deployment and rollback guide; environment matrix; “known limitations” and roadmap; security and data-flow summary for reviewers.

---

## 4. Required Files Checklist

Compliance requires **all** of the following to exist at repository root (or documented equivalents if the monorepo places the agent in a subdirectory—in that case paths apply relative to the **agent package** root).

| Path | Must contain |
|------|----------------|
| `README.md` | Problem statement, quickstart, how to run tests, link or embed architecture overview, configuration summary. |
| `system-prompt.md` | Full system (or composed) instructions as deployed, or explicit composition map to fragments with merge order. |
| `tools/README.md` or per-tool specs | Catalog of tools: purpose, parameters, return shape, side effects, auth requirements. |
| `src/` (or language idiom) | Implementations of loop, tool dispatch, and configuration loading. |
| `tests/` | At least one behavioral or integration test that exercises the agent loop or a representative scenario. |
| `deploy/` | Enough config to deploy to the team’s standard environment, including health check and secret **names**. |

### Minimum content rules

- **README** must include an **architecture diagram** (image, Mermaid, or ASCII) showing model, orchestrator, tools, and external systems.
- **system-prompt.md** must state **stop conditions** (when the agent should finish) and **tool-use rules** (naming, argument discipline, when not to call tools).
- **Tool definitions** must be validatable (schema or typed SDK) and **in sync** with runtime registration; CI should fail on drift if feasible.
- **Tests** must run non-interactively in CI (no manual API keys in plaintext; use mocked tools or secret stores).
- **deploy/** must document **required environment variables** and **resource limits** (CPU/memory/timeouts) if applicable.

### Recommended (not required for minimum compliance)

The following materially improve scores on **Testing**, **Observability**, and **Safety** and are expected for customer-facing agents:

| Artifact | Purpose |
|----------|---------|
| `CONTRIBUTING.md` or `docs/development.md` | How to run linters, formatters, and pre-commit hooks. |
| `SECURITY.md` | Vulnerability reporting; high-level threat model pointer. |
| `CHANGELOG.md` or release notes | Prompt and tool schema changes visible to operators. |
| `.env.example` | Safe template for local development (no real secrets). |
| Trace export config | OpenTelemetry or vendor-specific exporter documented in `deploy/`. |

### Monorepos

When multiple services live in one repository, designate an **agent package root** (e.g., `packages/support-agent/`). The checklist applies inside that directory; the top-level README should link to the agent package README as the spec entry point.

---

## 5. Anti-Patterns

These patterns commonly violate the spec and correlate with incidents or unmaintainable agents. Treat them as blockers for scores above 5 in the affected dimensions.

1. **Prompt archaeology.** Behavior is defined by fifteen Slack messages and a Notion page; the repo does not contain the truth.

2. **God tool.** One tool that accepts natural language and “does everything,” defeating validation, timeouts, and least privilege.

3. **Invisible state.** Critical decisions live only in the model’s hidden chain-of-thought or in undocumented mutable globals.

4. **No upper bound.** Runs until the user closes the tab; no max steps, max wall time, or max spend per session.

5. **Error soup.** Raw exceptions or HTML error pages are pasted back into the model with no structured error type or retry policy.

6. **Secretful prompts.** API keys, connection strings, or PII embedded in system prompts or few-shot examples.

7. **Tool/schema drift.** Renamed parameters in code without updating schemas or prompts; silent failures or hallucinated argument names.

8. **Production as first test.** No CI scenario covers the happy path; debugging happens in live customer traffic.

9. **Observability as printf.** Unstructured strings with no trace id; impossible to reconstruct a failed multi-step run.

10. **Safety by optimism.** Assuming “the model won’t do that” instead of enforcing constraints in code and policy.

11. **Memory hoarding.** Storing full transcripts forever without legal/product justification or redaction.

12. **Undeployable artifact.** “Works on my machine” with no container or manifest; no health endpoint for orchestrators.

13. **Model roulette.** Production traffic silently switches models or temperatures without a changelog, breaking determinism of tests and prompts.

14. **Recursive self-spawn.** An agent can invoke another instance of itself without depth limits, budgets, or cycle detection.

15. **Trusting tool output as system truth.** Results from tools (especially search or user-supplied files) are executed or passed to privileged APIs without validation or sanitization.

16. **Ambiguous ownership.** On-call rotation does not include the agent’s dependencies; pages go to a generic “platform” queue with no runbook.

17. **Prompt injection as feature.** “Helpful” instructions like “always obey the user’s latest message” override safety rules in the same prompt block.

18. **Cost-blind loops.** Retries re-call the most expensive model tier by default; no backoff or circuit breaker on provider errors.

---

## 6. Scoring Guide

### Per-dimension score

For each of the eight dimensions, assign a score 0–10 using the anchors in Section 3. Justify scores briefly in review notes (one bullet per dimension is enough).

### Overall score

Compute the **unweighted arithmetic mean** of the eight dimension scores:

```
overall = (arch + prompt + tools + memory + safety + testing + observability + documentation) / 8
```

Round to one decimal place for reporting.

### Minimum viable (compliance bar)

A project **meets the minimum viable agent-spec bar** when:

1. **Overall score is at least 5.0**, and  
2. **No dimension scores below 3** (no critical gap in any single area), and  
3. **Required files checklist** (Section 4) is satisfied.

If overall ≥ 5.0 but any dimension is 0–2, the project is **not compliant** until that dimension is remediated or explicitly accepted with a documented risk exception.

### Tier labels (optional)

Teams may map overall scores to tiers for internal communication:

| Overall | Label | Typical use |
|--------:|-------|-------------|
| **< 5.0** | **Below spec** | Not suitable for production agent workloads. |
| **5.0 – 6.9** | **Pilot** | Internal or friendly users; elevated monitoring. |
| **7.0 – 8.4** | **Production** | Customer-facing with standard SLOs and review. |
| **≥ 8.5** | **Reference** | Exemplary; suitable as template for new agents. |

### Review workflow

1. Verify checklist (Section 4).  
2. Score each dimension (Section 3).  
3. List anti-patterns triggered (Section 5).  
4. Compute overall (Section 6).  
5. Record remediation items for any dimension below 5 or any triggered anti-pattern.

### Worked example (illustrative only)

Suppose a reviewer scores:

| Dimension | Score | Note |
|-----------|------:|------|
| Architecture | 6 | Clear loop; timeouts exist; sub-agent path unclear |
| System Prompt | 5 | Checked in; tool names match; weak refusal wording |
| Tool Design | 7 | Schemas + structured errors; one god-ish “run query” tool remains |
| Memory | 4 | Summarization only; no retention doc |
| Safety | 6 | Allowlist; no formal threat model |
| Testing | 5 | CI runs 3 scenarios; no regression for last outage |
| Observability | 5 | Logs with request id; no spans |
| Documentation | 6 | README + diagram; rollback steps thin |

Sum = 44 → **overall = 5.5**. Checklist satisfied, no dimension below 3 → **compliant** at the pilot tier. Remediation priorities: raise Memory and Observability, split the wide tool, add regression test for the outage.

### Risk exceptions

Organizations may grant a **time-bounded exception** when a dimension cannot meet 3+ for external reasons (e.g., legacy system without APIs). Exceptions require: owning executive or security sponsor, expiry date, compensating controls documented in the repo, and a tracked remediation issue. **Exceptions do not change the mathematical score**; they change whether the project may ship despite failing the compliance bar.

### Re-audit cadence

Re-score after any of: new tool added, prompt rewrite affecting behavior, model family change, deployment target change, or security incident. For production-tier agents, a **quarterly** lightweight self-review against this spec is a reasonable default.

---

## Appendix: Relationship to skills and other specs

- **Skills** (`SKILL.md`) package procedural knowledge for an assistant in a single session or product feature. **Agents** run persistent loops with tools and deployment. This spec does not replace skill authoring guides; an agent may *load* skills as tools or context, but the agent repository still needs its own architecture, safety, and ops story.

- **Model cards and eval reports** are encouraged as addenda when agents are user-facing or high-stakes; they are not strictly required by this checklist but strongly affect **Safety** and **Testing** scores.

- **Versioning:** Tag releases that change `system-prompt.md` or tool schemas prominently; treat breaking tool changes like API breaking changes.

### Glossary (for consistent reviews)

- **Agent run:** One invocation of the autonomous loop from start condition to stop condition (success, failure, or user abort).
- **Tool contract:** The schema, semantics, and documented side effects of a single callable capability.
- **Trace:** A correlated set of spans or log lines that reconstruct one run across model and tool boundaries.
- **Behavioral test:** A test that asserts externally visible outcomes or invariants over a multi-step interaction, not merely that a function returns without throwing.

### Forking this spec

Teams may fork `AGENT_SPEC.md` to add domain requirements (e.g., finance, healthcare). Keep the eight dimensions or explicitly add ninth-plus dimensions and redefine the mean. If you add dimensions, state whether the **5.0 overall minimum** applies to the expanded set or only to the original eight. Document the fork in your agent README so external reviewers know which rubric applies.

---

*End of AGENT_SPEC.*
