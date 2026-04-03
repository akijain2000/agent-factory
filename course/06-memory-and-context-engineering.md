# Module 06: Memory and Context Engineering

**Duration:** approximately 45 minutes  
**Prerequisites:** Module 03 (The Agent Loop); Module 05 (Tool Design) optional for retrieval-tool patterns.

---

## Learning objectives

By the end of this module, you should be able to:

- **Choose** appropriate memory mechanisms (short-term, long-term, episodic, semantic) for a given agent task.
- **Apply** context engineering principles to curate what enters the model’s effective “information environment.”
- **Recognize** context rot patterns and mitigate them in prompts, retrieval, and harness design.
- **Explain** ByteRover-style context tree ideas and why structured context can improve long-horizon recall benchmarks such as LoCoMo.

---

## 1. Memory types

**Short-term (context window)**  
Everything currently in the chat transcript, system prompt, tool outputs, and injected state. Scarce, high-bandwidth, and volatile. This is where **attention** is spent directly.

**Long-term (vector stores, databases)**  
Embeddings plus metadata, or classical DB rows. Survives sessions but requires **retrieval** to become useful in the loop. Tune chunking, overlap, and filters aggressively.

**Episodic memory**  
Time-ordered traces: what the agent did, what worked, what failed. Useful for personalization and debugging; risky if raw logs pollute retrieval (“we tried X three times and failed”).

**Semantic memory**  
Stable facts, policies, and domain knowledge—often curated docs or knowledge graphs. Prefer **authoritative** sources over stale chat summaries.

No single store wins. Production agents usually combine a **small hot context** with **on-demand retrieval** from colder stores.

---

## 2. RAG for agents: retrieval in the loop

Retrieval-augmented generation in agents differs from one-shot RAG:

- The **query evolves** each turn; re-embed or re-rank as subgoals change.
- **Tool outputs** become new evidence; deduplicate against prior chunks before stuffing the window.
- **Citations** matter: store `source_id`, `uri`, and `retrieved_at` so the model can ground claims.

Example retrieval tool result shape:

```json
{
  "chunks": [
    {
      "text": "...",
      "source": "runbook/deploy.md",
      "score": 0.82,
      "chunk_id": "deploy.md#l120-140"
    }
  ],
  "query_used": "rollback kubernetes deployment staging"
}
```

---

## 3. Context engineering (Lutke / Karpathy framing)

**Context engineering** is the discipline of **designing what the model sees**: not just the prompt string, but files, tool results, memories, UI state, and instructions ordering. Karpathy-style emphasis: the context window is **precious compute**; treat it like RAM.

Practical tactics:

- **Lead with invariants** (goals, constraints) before long evidence.
- **Summarize** older turns when the task is long; keep **decision-relevant** detail.
- **Separate** “facts” from “hypotheses” so the model does not merge them.
- **Inject** only the **minimal** codebase slices (relevant paths, signatures) for coding agents.

---

## 4. Context rot patterns (Willison)

**Poisoning**  
Bad retrieved chunks or erroneous tool output repeated across turns becomes “truth.” Mitigate with validation tools, confidence gating, and human review for high-stakes facts.

**Distraction**  
Irrelevant retrieved text crowds out the actual task. Mitigate with **hard caps** on retrieved tokens, MMR-style diversity, and query reformulation.

**Confusion**  
Contradictory sources without ranking or dates. Mitigate with explicit **source metadata** and instructions to reconcile or escalate conflicts.

**Clash**  
System prompt says X, retrieved docs say Y. Mitigate with **precedence rules** (“policy in system prompt overrides docs unless version > 2025-01”).

---

## 5. Study: ByteRover’s context tree architecture (LoCoMo)

ByteRover (and similar research-informed products) organize context as a **tree**: hierarchical nodes for project, task, file, and subgoal, often with **summaries at higher levels** and **detail on demand** at leaves. Reported results on **LoCoMo**-style long-context benchmarks (e.g., high accuracy when locating prior facts across long dialogs) support the idea that **structure beats raw transcript stuffing**.

Takeaways for your own agents:

- Maintain a **working tree** or outline of the current objective.
- **Promote** stable facts upward; **demote** verbose tool logs after use.
- **Address** nodes by id so the model can request “expand subtree B” instead of rereading everything.

---

## 6. Practical: building a memory layer

A minimal memory layer often includes:

1. **Session buffer** — last N messages or token-budgeted transcript.  
2. **Scratchpad** — structured JSON the harness updates (`current_plan`, `open_questions`).  
3. **Vector index** — chunked docs with metadata filters.  
4. **Write policy** — when the agent may persist memory (user opt-in, PII scrubbing).

```text
[system] + [scratchpad JSON] + [retrieved chunks with citations] + [trimmed history] + [user message]
```

Instrument **token counts** per segment so you know what to trim when the budget tightens.

---

## Exercises

1. **Design a memory strategy** for a coding assistant agent: what stays in the sliding window, what goes to a repo-wide index, what is never stored, and how you handle secrets in files. Include one diagram (ASCII is fine) of data flow from user message to model context.

2. **Identify context rot** in a given agent transcript (use a sample from your own logs or a fictional multi-turn debugging session). Label each problematic span as poisoning, distraction, confusion, or clash, and propose a concrete fix (prompt rule, retrieval change, or harness change).

---

## Further reading

- [Memory systems](../../wiki/concepts/memory-systems.md)
- [Context engineering](../../wiki/concepts/context-engineering.md)
- [Context and memory architecture](../../wiki/research/context-memory-architecture.md)

---

## Summary

Memory is not “add a vector DB.” It is **policy plus structure**: what to remember, how to retrieve it, and how to keep the context window **coherent**. RAG inside agent loops needs **fresh queries** and **deduplication**. Context rot is predictable; counter it with metadata, caps, and explicit precedence. Hierarchical context trees are a practical pattern for long-horizon work.
