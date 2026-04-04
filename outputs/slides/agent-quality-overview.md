---
marp: true
theme: default
paginate: true
title: Agent Quality Overview — What Makes a 9/10 Agent
---

# Agent Quality Overview
## What Makes a 9/10 Agent

From 100-iteration autoresearch across 20 agents

---

# 8 Quality Dimensions (AGENT_SPEC)

| Dimension | What a 10 looks like |
|-----------|---------------------|
| Architecture | Typed state machine, circuit breakers |
| System Prompt | HITL gates, refusal paths, memory strategy |
| Tool Design | Per-tool error taxonomy with retryable flag |
| Memory | Ephemeral vs durable, retention, redaction |
| Safety | SECURITY.md, domain threat model |
| Testing | 4 scenarios: happy, error, adversarial, regression |
| Observability | SLOs, tracing, cost tracking |
| Documentation | Mermaid diagrams, env matrix, limitations |

---

# Ranked Improvements by Impact

| Wave | Dimension | Score Delta |
|------|-----------|------------|
| 5 | Observability | +9.0 |
| 3 | Source Code | +5.0 |
| 4 | Testing | +4.0 |
| 7 | Safety + Memory | +4.0 |
| 2 | Tool Design | +3.0 |
| 6 | Documentation | +3.0 |
| 1 | System Prompts | +2.5 |

---

# Anti-Patterns That Tank Scores

- **NotImplementedError stubs** → 0/10 source code
- **Happy-path-only tests** → Testing < 5
- **No circuit breakers** → runaway agents
- **Generic SLOs** → no domain understanding
- **Missing error taxonomy** → retry guessing

---

# The 9/10 Checklist

- [ ] State machine with typed enum states
- [ ] Circuit breakers: max_steps, max_wall_time_s, max_spend_usd
- [ ] Per-tool error taxonomy with retryable flag
- [ ] System prompt with refusal paths and HITL gates
- [ ] 4 test scenarios: happy, error, adversarial, regression
- [ ] SLOs with domain-specific numbers
- [ ] SECURITY.md with domain threat model
- [ ] Mermaid architecture diagram + env matrix

---

# Results

- **AGENT_SPEC mean:** 9.04/10 (was 7.6)
- **CLASSic mean:** 9.02/10 (was 5.5)
- **All 20 agents >= 9.0/10**
- **Zero regressions across 7 waves**

Learn more: [Factory Showcase LEARNINGS.md](https://github.com/akijain2000/factory-showcase)
