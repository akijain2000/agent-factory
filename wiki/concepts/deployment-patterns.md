# Deployment Patterns

## What it is

**Deployment patterns** describe where and how agent runtimes execute: **serverless** (ephemeral functions, pay-per-invocation), **containers** (Docker images on VMs, Kubernetes, or PaaS), and **edge** (low-latency nodes close to users). For agents, the choice couples to **cold start**, **GPU availability**, **network egress to model APIs**, and whether work is **on-demand** (per user message) versus **long-running** (watches, schedulers, background research). Representative stacks include **Modal** (Python-centric serverless with custom images), **Daytona** (dev sandboxes and isolated environments for coding agents), **Fly.io** (global VMs and Machines with persistent volumes), and plain **Docker** (portable images for any orchestrator).

## Why it matters for agents

Agent workloads are bursty, often **I/O-bound** (LLM and tool calls), and sometimes **CPU- or GPU-bound** (local models, embeddings). The wrong topology yields timeouts on HTTP gateways, **orphaned** side effects when functions freeze mid-loop, or runaway cost when every step spins a new cluster. Long-running agents need **durable state** and **graceful shutdown**; on-demand agents need **fast scale-to-zero** and **idempotent** resume. Deployment is the substrate for **sandboxing**, **secrets**, and **observability** export.

Poor placement also complicates **compliance**: model calls may need to stay in-region, while user-facing APIs may need **global** edges. Treat **egress** (to providers, to customer VPCs) as a first-class line item in architecture reviews.

## How to implement it

1. **Classify the agent:** interactive (short runs, strict latency) vs worker (minutes to hours) vs cron-like (scheduled). Map each to max wall time and concurrency.
2. **Serverless / functions:** wrap each **iteration** or **bounded chunk** of the loop in a function with a hard timeout; persist state (run id, messages, tool results) in object storage or a DB between invocations. Use **async** job queues for anything exceeding gateway limits.
3. **Containers:** package the harness, tool binaries, and config in one image; inject secrets at runtime (not bake-time). Use **read-only** root where possible; mount ephemeral workspaces for coding agents.
4. **Edge:** reserve for **latency-sensitive** pre/post processing (classification, redaction) or cached retrieval; avoid placing full autonomous loops at the edge unless models and policies are local and compliant.
5. **Modal / similar:** define images and secrets declaratively; colocate data-heavy steps in the same region as storage; cap **concurrency** per account to match provider and your budget.
6. **Daytona-style sandboxes:** isolate **file and network** surface for untrusted code; tear down environments after runs; snapshot only when audits require it.
7. **Fly.io / VMs:** use **Machines** or similar for processes that must stay warm; attach volumes for durable checkpoints; health-check the agent API separately from the model provider.

**Long-running vs on-demand:** long-running favors processes with **supervisors** (systemd, k8s Deployment) and **heartbeats**; on-demand favors **queue workers** and **stateless** handlers that reload state each time.

**Networking:** put the harness in the same **region** as data stores when tools read/write heavily; use **private** connectivity to internal APIs. For coding agents, restrict outbound **egress** lists to package registries and known git hosts.

**Images and supply chain:** pin base images with **digest**; scan for CVEs in CI; rebuild on **critical** patches. Agent images often bundle CLIs (`git`, language runtimes)—smaller images start faster and reduce attack surface.

## Operational checklist

Define **SLA** per surface (time to first token, max run duration). Log **run_id** with deployment **revision** and **region**. For multi-step loops, ensure **at-least-once** delivery does not double-charge: idempotency keys on tool side effects.

**Decision cues:** choose **serverless** when invocations are short, spiky, and state is externalized; choose **containers/VMs** when you need **hours-long** runs, GPUs, or sticky local caches; choose **edge** only when latency or data locality truly dominates and the workload is **constrained**.

## Common mistakes

- Holding **HTTP requests open** for unbounded agent loops instead of returning run ids and streaming events.
- **Cold starts** on every message without connection pooling or warm pools for premium tiers.
- Running agents with **same network** as production databases without network segmentation.
- **Pinning** one pattern globally (everything serverless) when workers need hours and GPUs.
- **Undersized** health checks that only ping `/health` while the **tool pool** or **queue** is dead.
- **Co-locating** dev and prod agent credentials in one cluster without **namespace** isolation.

## References to course modules

These map to the **23-module Agent Factory course** (see [`../../course/README.md`](../../course/README.md) when published).

- **Module 20 — Deployment and Scaling** — topology, SLAs, graceful shutdown, and orphaned-run recovery.
- **Module 19 — Observability and Debugging** — correlating deploys with traces and failures.
- **Module 18 — Safety and Guardrails** — production hardening and blast-radius controls.

Full curriculum index: [`../../course/README.md`](../../course/README.md) (when present).

## See also

- [Observability](observability.md)
- [Cost Optimization](cost-optimization.md)
- [Sandboxing](sandboxing.md)
- [Agent Lifecycle](agent-lifecycle.md)
- [Rate Limiting](rate-limiting.md)
