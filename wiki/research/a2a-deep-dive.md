# Agent-to-Agent (A2A) Protocol: Cross-Framework Communication

A2A targets a problem MCP alone does not solve: **peer agents**—possibly built with different frameworks—must **delegate tasks**, **discover capabilities**, and **return results** without sharing a monolithic runtime. Think “HTTP for agent collaboration” rather than “shared tool DLL.”

## Motivation

Enterprises will run **heterogeneous** agents: vendor SDK bots, in-house graphs, legacy RPA wrappers. A2A-style protocols aim for **interoperable envelopes** for task specs, status, artifacts, and errors—reducing bespoke glue per pairwise integration.

## Task delegation

Delegation messages typically carry **goal statements**, **constraints** (time, cost, policy), **acceptance criteria**, and **correlation IDs**. The delegate agent responds with **structured progress** events and a terminal **result package** suitable for machine merge—not only natural language.

## Result passing

Results should include **typed payloads** (JSON, files, diffs) and **provenance** (which tools ran, which models). This supports orchestrators that **verify** outputs (tests, schema checks) before accepting handoffs.

## Capability discovery

Agents advertise **skills** or **tool catalogs** discoverable by peers—analogous to service registries. Discovery must be **auth-aware**: not every peer may invoke every capability.

## Comparison to MCP

**MCP** connects a host to **tool servers** inside an application boundary. **A2A** connects **agents** as actors across boundaries. They compose: an agent may use MCP tools locally while speaking A2A to a remote specialist agent.

## Failure modes

Without strict schemas, A2A devolves into **chatty email between bots**—ambiguous ownership, duplicated work, and unbounded retries. Mitigate with **timeouts**, **single-writer** state rules, and **idempotent** task IDs.

## Security posture

Authenticate peers, authorize capabilities, and **log** cross-agent calls for audit. Treat remote agent outputs as **untrusted** until validated—parallel to prompt-injection defenses for tool outputs.

## Maturity note

Protocols in this space evolve quickly; treat specifications as **versioned contracts** and pin supported feature levels in production gateways.

## Message schema considerations

Inter-agent messages benefit from **typed envelopes**: `task_id`, `parent_task_id`, `issuer`, `capabilities_required`, `deadline`, `payload`, `attachments`, `policy_tags`. Plain prose bodies alone recreate email-thread chaos. Attach **hashes** of large artifacts instead of inlining binary blobs through LLM contexts.

## Federation and tenancy

In multi-tenant deployments, **isolate** agent registries per tenant and sign messages to prevent **cross-tenant** task injection. Federation across organizations may require **mTLS** and **contractual** logging of payloads.

## Observability across peers

Propagate **trace context** (W3C traceparent or equivalent) through A2A messages so operators can stitch **client → orchestrator → remote specialist** spans. Without this, latency triage stops at organizational boundaries.

## Summary

A2A is the **inter-agent** complement to MCP’s host–tool boundary: success requires **typed** delegation, **authz**, and **distributed tracing**, not prose handshakes between bots.

## Sources and further reading

- Agent-to-Agent protocol materials and vendor announcements (Google-led ecosystem efforts as of 2024–2026).
- MCP specification for complementary tool-host patterns.

## See also

- [MCP deep dive](mcp-deep-dive.md)
- [Multi-agent landscape](multi-agent-landscape.md)
- [Framework comparison](framework-comparison.md)
- Concepts: [Agent Handoffs](../concepts/agent-handoffs.md), [Multi-Agent Orchestration](../concepts/multi-agent-orchestration.md), [Agent Security](../concepts/agent-security.md)
- Course: [Agent Factory course](../../course/README.md)
