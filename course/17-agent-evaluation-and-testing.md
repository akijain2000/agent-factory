# Module 17: Agent Evaluation and Testing

**Duration:** approximately 40 minutes  
**Prerequisites:** Module 03 (The Agent Loop); Module 05 (Tool Design) recommended.

---

## Learning objectives

By the end of this module, you should be able to:

- **Build** behavioral test suites that assert outcomes and trajectories, not only final strings.
- **Analyze** execution traces to localize failures in planning, tool use, or policy.
- **Implement** benchmark-based evaluation with reproducible harnesses and baselines.
- **Score** agent compliance against explicit guardrails and system constraints.

---

## Why agent testing is different from software testing

Traditional software tests assume **deterministic** functions: same inputs yield same outputs. Agents combine **stochastic** models, **open-ended** tool environments, and **emergent** multi-step behavior. A “correct” answer may vary in wording; a “wrong” run may still look plausible.

Implications:

- Prefer **property-based** and **behavioral** assertions over brittle string equality on full replies.
- Run **many** trials per scenario when sampling matters; report **distributions**, not single scores.
- Separate **functional** correctness (did the task complete?) from **process** quality (did it follow policy, stay in budget, avoid unsafe tools?).

Treat evaluation as **continuous**: every prompt or tool schema change can shift behavior without a compile error.

---

## Behavioral tests: input/output expectations, multi-step scenarios

**Behavioral tests** specify **initial state**, **user or task inputs**, **allowed tools**, and **expected artifacts or outcomes**. They often assert on **structured** outputs (JSON, file diffs, API side effects) rather than natural language alone.

Example structure:

```yaml
scenario: refund_high_value_order
given:
  order_id: "ord_123"
  order_total_usd: 500
  policy: refunds_over_200_require_supervisor
expect:
  final_state: escalated_or_denied_without_chargeback
  tools_called:
    - name: lookup_order
    - name: request_supervisor_approval  # must appear before refund_issue
  must_not_call: [refund_issue]
```

**Multi-step scenarios** chain tool mocks or a sandbox so the agent experiences realistic feedback loops. Use **fixtures** for tool responses to keep tests fast and deterministic where possible.

**Flake control:** for LLM assertions, combine **deterministic checks** (schema, tool sequence) with optional **judge models** or human spot checks for open-ended quality.

---

## Trace analysis: debugging agent decisions step by step

A **trace** records each model turn: prompts (or hashes), completions, **tool calls**, tool results, and **token/cost** metadata. Debugging means walking the timeline and asking:

1. Did the **plan** match the user goal (hallucinated constraints, missed steps)?
2. Were **tool arguments** well-formed and grounded in prior observations?
3. Did **tool errors** propagate correctly, or did the model ignore failures?
4. Did **context truncation** drop critical facts before a bad decision?

Annotate traces with **run_id**, **scenario_id**, and **git revision** of prompts so regressions are attributable. For long runs, build a **step index** (turn number, tool name, latency) and jump to anomalies (retries, loops, spikes in tokens).

---

## Benchmark suites: SWE-Bench, HumanEval, custom benchmarks

**Public benchmarks** anchor comparisons: **HumanEval**-style coding tasks measure single-shot code generation; **SWE-Bench**-style suites evaluate **repository-level** repair with tests. They are useful for **capability** tracking but rarely match your product’s exact stack or policies.

**Custom benchmarks** should mirror **real tickets**: same tools, same APIs, anonymized production-like inputs. Define:

- **Pass criteria** (tests pass, ticket resolved, policy satisfied).
- **Timeout** and **step budget** to penalize runaway loops.
- **Versioning** of benchmark JSON or task packs so scores are comparable across model changes.

```python
# Conceptual: run harness returns structured result
def evaluate_agent(agent, task_pack) -> dict:
    results = []
    for task in task_pack:
        trace = agent.run(task.input, tools=task.allowed_tools)
        results.append({
            "task_id": task.id,
            "success": task.grader(trace),
            "steps": len(trace.tool_calls),
            "cost_usd": trace.total_cost,
        })
    return aggregate(results)
```

---

## Compliance scoring: does the agent follow its guardrails?

**Compliance** tests encode **must** and **must not** rules: PII handling, disallowed tools, escalation when confidence is low, citation of sources. Score with a **rubric** (binary checks + weighted deductions).

Examples of machine-checkable compliance signals:

- No `send_email` without `draft_review` in trace.
- System prompt **forbidden topics** never appear in user-visible outputs (with careful definition of “user-visible”).
- **Structured** `decision` field matches allowed enum (`approve`, `reject`, `escalate`).

Combine **automated** rubrics with periodic **human audit** on a stratified sample; models adapt to narrow automated checks over time.

---

## A/B testing agents in production

Ship two **policies** (prompts, models, or tool sets) to disjoint traffic cohorts. Track **task success**, **latency**, **cost**, **human takeover rate**, and **incident** counts. Use **consistent** randomization keys (e.g., `user_id` hash) to avoid within-user flicker.

Guardrails for A/B:

- **Kill switch** per variant.
- **Minimum exposure** before trusting lift; watch **variance** on rare failure modes.
- **Ethical** parity: do not A/B on safety-critical behavior without explicit review.

---

## Study: AutoAgent's score-driven hill-climbing, Harbor benchmark format

**AutoAgent**-style systems use a **harness loop**: the agent proposes changes; a **scorer** (tests, linters, benchmarks) returns a scalar or vector signal; the loop **iterates** toward higher scores. Lessons: make the score **aligned** with real goals (avoid optimizing only for syntax lint while breaking behavior).

**Harbor** and similar benchmark **formats** emphasize **containerized** tasks, **fixed** dependencies, and **objective** graders. When designing internal suites, borrow **isolation** and **reproducible environment** ideas even if you do not adopt the full spec.

---

## Exercises

1. **Five behavioral test cases**  
   For a given agent spec (e.g., internal support bot or code assistant), write **five** behavioral test cases in YAML or structured JSON: include at least one **multi-step** scenario, one **negative** case (must not call a tool), and one **policy** case (escalation or refusal).

2. **Trace analysis**  
   Take a provided (or anonymized) agent trace where the outcome was wrong. **Identify** the first turn where the trajectory diverged from a reasonable policy, cite **evidence** from tool inputs/outputs, and propose **one** harness or prompt change that would likely prevent recurrence.

---

## Further reading

- [Agent evaluation (wiki)](../../wiki/concepts/agent-evaluation.md)
- [Agent testing patterns (wiki)](../../wiki/concepts/agent-testing-patterns.md)
- [Agent evaluation methods (wiki)](../../wiki/research/agent-evaluation-methods.md)
