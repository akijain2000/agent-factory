# Sandboxing

## What it is

**Sandboxing** isolates agent-executed code and tools from the host environment and sensitive data. Typical layers include **OS containers** (Docker), **microVMs or hardened kernels** (Firecracker, **gVisor** as a runtime isolation layer), **managed sandboxes** (e.g., **E2B** and similar API sandboxes for arbitrary code), and **permission boundaries** (separate cloud accounts, scoped IAM, read-only mounts, network egress allowlists). The agent’s process should not equate to root on production infrastructure.

## Why it matters for agents

Models are stochastic and user input is adversarial; **tool misuse** or **prompt injection** can exfiltrate secrets or destroy data. Sandboxes contain blast radius, make **least privilege** enforceable, and give security reviewers a clear trust boundary. They also improve reproducibility: runs see a defined filesystem and dependency set.

## How to implement it

1. **Classify tools:** read-only queries vs mutating vs arbitrary code; escalate isolation with risk.
2. **Container baseline:** minimal image, non-root user, no host Docker socket, dropped capabilities, seccomp where supported.
3. **Network policy:** default deny; allow only required egress; use a proxy for audit logging of outbound URLs.
4. **Secrets:** never mount production credentials into code-execution sandboxes; use short-lived tokens brokered by a sidecar.
5. **Resource limits:** CPU, memory, wall-clock timeouts, output size caps; kill runaway processes deterministically.
6. **Managed sandboxes:** prefer for user-supplied code; map each session to a disposable environment with explicit data import/export.

## Permission boundaries

Separate **control plane** (orchestrator, approvals) from **data plane** (tool execution). Use scoped roles per tool class. For browser or shell tools, require human approval or static allowlists of commands.

## Docker, e2b, and gVisor roles

**Docker** (or OCI containers) provides filesystem and package isolation suitable for many internal tools when combined with seccomp, user namespaces, and strict images. **e2b** and similar APIs offer **ephemeral** dev environments ideal for user code: fast spin-up, no host coupling, explicit file exchange. **gVisor** adds a userspace kernel between containers and the host kernel—useful when multi-tenant density demands stronger syscall filtering than default runc profiles. Pick **depth** of isolation from threat model: trusted internal batch jobs vs arbitrary user uploads.

## Designing sandbox contracts

Document **inputs** (files, env vars), **outputs** (artifacts, logs), **forbidden** capabilities, and **cleanup** semantics. Automate image builds; pin digests in prod. Test sandbox **startup** and **teardown** as part of deploy health checks.

## Multi-tenant isolation

Never share writable temp directories across tenants. Reset state between sessions. If using warm pools, verify no residual processes or mounts leak between jobs.

## Common mistakes

- Running shell tools on the host with the orchestrator’s full filesystem access.
- Sharing one long-lived container across untrusted tenants without reset.
- Allowing outbound network from code sandboxes without domain restrictions.
- Treating “read-only” SQL as safe without row-level security and connection scoping.

## Quick checklist

- Images are pinned; non-root user; read-only root filesystem where feasible.
- Egress default-deny with audited exceptions; no production secrets in sandbox env.
- Timeouts and output caps tested under load, not only in happy paths.

## References to course modules

These map to the **23-module Agent Factory course** (see [`../../course/README.md`](../../course/README.md) when published).

- **Module 06 — MCP: Servers, Resources, and Security** — trust boundaries for tools.
- **Module 20 — Sandboxing & Isolation** — containers, gVisor, and policies.
- **Module 21 — Secrets, IAM, and Blast Radius** — credential hygiene for agents.

Full curriculum index: [`../../course/README.md`](../../course/README.md) (when present).

## See also

- [Guardrails](guardrails.md)
- [Agent Security](agent-security.md)
- [Tool Design](tool-design.md)
- [Error Recovery](error-recovery.md)
- [Deployment Patterns](deployment-patterns.md)
