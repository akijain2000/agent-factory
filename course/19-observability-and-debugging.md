# Module 19: Observability and Debugging

**Duration:** approximately 35 minutes  
**Prerequisites:** Module 03 (The Agent Loop); Module 17 (Agent Evaluation and Testing) recommended.

---

## Learning objectives

By the end of this module, you should be able to:

- **Implement** tracing that captures decisions, tool calls, state transitions, and token usage.
- **Track** costs per run, per user, and per feature with actionable aggregation.
- **Debug** long multi-step runs by narrowing traces to anomalies and failure fronts.
- **Design** logging that supports on-call response without drowning storage and privacy controls.

---

## What to trace: decisions, tool calls, state transitions, token usage

A useful **trace span** per model turn includes:

- **Identifiers:** `run_id`, `parent_run_id`, `user_id` (hashed if needed), `environment`.
- **Decision inputs:** compressed prompt metadata (hash, token count), retrieved doc ids, not necessarily full verbatim if policy forbids.
- **Tool calls:** name, arguments (redacted where needed), latency, HTTP status, error class.
- **State transitions:** FSM phase changes, checkpoint ids.
- **Token and cost:** prompt tokens, completion tokens, model id, billed cost if available.

Correlate with **business context**: `feature`, `experiment_variant`, `ticket_id`. That correlation turns “spend doubled” into “spend doubled on summarization after prompt change X.”

---

## Tracing tools: LangSmith, Braintrust, custom solutions

**Hosted platforms** (e.g., LangSmith, Braintrust) offer searchable traces, comparisons across runs, and dataset attachment for evals. They accelerate teams that do not want to build UIs.

**Custom solutions** store **OpenTelemetry**-style spans in your warehouse (BigQuery, ClickHouse) or object storage (JSONL per run). Tradeoffs:

- **Control:** you own PII handling, retention, and residency.
- **Cost:** you pay for storage and query engines; optimize with **sampling** for high-volume low-value paths.

Minimal custom event schema:

```json
{
  "ts": "2026-04-03T12:00:01Z",
  "run_id": "r_9f3a",
  "span": "tool.web_search",
  "duration_ms": 420,
  "input_hash": "sha256:...",
  "output_summary": "3 results, top domain wikipedia.org",
  "tokens": { "prompt": 1200, "completion": 80 }
}
```

Use **hashes** or **summaries** when storing full prompts violates policy; keep **rehydration** keys in a secure vault for incident response only.

---

## Cost tracking: per-run, per-user, per-feature budgets

Instrument every LLM call with **model**, **token counts**, and **unit pricing** (from your provider contract). Aggregate:

- **Per run:** total cost and cost by phase (plan vs execute vs verify).
- **Per user / tenant:** for fairness, abuse detection, and quota enforcement.
- **Per feature:** which product surfaces drive margin erosion.

Enforce **budgets** with soft caps (warn, degrade model tier) and hard caps (stop run, notify). Surface **projected** cost before long autonomous loops.

```python
# Conceptual budget check
def before_llm_call(run_state, estimated_tokens: int) -> None:
    projected = run_state.spent_usd + estimate_cost(run_state.model, estimated_tokens)
    if projected > run_state.budget_usd:
        raise BudgetExceeded("Defer to cheaper model or human")
```

Reconcile **provider invoices** with internal meters monthly; pricing and caching discounts drift.

---

## Debugging long runs: finding the needle in a 50-step trace

Tactics:

1. **Index** tool calls and errors; sort by **first error** or **first retry burst**.
2. **Diff** traces: same scenario, two commits—highlight changed tool sequences or token jumps.
3. **Collapse** successful middle steps; expand around **branch points** (plan revisions, tool failures).
4. **Replay** from checkpoint **N** with frozen tool mocks to reproduce without full cost.

If the model **lost the plot**, check **summarization** boundaries: did a digest drop a constraint? If tools **misbehaved**, verify **argument** schema and **idempotency** on retries.

---

## Logging strategy: what to log, what to skip

**Log:** errors, approval decisions, policy violations, **anonymized** latency percentiles, and **aggregated** token usage.

**Avoid logging:** full credit cards, health data, raw passwords, and **complete** prompts if your retention or jurisdiction forbids it. Use **structured** fields and **redaction** middleware on tool I/O.

**Sampling:** log 100% of failures and 1–5% of successes in high-traffic paths; tune so on-call can still see **patterns**.

**Retention:** align with GDPR/CCPA and internal policy; shorter for raw prompts, longer for **metadata** and **hashes**.

**Alerting:** tie traces to **SLOs**: p95 latency per tool, error rate on payments-related actions, and **cost per successful task**. Page on **burn rate** (error budget consumption), not single blips, to reduce fatigue.

---

## Study: Paperclip's cost dashboard, LiteLLM unified tracking

**Paperclip**-style agent teams often ship **cost dashboards** tied to **orchestration**: which sub-agent, which model route, which customer job burned budget. Borrow the idea of **first-class cost as a metric** next to latency and success rate.

**LiteLLM** (and similar gateways) centralize **routing**, **rate limits**, and **usage** across providers. Even if you do not adopt the gateway, mirror its **unified logging** shape so swapping models does not break dashboards.

---

## Exercises

1. **Add tracing**  
   For a small agent loop (pseudocode acceptable), define **five** span types you would emit, the **fields** on each, and which fields get **redacted** in production. Include how you would link spans to a single `run_id`.

2. **Cost tracking dashboard**  
   Sketch a **dashboard** (wireframe or bullet spec) with at least four widgets: daily spend, spend by model, spend by feature, and **budget overrun** alerts. List the **SQL or metrics** each widget needs from your trace tables.

---

## Further reading

- [Observability (wiki)](../../wiki/concepts/observability.md)
- [Cost optimization (wiki)](../../wiki/concepts/cost-optimization.md)
