# Feedback Loops

## What it is

**Feedback loops** let agents improve outputs through iteration using **reflection** (critique own draft), **self-evaluation** (checklist or rubric), **Reflexion**-style verbal reinforcement learning (store mistakes as textual lessons for retries), **critic agents** (separate model or policy that scores or repairs), and **human feedback** (ratings, edits, approvals). Loops can run **inside** a single request or **across** sessions via memory and datasets.

## Why it matters for agents

Single-pass generation plateaus on complex tasks. Controlled feedback reduces **hallucination**, aligns tone and policy, and supports **continuous improvement** when traces feed offline training or prompt updates. Without structure, “try again” loops burn budget and amplify drift.

## How to implement it

1. **Define stop criteria:** max revisions, quality threshold, or validator pass (schema, tests, linter).
2. **Reflection prompt:** ask for concrete defects referencing evidence (quotes, tool outputs), not vague self-praise.
3. **Critic separation:** use a different system prompt or model temperature; avoid identical prompts that rubber-stamp the first draft.
4. **Reflexion memory:** append short **lessons** to session memory after failures (`"When API returns 429, backoff and reduce page size"`); cap list length and deduplicate.
5. **Human in the loop:** route low-confidence or high-impact steps to review; capture structured accept/reject reasons for eval datasets.
6. **Cost control:** cheaper model for critique when task allows; skip reflection for trivial intents via a router.

## Safety note

Feedback loops can **overfit** to the critic’s quirks or leak sensitive content into persistent “lessons.” Redact before write; validate lessons with the same policy filters as user-visible output.

## Reflexion pattern details

After a failed attempt, append a concise **verbal critique** to the next context: what went wrong, which assumption was false, what to try instead. Keep critiques **actionable** and **short** to limit context growth. Prune or summarize old critiques when they reference stale tool behavior.

## Critic agents: architecture options

Run the critic **sequentially** (draft then review) or **in parallel** for speed when tasks decompose cleanly. Use **structured** critic outputs (scores per rubric item) when you need analytics. Ensure the critic sees the same **evidence** the author saw—omitting tool outputs produces false confidence.

## Integrating human feedback

Convert approvals and edits into **labeled spans** for training and eval updates. Close the loop weekly: sample production failures, tag root causes, feed prompt or policy changes, re-run golden traces.

## Common mistakes

- Unlimited self-revision loops without progress detection (oscillation).
- Critics that only paraphrase the draft without independent checks.
- Storing raw user data in global lesson banks without tenancy controls.
- No metrics: cannot tell if reflection improved win rate or just latency.

## Quick checklist

- Max revisions and stop conditions are **configuration**, not ad hoc.
- Persistent lessons pass the same **redaction** pipeline as user output.
- Critics use **independent** prompts or models where budget allows.

## References to course modules

These map to the **23-module Agent Factory course** (see [`../../course/README.md`](../../course/README.md) when published).

- **Module 13 — Reflection, Critics, and Self-Correction** — loop design patterns.
- **Module 14 — Behavioral Test Suites & Golden Traces** — measuring loop quality.
- **Module 23 — Human Feedback & Active Learning** — closing the outer loop.

Full curriculum index: [`../../course/README.md`](../../course/README.md) (when present).

## See also

- [Agent Evaluation](agent-evaluation.md)
- [Planning Strategies](planning-strategies.md)
- [Human-in-the-Loop](human-in-the-loop.md)
- [Agent Memory Patterns](agent-memory-patterns.md)
- [Cost Optimization](cost-optimization.md)
