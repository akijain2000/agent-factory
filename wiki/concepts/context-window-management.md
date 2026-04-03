# Context Window Management

## What it is

**Context window management** is the discipline of fitting the **right information** into a **finite token budget** each model call. Techniques include **token budgets** per section (system, memory, tools, user), **summarization** of old turns, **sliding windows** that keep recent messages verbatim, **priority-based truncation** (drop lowest-value chunks first), and **compaction** events that rewrite history into dense notes plus pointers to external artifacts.

## Why it matters for agents

Long runs accumulate noise; models attend poorly to middle sections; cost scales superlinearly with abuse. Without management, you get **context rot**: contradictory instructions, stale tool outputs, and failure to follow the latest user goal. Hard caps are also a **safety** lever (limit exfiltration payload size).

## How to implement it

1. **Budget table:** max tokens for system, retrieved docs, tool definitions, rolling transcript, and completion reserve; enforce before the API call.
2. **Summarization:** trigger when crossing threshold; summarize *decisions and open questions*, not verbatim fluff; store summary version in state.
3. **Sliding window:** keep last K user/assistant turns full fidelity; older → summary only.
4. **Priority truncation:** score segments by recency, source trust, and task relevance; drop low scores first; never drop system/developer policy blocks.
5. **Tool output hygiene:** persist large payloads externally; inject short handles + checksum into context.
6. **Re-fetch strategy:** when the model needs detail elided earlier, retrieve from checkpoint or tool, don’t assume it is still inline.

**Monitoring:** track tokens per segment and truncation events; alert on chronic over-truncation (signals wrong memory tier).

## Budget template

Example allocation for a 128k window (adjust per model): **system + policies** ≤ 8k, **tool defs** ≤ 12k, **retrieved docs** ≤ 24k, **rolling transcript** ≤ 48k, **reserved completion** ≥ 16k. Recompute when you add tools; oversized definitions are a frequent silent budget thief. Prefer **tool result eviction** to external store with stable URIs the model can re-fetch via a read tool.

## Summarization quality

Summaries should preserve **constraints**, **open questions**, **decided identifiers** (order ids, commit shas), and **failure context**. Avoid generic “the user asked about X” without parameters. Where possible, use **extractive-first** summarization for IDs and amounts, then light abstractive phrasing for narrative.

## Tool-definition pressure

When budgets tighten, shorten **example payloads** in tool descriptions before dropping safety instructions. Consider **dynamic tool loading**: expose only the subset relevant to the current phase to reclaim thousands of tokens per turn.

## Common mistakes

- **Context stuffing every turn:** sending full corpora “just in case.”
- **Naive middle truncation** that removes the user’s actual constraint.
- **Summaries that hallucinate commitments** the user never made.
- **Unbounded tool result injection** after a single “verbose” call.

## References to course modules

These map to the **23-module Agent Factory course** (see [`../../course/README.md`](../../course/README.md) when published).

- **Module 22 — Context Engineering & Compaction** — practical budget patterns.
- **Module 07 — Memory Tiers & Retention** — what should leave the window entirely.
- **Module 02 — Tokens, Models, and Cost** — measurement fundamentals.

Full curriculum index: [`../../course/README.md`](../../course/README.md) (when present).

Revisit budgets whenever you change **model family**—different encodings and tool formats move the effective ceiling without obvious UI warnings.

Log **pre-call token estimates** server-side; client-side math often drifts from provider billing.

## See also

- [Memory Systems](memory-systems.md)
- [Context Engineering](context-engineering.md)
- [Prompt Engineering for Agents](prompt-engineering-for-agents.md)
- [State Management](state-management.md)
- [Cost Optimization](cost-optimization.md)
