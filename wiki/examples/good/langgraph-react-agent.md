# LangGraph ReAct Agent: State Machine and Tool Loop

## Summary

This example imagines a production ReAct-style agent implemented in LangGraph: a directed graph of nodes for reasoning, tool invocation, and observation, with explicit transitions rather than ad hoc control flow in application code. The agent alternates between planning the next action, calling a bounded set of tools, and integrating observations until a terminal condition is met.

## Pattern

**Explicit state machine plus ReAct loop.** Graph nodes own narrow responsibilities (e.g., `plan`, `act`, `observe`, `finalize`). Edges encode allowed transitions and guard conditions. Tool calls are routed through a single `execute_tools` node that validates arguments and records results in shared state.

## The code

```python
from typing import Annotated, TypedDict
from langgraph.graph import StateGraph, END
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode
from langchain_openai import ChatOpenAI
from langchain_core.tools import tool

@tool
def search(query: str) -> str:
    """Search the web for current information."""
    return f"Results for '{query}': LangGraph is a library for building stateful agent workflows."

class AgentState(TypedDict):
    messages: Annotated[list, add_messages]

tools = [search]
model = ChatOpenAI(model="gpt-4o-mini").bind_tools(tools)

def call_model(state: AgentState) -> dict:
    return {"messages": [model.invoke(state["messages"])]}

def should_continue(state: AgentState) -> str:
    last = state["messages"][-1]
    return "tools" if last.tool_calls else END

graph = StateGraph(AgentState)
graph.add_node("agent", call_model)
graph.add_node("tools", ToolNode(tools))
graph.set_entry_point("agent")
graph.add_conditional_edges("agent", should_continue, {"tools": "tools", END: END})
graph.add_edge("tools", "agent")

app = graph.compile()
result = app.invoke({"messages": [("user", "What is LangGraph?")]})
print(result["messages"][-1].content)
```

**Walkthrough:** `AgentState` holds the message list with LangGraph's built-in deduplication via `add_messages`. The graph has two nodes: `agent` (calls the model) and `tools` (executes any tool calls). `should_continue` inspects the last message—if it contains tool calls, route to the `tools` node; otherwise end. The `tools -> agent` edge creates the ReAct loop: act, observe, reason again. `compile()` produces a runnable with built-in checkpointing support.

## What makes it good

Clear state reduces ambiguity: the runtime always knows whether the system is awaiting a model decision, a tool result, or human input. Tool routing is centralized, so policies (retries, timeouts, redaction) apply consistently. The observation loop is visible in the graph, which makes debugging and testing easier than burying the same logic in nested callbacks.

Compared to a free-form while-loop around `chat.completions`, LangGraph forces you to name phases and persist checkpoints. That supports human-in-the-loop interrupts and replay without re-deriving control flow from logs.

### In practice

Typical node boundaries include: parsing the latest user message into intent, selecting a tool plan, executing tools with idempotency keys, summarizing observations when context grows, and emitting a final structured response. Checkpoints after `observe` let you resume after provider outages without duplicating side effects.

### Failure modes this design mitigates

Unstructured loops often lose track of whether a tool already ran; explicit state prevents double-charging or duplicate writes. Graph-level timeouts can transition to a `recover` node instead of hanging forever. Testing can inject fixed transitions to validate each node in isolation.

### When to reconsider

If your workflow is strictly linear ETL with no branching, a plain DAG job may be simpler than an LLM-in-the-loop graph. The graph pays off when **language-mediated decisions** must coexist with **deterministic policies**.

## Key takeaway

When the **control structure is part of the product** (compliance, audits, recovery), encode it as an explicit graph with typed state rather than as prose instructions inside a single mega-prompt.

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

- [Agent loop](../../concepts/agent-loop.md)
- [State management](../../concepts/state-management.md)
- [Error recovery](../../concepts/error-recovery.md)
- [Tool design](../../concepts/tool-design.md)
- [Framework comparison](../../research/framework-comparison.md)
