# Agent Personas

## What it is

An **agent persona** is the explicit definition of identity and behavior: role (e.g., support engineer, research analyst), **tone** (concise vs tutorial), **expertise boundaries** (what it may claim to know), and **behavioral consistency** rules (citations required, escalation triggers). Personas live in system prompts, policy modules, and sometimes separate **style** vs **substance** instructions for multi-agent systems.

## Why it matters for agents

Without a persona, models default to generic assistant behavior: overconfident claims, inconsistent formality, or unsafe role drift. Personas anchor **user trust**, **brand**, and **compliance** (“I am not a lawyer”). In **multi-agent** setups, distinct personas reduce goal interference and make handoffs interpretable—users and developers know which voice owns which subtask.

## How to implement it

1. **Write a role charter:** mission, non-goals, mandatory behaviors (e.g., always confirm destructive actions), and prohibited claims.
2. **Separate layers:** stable identity and policies in system message; task-specific detail in user or developer turns to reduce prompt thrash.
3. **Expertise boundaries:** instruct the model to defer or escalate when outside scope; wire tools and humans to those escalation paths.
4. **Tone cards:** short bullet style guides; avoid contradictory adjectives; test with sample user segments.
5. **Multi-agent:** give each sub-agent a narrow persona and explicit **inputs/outputs**; avoid duplicate authority on the same decision type.
6. **Evaluation:** behavioral tests for tone, refusal quality, and boundary adherence—not only task success.

## Consistency across sessions

Persist **user-facing preferences** (verbosity, locale) in structured memory; keep **policy** in versioned prompts. Document persona version in traces for debugging regressions.

## Multi-agent persona interactions

When agents hand off, align **voice**: either a unified customer-facing persona with internal specialists, or explicit disclosure (“Transferring you to the billing specialist”). Avoid dueling tones in a single thread. Define which persona **owns** apologies, compliance disclaimers, and pricing statements.

## Behavioral consistency testing

Add scenarios that probe **refusal** quality: requests for credentials, illegal acts, or out-of-scope medical advice. Score not only whether the agent refused but whether it offered safe alternatives. Track **persona drift** when base model versions change.

## Why personas differ from raw prompts

Personas bundle **identity**, **values**, and **operational rules** into a coherent contract. Raw prompt tweaks without a persona model tend to accrete contradictions. Treat persona updates like API changes: review, version, and test.

## Common mistakes

- Persona prose that conflicts with tool capabilities (“I cannot access the internet” while browsing tools exist).
- Overly long character backstory that crowds tool rules and safety instructions.
- Identical personas for every sub-agent, causing redundant reasoning and confusion at handoffs.
- No tests for persona rules; they erode silently as prompts are edited.

## Quick checklist

- Persona doc lists **non-goals** and **mandatory behaviors** on one page.
- Tool catalog and persona claims are reviewed together for contradictions.
- Persona version string is logged on every trace root span.

## References to course modules

These map to the **23-module Agent Factory course** (see [`../../course/README.md`](../../course/README.md) when published).

- **Module 04 — System Prompts for Agents** — identity, policy layering, and persona design.
- **Module 10 — Multi-Agent Patterns** — specialized roles in orchestrated systems.
- **Module 17 — Agent Evaluation and Testing** — validating persona adherence and drift.

Full curriculum index: [`../../course/README.md`](../../course/README.md) (when present).

## See also

- [Prompt Engineering for Agents](prompt-engineering-for-agents.md)
- [Multi-Agent Orchestration](multi-agent-orchestration.md)
- [Agent Handoffs](agent-handoffs.md)
- [Guardrails](guardrails.md)
- [Human-in-the-Loop](human-in-the-loop.md)
