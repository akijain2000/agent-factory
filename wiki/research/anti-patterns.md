# Agent Anti-Patterns: A Catalog

Anti-patterns are attractive defaults that **scale poorly** under real users, flaky tools, and model drift. This catalog groups failures seen across demos, early production systems, and research harnesses—use it as a review checklist before shipping.

## God agent and prompt soup

A single prompt tries to **reason, plan, retrieve, critique, and format** while also encoding business policy. Result: unmaintainable prompts, opaque failures, and no seam for testing. Prefer **factored steps** with narrow contracts.

## Over-tooling

Exposing dozens of overlapping tools **increases** mis-selection and description collisions. Models confuse similar names; latency grows. Prefer **small, orthogonal** surfaces and compose higher-level tools in code when logic is deterministic.

## Premature multi-agent

Multiple personas before a **single-agent loop** is stable multiplies coordination bugs, handoff ambiguity, and cost. Multi-agent pays off when subtasks are **genuinely parallel** or require **separation of concerns** (e.g., generator vs judge)—not as default architecture.

## Context abuse

Stuffing full histories, raw logs, and every retrieved chunk every turn burns budget and **dilutes attention**. Anti-patterns include: no summarization policy, recursive “paste everything again,” and treating the window as a database. Prefer **summaries, pointers, and on-demand retrieval**.

## Sycophantic loops

The model agrees with its own bad plan or repeats failed tool calls to appear helpful. Mitigations: **explicit critique roles**, **diverse sampling** on retry, hard **caps** on identical actions, and logging **tool outcomes** the model cannot rewrite.

## Infinite retries and unbounded autonomy

“Try until it works” without backoff, circuit breaking, or human escalation produces runaway cost and silent harm. Pair every loop with **max steps**, **max cost**, and **escalation** to a narrower task or a person.

## Brittle parsing and regex on free text

Parsing model prose with fragile regex breaks on the next tokenizer or style shift. Prefer **structured outputs** (JSON schema, tool arguments) at boundaries.

## Silent error swallowing

Catching exceptions to keep the chat “smooth” hides incidents from operators. Surface **correlated errors**, degrade gracefully, and preserve **audit trails** for sensitive actions.

## Over-privileged tools

Filesystem, network, and shell tools with broad scope turn prompt injection into **remote code execution**. Default-deny, path allowlists, and **human approval** on sensitive operations.

## LLM-as-the-only-judge

Using a single model to score another without calibration invites **grade inflation** and **shared blind spots**. Combine with executable checks, human spot audits, or **disagreement-aware** ensembles where affordable.

## Monoculture models and prompts

Shipping without **versioning** prompts, tools, and evals guarantees surprise regressions when providers update base models. Version all three and run **regression evals** in CI.

## Sources and further reading

- Anthropic, *Building Effective Agents*: workflows before agents.
- OpenAI agent guidance: when autonomy helps vs hurts.
- Wiki examples under `wiki/examples/bad/` for concrete scenarios.

## See also

- [Anatomy of a good agent](anatomy-of-a-good-agent.md)
- [Agent vs workflow](agent-vs-workflow.md)
- [Multi-agent landscape](multi-agent-landscape.md)
- [Agent evaluation methods](agent-evaluation-methods.md)
- Concepts: [Guardrails](../concepts/guardrails.md), [Context Window Management](../concepts/context-window-management.md), [Error Recovery](../concepts/error-recovery.md), [Multi-Agent Orchestration](../concepts/multi-agent-orchestration.md), [Tool Design](../concepts/tool-design.md)
- Course: [Agent Factory course](../../course/README.md)
