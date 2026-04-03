# Module 16: Building with Anthropic

**Duration:** approximately 45 minutes  
**Prerequisites:** Module 03 (The Agent Loop); Module 05 (Tool Design); Module 04 (System Prompts) recommended.

---

## Learning objectives

By the end of this module, you should be able to:

- **Implement** **Claude tool use** with clear schemas, parallel tool calls where appropriate, and robust parsing of results.
- **Apply** **extended thinking** for hard planning or analysis steps inside an agent loop.
- **Describe** **computer use** patterns and their safety implications (screen capture, UI actions).
- **Build** **Anthropic-native** agents using orchestrator-worker and routing patterns suited to Claude.
- **Optimize** **system prompts** and context packing for token efficiency without hiding constraints.

---

## Claude tool use: function calling, structured outputs

Claude’s **tool use** flow mirrors the standard loop: assistant message may include `tool_use` blocks; your harness runs tools; you return `tool_result` content blocks.

**Schema design:**

- Prefer **fewer, well-named** tools over dozens of thin wrappers.
- Document **units** and **enums** in parameter descriptions—the model reads them.
- Return **machine-readable** tool results (JSON strings or structured text) to simplify the next turn.

```python
# Illustrative message flow (conceptual)
# messages = [
#   {"role": "user", "content": "What failed in deploy job 8821?"},
# ]
# # assistant returns tool_use: get_ci_logs(job_id="8821")
# messages.append(assistant_message)
# messages.append(tool_result_message("get_ci_logs", logs_json))
# # assistant returns final natural language answer
```

**Parallel tools:** when tasks are independent (fetch repo, fetch ticket), allow parallel `tool_use` blocks and execute concurrently with **per-tool timeouts**.

**Structured outputs:** combine tool use with a final **schema-constrained** step (or a dedicated “emit JSON” tool) for downstream pipelines.

---

## Extended thinking: complex reasoning in agent loops

**Extended thinking** (where available) lets Claude expose a separate reasoning channel before the visible answer. In agents, use it for:

- **Planning** multi-step refactors or investigations.
- **Risk assessment** before irreversible tools.

Pattern: **thinking-enabled** call for `plan` → regular calls for tool execution following the plan → optional **thinking** again if the situation diverges.

**Caveats:**

- **Do not** treat thinking text as user-facing; it may contain exploratory reasoning.
- **Log** policy: decide whether thinking is stored (compliance, debug) or stripped after the turn.
- **Budget** thinking tokens—they count toward limits and cost.

---

## Computer use: screen reading, mouse/keyboard control

**Computer use** APIs let models consume **screenshots** and emit **actions** (click, type, scroll). This enables agents to operate legacy UIs without APIs.

**Safety:**

- Run inside **VMs** or **containerized** desktops with **no** access to production secrets.
- **Block** credential entry except via **controlled** secret injection your harness performs.
- **Rate-limit** actions; require **human** approval for send/submit/purchase classes of clicks.

**Reliability:** prefer **APIs** when they exist; computer use is slower and flakier. Use **deterministic** selectors or accessibility trees when the platform exposes them instead of pure pixel guessing.

---

## Anthropic agent patterns: prompt chaining, routing, orchestrator-workers

**Prompt chaining:** linear pipeline of Claude calls, each with a narrow job—good when intermediate outputs must be **audited** between steps.

**Routing:** a lightweight model or rules pick **which** specialist prompt or tool set runs next; keep the router **simple** to debug.

**Orchestrator-workers:** a **lead** Claude decomposes the task; **workers** (possibly same model, different tools) handle subtasks; orchestrator **merges** results. Useful for code review across files or multi-source research.

```text
Orchestrator: "Subtask A: summarize src/auth/*; Subtask B: summarize tests; merge findings."
Worker A / Worker B: restricted file globs + read-only tools
Orchestrator: integrated report + residual risks
```

**Failure handling:** workers should return **structured errors** (`file_not_found`, `timeout`) so the orchestrator can retry or escalate.

---

## Claude-specific best practices: system prompt design, token efficiency

**System prompt:**

- Put **non-negotiables** up front: security rules, tool-call discipline, citation requirements.
- Separate **stable** policy (rarely changes) from **volatile** task text (per-request) to maximize **prompt cache** benefits where applicable.

**Token efficiency:**

- **Summarize** long tool outputs before feeding them back; keep raw blobs in object storage with **references** in context.
- Avoid repeating **identical** system instructions in every user turn if your client supports **caching** or **pinned** system blocks.
- Use **XML or markdown** sections consistently so the model can scan quickly (`<context>`, `<task>`).

**Evaluation:** regression-test with **representative** Claude snapshots (Sonnet vs Opus) if you rely on nuanced reasoning.

---

## Walkthrough: building a code analysis agent with Claude

**Goal:** Given a repo slice, produce a **risk report**: security hotspots, test gaps, dependency concerns.

1. **Tools:** `list_files`, `read_file`, `grep`, `parse_manifest` (package.json / pyproject).
2. **Flow:** extended thinking for **plan** → parallel `read_file` on hotspots → synthesize report with **citations** (`path:line`).
3. **Guardrails:** refuse to **exfiltrate** secrets; redact tokens if found in file contents before logging.
4. **Output:** structured JSON + short executive summary for humans.

**Acceptance tests:** known vulnerable pattern in fixture file must appear in output; benign repo should not hallucinate **critical** issues without evidence.

---

## Exercises

### Exercise 1: Build a tool-using agent with Claude

Specify **three tools** (names, parameters, and return shapes) for a domain you care about. Write the **system prompt** section that tells Claude **when** to call each tool and **when** to answer without tools. Include one example user message and the expected **first** assistant action (tool vs text).

### Exercise 2: Add extended thinking to a planning step

Take a task that currently uses a single long completion. Split it into: (a) a **planning** call with extended thinking enabled, (b) **execution** calls that follow the plan without thinking. Document what you **strip** from logs before user-facing channels.

---

## Further reading

- [Anthropic agent patterns (wiki)](../wiki/research/anthropic-agent-patterns.md) — curated patterns and notes for Claude-centric agents.
- [Anthropic tool use documentation](https://docs.anthropic.com/en/docs/build-with-claude/tool-use) — official guides and API details (verify current model support for thinking and computer use).
