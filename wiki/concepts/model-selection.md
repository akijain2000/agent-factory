# Model Selection

## What it is

**Model selection** is the practice of matching **capabilities, cost, latency, and risk** to each agent subtask. Frontier **multimodal** models (e.g. **GPT-4o**-class) excel at ambiguous reasoning and tool planning; **Claude**-family models often favor long-context coherence and careful instruction following; **Gemini** offerings integrate with Google ecosystems and vary by tier; **local** or **open-weight** models reduce data egress and per-token cost but shift burden to **ops**, **hardware**, and **evaluation**. Production agents rarely use one model for everything—they **route** by task type, confidence, and budget.

## Why it matters for agents

The loop multiplies inference cost and latency. A model that is “good enough” for chat may be **too slow** for tight tool loops or **too expensive** at high volume. Wrong choices show up as **hallucinated tool args**, brittle JSON, or inability to recover from errors—problems that **evaluations** attribute to “the agent” when the root cause is **routing**.

Latency **SLOs** often force **cascading** choices: a faster model for the first response with **upgrade** paths when confidence is low. Document **expected** p95 token latency per route so product and infra can reason about UX.

## How to implement it

1. **Task taxonomy:** label steps as **plan**, **extract**, **classify**, **summarize**, **code**, **verify**. Assign default models per label with **fallbacks** when unavailable.
2. **Routing rules:** start with **explicit** rules (if structured extraction then Model A); add **learned** or **classifier** routing only after baselines exist.
3. **Cost/quality/speed:** define **acceptance metrics** per task (schema validity, human win-rate, latency p95). Plot **Pareto** curves; pick operating points per tier (free vs enterprise).
4. **Sub-task models:** use a **small** model for intent and entity extraction, a **large** model for planning and exception handling, and a **code-specialized** model for implementation when quality gains justify it.
5. **Local models:** containerize with pinned weights; run **offline eval** for regression on each upgrade; monitor **VRAM** and batching; keep **escape hatch** to cloud for edge cases.
6. **Versioning:** pin **model ids** in config; canary new versions on a slice of traffic; roll back via feature flags.

7. **Structured output fit:** some families adhere to **JSON schema** or **tool** modes more reliably—weight that in routing for extraction and planning steps.

**Evaluation gates:** no routing change ships without **offline** sets and **shadow** or **canary** online checks.

## Provider diversity

Using multiple providers improves **resilience** (outage failover) but increases **compliance** and **billing** surface. Standardize on a thin **adapter** layer in the harness.

Keep **capability matrices** (context length, vision, function calling, batch APIs) in source control and review quarterly—provider roadmaps move quickly.

For **regulated** workloads, record **data processing** agreements and **retention** settings per route, not only per vendor account.

**Embeddings** and rerankers are part of routing stacks—version them alongside chat models when retrieval quality shifts.

## Common mistakes

- One **global** model for all tenants regardless of SLA or budget.
- Swapping models without **re-running** tool-schema and safety evals.
- Optimizing **average** quality while **tail** failures (bad tool calls) dominate incidents.
- Ignoring **context length** differences when migrating between families.
- Routing by **marketing** tier names instead of measured **task** accuracy.
- Failing to test **non-English** locales on the cheaper route.

## References to course modules

These map to the **23-module Agent Factory course** (see [`../../course/README.md`](../../course/README.md) when published).

- **Module 13 — Framework Selection** — policies, routing, and provider or model tiering.
- **Module 17 — Agent Evaluation and Testing** — measuring quality per model and task.
- **Module 20 — Deployment and Scaling** — tying model choice to cost, quotas, and capacity.

Full curriculum index: [`../../course/README.md`](../../course/README.md) (when present).

## See also

- [Cost Optimization](cost-optimization.md)
- [Agent Evaluation](agent-evaluation.md)
- [Context Window Management](context-window-management.md)
- [Structured Outputs](structured-outputs.md)
- [Agent Loop](agent-loop.md)
