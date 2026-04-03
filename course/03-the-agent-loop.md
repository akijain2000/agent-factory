# Module 03: The Agent Loop

**Duration:** approximately 40 minutes  
**Prerequisites:** Module 01 (What Are Agents); basic comfort reading pseudocode or Python-like snippets.

---

## Learning objectives

By the end of this module, you should be able to:

- Explain the **plan–act–observe–reflect** cycle as the conceptual core of agent behavior.
- Describe the **ReAct** pattern and relate it to tool-calling LLM APIs.
- Contrast **free-form** loops with **state-machine** control for reliability.
- Define **termination** strategies and **infinite loop** mitigations.

---

## 1. The fundamental loop: plan–act–observe–reflect

Most agent harnesses implement a variation of this cycle:

1. **Plan** — Given goal and current context, decide what to do next (explicit plan object or implicit next action).
2. **Act** — Invoke a tool, run code, or emit a structured command.
3. **Observe** — Record tool output, errors, and environment deltas in context or state.
4. **Reflect** — Update beliefs, revise plan, or decide to finish.

In practice, “plan” and “reflect” may be **one model call** that outputs either a final answer or a tool request. The harness is responsible for **serializing observations** back into the prompt or state store on the next iteration.

**Key idea:** The loop is not magic; it is **explicit control flow** around the model. Your code owns **iteration**, **permissions**, and **stopping rules**.

---

## 2. ReAct pattern dissected with examples

**ReAct** (reasoning + acting) interleaves **natural language rationales** with **actions** (often tool calls). A simplified turn looks like:

```text
Thought: I need the latest error rate for service X before answering.
Action: query_metrics(service="X", window="1h")
Observation: error_rate=0.02, p99_latency_ms=450
Thought: The error rate is within SLO; I can report stability.
Final: Service X is healthy over the last hour (2% errors, p99 450ms).
```

In API terms, the model might return structured JSON instead of free-form “Thought/Action” lines:

```json
{
  "reasoning": "Fetch metrics for X for the last hour.",
  "tool": "query_metrics",
  "arguments": { "service": "X", "window": "1h" }
}
```

The harness executes `query_metrics`, appends an **observation** message, and calls the model again until it returns a **final** response or hits a limit.

**Why it works:** Observations **ground** the next reasoning step in facts rather than pure hallucination—when tools are trustworthy and schemas are clear.

---

## 3. State machines vs free-form loops

**Free-form loop**  
The model chooses any next action from a broad set each iteration. Maximum flexibility; higher risk of **drift**, repeated mistakes, or incoherent sequences.

**State-machine-guided loop**  
The harness constrains **which actions are legal** in the current phase. Example phases: `GATHER_CONTEXT` → `DRAFT` → `VERIFY` → `DELIVER`.

```text
states = { GATHER, DRAFT, VERIFY, DONE }
transitions:
  GATHER  -> DRAFT   when required_docs_retrieved
  DRAFT   -> VERIFY  when draft_exists
  VERIFY  -> DRAFT   when checks_failed (max 2 retries)
  VERIFY  -> DONE    when checks_passed
```

The model still reasons inside each state, but **invalid jumps** are blocked by code. This pattern improves **auditability** and **testability** (you can unit test transitions independent of the model).

**When to use which:** Prototyping and exploratory agents often start free-form; **production** systems usually introduce **phases**, **gates**, or **explicit planners** as reliability requirements grow.

---

## 4. Loop termination: max iterations, success criteria, timeouts

**Max iterations**  
Hard cap on loop count. Simple and essential; combine with logging when the cap is hit to detect **stuck** behavior.

**Success criteria**  
Structured check: e.g., model returns `finish=true`, or validator passes on output schema, or human approves.

**Timeouts**  
Wall-clock limit per session or per phase. Protects user experience and infrastructure when tools hang.

**Composite policy** (recommended):

```text
stop if:
  final_answer_validated OR
  user_abort OR
  iterations >= N OR
  elapsed_time >= T OR
  cost_budget_exceeded
```

Expose **which clause fired** in observability; it tells you whether to tune prompts, tools, or limits.

---

## 5. Infinite loop prevention

Common causes:

- **Tool errors** interpreted as “try again forever” without backoff.
- **Ambiguous goals** so the model never emits a terminal action.
- **Duplicate observations** re-injected without deduplication, causing repetitive reasoning.

**Mitigations**

- **Detect repetition**: same tool + same arguments within k steps → escalate or ask human.
- **Exponential backoff** on transient failures; **circuit breakers** on persistent failures.
- **Require explicit “give up”** path in the prompt with a structured output for partial results.
- **Summarize** long traces instead of appending raw duplicates to context.

---

## Exercises

### Exercise 1: Minimal ReAct loop in pseudocode

Write pseudocode (not framework-specific) that:

1. Accepts `goal` and `max_steps`.  
2. In a loop, calls `llm.step(messages)` which returns either `{ "final": string }` or `{ "tool": name, "args": object }`.  
3. Executes tools via `tools.run(name, args)` and appends observations to `messages`.  
4. Stops on `final`, `max_steps`, or tool error policy you define.

Include comments for where **validation** of tool arguments would occur.

### Exercise 2: Termination criteria for three agent types

For each agent type below, specify **at least three** termination conditions (mix of success and failure), including one **safety** or **cost** condition:

1. **Customer support triage agent** (reads tickets, may query order system).  
2. **Repo documentation updater** (reads files, proposes patches).  
3. **Data analysis agent** (runs queries in a sandbox).

---

## Further reading

- [Agent loop (concept)](../wiki/concepts/agent-loop.md) — expanded treatment in this project’s wiki.  
- [Andrew Ng patterns (research)](../wiki/research/andrew-ng-patterns.md) — practical workflow patterns.  
- Yao et al., **ReAct: Synergizing Reasoning and Acting in Language Models** — original ReAct paper.

---

## Summary

The agent **loop** implements **plan–act–observe–reflect** under your harness’s rules.**ReAct** makes reasoning and tool use explicit in the trace.**State machines** trade some flexibility for **control and testability**. Always define **termination** with iteration, time, and success predicates, and add **anti-loop** guards as soon as tools can fail or repeat.
