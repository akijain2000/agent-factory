# Module 02: Agent Architectures

**Duration:** approximately 40 minutes  
**Prerequisites:** Module 01 (What Are Agents) or equivalent understanding of agent components and loops.

---

## Learning objectives

By the end of this module, you should be able to:

- Describe **single-agent**, **multi-agent**, and **hierarchical** architectures at a high level.
- Match architecture choices to **problem shape**, **team constraints**, and **risk**.
- Build a simple **architecture decision tree** for a new project.
- Recognize **case patterns** where a chosen architecture succeeded or failed.

---

## 1. Single agent: one LLM, one loop, focused tools

In the **single-agent** pattern, one model instance (or one logical “brain”) runs the main loop. It receives goals, selects tools, and iterates until completion or limits.

**Strengths**

- **Lower coordination overhead**: no inter-agent protocol, fewer failure modes from miscommunication.
- **Easier debugging**: one trace, one policy to tune.
- **Predictable cost profile**: one context budget and call pattern to optimize.

**Typical fit**

- Tasks that are **sequential** but not fully known in advance (research, coding assistance with tools, structured analysis).
- Teams early in agent adoption who need **observability** and iteration speed.

**Design discipline**

- Keep the **tool surface** coherent; avoid dozens of overlapping tools.
- Use **state** in the harness to reduce reliance on the model re-deriving facts every turn.

---

## 2. Multi-agent: multiple LLMs collaborating

**Multi-agent** systems assign **roles** to separate agents: researcher, writer, critic, planner, etc. They exchange messages, shared memory, or handoff artifacts.

**Strengths**

- **Parallelism**: explore alternatives or subtasks concurrently.
- **Separation of concerns**: different prompts, models, or tool sets per role.
- **Diversity of “opinion”**: critic vs proposer patterns can catch errors.

**Risks**

- **Duplicated work** or conflicting conclusions if coordination is weak.
- **Higher latency and cost** without clear benefit over one agent with good tools.
- **Debugging complexity**: failures may be social (protocol) not logical (single plan).

Use multi-agent when the problem **decomposes cleanly** into roles with **different tools or objectives**, not because the diagram looks impressive.

---

## 3. Hierarchical: supervisor + worker agents

**Hierarchical** architectures place a **supervisor** (or orchestrator) above **workers**. The supervisor assigns subgoals, aggregates results, and may retry or re-delegate.

Variants include:

- **Static hierarchy**: fixed roles (supervisor always delegates to the same worker types).
- **Dynamic delegation**: supervisor spawns or selects workers based on task type.

**Strengths**

- Scales to **heterogeneous** subtasks (code vs research vs formatting).
- Central place for **global constraints** (budget, allowed tools, compliance checks).

**Risks**

- **Supervisor bottleneck**: poor delegation prompts or weak worker specs tank the whole run.
- **Over-centralization**: supervisor context may balloon; workers may lack nuance.

Hierarchical designs often appear in **enterprise** settings where a single entry point must enforce policy even if work is distributed.

---

## 4. Architecture decision tree: how to choose

Use this sequence as a **default**; adapt to your compliance and latency needs.

1. **Can the task be a deterministic workflow?**  
   If yes, prefer **workflow** (or workflow + LLM in one step). Stop here.

2. **Is one loop with a focused toolset enough?**  
   If yes, start with a **single agent**. Instrument traces and evals before splitting.

3. **Do subtasks require different tools, models, or security boundaries?**  
   If yes, consider **multi-agent** or **hierarchical** delegation.

4. **Do you need parallel exploration or adversarial review?**  
   If yes, **multi-agent** (e.g., proposer + critic) may justify the complexity.

5. **Is there a mandatory policy gate between phases?**  
   If yes, **hierarchical** supervisor often maps to “approve before execute” naturally.

Document the **reason** you skipped simpler tiers. That document becomes your **architecture decision record** when the system grows.

---

## 5. Case studies: when each architecture was the right (and wrong) choice

**Single agent — right**  
Internal “ask the docs” assistant with search, read, and synthesize: one loop, clear tools, easy eval on answer quality and citations.

**Single agent — wrong**  
Trying to cram **unrelated** domains (finance + legal + IT) into one prompt and one undifferentiated tool dump: context noise and tool confusion dominate.

**Multi-agent — right**  
Research product where **two independent** retrieval strategies run in parallel and a merger step combines evidence—measurable lift over sequential single-agent.

**Multi-agent — wrong**  
Three agents that all call the same API in sequence “for quality,” without distinct roles: pure latency and cost increase.

**Hierarchical — right**  
Supervisor enforces **tool allowlists** and **human approval** before destructive actions; workers stay narrow.

**Hierarchical — wrong**  
Deep trees of supervisors for simple FAQs: each layer adds latency without reducing uncertainty.

---

## Exercises

### Exercise 1: Design an architecture for a given problem

Pick one scenario:

- A) On-call incident summarizer that pulls logs, tickets, and runbooks.  
- B) Marketing copy generator with brand guidelines and compliance checks.  
- C) Code migration assistant across two repositories.

For your choice, specify:

- **Architecture** (single / multi / hierarchical) and why.  
- **Agents** (if more than one): names, responsibilities, inputs, outputs.  
- **Critical risks** and **mitigations** (timeouts, fallbacks, human gates).

### Exercise 2: When to split a single agent

Describe a **hypothetical** single-agent system that is beginning to fail (high error rate, context bloat, or contradictory tool use). List **three signals** that would justify splitting into multiple agents or adding a supervisor—and **one signal** that would instead justify **better tools or prompts** without splitting.

---

## Further reading

- [Multi-agent orchestration (concept)](../wiki/concepts/multi-agent-orchestration.md) — patterns, handoffs, and platform concerns.  
- [Multi-agent landscape (research)](../wiki/research/multi-agent-landscape.md) — survey of approaches and tradeoffs.

---

## Summary

**Single-agent** architectures cover most production use cases when tools and state are well designed.**Multi-agent** and **hierarchical** layouts earn their complexity through **parallelism**, **role separation**, or **policy gates**—not through diagram aesthetics. Use a **decision tree** anchored in measurability: start simple, split only when evidence demands it.
