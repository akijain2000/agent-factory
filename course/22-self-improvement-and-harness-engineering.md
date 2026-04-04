# Module 22: Self-Improvement and Harness Engineering

**Duration:** approximately 45 minutes  
**Prerequisites:** Modules 03 (Agent Loop), 07 (Planning and Reasoning), 17 (Evaluation and Testing), and 20 (Deployment) recommended.

---

## Learning objectives

By the end of this module, you should be able to:

- **Define** harness engineering and separate **meta-control** from task-level agent behavior.
- **Implement** learning loops where experience updates prompts, tools, or policies under explicit gates.
- **Describe** how agents can crystallize **skills** or procedures from repeated successes and failures.
- **Apply** score-driven optimization (hill-climbing) without fooling yourself with metrics that game the score.
- **Assess** self-modifying agent patterns (**Ouroboros**-style) and their safety trade-offs.
- **Measure** improvement through **evaluation loops** and baselines, not anecdotal demos.

---

## What is harness engineering: the discipline of meta-agent control

A **harness** is everything **around** the model that turns stochastic text into a **reliable system**: prompts, tool routers, memory, budgets, retries, evaluators, and deployment. **Harness engineering** treats that layer as a product: versioned, tested, and observable.

The agent “does the work”; the harness **decides** when to stop, which model to call, what context to load, and whether output is acceptable. Confusing the two leads to brittle demos: the model improvises policy the harness should own.

Design principle: **push nondeterminism inward** (sampling) and **push policy outward** (deterministic code and tests).

---

## Learning loops: agents that improve from experience

A **learning loop** closes the gap between runtime behavior and updated configuration. Common stages:

1. **Capture:** structured traces (tool calls, errors, user corrections).
2. **Mine:** cluster failure modes; tag root causes (bad tool schema, missing doc, over-eager autonomy).
3. **Propose:** candidate changes—prompt diff, new few-shot, tool split, retrieval tweak.
4. **Verify:** run **regression** suites and shadow traffic before promotion.
5. **Promote:** merge to a named prompt/tool version with changelog.

Loops can be **human-in-the-loop** (review every change) or **automated** within tight sandboxes (e.g., only allow edits to a `program.md` file under tests). Unbounded self-edit without verification is an incident waiting to happen.

---

## Skill creation from experience: how agents build new capabilities

**Skills** (procedures, checklists, compressed playbooks) differ from raw chat logs: they are **reusable**, **scoped**, and **triggerable**. Agents can draft skills from experience when you provide:

- A **template** (goal, prerequisites, steps, verification, failure handling).
- A **critic** step that rejects vague or unsafe instructions.
- **Storage** with naming and discovery rules (when should this skill load?).

This mirrors human runbooks: the harness stores the artifact; the model **invokes** it when descriptions match. Avoid auto-publishing skills to production without review in high-risk domains.

---

## Score-driven hill-climbing: AutoAgent’s program.md pattern

**AutoAgent**-style harnesses maintain a mutable **program** (often `program.md`): instructions the agent edits to raise a **score** on benchmarks. The pattern is **hill-climbing** in configuration space:

- Define a **numeric or rubric score** on a fixed task set.
- Allow constrained edits (e.g., single file, bounded tokens).
- **Run eval**; keep changes that improve score subject to monotonic constraints.

Strength: rapid iteration on **prompt-level** performance. Risk: **overfitting** evals and Goodharting the metric—your agent optimizes the score, not user value. Mitigate with **held-out** tasks, **diverse** rubrics, and periodic human spot checks.

---

## Self-modifying agents: Ouroboros pattern and safety considerations

**Ouroboros**-like systems feed the agent’s outputs back as inputs (code that rewrites code, prompts that rewrite prompts). Benefits include adaptation; hazards include **goal drift**, **privilege escalation**, and **unreviewed** behavioral change.

Guardrails:

- **Write scopes:** only designated files or branches; no arbitrary filesystem.
- **Two-person rule** or automated diff review for promotion.
- **Capability reduction** by default; expansion requires explicit approval.
- **Kill switches** and version rollback for harness artifacts.

Treat self-modification as **deploying software**, not chatting.

---

## Evaluation loops: measuring improvement objectively

An **evaluation loop** ties learning to evidence:

- **Baseline:** snapshot score before change.
- **Hypothesis:** what will improve and why.
- **Change:** minimal diff.
- **Measure:** same harness, same seeds where applicable, same task buckets.
- **Decide:** promote, revert, or iterate.

Use **multiple metrics**: task success, tool error rate, cost per task, latency p95, and safety probe pass rate. Publish results next to the harness version so regressions are attributable.

---

## Study: AutoAgent program.md pattern, Hermes self-improving loop, Ouroboros self-modification, autocontext recursive harness

Work through these wiki examples and research notes with a single question in mind: *what is fixed, what is allowed to change, and who verifies the change?*

