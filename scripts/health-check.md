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

## Output format

Emit a table per area: **Check** | **Pass/Warn/Fail** | **Notes** | **Suggested action**.

Summarize counts: total articles scanned, orphans, stale links, duplicates.

## Done when

Every **Fail** has a concrete next step; **Warn** items are backlog-ready one-liners with owners or priority hints.

## Cadence

Run after large imports, before a release of Agent Factory content, or quarterly if the wiki is stable.

## Constraints

Do not delete user content without explicit approval; prefer marking deprecated sections in-place and linking replacements.
