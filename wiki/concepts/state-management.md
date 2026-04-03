# State Management

## What it is

**State** is everything required to resume, audit, or branch an agent run: conversation messages, plan version, tool results, user metadata, feature flags, and control flags (e.g., `awaiting_human`). **Checkpointing** persists snapshots to durable storage; **persistence** spans process restarts; **conversation threading** ties runs to user or session ids. **State machines** make transitions explicit (e.g., `triage → gather_info → propose_action → await_approval → execute`).

**LangGraph** models state as a typed dictionary (or reducer-backed channels) flowing through nodes; checkpoints enable time travel and human interrupt/resume.

## Why it matters for agents

Implicit state in globals or opaque model hidden chains causes **non-reproducible** bugs and blocks compliance (“show me the decision at step 4”). Clear state enables **idempotent** retries, **human review** at known points, and **horizontal scaling** (workers claim jobs with serialized state blobs).

## How to implement it

1. **Single source of truth:** a serializable `RunState` object; messages are a projection, not the only store.
2. **Checkpointing:** after each tool completion or major decision; include schema version for migrations.
3. **Context vs durable state:** large tool payloads live in object storage; the in-context view holds handles and summaries.
4. **Threading:** stable `thread_id`; branch for “what-if” replays without mutating production thread.
5. **State machines:** encode illegal transitions as impossible in code, not “please don’t” in prompts.
6. **LangGraph-style:** define reducers for append-only lists, last-writer wins for scalars; use `interrupt_before` on sensitive nodes for HITL.

**Context window management** intersects here: state outside the window must be reloadable via checkpoints and summaries, not assumed “still in history.”

## Serialization and migrations

Use a **schema version** field on every checkpoint. Migrations should be **forward-only** with explicit upgrade functions; never assume old processes can read new fields without defaults. For sensitive fields, encrypt at rest and keep keys outside serialized blobs attached to the run record. When using LangGraph or similar, document **which channels are reducers** versus last-value to avoid surprise list resets on resume.

## Concurrency

If multiple workers can touch one `thread_id`, you need **optimistic locking** (version counters) or a single-writer queue. Race conditions often appear as duplicate tool execution or lost human approvals—reproduce with concurrent integration tests.

## Debugging playbooks

When a run “looks stuck,” dump: current **state machine phase**, last **checkpoint hash**, pending **HITL** flags, and **tool attempt counts**. Compare to golden traces for the same phase. Restore from checkpoint **minus one** step only when idempotency allows; otherwise replay forward with patched policy.

## Common mistakes

- **Invisible state:** critical variables only in Python locals or UI memory.
- **Checkpoint without schema version:** cannot resume after deploy.
- **Giant checkpoints:** serializing full base64 blobs into the graph state every step.
- **Dual writers:** two subsystems updating `status` without a single reducer or lock.

## References to course modules

These map to the **23-module Agent Factory course** (see [`../../course/README.md`](../../course/README.md) when published).

- **Module 12 — State Management** — explicit state, reducers, and invariants.
- **Module 14 — Building with LangGraph** — graphs, interrupts, and checkpoint-friendly patterns.
- **Module 03 — The Agent Loop** — where message history meets durable run state.

Full curriculum index: [`../../course/README.md`](../../course/README.md) (when present).

Good state design pays off first in **support**: engineers can replay stuck runs without re-running expensive tools blindly.

## See also

- [Agent Loop](agent-loop.md)
- [Error Recovery](error-recovery.md)
- [Human-in-the-Loop](human-in-the-loop.md)
- [Context Window Management](context-window-management.md)
- [Agent Handoffs](agent-handoffs.md)
