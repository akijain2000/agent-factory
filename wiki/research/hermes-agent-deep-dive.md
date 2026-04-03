# Hermes: Skills from Experience, Multi-Platform Agents

Hermes-family architectures (as described in public materials and community writeups) emphasize **learning from use**: converting recurring interactions into **skills** or procedures that tighten future loops. This note analyzes the pattern stack—**self-improvement during use**, **persistent knowledge**, **multi-channel surfaces**, and **provider fallback chains**—as transferable engineering lessons.

## Skills from experience

Rather than freezing behavior at deploy time, systems observe **successful trajectories** (tool sequences, prompt edits, user corrections) and promote them into **reusable skill files** or templates. Engineering challenges include **privacy** (what may be retained), **validation** (false skill promotion), and **versioning** (skills are code-like artifacts requiring review).

## Persistent knowledge layers

Hermes-style agents combine **session memory** with **durable stores**: facts about user preferences, project conventions, and integration endpoints. The architectural split mirrors **episodic vs semantic** memory—implemented as logs, KV stores, or vector indices depending on retrieval needs.

## Multi-platform architecture (Telegram, Discord, Slack, CLI)

Channels differ in **identity**, **rate limits**, **rich media**, and **threading models**. A robust core hosts **channel adapters** that normalize inbound events to a **task envelope** and render outbound responses per platform capabilities. This avoids re-implementing reasoning per chat network.

## Fallback provider chains

Reliability strategies chain **LLM providers** or models: on timeout, rate limit, or quality check failure, degrade to alternate endpoints. Tradeoffs include **behavior drift** across providers and **data residency** constraints—fallback is not always legal or safe.

## Self-improvement guardrails

Promotion of learned behavior should pass **automated checks**: schema validity, policy alignment, and regression evals on a **skill test suite**. Without gates, “hill-climbing on user chats” encodes **bias** and **unsafe** shortcuts.

## Operational observability

Per-channel **metrics** (latency, error codes, cost) and **unified trace IDs** help debug cross-platform issues. Correlate provider fallbacks to **incident** patterns for capacity planning.

## Comparison to harness-first systems

Gstack-style **human-authored** skills prioritize explicit governance; Hermes-like **experience-derived** skills prioritize adaptation speed. Hybrids version **promoted** skills through PR workflows.

## Channel adapters and identity

Telegram bots, Discord apps, and Slack workflows differ in **user identity** resolution and **OAuth** scopes. A normalized internal user record prevents **privilege confusion** when the same human interacts through multiple surfaces. Rate-limit backoff must be **per-channel** to avoid global throttling of unrelated traffic.

## Skill promotion pipeline (idealized)

1. Capture candidate trajectory with **redaction**.  
2. Score utility vs risk via **offline replay** on fixtures.  
3. Open a **change proposal** (diff) for human or automated review.  
4. Merge into library with **semver** and **rollback** hooks.

Skipping steps 2–4 yields “self-modifying” agents that encode **toxic** shortcuts.

## Provider drift and testing

Fallback chains should run **contract tests** per provider: identical prompts may yield **incompatible** tool-call formats or safety refusals. Continuous **canary** prompts detect silent behavior drift after vendor updates.

## Sources and further reading

- Public Hermes project documentation and community analyses (verify details against current repos).
- Research on continual learning risks in LLM agents.

## See also

- [Gstack agent analysis](gstack-agent-analysis.md)
- [Context memory architecture](context-memory-architecture.md)
- [Autoagent harness patterns](autoagent-harness-patterns.md)
- Concepts: [Self-Improving Agents](../concepts/self-improving-agents.md), [Agent Memory Patterns](../concepts/agent-memory-patterns.md), [Feedback Loops](../concepts/feedback-loops.md), [Deployment Patterns](../concepts/deployment-patterns.md)
- Course: [Agent Factory course](../../course/README.md)
