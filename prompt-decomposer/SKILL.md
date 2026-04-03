---
description: Extract agent components from large prompts, codebases, or system descriptions. Identifies potential agents, tools, memory patterns, and orchestration strategies within existing systems.
---

# Agent Prompt Decomposer

Turn monolithic prompts, sprawling code, or high-level system narratives into a clear map of agent-shaped components: who decides, what runs deterministically, and what should be a callable capability.

## When to use

Invoke this skill when:

- A **large system prompt** or product spec mixes planning, execution, retrieval, and policy in one document and needs a maintainable split.
- You are **reviewing a codebase** to see where an autonomous loop already exists implicitly (or should be introduced) versus where logic should stay procedural.
- A **natural-language system description** needs to become an implementable architecture (single agent, multi-agent, or hybrid).
- Stakeholders ask whether something should be “an agent,” “a workflow,” or “a tool” and you need a repeatable decomposition pass.

## Input Types

1. **Large prompt** — A long system prompt or specification that could be decomposed into agent components (roles, policies, procedures, and examples bundled together).
2. **Codebase** — An existing repository where orchestration, API clients, schedulers, and LLM calls are intertwined; extraction clarifies boundaries.
3. **System description** — Prose or diagrams describing behavior end-to-end without implementation detail; decomposition yields a build plan.

## Decomposition Process

### Step 1: Analyze the Input

Read the input and identify:

- **Core responsibilities** — What outcomes does the system produce? What sub-problems recur?
- **Tool-like operations** — External calls, file I/O, database queries, HTTP/MCP invocations, shell commands, or other side effects with clear inputs and outputs.
- **Memory patterns** — Short-term thread state, session summaries, long-term knowledge bases, vector stores, checkpoints, and anything that must persist across turns or runs.
- **Decision points** — Branching on ambiguous input, tradeoffs, policy interpretation, prioritization, or open-ended planning.
- **Loops and iterations** — Retry policies, refinement cycles, polling, multi-step plans, or “until satisfied” behaviors.

If the input is a codebase, trace entrypoints, background jobs, and LLM call sites. Note implicit prompts (strings in code, config templates) as first-class artifacts. If it is prose only, infer these categories from described behavior and flag assumptions.

Deduplicate responsibilities that appear under different wording in the same document before clustering.

### Step 2: Identify Agent Candidates

For each cluster of responsibilities, evaluate:

- **Autonomous agent** — Needs a loop (plan, act, observe), discretionary judgment, or open-ended goals; benefits from tools and explicit stop conditions.
- **Tool** — Mostly stateless, single-purpose, deterministic or thinly wrapped IO; invoked by an agent or workflow with a stable schema.
- **Workflow** — Deterministic sequence or state machine; no ongoing LLM judgment required except perhaps at fixed human gates.

Prefer the **smallest** abstraction that preserves safety and clarity. When in doubt between “tiny agent” and “tool,” default to tool unless the cluster needs iterative reasoning.

### Step 3: Map Architecture

Based on the candidates, suggest one of:

- **Single agent with tools** — Cohesive goal, shared context, moderate tool count; one loop owns the narrative.
- **Multi-agent system** — Separable roles (e.g., research vs. implement vs. review), different trust boundaries, or parallelizable work with handoffs.
- **Hybrid** — Agents for judgment, workflows for reliability, tools for capabilities; explicit boundaries between LLM and code.

For decision criteria on when autonomy is warranted versus deterministic orchestration, read the file:

`agent-factory/wiki/research/agent-vs-workflow.md`

If the repository root differs, resolve paths relative to the `agent-factory` checkout that contains `AGENT_SPEC.md` and `wiki/`.

### Step 4: Generate Component Specs

For each identified component, produce:

- **Name and purpose** — One line each; avoid overlapping missions.
- **Type** — `agent`, `tool`, or `workflow`.
- **If agent** — System prompt outline (role, constraints, success criteria), tool list (names and responsibilities), memory strategy (what is stored, where, TTL or scope).
- **If tool** — Input/output schema (or JSON-Schema-shaped description), idempotency notes, timeout and retry expectations, error handling and safe failure modes.
- **If workflow** — Ordered or graph-shaped steps, transitions, failure branches, and where human or LLM gates belong (if any).

