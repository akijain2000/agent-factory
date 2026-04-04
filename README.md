# Agent Factory

**An LLM knowledge base and course for building production-quality AI agents.**

Built on [Karpathy's LLM-KB pattern](https://x.com/karpathy/status/1909366683415642209): raw sources are collected from 40+ repositories and 25 reference documents, LLM-compiled into a structured wiki of 80+ articles, then queried by meta-skills to produce better agents. Sibling project to [Skill Factory](../skill-factory/), which teaches how to write the SKILL.md files that augment these agents.

```
            ┌──────────────────────────────────────────────────┐
            │          RAW SOURCES (40+ repos, 25 docs)        │
            │  Hermes, Paperclip, AutoAgent, ByteRover,        │
            │  LangGraph, CrewAI, OpenAI SDK, gstack, ...      │
            │  + papers (Weng, Yao, Shinn) + guides (Anthropic,│
            │    OpenAI, Ng) + protocol specs (MCP, A2A)       │
            └───────────────────────┬──────────────────────────┘
                                    │
                         compile-wiki.md (LLM)
                                    │
                                    ▼
            ┌──────────────────────────────────────────────────┐
            │           COMPILED WIKI (80+ articles)           │
            │  35 concepts · 20 research · 22 examples         │
            │  INDEX.md · GLOSSARY.md (67 terms) · query logs  │
            └───────────────────────┬──────────────────────────┘
                                    │
               authoring + agent-maker + prompt-decomposer
                                    │
                                    ▼
            ┌──────────────────────────────────────────────────┐
            │          NEW AGENTS (higher quality)             │
            │  Spec-validated · Production-ready · Tested      │
            │  Scored across 8 AGENT_SPEC dimensions           │
            └───────────────────────┬──────────────────────────┘
                                    │
                         health-check.md (audit loop)
                                    │
                                    ▼
                             Wiki improves ↺
```

---

## What This Is

This repo is six things:

1. **A knowledge base** -- 80+ wiki articles distilled from 40+ top AI agent repos (700K+ stars combined), covering every pattern, anti-pattern, and technique for building autonomous agents
2. **A 23-module course** -- Zero-to-production curriculum (~11-13 hours) with exercises, code examples, and framework walkthroughs across LangGraph, OpenAI Agents SDK, and Anthropic
3. **An Agent Maker** -- An interactive `agent-maker/SKILL.md` that asks 6 forcing questions, challenges assumptions, and guides you through 8 phases from idea to validated agent
4. **A Prompt Decomposer** -- A `prompt-decomposer/SKILL.md` that takes a large prompt, codebase, or system description and identifies sections that could become agent components
5. **A meta-skill** -- An `authoring/SKILL.md` that queries the wiki to help you review, score, and improve existing agents against the AGENT_SPEC quality standard
6. **A quality standard** -- `AGENT_SPEC.md` defines 8 dimensions for scoring agent projects, with a canonical project structure and minimum quality bar

## Why This Exists

Building a production agent is harder than it looks. Most agents fail at architecture (no clear loop or state management), tools (too many, poorly described, no error handling), safety (no guardrails, no sandbox, no approval gates), or testing (no behavioral tests, no trace analysis, no baselines).

This project codifies what works and what doesn't, drawn from analyzing the architectures and patterns of 40+ real agent systems across the ecosystem -- from OpenClaw (344K stars) to AutoAgent (714 stars). It covers the full spectrum: single-agent tools, multi-agent orchestration, self-improving harness loops, protocol interoperability, and production deployment.

**The key insight:** Skills augment agents. Agents are the autonomous systems themselves. Skill Factory teaches you to write `SKILL.md` files. Agent Factory teaches you to build the agent that reads them.

---

## Directory Structure

```
agent-factory/
├── SKILL.md                     # Entry point: A/B/C/D concierge router
├── AGENT_SPEC.md                # Quality standard (8 dimensions, scoring guide)
├── README.md                    # You are here
│
├── agent-maker/                 # Interactive agent creator
│   └── SKILL.md                 # 8-phase guided creation with forcing questions
│
├── authoring/                   # The review meta-skill
│   └── SKILL.md                 # Wiki-backed agent review and improvement
│
├── prompt-decomposer/           # System-to-agents extractor
│   └── SKILL.md                 # Analyze prompts/codebases, suggest agent components
│
├── course/                      # 23-module agent building course
│   ├── README.md                # Course overview and learning path
│   ├── 01-what-are-agents.md    # Foundation: agents vs chatbots vs copilots
│   ├── 02-agent-architectures.md # Single, multi-agent, hierarchical
│   ├── 03-the-agent-loop.md     # Plan-act-observe-reflect, ReAct pattern
│   ├── 04-system-prompts-for-agents.md # Persona, constraints, tool instructions
│   ├── 05-tool-design-and-integration.md # Function calling, MCP, structured I/O
│   ├── 06-memory-and-context-engineering.md # Memory types, context rot, ByteRover
│   ├── 07-planning-and-reasoning.md # CoT, ToT, task decomposition, AutoAgent
│   ├── 08-error-handling-and-recovery.md # Retries, fallbacks, circuit breakers, Hermes
│   ├── 09-agent-design-patterns.md # Ng's 4 patterns, ReAct, Reflexion
│   ├── 10-multi-agent-patterns.md # Supervisor, pipeline, swarm, Paperclip
│   ├── 11-anti-patterns.md      # God agent, over-tooling, premature autonomy
│   ├── 12-state-management.md   # Checkpointing, persistence, git-as-memory
│   ├── 13-framework-selection.md # Decision matrix: LangGraph vs CrewAI vs SDK
│   ├── 14-building-with-langgraph.md # State graphs, persistence, human-in-the-loop
│   ├── 15-building-with-openai-agents-sdk.md # Agent class, handoffs, guardrails
│   ├── 16-building-with-anthropic.md # Tool use, extended thinking, computer use
│   ├── 17-agent-evaluation-and-testing.md # Behavioral tests, benchmarks, A/B testing
│   ├── 18-safety-and-guardrails.md # Sandboxing, prompt injection, approval gates
│   ├── 19-observability-and-debugging.md # Tracing, cost tracking, debugging long runs
│   ├── 20-deployment-and-scaling.md # Serverless vs containers, rate limits, scaling
│   ├── 21-protocols-and-interoperability.md # MCP servers, A2A, tool marketplaces
│   ├── 22-self-improvement-and-harness-engineering.md # Learning loops, harnesses
│   └── 23-capstone-build-a-production-agent.md # End-to-end project (3 tracks)
│
├── wiki/                        # LLM-compiled knowledge base
│   ├── INDEX.md                 # Master table of contents (start here)
│   ├── GLOSSARY.md              # 67 terms with definitions
│   ├── concepts/                # 35 core agent-building concept articles
│   │   ├── agent-loop.md
│   │   ├── tool-design.md
│   │   ├── memory-systems.md
│   │   ├── context-engineering.md
│   │   ├── harness-engineering.md
│   │   ├── self-improving-agents.md
│   │   ├── autonomous-loops.md
│   │   └── ... (28 more)
│   ├── research/                # 23 ecosystem analysis and deep-dive articles + 3 raw data files
│   │   ├── hermes-agent-deep-dive.md
│   │   ├── paperclip-orchestration-analysis.md
│   │   ├── autoagent-harness-patterns.md
│   │   ├── context-memory-architecture.md
│   │   ├── openclaw-scale-analysis.md
│   │   ├── framework-comparison.md
│   │   └── ... (14 more)
│   ├── examples/
│   │   ├── good/                # 14 exemplary agents with annotations
│   │   └── bad/                 # 8 anti-pattern agents with analysis
│   └── queries/                 # Filed Q&A and update logs
│
├── scripts/                     # Automation
│   ├── validate-agent.ts        # Automated agent project linter (Bun/Node)
│   ├── compile-wiki.md          # LLM instructions: compile raw/ into wiki/
│   ├── health-check.md          # LLM instructions: audit wiki quality
│   ├── update-sources.md        # LLM instructions: monthly discovery + update
│   └── discovery-keywords.txt   # Keywords for finding new agent repos
│
└── raw/                         # Source material
    ├── docs/
    │   └── SOURCES.md           # 25 reference documents (URLs + summaries)
    └── repos/
        └── SOURCES.md           # 40+ repo manifest with tiers and descriptions
```

---

## Quick Start

**Tell your AI agent to read `SKILL.md` in this repo.** It will ask what you want to do:

- **A) Review and improve an existing agent** -- guided brainstorm review or quick AGENT_SPEC report
- **B) Brainstorm and create a new agent** -- interactive 8-phase Agent Maker with forcing questions
- **C) Learn about agent building** -- 23-module course or wiki browsing
- **D) Extract agent components from a codebase/prompt** -- decompose into modules

