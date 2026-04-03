# Agent Factory -- Reference Documents

> Last updated: 2026-04-03

Curated index of reference documents (URLs + summaries). We do NOT mirror full documents -- this file is a lightweight index with pointers. Each entry has: title, URL, author, date, summary, and which wiki/course articles reference it.

---

## Research Papers and Surveys

### 1. LLM Powered Autonomous Agents
- **Author:** Lilian Weng
- **URL:** https://lilianweng.github.io/posts/2023-06-23-agent/
- **Date:** 2023-06-23
- **Summary:** Comprehensive survey of autonomous agent architectures covering planning (task decomposition, self-reflection), memory (short-term, long-term, external), and tool use. The foundational survey for agent design.
- **Referenced by:** course/01, course/03, course/06, wiki/concepts/agent-loop, wiki/concepts/memory-systems, wiki/concepts/planning-strategies

### 2. ReAct: Synergizing Reasoning and Acting in Language Models
- **Author:** Shunyu Yao et al.
- **URL:** https://arxiv.org/abs/2210.03629
- **Date:** 2022-10-06
- **Summary:** Introduces the ReAct pattern -- interleaving reasoning traces with actions. Agents that think-then-act outperform pure reasoning or pure acting. Foundational pattern for most modern agents.
- **Referenced by:** course/03, course/09, wiki/concepts/agent-loop, wiki/research/andrew-ng-patterns

### 3. Reflexion: Language Agents with Verbal Reinforcement Learning
- **Author:** Noah Shinn et al.
- **URL:** https://arxiv.org/abs/2303.11366
- **Date:** 2023-03-20
- **Summary:** Agents that reflect on failures and store verbal feedback improve over successive attempts. Key inspiration for self-improving agent patterns.
- **Referenced by:** course/09, course/22, wiki/concepts/feedback-loops, wiki/concepts/self-improving-agents

### 4. Google "Agents" White Paper
- **Author:** Google DeepMind
- **URL:** https://cloud.google.com/discover/what-are-ai-agents
- **Date:** 2024
- **Summary:** Google's definition and architecture for AI agents. Covers agent types, orchestration, and evaluation. Aligns with ADK patterns.
- **Referenced by:** course/01, course/02, wiki/concepts/agent-loop

## Industry Guides (Primary Sources)

### 5. Building Effective Agents
- **Author:** Anthropic
- **URL:** https://www.anthropic.com/research/building-effective-agents
- **Date:** 2024-12
- **Summary:** Anthropic's opinionated guide to building agents. Advocates starting simple (augmented LLM), using workflows before agents, and specific patterns (prompt chaining, routing, parallelization, orchestrator-workers, evaluator-optimizer).
- **Referenced by:** course/02, course/04, course/16, wiki/research/anthropic-agent-patterns

### 6. Harness Design for Long-Running Apps
- **Author:** Anthropic Engineering
- **URL:** https://www.anthropic.com/engineering/building-effective-agents
- **Date:** 2025
- **Summary:** How to build the infrastructure ("harness") around agents for production reliability -- error handling, context management, state persistence for long-running tasks.
- **Referenced by:** course/08, course/22, wiki/concepts/harness-engineering

### 7. A Practical Guide to Building Agents
- **Author:** OpenAI
- **URL:** https://cdn.openai.com/business-guides-and-resources/a-practical-guide-to-building-agents.pdf
- **Date:** 2025
- **Summary:** OpenAI's step-by-step guide covering when to use agents, agent design foundations, guardrails, and orchestration patterns with the Agents SDK.
- **Referenced by:** course/01, course/15, course/18, wiki/research/openai-agent-patterns

### 8. Andrew Ng's 4 Agentic Design Patterns
- **Author:** Andrew Ng
- **URL:** https://www.deeplearning.ai/the-batch/
- **Date:** 2024 (series)
- **Summary:** Four patterns that make LLM applications agentic: reflection, tool use, planning, and multi-agent collaboration. Each pattern explained with examples and implementation guidance.
- **Referenced by:** course/09, wiki/research/andrew-ng-patterns, wiki/concepts/feedback-loops

### 9. Context Engineering (Lutke/Karpathy)
- **Author:** Tobi Lutke, Andrej Karpathy
- **URL:** Various (Twitter/X threads, blog posts, 2025-2026)
- **Date:** 2025-2026
- **Summary:** The art of curating the information environment an LLM operates in. Lutke coined "context engineering" as the core AI skill. Karpathy endorsed and expanded the concept. Shifts focus from prompt engineering to information architecture.
- **Referenced by:** course/06, wiki/concepts/context-engineering

### 10. Context Rot Patterns
- **Author:** Simon Willison
- **URL:** https://simonwillison.net/
- **Date:** 2025
- **Summary:** Four patterns of context degradation: poisoning (wrong info injected), distraction (irrelevant context competing), confusion (conflicting instructions), clash (context from different sessions bleeding). Essential for long-running agents.
- **Referenced by:** course/06, course/11, wiki/concepts/context-engineering

## Framework and Protocol Docs

### 11. MCP Specification
- **URL:** https://modelcontextprotocol.io/
- **Summary:** The Model Context Protocol -- standard for connecting LLMs to external tools, data, and services. Defines server/client architecture, tool schemas, resource access.
- **Referenced by:** course/05, course/21, wiki/research/mcp-deep-dive

