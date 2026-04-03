# Model Context Protocol (MCP): Architecture Deep Dive

MCP standardizes how **hosts** (IDEs, agents, chat clients) connect to **servers** that expose **tools**, **resources**, and optional **sampling** primitives. It is an integration layer—not a replacement for your orchestration graph, but a way to shrink bespoke adapter code per product.

## Roles: hosts, clients, servers

The **host** embeds an MCP **client** that maintains sessions with one or more **servers**. Servers advertise **capabilities**; clients discover them at connect time. This mirrors language-server patterns: one wire protocol, many backends.

## Tools

Tools are schema-described operations the model can invoke. MCP pushes **discovery** and **invocation** into a uniform envelope so agents swap implementations (local vs remote) without rewriting prompt contracts—though **prompts still need** careful tool descriptions and cardinality discipline.

## Resources

Resources are **readable** artifacts (files, URLs, records) exposed with metadata. They support **context injection** patterns: fetch just-in-time instead of pre-stuffing the window. Resource access should respect **auth** and **PII** policies at the host boundary.

## Prompts (templates)

Servers may ship **prompt templates** to standardize recurring tasks. Templates reduce drift across clients but require **versioning** like any shared library.

## Sampling (optional)

Some configurations allow servers to request **model completions** via the host, inverting the usual call direction. This enables richer server-side workflows but raises **governance** questions: who pays, who logs, and which model policy applies.

## Transport and security

Typical deployments use **stdio** for local tools or **HTTP/SSE** for remote servers. Treat servers as **privileged code**: authenticate connections, sandbox filesystem and network access, and audit **tool calls** centrally.

## How MCP changes tool integration

Before MCP, each agent stack invented its own plugin ABI. MCP offers a **shared discovery and invocation** story, improving **ecosystem reuse** (one database server, many hosts). It does **not** solve: prompt injection, tool selection accuracy, or business logic correctness—those remain application concerns.

## Operational implications

Operators gain **inventory**: which servers are connected, which tools exist, failure rates per tool. Pair MCP with **trace IDs** spanning host and server for incident response.

## Sampling governance

When servers can request completions via the host, define **budgets**, **allowed models**, and **logging** parity with normal client calls. Avoid “shadow” spend invisible to central dashboards. Require **user-visible** indicators when sampling is invoked on their behalf.

## Compatibility and versioning

Servers and hosts may skew feature levels; negotiate **capabilities** at handshake and fail gracefully when optional features are absent. Document **minimum host version** per server release to reduce integration surprises.

## Testing strategy

Provide **mock MCP servers** in CI that simulate latency, partial failures, and malformed tool outputs. Contract-test **schema** compatibility whenever server or host major versions bump.

## Summary

MCP is an **integration bus** for tools and resources: it standardizes discovery and invocation but leaves **business correctness**, **safety**, and **evals** to application engineers.

## Sources and further reading

- Model Context Protocol specification (Anthropic, open standard).
- MCP SDK documentation and reference server implementations.

## See also

- [A2A deep dive](a2a-deep-dive.md)
- [Framework comparison](framework-comparison.md)
- [Anti-patterns](anti-patterns.md)
- Concepts: [Tool Design](../concepts/tool-design.md), [Agent Security](../concepts/agent-security.md), [Observability](../concepts/observability.md)
- Course: [Agent Factory course](../../course/README.md)
