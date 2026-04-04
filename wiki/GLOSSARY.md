# Agent Factory Wiki -- Glossary

Concise definitions for vocabulary used across agent design, runtime, and operations. Terms appear in **bold** with an em dash before the definition.

**A2A Protocol** -- An interoperability pattern for agent-to-agent messaging and delegation so heterogeneous agents can exchange tasks and results with explicit contracts rather than ad hoc string passing.

**Agent** -- An LLM-driven system that iterates: it plans actions, invokes tools or APIs, observes outcomes, and continues until a stop condition, rather than answering in a single forward pass.

**AdaRubric** -- A task-adaptive evaluation framework (arXiv:2603.21362, 2026) that generates domain-specific rubrics for scoring LLM agent trajectories; uses a three-stage pipeline (Rubric Generator, Trajectory Evaluator, DimensionAwareFilter) achieving Pearson r=0.79 human correlation.

**Agent Loop** -- The core control cycle (observe context, decide, act via tools, update state) that repeats until completion, failure, or an external halt; quality depends on bounds, recovery, and observability on each iteration.

**Autoresearch** -- A self-improvement pattern (Karpathy, 2025-2026) where an LLM agent iteratively reads a living document (`program.md`), hypothesizes improvements, evaluates against an objective scorer, and keeps or discards changes autonomously within safety bounds.

**Behavioral Test** -- A test that validates agent behavior end-to-end: given an input scenario and tool stubs, assert on the sequence of actions, final output, or side effects rather than internal implementation details.

**Autonomous Loop** -- An agent loop that runs with minimal human intervention across many steps; risk scales with tool power, missing guardrails, and unclear stop conditions.

**Chain of Thought** -- Intermediate natural-language reasoning steps emitted before a final answer; improves reliability on some tasks but increases tokens and can leak reasoning you intended to keep internal.

**Checkpointing** -- Persisting durable snapshots of conversation state, tool outputs, and decisions so a run can resume, audit, or roll back after crashes or human review.

**Circuit Breaker** -- A pattern that stops calling a failing dependency (tool, API, model route) after thresholds are hit, failing fast instead of amplifying errors or cost.

**CLASSic Framework** -- A five-dimensional operational evaluation framework (Zylos Research, 2026) measuring agent production-readiness across Cost, Latency, Accuracy, Stability, and Security; grounded in 2,100+ real enterprise messages across 7 industry domains.

**Composability** -- Designing agents, tools, and sub-workflows as replaceable units with clear interfaces so you can assemble larger systems without rewriting core loops.

**Context Engineering** -- Deliberately curating what enters the model context (system prompt, retrieved docs, summaries, tool results) to maximize signal per token and slow **context rot**.

**Context Rot** -- Degradation of model behavior as the prompt fills with stale, redundant, or conflicting information; often fixed via summarization, pruning, and structured state outside the window.

**Context Window** -- The maximum tokens a model can attend to in one request; the hard constraint that drives summarization, retrieval, and multi-turn design.

**Copilot** -- An assistive model UX that suggests edits or answers inline while a human drives; contrast with a full **agent** that may act autonomously across many steps.

**CrewAI** -- A Python-oriented framework for role-based **multi-agent** collaboration (crews, tasks, tools); one of several options compared in **framework** discussions.

**Dead Letter Queue** -- A durable sink for tasks or tool jobs that failed beyond retry policy; enables inspection, replay, and alerting instead of silent loss.

**DimensionAwareFilter** -- A component of the **AdaRubric** pipeline that prevents high scores on one evaluation dimension from masking failures on another; uses harmonic mean aggregation and flags any dimension below threshold for mandatory remediation.

**Directed Graph** -- A workflow or state model where nodes are steps and edges are explicit transitions; contrasts with a free-form **agent loop** when you need guaranteed ordering.

**Embedding** -- A dense vector representation of text (or other modalities) used for similarity search, clustering, and retrieval alongside a **vector store**.

**Episodic Memory** -- Storage of concrete past interactions or events (sessions, decisions, outcomes), often for personalization and debugging, distinct from static **semantic memory**.

