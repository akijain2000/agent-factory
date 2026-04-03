# Tool Selection

## What it is

**Tool selection** is how a model (or a wrapper policy) decides **which tool** to invoke among many candidates. It depends on **tool names and descriptions**, **schemas** that telegraph valid use cases, optional **routing** layers (classifiers, rules, or smaller models), and **tool recommendation** patterns that narrow the active set per turn. At scale, the problem is **tool confusion**: similar names, overlapping behavior, or twenty-plus tools without grouping.

## Why it matters for agents

Wrong-tool calls waste latency, money, and user trust; they can also cause **security** issues if a powerful tool is chosen accidentally. Good selection is the difference between a reliable copilot and a stochastic remote control. It interacts directly with **evals**: selection errors show up as trace anomalies before user-visible failure.

## How to implement it

1. **Names and descriptions:** first line = precise trigger; include negative examples (“Do not use for X; use Y instead”). Keep descriptions parallel in structure for easier comparison by the model.
2. **Disambiguate overlaps:** merge near-duplicate tools or split responsibilities until each tool has one clear job (see [Tool Design](tool-design.md)).
3. **Dynamic subsets:** retrieve or classify to **k** candidate tools per query instead of listing the entire catalog; refresh the subset when the task shifts.
4. **Router model:** a small, fast model or rules engine assigns `intent → bundle` before the main reasoning call; log router decisions for debugging.
5. **Hard constraints:** policies that forbid certain tools unless prerequisites fire (e.g., `deploy` only after `tests_pass` tool).
6. **Telemetry:** histogram of tool confusion pairs; drill into traces where the model corrected itself after a bad call.

## Large tool sets

Prefer **hierarchical exposure:** category tools that expand detail, or MCP servers mounted per workspace. Avoid flat namespaces with fifty similarly named `get_*` operations without qualifiers.

## Tool descriptions that improve routing

Lead with **user-intent phrasing** the model already sees in chat (“Use when the user asks to refund…”). Follow with **inputs** the tool needs and **outputs** it returns. Close with **failure modes** (“Returns NOT_FOUND if the order is older than 90 days”). Keep examples in developer docs; long examples in-schema steal context.

## Recommendation and retrieval

Treat active tools like a **mini-RAG** problem: embed descriptions, retrieve top-k by query similarity, then let the main model choose among k. Refresh k when the user switches topics (detect via embeddings or lightweight classifiers). Log when the final pick was **outside** the recommended set—signals router drift.

## Reducing confusion under load

Under latency pressure, models shortcut to familiar tools. Counter with **forced disambiguation**: if two tools score similarly, ask a clarifying question or run a cheap verifier model before execution.

## Common mistakes

- Descriptions that read like internal API docs instead of decision criteria for the model.
- Identical parameter shapes across tools, making arguments interchangeable by accident.
- No measurement of mis-selection rate; only monitoring final answer quality.
- Routers trained on production without handling new tools (silent skew).

## Quick checklist

- Every tool has a **negative** description line (“do not use when…”).
- Production traces sample **mis-selection** pairs for monthly review.
- Dynamic tool subsets log both **offered** and **chosen** tools.

## References to course modules

These map to the **23-module Agent Factory course** (see [`../../course/README.md`](../../course/README.md) when published).

- **Module 05 — Tool Design and Integration** — schemas, metadata, and how models choose tools.
- **Module 04 — System Prompts for Agents** — surfacing the right tool subset in context.
- **Module 09 — Agent Design Patterns** — routing, intent detection, and scalable selection.

Full curriculum index: [`../../course/README.md`](../../course/README.md) (when present).

## See also

- [Tool Design](tool-design.md)
- [Structured Outputs](structured-outputs.md)
- [Planning Strategies](planning-strategies.md)
- [Agent Composition](agent-composition.md)
- [Observability](observability.md)
