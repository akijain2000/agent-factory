# phidata-Style Knowledge Agent: RAG, Memory, and Tools

## Summary

This example follows the phidata pattern: an assistant **retrieves** from a knowledge base, **maintains** structured session or long-term memory, and **calls tools** for live data or side effects. Retrieval is not “paste everything”; it is a pipeline with chunking, ranking, and citation-friendly snippets fed into the model alongside a concise working memory.

## Pattern

**Knowledge-augmented loop with clean memory boundaries.** Short-term state holds the active task, recent tool results, and user preferences for this session. Long-term store holds embeddings or summaries with pointers back to sources. Tools are orthogonal to retrieval (e.g., calendar vs SQL vs HTTP), each with explicit schemas.

## What makes it good

Separating **retrieval** from **reasoning** reduces hallucination pressure: the model sees labeled context (“from KB: …”) versus free speculation. Structured memory avoids dumping full chat logs every turn; summarization and compaction policies keep the window useful. Tool integration stays predictable because arguments are validated before execution.

The design maps cleanly to evaluation: you can score retrieval hit rate, citation accuracy, and tool correctness independently.

### In practice

Use chunk metadata (document ID, section, last updated) in every retrieved span. Refresh or invalidate embeddings when sources change. Cap retrieved tokens per turn and escalate to a “refine query” sub-step when recall@k is empty twice in a row.

### Failure modes this design mitigates

Dumping chat history causes **lost-in-the-middle** and stale instructions surfacing from old turns. Structured memory with summarization policies keeps the model anchored on current goals. Ungrounded answers become easier to detect when citations are mandatory in the output schema.

### When to reconsider

If knowledge is tiny (a few pages), a single well-curated system prompt may beat RAG complexity. Grow retrieval when content exceeds what you can responsibly fit and maintain in prompt form.

## Key takeaway

**Treat memory and retrieval as first-class subsystems** with contracts, not as ad hoc strings appended to the latest user message.

## Review checklist

- [ ] Is the active tool set small enough to name from memory?
- [ ] Are transitions or handoffs explicit in code, not only in prose?
- [ ] Do traces identify phase, tool, and outcome for each step?
- [ ] Are step, cost, and time limits enforced in the host, not the model?
- [ ] Can you replay a failed run with mocks for tools and LLM?
- [ ] Are high-risk actions behind sandbox, schema validation, or human approval?

## Metrics and evaluation

Define SLIs for the loop: success rate per task type, median steps to completion, tool-error ratio, and cost per successful outcome. Store traces with default PII redaction and retain enough detail to replay decisions. Run periodic canaries on pinned prompts and tool versions to catch provider or dependency drift before users do.

## Contrast with common failures

For unstructured alternatives and their failure modes, see [God agent](../bad/god-agent.md), [Over-tooled agent](../bad/over-tooled-agent.md), and the wiki [Anti-patterns](../../research/anti-patterns.md) catalog.

## See also

- [Memory systems](../../concepts/memory-systems.md)
- [Agent memory patterns](../../concepts/agent-memory-patterns.md)
- [Context engineering](../../concepts/context-engineering.md)
- [Context memory architecture](../../research/context-memory-architecture.md)
- [Structured outputs](../../concepts/structured-outputs.md)
