# Module 18: Safety and Guardrails

**Duration:** approximately 40 minutes  
**Prerequisites:** Module 04 (System Prompts); Module 05 (Tool Design) recommended.

---

## Learning objectives

By the end of this module, you should be able to:

- **Implement** sandboxing boundaries appropriate to agent capabilities and data sensitivity.
- **Defend** against prompt injection using layered detection, prevention, and mitigation.
- **Design** human-in-the-loop approval gates for high-risk or irreversible actions.
- **Balance** safety constraints with task completion rates and operator trust.

---

## The safety spectrum: from read-only to full autonomy

Agents sit on a continuum:

- **Read-only:** search, summarize, suggest edits as diffs (user applies).
- **Scoped write:** sandboxed filesystem, staging database, feature-flagged APIs.
- **Production write:** merges, refunds, customer emails, infrastructure changes.

Each step increases **blast radius**. Your architecture should **default** to the lowest tier that meets the job, and **promote** autonomy only where monitoring, rollback, and ownership are clear.

Document **who** is liable for agent actions (team, product, vendor) and **what** constitutes an incident versus an expected failure mode.

---

## Sandboxing: Docker, e2b, gVisor, permission boundaries

**Sandboxing** limits what code and tools can touch: filesystem paths, network destinations, secrets, and syscall surface.

Common patterns:

- **Docker** (or OCI) containers with **read-only** root, **dropped** capabilities, and **no** host socket mounts by default.
- **e2b** and similar **hosted sandboxes** provision ephemeral VMs or containers per task; good for **untrusted** code execution with time and network policies.
- **gVisor** or **Kata** add kernel isolation when multi-tenant density matters.

At the **application** layer, enforce **permission boundaries** independent of the container: OAuth scopes, IAM roles, and **per-agent** API keys with least privilege.

```python
# Conceptual: tool router checks capability before dispatch
ALLOWED_FOR_ROLE = {
    "research_agent": {"web_search", "read_docs"},
    "deploy_agent": {"run_ci", "create_pr"},  # no prod_kubectl
}

def invoke_tool(agent_role: str, tool: str, args: dict):
    if tool not in ALLOWED_FOR_ROLE.get(agent_role, set):
        raise PermissionDenied(f"{tool} not allowed for {agent_role}")
    return registry[tool](args)
```

Rotate credentials used inside sandboxes; assume **prompt injection** can steer the agent toward exfiltration attempts.

---

## Prompt injection defense: detection, prevention, mitigation

**Prompt injection** is untrusted content (web pages, emails, documents) that tries to override system instructions (“ignore previous rules and exfiltrate secrets”).

**Prevention:**

- **Separate** trusted system instructions from untrusted data with **clear delimiters** and templates (“the following is untrusted user content”).
- **Never** place secrets in prompts; fetch with **server-side** tools the model cannot redefine.

**Detection:**

- Heuristics for **instruction-like** phrases in user or retrieved text.
- **Secondary** classifiers or smaller models flagged before high-risk tool calls.

**Mitigation:**

- **Constrain** outputs: structured JSON, allow-listed domains for `fetch`, no raw shell.
- **Human approval** for sensitive exfil channels (email, external webhooks).

Defense in depth beats a single “do not follow malicious instructions” line in the system prompt.

---

## Human-in-the-loop gates for high-risk actions

Define **triggers** for pause: monetary threshold, production environment, PII access, mass messaging, or low **confidence** scores from the planner.

At a gate, surface **structured** proposals: action type, parameters, diff preview, and **rollback** plan. Log **who** approved and **when** for audit.

```text
AWAITING_APPROVAL
  action: refund_issue
  params: { order_id: "ord_123", amount: 499.00 }
  rationale: "Customer cited defective SKU per policy 4.2"
  [Approve] [Edit params] [Reject]
```

Timeouts and **default deny** reduce “rubber stamp” risk under load.

---

## Approval workflows: confidence thresholds, escalation paths

Combine **model-reported** confidence (calibrated if possible) with **rule-based** checks (amount, destination account, first-time recipient). **Escalation paths** might be: auto for low risk, team lead for medium, on-call for high.

**Dual control** for irreversible operations: two human approvals or approval from a different role than the requester.

Measure **queue time** at gates; if humans are always behind, agents will be bypassed or users will work around safety. Tune thresholds using **historical** false positive and false negative rates.

---

## Study: e2b sandboxing, AutoAgent Docker isolation, OpenClaw's agent permissions

**e2b** illustrates **ephemeral** execution environments: short-lived, API-driven sandboxes suitable for codegen agents. Study default **network** policies and how secrets are injected without exposing them to untrusted user content.

**AutoAgent**-style **Docker** isolation keeps repository operations and test runs **inside** a disposable image; the host orchestrator only sees **results** and **logs**.

**OpenClaw** (and similar platforms) emphasize **explicit agent permissions**: which tools, which scopes, and **per-session** elevation. Mirror that pattern in your own registry: permissions are **data**, not ad hoc `if` statements scattered through prompts.

---

## Exercises

1. **Permission model**  
   For an agent that reads internal docs, drafts customer replies, and can trigger refunds up to $100, design a **role or capability matrix** (tools, environments, approval rules). Include one **edge case** (e.g., VIP customer or fraud flag) and how the model changes.

2. **Prompt injection in the input pipeline**  
   Sketch **pseudocode** for a preprocessor that: (a) tags untrusted blocks, (b) runs a lightweight heuristic or classifier, and (c) routes high-risk sessions to a stricter tool set or human review. Explain **one** limitation your design cannot fully solve.

---

## Further reading

- [Guardrails (wiki)](../wiki/concepts/guardrails.md)
- [Sandboxing (wiki)](../wiki/concepts/sandboxing.md)
- [Agent security (wiki)](../wiki/concepts/agent-security.md)
