# Agent Factory Course

This course is a structured path through the **Agent Factory** wiki and examples: from definitions and loops to frameworks, production concerns, and advanced interoperability and self-improvement. It is designed for builders who learn best by **reading**, **exercising**, and **shipping** small vertical slices.

## Who this is for

You should be comfortable with **basic LLM usage** (chat APIs, tokens, temperature) and **general programming** (read code, run scripts, use git). Prior exposure to HTTP APIs and JSON helps for tool and protocol modules. You do not need to be a researcher; the emphasis is **practical systems**.

## Learning path

Work modules in order within each block unless a module’s prerequisites note otherwise. Blocks 1–3 establish vocabulary and architecture; Blocks 4–5 map those ideas to real frameworks and operations; Block 6 extends to protocols, harness engineering, and a **capstone**.

**Estimated time:** about **11–13 hours** of focused study for all 23 modules (excluding capstone implementation time, which varies by scope).

## Course structure: six blocks

### Block 1: Foundations (Modules 01–04)

What agents are, architectures, the agent loop, and system prompts. Establishes shared language for the rest of the course.

### Block 2: Core Building Blocks (Modules 05–08)

Tools, memory and context, planning and reasoning, error handling and recovery. These modules mirror what most production agents spend engineering time on.

### Block 3: Patterns and Anti-Patterns (Modules 09–12)

Design patterns, multi-agent patterns, explicit anti-patterns, and state management. Use this block to critique designs before you commit to code.

### Block 4: Frameworks (Modules 13–16)

Framework selection, LangGraph, OpenAI Agents SDK, and Anthropic-oriented patterns. Compare trade-offs rather than treating any stack as universal.

### Block 5: Production (Modules 17–20)

Evaluation and testing, safety and guardrails, observability and debugging, deployment and scaling. Treat this block as the **minimum bar** before user-facing or high-impact automation.

### Block 6: Mastery (Modules 21–23)

Protocols and interoperability (MCP, A2A), self-improvement and harness engineering, and the **production capstone**. Completing Block 6 means you can situate agents in an ecosystem, not only a single repository.

## Module listing

| Module | Title | Duration |
|--------|--------|----------|
| [01](01-what-are-agents.md) | What Are Agents | 30 min |
| [02](02-agent-architectures.md) | Agent Architectures | 40 min |
| [03](03-the-agent-loop.md) | The Agent Loop | 40 min |
| [04](04-system-prompts-for-agents.md) | System Prompts for Agents | 30 min |
| [05](05-tool-design-and-integration.md) | Tool Design and Integration | 45 min |
| [06](06-memory-and-context-engineering.md) | Memory and Context Engineering | 45 min |
| [07](07-planning-and-reasoning.md) | Planning and Reasoning | 40 min |
| [08](08-error-handling-and-recovery.md) | Error Handling and Recovery | 30 min |
| [09](09-agent-design-patterns.md) | Agent Design Patterns | 45 min |
| [10](10-multi-agent-patterns.md) | Multi-Agent Patterns | 45 min |
| [11](11-anti-patterns.md) | Anti-Patterns | 35 min |
| [12](12-state-management.md) | State Management | 35 min |
| [13](13-framework-selection.md) | Framework Selection | 30 min |
| [14](14-building-with-langgraph.md) | Building with LangGraph | 45 min |
| [15](15-building-with-openai-agents-sdk.md) | Building with OpenAI Agents SDK | 45 min |
| [16](16-building-with-anthropic.md) | Building with Anthropic | 45 min |
| [17](17-agent-evaluation-and-testing.md) | Agent Evaluation and Testing | 40 min |
| [18](18-safety-and-guardrails.md) | Safety and Guardrails | 40 min |
| [19](19-observability-and-debugging.md) | Observability and Debugging | 35 min |
| [20](20-deployment-and-scaling.md) | Deployment and Scaling | 35 min |
| [21](21-protocols-and-interoperability.md) | Protocols and Interoperability | 40 min |
| [22](22-self-improvement-and-harness-engineering.md) | Self-Improvement and Harness Engineering | 45 min |
| [23](23-capstone-build-a-production-agent.md) | Capstone: Build a Production Agent | 60 min |

## Using the wiki alongside the course

Each module points to **concept** and **research** articles under [`../wiki/`](../wiki/INDEX.md). Use the wiki when you need depth, citations, or alternative phrasing of the same idea. The [`../wiki/examples/`](../wiki/examples/good/) tree contains **good** and **bad** exemplars; read bad examples to sharpen design reviews.

Start from [`../wiki/INDEX.md`](../wiki/INDEX.md) if you prefer browsing by topic instead of linear modules.

## Quality standard

Treat **[AGENT_SPEC.md](../AGENT_SPEC.md)** as the repository’s cross-cutting quality bar: clarity of purpose, tooling discipline, safety, observability, and operational readiness. Use it when reviewing your own capstone or a teammate’s agent PR.

## Companion project: Skill Factory

Agents and **skills** (procedures loaded by hosts) share engineering concerns: scoping, discovery, verification, and safety. The companion **Skill Factory** project lives at [`../../skill-factory/`](../../skill-factory/README.md) relative to this folder (sibling of `agent-factory` under the same parent workspace). Use it when you want parallel depth on authoring reusable **SKILL.md** assets and validation loops.

---

*Agent Factory course README — aligns with modules 01–23 and the project wiki.*
