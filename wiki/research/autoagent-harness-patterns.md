# Autoagent: Program the Meta-Agent, Not the Harness

Autoagent-style projects invert typical tutorials: engineers invest in a **durable harness** (isolation, benchmarks, scoring) while the **human-facing artifact**—often `program.md` or equivalent—steers a **meta-agent** that writes/refines task solutions. This pattern separates **environment engineering** from **policy prose**.

## program.md as human interface

`program.md` encodes goals, constraints, and evaluation semantics in natural language **consumed by** the meta-agent. Treat it like **infrastructure-as-contract**: changes should trigger **regression** runs because they redefine success.

## Hill-climbing on benchmarks

The meta-agent iterates against **scorable tasks** (unit tests, harness checks), adjusting plans and code until scores improve. This is **optimization under noise**: stochastic proposals require **caps** on attempts and **diversity** mechanisms to escape local minima.

## Docker isolation

Sandboxes standardize dependencies and **contain** side effects. Isolation boundaries also enable **parallel** attempts across shards with reduced fear of host corruption. Costs include image maintenance and **I/O** overhead.

## Harness engineering pattern

The harness provides: **task ingestion**, **tool surfaces**, **timeout enforcement**, **artifact capture** (logs, diffs), and **grading**. The meta-agent consumes these signals **without** bespoke per-task harness rewrites.

## Separation of concerns

When the harness is stable, iteration moves faster: you are **tuning** prompts and strategies, not debugging ad-hoc shell glue each run. Conversely, a weak harness makes the meta-agent **confabulate success** where tooling failed silently.

## Risks

- **Overfitting** to benchmark quirks.
- **Unsafe** tool exposure inside sandboxes still risks **data exfiltration** if secrets mount incorrectly.
- **Cost explosions** on unbounded hill-climb loops.

## Relation to gstack skills

Gstack **skills** resemble curated `program.md` slices—human-maintained procedures—whereas autoagent emphasizes **machine-driven** refinement. Both converge on **versioned** procedural artifacts.

## Harness acceptance checklist

- Task input/output **schemas** frozen per benchmark suite.  
- Deterministic **seeds** where randomness exists (sampling temperature logged).  
- **Artifact retention** policy (how long diffs/logs live).  
- **Network egress** default-deny unless a task explicitly requires it.  
- **Grader** transparency: human-readable rubric alongside automated score.

## When hill-climb helps vs hurts

Helpful when search space is **structured** (code edits with test signals). Harmful when rewards are **sparse/noisy** (subjective UX tasks) without human labels—meta-agents **game** proxies.

## Documentation contract

Treat `program.md` like an **API spec**: breaking edits require **semver** or migration notes. Consumers (humans and meta-agents) depend on stable **evaluation semantics** encoded there.

## Summary

Autoagent patterns shine when **harness quality** is non-negotiable and iteration focuses on **meta-policy** (`program.md`) rather than rewiring sandboxes each week.

## Sources and further reading

- Autoagent repository documentation and `program.md` conventions (verify current filenames).
- Literature on neural architecture search analogies for LLM meta-optimization.

## See also

- [Gstack agent analysis](gstack-agent-analysis.md)
- [Agent evaluation methods](agent-evaluation-methods.md)
- [Anti-patterns](anti-patterns.md)
- Concepts: [Harness Engineering](../concepts/harness-engineering.md), [Sandboxing](../concepts/sandboxing.md), [Agent Testing Patterns](../concepts/agent-testing-patterns.md), [Feedback Loops](../concepts/feedback-loops.md)
- Course: [Agent Factory course](../../course/README.md)
