---
marp: true
theme: default
paginate: true
title: Autoresearch Results — 7 Waves, 20 Agents, 100 Iterations
---

# Autoresearch Results
## Karpathy-Style Self-Improvement Loop

7 waves x 20 agents x ~100 iterations

---

# The Method

1. **Read** current agent state (scores, artifacts)
2. **Hypothesize** what change improves scores
3. **Edit** one dimension across all 20 agents
4. **Evaluate** using AGENT_SPEC + CLASSic scoring
5. **Keep** improvements, revert regressions

Based on [karpathy/autoresearch](https://github.com/karpathy/autoresearch)

---

# Wave 1: System Prompts (+2.5)

**Before:** Basic persona + constraints (6.5/10)
**After:** Refusal paths, HITL gates, memory strategy, cost awareness (9.0/10)

Key additions:
- Explicit "when NOT to act" rules
- Human approval gates with timeout behavior
- Memory strategy: ephemeral vs durable

---

# Wave 2: Tool Design (+3.0)

**Before:** Basic JSON schemas (6.0/10)
**After:** Error taxonomy, idempotency, pagination (9.0/10)

Key additions:
- Retryable flag on every error code
- Per-tool timeouts with backoff strategy
- Idempotency keys for mutating operations

---

# Wave 3: Source Code (+5.0)

**Before:** NotImplementedError stubs (4.0/10)
**After:** Real state machines + circuit breakers (9.0/10)

Key additions:
- AgentState enum (IDLE, PLANNING, EXECUTING, ERROR, DONE)
- Circuit breakers: max_steps, max_wall_time_s, max_spend_usd
- LLMClient as Protocol for testability

---

# Wave 4: Testing (+4.0)

**Before:** 1 happy-path test (5.0/10)
**After:** 4 test types (9.0/10)

Test types:
1. Happy path — standard multi-step flow
2. Error recovery — tool failures, retries
3. Adversarial — prompt injection, privilege escalation
4. Regression — domain-specific edge cases

---

# Wave 5: Observability (+9.0)

**Before:** Nothing (0.0/10)
**After:** Full production observability (9.0/10)

From zero to:
- SLOs with domain-specific numbers
- OpenTelemetry tracing (trace_id, span_id)
- Cost tracking per request (tokens + USD)
- Health check endpoints
- Alert rules with runbook pointers

---

# Wave 6: Documentation (+3.0)

**Before:** Basic README (6.0/10)
**After:** Production-grade docs (9.0/10)

Key additions:
- Mermaid architecture diagrams
- Environment variable matrix tables
- Honest known limitations
- Deployment + rollback guides

---

# Wave 7: Safety + Memory (+4.0)

**Before:** Generic safety notes (5.0/10)
**After:** Domain-specific threat models (9.0/10)

Key additions:
- SECURITY.md per agent (threat model, attack surface)
- HITL gates with explicit timeout behavior
- Data classification tables
- Incident response playbooks

---

# Final Scores

| Metric | Before | After | Delta |
|--------|--------|-------|-------|
| AGENT_SPEC mean | 7.6/10 | 9.04/10 | +1.44 |
| CLASSic mean | 5.5/10 | 9.02/10 | +3.52 |
| Tests per agent | 1 | 4 | +3 |
| Files per agent | ~8 | ~16 | +8 |

**All 20 agents >= 9.0/10. Zero regressions.**

---

# What We Learned

See full findings: [LEARNINGS.md](https://github.com/akijain2000/factory-showcase/blob/main/grading/autoresearch-logs/LEARNINGS.md)