**Error Recovery** -- Policies and prompts for classifying failures, retrying with backoff, substituting **fallback** tools, surfacing errors to users, and preventing infinite loops.

**Evaluation** -- Systematic measurement of agent quality via offline datasets, online metrics, human rubrics, and trace-based checks; distinct from anecdotal prompting.

**Extended Thinking** -- Models or modes that allocate additional internal computation (often hidden) before responding; trades latency and cost for harder reasoning tasks.

**Fallback** -- A secondary path when the primary tool, model, or plan fails, such as a simpler tool, cached answer, or **human-in-the-loop** escalation.

**Fan-Out** -- Dispatching many parallel subtasks (to tools, workers, or sub-agents) from one decision; needs aggregation, **rate limiting**, and idempotency to stay safe.

**Feedback Loop** -- A cycle where agent outputs (traces, scores, user corrections) feed back into improving prompts, skills, tool policies, or retrieval—either within a session (online) or across sessions (offline batch).

**Framework** -- A library or platform that provides pre-built primitives for agent construction (loop management, tool routing, state, checkpointing), such as LangGraph, CrewAI, or OpenAI Agents SDK; trades flexibility for faster scaffolding.

**Function Calling** -- Structured invocation of named tools with JSON (or schema-conformant) arguments returned by the model; the standard bridge between LLMs and side effects.

**Guardrail** -- Policy, classifier, schema check, or allowlist that constrains inputs, outputs, or tool use to reduce abuse, leaks, and unsafe actions.

**Handoff** -- Transfer of control, state, and responsibility from one agent or process to another with an explicit payload and often a **human-in-the-loop** checkpoint.

**Harness** -- The non-model code that runs the **agent loop**: invokes the API, parses **structured output**, calls tools, enforces limits, and records **traces**.

**Harness Engineering** -- The discipline of building reliable harnesses: timeouts, retries, state machines, security boundaries, and test hooks around the model.

**Human-in-the-Loop** -- Explicit points where a person approves, corrects, or chooses among options before irreversible or high-risk actions proceed.

**Idempotent** -- An operation safe to repeat with the same effect as once, typically keyed so retries and duplicate model calls do not double-charge or double-write.

**Knowledge Graph** -- Entities and typed relations stored for structured reasoning and retrieval; complements **RAG** when facts are relational rather than textual chunks.

**LangGraph** -- A graph- and state-centric library (LangChain ecosystem) for building cyclical, checkpointable agent workflows with explicit nodes and edges.

**Long-Term Memory** -- Durable store outside the **context window** (database, vector index, graph) persisting user preferences, facts, or task history across sessions.

**MCP** -- Abbreviation for **Model Context Protocol**; see below.

**Memory Tier** -- Classification of memory by lifetime and purpose (e.g., working context, session summary, **long-term memory**) to decide what to load each turn.

**Meta-Agent** -- An agent whose job is to configure, route, or supervise other agents or prompts rather than executing every end-user task directly.

**Model Context Protocol** -- A standard for exposing tools, resources, and prompts to models via structured servers, reducing one-off integrations and easing **tool** discovery.

**Multi-Agent** -- Systems where several agents or roles collaborate, often with an **orchestrator**, **supervisor pattern**, or peer **routing**.

**Observability** -- Logs, metrics, and **traces** that make each model call and tool invocation inspectable in production for debugging, **evaluation**, and compliance.

**Orchestrator** -- A component that schedules subtasks, selects agents or tools, and merges results; may be implemented as code, another LLM, or a hybrid.

**Parallel Traces** -- Running N independent reasoning rollouts of the same task and aggregating results (majority vote, best-of-N, trace merge) to improve reliability at the cost of linear compute multiplication; distinct from Tree of Thoughts in that traces share no intermediate state.

**Persona** -- The role, tone, and behavioral constraints encoded in the **system prompt** or policy layer so the model acts consistently for a use case.

**Plan-Act-Observe-Reflect** -- A variant of the agent cycle emphasizing explicit planning, execution, observation of outcomes, and reflection before the next plan.