Or jump directly:

```
# Review an agent
Read SKILL.md and help me review my agent at path/to/my-agent/

# Create an agent
Read agent-maker/SKILL.md and help me create an agent for [your idea]

# Break a system into agents
Read prompt-decomposer/SKILL.md and analyze this prompt for agent components

# Take the course
Read course/README.md
```

### Additional tools

**Validate an agent project:**

```bash
bun scripts/validate-agent.ts path/to/your-agent/
```

Checks: README exists with architecture section, system prompt file present, tool definitions exist, tests directory non-empty, no committed secrets, system prompt has persona/constraints/tool instructions.

**Compile the wiki** (after adding new sources):

```
Read scripts/compile-wiki.md and compile the wiki.
```

**Run a health check:**

```
Read scripts/health-check.md and run a health check.
```

---

## Course Overview

The [course/](course/) directory contains a 23-module curriculum organized in 6 blocks, from "what is an agent?" to shipping a production agent. Each module has learning objectives, content sections with code examples, exercises, and further reading that links into the wiki.

### Block 1: Foundations (Modules 01-04, ~2.5 hours)

| # | Module | Time | What You Learn |
|---|--------|------|----------------|
| 01 | What Are Agents | 30 min | Agents vs chatbots vs copilots vs workflows; anatomy of an agent; the autonomy spectrum |
| 02 | Agent Architectures | 40 min | Single, multi-agent, hierarchical; architecture decision tree; case studies |
| 03 | The Agent Loop | 40 min | Plan-act-observe-reflect; ReAct pattern dissected; state machines vs free-form; loop termination |
| 04 | System Prompts for Agents | 30 min | Persona + constraints + tool instructions + guardrails; how agent prompts differ from chat prompts |

