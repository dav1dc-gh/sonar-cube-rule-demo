---
applyTo: rules/performance/**
---

# Performance Rules — Custom Instructions

You are assisting with SonarQube **performance** rule definitions in `rules/performance/`. These rules detect runtime efficiency problems that degrade throughput, increase latency, waste resources (CPU, memory, I/O, network), or cause scalability bottlenecks under load.

## Category Constraints

- **`type` is `CODE_SMELL` or `BUG`** — use `BUG` when the issue causes observable failures at scale (e.g., memory leaks that crash the process, connection pool exhaustion that causes downtime). Use `CODE_SMELL` for inefficiencies that degrade performance without causing outright failure.
- **`severity` should be `CRITICAL` for production-impacting issues** (N+1 queries, memory leaks, connection exhaustion). Use `MAJOR` for suboptimal patterns that cause measurable but non-critical degradation.
- **`tags` MUST include `"performance"`** as the first tag. Add domain-specific tags: `"database"`, `"orm"`, `"memory"`, `"concurrency"`, `"io"`, `"gc"`, `"caching"`, `"optimization"` where applicable.
- **`impacts` should target `"MAINTAINABILITY"` or `"RELIABILITY"`** — performance issues can impact both. Use `"RELIABILITY"` with severity `HIGH` for issues that cause failures under load.

## Writing Performance Rule Descriptions

Descriptions must clearly communicate:
1. **The inefficiency pattern** — the specific code construct causing the problem (e.g., "database query executed inside a loop iterating over N elements").
2. **The scaling behavior** — how performance degrades (e.g., "produces O(N) queries instead of O(1), causing response times to grow linearly with dataset size").
3. **The production impact** — real-world consequences (e.g., "under typical production loads of 10K+ records, this causes 30-second response times and database connection pool saturation").

Use quantitative language where possible: O(N), latency multipliers, memory growth patterns, connection counts.

## Remediation Examples

Performance remediation examples MUST show:
- **Before**: The inefficient pattern with a comment indicating the performance characteristic (e.g., `// O(N) queries`, `// allocates on every iteration`).
- **After**: The optimized version with a comment explaining the improvement (e.g., `// Single query with JOIN`, `// Reuses pre-allocated buffer`).

Common optimization patterns to reference:
- N+1 queries → Eager loading, JOIN fetch, batch queries, `@EntityGraph`
- String concatenation in loop → `StringBuilder`, `String.join()`, `Collectors.joining()`
- Excessive object creation → Object pooling, flyweight, pre-allocation, primitive arrays
- Connection leaks → try-with-resources, connection pool configuration, `finally` blocks
- Unbounded collections → LRU eviction, size limits, weak references, `Cache` implementations
- Synchronous I/O in async → Non-blocking I/O, reactive streams, `CompletableFuture`
- Inefficient collections → `HashMap` vs `TreeMap` choice, `ArrayList` vs `LinkedList`, pre-sizing
- Unnecessary boxing → Primitive specializations, `IntStream`, `OptionalInt`
- Regex backtracking → Possessive quantifiers, atomic groups, pre-compiled patterns

## Remediation Cost Guidelines

| Fix Complexity | `constantCost` | Examples |
|---|---|---|
| Swap API call | `10min` | `StringBuilder` instead of `+`, pre-size collection |
| Add batch/bulk operation | `30min` | Batch DB writes, eager fetch |
| Introduce caching layer | `1h` | Add memoization, result cache, connection pool |
| Architectural restructuring | `4h` | Async pipeline, read replicas, CQRS |

## Performance-Specific Params

Performance rules should expose thresholds when the "hot path" definition is configurable:

| Common Parameter | Type | Typical Default | Use When |
|---|---|---|---|
| `maxIterations` | `INTEGER` | `100` | Loop-based inefficiency thresholds |
| `maxQueryCount` | `INTEGER` | `10` | Maximum acceptable queries per operation |
| `maxObjectAllocations` | `INTEGER` | `1000` | Object creation in tight loops |
| `maxCollectionSize` | `INTEGER` | `10000` | Unbounded growth detection |
| `timeoutMs` | `INTEGER` | `5000` | Blocking operation thresholds |

## Severity Decision Matrix

| Production Impact | Scaling | Severity |
|---|---|---|
| Causes outage / OOM / connection exhaustion | O(N²) or worse | `CRITICAL` |
| Measurable latency degradation at typical scale | O(N) where N is large | `CRITICAL` |
| Suboptimal but within acceptable bounds | O(N) where N is bounded | `MAJOR` |
| Micro-optimization, marginal gain | Constant factor improvement | `MINOR` |

## Debt Function Selection

- **`CONSTANT_ISSUE`** — most performance rules use this because each occurrence takes a fixed effort to fix (refactor one loop, add one batch call).
- **`LINEAR`** — use when multiple sites in the same file/class need the same fix (e.g., multiple unbounded collections in one service).

## Key Principles

- **Measure, don't guess** — descriptions should reference observable metrics (query count, allocation rate, latency percentiles), not subjective "slowness."
- **Context matters** — a pattern that's fine for 10 items is catastrophic for 10,000. Rules should articulate the scaling threshold where the pattern becomes problematic.
- **Prefer algorithmic fixes over micro-optimizations** — O(N) → O(1) trumps constant-factor improvements.
- **Consider the hot path** — flag patterns in code paths that execute frequently (request handlers, batch processors, event loops), not one-time startup code.
- **Resource exhaustion is a reliability issue** — memory leaks, connection leaks, and thread pool starvation can cause outages, making them `BUG` type candidates.
