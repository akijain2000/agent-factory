---
description: Review and improve existing agent projects using wiki-backed best practices and AGENT_SPEC.md quality standards. Two modes: guided brainstorm or quick report.
---

# Agent Authoring Review

Meta-skill for auditing an **existing** agent codebase against `AGENT_SPEC.md` and the agent-factory wiki. You produce scores, evidence-backed gaps, and concrete improvements, optionally iterating with the user.

## When to use

Invoke when the user wants to **review**, **audit**, **improve**, or **refactor** an agent project that already has (or should have) a loop, tools, and runtime code. Use for pre-release checklists, onboarding another engineer to an agent repo, or closing gaps versus the eight AGENT_SPEC dimensions. Do **not** use this as a substitute for organizational security sign-off or penetration testing; cite spec and wiki gaps, then defer high-risk items to dedicated review.

**Choosing a mode:** If the user asks for a **report**, **rubric**, **scores only**, or **shareable output**, use Mode B. If they ask to **workshop**, **brainstorm**, **pair on fixes**, or **iterate**, use Mode A. If unspecified, ask once; default to Mode B when they paste a repo path with no other context.

## Prerequisites

Assume the `agent-factory` directory is in the workspace so you can read `AGENT_SPEC.md` and `wiki/` without asking. If only the target agent repo is open, ask the user to add `agent-factory` to the workspace or paste the paths they want treated as canonical for spec and wiki.

## Mode A: Guided Brainstorm

Interactive pass with the user:

1. Read the agent’s system prompt, tool definitions, and architecture (see Step 1 below).
2. Score every dimension in Section 3 of `AGENT_SPEC.md` (0–10, half-steps allowed), with one sentence of evidence per score.
3. For each dimension **below 7/10**, read the relevant wiki articles from the Wiki Lookup Guide and extract 1–3 applicable recommendations.
4. Present findings in dimension order: score, issue summary, wiki-backed suggestion, and one clarifying question where tradeoffs matter.
5. After the user responds, generate **improved drafts** for the weakest artifacts (prompt excerpts, tool schemas, test scenarios, README sections) without rewriting unrelated files.

Optional follow-up rounds: re-score only the dimensions that changed after edits; keep a short **changelog** of what moved and why so the user can track review progress.

## Mode B: Quick Report

Non-interactive pass:

1. Read the agent project using the same scope as Step 1.
2. Score **all eight** AGENT_SPEC dimensions with brief evidence each.
3. Emit a single **markdown report** with: executive summary (3–5 bullets), scoring table, per-dimension issues, and prioritized recommendations.
4. For each recommendation, add a markdown link or path to the **specific** wiki file that supports it (e.g. `agent-factory/wiki/concepts/tool-design.md`).
5. End with an optional **compliance note**: map findings to Section 4 (required files) and Section 5 (anti-patterns) of `AGENT_SPEC.md` where relevant.

**Report structure (Mode B):** Use consistent headings: `## Summary`, `## Scores`, `## Findings by dimension`, `## Recommendations` (numbered, each with wiki link), `## Required files / anti-patterns`, `## Suggested next steps`. Keep the full report under roughly four screenfuls unless the user asked for exhaustive detail.

## Relationship to Agent Maker

`agent-maker` is for **greenfield** design. This skill is for **brownfield** review. If the user mixes goals (e.g. “audit this repo then redesign from scratch”), finish the review pass first, then offer to switch to agent-maker for a new architecture phase.

## Review Process

### Step 1: Read the Agent Project

Establish the **agent package root** (repo root or a documented subdirectory in a monorepo). Then read, at minimum:

- Read the file: `README.md` (purpose, quickstart, architecture, config).
- Read the file: `system-prompt.md` or the documented equivalent (composed prompts: read every fragment and the merge order).
- Read the file: `tools/README.md` and each tool spec or schema under `tools/` (or the repo’s source of truth for tool contracts).
- Read representative files under `src/` (loop entrypoint, tool dispatch, config loading).
- Read the file: one or more files under `tests/` that exercise the loop or tools.
- Skim `deploy/` and CI config at repo root when present (timeouts, secrets as names only, health checks).

If something is missing, record it as a **Documentation** or **Architecture** finding and still score honestly.

**Monorepos:** Read the file: the agent package `README.md` that `AGENT_SPEC.md` treats as the entry point; apply the required-files checklist relative to that directory per Section 4.

**Drift checks:** Compare tool names and parameters in `system-prompt.md` (or fragments) against live schemas and `src/` registration. Flag **tool/schema drift** explicitly when prompt text and code disagree, even if both sides look healthy in isolation.

**Models and config:** Note model ids, temperature caps, and max-step or budget settings when they appear in code or config; tie runaway-cost risk to `wiki/concepts/cost-optimization.md` and `wiki/concepts/rate-limiting.md` when relevant.

### Step 2: Score Against AGENT_SPEC.md

Read the file: `AGENT_SPEC.md`. Score these eight dimensions using anchors in Section 3 (0 / 5 / 10):

1. Architecture  
2. System Prompt  
3. Tool Design  
4. Memory Strategy  
5. Safety  
6. Testing  
7. Observability  
8. Documentation  

Cross-check Section 5 anti-patterns and Section 4 required files; mention any direct hits by name.

When two dimensions conflict in your narrative (e.g. high Documentation, low Testing), apply the coupling note in Section 3 of `AGENT_SPEC.md` and adjust the written assessment so scores stay credible.

### Step 3: Consult the Wiki

For dimensions below your chosen threshold (default **7/10** in Mode A; in Mode B, still read wiki for every dimension scored **below 8/10** or any dimension with an anti-pattern hit). Read the file for each path under `agent-factory/` (or the workspace-relative path if the user symlinked wiki elsewhere).

