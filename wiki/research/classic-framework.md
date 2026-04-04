# CLASSic Framework: Operational Agent Evaluation

## Overview

The **CLASSic** framework (Zylos Research, 2026) provides a five-dimensional evaluation methodology for assessing AI agent production-readiness. Unlike design-focused quality standards (e.g., AGENT_SPEC's 8 architectural dimensions), CLASSic targets **operational** concerns that determine whether an agent survives contact with real users.

The framework emerged from analysis of **2,100+ real enterprise messages** across **7 industry domains** (finance, healthcare, legal, retail, logistics, education, technology).

## The Five Dimensions

### 1. Cost (C)

How efficiently does the agent use compute resources?

| Score | Anchor |
|---|---|
| 0-2 | No awareness of token consumption; unbounded API calls; no model tiering |
| 3-4 | Basic token counting; single model with no routing |
| 5-6 | Model routing (cheap for simple, expensive for complex); budget warnings |
| 7-8 | Per-task cost tracking; automatic downgrade under budget pressure; cost-per-outcome metrics |
| 9-10 | Predictive cost estimation before execution; Pareto-optimal model selection; user-facing cost transparency |

**Signals in agent files:**
- `system-prompt.md`: mentions tokens, budget, cost, model tiers
- `tools/`: cost estimation tools, budget-check tools
- `src/`: token counting, model routing logic
- `tests/`: budget exhaustion scenarios

### 2. Latency (L)

How fast does the agent respond, and does it manage user expectations?

| Score | Anchor |
|---|---|
| 0-2 | No streaming; sequential tool calls; no timeout handling |
| 3-4 | Basic streaming; fixed timeouts |
| 5-6 | Parallel tool execution where independent; progress indicators |
| 7-8 | P95/P99 latency targets; adaptive concurrency; partial result delivery |
| 9-10 | Predictive prefetching; sub-second for cached paths; latency budgets per step |

**Signals in agent files:**
- `system-prompt.md`: streaming, parallel, timeout, progress
- `tools/`: async execution, batch operations
- `src/`: concurrency, caching, prefetch

### 3. Accuracy (A)

How reliable are the agent's outputs?

| Score | Anchor |
|---|---|
| 0-2 | No output validation; no source citation; hallucination-prone |
| 3-4 | Basic format validation; some source grounding |
| 5-6 | Self-verification steps; confidence scoring; structured output schemas |
| 7-8 | Multi-source cross-validation; uncertainty quantification; fact-checking tools |
| 9-10 | Formal verification where applicable; calibrated confidence intervals; zero-hallucination architecture |

**Signals in agent files:**
- `system-prompt.md`: verify, validate, check, confirm, cite, source
- `tools/`: verification tools, fact-checking, schema validation
- `tests/`: accuracy benchmarks, hallucination probes

### 4. Stability (S)

How consistently does the agent behave across varied inputs and conditions?

| Score | Anchor |
|---|---|
| 0-2 | No retry logic; crashes on unexpected input; inconsistent output format |
| 3-4 | Basic error handling; single retry |
| 5-6 | Exponential backoff; graceful degradation; structured error responses |
| 7-8 | Idempotent operations; deterministic output format; chaos testing |
| 9-10 | Self-healing; automatic failover; consistent behavior across model versions |

**Signals in agent files:**
- `system-prompt.md`: retry, fallback, degrade, consistent, idempotent
- `tools/`: health checks, circuit breakers
- `tests/`: edge cases, malformed input, high-load scenarios

### 5. Security (S)

How well does the agent protect against adversarial inputs and unauthorized actions?

| Score | Anchor |
|---|---|
| 0-2 | No input sanitization; tools accept arbitrary input; no privilege model |
| 3-4 | Basic input validation; some restricted operations |
| 5-6 | Prompt injection defenses; least privilege tool design; output filtering |
| 7-8 | Defense-in-depth; audit logging; sandboxed execution; HITL for destructive ops |
| 9-10 | Formal threat model; red-team tested; zero-trust architecture; cryptographic verification |

**Signals in agent files:**
- `system-prompt.md`: sanitize, validate input, restrict, audit, permission
- `tools/`: input constraints, privilege levels, confirmation gates
- `tests/`: injection probes, privilege escalation attempts

## Comparison to AGENT_SPEC

| Aspect | AGENT_SPEC | CLASSic |
|---|---|---|
| Focus | Design quality | Operational readiness |
| Dimensions | 8 (Architecture, System Prompt, Tool Design, Memory, Safety, Testing, Observability, Documentation) | 5 (Cost, Latency, Accuracy, Stability, Security) |
| When to use | During agent authoring | During production evaluation |
| Overlap | Safety dimension | Security dimension (partial) |
| Score range | 0-10 per dimension | 0-10 per dimension |

**Best practice:** Use AGENT_SPEC during design/authoring (before deployment) and CLASSic during operational evaluation (before and after deployment). An agent scoring 8+ on AGENT_SPEC but <5 on CLASSic Cost is well-designed but unaffordable.

## Application in Factory Showcase

In the Karpathy loop (Cycles 2-5), CLASSic evaluation revealed:
- **Mean initial score:** 5.5/10 across 20 agents
- **Weakest dimension:** Cost (many agents had zero cost awareness)
- **Post-improvement mean:** 5.7/10 (targeted prompt updates to bottom 5 agents)
- **Key finding:** AGENT_SPEC score correlates with CLASSic Accuracy (r≈0.6) but poorly with Cost (r≈0.2)

## References

- Zylos Research (2026). "CLASSic: A Framework for Evaluating Enterprise AI Agents"
- Factory Showcase Cycle 2 Report: `factory-showcase/grading/cycle-2-classic.md`
- CLASSic evaluator template: `factory-showcase/scripts/classic-evaluator.md`

## See also

- [Agent evaluation methods](agent-evaluation-methods.md)
- [AdaRubric evaluation](adarubric-evaluation.md)
- [Cost analysis](cost-analysis.md)
- [Raw CLASSic data](raw/classic-enterprise-data.md)
