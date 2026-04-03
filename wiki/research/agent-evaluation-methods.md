# Agent Evaluation Methods

Evaluating agents requires **layered signals**: behavioral success on tasks, **structural** correctness of traces, safety compliance, and economic feasibility. No single metric suffices; production teams blend **offline** regression with **online** monitoring.

## Behavioral end-to-end tests

Task suites with **binary or graded** success criteria (tests pass, ticket resolved, JSON validates) anchor evaluation to outcomes users care about. Golden tasks should span **difficulty tiers** and include **adversarial** inputs (injection attempts, ambiguous specs).

## Trace analysis

Beyond final answers, inspect **tool sequences**: unnecessary calls, repeated failures, policy violations. Trace-based tests catch **regressions** in routing and tool selection when wording of success is unchanged but pathologies appear.

## Benchmark suites

Public benchmarks provide **comparability**: coding (e.g., **SWE-Bench**-class tasks), reasoning, tool-use harnesses. Treat benchmarks as **stress tests**, not market promises—distribution shift to your domain is the norm.

## Compliance and policy scoring

Checklists for **PII handling**, disallowed actions, and approval workflows. Automate where possible with **rules + classifiers**, and sample human review for calibration.

## LLM-as-judge

Judges score rubric dimensions (correctness, completeness, tone). Risks: **bias**, **position effects**, and **shared blind spots** with the generator. Mitigate with **multiple judges**, **spot human audits**, and preference for **executable** checks when available.

## Human-in-the-loop evaluation

Expert review remains the gold standard for **nuanced** domains. Structure reviews with **blinded** comparisons and **rubric** consistency training to reduce noise.

## Regression discipline

Version prompts, tools, and model pins; on change, rerun **minimum viable** eval suites in CI. Promote flaky tests to **investigations**—flakiness often signals **nondeterministic tools** or **under-specified** tasks.

## Economic metrics

Track **tokens per successful task**, **p95 latency**, and **cost per outcome**. A quality gain that doubles cost may be unacceptable for a tier-1 support bot but acceptable for **security review**.

## Rubric design for LLM judges

Anchor rubrics to **observable criteria** (“cites tool output IDs”) rather than vibes (“seems smart”). Use **likert** scales with calibration examples per score level. Rotate **golden** tasks into the suite monthly to detect **overfitting** to legacy prompts.

## Stratified sampling for live traffic

Online, sample tasks by **intent class** and **risk tier**—uniform random misses tail risks where failures hurt most. Weight review queues toward **financial** and **PII**-touching flows even if low volume.

## Red teaming and adversarial sets

Maintain **injection**, **jailbreak**, and **tool-abuse** cases that evolve monthly. Tie red-team findings to **blocking** CI tests where feasible—otherwise regressions creep back with model updates.

## Summary

Robust evaluation **stacks** executable checks, trace analytics, calibrated judges, and risk-weighted sampling. Treat public benchmarks as **useful pressure** but not a substitute for domain fixtures.

## Sources and further reading

- SWE-Bench and related software engineering agent benchmarks.
- OpenAI and Anthropic documentation on evals and tracing.
- Literature on LLM-as-judge limitations and debiasing.

## See also

- [Production case studies](production-case-studies.md)
- [Cost analysis](cost-analysis.md)
- [Anatomy of a good agent](anatomy-of-a-good-agent.md)
- Concepts: [Agent Evaluation](../concepts/agent-evaluation.md), [Agent Testing Patterns](../concepts/agent-testing-patterns.md), [Observability](../concepts/observability.md), [Feedback Loops](../concepts/feedback-loops.md)
- Course: [Agent Factory course](../../course/README.md)
