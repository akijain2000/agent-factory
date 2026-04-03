# Agent Memory Patterns

## What it is

**Agent memory patterns** are reusable ways to persist and retrieve information across turns or sessions. Common patterns include the **scratchpad** (writable working notes inside the loop), **conversation buffer** (raw or windowed chat history), **summary memory** (rolling digests of older turns), **knowledge base** (curated documents or records), and **RAG** (retrieval-augmented generation over embedded corpora). These map to different **latency, fidelity, and compliance** tradeoffs (see also [Memory Systems](memory-systems.md) for tiered architecture).

## Why it matters for agents

Memory is how agents maintain **continuity** and **grounding** without refitting the whole world into every prompt. The wrong pattern causes **stale facts**, **context rot**, **PII leakage**, or **unbounded cost**. Explicit patterns make retention policies and evaluations feasible: you know what should be remembered for the next turn versus what must never be stored.

## How to implement it

1. **Scratchpad:** short structured notes the model updates each loop iteration; cap size; clear on task completion; do not treat as authoritative for external systems until validated.
2. **Conversation buffer:** keep recent verbatim turns for nuance; trim with a fixed window or token budget; pair with summaries for older segments.
3. **Summary memory:** async or end-of-session summarization with structured fields (`goals`, `decisions`, `open_questions`); store versioned summaries, not silent overwrites.
4. **Knowledge base:** human- or ETL-maintained facts with effective dates; prefer structured rows for deterministic fields; attach citations when injected into prompts.
5. **RAG:** chunk, embed, retrieve; filter by tenant and sensitivity; wrap retrieved text in delimiters and label as untrusted evidence; log retrieval ids for debugging.

## When to use which

Use **scratchpad** for intermediate reasoning and tool chaining. Use **buffer** when exact phrasing matters (negotiation, support). Use **summary** for long sessions where old detail matters but not verbatim. Use **knowledge base** for stable org truth. Use **RAG** for large, evolving corpora where similarity search is the right access path.

## Operational hooks

Tag memory writes with **classification** (PII, user preference, system fact), **TTL**, and **source**. Enforce **right to erasure** at the write path, not as a batch job only.

## Combining patterns in one agent

Typical production stacks pair a **trimmed buffer** (last N turns) with a **rolling summary** of older content, a **scratchpad** for the current task, and **RAG** for org docs. Order injection carefully: policy and safety first, then summary, then retrieval, then scratchpad, then the latest user message.

## Evaluation per pattern

Test whether summaries **preserve** critical constraints (legal language, numeric thresholds). Test whether RAG retrieves **correct** tenant data under adversarially similar filenames. Test scratchpad clearing so secrets do not leak into unrelated follow-up tasks.

## Capacity planning

Summaries and embeddings add **async** jobs; plan queues and backoff. Vector indexes need **reindex** strategies when models or chunking change. Memory is not free—budget storage and query cost like any other dependency.

## Common mistakes

- Dumping retrieved chunks into the system role as if they were instructions (injection risk).
- One giant vector store without metadata filters across tenants.
- Summaries that drop safety constraints or legal disclaimers present in raw history.
- Infinite scratchpad growth across sessions without summarization or archival.

## References to course modules

These map to the **23-module Agent Factory course** (see [`../../course/README.md`](../../course/README.md) when published).

- **Module 07 — Memory Tiers & Retention** — lifecycle and policy.
- **Module 08 — RAG, Vector Stores, and Chunking** — retrieval pattern details.
- **Module 09 — Knowledge Graphs & Structured Facts** — when tables or graphs beat vectors.

Full curriculum index: [`../../course/README.md`](../../course/README.md) (when present).

## See also

- [Memory Systems](memory-systems.md)
- [Context Window Management](context-window-management.md)
- [Context Engineering](context-engineering.md)
- [State Management](state-management.md)
- [Feedback Loops](feedback-loops.md)
