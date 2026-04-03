# Memory Systems

## What it is

**Memory** for agents is any store that influences future decisions beyond the current forward pass. Common categories:

- **Short-term / working:** messages and scratchpad inside the **context window** (volatile, highest fidelity, smallest capacity).
- **Long-term:** durable stores—relational DBs, object storage, **vector stores**—persisting across sessions and deployments.
- **Episodic:** time-ordered records of what happened in sessions (transcripts, decisions, tool outcomes); supports personalization and audit.
- **Semantic:** generalized facts and relations—often **knowledge graphs**, curated tables, or embedded corpora—less tied to a single timeline.

A **memory tier architecture** assigns each fact a lifetime and loading policy: what is always in prompt, what is retrieved on demand, what is never stored.

## Why it matters for agents

The context window is finite; naive “keep everything” causes **context rot** and cost blowups. Wrong tier choice leaks PII, stale instructions, or contradictory “truths.” Explicit tiers make retention, GDPR erasure, and debugging feasible.

## How to implement it

1. **Classify data** at write time: session-only vs user-profile vs org-knowledge vs audit log.
2. **Short-term:** system + developer instructions, recent turns, compact tool summaries; refresh each loop iteration.
3. **Long-term retrieval:** chunk, embed, and retrieve top-k with citations; inject retrieved blocks in a delimited, untrusted block to reduce injection risk.
4. **Episodic:** store structured events `{ts, actor, action, outcome}`; summarize old threads into rolling digests kept in long-term store.
5. **Semantic graph:** use when answers require multi-hop relations (“which dependencies touch PII?”); pair with retrieval for narrative evidence.
6. **Policies:** TTLs, redaction before write, and “right to be forgotten” hooks documented per tier.

**When to use each:** working memory for reasoning *this* turn; episodic for continuity and support; semantic/graph for stable domain truth; vectors for similarity-heavy lookup; raw transcripts only when compliance demands—and then protected.

## Loading policy (per turn)

Define a function `load_memory(tenant, user, task)` that returns ordered segments: **pinned** policy snippets, **session summary**, **retrieved facts** with citations, and **scratch** space budget. Cap each segment; if retrieval overfills, rerank rather than truncate arbitrarily. Log which **tier** satisfied each query to tune indexes and chunk sizes over time.

## Consistency and updates

When semantic memory changes (pricing, policy), version documents and prefer **time-bounded facts** in structured stores (“effective_until”). Episodic logs should store **immutable events**; corrections append new events rather than silently rewriting history unless privacy erasure compels deletion. For **multi-region** deployments, clarify which tier is source of truth to avoid split-brain retrieval.

## Common mistakes

- **Memory hoarding:** infinite transcript retention without legal/product basis.
- **Single blob memory:** dumping all tiers into one vector index with no metadata filters.
- **Trusting retrieved text as instructions** (prompt injection via documents).
- **No migration plan** when embeddings or schema change.

## References to course modules

These map to the **23-module Agent Factory course** (see [`../../course/README.md`](../../course/README.md) when published).

- **Module 07 — Memory Tiers & Retention** — designing lifetime and access paths.
- **Module 08 — RAG, Vector Stores, and Chunking** — retrieval layer mechanics.
- **Module 09 — Knowledge Graphs & Structured Facts** — when graphs beat chunks.

Full curriculum index: [`../../course/README.md`](../../course/README.md) (when present).

## See also

- [Context Window Management](context-window-management.md)
- [Context Engineering](context-engineering.md)
- [Agent Memory Patterns](agent-memory-patterns.md)
- [Guardrails](guardrails.md)
- [State Management](state-management.md)
