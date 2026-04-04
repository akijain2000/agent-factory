# AdaRubric: Task-Adaptive Evaluation for LLM Agents

## Overview

**AdaRubric** (arXiv:2603.21362, March 2026) addresses a fundamental limitation of static evaluation rubrics: different agent tasks require different quality dimensions. A code-review agent needs "Coverage Completeness" and "Actionability of Feedback"; a database admin needs "DDL Safety" and "Backup Discipline." Fixed rubrics either miss domain-specific failures or waste evaluator attention on irrelevant dimensions.

## The Three-Stage Pipeline

### Stage 1: Rubric Generator

Given a task description and agent type, the rubric generator produces N orthogonal evaluation dimensions with calibrated 5-point scoring criteria.

**Universal dimensions** (always included):
1. **Task Completion Fidelity** — Does the agent accomplish its stated purpose end-to-end?
2. **Failure Mode Coverage** — Are error paths, edge cases, and degraded states handled?

**Domain-specific dimensions** (3-5 generated per agent type):

| Agent Type | Example Dimensions |
|---|---|
| Code Review | Coverage Completeness, Actionability of Feedback, False Positive Rate |
| Database Admin | DDL Safety, Backup Discipline, Query Optimization Awareness |
| Customer Support | Empathy Calibration, Escalation Timing, Resolution Rate |
| File Organizer | Undo/Rollback Safety, Taxonomy Consistency, Metadata Preservation |
| Security Auditor | Threat Coverage, False Alarm Rate, Remediation Specificity |

### Stage 2: Trajectory Evaluator

Each agent step is scored per-dimension with confidence-weighted feedback. The evaluator examines:

- Tool call sequences and their outcomes
- Intermediate reasoning quality
- Error handling behavior
- Final output against task requirements

Scoring uses a 5-point scale with anchored definitions per dimension:
- **1**: Absent — dimension not addressed at all
- **2**: Minimal — token effort, major gaps
- **3**: Adequate — basic competence, some misses
- **4**: Strong — thorough coverage, minor improvements possible
- **5**: Exemplary — exceeds expectations, could serve as reference

### Stage 3: DimensionAwareFilter

Prevents high scores on one dimension from masking failures on another. Key rules:

- Any dimension scoring **1/5** flags the agent for immediate remediation regardless of aggregate score
- Aggregate scores are computed as **harmonic mean** (not arithmetic) to penalize low outliers
- Dimensions with high variance across test cases trigger additional probing
- Output includes both per-dimension breakdowns and a filtered aggregate

## Key Results

| Metric | AdaRubric | Best Static Baseline | Improvement |
|---|---|---|---|
| Pearson r (human correlation) | 0.79 | 0.63 | +0.16 |
| Krippendorff alpha (reliability) | 0.83 | 0.71 | +0.12 |
| DPO training gain (MMLU-Pro) | +8.5 pp | +3.2 pp | +5.3 pp |
| DPO training gain (SWE-bench) | +6.8 pp | +2.1 pp | +4.7 pp |
| Transfer learning (cross-domain) | +4.9 pp | N/A | N/A |

## Practical Application

### When to use AdaRubric vs. AGENT_SPEC vs. CLASSic

| Framework | Focus | When |
|---|---|---|
| AGENT_SPEC | Structural quality (8 design dimensions) | Agent authoring |
| CLASSic | Operational readiness (Cost, Latency, Accuracy, Stability, Security) | Production evaluation |
| AdaRubric | Task-specific behavioral quality (N adaptive dimensions) | Behavioral testing per task type |

### Implementation guidance

1. Generate rubric dimensions **before** running evaluation (not post-hoc)
2. Include universal dimensions in every rubric (Task Completion, Failure Modes)
3. Generate 3-5 domain-specific dimensions from the agent's task description
4. Use **harmonic mean** for aggregate scoring
5. Flag any dimension below 2/5 for mandatory remediation
6. Store generated rubrics alongside test results for reproducibility

## Application in Factory Showcase

In the Karpathy loop (Cycle 3), AdaRubric evaluation revealed:
- **Mean score:** 3.7/5.0 across 20 agents
- **Flagged dimensions:** `01-file-organizer` "Undo/Rollback Safety" (2/5), `10-support-triage` "Customer Satisfaction Impact" (2/5)
- **Post-fix:** Both agents improved by adding specific guidance to system prompts
- **Key finding:** Agents scoring 8+ on AGENT_SPEC could still score 2/5 on domain-specific AdaRubric dimensions—confirming that design quality ≠ behavioral quality

## References

- arXiv:2603.21362 (March 2026). "AdaRubric: Task-Adaptive Rubrics for Evaluating LLM Agents"
- Factory Showcase Cycle 3 Report: `factory-showcase/grading/cycle-3-adarubric.md`
- AdaRubric generator template: `factory-showcase/scripts/adarubric-generator.md`

## See also

- [CLASSic framework](classic-framework.md)
- [Agent evaluation methods](agent-evaluation-methods.md)
- [Raw AdaRubric data](raw/adarubric-results.md)
