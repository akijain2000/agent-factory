# Update Sources (LLM runbook)

Use this runbook to discover new reference repositories and documentation for Agent Factory, then record them without bloating the wiki or violating licenses.

## Goals

- Surface high-signal agent harnesses, SDKs, evaluations, and postmortems aligned with production agents.
- Prefer sources with clear licenses, stable URLs, and architecture you can summarize in your own words.

## Discovery workflow

1. Read `scripts/discovery-keywords.txt`. Combine two to four keywords with site filters (GitHub topics, official docs, conference proceedings) instead of single-word queries that return noise.

2. For each candidate, capture: **name**, **URL**, **one-line purpose**, **license** if visible, and **mapping** to `AGENT_SPEC.md` dimensions (loop, tools, eval, safety, deploy, observability).

3. De-duplicate against existing citations in `wiki/research/`, examples in `wiki/examples/`, and bullets in `raw/docs/SOURCES.md` or `raw/repos/SOURCES.md` if present.

4. **Triage.** Accept, defer (needs deeper read), or reject (duplicate, low quality, license risk, or inaccessible). Record rejections briefly so the same URL is not rediscovered endlessly.

## Integration options

- **Lightweight:** Add a reference line under the relevant `wiki/research/` article or `raw/` SOURCES file.
- **Medium:** Add a short new research note if the theme is missing, then link from INDEX.
- **Deep:** Draft `wiki/examples/good/` only when you can describe architecture and tradeoffs without copying proprietary text.

## Hygiene

- Never commit API keys, cookies, or private repo URLs.
- Prefer permalinks to tagged releases or commit SHAs when pointing at code.
- Note retrieval date for fast-moving docs when the content is version-sensitive.

## Done when

- Each candidate is linked, filed under raw sources, or rejected with a one-line reason.
- `wiki/INDEX.md` is updated if a new top-level theme or section was introduced.

## Cadence

Run monthly for active curation or ad hoc before major wiki expansion work.

## Quality bar

Accept a source only if you can summarize its **agent loop** (who plans, what tools exist, how it stops) in a few sentences. Skip pure marketing pages, abandoned repos with no license, and forks that add no new architectural insight over the upstream project.
