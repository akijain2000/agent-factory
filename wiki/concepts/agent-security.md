# Agent Security

## What it is

**Agent security** is the set of controls that keep **LLM-driven automation** from being misused to leak data, escalate privilege, or corrupt systems. It spans **prompt injection** defense (untrusted content influencing tools), **data exfiltration** prevention (what the model may emit or fetch), **least privilege** for tools and credentials, **secrets management** (rotation, scoping, no prompts), and **audit logging** (who approved what, which tools ran, with which arguments). A concise **threat model** ties these to actors: malicious users, compromised documents, poisoned retrieval, and compromised supply chains.

## Why it matters for agents

Agents **act**: they call APIs, run code, and read files. A single successful injection can exfiltrate **PII**, trigger **financial** actions, or pivot through internal networks. Unlike static apps, the attack surface includes **natural language** and **dynamic plans**. Security failures are often **silent** until an incident—logs without structured tool traces are not auditable.

Agents also inherit **supply-chain** risk: compromised dependencies in tools, poisoned **skills** libraries, and **shadow** APIs added without review expand blast radius faster than in traditional apps.

## How to implement it

1. **Trust boundaries:** treat **user content**, **web pages**, and **email bodies** as hostile. Never let them override **system policy** without a separate authorization path (human or rules engine).
2. **Prompt injection mitigations:** separate **instructions** from **data** (delimiters, structured channels); use **output filters** for known secret patterns; constrain tools to **allow-listed** operations; consider **dual-control** for high-risk tools.
3. **Data exfiltration:** block or scan outbound destinations; redact logs; avoid passing full **secret stores** into context. For retrieval, enforce **document ACLs** at query time.
4. **Least privilege:** one **scoped** credential per tool or tenant; short-lived tokens; no shared “god” API keys in the harness. Default **deny** for filesystem and network tools.
5. **Secrets management:** inject via KMS/Vault/env at runtime; rotate on compromise; never echo secrets in **tool results** returned to the model.
6. **Audit logging:** append-only records of `run_id`, `actor`, `tool`, `args_hash`, `outcome`, and **policy version**. Correlate with **human approvals** where applicable.

7. **Output and egress controls:** DLP-style scanning on assistant messages when channels are **external**; block attachment of **private** URLs to public tickets.

**Defense in depth:** no single layer (prompt, classifier, sandbox) is sufficient; combine **policy in code** with **runtime isolation**.

## Threat model sketch

Enumerate assets (customer data, internal APIs), entry points (chat, files, web tools), and misuse cases (exfiltration, privilege abuse, denial of wallet). Review after every **new tool** or **model** upgrade.

Run **tabletop** exercises for injection via **email**, **PDF**, and **web** tools—channels users forget to mark untrusted.

Map controls to frameworks your customers ask for (SOC2, ISO) so sales and security share the same **control narrative**.

**Red-team** findings should flow into **regression** tests—prompt injections become fixtures, not anecdotes.

## Common mistakes

- **Prompt-only** safety (“do not reveal secrets”) without tool-level enforcement.
- Logging **full prompts** containing PII or keys for “debugging.”
- **Overprivileged** shell or SQL tools attached to general assistants.
- Skipping **reviews** when adding tools that read email or payment systems.
- **Storing** raw transcripts in analytics warehouses without **redaction** pipelines.
- Assuming **internal** chat is safe—colleagues can paste **phishing** content the agent then acts on.

## References to course modules

These map to the **23-module Agent Factory course** (see [`../../course/README.md`](../../course/README.md) when published).

- **Module 18 — Safety and Guardrails** — threat modeling, trust boundaries, and isolation.
- **Module 05 — Tool Design and Integration** — contracts that resist misuse and limit blast radius.
- **Module 19 — Observability and Debugging** — audit-grade telemetry without leaking secrets.

Full curriculum index: [`../../course/README.md`](../../course/README.md) (when present).

## See also

- [Guardrails](guardrails.md)
- [Sandboxing](sandboxing.md)
- [Tool Design](tool-design.md)
- [Observability](observability.md)
- [Human-in-the-Loop](human-in-the-loop.md)
