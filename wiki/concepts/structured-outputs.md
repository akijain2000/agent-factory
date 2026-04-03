# Structured Outputs

## What it is

**Structured outputs** are model responses constrained to a machine-parseable shape: JSON objects, typed tool-call arguments, or schema-validated payloads. They bridge natural-language reasoning with downstream systems (databases, UIs, workflows). Common mechanisms include **JSON mode** (emit valid JSON only), **function / tool calling** (named functions with argument objects), and **explicit schema enforcement** via JSON Schema, **Pydantic** (Python), or **Zod** (TypeScript) with repair or retry on validation failure.

## Why it matters for agents

Agents chain many steps; brittle free-form text forces regex parsing and silent structural drift. Structured outputs improve **reliability**, **testability**, and **safety**: you can assert invariants (`severity` enum, bounded arrays), reject partial objects before side effects, and log comparable artifacts for evaluation. They also reduce token waste when the consumer only needs fields, not prose.

## How to implement it

1. **Pick the constraint layer:** native tool calling when the model must *choose* an action; JSON mode or response-format APIs when the output is a single structured blob (extraction, classification).
2. **Define schemas first:** JSON Schema with `required`, `enum`, `maxItems`, and `additionalProperties: false` where appropriate. Generate Pydantic / Zod models from one source of truth to avoid drift.
3. **Validate at the boundary:** parse JSON, run `model_validate` (Pydantic) or `safeParse` (Zod). On failure, return a compact error to the model (field path + constraint) and retry with a capped budget.
4. **Separate reasoning from payload:** allow scratch reasoning in a non-persisted channel if the API supports it; persist only validated objects.
5. **Tool returns:** mirror the same discipline—tools return typed success/error envelopes so the next model turn is not ambiguous.
6. **Streaming:** if you stream partial JSON, use a parser tolerant of chunks or buffer until complete before validation.

## Schema design tips

Prefer flat structures when possible; nest only when it mirrors domain ownership. Use enums over free strings for categorical fields. Document default semantics in code, not only in prompt prose. Version schemas (`schema_version` field) when evolving production contracts.

## Pydantic and Zod at the boundary

In Python, define `BaseModel` classes with `Field` constraints (`min_length`, `pattern`, custom validators). Use `model_dump(mode="json")` when persisting. In TypeScript, Zod schemas compose with `z.object`, `z.discriminatedUnion` for tagged variants, and `.strict()` to reject unknown keys. Share **one** JSON Schema export in `tools/` for LLM registration and generate language models in CI so the runtime and the API never disagree.

## Repair loops

When validation fails, return a minimal machine-readable error: `path`, `expected`, `received`. Cap retries (typically two to three). If repairs still fail, fall back to a safe default (partial save, human queue) rather than looping indefinitely. Log failure **fingerprints** (hash of error shape) to spot systematic schema misunderstandings.

## Provider and API notes

Vendor **JSON mode** and **structured output** features differ in how strictly they enforce schemas; some guarantee syntax only, not semantic fit. Treat native guarantees as **necessary** but not sufficient—always validate in your process. For tool calling, remember the model may emit parallel calls; your harness must handle batches deterministically.

## Common mistakes

- Validating only in the client while the model still emits markdown fences around JSON.
- Oversized schemas that consume context and confuse the model; split into multiple calls or tools.
- Retrying without feeding validation errors back—wastes tokens and repeats the same mistake.
- Treating model-produced JSON as trusted executable code; always validate and sandbox side effects.

## Quick checklist

- Schema is the single source of truth in `tools/` and generated types.
- Validation runs server-side before any side effect or persistence.
- Retry budget and structured validation errors are wired into the harness.

## References to course modules

These map to the **23-module Agent Factory course** (see [`../../course/README.md`](../../course/README.md) when published).

- **Module 05 — Function Calling & JSON Schema** — argument and return contracts.
- **Module 12 — Structured Extraction & Classification** — JSON mode patterns for non-tool flows.
- **Module 16 — Validation, Repair Loops, and Type Safety** — Pydantic, Zod, and retry policies.

Full curriculum index: [`../../course/README.md`](../../course/README.md) (when present).

## See also

- [Tool Design](tool-design.md)
- [Tool Selection](tool-selection.md)
- [Agent Testing Patterns](agent-testing-patterns.md)
- [Error Recovery](error-recovery.md)
- [Observability](observability.md)
