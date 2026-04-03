# Goose: Extensible Agent via Plugins

## Summary

Goose (as a pattern) centers on a **small core agent** that handles reasoning, tool invocation, and session lifecycle, while **capabilities arrive through plugins**: connectors to APIs, custom tools, project-specific workflows, and optional UI. The core stays stable; extensions ship as isolated packages with declared interfaces and permissions.

## Pattern

**Composition over monolith.** Plugins export a narrow contract—tool definitions, metadata, initialization hooks, and optional context providers. The core orchestrator discovers plugins, merges tool registries with deduplication rules, and enforces capability boundaries (which plugin may access which secrets or paths).

## What makes it good

Teams can add domain behavior without forking the agent runtime. Versioning and dependency boundaries are clearer than stuffing every integration into one repository. Security reviews can scope to “what does this plugin expose?” rather than re-auditing the entire stack on each change.

Users get a familiar mental model: the **same agent**, different **capability sets** per project or role.

### In practice

Ship a manifest per plugin listing permissions, required env vars, and compatible core versions. Run plugin tests in isolation with mocked tool backends. Provide a CLI flag or workspace file that enables only the plugins needed for the current repo to reduce accidental cross-project access.

### Failure modes this design mitigates

Monoliths tend toward **tool soup**—dozens of overlapping endpoints with unclear ownership. Plugins force boundaries and let you disable entire capability bundles when an integration is compromised or deprecated.

### When to reconsider

If you only ever need three tools and one team owns them all, a tiny inline registry is fine. Introduce plugin architecture when **third parties** or **many internal teams** extend the same runtime.

## Key takeaway

**Extend agents through well-typed plugin surfaces**, not by inflating a single global tool list and prompt.

## Review checklist

- [ ] Is the active tool set small enough to name from memory?
- [ ] Are transitions or handoffs explicit in code, not only in prose?
- [ ] Do traces identify phase, tool, and outcome for each step?
- [ ] Are step, cost, and time limits enforced in the host, not the model?
- [ ] Can you replay a failed run with mocks for tools and LLM?
- [ ] Are high-risk actions behind sandbox, schema validation, or human approval?

## Metrics and evaluation

Define SLIs for the loop: success rate per task type, median steps to completion, tool-error ratio, and cost per successful outcome. Store traces with default PII redaction and retain enough detail to replay decisions. Run periodic canaries on pinned prompts and tool versions to catch provider or dependency drift before users do.

## Contrast with common failures

For unstructured alternatives and their failure modes, see [God agent](../bad/god-agent.md), [Over-tooled agent](../bad/over-tooled-agent.md), and the wiki [Anti-patterns](../../research/anti-patterns.md) catalog.

## See also

- [Agent composition](../../concepts/agent-composition.md)
- [Tool selection](../../concepts/tool-selection.md)
- [Deployment patterns](../../concepts/deployment-patterns.md)
- [Agent orchestration platforms](../../concepts/agent-orchestration-platforms.md)
- [Harness engineering](../../concepts/harness-engineering.md)