### Block 2: Core Building Blocks (Modules 05-08, ~2.5 hours)

| # | Module | Time | What You Learn |
|---|--------|------|----------------|
| 05 | Tool Design and Integration | 45 min | Function calling schemas, MCP servers, tool routing, error handling; gstack + Composio patterns |
| 06 | Memory and Context Engineering | 45 min | Short-term/long-term/episodic/semantic memory; RAG for agents; context rot (Willison); ByteRover's context tree (96%+ LoCoMo) |
| 07 | Planning and Reasoning | 40 min | Chain of Thought, Tree of Thoughts, task decomposition; AutoAgent's program.md as planning interface |
| 08 | Error Handling and Recovery | 30 min | Retries with backoff, fallback chains, circuit breakers, dead letter queues; Hermes Agent's fallback provider chains |

### Block 3: Patterns and Anti-Patterns (Modules 09-12, ~2.5 hours)

| # | Module | Time | What You Learn |
|---|--------|------|----------------|
| 09 | Agent Design Patterns | 45 min | Andrew Ng's 4 patterns (reflection, tool use, planning, multi-agent); ReAct and Reflexion deep dives; neural-maze implementations |
| 10 | Multi-Agent Patterns | 45 min | Supervisor, sequential, parallel, swarm, debate; Paperclip's team orchestration; CrewAI roles; Swarm handoffs |
| 11 | Anti-Patterns | 35 min | God agent, over-tooling, premature multi-agent, context abuse, sycophantic loops, premature autonomy; AutoGPT lessons |
| 12 | State Management | 35 min | Checkpointing, persistence, conversation threading, context window management; LangGraph checkpointing; Ralph's git-as-memory |

### Block 4: Frameworks (Modules 13-16, ~2.5 hours)

| # | Module | Time | What You Learn |
|---|--------|------|----------------|
| 13 | Framework Selection | 30 min | Decision matrix: LangGraph vs CrewAI vs OpenAI Agents SDK vs Anthropic vs raw API; when to go framework-free |
| 14 | Building with LangGraph | 45 min | State machines as directed graphs, persistence, human-in-the-loop, streaming; building a research agent |
| 15 | Building with OpenAI Agents SDK | 45 min | Agent class, handoffs, guardrails, tracing, MCP integration; building a customer service agent |
| 16 | Building with Anthropic | 45 min | Tool use, extended thinking, computer use, orchestrator-workers; building a code analysis agent |

### Block 5: Production (Modules 17-20, ~2.5 hours)

| # | Module | Time | What You Learn |
|---|--------|------|----------------|
| 17 | Agent Evaluation and Testing | 40 min | Behavioral tests, trace analysis, benchmarks (SWE-Bench, HumanEval), compliance scoring, A/B testing; AutoAgent's hill-climbing |
| 18 | Safety and Guardrails | 40 min | Sandboxing (Docker, e2b), prompt injection defense, approval gates, confidence thresholds; OpenClaw's permissions |
| 19 | Observability and Debugging | 35 min | Tracing (LangSmith, Braintrust), cost tracking, debugging 50-step traces; Paperclip's cost dashboard; LiteLLM |
| 20 | Deployment and Scaling | 35 min | Serverless vs containers vs edge, rate limiting, cost optimization at scale; Hermes Agent's VPS-to-GPU range |

### Block 6: Mastery (Modules 21-23, ~2.5 hours)

| # | Module | Time | What You Learn |
|---|--------|------|----------------|
| 21 | Protocols and Interoperability | 40 min | MCP server authoring, A2A communication, tool marketplaces, cross-org agent composition |
| 22 | Self-Improvement and Harness Engineering | 45 min | Learning loops, skill creation from experience, score-driven hill-climbing, self-modifying agents; AutoAgent, Hermes, Ouroboros |
| 23 | Capstone: Build a Production Agent | 60 min | End-to-end project. Track A: coding assistant. Track B: multi-agent research team. Track C: self-improving agent with harness |

---

## What the Wiki Covers

### Core Concepts (35 articles)

