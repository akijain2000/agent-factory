---
description: Agent Factory -- LLM knowledge base for building production-quality AI agents. Navigate to review an existing agent, create a new agent, learn about agent building, or decompose a system into agent components.
---

# Agent Factory

Agent Factory is a structured knowledge base for designing, reviewing, and shipping autonomous LLM agents that meet production standards. It combines a modular course, a deep wiki, and guided workflows so you can move from vague intent to a spec-aligned agent layout without improvising from scratch. When you load this skill, your first job is to help the user pick a path, then open and follow the referenced file for that path instead of substituting generic advice.

## Operating principles

- Prefer **file-backed** guidance over improvisation: the course, wiki, and sub-skills encode decisions the project already made about vocabulary and quality bars.
- When reviewing or creating agents, keep **AGENT_SPEC.md** in view as the contract for what “production-quality” means in this ecosystem.
- Separate **instructions** (prompts), **capabilities** (tools and contracts), **runtime** (loop and state), and **verification** (tests and evals); call out mixing these layers when you see it.
- Be explicit about **assumptions** (model provider, sync versus async loop, deployment environment) before recommending structure.

## Menu

Present these options to the user:

**A) Review and improve an existing agent**
**B) Brainstorm and create a new agent**
**C) Learn about agent building**
**D) Extract agent components from a codebase or prompt**

After the user chooses, confirm the choice briefly and proceed with the matching route. If they are unsure, suggest **C** for grounding, then **B** or **A** depending on whether they already have code. **D** fits large prompts, runbooks, or legacy descriptions they want to split into agent-shaped pieces.

## Route A: Review an Existing Agent

Read the file: `authoring/SKILL.md`

Treat that file as the single source of truth for the review workflow. Load it fully before offering opinions. Follow its steps in order: gather the agent repository or artifact, apply the quality bar from `AGENT_SPEC.md`, and produce actionable edits rather than high-level praise. If the user only has a partial export (prompt only, or tools only), state that explicitly and scope the review to what is present.

When the repository is on disk, you may run `bun scripts/validate-agent.ts <project-root>` (or Node with Bun-compatible execution) and weave machine Pass/Warn/Fail results into your narrative. Name concrete gaps: missing tests, unclear stop conditions, undocumented tools, or prompts that mix policy with implementation. Tie recommendations to sections in `AGENT_SPEC.md` when possible so remediation is traceable.

If the user pastes only a system prompt, review it against the same dimensions (persona, constraints, tool-use clarity, stop conditions) and ask for the missing repository pieces before claiming full compliance.

## Route B: Create a New Agent

Read the file: `agent-maker/SKILL.md`

Load and read that file fully before offering opinions or starting creation. Use the agent-maker skill for interactive creation: clarify goals, constraints, and deployment context before drafting structure. Align outputs with the canonical layout and required artifacts in `AGENT_SPEC.md` (README, system prompt, tool contracts, tests, separation of orchestration code). Prefer concrete file names and section headings the runtime can load, not prose that lives only in chat.

Default assumption: the user wants an autonomous tool loop, not a single-shot chat wrapper. If they only need a markdown skill for an existing assistant, point them to **Skill Factory** instead of over-building an agent repository here.

Offer a short checklist after the first pass: README with architecture, versioned system prompt, `tools/` contracts, non-empty `tests/`, and separation of orchestration from narrative prompts.

## Route C: Learn

Two sub-routes. If the user's topic already implies one, go directly; otherwise offer both:

1. **Browse the 23-module course:** Read the file: `course/README.md`. Use it as the table of contents for the full sequence. When the user names a topic, open the matching module file under `course/` rather than summarizing from memory.
2. **Browse the wiki:** Read the file: `wiki/INDEX.md`. Use it to navigate articles by theme. Prefer primary wiki pages over ad hoc explanations when the user wants depth, pattern citations, or vocabulary.

If the user is new, start from `course/01-what-are-agents.md` or the INDEX entry that best matches their goal. If they are experienced, jump from INDEX into `wiki/concepts/` or `wiki/research/` as appropriate. When answering from course or wiki material, cite the file path you used so the user can reopen it later.

Encourage spaced learning: one module plus one wiki article often beats a long abstract summary. If they ask for “everything about X,” point to the INDEX cluster for X and offer a reading order.

## Route D: Extract from Prompt

Read the file: `prompt-decomposer/SKILL.md`

Load and read that file fully before responding. Follow that skill when the user wants to turn a large prompt, runbook, or monolithic system description into separable agent components (sub-agents, tools, policies, evaluation hooks). The output should be structured and mappable to files under an agent repo, not a single blob prompt.

If the source is a codebase rather than prose, still use the decomposer skill for the inventory step, then cross-check against `AGENT_SPEC.md` for where each piece should live (prompt versus tools versus orchestration).

Deliverables from route D should read like a **skeleton repo plan**: proposed files, ownership of each concern, and which parts are human-only policy versus machine-executable tools.

## Wiki Reference

The wiki contains 80+ articles:

- 35 concept articles in `wiki/concepts/`
- 20 research articles in `wiki/research/`
- 22 annotated examples in `wiki/examples/`
- Glossary with 60+ terms (`wiki/GLOSSARY.md` and links from `wiki/INDEX.md`)

Cross-check terminology and minimum bars against `AGENT_SPEC.md` whenever you claim a project is production-ready or spec-compliant.

Use `wiki/examples/bad/` when the user is about to repeat a known failure mode; use `wiki/examples/good/` when they need a concrete pattern to emulate.

## Companion Project

Agent Factory is a sibling project to Skill Factory. Skills are markdown files that augment existing agents with procedures and checklists. Agents are the autonomous systems themselves: loops, tools, state, and runtime harnesses. Use Skill Factory when the deliverable is a reusable skill; use Agent Factory when the deliverable is an agent product or harness.

The two projects compose naturally: a mature agent may load several skills as procedural overlays while still owning its own repo layout, tests, and deployment story described here.

## Handoffs between routes

It is normal to move between routes in one session. Typical flows:

- **C then B:** Learn vocabulary, then design a new agent with shared terms.
- **B then A:** Draft structure, then review the resulting repo against `AGENT_SPEC.md`.
- **D then B:** Decompose a monolith or giant prompt, then run agent-maker to turn the decomposition into files.

State where you are in the flow so the user can resume if the conversation fragments.

## Path resolution and maintainer scripts

Assume paths in this skill are relative to the Agent Factory repository root unless the user specifies another workspace. If only a nested folder is open in the editor, search upward for `AGENT_SPEC.md` or `wiki/INDEX.md` to locate the project root before reading routes.

For **maintainers** of this repository, optional LLM runbooks and tooling live under `scripts/`: `compile-wiki.md`, `health-check.md`, `update-sources.md`, `discovery-keywords.txt`, and `validate-agent.ts`. End users on routes A through D do not need these unless they ask to maintain Agent Factory itself.

When a user’s agent repo lives outside Agent Factory, run `validate-agent.ts` against **their** project root, not the Agent Factory tree, so results reflect their layout rather than this knowledge base’s layout.

`validate-agent.ts` is written for Bun (`#!/usr/bin/env bun`). If Bun is not available, it also runs under Node 18+ with `npx tsx scripts/validate-agent.ts` or similar TypeScript runners.
