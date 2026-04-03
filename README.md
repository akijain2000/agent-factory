# Agent Factory

> LLM knowledge base for building production-quality AI agents.

Agent Factory is a structured knowledge base, course, and toolkit that teaches AI agents (and their developers) how to build autonomous agent systems. It follows the Karpathy LLM-KB pattern: curated raw sources compiled into a wiki, queried by meta-skills, taught through a structured course.

**Sibling project to [Skill Factory](../skill-factory/).** Skills are markdown files that augment existing agents. Agents are the autonomous systems themselves -- architecture, orchestration, tools, memory, state, deployment.

---

## Architecture

```
agent-factory/
├── SKILL.md                    # Router -- entry point (Routes A-D)
├── AGENT_SPEC.md               # Quality standard for agent projects
├── README.md                   # You are here
│
├── agent-maker/SKILL.md        # Meta-skill: interactive agent creation (8 phases)
├── authoring/SKILL.md          # Meta-skill: review and improve existing agents
├── prompt-decomposer/SKILL.md  # Meta-skill: extract agent components from prompts
│
├── course/                     # 23-module course (~11-13 hours)
│   ├── README.md               # Course overview and learning path
│   ├── 01-what-are-agents.md
│   ├── 02-agent-architectures.md
│   ├── ...
│   └── 23-capstone-build-a-production-agent.md
│
├── wiki/                       # 80+ articles
│   ├── INDEX.md                # Article index
│   ├── GLOSSARY.md             # 60+ term glossary
│   ├── concepts/               # 35 concept articles
│   ├── research/               # 20 research deep dives
│   └── examples/               # 14 good + 8 bad annotated examples
│
├── scripts/                    # Maintenance tools
│   ├── validate-agent.ts       # Linter for agent projects
│   ├── compile-wiki.md         # LLM runbook: raw -> wiki
│   ├── health-check.md         # LLM runbook: wiki audit
│   ├── update-sources.md       # LLM runbook: source discovery
│   └── discovery-keywords.txt  # Search terms for new repos
│
└── raw/                        # Reference material
    ├── docs/SOURCES.md         # 25 reference document index
    └── repos/SOURCES.md        # 40+ reference repo manifest
```

---

## Quick Start

### For AI Agents

Point your agent at `SKILL.md` to get started. The router presents four options:

| Route | What it does | Meta-skill |
|-------|-------------|------------|
| **A** | Review and improve an existing agent | `authoring/SKILL.md` |
| **B** | Create a new agent from scratch | `agent-maker/SKILL.md` |
| **C** | Learn about agent building | `course/README.md` or `wiki/INDEX.md` |
| **D** | Decompose a prompt into agent components | `prompt-decomposer/SKILL.md` |

### For Developers

1. Browse the [course](course/README.md) for structured learning (23 modules, ~11-13 hours)
2. Use the [wiki](wiki/INDEX.md) as a reference while building
3. Run `bun scripts/validate-agent.ts /path/to/your/agent` to lint your agent project
4. Review [AGENT_SPEC.md](AGENT_SPEC.md) for the quality standard

---

## Course Overview

Six blocks, 23 modules, from fundamentals to production mastery.

| Block | Modules | Focus | Hours |
|-------|---------|-------|-------|
| **1. Foundations** | 01-04 | What agents are, architectures, the loop, system prompts | ~2.5 |
| **2. Core Building Blocks** | 05-08 | Tools, memory, planning, error handling | ~2.5 |
| **3. Patterns & Anti-Patterns** | 09-12 | Design patterns, multi-agent, anti-patterns, state | ~2.5 |
| **4. Frameworks** | 13-16 | Framework selection, LangGraph, OpenAI SDK, Anthropic | ~2.5 |
| **5. Production** | 17-20 | Testing, safety, observability, deployment | ~2.5 |
| **6. Mastery** | 21-23 | Protocols, self-improvement, capstone project | ~2.5 |

---

## Wiki at a Glance

### Concepts (35 articles)

Core building blocks of agent design:

| Category | Articles |
|----------|----------|
| **Agent Core** | agent-loop, planning-strategies, state-management, agent-lifecycle |
| **Tools** | tool-design, tool-selection, structured-outputs |
| **Memory** | memory-systems, agent-memory-patterns, context-window-management, context-engineering |
| **Safety** | guardrails, human-in-the-loop, sandboxing, agent-security |
| **Multi-Agent** | multi-agent-orchestration, agent-handoffs, agent-orchestration-platforms |
| **Production** | error-recovery, observability, cost-optimization, deployment-patterns, rate-limiting |
| **Design** | prompt-engineering-for-agents, agent-personas, progressive-complexity, agent-composition, model-selection, agent-ux |
| **Advanced** | feedback-loops, agent-evaluation, agent-testing-patterns, harness-engineering, self-improving-agents, autonomous-loops |

