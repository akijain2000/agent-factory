# Anatomy of a Good Agent

Production-quality agents resemble **reliable services** more than viral demos. Convergence across mature open-source harnesses (structured tool layers, explicit graphs or state machines, trace-first debugging) and vendor playbooks (Anthropic, OpenAI) yields a short list of **non-negotiables**: bounded autonomy, legible control flow, and graceful degradation under partial failure.

## Architecture clarity

Strong agents expose a **thin public surface**: task schema, policies, budgets, and machine-checkable outputs (JSON schemas, diffs, junit XML, exit codes). Internally, top repositories **factor** retrieval, planning, execution, and critique into steps with stable interfaces—closer to microservice boundaries than monolithic mega-prompts.

**State** is explicit: what is verified, what is hypothesized, what was attempted, and what failed. Implicit “conversation memory” as the sole substrate invites non-replayable bugs; production systems prefer **append-only event logs** or versioned checkpoints that support deterministic replay for debugging and regression.

## Error handling and recovery

Assume **tools lie, stall, and return partial payloads**. Recurring patterns: **idempotent** tool contracts, **backoff with jitter**, **circuit breakers** on flaky dependencies, and **escalation ladders** (small model for triage, frontier model for synthesis, human for irreversible actions). Errors carry **correlation IDs** and land in structured logs; they are not swallowed to preserve conversational polish.

Recovery should be **policy-driven**: after N failures, narrow scope, switch strategy, or halt. This aligns with “workflows before agents”—deterministic fallbacks often beat optimistic infinite replanning.

## Testing and verification

Investment shifts from brittle string matching to **behavioral tests**: golden traces for representative tasks, **contract tests** for tools (schemas, timeouts, sandbox egress), and **regression suites** gated on prompt or model changes. Where stakes are high, **dual verification** appears—execution, linters, or tests as primary; LLM-as-judge only as a secondary signal.

## Documentation and operability

“Good” documentation includes **runbooks**: key rotation, quotas, queue draining, trace field semantics, and kill switches. Separate narratives for **operator**, **integrator**, and **safety reviewer** personas reduce mean-time-to-recovery.

Budgets—max steps, cost, wall clock—and **explicit stop conditions** belong in the same tier as feature specs for production acceptance.

## Patterns from top repositories

Common motifs: **structured outputs** at boundaries; **minimal tool sets** with sharp descriptions; **observability** (OpenTelemetry-style spans, JSONL); **sandboxed** code and shell; **progressive disclosure** of context (skills and docs loaded on demand).

## Security and cost posture

Treat the model as **untrusted** for exfiltration and privilege escalation: secret separation, short-lived credentials, egress policies per tool. Declare **cost bands** per task class; route cheap models to classification and reserve frontier capacity for high-uncertainty synthesis.

## Release engineering for agents

Align **prompt**, **tool**, and **model** pins in release artifacts. Rollouts should support **shadow** traffic (new prompt, old model) and **instant rollback** when error budgets breach. Feature flags per **tool** beat global kill switches when diagnosing incidents.

## On-call signals

Page on **error-rate spikes**, **cost anomalies**, and **sudden refusal-rate** changes—the latter often tracks provider policy updates more than your code.

## Summary

Production agents win on **clarity** (interfaces, state), **honesty** about failures, and **operability** (traces, budgets, runbooks)—not maximal autonomy. Treat the model as one **unreliable** component in an otherwise disciplined system.

## Human-in-the-loop without approval fatigue

Batch **low-risk** confirmations, default-deny **high-risk** tools, and surface **dry-run** previews where possible. Operators tolerate frequent nudges when each nudge is **specific** (what will run, on which resources) rather than generic “the agent wants permission.”

## Sources and further reading

- Anthropic, *Building Effective Agents* (2024): workflow-first decomposition.
- OpenAI, Agents SDK documentation: guardrails, tracing, handoffs.
- OpenTelemetry and structured logging practices for LLM applications.

## See also

- [Anti-patterns](anti-patterns.md)
- [Agent vs workflow](agent-vs-workflow.md)
- [Production case studies](production-case-studies.md)
- [Framework comparison](framework-comparison.md)
- Concepts: [Agent Loop](../concepts/agent-loop.md), [Error Recovery](../concepts/error-recovery.md), [Agent Testing Patterns](../concepts/agent-testing-patterns.md), [Observability](../concepts/observability.md), [Agent Security](../concepts/agent-security.md)
- Course: [Agent Factory course](../../course/README.md)
