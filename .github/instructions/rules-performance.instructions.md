---
applyTo: "rules/performance/**"
---

# Performance Rules — Copilot Custom Instructions

You are assisting with SonarQube **performance** rule definitions in the `rules/performance/` directory. This category targets runtime efficiency problems that degrade application throughput, increase latency, waste resources, or lead to capacity bottlenecks under load.

---

## Category Context

This directory currently contains **18 rules** covering database access patterns, memory management, concurrency issues, I/O efficiency, collection misuse, and resource lifecycle problems. Rules here focus on measurable runtime impact — not code style.

---

## Rule Authoring Guidelines for Performance

### Type & Severity
- **Type** is typically `CODE_SMELL` for inefficiency patterns, or `BUG` when the issue causes resource exhaustion, deadlocks, or data corruption under load.
- **Severity** mapping:
  - `CRITICAL` — causes visible degradation in production (N+1 queries, memory leaks, connection pool exhaustion, thread pool starvation).
  - `MAJOR` — measurable impact under moderate load (inefficient loops, unnecessary boxing, suboptimal collections).
  - `MINOR` — micro-optimizations with limited real-world impact (minor object creation overhead in cold paths).

### Impacts
- Primary `softwareQuality` is typically `"MAINTAINABILITY"` (since performance smells increase operational burden) or `"RELIABILITY"` (when they cause failures under load).
- Use `"HIGH"` severity for issues that cause outages or severe SLA violations.
- Use `"MEDIUM"` for issues that cause gradual degradation.
- Add a secondary impact when appropriate — many performance issues affect both reliability and maintainability.

### Tags — Required Conventions
- Always include `"performance"` as a tag.
- Include the resource domain: `"database"`, `"memory"`, `"cpu"`, `"io"`, `"network"`, `"concurrency"`, `"threading"`.
- Include the pattern type: `"optimization"`, `"resource-management"`, `"caching"`, `"pooling"`, `"batching"`.
- Add `"orm"` when the rule is specific to ORM frameworks (Hibernate, JPA, Entity Framework).

### Description Best Practices
- Quantify the impact when possible: "causes N additional database round-trips per parent entity" or "allocates O(n²) temporary objects".
- Explain the **scaling behavior** — does the problem get worse linearly, quadratically, or exponentially with load?
- Describe the **production symptom**: increased latency, CPU spikes, memory pressure, connection timeouts, thread exhaustion.
- Specify the context where the issue manifests (hot paths, request handlers, batch jobs, event loops).

### Remediation Examples
- `before` examples must show the **inefficient pattern in context** — include the loop, the query call site, or the resource acquisition.
- `after` examples must show the **optimized approach**: batch fetching, connection pooling, lazy initialization, proper resource cleanup, async patterns.
- Show framework-specific solutions where relevant (e.g., `@BatchSize` for Hibernate N+1, `try-with-resources` for leaks).
- Remediation cost should reflect real-world effort: simple refactor → `"15min"`–`"30min"`, architectural change (adding caching, connection pooling) → `"2h"`–`"4h"`.

### Parameters (params)
- Performance rules often benefit from thresholds: max iterations before suggesting batching, collection size limits, timeout values.
- Common params: `maxIterations`, `maxCollectionSize`, `connectionTimeout`, `batchSize`, `maxAllocationRate`.
- Provide defaults based on production-informed baselines.

### Debt Estimation
- Use `CONSTANT_ISSUE` for localized fixes (wrapping in try-with-resources, switching to StringBuilder, adding batch annotation).
- Use `LINEAR` when remediation scales with the number of affected call sites (e.g., replacing all raw string concatenations in loops across a codebase).

### Common Pitfalls to Avoid
- Do NOT conflate performance smells with code smells — a performance rule must have **measurable runtime impact**, not just "this could be written more elegantly".
- Do NOT mark micro-optimizations as `CRITICAL` — reserve that for issues with proven production impact.
- Do NOT forget to describe the **load condition** under which the problem manifests.
- Do NOT ignore concurrency concerns — many performance rules interact with threading (race conditions, pool exhaustion).
- Do NOT duplicate rules that already exist in this directory — check for overlapping resource concerns.

---

## When Creating New Performance Rules

1. Verify the performance issue has **measurable impact** — can you describe the O(n) complexity or resource waste?
2. Determine if it's a `BUG` (causes failures under load) or `CODE_SMELL` (causes degradation but not failure).
3. Name the `key` after the anti-pattern or the symptom (e.g., `"n-plus-one-query"`, `"connection-pool-exhaustion"`).
4. Describe the scaling behavior and the production context where it manifests.
5. Provide remediation that targets the specific framework/runtime the pattern appears in.

---

## Existing Rules Reference

connection-pool-exhaustion, excessive-object-creation, inefficient-collection-usage, inefficient-loops, memory-leaks, missing-batch-operations, missing-lazy-initialization, missing-transaction-boundary, n-plus-one-query, race-condition, resource-leak, string-concatenation-in-loop, synchronous-io-in-async, thread-pool-starvation, unbounded-collection-growth, unclosed-resources, unnecessary-boxing, unoptimized-regex
