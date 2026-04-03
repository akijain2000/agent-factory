# Module 13: Framework Selection

**Duration:** approximately 30 minutes  
**Prerequisites:** Module 02 (Agent Architectures); Module 05 (Tool Design) recommended.

---

## Learning objectives

By the end of this module, you should be able to:

- **Evaluate** agent frameworks against concrete project requirements instead of hype or defaults.
- **Apply** a decision matrix to compare LangGraph, CrewAI, OpenAI Agents SDK, Anthropic-first stacks, and raw API approaches.
- **Explain** tradeoffs across maturity, ecosystem, learning curve, production readiness, and cost.

---

## The framework landscape in 2024–2026

Between roughly 2024 and 2026, production agent stacks converged around a few patterns: **graph-orchestrated** flows (LangGraph and similar), **role-based crews** (CrewAI, AutoGen-style teams), **vendor SDKs** that wrap models plus tools and tracing (OpenAI Agents SDK), **model-native** APIs with strong tool-use contracts (Anthropic Claude), and **framework-free** apps that call HTTP APIs directly and own orchestration in application code.

The landscape is **fast-moving**: features that were unique to one framework often appear elsewhere within months. Your choice should track **your** constraints—team skills, compliance, latency budgets, and observability—not a single blog post’s “winner.”

**Stable questions** to ask regardless of year: Who owns state and persistence? How do you test and replay runs? What happens when the model loops or calls a dangerous tool?

---

## Decision matrix: LangGraph vs CrewAI vs OpenAI Agents SDK vs Anthropic vs raw API

Use a **scoring matrix** (e.g., 1–5 per row) for each serious candidate. Example dimensions and rough characterizations:

| Dimension | LangGraph | CrewAI | OpenAI Agents SDK | Anthropic (API/SDK) | Raw API |
|-----------|-----------|--------|-------------------|----------------------|---------|
| **Orchestration model** | Explicit graph, cycles, checkpoints | Roles, tasks, crews | Agents, handoffs, runners | You design loop + tools | Fully custom |
| **State / persistence** | First-class checkpoints | Often app-owned | Tracing + session patterns | App-owned | App-owned |
| **Best when** | Complex control flow, HITL | Multi-role storytelling workflows | Handoffs, guardrails, MCP | Claude-centric products | Minimal deps, full control |

```text
# Example weight file (YAML) — tune per project
criteria:
  production_readiness: 0.25
  team_familiarity: 0.20
  time_to_first_deploy: 0.15
  observability: 0.15
  cost_predictability: 0.10
  vendor_lock_in_tolerance: 0.15
```

Normalize weights to 1.0, score each framework, then **discuss** scores that tie—ties often mean “either works; pick based on hiring and support.”

---

## Evaluation criteria: maturity, ecosystem, learning curve, production readiness, cost

**Maturity:** release stability, breaking-change frequency, migration guides, and real production references (not only demos).

**Ecosystem:** integrations (vector DBs, auth, queues), community examples, and whether your **existing** stack already fits (e.g., LangChain-adjacent shops often adopt LangGraph faster).

**Learning curve:** time for a mid-level engineer to ship a **safe** agent (with retries, logging, and tests)—not time to run a notebook.

**Production readiness:** idempotency story, backoff, concurrency, secrets handling, and whether the framework **forces** good patterns or merely allows them.

**Cost:** not only API dollars but **engineering** cost—debug hours, rewrites when the framework pivots, and operational load (self-hosted runners vs managed).

---

## When to use each framework (decision tree)

1. **Need cyclic graphs, branching, durable checkpoints, or strict HITL gates?** Strongly consider **LangGraph** (or another graph runtime) so control flow is **data**, not prompt hope.
2. **Team thinks in “roles” and parallel research/writing tasks?** **CrewAI** (or similar crew abstractions) can match mental models—watch for **implicit** state and testability.
3. **You are standardized on OpenAI models, want handoffs, guardrails, MCP, and tracing in one SDK?** **OpenAI Agents SDK** reduces glue code; still **own** persistence and security boundaries.
4. **Product is Claude-first (extended thinking, computer use, Opus/Sonnet tuning)?** Prefer **Anthropic APIs** and patterns documented for Claude; wrap with your harness.
5. **Small surface area, hard latency/dependency constraints, or you already have a workflow engine?** **Raw API** + your orchestrator is often **less** code than fighting a framework.

---

## When to go framework-free (raw API calls)

Choose **raw HTTP/SDK calls** when:

- You already run **Temporal**, **Step Functions**, or an internal job system that should own retries and state.
- **Compliance** requires every branch to be auditable in **your** store, not a black-box runner.
- The agent is a **thin** layer over one model and three tools—framework ceremony adds more risk than value.
- You need **minimal** supply-chain surface (fewer transitive dependencies).

You still implement: **tool schemas**, **timeouts**, **logging**, **redaction**, and **tests**. Framework-free is not “no engineering.”

---

## Common mistake: choosing based on popularity, not fit

**GitHub stars** and conference talks skew toward demos and greenfield startups. Your criteria should include: **on-call** ownership, **junior** maintainability, and **upgrade** pain.

**Anti-pattern:** picking LangGraph because “everyone uses it” when your product is a linear FAQ bot with two tools— you pay **complexity tax** without gaining graph semantics.

**Better pattern:** write a **one-page** decision record: requirements, rejected options, and **what would change our mind** (e.g., “If we add multi-step approvals and branching research, we revisit LangGraph.”).

---

## Quick checklist before you commit

Use this before locking a framework for a quarter or more:

- [ ] **Requirements doc** lists latency, data residency, and which tools touch production.
- [ ] **Two engineers** who will maintain it have **run** the official quickstart and a **failure** scenario (timeout, bad tool args).
- [ ] **Observability** plan names the store for traces and whether PII is scrubbed.
- [ ] **Exit criteria** are written: what evidence would trigger a **re-evaluation** or migration?

Skipping the checklist is how teams end up with **framework soup**—multiple overlapping runtimes in one repo because each feature team picked a different default.

---

## Exercises

### Exercise 1: Evaluate three frameworks for a given project

**Scenario:** Internal “IT helpdesk” agent that reads a ticket API, searches Confluence, and can open a **limited** set of Jira transitions. Uptime matters; wrong transitions are high impact.

Pick **three** candidates (e.g., LangGraph, OpenAI Agents SDK, raw API). For each, list **two strengths**, **two risks**, and **one mitigation** for each risk. Finish with a **recommended** choice and a single sentence of rationale.

### Exercise 2: Design criteria weights for a specific use case

Pick a real or hypothetical product (your choice). Define **five** criteria with **weights** summing to 100%. Explain **why** one criterion is weighted higher than another (e.g., regulated industry vs hobby project). Optionally score two frameworks against your rubric.

---

## Further reading

- [Framework comparison (wiki)](../wiki/research/framework-comparison.md) — consolidated notes and comparison axes for major stacks.
- Your project’s own **AGENT_SPEC** or architecture doc — align framework choice with documented boundaries and threat model.
