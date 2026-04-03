# Production Case Studies: Agents That Ship

This survey contrasts **productized** agent systems—IDE assistants, dev harnesses, workflow automation—with demo-grade loops. The theme: production winners **bound** autonomy, **instrument** everything, and **compose** deterministic code with model judgment.

## IDE and coding assistants (e.g., Cursor-class products)

**What works:** Tight **context** from open buffers and LSP; **diff-based** edits; user-visible **plans**; local execution with sandbox awareness. **Challenges:** large-repo retrieval quality, long-horizon refactors, and safe **terminal** access.

**Lesson:** UX that keeps humans **in the loop** for irreversible actions beats pure autonomy for mainstream adoption.

## gstack-style harnesses

**What works:** **Skills** as procedural modules; **browse daemon** for fast headless verification; workflows like **ship** and **land-and-deploy** encode organizational policy. Agents become **orchestrators** over stable tools.

**Lesson:** Package operational expertise as **repeatable skills**, not one-off prompts.

## Autonomous coding agents (e.g., Devin-class narratives)

**What works:** End-to-end task framing with **environments** (VMs, containers) and **test feedback**. **Challenges:** cost, flakiness on real enterprise codebases, and **integration** depth (CI, auth, private deps).

**Lesson:** Sandboxed **runtime + tests** beat prose-only self-verification.

## Customer support agents

**What works:** **RAG** over policies, **triage routers**, and **human handoff** on low confidence. **Challenges:** brand-safe tone vs accuracy; PII; tool actions (refunds) needing **approval**.

**Lesson:** Policy engines and **structured escalation** matter as much as model quality.

## Cross-cutting production patterns

- **Trace-first** debugging and correlation IDs.
- **Budgets** on steps and spend.
- **Schema boundaries** between steps.
- **Versioned** prompts/tools/evals in CI.

## Internal platform agents (data/ops)

Enterprises deploy agents for **ETL diagnostics**, **on-call summarization**, and **runbook suggestion**. Wins come from **read-only** default tools and **tight** scopes on production credentials. Failures track with **stale documentation**—agents confidently recommend retired procedures unless KBs are living artifacts.

## Lessons for greenfield builders

Ship a **thin** agent with **one** high-value workflow, **full** tracing, and **explicit** stop conditions before expanding tool breadth. Breadth-first launches score demos; depth-first launches survive **week two** operations.

## Summary

Production wins repeat the same motifs: **bounded** autonomy, **transparent** actions, **test-backed** verification, and **human gates** on irreversible tools—whether the surface is an IDE, a harness, or a support console.

## Sources and further reading

- Public engineering blogs from IDE/agent vendors (where available).
- Anthropic and OpenAI operational guidance.
- Internal runbooks and postmortems (pattern synthesis).

## See also

- [Gstack agent analysis](gstack-agent-analysis.md)
- [Agent vs workflow](agent-vs-workflow.md)
- [Cost analysis](cost-analysis.md)
- [Anatomy of a good agent](anatomy-of-a-good-agent.md)
- Concepts: [Deployment Patterns](../concepts/deployment-patterns.md), [Human-in-the-Loop](../concepts/human-in-the-loop.md), [Observability](../concepts/observability.md), [Sandboxing](../concepts/sandboxing.md)
- Course: [Agent Factory course](../../course/README.md)
