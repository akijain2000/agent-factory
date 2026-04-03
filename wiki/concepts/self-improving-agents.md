# Self-Improving Agents

## What it is

**Self-improving agents** close **learning loops** over experience: they **reflect** on failures, **distill** reusable procedures, and sometimes **author** new **skills** or **tools** from successful traces. **Persistent knowledge** across sessions—playbooks, embeddings, or parameterized skill files—lets behavior improve without retraining weights. Research threads such as **hermes-agent**, **ouroboros**, and **autoagent** explore automated skill libraries, recursive self-modification guardrails, and harness-driven **meta** optimization.

## Why it matters for agents

Static prompts cannot capture org-specific **edge cases** or evolving APIs. Controlled self-improvement reduces **repeat** incidents and onboarding cost for new **tools**—if every lesson is **auditable** and **scoped**. Without governance, “learning” becomes **unbounded** prompt drift or unsafe **code** accumulation.

Treat **feedback** as data: label quality, toxicity, and **PII** presence before it enters training or retrieval corpora used by other customers.

## How to implement it

1. **Capture:** log **structured** outcomes (task type, tools, errors, human corrections) with **run_id** correlation.
2. **Reflect:** offline jobs summarize **failure clusters**; propose **skill** updates or **FAQ** entries—never auto-apply without review in high-risk domains.
3. **Skill creation:** represent skills as **versioned** artifacts (markdown procedures, JSON schemas, small programs) with **tests**; attach **scope** (which products, which tenants).
4. **Promotion pipeline:** human or automated **lint**, **security** scan, and **eval** replay before a skill enters production retrieval.
5. **Session continuity:** separate **user-specific** memory from **global** playbooks; prevent **cross-tenant** bleed via storage keys and ACLs.
6. **Rollback:** feature-flag skill corpora; keep **diffs** and **authors** for audit.

7. **Negative learning:** capture **anti-examples** (“do not do X in case Y”) with the same rigor as success playbooks to prevent repeated mistakes.

**Hermes-agent**-style emphasis: tool-centric **memory** and **planning** artifacts. **Ouroboros**-style caution: self-modification requires **sandbox** and **approval**. **Autoagent**-style harness: automate **proposals**, not **silent** commits to prod behavior.

## Human oversight

Treat **automatic** skill writes as **pull requests**: diff, review, merge. For low-risk assistants, allow **auto-merge** only with **narrow** scopes and **kill** switches.

Schedule **corpus** audits: deprecate skills tied to retired APIs or **wrong** policies before they surface in retrieval.

Measure **skill usage**: hot skills need tighter review cadence; **zombie** skills should be archived to reduce retrieval noise.

Align learning cadence with **deploy** trains—skills promoted mid-release can desync from shipped tool schemas.

## Common mistakes

- Writing **successful** but **wrong** trajectories into “best practices.”
- **Global** memory without PII redaction.
- No **deprecation** path—skills accumulate contradictions.
- Confusing **online** weight updates with **artifact** learning (different risk profiles).
- **Overfitting** to a single power user’s phrasing at the expense of broader cohorts.

## References to course modules

These map to the **23-module Agent Factory course** (see [`../../course/README.md`](../../course/README.md) when published).

- **Module 22 — Self-Improvement and Harness Engineering** — distilling feedback into better harnesses and skills.
- **Module 06 — Memory and Context Engineering** — what to retain and how it feeds the next run.
- **Module 17 — Agent Evaluation and Testing** — measuring whether self-updates actually help.

Full curriculum index: [`../../course/README.md`](../../course/README.md) (when present).

## See also

- [Feedback Loops](feedback-loops.md)
- [Agent Memory Patterns](agent-memory-patterns.md)
- [Harness Engineering](harness-engineering.md)
- [Agent Evaluation](agent-evaluation.md)
- [Autonomous Loops](autonomous-loops.md)