**Order:** Address **Safety** and **Architecture** gaps before cosmetic **Documentation** improvements when both are weak, unless the user scoped the review narrowly.

Read the file: `wiki/INDEX.md` when you are unsure which concept article fits; prefer `wiki/concepts/` for prescriptive guidance and `wiki/research/` for landscape and comparisons.

### Step 4: Generate Recommendations

Each recommendation must be **specific and actionable** (what to change, where, and why). Tie recommendations to spec subsections or anti-pattern IDs when possible. Avoid generic advice that does not reference observed files or behaviors.

**Prioritization:** Rank by severity (safety and data loss first), then by leverage (fixes that unlock testing or observability), then by effort. Mark **quick wins** (under an hour of engineering) when obvious.

### Step 5: Improve

Produce improved text or schemas **only** for components you identified as weak: e.g. revised `system-prompt.md` sections, stricter JSON Schema, a new behavioral test description, or README diagram text. Label drafts clearly as **proposed** so the user can paste or PR them. Do not claim AGENT_SPEC compliance unless Section 4 checklist items are satisfied and you have stated that explicitly.

When the user only wanted a report, put proposed rewrites in a final **Appendix: optional patches** section instead of editing their repo.

## Wiki Lookup Guide

Use this map to pick articles; read additional linked concepts from `wiki/INDEX.md` when the issue spans topics.

| Issue type | Read the file |
|------------|----------------|
| Loop shape, orchestration, stop conditions | `wiki/concepts/agent-loop.md`, `wiki/concepts/progressive-complexity.md`, `wiki/concepts/autonomous-loops.md` |
| Tool contracts, schemas, side effects | `wiki/concepts/tool-design.md`, `wiki/concepts/tool-selection.md`, `wiki/concepts/structured-outputs.md` |
| Context, memory, retrieval | `wiki/concepts/memory-systems.md`, `wiki/concepts/context-engineering.md`, `wiki/concepts/context-window-management.md`, `wiki/concepts/agent-memory-patterns.md` |
| Guardrails, injection, privilege | `wiki/concepts/guardrails.md`, `wiki/concepts/sandboxing.md`, `wiki/concepts/agent-security.md` |
| Tests, evals, regression | `wiki/concepts/agent-testing-patterns.md`, `wiki/concepts/agent-evaluation.md` |
| Prompt quality, persona, refusal | `wiki/concepts/prompt-engineering-for-agents.md`, `course/04-system-prompts-for-agents.md` |
| Planning and recovery | `wiki/concepts/planning-strategies.md`, `wiki/concepts/error-recovery.md` |
| Multi-agent and handoffs | `wiki/concepts/multi-agent-orchestration.md`, `wiki/concepts/agent-handoffs.md`, `wiki/concepts/agent-composition.md` |
| Ops, traces, cost | `wiki/concepts/observability.md`, `wiki/concepts/feedback-loops.md`, `wiki/concepts/cost-optimization.md` |
| Human gates and UX | `wiki/concepts/human-in-the-loop.md`, `wiki/concepts/agent-ux.md` |
| Anti-pattern calibration | `wiki/research/anti-patterns.md`, `course/11-anti-patterns.md`, relevant files under `wiki/examples/bad/` |
| State, persistence, recovery | `wiki/concepts/state-management.md`, `wiki/concepts/agent-lifecycle.md`, `course/12-state-management.md` |
| Deployment and scaling | `wiki/concepts/deployment-patterns.md`, `course/20-deployment-and-scaling.md` |
| Framework fit | `course/13-framework-selection.md`, `wiki/research/framework-comparison.md` |

## Conflicts with spec or wiki

When the user wants a change that violates `AGENT_SPEC.md` or strong wiki guidance (e.g. no tests, secrets in prompts, unbounded loops), state the **risk**, cite the spec section or wiki path, and offer the **smallest compliant alternative**. Do not silently approve unsafe shortcuts.

## Instructions for the LLM

1. **Paths**: Treat `agent-factory/AGENT_SPEC.md` and `agent-factory/wiki/` as the knowledge base. If the reviewed project lives outside this tree, still use those paths when the wiki is available in the workspace; otherwise ask the user to open or attach `agent-factory`.
2. **Reading**: Use “Read the file:” with the path (e.g. `Read the file: agent-factory/AGENT_SPEC.md`). Do not rely on shell `cat` or `head` for content you must reason about.
3. **Scoring**: Never inflate scores without evidence. If files are missing, score down and cite Section 4.
4. **Output**: Mode A uses conversational sections with scores first, then wiki-backed fixes. Mode B uses a single markdown document suitable to save as `REVIEW.md` with a scoring table and linked recommendations.
5. **Scope**: Prefer the smallest change that raises the weakest dimension; avoid repo-wide rewrites unless the user asks.
6. **Aggregate**: If the user needs a single number, read Section 6 of `AGENT_SPEC.md` and apply the documented aggregate rule; state it explicitly when you report an overall score.
7. **Evidence**: Quote short snippets or cite file paths when stating a defect; avoid unverifiable claims about runtime behavior unless logs or tests are in the repo.
8. **Good examples**: When recommending a pattern, you may point to one file under `wiki/examples/good/` that illustrates the shape (read the file before citing).
9. **Course depth**: Use `course/` chapters when the wiki article is thin and the gap is pedagogical (e.g. first-time loop design); keep citations one layer deep unless the user asks for a syllabus-style reading list.
10. **Tone**: Be direct and kind; assume the author had constraints. Separate **must-fix** (safety, compliance, anti-pattern blockers) from **should-fix** and **nice-to-have**.
