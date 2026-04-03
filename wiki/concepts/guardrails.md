# Guardrails

## What it is

**Guardrails** are enforceable boundaries on what agents may read, infer, or do: **input validation** on user and tool-supplied data, **output filtering** (PII redaction, policy classifiers, schema validation), **behavioral boundaries** in prompts backed by code (allowlisted tools, path prefixes), **content policies** (refusal templates, topic blocks), and layered **safety** (sandboxing, secrets isolation, approval gates).

Guardrails are not “please be nice” instructions alone—they are **defense in depth** where the model is untrusted relative to system intent.

## Why it matters for agents

Agents combine **prompt injection** surface (untrusted documents, web pages, user messages) with **side-effecting tools**. Without guardrails, a single crafted paragraph can exfiltrate data or trigger mutations. Regulated environments require demonstrable controls, not optimism.

## How to implement it

1. **Input path:** validate size, type, and encodings; strip or quarantine HTML; separate *trusted developer instructions* from *untrusted user content* with delimiters and parsing rules.
2. **Tool layer:** allowlists, argument validators, read vs write roles, sandboxed execution for code.
3. **Output path:** JSON/schema enforcement; regex or ML filters for secrets; block streaming until final structured object validates.
4. **Policy layers:** lightweight classifier for escalation; high-risk tools require HITL.
5. **Monitoring:** log policy hits with trace ids; sample for red-team regression tests.

**Behavioral boundaries** belong in `system-prompt.md` *and* in code: if the code allows an action, the prompt denied it is worthless; if the code forbids it, the prompt is backup UX.

## Layered defense sketch

1. **Edge:** WAF/size limits/authn on your agent API.  
2. **Pre-model:** strip/quarantine untrusted attachments; run PII detectors if required.  
3. **Model envelope:** system vs developer vs user roles where the API supports separation.  
4. **Tool shell:** allowlists, argument validation, sandboxed execution.  
5. **Post-model:** schema validation, secret scanners on text, optional secondary classifier for policy classes.

Each layer logs **which** rule fired to support appeals and tuning.

## Red teaming cadence

Run **automated adversarial suites** on each prompt/tool change: injection strings, jailbreak templates, and tool argument fuzzing proportional to risk tier. Track regressions like unit tests; failing gates block release for high-risk agents.

## Common mistakes

- **Safety by optimism** assuming the model will refuse attacks.
- **Trusting tool output** as instructions for privileged APIs.
- **Brittle regex** on model prose instead of structured channels.
- **Single layer:** only prompt, no schema or sandbox.

## References to course modules

These map to the **23-module Agent Factory course** (see [`../../course/README.md`](../../course/README.md) when published).

- **Module 18 — Safety and Guardrails** — threat modeling, policies, and enforcement layers.
- **Module 05 — Tool Design and Integration** — least-privilege tools and narrow blast radius.
- **Module 11 — Anti-Patterns** — common safety mistakes and how to avoid them.

Full curriculum index: [`../../course/README.md`](../../course/README.md) (when present).

## See also

- [Human-in-the-Loop](human-in-the-loop.md)
- [Tool Design](tool-design.md)
- [Sandboxing](sandboxing.md)
- [Agent Security](agent-security.md)
- [Prompt Engineering for Agents](prompt-engineering-for-agents.md)
