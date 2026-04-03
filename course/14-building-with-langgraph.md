# Module 14: Building with LangGraph

**Duration:** approximately 45 minutes  
**Prerequisites:** Module 03 (The Agent Loop); Module 12 (State Management); Module 13 (Framework Selection) recommended.

---

## Learning objectives

By the end of this module, you should be able to:

- **Model** agents as **directed state graphs** with explicit nodes and edges rather than implicit prompt chains.
- **Implement** **persistence** and **checkpointing** so runs survive restarts and support replay.
- **Add** **human-in-the-loop** gates using interrupts and resume semantics.
- **Stream** partial outputs from graph nodes for responsive UIs and observability.

---

## LangGraph mental model: agents as graphs, not chains

A **chain** runs steps in a fixed order; an **agent loop** is inherently **cyclic** (think, act, observe, repeat). LangGraph expresses that cycle as a **graph**: **nodes** do work (call a model, run a tool, summarize), **edges** choose the next step based on **state**.

Benefits:

- **Cycles** are first-class—no hacks to “loop until done.”
- **Branching** (e.g., escalate vs continue) is explicit.
- **Checkpointing** attaches to graph execution, not ad-hoc JSON blobs.

Mental model: **state** flows through the graph; each node reads state, returns **updates**, and the reducer merges updates into the next snapshot.

---

## State schemas and typed state

Define **typed state** (e.g., Pydantic or TypedDict) so every node agrees on fields: `messages`, `plan`, `tool_outputs`, `human_approval`, etc.

```python
# Conceptual TypedDict-style state (illustrative)
from typing import TypedDict, Annotated, List
import operator

class ResearchState(TypedDict):
    messages: Annotated[list, operator.add]
    query: str
    sources: list
    draft: str
    needs_human: bool
```

Use **reducers** (like `operator.add` for message lists) when multiple nodes append to the same key. **Single-assignment** keys suit “current phase” or “last error.”

**Discipline:** avoid dumping unstructured strings into one mega-field; you will lose the ability to **assert** invariants in tests.

---

## Nodes and edges: building the agent graph

A **node** is a callable: `(state) -> partial_state_update`. An **edge** connects nodes; **conditional edges** branch on a routing function that inspects state.

Typical research agent nodes:

1. **plan** — model proposes steps or search queries.
2. **search** — tool calls to retrievers or web APIs.
3. **synthesize** — model writes draft from `sources`.
4. **verify** — optional second pass or checklist.

```python
# Pseudocode structure (API names vary by version)
# graph.add_node("plan", plan_node)
# graph.add_node("search", search_node)
# graph.add_node("synthesize", synthesize_node)
# graph.set_entry_point("plan")
# graph.add_conditional_edges("plan", route_after_plan, {...})
# graph.add_edge("search", "synthesize")
```

**Routing functions** should be **pure** where possible: given state, return the next node name. Keep **side effects** inside nodes, not inside routers.

---

## Persistence and checkpointing

LangGraph integrates with **checkpointers** (memory, SQLite, Postgres, etc.) keyed by `thread_id`. Each **superstep** (or configurable boundary) persists state so you can:

- **Resume** after process crash.
- **Fork** threads for A/B prompts.
- **Audit** what the graph knew at step *k*.

**Production tips:**

- Use a **durable** checkpointer for anything customer-facing.
- Include **schema version** in metadata when state shape evolves.
- **Expire** or **archive** old threads per retention policy (GDPR, etc.).

---

## Human-in-the-loop: interrupt and approve

**Interrupt** before destructive or irreversible nodes: e.g., before `send_email` or `merge_pr`. The runtime pauses, persists state, and surfaces a **payload** to a human UI. After approval, **resume** with the same `thread_id`.

Pattern:

1. Node sets `needs_human=True` and writes a **proposal** (diff, recipient list, SQL).
2. Graph **interrupts**; external system shows proposal.
3. Human **approves** or **rejects**; resume with `human_decision` in state.
4. Next routing sends flow to **execute** or **revise**.

**Do not** rely on the model to “promise” it will wait—**the graph** must not enter the tool node until approval is recorded in state.

---

## Streaming: real-time output from graph nodes

Streaming APIs emit **tokens** or **node events** as the graph runs. Use this for:

- **UX:** progressive disclosure in chat UIs.
- **Debug:** see which node is active when latency spikes.

Subscribe to stream modes that include **node boundaries** so you can attribute output to `plan` vs `search` vs `synthesize`. Log **correlation IDs** (`thread_id`, `run_id`) on every chunk for trace stitching.

---

## Walkthrough: building a research agent with LangGraph

**Goal:** User query in → planned searches → retrieved snippets → cited draft out, with optional **human** review before returning externally.

1. **State:** `query`, `search_plan`, `raw_hits`, `draft`, `citations`, `review_status`.
2. **Nodes:** `plan_searches`, `run_search_tools`, `write_draft`, `format_answer`.
3. **Conditional edge** after `write_draft`: if `risky_claims` heuristic fires, route to `human_review`; else `END`.
4. **Checkpointer:** Postgres with `thread_id` per user session.
5. **Streaming:** UI shows `plan_searches` reasoning tokens, then tool progress, then draft sections.

**Test:** replay a fixed `thread_id` after injecting a tool error; assert the graph retries or escalates per your policy.

---

## Exercises

### Exercise 1: Build a three-node agent graph

Implement (on paper or in code) a minimal graph: `ingest` → `classify` → `respond`. `classify` sets an intent enum; `respond` uses different system prompts per intent. Draw the graph and list **exact** state fields each node reads and writes.

### Exercise 2: Add checkpointing and human approval to an existing agent

Take an agent you have today (or the Module 03 loop). Identify **one** high-risk tool call. Specify: (a) where the interrupt fires, (b) what data the human sees, (c) how resume updates state, (d) how you test the paused and resumed paths.

---

## Further reading

- [Framework comparison (wiki)](../wiki/research/framework-comparison.md) — how LangGraph compares to other orchestration options.
- [LangGraph documentation](https://langchain-ai.github.io/langgraph/) — official tutorials on state, persistence, interrupts, and streaming (URLs and APIs evolve; verify against current docs).
