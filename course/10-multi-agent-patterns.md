# Module 10: Multi-Agent Patterns

**Duration:** approximately 45 minutes  
**Prerequisites:** Module 09 (Agent Design Patterns); Module 03 (The Agent Loop).

---

## Learning objectives

By the end of this module, you should be able to:

- **Implement** supervisor, sequential pipeline, parallel fan-out, swarm-style handoff, and debate-style multi-agent flows at the design level.
- **Explain** when multi-agent systems outperform a single agent (specialization, critique, parallelism) and when they add only coordination tax.
- **Design** clean handoffs: explicit payloads, ownership of mutable state, and termination conditions.

---

## Supervisor pattern: one agent directing others

A **supervisor** (or orchestrator) **routes** work to worker agents based on intent, file type, or phase. The supervisor **does not** need to be a different model; it is a **role** with authority to delegate.

```text
Supervisor: User request is "audit SQL in this PR."
  -> delegate to sql_specialist(agent_input=diff, constraints=read_only)
  -> delegate to security_linter(agent_input=sql_specialist_report)
  -> synthesize final summary for user
```

Keep the supervisor’s **routing policy** versioned (prompt or small classifier). Log **which worker ran** for auditability.

Failure mode: the supervisor becomes a **bottleneck** that re-explains the whole world to every worker. Prefer **pointer-based** briefs (artifact URIs, ticket ids) over full chat dumps.

---

## Sequential pipeline: agents in a chain

**Sequential** pipelines pass a **shared artifact** through stages: extract → normalize → verify → summarize. Each stage reads the previous **structured output** (JSON or markdown sections), not the entire raw chat.

Define **schemas** between stages to prevent semantic drift. Example: Stage 1 outputs `Finding[]`; Stage 2 may only add `severity` and `evidence`, not rewrite `description`.

Add **validation gates**: if Stage 2’s JSON fails schema validation, **do not** silently pass prose downstream; retry or escalate.

---

## Parallel fan-out: agents working simultaneously

**Parallel fan-out** runs **independent** subtasks concurrently (different files, regions, or hypotheses), then **reduces** results (merge, vote, rank). Requires **idempotent** tasks and a **merge strategy** (deterministic sort, dedupe keys).

Watch **rate limits** and **cost**: N parallel LLM calls multiply spend. Use parallel only when **latency** or **coverage** wins justify it.

```python
# Conceptual: fan-out then reduce
results = await asyncio.gather(
    agent_a.run(chunk=chunks[0]),
    agent_a.run(chunk=chunks[1]),
)
merged = reducer.merge(results)
```

If one shard fails, decide **fail-fast** vs **partial result + explicit gaps**; do not let the reducer invent content for missing shards.

---

## Swarm pattern: OpenAI’s lightweight handoffs

**Swarm** (OpenAI) emphasizes **lightweight handoffs**: agents transfer control with a **small context package** (goal, constraints, pointers to artifacts) rather than copying full history. Functions as tools can **switch active agent** in the harness.

Fits **customer support** (triage → billing → technical) and **internal copilots** with clear escalation rules. Avoid deep nesting of handoffs without a **global trace id** for debugging.

---

## Debate pattern: agents arguing to find better answers

**Debate** assigns **adversarial roles** (proposer vs critic, or red team vs blue team) over a fixed number of rounds, then a **judge** or **merge** step picks or synthesizes. Improves **robustness** on ambiguous specs and security reviews.

Set **max rounds** and **stopping criteria** (e.g., critic finds no new issues). Without limits, agents **agree too easily** or **nitpick forever** (see Module 11 on sycophantic loops).

Use a **frozen evidence packet** (same bullets for both sides) so debate is about reasoning, not who saw different context.

---

## Designing clean handoffs

Every handoff should answer:

1. **Payload:** structured input + artifact pointers (not unbounded history).  
2. **Authority:** who may write shared state (single-writer per resource).  
3. **Termination:** max steps, success predicate, or human gate.  
4. **Trace:** `correlation_id` across all agents for logs.

Example payload shape:

```json
{
  "correlation_id": "req-8f3a",
  "objective": "Summarize security impact of dependency bump",
  "constraints": ["read_only", "no_network_except_npm_registry"],
  "inputs": {"lockfile_diff_uri": "blob://..."},
  "output_schema": "SecuritySummaryV1"
}
```

---

## When multi-agent beats single-agent (and when it does not)

**Multi-agent tends to win** when:

- Expertise is **genuinely partitioned** (security vs readability vs tests).  
- **Parallelism** cuts wall-clock time for independent chunks.  
- **Adversarial critique** catches classes of errors self-reflection misses.

**Single-agent often wins** when:

- The task is **short** and **serial**.  
- Handoffs would **duplicate** the same context N times.  
- You lack evals proving the extra agents help.

Measure **end-to-end success**, not “more agents = more serious.”

---

## Study: Paperclip, CrewAI, OpenAI Swarm

- **Paperclip-style team orchestration:** multiple specialists with a coordinator; study how **task boundaries** and **shared scratchpad** are defined in real products (see wiki research note).
- **CrewAI role-based agents:** roles, goals, and backstories shape behavior; useful for **prompt reuse** and **human-readable** team configs. Tradeoff: verbosity and token overhead.
- **OpenAI Swarm:** study **handoff functions** and minimal state; good reference for **flat** orchestration without a heavy framework.

---

## Exercises

1. **Multi-agent code review**  
   Design three agents (e.g., style, logic/tests, security) plus a merger. Specify: inputs per agent, output schema, sequential vs parallel, and how conflicts are resolved.

2. **Sequential to parallel**  
   Take a linear pipeline (e.g., summarize five sections one after another). Redesign so **independent** sections run in parallel, then **one** consolidation agent merges. List risks (inconsistent terminology) and mitigations (shared glossary in merger prompt).

---

## Further reading

- [Multi-agent orchestration (wiki)](../wiki/concepts/multi-agent-orchestration.md)
- [Paperclip orchestration analysis (wiki)](../wiki/research/paperclip-orchestration-analysis.md)
- [Multi-agent landscape (wiki)](../wiki/research/multi-agent-landscape.md)
