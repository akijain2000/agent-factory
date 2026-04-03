# Gstack Agent Architecture: Deep Dive

Gstack illustrates how **production agent behavior** emerges from **composed skills**, daemons, and workflows—not from a single omniscient prompt. This analysis maps major subsystems and how they interoperate in practice.

## Skills as the unit of capability

Gstack organizes behavior into **skills** (SKILL.md files with procedures). Skills encode domain runbooks: QA passes, PR workflows, security audits. The agent **selects** skills by relevance rather than re-deriving process each session—reducing variance and improving **auditability**.

## Browse daemon and verification

A **headless browse daemon** supports fast page interaction, screenshots, and assertions. For agent QA, this closes the loop between **code change** and **observed UI state**, catching regressions prose-only reasoning misses.

## QA and review skills

QA skills (e.g., tiered **test-fix-verify** loops) systematize **dogfooding** with evidence (screenshots, traces). Review skills apply **checklists** (SQL safety, trust boundaries) before merge. Together they mimic **human engineering gates** at machine speed—within bounded scopes.

## Ship and land-and-deploy workflows

**Ship** automates the path from clean working tree to **PR**: tests, changelog discipline, versioning semantics. **Land-and-deploy** continues after merge: wait for CI/deploy, run **canary** checks. These workflows embody **policy** (what “done” means) as executable structure.

## Composition model

The “agent” is often a **router + planner** over stable tools: git, HTTP, browser, linters, project-specific scripts. This matches Anthropic’s **workflows before agents** guidance—LLM judgment sits at **decision points**, not inside every line of bash.

## Observability and safety modes

Skills such as **careful** and **guard** layer **destructive-command** warnings and **directory-scoped edits**—operational guardrails that reduce incident blast radius during autonomous sessions.

## Limitations and boundaries

Skill quality determines ceiling; ambiguous SKILL.md instructions propagate errors. **Human oversight** remains appropriate for production data, legal commitments, and irreversible infra changes.

## Browse daemon and latency budgets

Fast headless browsing (~100ms-class commands in documentation) enables **tight feedback loops** during QA: the agent can afford more verify steps when each interaction is cheap. That shifts the Pareto frontier toward **test-after-every meaningful edit** rather than batching verification at the end—reducing compounding UI regressions.

## Skill factory and duplication

Multiple install paths (global vs vendored skills) create a **supply-chain** question: which SKILL.md is authoritative? Mature usage pins versions and treats skill updates like **library upgrades**—changelog, compatibility notes, and incremental rollout.

## Traceability for audits

Because skills encode operational policy, compliance teams can map **controls** to named skills (e.g., destructive-command warnings, directory freeze). This is weaker in ad-hoc prompt-only agents where policy lives only in chat logs.

## Interoperability with generic agents

Gstack skills are consumable by any **orchestrator** that can read markdown procedures and invoke tools—LangGraph, CrewAI, or bespoke hosts. The differentiator is **discipline** in keeping skills **small**, **testable**, and **versioned**.

## Summary

Gstack demonstrates **composition over monolith**: daemons and workflows supply reliability; skills encode policy; the LLM fills gaps **between** deterministic steps rather than replacing the engineering system.

## Sources and further reading

- Gstack skill files under `.agents/skills/gstack/` (vendored patterns in this workspace).
- Wiki: [Anatomy of a good agent](anatomy-of-a-good-agent.md) for generalized production patterns.

## See also

- [Production case studies](production-case-studies.md)
- [Autoagent harness patterns](autoagent-harness-patterns.md)
- [Anatomy of a good agent](anatomy-of-a-good-agent.md)
- Concepts: [Agent Composition](../concepts/agent-composition.md), [Harness Engineering](../concepts/harness-engineering.md), [Agent Testing Patterns](../concepts/agent-testing-patterns.md), [Deployment Patterns](../concepts/deployment-patterns.md)
- Course: [Agent Factory course](../../course/README.md)