### Research (20 deep dives)

Surveys, framework comparisons, and system analyses including: Andrew Ng patterns, Lilian Weng survey, Anthropic/OpenAI agent patterns, MCP/A2A protocol deep dives, and analyses of Hermes Agent, Paperclip, AutoAgent, ByteRover, and OpenClaw.

### Examples (22 annotated)

14 good examples (LangGraph ReAct, CrewAI research team, Hermes self-improving, AutoAgent harness loop, and more) and 8 anti-pattern examples (god agent, over-tooled, context-stuffing, premature autonomy, and more).

---

## Reference Sources

### Top Repos (40+ in manifest)

| Tier | Focus | Key repos |
|------|-------|-----------|
| **1. Major Systems** | Deep analysis | OpenClaw, Hermes Agent, Paperclip, AutoGPT |
| **2. Frameworks** | Architecture patterns | LangGraph, CrewAI, OpenAI Agents SDK, Google ADK, AutoGen |
| **3. Optimizers** | Harness engineering | AutoAgent, ByteRover, AutoContext |
| **4. Coding Agents** | Autonomous patterns | Goose, gstack, Ralph, Aperant, Ouroboros |
| **5. Infrastructure** | Protocols & tools | MCP servers, A2A, e2b, LiteLLM, Composio |
| **6. Capabilities** | Agent tools | Stagehand, Firecrawl, phidata, LlamaIndex |
| **7. Learning** | Reference | agentic_patterns, Anthropic/OpenAI cookbooks |

Full manifest: [raw/repos/SOURCES.md](raw/repos/SOURCES.md)

### Reference Documents (25)

Research papers (Weng, Yao, Shinn), industry guides (Anthropic, OpenAI, Ng), framework docs (MCP, A2A, LangGraph, CrewAI), and agent-specific references (AutoAgent, ByteRover, Hermes, Paperclip).

Full index: [raw/docs/SOURCES.md](raw/docs/SOURCES.md)

---

## Key People

| Person | Contribution |
|--------|-------------|
| Andrej Karpathy | LLM-KB pattern, context engineering |
| Andrew Ng | 4 agentic design patterns |
| Lilian Weng | Autonomous agents survey |
| Shunyu Yao | ReAct pattern |
| Noah Shinn | Reflexion (self-improvement) |
| Tobi Lutke | "Context engineering" concept |
| Simon Willison | Context rot patterns |
| Harrison Chase | LangGraph, agent state machines |
| Joao Moura | CrewAI, multi-agent design |
| Kevin Gu | AutoAgent, harness engineering |
| Garry Tan | gstack, production agent skills |

---

## Quality Standard

Agent projects are evaluated against [AGENT_SPEC.md](AGENT_SPEC.md) across 8 dimensions:

1. **Architecture** -- Clear agent loop, defined tools, state management
2. **System Prompt** -- Persona, constraints, tool instructions, guardrails
3. **Tool Design** -- Structured I/O, error handling, timeouts
4. **Memory** -- Appropriate memory type for the use case
5. **Safety** -- Guardrails, sandboxing, human-in-the-loop
6. **Testing** -- Behavioral tests, trace analysis, baselines
7. **Observability** -- Tracing, logging, cost tracking
8. **Documentation** -- Architecture diagram, tool catalog, deploy guide

Minimum viable score: 5/10 average, no dimension below 3/10.

---

## Scripts

| Script | Purpose | Usage |
|--------|---------|-------|
| `validate-agent.ts` | Lint agent projects | `bun scripts/validate-agent.ts /path/to/agent` |
| `compile-wiki.md` | LLM runbook: compile raw sources into wiki | Follow instructions in file |
| `health-check.md` | LLM runbook: audit wiki quality | Follow instructions in file |
| `update-sources.md` | LLM runbook: discover new sources | Follow instructions in file |
| `discovery-keywords.txt` | Search terms for source discovery | Used by update-sources.md |

---

## Companion Project

**[Skill Factory](../skill-factory/)** is Agent Factory's sibling project. While Agent Factory teaches how to build autonomous agents, Skill Factory teaches how to write SKILL.md files that augment those agents with new capabilities.

Together they cover the full stack of AI agent development: the agent itself (Agent Factory) and the skills that extend it (Skill Factory).
