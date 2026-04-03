# Module 04: System Prompts for Agents

**Duration:** approximately 30 minutes  
**Prerequisites:** Module 01 (What Are Agents); Module 03 (The Agent Loop) recommended for context on tool cycles.

---

## Learning objectives

By the end of this module, you should be able to:

- **Structure** a system prompt with persona, constraints, tool instructions, and guardrails.
- Explain how **agent** prompts differ from **single-turn chatbot** prompts.
- **Author** tool usage guidance that reduces ambiguity and misuse.
- **Spot** common prompt mistakes that cause unreliable or unsafe agent behavior.

---

## 1. System prompt anatomy: persona + constraints + tool instructions + guardrails

A durable agent system prompt usually covers four layers:

**Persona**  
Who the agent is for the user and what tone or expertise to project. Keep it **task-aligned** (“senior backend reviewer”) rather than generic (“helpful assistant”) when possible.

**Constraints**  
Hard limits: allowed data sources, environments (sandbox vs prod), maximum steps, what must **never** be done without human approval, output format expectations.

**Tool instructions**  
For each tool: **when** to use it, **inputs** (with examples), **outputs** (how to interpret), and **fallbacks** if the tool errors.

**Guardrails**  
Refusal boundaries, PII handling, escalation rules, and how to behave on ambiguity (“ask a clarifying question” vs “state assumptions explicitly”).

Skipping any layer invites predictable failures: wrong tone (persona), scope creep (constraints), tool soup or no tools (tool instructions), incidents (guardrails).

---

## 2. How agent prompts differ from chatbot prompts

**Chatbot prompts** often optimize for **single responses**: one coherent reply per user message, minimal commitment to future action.

**Agent prompts** must optimize for **sequences**: the model will see its own prior thoughts and tool outputs. Therefore:

- **Idempotency and hygiene**: instruct how to **avoid repeating** failed actions blindly.
- **Termination**: when to return a **final** answer vs call another tool.
- **Error handling**: how to summarize tool failures and what to try next.
- **State discipline**: what to track mentally vs what is already in the provided state block.

Agent prompts are closer to **operating procedures** than to marketing copy.

---

## 3. Tool instruction design: when to use each tool, input/output format

For each tool, document:

1. **Intent** — One line: what problem this tool solves.  
2. **Preconditions** — Required prior steps or data (e.g., “ticket_id must be validated”).  
3. **Arguments** — Field-by-field with types and an **example JSON** payload.  
4. **Postconditions** — What a successful response means; what **not** to infer.  
5. **Errors** — Typical failure codes and the **allowed** retries.

Example fragment (illustrative):

```markdown
## Tool: `search_docs`

- Use when the user’s question may be answered from internal documentation.
- Do NOT use for executing code or modifying files.
- Input: `query` (string, max 200 chars), optional `product` (enum: A|B).
- Output: list of `{ "title", "url", "snippet" }`; snippets are not authoritative—open `url` for full pages when citing.
- On empty results: broaden query once; if still empty, tell the user and stop searching.
```

Prefer **one primary tool** per subgoal to reduce ambiguous choice.

---

## 4. Behavioral guardrails in prompts

Guardrails belong in the system prompt **and** in code (allowlists, output validation). Prompt-side guardrails should be **specific**:

- **Data:** “Do not paste secrets or full credit card numbers; redact with `[REDACTED]`.”  
- **Actions:** “Never call `deploy_production` without `human_approval_token` in state.”  
- **Quality:** “If confidence is low, list assumptions and request confirmation before irreversible steps.”

Avoid vague “be ethical”; replace with **testable** behaviors your evals can check.

---

## 5. Common prompt mistakes for agents

**Omitting termination rules**  
The model loops or hedges forever. Fix: explicit “stop when …” and structured `FINAL` format.

**Tool catalog without selection logic**  
Twenty tools with equal priority → random calls. Fix: decision rubric or phased tool availability.

**Contradictions**  
“Be concise” plus “show all reasoning” without priority. Fix: separate **internal** reasoning channel or length limits per phase.

**Overfitting to demo phrasing**  
Brittle triggers like “always call tool X first.” Fix: goal-based criteria tied to user intent.

**Security by optimism**  
Assuming the model will refuse misuse. Fix: enforce permissions **outside** the prompt; prompt is backup, not primary control.

---

## Exercises

### Exercise 1: System prompt for a code review agent

Write a full system prompt (target 400–800 words) for an agent that:

- Reads a pull request diff (provided as context or via a `fetch_diff` tool you describe).  
- Comments on **correctness**, **tests**, **security**, and **maintainability**.  
- Uses at most **two** hypothetical tools (name them and document usage).  
- Includes **guardrails** (no destructive repo actions; no leaking other teams’ code if absent from diff).  
- Specifies **output format**: summary, numbered findings with severity, optional questions to the author.

### Exercise 2: Audit a given system prompt

Take an existing agent system prompt from your project or a public template. Create a checklist table with columns: **Component** (persona / constraints / tools / guardrails), **Present?** (Y/N), **Gap**, **Suggested fix** (one sentence). Identify at least **five** gaps or improvements.

---

## Further reading

- [Prompt engineering for agents (concept)](../wiki/concepts/prompt-engineering-for-agents.md) — patterns aligned with this curriculum.  
- [Guardrails (concept)](../wiki/concepts/guardrails.md) — defense in depth beyond prompting.

---

## Summary

Effective **agent system prompts** read like **policies**: clear persona, explicit **constraints**, **per-tool** procedures, and **guardrails** suited to multi-step runs. They differ from chatbot prompts by emphasizing **sequences**, **termination**, and **tool discipline**. Pair prompt design with **harness enforcement**; the prompt aligns the model, but code should **constrain** what is actually possible.
