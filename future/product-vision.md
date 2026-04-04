# Product Vision: Beyond Hacky Scripts

Design doc for evolving Agent Factory from a markdown knowledge base into a proper product.

## Current state

Agent Factory is a collection of markdown files, LLM runbooks, and TypeScript CLI scripts. It works, but requires manual orchestration: you read a SKILL.md, the LLM follows instructions, and produces output. There is no unified interface, no API, and no automation beyond what the user manually triggers.

## Vision: Three horizons

### Horizon 1: Developer tooling (now → 3 months)

**Goal:** Make the knowledge base self-service for developers.

| Capability | Current | Target |
|-----------|---------|--------|
| Search | `bun scripts/search-wiki.ts` (CLI) | Web UI with semantic search + filters |
| Article browsing | Open markdown files | Obsidian vault with graph view (done) |
| Wiki compilation | Manual LLM runbook | CI job triggered on raw/ changes |
| Health checks | Manual LLM runbook | Weekly automated report to Slack/email |
| Agent validation | `bun scripts/validate-agent.ts` (CLI) | GitHub Action for PR checks |
| Chart generation | `python generate-charts.py` (manual) | Auto-generated on grading data changes |

**Key deliverables:**
- GitHub Actions workflow for wiki compilation and health checks
- Simple static site (Astro/Next.js) for wiki browsing and search
- PR-level agent validation as a GitHub check

### Horizon 2: API and integrations (3-6 months)

**Goal:** Let other tools and agents query the knowledge base programmatically.

| Capability | Implementation |
|-----------|---------------|
| REST API | `/api/search?q=circuit+breaker` → ranked wiki results with snippets |
| MCP server | Expose wiki as MCP resources; agent-maker as MCP tool |
| VS Code extension | Inline agent-building guidance from wiki while coding |
| Slack bot | Ask agent-building questions, get wiki-grounded answers |
| CI integration | Score agents on PR, block merge if below threshold |

**Key deliverables:**
- FastAPI/Express API server with wiki search endpoint
- MCP server wrapping the wiki and agent-maker
- GitHub App for automated agent scoring

### Horizon 3: Self-improving knowledge system (6-12 months)

**Goal:** The knowledge base improves itself.

| Capability | Implementation |
|-----------|---------------|
| Auto-discovery | Weekly GitHub search for new agent repos, auto-classify, auto-ingest |
| Auto-compilation | New raw sources trigger wiki article updates automatically |
| Quality tracking | Dashboard showing wiki health score over time |
| Feedback loop | Users report gaps → auto-prioritize → auto-draft articles |
| Fine-tuned model | Specialized model trained on wiki for instant Q&A |

**Key deliverables:**
- Autonomous update pipeline (discovery → ingest → compile → health-check → publish)
- Quality dashboard with historical trends
- Fine-tuned model serving wiki-grounded answers

## Architecture evolution

```
CURRENT:                          HORIZON 3:
                                  
  User → SKILL.md → LLM           User → Web UI → API
    ↓                                ↓         ↓
  Manual wiki browse               Search    MCP tools
    ↓                                ↓         ↓
  Manual CLI scripts               Auto CI    Agent scoring
                                     ↓
                                  Self-update loop
```

## Principles

1. **Markdown first** -- the knowledge base remains readable without any tooling
2. **Incremental value** -- each horizon delivers standalone value
3. **LLM-native** -- the primary users of the API are other LLMs, not humans
4. **Open source** -- the knowledge base and tools remain MIT licensed

## Status

Horizon 1 is partially implemented (CLI tools, Obsidian config). Horizons 2 and 3 are design-only.
