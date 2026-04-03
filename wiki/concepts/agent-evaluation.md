# Agent Evaluation

## What it is

**Agent evaluation** is the practice of measuring whether an agent (loop + tools + prompts) meets product and safety requirements. It spans **behavioral tests** (scenario outcomes), **trace analysis** (step-by-step tool and model decisions), **benchmark suites** (standard tasks and rubrics), **A/B testing** (live traffic splits), and **compliance scoring** (policy adherence, PII handling). Evaluations are often split into **offline** (replay, synthetic, human-labeled datasets) and **online** (production metrics, shadow mode, canaries).

## Why it matters for agents

Models and tools change constantly; without evaluation, regressions ship silently. Agents have **long tails**: rare paths dominate incidents. Evaluation ties iteration to evidence, supports governance, and makes model or prompt upgrades auditable. It is the main feedback signal for when cheaper models or shorter prompts are safe.

## How to implement it

1. **Define dimensions:** task success (binary or graded), tool correctness, latency, cost, safety violations, user satisfaction proxies.
2. **Offline behavioral suites:** fixed scenarios with expected final states or allowed tool sequences; run in CI on every change to prompts, tools, or routing.
3. **Trace-based checks:** assert invariants on spans (e.g., no `delete` without prior `confirm` tool); use platforms like **LangSmith** or **Braintrust** for trace storage and diffing.
4. **LLM-as-judge:** use only with rubrics, calibration sets, and human spot checks; log judge prompts and versions.
5. **Online A/B:** route a small fraction to candidate configs; monitor guardrail triggers, escalation rates, and business KPIs; watch for Simpson’s paradox across segments.
6. **Compliance scoring:** encode policy rules as automated checks on structured outputs and tool args where possible; sample human review for ambiguous cases.

## Offline vs online

**Offline** gives reproducibility and speed; it misses real user phrasing and load. **Online** captures reality but is noisy and slower. Use offline for gates; use online for validation and drift detection. Bridge them with **production trace sampling** replayed into offline harnesses.

## Dataset hygiene

Label **intent**, **risk class**, and **expected tools** where possible so you can slice metrics. Balance classes so a headline accuracy does not hide collapse on rare but critical scenarios (refunds, deletes, medical). Version datasets like code (`evalset-v3.2`); pin which set blocked a release in change logs.

## Governance and compliance scoring

Map policies to **automatic** checks first: PII patterns in outbound text, disallowed tool sequences, jurisdiction-specific wording. Reserve manual review for ambiguous bands. Store adjudication outcomes to refine rubrics and to train lightweight classifiers for pre-screening.

## Operational cadence

Run **smoke** evals on every PR touching prompts or tools; run **full** suites nightly or on release candidates. After model upgrades, run **diff reports** against golden traces: changed tool args, extra reasoning tokens, or new refusals may be acceptable—but must be reviewed.

## Common mistakes

- Optimizing only for end-task accuracy while ignoring harmful intermediate steps.
- Single global score without stratifying by intent, locale, or data sensitivity.
- Judges without version pins or without correlation to human labels.
- Skipping evaluation when swapping models—“it feels fine” is not a release criterion.

## Quick checklist

- Every prompt or tool change runs a **smoke** behavioral suite in CI.
- Online dashboards slice by **intent** and **risk**, not only global averages.
- Judge prompts and model ids are **pinned** and re-calibrated on schedule.

## References to course modules

These map to the **23-module Agent Factory course** (see [`../../course/README.md`](../../course/README.md) when published).

- **Module 14 — Behavioral Test Suites & Golden Traces** — scenario design and CI integration.
- **Module 15 — Benchmarks, Rubrics, and LLM-as-Judge** — scalable grading patterns.
- **Module 18 — Online Evaluation, A/B Testing, and Drift** — production measurement.

Full curriculum index: [`../../course/README.md`](../../course/README.md) (when present).

## See also

- [Observability](observability.md)
- [Feedback Loops](feedback-loops.md)
- [Agent Testing Patterns](agent-testing-patterns.md)
- [Guardrails](guardrails.md)
- [Cost Optimization](cost-optimization.md)