| Category | Articles | What You Learn |
|----------|----------|----------------|
| **Agent Core** | agent-loop, planning-strategies, state-management, agent-lifecycle | The fundamental cycle, how agents plan and persist, lifecycle from prototype to production |
| **Tools** | tool-design, tool-selection, structured-outputs | Building tools agents can use effectively; routing; schema enforcement (Pydantic, Zod) |
| **Memory** | memory-systems, agent-memory-patterns, context-window-management, context-engineering | Short/long/episodic/semantic memory; scratchpad vs RAG vs knowledge base; Lutke/Karpathy context engineering; Willison's context rot |
| **Safety** | guardrails, human-in-the-loop, sandboxing, agent-security | Input validation, approval gates, Docker/e2b isolation, prompt injection defense, least privilege |
| **Multi-Agent** | multi-agent-orchestration, agent-handoffs, agent-orchestration-platforms | Supervisor/pipeline/fan-out/swarm; clean handoffs; Paperclip-style team management |
| **Production** | error-recovery, observability, cost-optimization, deployment-patterns, rate-limiting | Retries, circuit breakers; tracing; token budgets; serverless vs containers; backpressure |
| **Design** | prompt-engineering-for-agents, agent-personas, progressive-complexity, agent-composition, model-selection, agent-ux | System prompt design; role identity; start simple; modular agents; cost/quality tradeoffs; streaming UX |
| **Testing** | feedback-loops, agent-evaluation, agent-testing-patterns | Reflection, Reflexion, critic agents; behavioral tests; unit/integration/trace-based testing |
| **Advanced** | harness-engineering, self-improving-agents, autonomous-loops | Meta-agent control structures; learning from experience; score-driven hill-climbing; self-modifying agents |

### Research (23 deep dives + 3 raw data files)

| Article | What You Learn |
|---------|----------------|
| anatomy-of-a-good-agent | What makes an agent production-quality: architecture clarity, error handling, testing, docs |
| anti-patterns | Comprehensive catalog: god agent, over-tooling, premature multi-agent, context abuse, and more |
| framework-comparison | LangGraph vs CrewAI vs OpenAI SDK vs Anthropic vs AutoGen: architecture, strengths, maturity |
| andrew-ng-patterns | Deep dive into reflection, tool use, planning, multi-agent collaboration with implementations |
| lilian-weng-survey | Analysis of the foundational "LLM Powered Autonomous Agents" survey; what changed since |
| anthropic-agent-patterns | "Building Effective Agents" dissected: workflows before agents, prompt chaining, orchestrator-workers |
| openai-agent-patterns | OpenAI's guide + Agents SDK patterns: handoffs, guardrails, tracing |
| mcp-deep-dive | Model Context Protocol architecture: servers, clients, tools, resources, sampling |
| a2a-deep-dive | Agent-to-Agent protocol: cross-framework communication, task delegation |
| multi-agent-landscape | Survey of multi-agent approaches 2024-2026: what works and what doesn't |
| agent-evaluation-methods | How to evaluate agents: behavioral tests, trace analysis, SWE-Bench, LLM-as-judge |
| production-case-studies | Real-world agents in production: gstack, Cursor, Devin, customer service |
| gstack-agent-analysis | Browse daemon, QA skill, ship workflow: how production skills compose into an agent |
| agent-vs-workflow | When to use an agent vs a deterministic workflow: decision framework |
| cost-analysis | Economics of running agents: token costs, model selection, caching ROI |
| hermes-agent-deep-dive | Self-improving agent with learning loop, persistent skills, multi-platform, fallback chains |
| paperclip-orchestration-analysis | Zero-human company orchestration: agent teams, goal assignment, cost tracking |
| autoagent-harness-patterns | program.md as human interface, meta-agent hill-climbing, Docker isolation |
| context-memory-architecture | ByteRover's context tree, knowledge storage, 96%+ LoCoMo accuracy |
| openclaw-scale-analysis | Architecture of the 344K-star agent project: multi-channel, autonomous coding at scale |
| classic-framework | CLASSic operational evaluation: Cost, Latency, Accuracy, Stability, Security across 2,100+ enterprise messages |
| adarubric-evaluation | AdaRubric task-adaptive evaluation: 3-stage pipeline, Pearson r=0.79 human correlation, DPO training gains |
| karpathy-autoresearch | Autoresearch self-improvement pattern: program.md + objective scorer, 700 experiments, 11% training loss improvement |

### Curated Examples (22 annotated)

**14 good examples** with detailed annotations explaining what makes each one work:

| Example | Pattern | Key Takeaway |
|---------|---------|--------------|
| LangGraph ReAct Agent | State machine + tool loop | Explicit state transitions, clean tool routing |
| CrewAI Research Team | Role-based multi-agent | Clean role separation, sequential pipeline |
| OpenAI Agents Customer Service | Handoff architecture | Triage -> specialist handoffs with guardrails |
| gstack Browse Daemon | Focused tool agent | Structured output, diff-based verification |
| Anthropic Computer Use | Progressive capability | Screen reading with safety gates |
| Goose Extensible Agent | Plugin architecture | Composition over monolith |
| phidata Knowledge Agent | RAG pipeline agent | Clean memory pattern, focused retrieval |
| Simple Function Calling | Minimal agent | 20 lines, simplest possible agent loop |
| MCP Tool Server | Protocol-based tools | Framework-agnostic, composable |
| Multi-Agent Code Review | Parallel fan-out | Linter + security + style agents, structured aggregation |
| Hermes Self-Improving | Learning loop | Skills from experience, promotion criteria |
| Paperclip Agent Team | Orchestration platform | Goal assignment, cost tracking, agent-as-employee |
| AutoAgent Harness Loop | Meta-agent optimization | program.md + benchmarks + hill-climbing |
| Ralph PRD Completion | Autonomous build loop | Git as memory, iterative building, test verification |

