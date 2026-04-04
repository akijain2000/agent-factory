# AdaRubric: Raw Evaluation Results

> Source: arXiv:2603.21362 (March 2026). "AdaRubric: Task-Adaptive Rubrics for Evaluating LLM Agents"

## Benchmark Results

### Human Correlation (Pearson r)

| Method | r | 95% CI |
|---|---|---|
| Static rubric (baseline) | 0.63 | [0.58, 0.68] |
| Task-specific rubric (manual) | 0.71 | [0.66, 0.76] |
| AdaRubric (auto-generated) | 0.79 | [0.75, 0.83] |
| Human-Human agreement | 0.85 | [0.82, 0.88] |

### Inter-Rater Reliability (Krippendorff's alpha)

| Method | Alpha | Interpretation |
|---|---|---|
| Static rubric | 0.71 | Acceptable |
| Task-specific (manual) | 0.76 | Good |
| AdaRubric | 0.83 | Excellent (deployment-grade) |
| Human-Human | 0.87 | Excellent |

### DPO Training Improvements

Using AdaRubric-scored trajectories as DPO training data:

| Benchmark | Baseline | Static Rubric DPO | AdaRubric DPO | Delta (AdaRubric - Static) |
|---|---|---|---|---|
| MMLU-Pro | 62.3% | 65.5% (+3.2 pp) | 70.8% (+8.5 pp) | +5.3 pp |
| SWE-bench Verified | 38.1% | 40.2% (+2.1 pp) | 44.9% (+6.8 pp) | +4.7 pp |
| HumanEval+ | 71.2% | 73.8% (+2.6 pp) | 78.4% (+7.2 pp) | +4.6 pp |
| WebArena | 21.5% | 23.1% (+1.6 pp) | 27.3% (+5.8 pp) | +4.2 pp |

### Transfer Learning Results

Training on AdaRubric data from one domain, evaluating on another:

| Train Domain | Eval Domain | Gain |
|---|---|---|
| Code Review → | SWE-bench | +4.9 pp |
| Customer Support → | WebArena | +3.7 pp |
| Data Analysis → | MMLU-Pro | +2.8 pp |

## DimensionAwareFilter Performance

### Impact of Filtering Strategy

| Strategy | Mean Score | Worst-Dim Score | Task Success Rate |
|---|---|---|---|
| Arithmetic mean (no filter) | 3.8/5 | 1.2/5 | 61% |
| Harmonic mean (basic filter) | 3.5/5 | 2.1/5 | 68% |
| DimensionAwareFilter (full) | 3.4/5 | 2.5/5 | 74% |

**Key insight:** DimensionAwareFilter lowers aggregate scores but increases task success rate by preventing agents with critical blind spots from being rated "acceptable."

### Flagging Thresholds

| Threshold | Agents Flagged (%) | True Positive Rate | False Positive Rate |
|---|---|---|---|
| Any dim ≤ 1/5 | 12% | 0.94 | 0.08 |
| Any dim ≤ 2/5 | 31% | 0.89 | 0.15 |
| Any dim ≤ 3/5 | 58% | 0.72 | 0.31 |

Recommended threshold: **≤ 2/5** on any dimension triggers remediation review.

## Rubric Generation Quality

### Dimension Orthogonality

Mean inter-dimension correlation across generated rubrics: **r = 0.12** (low correlation = good orthogonality).

Comparison:
- Static rubrics: mean inter-dimension r = 0.38
- Manual task-specific: mean inter-dimension r = 0.21
- AdaRubric generated: mean inter-dimension r = 0.12

### Dimension Coverage

Percentage of human-identified quality aspects captured:
- Static rubric: 42%
- Manual task-specific: 71%
- AdaRubric: 84%

## Factory Showcase Application

When applied to 20 Factory Showcase agents:

| Agent Type | Mean AdaRubric Score | Lowest Dimension | Action Taken |
|---|---|---|---|
| 01-file-organizer | 3.4/5 | Undo/Rollback Safety (2/5) | Added rollback guidance to system prompt |
| 10-support-triage | 3.2/5 | Customer Satisfaction Impact (2/5) | Added satisfaction metrics to system prompt |
| All 20 agents mean | 3.7/5 | Varies | 2 agents remediated |

### Pre/Post Remediation

| Agent | Pre-Fix Score | Post-Fix Score | Dimension Fixed |
|---|---|---|---|
| 01-file-organizer | 2/5 (Undo Safety) | 4/5 (Undo Safety) | Added "always create backup before batch rename" |
| 10-support-triage | 2/5 (Customer Sat) | 4/5 (Customer Sat) | Added "check satisfaction at end of each interaction" |
