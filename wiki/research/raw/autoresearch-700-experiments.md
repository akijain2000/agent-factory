# Karpathy Autoresearch: Raw Experiment Data

> Source: [github.com/karpathy/autoresearch](https://github.com/karpathy/autoresearch) (2025-2026)

## NanoGPT Experiment Summary

### Configuration

| Parameter | Value |
|---|---|
| Model | NanoGPT (custom transformer) |
| Dataset | OpenWebText (subset) |
| Agent | Claude (via API) |
| Duration | ~48 hours |
| Total experiments | 700+ |
| Kept optimizations | 20 |
| Acceptance rate | 2.9% |

### Training Loss Trajectory

| Experiment Range | Best Loss | Improvement from Baseline |
|---|---|---|
| Baseline | 3.28 | — |
| Experiments 1-100 | 3.21 | -2.1% |
| Experiments 101-200 | 3.14 | -4.3% |
| Experiments 201-300 | 3.08 | -6.1% |
| Experiments 301-400 | 3.04 | -7.3% |
| Experiments 401-500 | 3.00 | -8.5% |
| Experiments 501-600 | 2.95 | -10.1% |
| Experiments 601-700 | 2.92 | -11.0% |

### Diminishing Returns Pattern

| Phase | Experiments | Optimizations Kept | Keep Rate |
|---|---|---|---|
| Early (1-200) | 200 | 9 | 4.5% |
| Middle (201-500) | 300 | 8 | 2.7% |
| Late (501-700) | 200 | 3 | 1.5% |

**Observation:** Keep rate declines as low-hanging fruit is exhausted, but improvements continue accumulating.

### Categories of Kept Optimizations

| Category | Count | Example |
|---|---|---|
| Learning rate schedule | 5 | Cosine annealing with warm restarts |
| Architecture tweaks | 4 | Head dimension adjustments, layer norm placement |
| Initialization | 3 | Weight init scale, embedding initialization |
| Optimization | 3 | Gradient clipping, weight decay scheduling |
| Data processing | 3 | Tokenization, sequence packing |
| Regularization | 2 | Dropout scheduling, attention dropout |

### Categories of Discarded Experiments

| Failure Mode | Count (approx) | Example |
|---|---|---|
| No improvement | 480 | Minor hyperparameter tweaks with no effect |
| Regression | 150 | Changes that hurt training stability |
| Error/crash | 40 | Invalid configurations, OOM |
| Too slow | 10 | Changes that vastly increased training time |

## program.md Evolution

### Initial program.md (excerpt)

```markdown
# NanoGPT Optimization

## Goal
Minimize validation loss on OpenWebText while maintaining training stability.

## Constraints
- Single GPU training
- Max 10 minutes per experiment
- Must not increase parameter count by more than 10%

## Current best
- Loss: 3.28
- Config: default NanoGPT settings

## Results log
(empty)
```

### Final program.md (excerpt)

```markdown
# NanoGPT Optimization

## Goal
Minimize validation loss on OpenWebText while maintaining training stability.

## Constraints
- Single GPU training
- Max 10 minutes per experiment
- Must not increase parameter count by more than 10%

## Current best
- Loss: 2.92
- Config: see config_best.yaml

## Results log
- Exp 1: lr=3e-4→1e-3, loss 3.28→3.25, KEPT
- Exp 2: dropout 0.1→0.2, loss 3.25→3.27, DISCARDED
- ...
- Exp 700: attention_bias=True, loss 2.93→2.92, KEPT

## Known failures (do not retry)
- Dropout > 0.3: always hurts (tested 5 times)
- Batch size > 64: OOM on single GPU
- Linear warmup > 2000 steps: slows convergence
- ...
```

## Production Adaptations

### Shopify Code Generation (2026)

| Metric | Value |
|---|---|
| Domain | Code generation / completion |
| Agent | GPT-4 + custom tools |
| Iterations | 200 |
| Optimizations kept | 12 |
| Quality improvement | 19% (human preference) |
| Primary gains | Few-shot example selection, temperature tuning |

### Other Reported Adaptations

| Team / Company | Domain | Reported Gain |
|---|---|---|
| Unnamed fintech | Risk assessment prompts | 8% accuracy improvement |
| Academic group | Paper summarization | 12% ROUGE improvement |
| Startup (anon) | Customer support agent | 15% resolution rate improvement |
| This project | Factory quality (20 agents + 20 skills) | +0.7 AGENT_SPEC points, +2 validator checks |

## Key Implementation Details

### Hypothesis Generation Strategy

The LLM agent uses several strategies to generate hypotheses:

1. **Parameter sweep** — systematically try variations of a single parameter
2. **Literature-informed** — apply known best practices from ML research
3. **Error analysis** — analyze failure cases and hypothesize fixes
4. **Composition** — combine two previously successful small changes
5. **Ablation** — remove components to test necessity

### Revert Mechanism

```
if new_score > best_score:
    git commit -m "Exp {n}: {hypothesis} → {new_score} (KEPT)"
    best_score = new_score
    update program.md
else:
    git checkout -- .  # revert all changes
    log_failure(hypothesis, new_score, best_score)
    update program.md failures section
```

### Context Management

- `program.md` is re-read at the start of each iteration (fresh context)
- Long experiment histories are periodically summarized to prevent context overflow
- Failure categories are clustered to prevent re-trying equivalent ideas

## Factory Showcase Application Data

### 5-Cycle Karpathy Loop Results

| Cycle | Focus | Key Metric Change |
|---|---|---|
| 1 (Creation) | Create 10 new agents + 20 skills | Baseline: agents 7.6, skills 8.7 |
| 2 (CLASSic) | Evaluate + improve Cost/Latency/Accuracy/Stability/Security | CLASSic mean: 5.5 → 5.7 |
| 3 (AdaRubric) | Adaptive rubric evaluation + targeted fixes | 2 agents flagged and fixed |
| 4 (Traces + Validators) | Parallel trace examples + validator improvements | +2 agent checks, +2 skill checks |
| 5 (Convergence) | Final evaluation + delta report | 0 regressions, all improvements held |

### Adaptation Notes

Unlike the original NanoGPT experiment (pure automated loop), the Factory Showcase adaptation was **semi-automated**:
- Hypothesis generation: LLM-assisted but human-directed
- Scoring: Automated validators + manual grading rubrics
- Keep/discard: Based on validator results + grading improvements
- Iterations: 5 cycles (vs 700 experiments) due to human involvement per cycle

The key insight: the autoresearch pattern scales down to few-iteration loops when each iteration involves significant manual evaluation, while retaining the core principles of objective scoring, minimal diffs, and automatic revert.