**8 anti-pattern examples** showing exactly what goes wrong:

| Anti-Pattern | What Fails | Root Cause |
|-------------|-----------|------------|
| God Agent | Tool confusion, context overflow, untestable | 50+ tools, 5000-token prompt, no specialization |
| Over-Tooled Agent | Decision paralysis, wrong tool selection | 100+ overlapping tools, LLM can't choose |
| Chatbot Pretending to Be Agent | No agency, no tools, no loop | Just a chatbot with a fancy system prompt |
| Framework Soup | Conflicting abstractions, maintenance nightmare | LangGraph AND CrewAI AND AutoGen in one project |
| No-Guardrails Agent | Deletes production database | Full system access, no sandbox, no approval |
| Infinite Loop Agent | Cost explosion, no recovery | No circuit breaker, no max iterations, no fallback |
| Context-Stuffing Agent | Context rot, high cost, poor performance | Dumps entire codebase into 200K context window |
| Premature Autonomy Agent | Unauthorized purchases, emails, data modification | Full autonomy before guardrails exist |

---

## Key Discoveries

Patterns and insights identified across the 40+ source repos:

1. **Context Engineering > Prompt Engineering** -- Tobi Lutke (Shopify CEO) coined "context engineering" as the real skill: curating the information environment an LLM operates in, not just writing prompts. Karpathy endorsed this shift. Source: Lutke tweets, Karpathy commentary (2025-2026).

2. **Context Rot** -- Simon Willison identified 4 patterns of context degradation in long-running agents: poisoning (wrong info injected), distraction (irrelevant context competing), confusion (conflicting instructions), clash (sessions bleeding together). Source: simonwillison.net.

3. **Harness Engineering** -- Kevin Gu's AutoAgent showed that you can "program the meta-agent, not the harness": write a `program.md` that specifies behavior, then let a meta-agent modify it, benchmark the result, and hill-climb on scores. The agent optimizes itself. Source: kevinrgu/autoagent.

4. **Workflows Before Agents** -- Anthropic's "Building Effective Agents" guide advocates starting with augmented LLMs, moving to workflows (prompt chaining, routing, parallelization), and only using agents when you need the full loop. Most teams over-agent. Source: anthropic.com.

5. **Andrew Ng's 4 Patterns** -- Reflection, tool use, planning, and multi-agent collaboration. These four patterns transform an LLM from a single-shot generator into an agentic system. Each has a distinct implementation shape. Source: deeplearning.ai/the-batch.

6. **Self-Improving Agents** -- Hermes Agent (Nous Research) learns from interactions, creates new skills autonomously, and maintains persistent knowledge across sessions. The learning loop is: interact -> evaluate -> extract skill -> promote to permanent. Source: NousResearch/hermes-agent.

7. **Git as Memory** -- Ralph uses git as the agent's memory store: commit state, branch for exploration, diff for comparison, log for history. Simple, auditable, already in every developer's workflow. Source: snarktank/ralph.

8. **Agent-as-Employee** -- Paperclip treats agents as employees in a "zero-human company": assign goals, track costs, manage performance, provide skills library. The orchestration layer is a React dashboard. Source: paperclipai/paperclip.

9. **Context Tree Architecture** -- ByteRover builds a hierarchical context tree for coding agents that achieves 96%+ accuracy on the LoCoMo long-context benchmark. Portable memory with cloud sync across 20+ LLM providers. Source: campfirein/byterover-cli.

10. **The Progressive Complexity Trap** -- The #1 anti-pattern is premature multi-agent: adding agents when a single agent with better tools would suffice. Start with the simplest thing that could work. Source: Anthropic, confirmed across AutoGPT's evolution.

11. **Micro-Agents** -- Some agents are 20 lines of code. The LLM already knows HOW to do things -- it just needs the loop, tools, and guardrails. Don't over-engineer the first version. Source: OpenAI Swarm (educational), mattpocock/skills pattern.

12. **Compliance Measurement** -- Don't hope your agent works, measure it. Generate behavioral specs, run scenarios, capture traces, classify adherence. AutoAgent takes this further with score-driven hill-climbing: the meta-agent modifies itself until benchmarks improve. Source: kevinrgu/autoagent.

13. **CLASSic Framework for Operational Evaluation** -- The CLASSic framework (Zylos Research, 2026) evaluates agents across 5 production-readiness dimensions: Cost, Latency, Accuracy, Stability, Security. Grounded in 2,100+ enterprise messages across 7 industry domains. Key finding: agents that ace behavioral tests can score ≤3/10 on Cost, making them unshippable. Source: [wiki/research/classic-framework.md](wiki/research/classic-framework.md).

14. **AdaRubric: Task-Adaptive Evaluation** -- Fixed rubrics fail because different agent domains need different quality dimensions. AdaRubric (arXiv:2603.21362) generates task-specific rubrics achieving Pearson r=0.79 human correlation. The DimensionAwareFilter prevents high aggregate scores from masking critical per-dimension failures. Source: [wiki/research/adarubric-evaluation.md](wiki/research/adarubric-evaluation.md).