### 12. A2A Specification
- **URL:** https://github.com/a2aproject/A2A
- **Summary:** Agent-to-Agent protocol for inter-agent communication and task delegation. Enables agents built with different frameworks to collaborate.
- **Referenced by:** course/21, wiki/research/a2a-deep-dive

### 13. OpenAI Agents SDK Documentation
- **URL:** https://openai.github.io/openai-agents-python/
- **Summary:** Official docs for OpenAI's Agents SDK. Covers Agent class, handoffs, guardrails, tracing, MCP integration.
- **Referenced by:** course/15, wiki/research/openai-agent-patterns

### 14. LangGraph Documentation
- **URL:** https://langchain-ai.github.io/langgraph/
- **Summary:** Official LangGraph docs. State machines as directed graphs, persistence/checkpointing, human-in-the-loop, streaming, multi-agent patterns.
- **Referenced by:** course/14, wiki/research/framework-comparison

### 15. CrewAI Documentation
- **URL:** https://docs.crewai.com/
- **Summary:** Official CrewAI docs. Role-based agents, YAML configuration, task delegation, crew orchestration.
- **Referenced by:** course/13, wiki/research/framework-comparison

### 16. Anthropic Tool Use Docs
- **URL:** https://docs.anthropic.com/en/docs/build-with-claude/tool-use
- **Summary:** How to give Claude access to external tools via function calling. Structured input/output, tool choice, error handling.
- **Referenced by:** course/05, course/16

### 17. Anthropic Extended Thinking Docs
- **URL:** https://docs.anthropic.com/en/docs/build-with-claude/extended-thinking
- **Summary:** Claude's extended thinking capability for complex reasoning. Budget tokens, streaming thinking, use in agent architectures.
- **Referenced by:** course/07, course/16

## Agent-Specific References

### 18. AutoAgent program.md Pattern
- **Author:** Kevin Gu
- **URL:** https://github.com/kevinrgu/autoagent
- **Summary:** The program.md is AutoAgent's core innovation -- a human-readable file that specifies agent behavior, evaluated by a meta-agent that hill-climbs on benchmark scores. The meta-agent modifies the program.md autonomously.
- **Referenced by:** course/22, wiki/research/autoagent-harness-patterns, wiki/concepts/harness-engineering

### 19. ByteRover Context Memory Architecture
- **Author:** ByteRover team
- **URL:** https://github.com/campfirein/byterover-cli
- **Summary:** Context tree architecture for portable agent memory. Knowledge storage, cloud sync, agentic map, 20+ LLM provider support. Achieves 96%+ accuracy on LoCoMo benchmark for long-context memory.
- **Referenced by:** course/06, wiki/research/context-memory-architecture, wiki/concepts/context-engineering

### 20. Hermes Agent Architecture
- **Author:** Nous Research
- **URL:** https://github.com/NousResearch/hermes-agent
- **Summary:** Self-improving agent with learning loop and persistent skills. Multi-platform support. Learns from interactions and creates new skills autonomously. Fallback provider chains for reliability.
- **Referenced by:** course/08, course/22, wiki/research/hermes-agent-deep-dive, wiki/concepts/self-improving-agents

### 21. Paperclip Orchestration Platform
- **Author:** Paperclip AI team
- **URL:** https://github.com/paperclipai/paperclip
- **Summary:** "Zero-human company" orchestration. Agent teams with goal assignment, cost tracking, company skills library. React UI for managing agent work. Key study for multi-agent orchestration at scale.
- **Referenced by:** course/10, wiki/research/paperclip-orchestration-analysis, wiki/concepts/agent-orchestration-platforms

## People and Blog Posts

### 22. Harrison Chase on Agent Architecture
- **Author:** Harrison Chase
- **URL:** https://blog.langchain.dev/ (various posts)
- **Summary:** LangChain founder's posts on agent state machines, when to use graphs vs chains, persistence patterns, and the evolution from chains to agents.
- **Referenced by:** course/14, wiki/research/framework-comparison

### 23. Karpathy LLM-KB Pattern
- **Author:** Andrej Karpathy
- **URL:** Various (Twitter/X, YouTube)
- **Summary:** The pattern of using LLMs as the query interface for a curated knowledge base. Raw sources -> compiled wiki -> LLM queries. The architectural pattern Agent Factory itself uses.
- **Referenced by:** SKILL.md, README.md

### 24. Joao Moura on Multi-Agent Design
- **Author:** Joao Moura
- **URL:** https://blog.crewai.com/ (various posts)
- **Summary:** CrewAI creator's insights on role-based agent design, crew orchestration, and when multi-agent outperforms single-agent.
- **Referenced by:** course/10, wiki/research/multi-agent-landscape

### 25. Garry Tan on Production Agent Workflows
- **Author:** Garry Tan
- **URL:** https://github.com/garrytan/gstack
- **Summary:** Production agent skill patterns: browse daemon for web interaction, QA testing, ship/deploy workflows. Practical patterns for making agents useful in real development workflows.
- **Referenced by:** course/05, wiki/research/gstack-agent-analysis
