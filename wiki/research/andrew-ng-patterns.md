---
category: research
tags: [andrew-ng, agentic-patterns, reflection]
---

# Andrew Ng’s Agentic Design Patterns

Andrew Ng’s widely cited framing organizes “agentic” behavior into **four patterns**: reflection, tool use, planning, and multi-agent collaboration. The value is pedagogical clarity—each pattern maps to **different engineering surfaces** (prompt structure, runtime, orchestration graph). Below: what each pattern optimizes, failure modes, and minimal implementation sketches.

## Reflection

**Idea:** A generator produces a draft; a **critic** (same or different model, or code checks) proposes improvements in a second pass.

**Engineering surfaces:** Two-step prompts, evaluator–optimizer graphs, or lint/test feedback loops. Reflection improves **draft quality** when errors are **local** and critique is grounded (e.g., failing tests).

**Failure modes:** Sycophantic agreement, uncapped iteration cost, critique that ignores tool reality. Mitigate with **hard stops**, diverse sampling on retry, and **grounding** critique in executable signals.

**Sketch:** `draft = model(task)` → `critique = model(draft + rubric)` → `revise = model(draft + critique)` with max two refinement rounds unless tests still fail.

## Tool use

**Idea:** The model **selects** external capabilities (APIs, search, code execution) instead of hallucinating facts or math.

**Engineering surfaces:** JSON-schema tools, MCP servers, sandboxed runners. Success depends on **tool cardinality**, descriptions, and **idempotency**.

**Failure modes:** Wrong tool selection, argument hallucination, prompt injection via tool outputs. Mitigate with **small tool sets**, output sanitization, and **human gates** on risky tools.

**Sketch:** Router classifies intent → one primary tool executes → model summarizes with **citations** from tool payloads only.

## Planning

**Idea:** Before acting, the model **decomposes** the task into steps, optionally revising the plan when observations change.

**Engineering surfaces:** Plan–execute graphs, ReAct-style interleaving, hierarchical task networks in code.

**Failure modes:** Over-planning, plans that ignore tool constraints, stale plans after environment shifts. Mitigate with **re-plan triggers** on tool error classes and **budgets** on plan depth.

**Sketch:** Emit structured plan (JSON) → execute stepwise → on `ToolError`, replan with **append-only** memory of attempts.

## Multi-agent

**Idea:** Specialized agents divide labor—researcher, coder, reviewer—often with a **coordinator** or shared blackboard.

**Engineering surfaces:** Handoff protocols, message buses, A2A-style delegation where frameworks interoperate.

**Failure modes:** Ambiguous ownership, duplicated work, inconsistent world models. Mitigate with **single-writer** policies for shared state and **explicit schemas** for handoffs.

**Sketch:** Orchestrator assigns subtasks with **acceptance criteria** → workers return structured results → integrator merges; human reviews **irreversible** steps.

## Composing patterns

Production systems rarely use one pattern in isolation. A robust coding agent might **plan**, **use tools** (repo, tests), **reflect** on failures, and optionally **split** codegen from review across roles—under **global budgets**.

## Sources and further reading

- Andrew Ng’s public talks and educational materials on agentic workflows (reflection, tool use, planning, multi-agent).
- Anthropic *Building Effective Agents* for workflow templates that map to these patterns.
- OpenAI Agents SDK for handoffs and tracing as multi-agent infrastructure.

## See also

- [Anthropic agent patterns](anthropic-agent-patterns.md)
- [Multi-agent landscape](multi-agent-landscape.md)
- [Anti-patterns](anti-patterns.md)
- Concepts: [Planning Strategies](../concepts/planning-strategies.md), [Tool Design](../concepts/tool-design.md), [Feedback Loops](../concepts/feedback-loops.md), [Multi-Agent Orchestration](../concepts/multi-agent-orchestration.md)
- Course: [Agent Factory course](../../course/README.md)
