# Agent Composition

## What it is

**Agent composition** builds complex behavior from **smaller, testable units**: modular **tool sets**, **sub-agents** with narrow contracts, **plugins** (load capabilities per tenant or task), and shared **harness** primitives (retry, validation, tracing). Frameworks and products vary; the **Goose** ecosystem exemplifies composable agents where extensions add tools and prompts without forking the core loop—composition is explicit in configuration, not only in prompt prose.

## Why it matters for agents

Monolithic prompts and flat tool dumps do not scale: context fills, responsibilities blur, and changes risk unintended side effects. Composition enables **reuse**, **A/B** at component granularity, and **least privilege** (load only the tool subset needed for a session). It also mirrors how teams ship: different owners can evolve plugins independently if contracts are stable.

## How to implement it

1. **Define capability bundles:** group tools by domain (`billing`, `docs`, `deploy`) and mount bundles per workflow or role.
2. **Sub-agents as functions:** inputs and outputs are structured; no shared scratchpad unless intentionally designed; parent orchestrator owns global state.
3. **Plugin manifest:** name, version, required secrets, tool schemas, and compatibility flags; validate at load time.
4. **Stable harness API:** logging, cancellation, budget checks, and schema validation live in the core, not in each extension.
5. **Avoid cyclic delegation:** cap delegation depth; detect ping-pong between specialists in traces.
6. **Test composition:** integration tests for each bundle plus a smoke suite for default stacks.

## Goose-oriented pattern

Treat extensions as **first-class packages**: declarative registration, isolated dependencies where possible, and documentation that states **when** the extension should be enabled. Prefer **narrow tool surfaces** per extension over one mega-plugin that reimplements half the platform.

## Composition vs multi-agent

Composition can be **in-process** (one loop, dynamic tools) or **multi-process** (agents as services). Choose in-process when latency and debugging simplicity dominate; choose services when scaling, isolation, or team boundaries require it.

## Interface contracts between components

Expose **typed** inputs and outputs between sub-agents and plugins (`RequestContext`, `ToolResult`, `PlanStep`). Version interfaces; deprecate with dual-write periods in tests. Avoid passing raw conversation strings across boundaries unless that is the explicit contract.

## Goose-style extensibility in practice

Ship a **core** package with loop, auth, and telemetry; ship **extensions** as separate packages declaring contributed tools and optional prompt fragments. Run **compatibility tests** in CI that load the core with each first-party extension to catch import-time failures early.

## Scaling composition

As the number of bundles grows, add a **registry** with discovery metadata and dependency ordering (e.g., `docs` before `deploy` validators). Monitor **load time** and **context size** when many extensions are enabled—composition should not linearly inflate every session.

## Common mistakes

- Loading every tool for every session “just in case.”
- Sub-agents without explicit output schemas, making merge steps fragile.
- Hidden cross-dependencies between plugins discovered only in production.
- Copy-pasting prompts between components instead of shared, versioned fragments.

## References to course modules

These map to the **23-module Agent Factory course** (see [`../../course/README.md`](../../course/README.md) when published).

- **Module 10 — Multi-Agent Roles & Specialization** — orchestration patterns.
- **Module 11 — Tool Catalogs & Least Privilege** — bundling and mounting tools.
- **Module 13 — Plugins, Extensions, and Composable Harnesses** — Goose-style architecture.

Full curriculum index: [`../../course/README.md`](../../course/README.md) (when present).

## See also

- [Tool Design](tool-design.md)
- [Tool Selection](tool-selection.md)
- [Multi-Agent Orchestration](multi-agent-orchestration.md)
- [Progressive Complexity](progressive-complexity.md)
- [State Management](state-management.md)
