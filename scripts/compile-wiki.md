# Compile Wiki (LLM runbook)

Use this runbook when raw notes, transcripts, exports, or external sources must become polished wiki articles under `wiki/`, consistent with `AGENT_SPEC.md` vocabulary and Agent Factory tone.

## Preconditions

- Raw material exists (bullets, outline, pasted doc, or repo URL plus allowed excerpt).
- Target bucket is chosen: `wiki/concepts/`, `wiki/research/`, or `wiki/examples/` (use `good/` or `bad/` under examples as appropriate).
- You have read a sibling article in the same folder to match heading depth and voice.

## Steps

1. **Normalize inputs.** Remove boilerplate, fix heading hierarchy (single H1 per file), and split sources that cover multiple theses into separate files. Name files `kebab-case.md` and align with naming patterns in `wiki/INDEX.md`.

2. **Align structure.** Open with one H1 title. Use sections comparable to neighbors: Context, Key ideas, Tradeoffs, References (adjust labels if the folder convention differs). Use relative links only.

3. **Cross-link.** Link to `wiki/GLOSSARY.md` terms and related concept articles. If the page is new, add a short entry or anchor path in `wiki/INDEX.md` so it is discoverable.

4. **Fact hygiene.** Label inference and open questions explicitly. Prefer primary sources in References; avoid long verbatim copies that may violate licenses.

5. **Examples discipline.** In `wiki/examples/`, state the pattern, failure modes, and what to copy versus avoid. For `bad/`, explain the anti-pattern and link to the good counterpart when one exists.

6. **Consistency pass.** Re-read INDEX for duplicate titles. Ensure no second H1 in the same file and that links resolve to paths that exist or are intentionally external.

## Output expectations

- One merged markdown file per logical article (or a clear series with cross-links).
- INDEX updated when navigation would otherwise miss the new material.

## Done when

- The article renders as valid Markdown, matches sibling tone, and INDEX (or a parent page) points to it.
- References are checked for obvious breakage; speculative claims are marked.

## Escalation

If scope spans multiple domains, split into multiple files and link them rather than one megapage. If raw sources conflict, document the conflict in References instead of silently picking one version.

## Cadence

Run after each import batch or when course modules reference wiki pages that do not yet exist.