**Planning** -- Decomposing a goal into ordered steps or subgoals inside the model or in external code; pairs with **task decomposition** and **tool selection**.

**Program.md** -- A versioned artifact (often markdown) that holds the evolving system prompt, tool policies, evaluation hooks, and stop conditions for an agent; the unit of change in harness-driven optimization loops like AutoAgent.

**Prompt Injection** -- Attacks that embed instructions in untrusted content to override developer intent; mitigated with **guardrails**, tool allowlists, and separation of trusted vs untrusted text.

**RAG** -- Abbreviation for **Retrieval-Augmented Generation**; see below.

**Rate Limiting** -- Capping requests per time window, user, or tenant to protect budgets, APIs, and fairness under **autonomous loop** load.

**ReAct** -- Reasoning-and-acting pattern interleaving short reasoning traces with **tool** calls in the visible transcript; a common baseline **agent loop** style.

**Reflection** -- A step where the model critiques its own draft answer or plan and revises; can be single-turn or part of a larger loop.

**Reflexion** -- A pattern using verbal self-reflection and often stored hints from past failures to improve subsequent attempts on similar tasks.

**Retrieval-Augmented Generation** -- Grounding model outputs by retrieving relevant documents or records into context instead of relying only on parametric knowledge.

**Routing** -- Choosing which model, agent, or tool path handles a request based on intent, cost, or policy—static rules, classifiers, or LLM-based **tool routing**.

**Sandboxing** -- Running tools in isolated environments (containers, VMs, restricted APIs) so compromise or bugs do not reach production systems or secrets.

**Self-Improving Agent** -- Systems that update prompts, policies, or retrieval from **feedback loops** and **evaluation** signals; requires governance to avoid drift and unsafe learning.

**Semantic Memory** -- General factual or procedural knowledge stored in structured or vector form, not tied to a single session timeline.

**Short-Term Memory** -- In-context conversation and scratchpad content within the current **context window**; volatile unless **checkpointed** externally.

**State Machine** -- Explicit states and transitions governing when tools run and when the run ends; reduces ambiguity compared to a fully free-form loop.

**Stop Condition** -- The explicit rule or set of rules that terminates an agent loop: step caps, cost limits, user confirmation, task-complete signals, or timeout—without one, agents run forever or until they exhaust resources.

**Streaming** -- Emitting model tokens or events incrementally to clients for latency perception and progressive UI; the harness must still parse final **structured output** when required.

**Structured Output** -- Responses constrained to JSON, enums, or schemas via grammar or tooling so downstream code can parse without fragile natural-language scraping.

**Supervisor Pattern** -- A **multi-agent** layout where a supervisor delegates to workers, reviews outputs, and decides continuation—common for quality and **guardrails**.

**Swarm** -- Loosely coordinated collection of agents often with decentralized **routing**; contrast with a strict hierarchical **supervisor pattern**.

**System Prompt** -- The developer-facing instruction block that sets capabilities, policies, and format expectations for the model across turns.

**Task Decomposition** -- Breaking a user goal into smaller steps assignable to tools, humans, or sub-agents; central to **planning** and reliable completion.

**Tool** -- Any callable capability exposed to the model (API, script, search, DB) with a schema describing inputs and outputs.

**Tool Routing** -- Logic or model choice that picks which **tool** to invoke among alternatives, sometimes via classification or a planning pass.

**Trace** -- An ordered record of spans (model calls, tool I/O, latencies) for one run; core to **observability** and regression **evaluation**.

**Trace Aggregation** -- Merging results from **parallel traces** into a single output via voting, scoring, or structured merge; the aggregation strategy determines the quality-cost trade-off of parallel reasoning.

**Tree of Thoughts** -- Search-like expansion of multiple reasoning branches scored or pruned before a final choice; higher cost than single **chain of thought**.

**Vector Store** -- Database or index optimized for **embedding** similarity search, typically backing **RAG** pipelines.

**Workflow** -- Predetermined sequence (often a **directed graph**) of steps with fixed control flow; differs from a fully adaptive **agent** when flexibility and **tool** choice are minimal.
