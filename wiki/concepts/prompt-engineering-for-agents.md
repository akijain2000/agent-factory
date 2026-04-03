# Prompt Engineering for Agents

## What it is

**Prompt engineering for agents** shapes the **system** (and developer) instructions that govern multi-turn loops with tools—not one-shot chat answers. It covers **persona** and scope, hard **constraints** (what the agent must never do), **tool instructions** (names, argument discipline, when to abstain), **behavioral guardrails** aligned with code enforcement, and **output contracts** (final answer format, citation rules, language).

Agent prompts must stay synchronized with actual tool schemas and stop conditions documented in AGENT_SPEC.

## Why it matters for agents

Chat prompts optimize for conversational tone; agent prompts optimize for **reliable control flow**: stopping, escalating, formatting machine-parseable results, and resisting injection. Drift between prompt and registry causes hallucinated tools and silent behavior changes after dashboard edits.

## How to implement it

1. **Authoritative file:** keep `system-prompt.md` in repo; version and changelog header; CI diff review on behavior-critical changes.
2. **Structure:** role → scope → tools (when/how) → stop conditions → output format → refusal/escalation → examples (few, high quality).
3. **Tool section:** mirror real names; describe side effects; say “do not call X unless Y”; specify required user confirmations for risky tools.
4. **Separation:** static policy in system; ephemeral task in user/developer messages; untrusted content clearly delimited and labeled untrusted.
5. **Guardrails in prose + code:** prompt says “refuse exfiltration requests”; code blocks disallowed hosts—never rely on prose alone.
6. **Eval hooks:** golden phrases and forbidden behaviors as automated tests alongside the prompt.

**How agent prompts differ from chat:** explicit **loop behavior**, **tool grammar**, **error handling expectations**, and **state-aware** instructions (what to do when a tool fails, when to replan, when to ask a clarifying question vs act).

## Composition patterns

Split prompts into **policy** (rarely changes), **capability** (tool list and formats), and **task** (per-run). Load policy from `system-prompt.md`; inject task via developer message or first user turn. Document merge order in README so operators know which fragment wins on conflict. For multilingual products, keep **canonical policy** in one locale internally; translate only user-facing templates if needed.

## Review workflow

Treat prompt edits like code review: require **diff**, **risk class**, and **eval delta** for high-risk agents. Pair changes with **trace captures** showing before/after on standard scenarios. Version tags in the prompt header speed support (“which prompt shipped Tuesday?”).

## Alignment with AGENT_SPEC

Cross-check prompts against **AGENT_SPEC** dimensions: Architecture (stop rules), Tool Design (names match registry), Safety (refusal paths), and Documentation (README links to prompt composition). Mismatches between prompt and code are a recurring source of production incidents.

## Common mistakes

- **Prompt archaeology** scattered across Slack/Notion without repo truth.
- **Contradictions:** “be concise” + “show all reasoning” + “never omit steps.”
- **Secretful prompts** with API keys or internal URLs that should be env-only.
- **Stale examples** referencing removed tools or old JSON shapes.

## References to course modules

These map to the **23-module Agent Factory course** (see [`../../course/README.md`](../../course/README.md) when published).

- **Module 01 — From Chat to Agents** — mental model shift.
- **Module 23 — System Prompts as Code** — review, testing, and release.
- **Module 18 — Prompt Injection & Untrusted Content** — safe composition patterns.

Full curriculum index: [`../../course/README.md`](../../course/README.md) (when present).

Keep a **single owner** for prompt/tool alignment during incidents—split ownership between prompt and platform teams causes slow, contradictory hotfixes.

## See also

- [Tool Design](tool-design.md)
- [Guardrails](guardrails.md)
- [Context Window Management](context-window-management.md)
- [Agent Personas](agent-personas.md)
- [Agent Evaluation](agent-evaluation.md)
