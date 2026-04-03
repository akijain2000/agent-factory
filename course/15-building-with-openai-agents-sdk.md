# Module 15: Building with OpenAI Agents SDK

**Duration:** approximately 45 minutes  
**Prerequisites:** Module 03 (The Agent Loop); Module 05 (Tool Design); Module 10 (Multi-Agent Patterns) recommended.

---

## Learning objectives

By the end of this module, you should be able to:

- **Configure** the **Agent** class with model, instructions, and tools appropriate to a task.
- **Implement** **handoffs** between specialized agents with clear ownership of user-facing turns.
- **Add** **guardrails** for input and output validation before side effects execute.
- **Integrate** **MCP** tool servers where appropriate.
- **Use** **tracing** to debug multi-step agent execution in development and staging.

---

## The Agent class: model, instructions, tools

An **Agent** bundles:

- **Model** — which OpenAI model and parameters (temperature, reasoning effort where applicable).
- **Instructions** — system-level behavior: tone, policies, and when to call tools.
- **Tools** — function schemas the runtime executes when the model selects them.

```python
# Illustrative pattern — consult current SDK for exact imports and types
# agent = Agent(
#     name="Billing assistant",
#     instructions="You help with invoices. Never guess amounts; use tools.",
#     model="gpt-4.1",
#     tools=[get_invoice, create_ticket],
# )
```

**Instructions** should encode **boundaries** (PII handling, escalation phrases) not just persona fluff. Keep **tool descriptions** aligned with harness behavior—ambiguous tools produce ambiguous calls.

**Testing:** snapshot the **tool call** arguments your harness receives for fixed prompts; do not only assert final natural language.

---

## Handoffs: transferring between specialized agents

**Handoffs** move control from one Agent to another when the task changes—e.g., triage bot → refund specialist → shipping specialist. The SDK models **which** agent is active and how **context** is passed.

Design rules:

- **One** agent should “own” the user reply for a given turn unless a handoff explicitly occurs.
- Pass **structured** context forward (order id, locale, entitlement flags), not only chat prose.
- Define **exit** conditions so sub-agents do not ping-pong forever.

```python
# Conceptual: specialist agents and a triage agent that hands off
# triage = Agent(..., handoffs=[refunds_agent, shipping_agent])
# refunds_agent = Agent(..., handoffs=[triage])  # only if you need return path
```

**Anti-pattern:** five handoffs for a question a single well-instructed agent could answer—each hop adds **latency** and **failure** surface.

---

## Guardrails: input/output validation

**Guardrails** run **before** or **after** model generations to block policy violations, injection-like instructions, or unsafe tool args.

Typical layers:

- **Input:** length limits, regex allowlists for IDs, profanity or hate classifiers if required.
- **Output:** JSON schema validation for structured replies; blocklists for secrets patterns (`sk-`, PEM headers).
- **Tool args:** validate against Pydantic (or similar) **before** executing side effects.

```python
# Pseudocode: output guardrail concept
# @output_guardrail
# def no_raw_secrets(ctx, output):
#     if looks_like_api_key(output.text):
#         return GuardrailResult(tripwire_triggered=True, message="Redacted.")
#     return GuardrailResult(tripwire_triggered=False)
```

**Balance:** over-strict guardrails cause **false positives** and user frustration; log **tripwire** counts to tune rules.

---

## MCP integration: connecting external tools

The **Model Context Protocol** exposes tools (and sometimes resources) from servers your app runs or trusts. Wiring MCP into the Agents SDK lets models call **filesystem**, **browser**, or **internal APIs** through a standard surface.

**Operational checklist:**

- Run MCP servers with **least privilege** (read-only roots, network egress allowlists).
- **Version** tool schemas; breaking changes should be deploy-coordinated.
- **Timeout** and **cancel** long-running MCP calls so one stuck server does not block the runner.

Treat MCP as **untrusted** unless the server is yours and audited—malicious or compromised servers can exfiltrate data via tool results.

---

## Tracing: debugging agent execution

**Tracing** records spans: model calls, tool invocations, handoffs, guardrail results. Use traces to answer:

- Why did the model **not** call `create_ticket`?
- Which handoff added **400 ms**?
- Did the guardrail fire on **input** or **output**?

In development, enable **verbose** or **dashboard** exporters; in production, sample traces and **scrub** PII before export.

**Correlation:** propagate `trace_id` / `conversation_id` from your API gateway through the runner so support can open one trace per ticket.

---

## Walkthrough: building a customer service agent with handoffs

**Architecture:**

1. **Triage Agent** — classifies intent: `billing`, `shipping`, `account`, `other`.
2. **Billing Agent** — tools: `lookup_charge`, `refund_eligibility` (read-only), `create_billing_ticket`.
3. **Shipping Agent** — tools: `track_package`, `open_lost_package_case`.
4. **Guardrails** — block raw credit card numbers in user input; redact account numbers in outbound text.
5. **Handoffs** — triage hands off once; specialists hand back to triage only if user changes topic.

**Flow:** User message → triage → (optional handoff) → specialist tools → final answer. **Human escalation** tool for confidence below threshold.

**Metrics:** deflection rate, mean handoffs per session, guardrail trip rate, tool error rate.

---

## Exercises

### Exercise 1: Build a two-agent system with handoffs

Design (diagram + short spec) **two** agents: a **router** and a **specialist**. List three **concrete** user utterances that should trigger a handoff and two that should **not**. Specify what structured fields the router passes to the specialist.

### Exercise 2: Add guardrails to an existing agent

Pick an agent prompt you use today. Add **one input** and **one output** guardrail rule with clear **tripwire** behavior (block, rewrite, or escalate). Write a **test case** where the guardrail should fire and one where it should not.

---

## Further reading

- [OpenAI agent patterns (wiki)](../wiki/research/openai-agent-patterns.md) — project-specific notes and patterns.
- [OpenAI Agents SDK documentation](https://openai.github.io/openai-agents-python/) — official reference for agents, handoffs, guardrails, and tracing (verify against the latest SDK version).
