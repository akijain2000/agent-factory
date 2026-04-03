# Agent UX

## What it is

**Agent UX** is how users **perceive** and **control** agent-powered products: **streaming** partial outputs, **progress** indicators across long runs, **transparency** into what the agent is doing (without unsafe verbosity), **error messaging** that suggests recovery, and **human takeover** when automation stalls or policy requires approval. Good UX aligns **mental models** with actual behavior—users should know when the system is thinking, acting, waiting on tools, or blocked on them.

## Why it matters for agents

Latency and nondeterminism are intrinsic. Without deliberate UX, interfaces feel **frozen**, **opaque**, or **overconfident**. Trust erodes when errors read as generic failures or when users cannot **interrupt** or **correct** a run. Regulatory and enterprise buyers increasingly expect **explainability** and **escalation** paths, which are UX concerns as much as engineering ones.

Consistency across surfaces (web, mobile, Slack) matters: if one channel streams and another batches, users develop **mismatched** expectations and support load rises.

## How to implement it

1. **Streaming:** stream **tokens** where helpful; for tools, stream **status events** (“searching…”, “calling `refund`—pending approval”). Keep final structured payloads **validated** before committing side effects.
2. **Progress:** map loop iterations to **stages** (understand, plan, execute, verify). Show **determinate** bars only when you have real estimates; otherwise use **indeterminate** states with elapsed time.
3. **Transparency:** show **high-level** plans and tool names; redact **secrets** and **PII** in UI mirrors of traces. Offer “why” at the **intent** level, not raw chain-of-thought if policy forbids it.
4. **Errors:** classify failures (network, policy, user input, tool bug) and surface **next steps** (retry, edit input, contact support). Never blame the user for model drift.
5. **Human takeover:** explicit **pause**, **edit plan**, and **approve/reject** affordances for gated tools. Preserve **context** when handing off so humans do not start cold.
6. **Responsiveness:** optimistic UI for safe actions; **disable** destructive confirms until requirements met. Time out visibly rather than hanging.

7. **Empty and loading states:** show **what** the agent is waiting on (user input, approval, external API) so users do not duplicate sends.

**Accessibility:** ensure streamed content works with screen readers; do not rely on color alone for state.

## Tone and trust

Calibrate **confidence** in copy—avoid “I have verified” unless checks exist. Offer **sources** when retrieval is involved.

Instrument **drop-off** after errors and long waits; UX fixes should move those curves, not only polish copy.

**Localization:** streaming order and **RTL** layouts affect how progress reads; verify agent status strings with native speakers, not only machine translation.

Offer **export** of transcripts where policy allows—enterprise users often need audit trails outside your UI.

## Common mistakes

- **Blank screens** during 30–60s tool calls.
- Dumping **raw JSON** or internal errors to end users.
- No **cancel** path, forcing users to abandon the tab.
- **Fake** progress bars that jump arbitrarily—worse than none.
- **Inconsistent** terminology (“task,” “job,” “run”) across surfaces.
- Showing **internal** tool names that confuse non-technical users without plain-language labels.

## References to course modules

These map to the **23-module Agent Factory course** (see [`../../course/README.md`](../../course/README.md) when published).

- **Module 01 — What Are Agents** — mental model for what users should expect on the surface.
- **Module 04 — System Prompts for Agents** — tone, disclosure, and trust copy aligned with behavior.
- **Module 19 — Observability and Debugging** — aligning user-visible status with internal traces.

Full curriculum index: [`../../course/README.md`](../../course/README.md) (when present).

## See also

- [Human-in-the-Loop](human-in-the-loop.md)
- [Error Recovery](error-recovery.md)
- [Progressive Complexity](progressive-complexity.md)
- [Observability](observability.md)
- [Agent Lifecycle](agent-lifecycle.md)
