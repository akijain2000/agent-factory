# Hermes: Skills from Experience, Multi-Platform Agents

Hermes-family architectures (as described in public materials and community writeups) emphasize **learning from use**: converting recurring interactions into **skills** or procedures that tighten future loops. This note analyzes the pattern stack—**self-improvement during use**, **persistent knowledge**, **multi-channel surfaces**, and **provider fallback chains**—as transferable engineering lessons.

## Architecture overview

Hermes agents follow a layered architecture that separates concerns vertically:

```
┌─────────────────────────────────────────────┐
│  Channel Adapters (Telegram, Discord, CLI)  │
├─────────────────────────────────────────────┤
│  Task Router & Intent Classifier            │
├─────────────────────────────────────────────┤
│  Agent Core (ReAct loop + skill loader)     │
├──────────┬──────────┬───────────────────────┤
│  Memory  │  Skills  │  Tool Registry        │
│  Manager │  Store   │  (MCP + native)       │
├──────────┴──────────┴───────────────────────┤
│  Provider Chain (primary → fallback → cache)│
├─────────────────────────────────────────────┤
│  Persistence (SQLite/Postgres + vector DB)  │
└─────────────────────────────────────────────┘
```

The **Agent Core** runs a standard ReAct loop but with a critical extension: before each planning step, it loads relevant **skills** from the skill store into context. Skills are selected by embedding similarity to the current task, recency of promotion, and explicit user or project tags. This dynamic skill injection means the agent's effective behavior changes over time without redeploying code.

## Skills from experience

Rather than freezing behavior at deploy time, systems observe **successful trajectories** (tool sequences, prompt edits, user corrections) and promote them into **reusable skill files** or templates. Engineering challenges include **privacy** (what may be retained), **validation** (false skill promotion), and **versioning** (skills are code-like artifacts requiring review).

### Trajectory capture mechanics

The system logs structured traces for every task: input, tool calls (with arguments and results), model reasoning steps, outcome (success/failure/partial), and user corrections if any. Traces are stored with PII redaction applied at write time, not retroactively.

A **skill candidate detector** runs offline (or on a schedule) over recent traces looking for:
- Repeated tool sequences (same 3+ tool chain across 5+ tasks)
- User corrections that converge (the model makes the same mistake, user fixes it the same way)
- Successful paths that are significantly shorter than average for that task type

### Skill file anatomy

```
skills/
├── promoted/           # active, loaded into context
│   ├── summarize-pr.md
│   └── debug-typescript.md
├── candidates/         # awaiting promotion
│   ├── draft-api-test.md
│   └── refactor-imports.md
├── deprecated/         # demoted after model change
│   └── old-sql-pattern.md
└── registry.json       # metadata: scores, versions, tags
```

Each skill file contains: trigger conditions (when to load), the procedure (step-by-step instructions), constraints (what not to do), and evidence metadata (which tasks it improved, by how much, which model version).

## The learning loop in detail

The learning loop has five distinct phases with explicit gates between them:

**Phase 1: Capture** — Every task produces a structured trace. The system annotates traces with outcome quality (binary success, user satisfaction signal, or automated eval score).

**Phase 2: Mine** — A batch job clusters successful traces by task type and extracts common subsequences. The mining step uses both structural matching (same tool sequence) and semantic matching (similar reasoning patterns across different tool sets).

**Phase 3: Draft** — A meta-agent (or the same agent in a special mode) converts a mined pattern into a skill file: natural language procedure, trigger conditions, and test fixtures. The draft explicitly cites which traces it was derived from.

**Phase 4: Validate** — The candidate skill is tested against a holdout task set. Key metrics:
- Does loading this skill improve success rate? (must be ≥15% lift on ≥10 tasks)
- Does it regress any existing skill's performance? (zero-regression policy)
- Does it pass safety checks? (no credential exposure, no guardrail bypasses)
- Is it model-version-specific? (tagged so it can be retired after upgrades)

