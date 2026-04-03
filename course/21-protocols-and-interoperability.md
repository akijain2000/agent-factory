# Module 21: Protocols and Interoperability

**Duration:** approximately 40 minutes  
**Prerequisites:** Modules 05 (Tool Design and Integration), 13 (Framework Selection), and 16–18 recommended for context on tools, frameworks, and safety.

---

## Learning objectives

By the end of this module, you should be able to:

- **Build** MCP servers that expose well-scoped tools with clear schemas and safe execution boundaries.
- **Explain** how agent-to-agent (A2A) communication differs from tool calls and human chat, including trust and tenancy concerns.
- **Design** agents that remain **framework-agnostic** at the capability layer so they can move between hosts and orchestrators.
- **Reason** about sharing capabilities through registries and marketplaces without leaking secrets or violating policy.
- **Sketch** multi-organization compositions where identity, audit, and data residency remain first-class.

---

## MCP server authoring: exposing tools via the Model Context Protocol

The **Model Context Protocol (MCP)** standardizes how hosts discover and invoke **tools**, **resources**, and **prompts** from servers the model does not “own.” Authoring an MCP server is not “another REST API”: you declare **capabilities**, **input schemas**, and **behavioral contracts** so any compliant client can bind them consistently.

Practical authoring checklist:

- **One tool, one job:** avoid mega-tools that hide branching; prefer composable primitives with explicit parameters.
- **Schema honesty:** required fields, enums, and defaults must match runtime validation; mismatches produce silent misuse across clients.
- **Side effects:** document whether a tool reads, writes, or triggers external workflows; hosts may gate execution by policy tier.
- **Errors:** return structured errors (codes, retry hints) rather than opaque strings so agents can recover.
- **Transport:** stdio for local dev; HTTP or SSE for remote servers—treat auth, TLS, and tenant headers as non-negotiable for shared deployments.

A minimal mental model: the LLM proposes `tool_name` + `arguments`; the host executes the server handler; results return as **content blocks** the model consumes in the next turn. Your server is the **trust boundary** for whatever it can reach.

**Concrete sketch (language-agnostic):** define three handlers—`tools/list` discovery, `tools/call` dispatch, and consistent JSON Schema for each tool’s `inputSchema`. Validate arguments **before** side effects; return `isError: true` with a machine-readable `code` when business rules fail (not only when the process crashes). If you expose resources (files, URIs), document whether reads are cached and how cache invalidation works, because agents will assume freshness unless told otherwise.

---

## A2A communication: how agents talk to each other across boundaries

**A2A** patterns treat another agent as a **peer** or **service** rather than as a subroutine inside one process. Boundaries include different frameworks, teams, VPCs, or legal entities. Compared to in-process tool calls, A2A adds:

- **Identity and authorization:** which agent may invoke which capability on behalf of which user or tenant.
- **Message envelopes:** correlation IDs, causality (who asked whom), and optional human approval tokens.
- **Schema versioning:** agents evolve prompts and tools independently; clients must tolerate backward-compatible changes or explicit version pins.
- **Failure modes:** timeouts, partial responses, and ambiguous handoffs require **escalation** paths (human, planner, or degraded mode).

Design flows as **explicit state machines** or **handoff documents** (goal, constraints, artifacts produced, open questions) rather than ad-hoc chat transcripts. That discipline is what makes cross-boundary debugging possible.

When two agents run under different vendors or frameworks, align on **three** layers: (1) a **canonical task record** (id, owner, deadline, allowed tools), (2) a **message envelope** with correlation and causality metadata, and (3) a **termination contract** (what “done” means and who acknowledges it). Without (3), you get endless ping-pong or duplicate commits.

---

## Interoperability: making agents framework-agnostic

Framework-specific graphs and SDKs are implementation details. **Interoperability** lives in:

- **Stable capability IDs** and JSON-serializable I/O for every external action.
- **Pluggable transports** (MCP, HTTP, message bus) behind thin adapters in your codebase.
- **Prompt and policy as data** (versioned bundles) rather than hard-coded strings scattered across nodes.
- **Evaluation fixtures** that run against the same scenarios regardless of orchestration backend.

When you must pick a framework, choose one—but **export** your agent’s contract (tools, memory interfaces, safety hooks) so another team could re-host it without rewriting business logic.

**Adapter pattern:** keep domain logic in pure functions or a small core package; let LangGraph, Agents SDK, or custom loops call into that core. Integration tests should target the **core** first, then smoke-test each host binding. That split is what makes “we might switch frameworks next quarter” a manageable risk instead of a rewrite.

---

## Tool marketplaces: sharing agent capabilities

Marketplaces and registries (public catalogs, internal developer portals, vendor integrations such as **Composio**-style connectors) accelerate adoption but concentrate risk:

- **Supply chain:** who published the server, how is it updated, and can you pin versions?
- **Least privilege:** default OAuth scopes and API keys should be minimal; agents should not inherit a user’s full cloud account.
- **Observability:** log tool invocations with tenant, latency, and outcome; alert on anomalous volume or new tool surfaces.
- **Policy:** block categories of tools in regulated environments unless reviewed.

Treat marketplace tools like **dependencies**: vet, version, and monitor them the same way you would a third-party library with network access.

---

## Composing agents across organizations

Multi-org composition usually means **federated identity** (SSO, workload identities), **contractual data handling**, and **shared audit trails**. Patterns:

- **B2B agent APIs** with mTLS or signed JWTs between orgs; no shared long-lived API keys in prompts.
- **Data minimization:** pass references (IDs, signed URLs) instead of full payloads when possible.
- **Human gates** at jurisdictional boundaries (PII export, financial transactions).
- **Replayable traces** stored per org for compliance, with redaction pipelines.

Success is measured in **defensible operations**, not clever autonomy—if you cannot explain who did what under which policy, do not ship it.

---

## Study: MCP specification, A2A project, Composio integrations

Read or skim:

- The **MCP specification** for transports, capability negotiation, and error shapes—focus on how hosts and servers establish sessions.
- **A2A**-oriented projects and write-ups (Google’s Agent2Agent direction and ecosystem notes) for messaging and discovery concepts; compare to your in-house handoff format.
- **Composio** (or similar integration layers) as an example of **pre-built tool auth** and action catalogs; note how they map third-party APIs to tool schemas and OAuth.

Your goal is not memorizing vendors but recognizing **recurring layers**: schema, auth, transport, policy, observability.

---

## Exercises

1. **Build an MCP server with three tools**  
   Implement (or fully specify in pseudocode plus JSON Schema) an MCP server that exposes exactly **three** tools—for example: `lookup_doc`, `append_note`, and `run_safe_query`. For each tool, document input/output schema, idempotency, and error codes. Describe how you would run it locally and attach it to a host that supports MCP.

2. **Design an A2A flow between two agents**  
   Pick two roles (e.g., **Researcher** and **Editor**). Draw or bullet a sequence: message types, handoff artifact, retry policy, and where a human approves. Include one failure scenario (timeout mid-handoff) and how the system recovers without duplicate side effects.

---

## Further reading

- [MCP deep dive (wiki)](../wiki/research/mcp-deep-dive.md)
- [A2A deep dive (wiki)](../wiki/research/a2a-deep-dive.md)
- [MCP tool server (good example)](../wiki/examples/good/mcp-tool-server.md)