15. **Karpathy Autoresearch Pattern** -- The autoresearch pattern (Karpathy, 2025-2026) formalizes score-driven self-improvement: `program.md` + objective scorer + minimal diffs + automatic revert. 700 experiments in 2 days, 11% training loss improvement on NanoGPT. Generalizes beyond ML to prompt engineering, code optimization, and factory quality improvement. Source: [github.com/karpathy/autoresearch](https://github.com/karpathy/autoresearch), [wiki/research/karpathy-autoresearch.md](wiki/research/karpathy-autoresearch.md).

---

## Source Repositories Analyzed

40+ repositories organized into 7 tiers, totaling 700K+ GitHub stars:

### Tier 1: Major Agent Systems (analyze deeply)

| Repo | Stars | Key Contribution |
|------|-------|-----------------|
| [openclaw/openclaw](https://github.com/openclaw/openclaw) | 344K | Most-starred agent project. Multi-channel personal AI, autonomous coding at scale |
| [significantgravitas/AutoGPT](https://github.com/significantgravitas/AutoGPT) | 177K | Pioneer autonomous agent. Lessons from autonomous loops and their limitations |
| [paperclipai/paperclip](https://github.com/paperclipai/paperclip) | 45K | "Zero-human company" orchestration. Agent teams, goal assignment, cost tracking |
| [NousResearch/hermes-agent](https://github.com/NousResearch/hermes-agent) | 23K | Self-improving agent with learning loop. Persistent skills, multi-platform |

### Tier 2: Frameworks (analyze architecture patterns)

| Repo | Stars | Key Contribution |
|------|-------|-----------------|
| [crewaiInc/crewAI](https://github.com/crewaiInc/crewAI) | 44K | Role-based multi-agent with YAML config. Fastest to prototype |
| [langchain-ai/langgraph](https://github.com/langchain-ai/langgraph) | 25K | Directed graph state machines. Production-grade persistence, human-in-the-loop |
| [openai/openai-agents-python](https://github.com/openai/openai-agents-python) | 19K | Handoff-based architecture, native MCP, guardrails, tracing |
| [google/adk-python](https://github.com/google/adk-python) | 18K | Google's Agent Development Kit. Multimodal, hierarchical orchestration |
| [microsoft/autogen](https://github.com/microsoft/autogen) | -- | AG2. Pioneered multi-agent conversation patterns |
| [openai/swarm](https://github.com/openai/swarm) | -- | Lightweight multi-agent handoff patterns (educational) |
| [pydantic/pydantic-ai](https://github.com/pydantic/pydantic-ai) | -- | Type-safe agent framework on Pydantic |
| [huggingface/smolagents](https://github.com/huggingface/smolagents) | -- | Minimal agent framework from HuggingFace |

### Tier 3: Agent Optimizers and Harness Engineering

| Repo | Stars | Key Contribution |
|------|-------|-----------------|
| [campfirein/byterover-cli](https://github.com/campfirein/byterover-cli) | 3.8K | Context tree, knowledge storage, cloud sync, 96%+ LoCoMo accuracy |
| [kevinrgu/autoagent](https://github.com/kevinrgu/autoagent) | 714 | program.md as planning interface, meta-agent hill-climbing, Docker isolation |
| [greyhaven-ai/autocontext](https://github.com/greyhaven-ai/autocontext) | 679 | Recursive self-improving harness for agents |
| [cobusgreyling/ai_harness_engineering](https://github.com/cobusgreyling/ai_harness_engineering) | -- | Complete harness engineering implementation |
| [walkinglabs/awesome-harness-engineering](https://github.com/walkinglabs/awesome-harness-engineering) | -- | Curated harness engineering tools and guides |

### Tier 4: Autonomous Coding Agents

| Repo | Stars | Key Contribution |
|------|-------|-----------------|
| [snarktank/ralph](https://github.com/snarktank/ralph) | 14K | Autonomous PRD completion loop. Git as memory store |
| [AndyMik90/Aperant](https://github.com/AndyMik90/Aperant) | 13K | Multi-agent coding framework: plans, builds, validates automatically |
| [block/goose](https://github.com/block/goose) | -- | Extensible agent with plugin architecture |
| [garrytan/gstack](https://github.com/garrytan/gstack) | -- | Production agent skills: browse, QA, ship, deploy |
| [razzant/ouroboros](https://github.com/razzant/ouroboros) | 457 | Self-modifying agent that writes its own code |

### Tier 5: Protocols and Infrastructure

| Repo | Stars | Key Contribution |
|------|-------|-----------------|
| [modelcontextprotocol/servers](https://github.com/modelcontextprotocol/servers) | -- | MCP reference server implementations |
| [a2aproject/A2A](https://github.com/a2aproject/A2A) | -- | Agent-to-Agent protocol specification |
| [e2b-dev/e2b](https://github.com/e2b-dev/e2b) | -- | Sandboxed code execution for agents |
| [BerriAI/litellm](https://github.com/BerriAI/litellm) | -- | Unified LLM API gateway |
| [composiodev/composio](https://github.com/composiodev/composio) | -- | Tool integration platform for agents |
| [vercel/ai](https://github.com/vercel/ai) | -- | AI SDK with streaming and tool support |

### Tier 6 & 7: Tools, Capabilities, and Learning

Browser automation (Stagehand), web scraping (Firecrawl), knowledge agents (phidata), RAG frameworks (LlamaIndex), Andrew Ng's patterns implemented (neural-maze/agentic_patterns), Anthropic and OpenAI cookbooks, Anthropic courses, and curated awesome lists.

Full manifest with descriptions: [raw/repos/SOURCES.md](raw/repos/SOURCES.md)

---

## Reference Documents (25)

In addition to repos, 25 reference documents are indexed in [raw/docs/SOURCES.md](raw/docs/SOURCES.md):

### Research Papers and Surveys

| Document | Author | Key Contribution |
|----------|--------|-----------------|
| LLM Powered Autonomous Agents | Lilian Weng | Foundational survey: planning, memory, tool use for agents |
| ReAct: Synergizing Reasoning and Acting | Shunyu Yao et al. | The ReAct pattern: interleaved reasoning traces and actions |
| Reflexion: Verbal Reinforcement Learning | Noah Shinn et al. | Agents that reflect on failures and improve over attempts |
| Google "Agents" White Paper | Google DeepMind | Agent types, orchestration, evaluation |

### Industry Guides

| Document | Author | Key Contribution |
|----------|--------|-----------------|
| Building Effective Agents | Anthropic | Workflows before agents; prompt chaining, routing, parallelization, orchestrator-workers |
| Harness Design for Long-Running Apps | Anthropic Engineering | Production harness: error handling, context management, state persistence |
| A Practical Guide to Building Agents | OpenAI | Step-by-step: when to use agents, design foundations, guardrails |
| 4 Agentic Design Patterns | Andrew Ng | Reflection, tool use, planning, multi-agent collaboration |
| Context Engineering | Tobi Lutke / Karpathy | Curating the information environment, shift from prompt engineering |
| Context Rot Patterns | Simon Willison | Poisoning, distraction, confusion, clash in long-running agents |

### Framework, Protocol, and Agent-Specific Docs

MCP specification, A2A specification, OpenAI Agents SDK docs, LangGraph docs, CrewAI docs, Anthropic tool use + extended thinking docs, AutoAgent's program.md pattern, ByteRover's context memory architecture, Hermes Agent architecture, Paperclip orchestration docs.

---

## Key People Referenced

| Person | Contribution | Referenced In |
|--------|-------------|---------------|
| **Andrej Karpathy** | LLM-KB pattern (this project's architecture), context engineering | SKILL.md, README, course/06 |
| **Andrew Ng** | 4 agentic design patterns: reflection, tool use, planning, multi-agent | course/09, wiki/research/andrew-ng-patterns |
| **Lilian Weng** | "LLM Powered Autonomous Agents" survey (planning, memory, tools) | course/01, wiki/research/lilian-weng-survey |
| **Shunyu Yao** | ReAct paper: reasoning + acting interleaved | course/03, course/09, wiki/concepts/agent-loop |
| **Noah Shinn** | Reflexion: self-improvement through verbal feedback | course/09, wiki/concepts/self-improving-agents |
| **Tobi Lutke** | Coined "context engineering" as the core AI skill | course/06, wiki/concepts/context-engineering |
| **Simon Willison** | Context rot patterns: poisoning, distraction, confusion, clash | course/06, wiki/concepts/context-engineering |
| **Harrison Chase** | LangGraph: agent state machines, persistence, graph-based control flow | course/14, wiki/research/framework-comparison |
| **Joao Moura** | CrewAI: role-based multi-agent design, crew orchestration | course/10, wiki/research/multi-agent-landscape |
| **Kevin Gu** | AutoAgent: harness engineering, program.md, meta-agent hill-climbing | course/22, wiki/research/autoagent-harness-patterns |
| **Garry Tan** | gstack: production agent skills (browse, QA, ship, deploy workflows) | course/05, wiki/research/gstack-agent-analysis |
| **Nous Research team** | Hermes Agent: self-improving agent, learning loop, persistent skills | course/22, wiki/research/hermes-agent-deep-dive |
| **Paperclip team** | Multi-agent orchestration platform, "zero-human company" | course/10, wiki/research/paperclip-orchestration-analysis |
| **ByteRover team** | Context tree architecture, portable memory, 96%+ LoCoMo | course/06, wiki/research/context-memory-architecture |

---

## Quality Standard (AGENT_SPEC.md)

Agent projects are evaluated against [AGENT_SPEC.md](AGENT_SPEC.md) across 8 dimensions, each scored 0-10:

| Dimension | What a 10 looks like |
|-----------|---------------------|
| **1. Architecture** | Clear agent loop, defined tools, state management, explicit stop conditions, documented control flow |
| **2. System Prompt** | Persona, constraints, tool instructions, behavioral guardrails, all in a dedicated file |
| **3. Tool Design** | Structured I/O schemas, error handling, timeouts, clear descriptions, bounded tool set |
| **4. Memory** | Appropriate memory type, no context abuse, compaction strategy, persistence where needed |
| **5. Safety** | Sandboxing, prompt injection defense, human-in-the-loop for high-risk, least privilege |
| **6. Testing** | Behavioral tests, trace analysis, baseline comparison, edge case coverage |
| **7. Observability** | Tracing, structured logging, cost tracking, alerting on anomalies |
| **8. Documentation** | Architecture diagram, tool catalog, deployment guide, quickstart |

**Minimum viable score:** 5/10 average across all dimensions, no single dimension below 3/10.

### Canonical agent project structure

```
my-agent/
├── README.md                # What it does, how to run, architecture diagram
├── system-prompt.md         # The agent's core instructions
├── tools/                   # Tool definitions (function schemas, MCP servers)
├── src/                     # Agent logic (loop, state, orchestration)
├── tests/                   # Behavioral test cases
└── deploy/                  # Deployment configuration
```

---

## Scripts

| Script | Purpose | Usage |
|--------|---------|-------|
| `validate-agent.ts` | Lint agent projects against AGENT_SPEC | `bun scripts/validate-agent.ts /path/to/agent` |
| `compile-wiki.md` | LLM runbook: compile raw sources into wiki articles | `Read scripts/compile-wiki.md` |
| `health-check.md` | LLM runbook: audit wiki for quality, staleness, orphans | `Read scripts/health-check.md` |
| `update-sources.md` | LLM runbook: discover and integrate new repos/docs | `Read scripts/update-sources.md` |
| `discovery-keywords.txt` | 24 search phrases for finding new agent repos | Used by update-sources.md |

### Monthly Auto-Updates

The knowledge base auto-discovers new repos and recompiles the wiki.

**To run:**

```
Read scripts/update-sources.md and run the monthly update.
```

**What it does:**

1. Searches GitHub using `discovery-keywords.txt` phrases
2. Filters for AI agent repos by relevance
3. Scores candidates and keeps high-quality ones
4. Updates raw/repos/SOURCES.md
5. Incrementally recompiles affected wiki articles
6. Regenerates INDEX.md and GLOSSARY.md
7. Logs everything to wiki/queries/

---

## Architecture: The Karpathy Pattern

This project implements the LLM Knowledge Base pattern described by [Andrej Karpathy](https://x.com/karpathy/status/1909366683415642209):

1. **Raw data ingest** -- Curate repos, save reference doc URLs, capture specs into `raw/`
2. **LLM compilation** -- An LLM reads raw sources and writes structured wiki articles into `wiki/`
3. **Auto-maintained indexes** -- INDEX.md and GLOSSARY.md are regenerated after every compilation
4. **Agent creation tools** -- Three wiki-backed workflows:
   - `authoring/SKILL.md` -- review and improve existing agents
   - `agent-maker/SKILL.md` -- interactive 8-phase creation
   - `prompt-decomposer/SKILL.md` -- extract agent components from prompts/codebases
5. **Quality standard** -- AGENT_SPEC.md with 8 scoring dimensions and automated validator
6. **Feedback loops** -- Health checks, monthly updates, and query logs feed back into the wiki
7. **Incremental enhancement** -- Each compilation pass improves existing articles and adds new ones

The wiki is the LLM's compiled knowledge -- not a static document, but a living system that gets smarter with every update cycle.

---

## Companion Projects

### Skill Factory

**[Skill Factory](../skill-factory/)** is Agent Factory's sibling project. Together they cover the full stack of AI agent development:

| Project | Domain | Teaches |
|---------|--------|---------|
| **Agent Factory** | The autonomous system | Architecture, orchestration, tools, memory, deployment |
| **Skill Factory** | The capability layer | Writing SKILL.md files that augment agents |

Skills are markdown files loaded by agents at runtime. Agents are the autonomous systems that read and execute them. You need both: an agent without skills has limited capabilities, and skills without an agent have no runtime.

### Factory Showcase

**[Factory Showcase](https://github.com/akijain2000/factory-showcase)** is a testing companion with 20 agents and 20 skills created using both factories, then evaluated through a 5-cycle Karpathy loop + 7-wave autoresearch improvement loop (~100 iterations). Final scores: AGENT_SPEC mean 9.04/10, CLASSic mean 9.02/10. Contains grading reports, per-wave learning logs documenting what increases and decreases agent scores, and a comprehensive [LEARNINGS.md](https://github.com/akijain2000/factory-showcase/blob/main/grading/autoresearch-logs/LEARNINGS.md) that distills the empirical findings for anyone building agents.

---

## Contributing

Contributions welcome:

- **Add a source repo**: Update `raw/repos/SOURCES.md`, recompile the wiki
- **Write a wiki article**: Follow the patterns in existing concept/research articles
- **Add a curated example**: Good or bad, with annotations explaining why
- **Improve the course**: Each module should be self-contained with exercises
- **Improve the spec**: AGENT_SPEC.md evolves as the ecosystem matures
- **Report a gap**: Open an issue if the wiki is missing a pattern you've seen

---

## License

MIT
