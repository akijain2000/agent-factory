# Dataset Sources

Structured data files for chart generation, evaluation baselines, and analysis.

Last updated: 2026-04-04

## Datasets

| File | Format | Records | Description |
|------|--------|---------|-------------|
| `autoresearch-scores.json` | JSON | 20 agents x 8 dims + 5 CLASSic | Final AGENT_SPEC and CLASSic scores from 7-wave autoresearch loop |
| `wave-improvements.csv` | CSV | 7 waves | Per-wave score deltas with before/after and key insight |
| `agent-progression.csv` | CSV | 20 agents x 3 stages | Score progression: Cycle 1 → Cycle 5 → Final |

## Provenance

All data extracted from [Factory Showcase](https://github.com/akijain2000/factory-showcase) grading reports:
- `grading/autoresearch-final.md` -- final 8-dimension and CLASSic scores
- `grading/autoresearch-delta.md` -- progression from Cycle 1 through Cycle 5 to Final
- `grading/autoresearch-logs/wave-*.md` -- per-wave learning logs

## Usage

```bash
# Generate charts from this data
python outputs/charts/generate-charts.py

# Load in Python
import json
with open("raw/datasets/autoresearch-scores.json") as f:
    data = json.load(f)
```
