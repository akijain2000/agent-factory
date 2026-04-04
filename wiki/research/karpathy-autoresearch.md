# Karpathy Autoresearch: Self-Improving Agent Pattern

## Overview

The **autoresearch** pattern (Andrej Karpathy, 2025-2026) formalizes score-driven LLM self-improvement into a reproducible loop. An LLM agent reads a living document (`program.md`), hypothesizes improvements, makes minimal edits, evaluates against an objective scorer, and keeps or discards changes—all autonomously within safety bounds.

Originally demonstrated on NanoGPT training optimization, the pattern has been adapted to prompt engineering, code optimization, and factory-quality improvement (this project).

**Repository:** [github.com/karpathy/autoresearch](https://github.com/karpathy/autoresearch)

## Architecture

### Core Components

```
┌─────────────────────────────────────────────────┐
│                   program.md                     │
│  - Goal description                              │
│  - Current best configuration                    │
│  - Constraints and safety rules                  │
│  - Results log (iteration, hypothesis, outcome)  │
│  - Known failures (do not retry)                 │
└──────────────────┬──────────────────────────────┘
                   │ reads fresh each iteration
                   ▼
┌─────────────────────────────────────────────────┐
│               LLM Agent                          │
│  1. Parse current state from program.md          │
│  2. Review past experiments and failures         │
│  3. Generate hypothesis ("change X because Y")   │
│  4. Produce minimal diff (single variable)       │
└──────────────────┬──────────────────────────────┘
                   │ applies change
                   ▼
┌─────────────────────────────────────────────────┐
│            prepare.py (optional)                 │
│  - Data preparation, preprocessing               │
│  - Environment setup                              │
└──────────────────┬──────────────────────────────┘
                   │
                   ▼
┌─────────────────────────────────────────────────┐
│              train.py / evaluate.sh              │
│  - Objective scorer                               │
│  - Returns numeric metric(s)                      │
│  - Deterministic given same inputs + seed         │
└──────────────────┬──────────────────────────────┘
                   │ score
                   ▼
┌─────────────────────────────────────────────────┐
│           Keep / Discard Decision                │
│  score > baseline → keep, update program.md      │
│  score ≤ baseline → discard, log to failures     │
│  error/crash → discard, log error class           │
└──────────────────┬──────────────────────────────┘
                   │
                   └── loop (bounded by max_iterations)
```

### File Roles

| File | Role | Analogy |
|---|---|---|
| `program.md` | Living experiment log + instructions | Lab notebook |
| `prepare.py` | Data/environment setup | Experimental apparatus |
| `train.py` | Objective scorer | Measurement instrument |
| Agent (LLM) | Hypothesis generator + implementer | Researcher |

## Design Principles

### 1. program.md as Durable Context

The context window is finite and ephemeral. `program.md` survives across iterations, providing:
- The agent's complete history of what worked and what failed
- Explicit constraints that prevent re-trying known-bad ideas
- Current best configuration as the baseline to beat

### 2. Objective Scorer Required

Self-assessed improvement is unreliable. The scorer must be:
- **External** to the agent (not the agent grading itself)
- **Deterministic** or low-variance (same inputs → same score ± small noise)
- **Aligned** with actual goals (not Goodhartable without real consequence)

### 3. Minimal Diffs

Each iteration changes **one thing**. Benefits:
- Clear attribution of score changes to specific modifications
- Easy revert on regression
- Human-auditable experiment log

### 4. Automatic Revert on Regression

No degradation is tolerated. If score drops or stays equal, the change is discarded and logged as a failure. This creates a **monotonically non-decreasing** quality trajectory.

### 5. Bounded Autonomy

The loop runs within guardrails:
- Maximum iteration count
- Time budget
- File/directory write scope
- Disallowed operations list

## Adaptation to Non-ML Domains

| Domain | program.md Content | Scorer | Score Metric |
|---|---|---|---|
| **ML training** | Model config, hyperparameters | `train.py` | Validation loss |
| **Prompt engineering** | System prompt, few-shot examples | Eval suite runner | Task success rate (%) |
| **Code optimization** | Source code, perf targets | Benchmark harness | Runtime (ms), memory (MB) |
| **Content generation** | Style guide, topic constraints | Preference model | Human preference score |
| **Factory quality** | AGENT_SPEC + SKILL_SPEC + validators | Validator + manual grading | Pass rate + mean quality score |
| **API design** | OpenAPI spec, test cases | Contract test suite | Coverage + error rate |

## Results

### Original NanoGPT Experiment

- **Duration:** ~2 days fully autonomous
- **Experiments run:** 700+
- **Optimizations kept:** 20 (2.9% acceptance rate)
- **Training loss improvement:** 11%
- **Key optimizations discovered:** learning rate schedules, architectural tweaks, initialization strategies

### Production Adaptations

- **Shopify:** 19% improvement in code generation quality using autoresearch on prompt engineering
- **Various teams:** Reported 5-15% improvements in agent task success rates

### Factory Showcase (This Project)

5-cycle Karpathy loop applied to 20 agents + 20 skills:

| Metric | Cycle 1 (Baseline) | Cycle 5 (Final) | Delta |
|---|---|---|---|
| Agent AGENT_SPEC mean | 7.6/10 | 8.3/10 | +0.7 |
| Skill quality mean | 8.7/10 | 8.7/10 | 0.0 (already high) |
| CLASSic coverage | 0% agents | 100% agents | +100% |
| AdaRubric flagged dims | Not measured | 2 (fixed) | N/A |
| Agent validator checks | 8 | 10 | +2 |
| Skill validator checks | 13 | 15 | +2 |
| Regressions | N/A | 0 | Clean |

## Implementation Checklist

For teams adopting the autoresearch pattern:

- [ ] Define `program.md` with clear goal, constraints, and scoring criteria
- [ ] Build deterministic scorer (`train.py` / `evaluate.sh`)
- [ ] Set iteration budget (start with 50, scale to 500+)
- [ ] Define write scope (which files/configs may change)
- [ ] Implement automatic git commit on keep / revert on discard
- [ ] Add failure logging to prevent re-trying known-bad hypotheses
- [ ] Set up monitoring for score trajectory over time
- [ ] Review kept changes periodically for Goodharting signals

## Anti-Patterns

1. **Scorer gaming** — Agent discovers loopholes in the metric. Mitigation: held-out tasks, diverse metrics, periodic human review.
2. **Hypothesis starvation** — After many iterations, all simple improvements are found. Mitigation: encourage the agent to try compositional changes or read external literature.
3. **Confounded experiments** — Multiple changes per iteration. Mitigation: enforce single-variable diffs, reject multi-change proposals.
4. **Stale program.md** — The living document grows so large the agent loses signal. Mitigation: periodically summarize and archive old experiments.

## References

- Karpathy, A. (2025). "autoresearch" — [github.com/karpathy/autoresearch](https://github.com/karpathy/autoresearch)
- Factory Showcase Delta Report: `factory-showcase/grading/delta-report.md`
- Factory Showcase Improvements Log: `factory-showcase/improvements.md`

## See also

- [AutoAgent harness patterns](autoagent-harness-patterns.md)
- [CLASSic framework](classic-framework.md)
- [AdaRubric evaluation](adarubric-evaluation.md)
- [Raw autoresearch data](raw/autoresearch-700-experiments.md)