### Step 5: Validate Against AGENT_SPEC.md

Check each proposed **agent** against the quality standard in the repository. Read the file:

`agent-factory/AGENT_SPEC.md`

In particular, confirm:

- The component truly involves an **autonomous loop** (plan, tools, observation) or is honestly reclassified as tool/workflow.
- **Prompts** are separable from **tool contracts** and **orchestration** in your proposed layout (even if not yet files).
- **Observability, tests, and guardrails** have a plausible home (not left implicit).
- Tool surfaces are **bounded** and **documented**; no unbounded “do anything” capability without explicit policy.

Adjust names and boundaries until the design could plausibly score against the spec’s dimensions without hand-waving.

If a component is borderline, state both options (e.g., “sub-agent vs. tool with summarization”) and the tradeoff in testability and cost.

### Step 6: Present Recommendations

Deliver a structured report containing:

- **Decomposition diagram** — Text-based (ASCII or indented tree): components and data/control flow between them.
- **Component list** — Table or bullets: name, type, one-line purpose, owner of state (if any).
- **Recommended architecture** — Single vs. multi-agent vs. hybrid with rationale tied to Step 1 findings.
- **Implementation order** — Foundational tools and workflows first, then agents that depend on them; note parallelizable work.
- **Estimated complexity** — Low/medium/high per component for implementation and operational risk (not story points unless the user asks).
- **Open questions** — Explicit list of decisions the user or team must still make (models, hosting, PII, approval flows).

## Red Flags (Signs of Over-Decomposition)

- An **agent** that exposes only **one** tool and adds no distinct policy or loop; usually that agent should collapse into the caller or become the tool implementation behind a simpler interface.
- An **agent** whose sole job is to **call another agent** with no added validation, context merge, or governance; remove the passthrough layer.
- **Multiple agents** forced to share one undifferentiated mutable state without clear ownership; often signals one agent with better memory design or a workflow with a shared store.
- **Micro-agents** per tiny subtask where a single loop with a checklist tool or structured output would reduce latency and failure modes.

## Red Flags (Signs of Under-Decomposition)

- An agent sketch with **roughly twenty or more** tools — a “god agent” that will be hard to prompt, test, and secure; split by domain or by workflow phase.
- A **system prompt outline** that would exceed roughly **three thousand tokens** when fully written — too many responsibilities for one loop; specialize or push logic into workflows and tools.
- **Unrelated capabilities** bundled in one agent (e.g., billing disputes and code review) without a strong reason; separate by trust boundary and user intent.
- **Mixed safety classes** in one prompt (untrusted user content co-mingled with privileged operator instructions); split retrieval, execution, and policy layers.

## Instructions for the LLM

1. **Gather context** — Read the file(s) the user points to using the editor or filesystem read tools. Do not rely on shell `cat`, `head`, or `tail` for file contents.
2. **Scope** — If the input is huge, ask for a path priority (entrypoints, README, orchestration module, prompt files) or read representative slices, then summarize gaps.
3. **Clarify** — Ask minimal questions when ownership, deployment environment, or compliance constraints would change the architecture map.
4. **Cross-check** — Before finalizing, read `agent-factory/wiki/research/agent-vs-workflow.md` and skim `agent-factory/AGENT_SPEC.md` for alignment unless the user forbids extra reads.
5. **Output** — Use clear headings matching Step 6; keep specs concise but actionable. Prefer tables and trees over long prose.
6. **Honesty** — If the input is already a thin chat wrapper, say so and recommend a smaller decomposition (or none) rather than inventing agents.

### What this skill does not do

- It does not rewrite production prompts or ship runnable code unless the user asks for a follow-up task.
- It does not replace product discovery; business prioritization stays with the user.
- It does not guarantee a unique “correct” architecture—offer the best-fit default and list alternatives when tradeoffs matter.

### Optional follow-ups

If the user wants to proceed after the report, suggest creating or updating `system-prompt.md`, tool schemas under `tools/`, and a short `README.md` architecture section per `AGENT_SPEC.md`, or hand off to an agent-maker workflow in the same repository.
