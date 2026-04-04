# CLASSic Framework: Raw Enterprise Data

> Source: Zylos Research (2026). "CLASSic: A Framework for Evaluating Enterprise AI Agents"

## Dataset Overview

- **Total messages analyzed:** 2,100+
- **Industry domains:** 7
- **Evaluation dimensions:** 5 (Cost, Latency, Accuracy, Stability, Security)
- **Scoring scale:** 0-10 per dimension

## Domain Distribution

| Domain | Messages | Typical Agent Types |
|---|---|---|
| Finance | ~350 | Trading assistants, compliance checkers, risk analysts |
| Healthcare | ~300 | Clinical decision support, scheduling, triage |
| Legal | ~250 | Document review, contract analysis, case research |
| Retail | ~350 | Customer service, inventory, recommendation |
| Logistics | ~300 | Route optimization, warehouse management, tracking |
| Education | ~250 | Tutoring, grading, curriculum planning |
| Technology | ~300 | Code review, DevOps, documentation |

## Dimension Definitions with Scoring Anchors

### Cost Dimension (0-10)

Measures token efficiency, model routing intelligence, and budget awareness.

**Scoring distribution across enterprise agents:**
- Mean: 4.2/10
- Median: 4.0/10
- Std dev: 2.1
- Min observed: 0 (no cost awareness)
- Max observed: 9 (predictive cost estimation with user transparency)

**Key finding:** Cost was the weakest dimension across all domains. Most agents treat model API calls as free, with no budget tracking or model tiering.

### Latency Dimension (0-10)

Measures response time management, streaming, and parallel execution.

**Scoring distribution:**
- Mean: 5.8/10
- Median: 6.0/10
- Std dev: 1.8
- Most common gap: No parallel tool execution (sequential chains of 5+ calls)

### Accuracy Dimension (0-10)

Measures output correctness, self-verification, and hallucination control.

**Scoring distribution:**
- Mean: 6.1/10
- Median: 6.0/10
- Std dev: 1.9
- Domain variance: Healthcare highest (7.2), Retail lowest (5.3)

### Stability Dimension (0-10)

Measures consistency, error handling, and graceful degradation.

**Scoring distribution:**
- Mean: 5.5/10
- Median: 5.5/10
- Std dev: 1.7
- Key gap: Most agents lack idempotent operation design

### Security Dimension (0-10)

Measures input sanitization, privilege management, and adversarial robustness.

**Scoring distribution:**
- Mean: 4.8/10
- Median: 5.0/10
- Std dev: 2.3
- Domain variance: Finance highest (6.5), Education lowest (3.1)

## Cross-Dimension Correlations

| | Cost | Latency | Accuracy | Stability | Security |
|---|---|---|---|---|---|
| **Cost** | 1.0 | 0.31 | 0.15 | 0.22 | 0.18 |
| **Latency** | | 1.0 | 0.28 | 0.45 | 0.12 |
| **Accuracy** | | | 1.0 | 0.52 | 0.38 |
| **Stability** | | | | 1.0 | 0.41 |
| **Security** | | | | | 1.0 |

**Notable correlations:**
- Accuracy-Stability (r=0.52): Agents that verify outputs also tend to handle errors well
- Latency-Stability (r=0.45): Agents with timeout handling also implement retries
- Cost-Accuracy (r=0.15): Weak correlation — expensive agents are not necessarily more accurate

## Enterprise Readiness Thresholds

Based on deployment success rates in the study:

| CLASSic Mean | Deployment Outcome |
|---|---|
| < 3.0 | Prototype only; not recommended for production |
| 3.0-5.0 | Internal use with supervision; incident-prone |
| 5.0-7.0 | Production-ready with monitoring; occasional issues |
| 7.0-9.0 | Production-grade; suitable for external-facing use |
| > 9.0 | Exceptional; observed only in mature, well-funded teams |

## Factory Showcase Comparison

When applied to the 20 Factory Showcase agents:

| Metric | Enterprise Dataset | Factory Showcase |
|---|---|---|
| Mean CLASSic score | 5.3/10 | 5.5/10 (pre-improvement) |
| Weakest dimension | Cost (4.2) | Cost (4.8) |
| Strongest dimension | Accuracy (6.1) | Accuracy (6.2) |
| Post-improvement mean | N/A | 5.7/10 |

The Factory Showcase agents tracked enterprise averages closely, validating CLASSic as a relevant evaluation framework for agent-factory outputs.
