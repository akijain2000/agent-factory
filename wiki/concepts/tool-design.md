# Tool Design

## What it is

**Tool design** is the practice of defining callable capabilities (functions, APIs, MCP tools) so that models can select the right action, supply valid arguments, and interpret results without ambiguity. It spans **JSON Schema** (or equivalent) for inputs, documented return shapes, **MCP servers** as a standardized host for tools/resources, and operational concerns: timeouts, idempotency, and **error taxonomies** the harness—not the model—should preferentially interpret.

## Why it matters for agents

The model only sees names, descriptions, and schemas you expose. Poor naming or overloaded “god tools” drive wrong calls, hallucinated parameters, and unsafe breadth of side effects. Good tool design is the main lever for **reliability**, **testability**, and **least privilege**: narrow tools compose; wide tools bypass validation and auditing.

## How to implement it

1. **One intent per tool:** prefer `search_orders` + `get_order` over `do_everything_with_orders`.
2. **Schemas:** required vs optional fields, enums for modes, sensible defaults in code—not hidden in prompt prose. Validate server-side; reject before side effects.
3. **Descriptions:** first line = when to use; second = when *not* to use; list side effects (read-only vs mutating). Keep examples in docs, not duplicated stale in the schema string.
4. **Structured outputs from tools:** return `{ ok, data?, error?: { code, message, retryable } }` so the harness can retry or circuit-break without parsing natural language.
5. **MCP:** group related tools on one server; version manifests; document auth and rate limits in the server README alongside the wiki tool catalog pattern (`tools/README.md` per AGENT_SPEC).
6. **Pagination and limits:** cap result rows and document continuation tokens so context is not flooded.

**Error return conventions:** use stable `code` values (`RATE_LIMIT`, `NOT_FOUND`, `VALIDATION_ERROR`, `UPSTREAM_TIMEOUT`). Mark `retryable: true` only when safe to repeat. Never leak stack traces to the model; log them server-side with trace ids.

## Contract checklist

Before shipping a tool, confirm: **input schema** validates at runtime; **output schema** is documented for both success and error; **timeouts** are set per tool class; **side effects** are listed in the catalog; **pagination** exists for large reads; **dry-run** or preview exists for risky writes where feasible; **telemetry** includes latency histograms and error codes. Add **contract tests** that feed boundary values and malformed JSON to ensure the model-facing layer never throws uncaught exceptions.

## Choosing granularity

Prefer several **composable** tools over one parameter-heavy Swiss Army knife. If the model must pass SQL or shell as a string, you have likely under-specified the task—wrap common operations as named tools with enums. When two tools overlap, merge them only if descriptions remain crisp; otherwise ambiguity rises and call accuracy falls.

## Documentation artifacts

Ship a **tool catalog** (`tools/README.md`) listing each tool’s purpose, parameters, return shape, auth, rate limits, and example calls. Link from the wiki index. For OpenAPI-backed tools, store the **operationId** mapping in one table to prevent drift between codegen and LLM-visible names.

## Common mistakes

- **God tool** accepting free-form strings for “command” or “query.”
- **Schema drift** between registered tools and prompts (renamed args without CI checks).
- **Opaque failures:** 500 with HTML body pasted into the next model message.
- **Missing idempotency keys** on writes, causing duplicate charges on model retries.
- **Overlong tool descriptions** that consume the context window and dilute signal.

## References to course modules

These map to the **23-module Agent Factory course** (see [`../../course/README.md`](../../course/README.md) when published).

- **Module 05 — Tool Design and Integration** — schemas, arguments, validation, and ergonomics.
- **Module 21 — Protocols and Interoperability** — standard integration surfaces and contracts.
- **Module 18 — Safety and Guardrails** — least privilege, boundaries, and safe execution.

Full curriculum index: [`../../course/README.md`](../../course/README.md) (when present).

Invest in tooling ergonomics early: refactors to split god tools are expensive once prompts, evals, and dashboards assume the old shape.

## See also

- [Tool Selection](tool-selection.md)
- [Error Recovery](error-recovery.md)
- [Guardrails](guardrails.md)
- [Structured Outputs](structured-outputs.md)
- [Sandboxing](sandboxing.md)
