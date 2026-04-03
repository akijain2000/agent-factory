# Module 01: What Are Agents

**Duration:** approximately 30 minutes  
**Prerequisites:** Basic familiarity with large language models (LLMs) and chat interfaces.

---

## Learning objectives

By the end of this module, you should be able to:

- Define what an **agent** is in the context of LLM-based systems.
- **Distinguish** agents from chatbots, copilots, and deterministic workflows.
- **Identify** the main components of an agent: LLM core, tools, memory, and control loop.
- **Decide** when an agent is appropriate versus a simpler pattern (prompt, RAG, or workflow).

---

## 1. Definitions: agent vs chatbot vs copilot vs workflow

**Chatbot**  
A system optimized for **turn-by-turn conversation**. Each user message typically triggers one model response. The model may retrieve context or call a tool occasionally, but there is no sustained **autonomous loop** where the model plans multiple steps without a human in each step.

**Copilot**  
An assistant **embedded in a human’s workflow** (IDE, document editor, browser). It suggests, completes, or edits alongside the user. The human remains the primary driver; the system rarely runs long, unsupervised action sequences.

**Workflow**  
A **deterministic or rule-based** pipeline: fixed steps, branches, and integrations (for example, “if form submitted, then validate, then enqueue job”). LLMs may appear as one step, but **orchestration is explicit code or configuration**, not an open-ended model loop.

**Agent**  
An LLM-driven system that **repeatedly reasons, acts, and observes** until a goal is reached or a stop condition fires. The model chooses **which tools to call**, in what order, and how to interpret results—within boundaries you define. Autonomy is **bounded**, not unlimited.

A useful shorthand: if removing the loop leaves you with “one-shot Q&A,” you probably have a chatbot or tool-augmented chat, not an agent.

---

## 2. The anatomy of an agent: LLM core, tools, memory, state, loop

**LLM core**  
The reasoning engine. It interprets goals, selects actions, and synthesizes answers. Quality of planning and tool use depends on model capability, prompting, and context.

**Tools**  
Callable capabilities: APIs, databases, code execution, browsers, file systems. Tools turn language into **effects in the world** (or in a sandbox). Clear schemas and descriptions matter as much as the code behind them.

**Memory**  
Short-term: conversation and scratchpad inside the context window. Long-term: vector stores, summaries, or structured stores keyed by user or session. Memory answers: “What should persist across turns or sessions?”

**State**  
Structured data the harness maintains: current subgoal, checklist, retrieved artifacts, flags (e.g. “user approved step 3”). State keeps the loop **coherent** when the raw transcript alone would be ambiguous.

**Loop**  
The cycle: observe context → plan or decide next action → invoke tool(s) or respond → append observations → repeat or terminate. Without a defined loop and termination rules, “agent” behavior becomes fragile or endless.

---

## 3. The spectrum of autonomy: augmented LLM → single agent → multi-agent

**Augmented LLM**  
Single call (or few calls) with retrieval or one tool invocation. Fast and predictable; good when the task decomposes to a known pattern.

**Single agent**  
One loop, one primary model, a focused toolset. Most production “agents” are here: one policy that sequences actions until done.

**Multi-agent**  
Several agents (or role-specialized loops) with handoffs or message passing. Use when **separation of concerns**, parallel exploration, or adversarial review genuinely helps—not by default.

Moving right on the spectrum increases flexibility and often **cost, latency, and failure modes**. Prefer the **leftmost** design that meets the requirement.

---

## 4. When to use agents (and when not to)

**Favor an agent when:**

- The path to the goal **cannot be fully specified** upfront.
- Multiple tool calls or searches must be **chained** based on intermediate results.
- The task benefits from **trial and error** within safe bounds (research, debugging support, structured analysis).

**Prefer something simpler when:**

- The procedure is **stable** and known (ETL, approvals, CRUD with fixed rules).
- **Latency or cost** must be minimal and variance is unacceptable.
- **Auditability** requires every step to be explicitly coded, not inferred.

---

## 5. The agent hype cycle: what is real and what is overblown

**Grounded claims:** Tool use and multi-step reasoning can automate real work in sandboxes; observability and evals are maturing; patterns (ReAct, planners, supervisors) are documented in industry and research.

**Overblown claims:** Fully autonomous “do anything” agents without guardrails; replacing all workflows with LLM loops; assuming multi-agent is always better than one well-tooled agent.

**Practical stance:** Treat agents as **policy + tools + loop + limits**. Measure success with tasks your users actually perform, and assume **first versions will need tighter scopes** than you imagine.

---

## Exercises

### Exercise 1: Classify five AI products

Pick five products or features you use (or know). For each, label it **chatbot**, **copilot**, **agent**, or **workflow** (mixed labels allowed if you explain the dominant mode). Write one sentence of justification citing **who drives the steps** and whether a **multi-step autonomous loop** exists.

### Exercise 2: Sketch agent components for one use case

Choose a concrete use case (for example, “answer questions over our internal wiki with citations,” “triage and draft replies to support tickets,” or “run a security review checklist on a pull request”). List:

- The **LLM’s** role  
- **Tools** (names and what they do)  
- **Memory** (what persists, where)  
- **State** the harness should track  
- **Loop** termination (what “done” means)

Keep the sketch to one page; avoid framework names unless they clarify the design.

---

## Further reading

- [Agent loop (concept)](../wiki/concepts/agent-loop.md) — loop structure and termination in depth.  
- [Agent vs workflow (research)](../wiki/research/agent-vs-workflow.md) — when to keep orchestration explicit.  
- Anthropic, **Building Effective Agents** — engineering patterns and anti-patterns from practice.  
- OpenAI, **Practical Guide to Building Agents** — design guidance for tool-using systems.

---

## Summary

Agents combine an **LLM**, **tools**, **memory**, **state**, and a **control loop** to pursue goals that are not fully scripted in advance. They differ from chatbots (turn-centric), copilots (human-led), and workflows (deterministic orchestration). Start with the **simplest** autonomy level that works, and expand only when measurement shows a clear win.
