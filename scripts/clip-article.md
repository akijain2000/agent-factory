# Clip Article

LLM runbook for ingesting web articles, blog posts, papers, and documentation into the raw sources.

## When to use

When you find a valuable article, paper, or documentation page about agent building that should be preserved in the knowledge base. Equivalent to Obsidian's Web Clipper extension but operating via LLM.

## Procedure

### Step 1: Fetch and extract

Given a URL:

1. Fetch the page content (use `WebFetch` or browser tools)
2. Extract the **title**, **author**, **date**, and **main body text**
3. Strip navigation, ads, footers, and other chrome
4. Preserve code blocks, tables, and structured content

### Step 2: Classify the source type

Determine which category the source falls into:

| Type | Save to | Example |
|------|---------|---------|
| Reference document (guide, paper, spec) | `raw/docs/` | Anthropic's "Building Effective Agents" |
| Repository analysis | `raw/repos/SOURCES.md` (add entry) | A new agent framework repo |
| Dataset or benchmark | `raw/datasets/SOURCES.md` (add entry) | SWE-Bench results |
| Image or diagram | `raw/images/` | Architecture diagram |

### Step 3: Save in standard format

For `raw/docs/` articles, save as markdown with this header:

```markdown
# [Title]

**Source:** [URL]
**Author:** [Author name]
**Date:** [Publication date]
**Clipped:** [Today's date]

## Summary

[2-3 sentence summary of why this is valuable]

## Content

[Extracted body text in markdown]
```

### Step 4: Update manifest

Add an entry to the appropriate `SOURCES.md`:

```markdown
| [Title] | [URL] | [Author] | [Date] | [1-line summary] | course/XX, wiki/YY |
```

### Step 5: Flag for compilation

Note which existing wiki articles should be updated with the new source:

```
NEW SOURCE: [title]
AFFECTS: wiki/concepts/[article].md, wiki/research/[article].md
ACTION: Re-run compile-wiki.md for affected articles
```

## Quality checks

- Verify the URL is accessible and content extracted correctly
- Ensure no copyright-protected full reproductions (summarize long works, link to originals)
- Check for duplicate content already in `raw/docs/`
- Verify the source adds genuinely new information not already covered in the wiki
