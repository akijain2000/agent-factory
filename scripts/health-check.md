# Wiki Health Check (LLM runbook)

Use this runbook to audit the Agent Factory wiki for quality, consistency, and staleness. Outputs should be actionable for maintainers without rewriting content unless explicitly requested.

## Scope

- `wiki/INDEX.md` as the navigation source of truth.
- `wiki/concepts/`, `wiki/research/`, `wiki/examples/` (including `good/` and `bad/`).
- `wiki/GLOSSARY.md` and glossary links from INDEX.

## Checks

1. **Orphans.** List markdown files with no inbound link from INDEX or from another wiki page. For each orphan, classify: add link, merge into parent, or delete with rationale.

2. **Stale cues.** Flag articles whose References contain dead URLs, unnamed framework versions, or time-sensitive claims without a date. Prefer **Warn** and a suggested fix unless the user asked for silent edits.

3. **Structure drift.** Sample several articles across folders. Compare heading patterns and optional front matter to the majority. List outliers and a one-line standardization suggestion.

4. **Duplication.** Search for near-duplicate titles or repeated paragraphs across files. Recommend consolidate, keep canonical location, and note INDEX redirects or merge steps.

5. **Examples balance.** Check that `examples/good/` and `examples/bad/` cover major themes (tooling, agent loop, safety, multi-agent, cost). Document gaps as backlog items.

6. **Glossary alignment.** Spot high-frequency terms in new articles that are missing from `wiki/GLOSSARY.md` or INDEX anchors. Propose additions in glossary style (short definition, see-also).

7. **Find inconsistencies.** Compare factual claims across articles. Flag cases where article A says one thing and article B contradicts it (e.g., different circuit breaker defaults, conflicting framework recommendations, incompatible scoring anchors). For each inconsistency, identify the authoritative source (AGENT_SPEC.md, course module, or primary research article) and recommend which to keep.

8. **Impute missing data.** Identify articles with placeholder text, TODO markers, or empty sections (heading followed immediately by another heading). For each gap, suggest content from related wiki articles, course modules, or raw sources that could fill it. Flag with priority: high (blocks understanding), medium (reduces quality), low (cosmetic).

9. **Suggest new articles.** Analyze course modules and raw/docs/SOURCES.md for topics frequently referenced but not yet covered by a dedicated wiki article. Check for patterns mentioned in 3+ course modules without a concepts/ article. Output as a ranked list with proposed title, suggested category (concepts/research/examples), and source material pointers.

10. **Find connections.** For each wiki article, identify the 3-5 most semantically related articles that are NOT currently linked. Use topic overlap, shared terminology, and complementary coverage to rank suggestions. Output as a list of recommended cross-links: `[source] → [target]: [reason]`. This builds the web of knowledge that makes the wiki navigable beyond INDEX.md.

## CLI pre-checks

Before starting the LLM-powered checks above, run these automated tools:

```bash
bun scripts/check-links.ts wiki/ course/    # broken internal links
bun scripts/wiki-stats.ts wiki/             # article count, word count, orphans
bun scripts/search-wiki.ts "TODO" --path wiki/  # find TODOs and placeholders
```

Include their output in the health check report.

## Output format

Emit a table per area: **Check** | **Pass/Warn/Fail** | **Notes** | **Suggested action**.

Summarize counts: total articles scanned, orphans, stale links, duplicates.

## Done when

Every **Fail** has a concrete next step; **Warn** items are backlog-ready one-liners with owners or priority hints.

## Cadence

Run after large imports, before a release of Agent Factory content, or quarterly if the wiki is stable.

## Constraints

Do not delete user content without explicit approval; prefer marking deprecated sections in-place and linking replacements.
