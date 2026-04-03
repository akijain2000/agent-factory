# Module 09: Agent Design Patterns

**Duration:** approximately 45 minutes  
**Prerequisites:** Module 03 (The Agent Loop); Module 05 (Tool Design) recommended.

---

## Learning objectives

By the end of this module, you should be able to:

- **Master** Andrew Ng’s four agentic design patterns and map each to concrete system behaviors.
- **Implement** ReAct (reasoning plus action) and Reflexion (verbal reinforcement learning) style loops in prompts and harness code.
- **Choose** the right pattern for a task based on latency, cost, failure modes, and observability needs.

---

## Pattern 1: Reflection — self-evaluation and improvement loops

**Reflection** means the agent (or a second pass) **critiques** its own draft output or plan before finalizing. It is not free introspection; it is a **structured compare step**: draft, criteria, critique, revise.

Use reflection when quality matters more than raw speed (writing, code review prep, policy-heavy answers). Keep critiques **short and checklisted** so you do not blow the context budget.

```text
1. Produce draft_answer.
2. Critique draft_answer against: correctness, citations, tone, safety.
3. Produce final_answer addressing each critique item.
```

**Anti-patterns to avoid:** unbounded “think harder” loops without criteria; asking the model to critique without showing the **same facts** it saw when drafting (it will invent issues).

---

## Pattern 2: Tool use — extending capabilities through external tools

**Tool use** offloads **grounding** and **side effects** to code: search, databases, filesystem, APIs. The LLM proposes **which** tool and **with what arguments**; the harness runs tools and returns observations.

Design tools with **narrow contracts** (one verb per tool where possible), **typed parameters**, and **idempotent reads** where feasible. The pattern fails when the model must choose among dozens of overlapping tools (see Module 11).

**Observability:** log tool name, normalized args, latency, and outcome. That single line often explains “why the agent went wrong” faster than re-reading the whole chat.

---

## Pattern 3: Planning — task decomposition and execution planning

**Planning** separates **what to do** from **doing it**: produce a plan (steps, dependencies, success checks), then execute stepwise with tool results feeding the next step. Combines well with reflection (critique the plan before execution).

Use explicit **plan artifacts** in the transcript so you can resume after failures and audit decisions. The harness should **enforce** plan steps when safety demands it (e.g., “migrate” only after “backup verified”), not rely on the model to remember.

---

## Pattern 4: Multi-agent collaboration — agents working together

**Multi-agent** assigns **roles** (researcher, critic, coder) or **stages** (extract, transform, verify). Each agent may share a model or use different models; what matters is **clear handoffs** and **single-writer rules** for mutable state (see Module 10).

Do not add agents for ceremony; add them when **separation of concerns** or **adversarial critique** measurably improves outcomes.

---

## Choosing patterns: a practical lens

| Pattern | Strong when | Weak when |
|--------|-------------|-----------|
| Reflection | Output quality > speed; rubric exists | Latency-sensitive chat; no clear criteria |
| Tool use | Facts change; actions must be grounded | Task is pure language transform with no external truth |
| Planning | Many dependencies; retries are expensive | Simple single-shot tasks; plan cost exceeds execution |
| Multi-agent | Roles are truly different; critique helps | One competent loop + tools already wins in evals |

Combine patterns deliberately: **plan → reflect on plan → ReAct execute** is a common production stack.

---

## ReAct pattern deep dive with implementation

**ReAct** interleaves **Reasoning** traces with **Actions** (typically tool calls) and **Observations** (tool results). The loop continues until a stop condition (answer emitted, max steps, or human approval).

Illustrative turn shape:

```text
Thought: I need the latest error rate before recommending a rollback.
Action: metrics.query(service="checkout", window="1h")
Observation: p99_latency_ms=840, error_rate=0.02
Thought: Within SLO; recommend monitor-only.
Final: No rollback; continue canary at 10%.
```

In code, your harness parses `Action:` lines or structured JSON tool calls, executes, appends `Observation:`, and prompts again. **Cap steps** and **log every Thought** for debugging.

```python
# Minimal loop shape (illustrative)
MAX_STEPS = 12
for step in range(MAX_STEPS):
    msg = model.complete(messages)
    if tool_call := parse_tool_call(msg):
        obs = run_tool(tool_call)
        messages.append(assistant_turn(msg))
        messages.append(tool_observation_turn(obs))
    elif is_final_answer(msg):
        return msg
raise TooManyStepsError(step)
```

Prefer **structured** tool JSON from providers over fragile free-text parsing when you can.

---

## Reflexion pattern: learning from failures

**Reflexion** adds a **post-mortem** after a failed trajectory: the model summarizes **what went wrong**, **what it would do differently**, and stores that as **verbal memory** for the next attempt (short bullet, not full chat replay).

Sketch:

```text
Trial 1: failed — tests failed on edge case X.
Reflection: I assumed empty string was invalid; spec allows it. Next trial: align with OpenAPI nullable fields.
Trial 2: apply Reflection; succeed.
```

**Injecting memory:** prepend a compact `REFLECTIONS:` block on retry (last 3 bullets max). Full transcript replay on every retry duplicates noise and burns context.

Use Reflexion when **search space is large** and failures are **informative** (coding, multi-step tools). It is weaker when failures are random (network flakes) unless you add **deterministic retries** first.

---

## Study: neural-maze/agentic_patterns implementations

The community repo **neural-maze/agentic_patterns** collects minimal reference implementations of common agentic loops. Study it to see **how little code** separates ReAct, reflection wrappers, and planner-executor splits. Compare their **prompt templates** and **state objects** to your Agent Factory harness; borrow structure, not dependencies you do not need.

Exercise while reading: for each demo, list (1) **what state is carried** between steps, (2) **where the loop stops**, and (3) **what would break** if you swapped models (tool schema adherence).

---

## Exercises

1. **Reflection loop for a writing agent**  
   Implement a three-phase prompt or harness: (a) draft blog outline, (b) critique against audience and factual-risk checklist, (c) revised outline. Log critique tokens vs final quality.

2. **ReAct vs Reflexion**  
   Pick one task (e.g., “fix a failing unit test from the error log”). Run a **ReAct-only** variant (thought/action/observation until pass or step cap) and a **Reflexion** variant (on failure, append reflection, retry with cap 2). Compare steps, cost, and success rate.

---

## Further reading

- [Andrew Ng agentic patterns (wiki)](../../wiki/research/andrew-ng-patterns.md)
- [Feedback loops (wiki)](../../wiki/concepts/feedback-loops.md)