**Phase 5: Promote or Reject** — Skills that pass validation enter `promoted/` and are loaded into future contexts. Rejected candidates get a rejection reason and can be re-submitted after edits. The promotion event is logged with full provenance.

### Demotion triggers

Promoted skills are not permanent. Demotion occurs when:
- A model upgrade changes behavior enough that the skill's lift drops below threshold
- The skill's trigger conditions overlap with a newer, better-performing skill
- A safety audit flags problematic instructions
- The skill hasn't been loaded in 90 days (staleness)

## Persistent knowledge layers

Hermes-style agents combine **session memory** with **durable stores**: facts about user preferences, project conventions, and integration endpoints. The architectural split mirrors **episodic vs semantic** memory—implemented as logs, KV stores, or vector indices depending on retrieval needs.

### Memory tier design

| Tier | Lifetime | Storage | Retrieval | Example |
|------|----------|---------|-----------|---------|
| Working | Single turn | In-context | Direct | Current tool results |
| Session | One conversation | KV store | Key lookup | User's stated goal |
| Project | Weeks–months | SQLite + embeddings | Semantic search | Codebase conventions |
| Global | Permanent | Postgres | Structured query | User preferences, API keys (encrypted) |

The memory manager decides what to load each turn based on: available context window budget, task relevance (embedding similarity), recency, and explicit user references. Eviction follows a priority order: working > session > project > global, with summarization applied before eviction when possible.

## Multi-platform architecture (Telegram, Discord, Slack, CLI)

Channels differ in **identity**, **rate limits**, **rich media**, and **threading models**. A robust core hosts **channel adapters** that normalize inbound events to a **task envelope** and render outbound responses per platform capabilities. This avoids re-implementing reasoning per chat network.

### Adapter contract

Each channel adapter implements a minimal interface:

```typescript
interface ChannelAdapter {
  parseInbound(raw: PlatformEvent): TaskEnvelope;
  renderOutbound(response: AgentResponse): PlatformMessage;
  resolveIdentity(platformUser: string): InternalUserId;
  getRateLimits(): RateLimitConfig;
}
```

The **TaskEnvelope** is platform-agnostic: it carries the user message, conversation context ID, attached files (normalized to URLs), and identity. The agent core never sees platform-specific types.

### Platform-specific considerations

- **Telegram**: 4096 char message limit, inline keyboards for confirmation flows, webhook-based delivery
- **Discord**: 2000 char limit, slash commands for structured input, thread support for long tasks
- **Slack**: Block Kit for rich responses, app mentions for invocation, enterprise grid identity
- **CLI**: No message limits, stdin/stdout streaming, local file access without upload

## Fallback provider chains

Reliability strategies chain **LLM providers** or models: on timeout, rate limit, or quality check failure, degrade to alternate endpoints. Tradeoffs include **behavior drift** across providers and **data residency** constraints—fallback is not always legal or safe.

### Chain configuration

```yaml
providers:
  - name: primary
    model: gpt-4o
    timeout_ms: 30000
    max_retries: 2
  - name: fallback_fast
    model: claude-3-5-sonnet
    timeout_ms: 20000
    trigger: [timeout, rate_limit]
  - name: fallback_cheap
    model: gpt-4o-mini
    timeout_ms: 15000
    trigger: [timeout, rate_limit, cost_cap]
  - name: cached
    type: semantic_cache
    similarity_threshold: 0.95
    trigger: [all_providers_down]
```

The chain evaluates triggers in order. A **quality gate** after each fallback response checks for format compliance and tool-call validity—if the fallback model returns incompatible output, the system escalates rather than silently degrading.

## Self-improvement guardrails

Promotion of learned behavior should pass **automated checks**: schema validity, policy alignment, and regression evals on a **skill test suite**. Without gates, "hill-climbing on user chats" encodes **bias** and **unsafe** shortcuts.

### Guardrail taxonomy

