# Autonomous Loops

## What it is

**Autonomous loops** are self-driven cycles that pursue a goal without per-step human input: **score-driven hill-climbing** (iterate until a metric improves enough), **PRD completion loops** (implement until acceptance checks pass), **git-as-memory** (commits and branches as durable state), and **self-modifying** agents that patch their own code or prompts. Systems such as **autoagent**, **ralph**, and **ouroboros** explore how much autonomy improves throughput—and where **runaway** behavior appears when scores are **gamed** or stop conditions are vague.

## Why it matters for agents

Autonomy unlocks **long-horizon** tasks (refactors, research, multi-file fixes) but amplifies **risk**: unbounded loops spend money, corrupt repos, or ship **regressions** that look fine to a shallow scorer. Product and safety teams need explicit **when autonomy helps** criteria versus **when** to require **human** gates.

Autonomy is not **binary**: design **stages** where the loop proposes and **CI** or humans **commit**, versus stages where the loop may edit freely inside a **sandbox** branch.

## How to implement it

1. **Objective function:** define **measurable** scores (tests pass, linter clean, eval suite threshold). Avoid single **LLM-judge** metrics without **human** calibration.
2. **Hill-climbing guardrails:** cap **iterations**, **wall time**, and **diff size**; require **monotonic** improvement on a **held-out** check or stop.
3. **PRD loops:** break PRDs into **verifiable** checkpoints; automate **verification** with CI; never mark complete without **artifact** links (PR URL, test run id).
4. **Git-as-memory:** use **branches** per run; **commit** messages include `run_id`; enforce **review** before merge to main; tag **releases** with harness version.
5. **Self-modification:** sandbox writes; **diff-only** proposals via PR; block **direct** push to protected branches. Log **pre** and **post** behavior snapshots.
6. **Stop conditions:** combine **success**, **no progress** (score plateau), **policy violation**, and **budget** exhaustion—mirroring [Agent Loop](agent-loop.md) discipline at macro scale.

7. **Telemetry:** log **score history** per run; alert on **oscillation** (scores flip-flop) or **monotonic** cost without **monotonic** quality.

**Ralph**-style loops emphasize **tight** feedback from the environment (tests, linters). **Ouroboros** warns that **self-edit** without isolation **compounds** errors. **Autoagent** patterns stress **harness-level** limits, not model politeness.

## When autonomy helps

**Clear** verifiers, **low** blast radius, **recoverable** state (git, VMs). **When it runs away:** fuzzy goals, **production** side effects, **untrusted** inputs, or **weak** scoring.

Pair **git-as-memory** with **branch protection** and mandatory **CI** so “memory” cannot bypass engineering norms.

When scores **plateau**, require a **human** or **different verifier** before allowing another N iterations—prevents thrash.

## Common mistakes

- **Infinite** “just one more fix” cycles after tests already pass flaky once.
- Letting agents **merge** without human or CI review.
- **Optimizing** the wrong score (coverage without meaningful asserts).
- **Recursive** self-spawn without **global** depth and **cost** limits.
- **Reward hacking** on surrogate metrics (comment density, line count) instead of user-valued outcomes.

## References to course modules

These map to the **23-module Agent Factory course** (see [`../../course/README.md`](../../course/README.md) when published).

- **Module 03 — The Agent Loop & Control Flow** — iteration, stops, and budgets at micro scale.
- **Module 11 — Autonomy, Goals, and Stop Conditions** — macro loops and safe objectives.
- **Module 15 — Advanced Orchestration & State Machines** — durable runs and checkpoints.
- **Module 16 — Testing & CI for Agents** — verifiers that autonomous loops must satisfy.

Full curriculum index: [`../../course/README.md`](../../course/README.md) (when present).

## See also

- [Agent Loop](agent-loop.md)
- [Harness Engineering](harness-engineering.md)
- [Guardrails](guardrails.md)
- [Human-in-the-Loop](human-in-the-loop.md)
- [Self-Improving Agents](self-improving-agents.md)
- [Agent Evaluation](agent-evaluation.md)
