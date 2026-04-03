# Context Engineering

## What it is

**Context engineering** (articulated in discussions by leaders such as **Tobi Lütke** and **Andrej Karpathy**) treats the **information environment** the model sees as the primary design surface—not a single static prompt. It is the shift from **prompt engineering** (wording tricks) to **information architecture**: what enters the window, in what order, with what provenance, and when it is **removed** or **summarized**. **Simon Willison** and others catalog **context rot** patterns: **poisoning** (malicious or misleading injected text), **distraction** (irrelevant bulk), **confusion** (contradictory sources), and **clash** (system vs tool vs user priorities fighting).

## Why it matters for agents

Agents run for many turns. Each iteration **re-embeds** history, tool outputs, and retrieved documents. Poor curation yields **garbled** tool arguments, **policy** drift visible to the model, and silent **priority inversion** (user email overriding system safety). The window is finite; **rot** is inevitable without explicit **compaction** and **trust labeling**.

**Context engineering** pairs naturally with **evaluations**: measure not only final answers but **intermediate** state quality after compaction events.

## How to implement it

1. **Source tagging:** label blocks as `system`, `developer`, `user`, `tool`, `retrieved` with timestamps and **ACL** hints. The model should know what is **canonical** vs **untrusted**.
2. **Compaction policy:** after N turns or M tokens, **summarize** with a structured template; keep **invariants** (safety rules, schema) immune to summarization or re-inject them verbatim.
3. **Retrieval hygiene:** cap chunk count; deduplicate; prefer **snippets** over full pages; re-check **permissions** on every query.
4. **Anti-poisoning:** never place untrusted web or email content adjacent to secrets; use **sandwich** structures where immutable policy wraps data sections.
5. **Distraction control:** move reference docs out of the permanent prefix into **on-demand** tool fetches; avoid pasting logs wholesale—normalize errors to **typed** messages.
6. **Clash resolution:** when sources disagree, expose **conflict** explicitly or fetch authoritative data via tools instead of asking the model to reconcile rumors.

7. **Working set discipline:** for coding agents, prefer **file lists** and **symbol** summaries over whole-repo pastes; refresh when the branch changes.

**Measurement:** track **tokens per role**, **age** of facts in context, and **retraction** events (what was dropped and why).

## From prompts to architecture

Maintain a **context manifest** per run: intended sections, max sizes, and summarization checkpoints. Review manifests when adding tools or **memory** layers.

Willison’s **rot** vocabulary is a useful **postmortem** lens: classify incidents as poisoning, distraction, confusion, or clash to pick the right fix (filter, trim, reconcile, or re-fetch).

**Karpathy / Lütke** framing reminder: invest in **what is true in the window**—provenance, freshness, and conflict handling—before chasing marginal prompt tweaks.

Diff **manifests** across turns in debug tooling so engineers can see exactly what changed before a bad tool call.

## Common mistakes

- **Infinite** chat history without summarization or archival.
- Treating **retrieved** text as trusted without provenance.
- Letting **tool errors** dump stack traces into the window.
- Editing only the **system** string while ignoring **tool output** shape.
- **Compaction** that drops **authorization** constraints or **tool schemas**.
- Duplicating the same **policy** in three places without a single **source of truth**.

## References to course modules

These map to the **23-module Agent Factory course** (see [`../../course/README.md`](../../course/README.md) when published).

- **Module 06 — Memory and Context Engineering** — curating what the model sees and when to compact.
- **Module 04 — System Prompts for Agents** — aligning instructions with the assembled context.
- **Module 09 — Agent Design Patterns** — reusable shapes for context assembly and retrieval.

Full curriculum index: [`../../course/README.md`](../../course/README.md) (when present).

## See also

- [Context Window Management](context-window-management.md)
- [Prompt Engineering for Agents](prompt-engineering-for-agents.md)
- [Memory Systems](memory-systems.md)
- [Agent Memory Patterns](agent-memory-patterns.md)
- [Harness Engineering](harness-engineering.md)
