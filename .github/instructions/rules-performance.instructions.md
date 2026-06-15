---
applyTo: "rules/performance/**"
---

# Performance Rules — Custom Instructions

You are assisting with SonarQube **performance** rule definitions in `rules/performance/`.

## Category Context

Performance rules detect runtime efficiency problems that degrade throughput, increase latency, exhaust resources, or waste compute. Unlike code smells (which affect humans reading code), performance issues affect the running system — causing slow responses, out-of-memory errors, connection pool exhaustion, or thread starvation under load. These rules require understanding of runtime behavior, concurrency, I/O patterns, and resource lifecycle.

## Constraints for This Category

- **`type` is either `CODE_SMELL` or `BUG`** — use `BUG` when the performance issue causes runtime failures (e.g., resource leaks leading to OOM, connection pool exhaustion causing timeouts). Use `CODE_SMELL` when it's an inefficiency that degrades performance without causing failures.
- **`severity` ranges from `CRITICAL` to `MAJOR`** — use `CRITICAL` for issues that cause production incidents under load (N+1 queries, memory leaks, thread pool starvation). Use `MAJOR` for inefficiencies that waste resources but don't cause outages.
- **`impacts[].softwareQuality`** — use `RELIABILITY` for resource exhaustion issues that can crash the system, or `MAINTAINABILITY` for inefficiencies that increase operational cost without causing failures.
- **`tags` MUST include `"performance"`** — additionally tag with:
  - `database` / `orm` — for query-related issues
  - `memory` — for allocation, GC, or leak issues
  - `concurrency` / `threading` — for thread pool or synchronization issues
  - `io` — for I/O blocking or inefficiency
  - `optimization` — general optimization opportunities
  - `resource-management` — for lifecycle/cleanup issues

## Writing Descriptions

Performance rule descriptions must articulate:
1. **What** the inefficient pattern is (e.g., "database queries executed inside a loop body")
2. **Why** it's harmful at runtime (e.g., "generates N+1 queries, scaling linearly with collection size")
3. **Observable symptoms** (e.g., "slow page loads, database connection saturation, increased P99 latency")
4. **Scale factor** — explain when/how the problem manifests (e.g., "unnoticeable with 10 records, catastrophic with 10,000")

Performance descriptions should quantify impact where possible — "causes O(n²) behavior" or "holds database connections for the full request lifecycle."

## Remediation Examples

For performance rules, remediation examples must:
- Show a **realistic inefficient pattern** with enough context to understand the runtime behavior
- Show the **optimized version** with clear explanation of why it's faster
- **Quantify the improvement** when possible (e.g., "reduces from N+1 queries to 2 queries")
- Include **framework-specific solutions** where applicable (e.g., JPA fetch joins, batch operations, connection pool settings)
- Show the **correct resource lifecycle** for resource management issues (try-with-resources, proper close/release)

## Remediation Cost Guidelines

| Fix Complexity | `constantCost` | Example |
|---|---|---|
| API swap | `15min` | Replace `String +` with `StringBuilder` in loop |
| Query optimization | `30min` | Add batch fetch, convert to JOIN |
| Resource lifecycle fix | `30min` | Add try-with-resources, proper close() |
| Caching/pooling | `1h` | Add connection pooling, memoization |
| Architecture change | `4h` | Convert synchronous I/O to async, add batch processing layer |

## Concurrency & Resource Management

Many performance rules involve concurrency and resource lifecycle. When writing these rules:
- Clearly distinguish between **correctness issues** (race conditions → `BUG`) and **efficiency issues** (thread pool sizing → `CODE_SMELL`)
- Specify the **resource type** being mismanaged (connections, threads, file handles, memory)
- Document the **failure mode** (what happens when the resource is exhausted)
- Include **diagnostic hints** in the description (e.g., "monitor connection pool active/idle counts")

## Configurable Thresholds (`params`)

Performance rules may benefit from `params` for:
- **Batch sizes** — `batchSize` for batch operation recommendations
- **Pool sizes** — `maxPoolSize`, `minIdle` for resource pool rules
- **Timeouts** — `maxWaitTime` for blocking operations
- **Loop iteration limits** — thresholds for when loop-based issues become problematic

## Common Tags for Performance Rules

`performance`, `database`, `orm`, `memory`, `concurrency`, `threading`, `io`, `optimization`, `resource-management`, `caching`, `allocation`, `gc`, `blocking`, `latency`, `throughput`, `scalability`

## When Creating New Performance Rules

1. Check the existing 18 rules for overlap — performance issues often have overlapping symptoms.
2. Determine if the issue is a `BUG` (causes failures) or `CODE_SMELL` (causes slowness).
3. Consider the **load dependency** — document whether the issue manifests at low load or only under stress.
4. Include measurable criteria — avoid rules that can't be objectively triggered.
5. Consider language/framework specificity — some performance patterns are JVM-specific, others are universal.
6. Verify the rule isn't better classified as `security` (e.g., uncontrolled resource consumption as DoS vector).

## Quality Checklist

- [ ] `type` is `CODE_SMELL` (inefficiency) or `BUG` (causes runtime failures)
- [ ] `severity` is `CRITICAL` (production incidents) or `MAJOR` (waste without failure)
- [ ] `impacts` correctly reflects reliability vs. maintainability impact
- [ ] `tags` includes `"performance"` plus at least one specific concern tag
- [ ] Description quantifies or explains scaling behavior
- [ ] Description documents observable symptoms
- [ ] Remediation example shows measurable improvement
- [ ] Resource lifecycle issues include proper cleanup pattern
- [ ] Filename matches `key` field in lower-kebab-case
