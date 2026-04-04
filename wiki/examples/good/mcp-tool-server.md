---
category: example-good
tags: [mcp, tool-server, protocol]
---

# MCP Tool Server: Protocol-First Tooling

## Summary

A Model Context Protocol (MCP) server exposes **resources and tools** to any compatible client over a standard wire format. Agents in Cursor, Claude Desktop, or custom harnesses discover tool names, descriptions, and JSON schemas the same way, without each framework re-implementing ad hoc adapters for every integration.

## Pattern

**Protocol-based, framework-agnostic tool surface.** Tools are declared with machine-readable schemas; the server handles execution, authentication to upstream APIs, and optional progress streaming. Clients treat MCP as a **capability provider** the model can call through a uniform interface.

## What makes it good

One implementation of “query the internal wiki” or “run the approved SQL template” can serve multiple agent frontends. Schema-first definitions reduce argument drift between demos and production. Composability improves: teams ship small MCP servers per domain instead of monolithic “tool bags” inside each app.

Security can centralize on the server (allowlists, audit logs, rate limits) rather than scattering checks across every caller.

### In practice

Version MCP tool schemas alongside server releases. Document which secrets the server needs and how they are scoped per tenant. For high-risk tools, require a second token or human-approved session ID passed as an argument the model cannot forge without host cooperation.

### Failure modes this design mitigates

Without a protocol, each IDE or chat UI reinvents brittle adapters—schema drift and silent breakage follow. MCP pushes **contract-first** tooling. Centralized servers also mean one place to patch SSRF or injection bugs in tool backends.

### When to reconsider

For tools that must run **on the user’s laptop** with zero network exposure, a local MCP server is ideal. For ultra-low-latency inline functions, calling Python directly in-process may win—expose those via MCP only when multiple clients need them.

## Key takeaway

**Standardize how tools are described and invoked** so agents and humans maintain one integration path.

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

- [Tool design](../../concepts/tool-design.md)
- [MCP deep dive](../../research/mcp-deep-dive.md)
- [Agent composition](../../concepts/agent-composition.md)
- [A2A deep dive](../../research/a2a-deep-dive.md)
- [Deployment patterns](../../concepts/deployment-patterns.md)
