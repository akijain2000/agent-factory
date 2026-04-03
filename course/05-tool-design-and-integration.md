# Module 05: Tool Design and Integration

**Duration:** approximately 45 minutes  
**Prerequisites:** Module 03 (The Agent Loop); Module 04 (System Prompts for Agents) recommended for tool-instruction context.

---

## Learning objectives

By the end of this module, you should be able to:

- **Design** tools that agents can discover, invoke, and interpret reliably (names, descriptions, structured I/O, error contracts).
- **Implement** function calling with JSON Schema (or equivalent) across major providers and in a framework-agnostic way.
- **Build** a minimal MCP server so multiple agent clients can share the same tool surface.
- **Route** tools so models choose the right capability under ambiguity.
- **Handle** tool failures with timeouts, retries, and structured error returns without poisoning the agent loop.

---

## 1. What makes a good tool

**Clear name**  
Use verb-noun pairs that match user intent (`search_documents`, not `tool7`). Avoid overloaded names that mean different things in different contexts.

**Description**  
The model reads descriptions when selecting tools. State **what the tool does**, **what it does not do**, and **when to prefer it** over alternatives. One dense paragraph beats vague marketing language.

**Structured I/O**  
Define arguments with types, required vs optional fields, enums for bounded choices, and sensible defaults. Return **machine-parseable** JSON (or structured text) with stable keys so the agent can branch on outcomes.

**Error handling**  
Return errors as structured objects (`{ "ok": false, "code": "RATE_LIMIT", "message": "...", "retry_after_ms": 5000 }`) instead of raw stack traces. The agent (and your harness) can map codes to retries or user-facing messages.

---

## 2. Function calling: OpenAI, Anthropic, and framework-agnostic patterns

**OpenAI-style**  
Tools are typically declared as JSON Schema attached to the chat completion or Responses API. The model emits `tool_calls` with `name` and `arguments` (JSON string). Your runtime parses arguments, executes, and appends a `tool` role message with the result.

**Anthropic**  
Tool use blocks carry `id`, `name`, and `input`. Responses interleave `assistant` content blocks with `tool_use` and `tool_result`. Keep **tool_result** tied to the matching `tool_use` id for correct multi-tool turns.

**Framework-agnostic pattern**  
1. Normalize provider-specific tool call shapes into an internal `{ tool, args, call_id }`.  
2. Execute through a single registry.  
3. Normalize results back to the provider’s expected message format.

Example schema fragment (illustrative JSON Schema):

```json
{
  "name": "fetch_url",
  "description": "Fetch a public HTTP URL and return text body up to max_bytes. Does not execute JavaScript.",
  "parameters": {
    "type": "object",
    "properties": {
      "url": { "type": "string", "format": "uri" },
      "max_bytes": { "type": "integer", "default": 100000, "minimum": 1024 }
    },
    "required": ["url"]
  }
}
```

---

## 3. MCP servers: tools any agent can use

The [Model Context Protocol](https://modelcontextprotocol.io/) exposes **tools**, **resources**, and **prompts** over a standard transport (often stdio or HTTP). A minimal MCP **tool** server:

- Declares tools with names, descriptions, and input schemas.
- Implements handlers that return **text or structured content** to the client.
- Keeps side effects explicit (file writes, network calls) and documented.

Benefits: one implementation serves Cursor, Claude Desktop, custom harnesses, and internal agents without duplicating adapter code. Version your tool schemas when breaking changes ship.

---

## 4. Tool routing: helping agents choose the right tool

**Reduce overlap**  
If two tools both “search,” differentiate by corpus, latency, or authority (“canonical docs” vs “slack history”).

**Prompt-level routing**  
In the system prompt, give **decision rules**: e.g., “Prefer `query_sql` for aggregate metrics; use `search_logs` only for raw line lookup.”

**Harness-level routing**  
Filter the tool list by **session state** or **role** so the model never sees dangerous tools in the wrong context.

**Post-hoc validation**  
Reject or rewrite calls that violate invariants (wrong repo, disallowed path) before execution, and return a structured error the model can correct.

---

## 5. Error handling in tools: timeouts, retries, structured error returns

**Timeouts**  
Every external call should have a bounded wait. Surface `TIMEOUT` with partial context (“connected but no response in 30s”) rather than hanging the loop.

**Retries**  
Retry only **idempotent** operations or those with deduplication keys. Use exponential backoff with **jitter** to avoid thundering herds. Cap `max_attempts` and propagate final failure clearly.

**Structured errors**  
Include `code`, `retryable` (boolean), and `details` for logging. Avoid leaking secrets in `message` fields shown to the model.

```python
# Illustrative pattern
def call_with_retry(fn, max_attempts=3, base_delay=0.5):
    for attempt in range(max_attempts):
        try:
            return {"ok": True, "data": fn()}
        except TransientError as e:
            if attempt == max_attempts - 1:
                return {"ok": False, "code": "TRANSIENT", "retryable": False, "message": str(e)}
            time.sleep(base_delay * (2 ** attempt) + random.uniform(0, 0.2))
```

---

## 6. Study: gstack tool design and Composio patterns

**gstack** (in this repo’s skills and browse daemon) emphasizes **fast, composable** tools with clear boundaries: navigate, snapshot, assert, screenshot—each with a narrow contract so QA loops stay predictable.

**Composio** (and similar integration layers) treat tools as **typed connectors** to SaaS APIs: standardized auth, action catalogs, and often pre-built schemas. Study how they **namespace** actions and **document** required OAuth scopes so agents do not hallucinate permissions.

Extract the pattern: **small surface, sharp descriptions, explicit failure modes**.

---

## Exercises

1. **Design three tool schemas** for a research agent: (a) web search with source caps and date filters, (b) save finding to a knowledge base with tags, (c) cite-check a claim against stored sources. For each, write JSON Schema (or your stack’s equivalent), a one-paragraph model-facing description, and example success/error payloads.

2. **Build a minimal MCP tool server** that exposes one tool (e.g., `echo` or `read_file` from a sandboxed directory). Document how an agent client registers and invokes it. If you cannot run MCP locally, write the handler pseudocode and the tool manifest you would register.

---

## Further reading

- [Tool design](../../wiki/concepts/tool-design.md)
- [Tool selection](../../wiki/concepts/tool-selection.md)
- [MCP deep dive](../../wiki/research/mcp-deep-dive.md)

---

## Summary

Good tools are **discoverable, typed, and honest about failure**. Normalize provider quirks behind a thin runtime, use MCP when multiple clients need the same tools, and combine prompt rules with harness validation for routing. Treat timeouts and retries as part of the tool contract, not as afterthoughts.
