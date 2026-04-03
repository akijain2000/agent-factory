# Module 12: State Management

**Duration:** approximately 35 minutes  
**Prerequisites:** Module 03 (The Agent Loop); Module 06 (Memory and Context) recommended.

---

## Learning objectives

By the end of this module, you should be able to:

- **Implement** checkpointing and persistence so agents can **resume** after crashes or human pause.
- **Manage** long-running conversations with **branching**, **summarization**, and **windowing** strategies.
- **Model** control flow with **explicit state machines** where loops, retries, and approvals matter.

---

## Why state matters: long-running agents, crash recovery, audit trails

Agents are **stateful processes**: tool results, plans, user approvals, and partial artifacts live across turns. Without durable state, you lose **progress** on failure and cannot **reconstruct** decisions for compliance or debugging.

Treat **state** as a first-class artifact: versioned, serializable, and **separable** from the raw chat log (which is noisy and large).

**Audit:** store **immutable event logs** (append-only) even if the model context is summarized; regulators and incident reviews ask for timelines, not “whatever fit in the window.”

---

## Checkpointing: saving and restoring agent state

**Checkpointing** writes a **snapshot** at boundaries: after each tool burst, after plan approval, or on a timer. A snapshot typically includes:

- `thread_id`, `turn_index`, `goal` (or task id)  
- **Structured** plan / todo list  
- **Last N** messages or a **summary + pointers** to blobs  
- **Tool results** needed for the next step (or references to object storage)

```python
# Conceptual schema (language-agnostic)
checkpoint = {
    "thread_id": "abc",
    "phase": "executing",
    "plan": [...],
    "pending_tool": {"name": "run_tests", "args": {...}},
    "artifacts": {"diff_uri": "s3://..."},
}
persist.save(checkpoint)
```

On restart, **load** checkpoint, validate **schema version**, and resume from `pending_tool` or next plan step. **Idempotent** tools make retries safer.

**Schema migration:** bump `checkpoint_version` when fields move; write a small migrator so old runs do not brick after deploy. **Stale detection:** if code version or tool manifest changed, mark checkpoint **needs_human_review** before resuming destructive steps.

---

## Conversation threading: managing multiple conversation branches

**Threading** supports **forks** (user tries two approaches), **subtasks** (child threads with scoped context), and **merge-back** (child returns a summary + structured result). Avoid copying **full parent history** into every child; pass a **brief** brief and **links** to artifacts.

Patterns:

- **Parent thread** owns global goal; **child threads** own hypotheses or spikes.  
- **Rejoin** with `RESULT_SUMMARY` + machine-readable payload for the parent planner.

**Concurrency:** if parent and child both write the same artifact store, use **locking** or **branch namespaces** (`thread/child-uuid/`) to avoid last-writer-wins surprises.

---

## State machines for agent control flow

A **finite state machine (FSM)** makes phases explicit: `INTAKE → PLAN → AWAIT_APPROVAL → EXECUTE → VERIFY → DONE` (with `FAILED` and `ESCALATE` transitions). The harness—not vague prompting—owns **legal transitions**.

Example transitions:

```text
PLAN --[plan_rejected]--> INTAKE
PLAN --[plan_approved]--> EXECUTE
EXECUTE --[tool_error_retryable]--> EXECUTE  (with backoff + cap)
EXECUTE --[tool_error_fatal]--> ESCALATE
VERIFY --[tests_fail]--> EXECUTE
VERIFY --[tests_pass]--> DONE
```

Benefits:

- **Retries** and **human gates** are first-class, not emergent behavior.  
- Logs show **current state**, simplifying on-call.  
- You can **disable** auto-progression per environment (staging vs prod).

Implement the FSM in code with a `transition(event)` function; keep the diagram in the repo next to the agent spec so they do not drift.

---

## Context window management: summarization, sliding windows, priority truncation

Long runs exceed **context limits**; quality **degrades** before hard errors. Strategies:

- **Summarization:** periodic “state digest” with **pinned facts** (versions, file paths, failing test names).  
- **Sliding window:** keep last K turns verbatim + rolling summary of older turns.  
- **Priority truncation:** drop low-value turns first (boilerplate), never drop **tool errors** without archiving elsewhere.

```text
[SYSTEM] Pinned: repo=agent-factory, branch=feat/state, failing_test=TestCheckpoint::resume
[SUMMARY] Turns 1–20: User asked for checkpointing; we added schema v1...
[RECENT] Turns 21–24: full verbatim...
```

Align with product needs: **compliance** may require **full logs** in external storage even if the model sees a summary.

**Trigger summarization** on token budget (e.g., 70% of model window) rather than only on turn count—attachments and tool outputs vary wildly.

---

## Study: LangGraph checkpointing, Ralph’s git-as-memory

**LangGraph** popularized **graph-native** checkpointing: each node transition can persist **channel state** so you can **time-travel** or resume. Study how **reducers** merge updates and how **interrupts** support human approval.

**Ralph** (and similar workflows) use **git as memory**: commits represent **durable milestones** (PRDs, task lists, code). The agent **reads** repo state as truth. Lessons: **human-readable** checkpoints, **diffable** progress, and **branching** that matches dev workflows.

---

## Exercises

1. **Add checkpointing**  
   Pick a simple agent loop (pseudo-code is fine). Define `save_checkpoint()` triggers, the **minimal fields** required to resume mid-task, and how you **detect stale** checkpoints after code deploys.

2. **Context strategy**  
   For a 50-turn support thread with occasional file attachments, design a **windowing policy**: what gets summarized every N turns, what stays verbatim, and where **attachments** live (inline vs storage pointer).

---

## Further reading

- [State management (wiki)](../../wiki/concepts/state-management.md)
- [Context window management (wiki)](../../wiki/concepts/context-window-management.md)
