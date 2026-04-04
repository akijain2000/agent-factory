# Opening Agent Factory in Obsidian

This repository is configured as an [Obsidian](https://obsidian.md/) vault for browsing the knowledge base with graph view, backlinks, and search.

## Setup

1. Install [Obsidian](https://obsidian.md/) (free for personal use)
2. Open Obsidian
3. Click **Open folder as vault**
4. Select the `agent-factory/` directory
5. Trust the vault when prompted

## What you get

- **File explorer** (left panel) -- browse raw/, wiki/, course/, and outputs/
- **Graph view** (right panel) -- visualize connections between wiki articles
  - Concepts are green
  - Research articles are blue
  - Good examples are teal
  - Bad examples are red
  - Course modules are purple
- **Full-text search** -- Cmd/Ctrl+Shift+F to search across all articles
- **Backlinks** -- click any article to see what links to it

## Recommended plugins

Install from Settings > Community plugins:

| Plugin | Purpose |
|--------|---------|
| **Marp Slides** | Preview slide decks in `outputs/slides/` |
| **Dataview** | Query wiki articles by frontmatter tags/categories |
| **Graph Analysis** | Advanced graph metrics (betweenness, clusters) |

## Notes

- All links use standard Markdown `[text](path.md)` syntax (no Obsidian wikilinks)
- YAML frontmatter on wiki articles provides `category` and `tags` for Dataview queries
- The graph view color groups are pre-configured in `.obsidian/graph.json`
- CSS snippets in `.obsidian/snippets/` improve table and code block rendering