| Category | Check | Enforcement |
|----------|-------|-------------|
| Schema | Skill file has required sections | Automated, blocks promotion |
| Safety | No credential patterns, no bypass instructions | Automated + human review |
| Regression | Existing skill test suites still pass | Automated, blocks promotion |
| Lift | ≥15% improvement on ≥10 tasks | Automated, blocks promotion |
| Provenance | Cites source traces, model version tagged | Automated warning |
| Staleness | Loaded in at least 1 task in last 90 days | Scheduled demotion |

## Operational observability

Per-channel **metrics** (latency, error codes, cost) and **unified trace IDs** help debug cross-platform issues. Correlate provider fallbacks to **incident** patterns for capacity planning.

### Key metrics

- **Skill hit rate**: % of tasks where a promoted skill was loaded and contributed to success
- **Promotion velocity**: skills promoted per week (too fast = weak gates, too slow = stagnation)
- **Provider fallback frequency**: triggers per hour by provider (capacity planning signal)
- **Cross-channel identity collisions**: users matched incorrectly across platforms (security metric)

## Comparison to harness-first systems

| Dimension | Hermes-style | Harness-first (e.g., gstack) |
|-----------|-------------|------------------------------|
| Skill origin | Mined from traces | Human-authored |
| Quality gate | Automated eval + optional review | Mandatory human review |
| Adaptation speed | Fast (hours) | Slow (days–weeks) |
| Governance | Medium (requires discipline) | High (PR-based) |
| Risk of drift | Higher | Lower |
| Best for | Repetitive, measurable tasks | High-stakes, policy-heavy tasks |

Gstack-style **human-authored** skills prioritize explicit governance; Hermes-like **experience-derived** skills prioritize adaptation speed. Hybrids version **promoted** skills through PR workflows.

## Channel adapters and identity

Telegram bots, Discord apps, and Slack workflows differ in **user identity** resolution and **OAuth** scopes. A normalized internal user record prevents **privilege confusion** when the same human interacts through multiple surfaces. Rate-limit backoff must be **per-channel** to avoid global throttling of unrelated traffic.

## Skill promotion pipeline (idealized)

1. Capture candidate trajectory with **redaction**.  
2. Score utility vs risk via **offline replay** on fixtures.  
3. Open a **change proposal** (diff) for human or automated review.  
4. Merge into library with **semver** and **rollback** hooks.

Skipping steps 2–4 yields "self-modifying" agents that encode **toxic** shortcuts.

## Provider drift and testing

Fallback chains should run **contract tests** per provider: identical prompts may yield **incompatible** tool-call formats or safety refusals. Continuous **canary** prompts detect silent behavior drift after vendor updates.

## Transferable lessons for agent builders

1. **Skills are code, not magic**: treat them as versioned artifacts with tests, not as ephemeral prompt tweaks.
2. **Learning loops need brakes**: unbounded self-improvement optimizes for the eval, not the user. Gates, holdouts, and human review are non-negotiable.
3. **Multi-platform is an adapter problem**: keep the agent core channel-agnostic and push all platform specifics to a thin adapter layer.
4. **Fallback is not free**: different models have different tool-call formats, safety boundaries, and quality profiles. Test each chain link independently.
5. **Observability enables trust**: if you can't show which skill fired, why the fallback triggered, and what the agent learned, operators won't trust autonomous operation.

## Sources and further reading

- Public Hermes project documentation and community analyses (verify details against current repos).
- Research on continual learning risks in LLM agents.
- Anthropic, "Building Effective Agents" (2024) — governance patterns applicable to self-improving systems.
- Shinn et al., "Reflexion" (2023) — foundational work on verbal self-reflection in agent loops.

## See also

- [Gstack agent analysis](gstack-agent-analysis.md)
- [Context memory architecture](context-memory-architecture.md)
- [Autoagent harness patterns](autoagent-harness-patterns.md)
- Concepts: [Self-Improving Agents](../concepts/self-improving-agents.md), [Agent Memory Patterns](../concepts/agent-memory-patterns.md), [Feedback Loops](../concepts/feedback-loops.md), [Deployment Patterns](../concepts/deployment-patterns.md)
- Course: [Agent Factory course](../../course/README.md)
