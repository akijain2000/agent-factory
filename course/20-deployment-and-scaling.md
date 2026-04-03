# Module 20: Deployment and Scaling

**Duration:** approximately 35 minutes  
**Prerequisites:** Module 18 (Safety and Guardrails); Module 19 (Observability and Debugging) recommended.

---

## Learning objectives

By the end of this module, you should be able to:

- **Deploy** agents on serverless, container, or hybrid infrastructure matched to workload shape.
- **Optimize** cost at scale using routing, caching, and batching without sacrificing reliability.
- **Handle** provider and downstream rate limits with queues, backoff, and degradation.
- **Choose** between long-running services and on-demand workers using clear criteria.

---

## Deployment options: serverless (Modal, Lambda), containers (Docker, Fly.io), edge

**Serverless functions** suit **spiky**, short tasks: single-turn classification, small tool graphs, bursty user traffic. Cold starts and **timeouts** hurt **long** reasoning chains unless you use **async** invocation and external state stores.

**Containers** on **Fly.io**, Kubernetes, or ECS give **predictable** runtimes for **minutes-long** agent jobs, custom system dependencies, and sidecars (proxies, local vector stores).

**Edge** deployment helps **latency-sensitive** thin clients but rarely hosts full tool-using agents; more often you run **small** routers or policy checks at the edge and **heavier** work in a region.

Decision checklist:

- Max **duration** per task vs platform limit.
- Need for **GPU** or large memory.
- **Data residency** and VPC peering to internal APIs.

---

## Long-running agents vs on-demand agents

**Long-running** processes (WebSocket sessions, persistent workers) preserve **warm** context and cheap **incremental** tool chatter; they need **heartbeat**, **reconnection**, and **graceful drain** on deploy.

**On-demand** workers pull jobs from a **queue**, run to completion, and exit; simpler autoscaling and blast radius, higher **per-job** startup cost.

Hybrid: **session front door** keeps UX responsive; **backend jobs** handle heavy codegen or batch evaluation.

---

## Cost optimization at scale: model routing, caching, batching

**Model routing:** send easy subtasks to **smaller** models; reserve frontier models for planning, ambiguity, or verification. Use **classifiers** or heuristics (length, language, domain) at the router.

**Caching:** cache **embeddings** and **retrieval** results keyed by corpus version; cache **LLM** responses only when **determinism** and **staleness** rules are explicit (e.g., FAQ with TTL).

**Batching:** group **offline** evals or summarization jobs; interactive agents rarely tolerate batch delay, but **nightly** jobs do.

Measure **savings** per technique; routing bugs that send hard tasks to small models show up as **silent** quality loss.

```python
def choose_model(task: Task) -> str:
    if task.risk_tier == "high" or task.ambiguity_score > 0.7:
        return "frontier-reasoning"
    if task.type in ("extract", "classify"):
        return "small-fast"
    return "default-balanced"
```

---

## Rate limit handling: queuing, backpressure, graceful degradation

Providers return **429** or quota errors; downstream APIs have **per-tenant** caps. Patterns:

- **Exponential backoff** with **jitter**; respect `Retry-After` when present.
- **Per-key** token buckets in Redis or in-process for single-host prototypes.
- **Queue** excess work; **shed load** with user-visible “try again” rather than unbounded retries.

**Backpressure:** slow **acceptance** of new runs when queue depth or error rate exceeds thresholds; protects workers and budgets.

**Degradation:** fall back to **cached** answers, shorter summaries, or **human** handoff when limits hit—document which degradations are **allowed** per product tier.

```python
async def call_with_limits(client, coro_factory, key: str):
    await rate_limiter.acquire(key)
    try:
        return await coro_factory()
    except RateLimited as e:
        await asyncio.sleep(e.retry_after_s)
        return await coro_factory()
```

---

## Scaling patterns: horizontal scaling, queue-based architectures

**Horizontal scaling:** stateless **workers** behind a load balancer; **sticky sessions** only if you must (prefer external session state).

**Queue-based:** producers enqueue `RunRequest`; workers **ack** after persistence of results. Enables **priority queues** (paid vs free) and **retry** semantics.

**Autoscaling** on **queue depth** or **CPU**; avoid scaling purely on request rate if each request triggers **heavy** background jobs—track **end-to-end latency** and **queue age**.

**Health checks and rollouts:** liveness should verify **worker can reach** dependencies (queue, secrets backend) without calling paid LLMs every probe. Use **readiness** to drain traffic before deploy; for agents, finish or **checkpoint** in-flight runs before terminating pods. **Blue/green** or **canary** new prompt bundles on a **small** traffic slice while comparing **error rate** and **cost per task** to baseline.

---

## Study: Hermes Agent's $5 VPS to GPU cluster range, Modal/Daytona serverless

**Hermes**-style self-improving agents illustrate **wide** deployment elasticity: from **minimal** VPS for orchestration and cheap loops to **GPU** clusters for training or large-batch eval. The lesson is to **match** spend to **experimental phase**—do not rent clusters before product-market fit on a single region container.

**Modal** and **Daytona** represent **serverless** sandboxes and functions colocated with **ephemeral** compute; valuable for **bursty** codegen or eval farms. Study their **cold start**, **network egress**, and **secret** models before committing core paths.

---

## Exercises

1. **Deployment architecture**  
   For an agent that averages 3 minutes per run, calls internal APIs in your VPC, and sees 10x traffic spikes twice daily, sketch a **deployment diagram** (bullets are fine): components, queue vs synchronous API, where secrets live, and how you **roll out** a new prompt version without dropping in-flight runs.

2. **Rate limit handling**  
   Implement or pseudocode a **token-bucket** limiter shared across worker processes (e.g., Redis), including **max wait** and **failure** behavior when the wait exceeds a SLA. Explain how you would **test** it under contention.

---

## Further reading

- [Deployment patterns (wiki)](../wiki/concepts/deployment-patterns.md)
- [Rate limiting (wiki)](../wiki/concepts/rate-limiting.md)
- [Cost optimization (wiki)](../wiki/concepts/cost-optimization.md)