- **AutoAgent** harness patterns and `program.md`-style optimization.
- **Hermes**-style self-improving loops operating on constrained infrastructure.
- **Ouroboros** discussions around recursive self-modification and containment.
- **Autocontext** / recursive harness ideas: nested evaluators controlling inner agents.

Compare **inner** agent freedom vs **outer** harness policy in each.

---

## Karpathy autoresearch: the named pattern for LLM self-improvement

The **autoresearch** pattern (Karpathy, 2025-2026) is a formalized version of score-driven hill-climbing where an LLM agent operates as both the researcher and the subject. Originally demonstrated on NanoGPT, where it ran 700 experiments in 2 days and achieved 11% training loss improvement.

### Architecture

```
┌──────────────────────────────────────────────┐
│                  program.md                   │
│  (living document: goals, constraints,        │
│   results log, current best configuration)    │
└──────────────┬───────────────────────────────┘
               │ reads
               ▼
┌──────────────────────────────────────────────┐
│              LLM Agent (Claude/GPT)           │
│  1. Read program.md + current state           │
│  2. Generate hypothesis                       │
│  3. Propose minimal edit (code or config)     │
│  4. Execute change                            │
└──────────────┬───────────────────────────────┘
               │ runs
               ▼
┌──────────────────────────────────────────────┐
│              train.py / evaluate.sh           │
│  (objective scorer—loss, accuracy, pass rate) │
└──────────────┬───────────────────────────────┘
               │ returns scalar score
               ▼
┌──────────────────────────────────────────────┐
│              Keep / Discard decision           │
│  if score improved → commit, update program.md│
│  if score regressed → revert, log failure     │
└──────────────────────────────────────────────┘
               │
               └── loop back to step 1
```

### Key design principles

1. **`program.md` as durable context** — survives context window limits; the agent reads it fresh each iteration
2. **Objective scorer required** — no self-assessed "I think this is better"; only measurable metrics count
3. **Minimal diffs** — each hypothesis changes one thing; avoids confounding
4. **Automatic revert on regression** — failures are logged but never promoted
5. **Bounded autonomy** — the loop runs unattended but within pre-set iteration limits and safety constraints

### Adaptation beyond ML training

The pattern generalizes to any domain with an objective function:

| Domain | `program.md` | `train.py` (scorer) |
|---|---|---|
| ML training | Model config, hyperparameters | Training loss, validation accuracy |
| Agent prompt engineering | System prompt + tool schemas | Task success rate on eval suite |
| Code optimization | Codebase state, perf targets | Benchmark runtime, test pass rate |
| Content generation | Style guide, topic constraints | Human preference model score |
| Factory quality (this project) | AGENT_SPEC + SKILL_SPEC | Validator pass rate, manual grading scores |

### Real-world results

- **NanoGPT**: 700 experiments, 20 optimizations kept, 11% training loss improvement (2 days autonomous)
- **Shopify** (production adaptation): 19% improvement in code generation quality
- **Factory Showcase** (this project): 5-cycle Karpathy loop + 7-wave autoresearch across 20 agents + 20 skills. AGENT_SPEC mean: 7.6 → 9.04 (+1.44). CLASSic mean: 5.5 → 9.02 (+3.52). ~100 iterations total. Key finding: observability was the biggest single-wave improvement (+9.0 from zero)

See [Karpathy autoresearch (wiki)](../wiki/research/karpathy-autoresearch.md) and the [original repo](https://github.com/karpathy/autoresearch).

---

## Exercises

1. **Design a learning loop for a coding agent**  
   Specify capture format (what gets logged), how often humans review proposals, what artifacts may change automatically (prompt only? tests?), and how you prevent the loop from optimizing for “tests green” while breaking real users. One page of bullets is enough.

2. **Build a score-driven evaluation harness**  
   Pick three small tasks (e.g., refactor, bugfix, docstring). Implement or pseudocode a script that runs the agent, scores outcomes with a simple rubric (0–2 per criterion), and writes results to JSON. Add a rule: only accept a new `program.md` if **held-out** task average does not drop. Document one way the agent could game your score and how you would patch the metric.

3. **Karpathy loop simulation**  
   Choose a simple task (e.g., optimizing a sorting function's performance). Write a `program.md` describing the goal. Run 5 manual iterations of the loop: read program.md → hypothesize → make a minimal change → measure (wall-clock time, correctness) → keep or discard. Log each iteration's hypothesis, result, and decision. What percentage of hypotheses were kept?

---

## Further reading

- [Harness engineering (wiki)](../wiki/concepts/harness-engineering.md)
- [Self-improving agents (wiki)](../wiki/concepts/self-improving-agents.md)
- [AutoAgent harness patterns (wiki)](../wiki/research/autoagent-harness-patterns.md)
- [Karpathy autoresearch (wiki)](../wiki/research/karpathy-autoresearch.md)
- [AutoAgent harness loop (good example)](../wiki/examples/good/autoagent-harness-loop.md)
- [Hermes self-improving (good example)](../wiki/examples/good/hermes-self-improving.md)
