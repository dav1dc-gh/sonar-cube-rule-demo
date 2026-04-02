---
description: "Use when creating, editing, or reviewing SonarQube performance rules in rules/performance/. Covers N+1 queries, memory leaks, connection pools, object creation, regex, boxing, collections, and async/IO patterns."
applyTo: "rules/performance/**"
---

# Performance Rules — Authoring Guidelines

## Category Overview

The `rules/performance/` directory contains **runtime efficiency rules** — rules that detect patterns causing degraded throughput, elevated latency, excessive memory consumption, or resource exhaustion. These rules focus on measurable runtime impact, not stylistic preferences.

Currently contains **12 rules** covering: database (N+1 queries, connection pool exhaustion), memory (memory leaks, excessive object creation, unbounded collection growth, unnecessary boxing), CPU (inefficient loops, string concatenation in loop, unoptimized regex), I/O (synchronous I/O in async contexts), and design (missing lazy initialization, inefficient collection usage).

## Mandatory Constraints

- **`type` is `CODE_SMELL` or `BUG`**:
  - Use `BUG` for issues that cause resource leaks or system failures (e.g., `memory-leaks` — unclosed resources will eventually crash the application).
  - Use `CODE_SMELL` for inefficiencies that degrade performance but don't cause failures (e.g., `n-plus-one-query`, `string-concatenation-in-loop`).
- **`severity` is typically `CRITICAL`** for high-impact problems (`n-plus-one-query`, `memory-leaks`, `connection-pool-exhaustion`). Use `MAJOR` for localized inefficiencies (`unnecessary-boxing`, `inefficient-loops`).
- **`tags` must include `"performance"`** as the first tag.
- **`severity` and `defaultSeverity` must match.**

## Impact Selection

Performance rules may impact multiple software qualities:

| softwareQuality | When to Use |
|-----------------|-------------|
| `RELIABILITY` | Resource leaks, connection exhaustion, OOM risks — issues that can cause outages |
| `MAINTAINABILITY` | Inefficient patterns that make scaling harder or require rework |

- Memory leaks, connection pool exhaustion, unbounded growth → `RELIABILITY` with `HIGH`
- N+1 queries, inefficient loops, missing lazy init → `MAINTAINABILITY` with `HIGH`
- Minor inefficiencies (boxing, regex) → `MAINTAINABILITY` with `MEDIUM`

## Tag Conventions

Always include these tags where applicable:

| Tag | When to Use |
|-----|-------------|
| `performance` | Every rule (required) |
| `database` | Database query issues (N+1, connection pools) |
| `orm` | ORM-specific patterns (lazy loading, fetch strategies) |
| `memory` | Memory allocation and GC issues |
| `resource-management` | Unclosed resources, pool management |
| `optimization` | General efficiency improvements |
| `concurrency` | Threading, async/await issues |
| `io` | I/O bound operations and blocking |

## Writing Descriptions

Performance rule descriptions must explain:
1. **What** inefficient pattern the rule detects
2. **Why** it degrades performance (quantify when possible — "causes N additional queries", "prevents garbage collection")
3. **At what scale** the problem manifests (loop iterations, connection count, request volume)

Example: *"Detects potential N+1 query issues where database queries are executed inside loops, causing severe performance degradation."*

## Remediation Examples

Performance remediation examples should:
- **`before`**: Show the inefficient pattern in a realistic context — include the loop, the allocation, or the blocking call.
- **`after`**: Show the optimized approach with a brief comment explaining the improvement (e.g., `// Single query with JOIN`, `// Automatically closed`).

Include framework-specific solutions when the rule relates to ORM or async patterns (JPA fetch joins, try-with-resources, CompletableFuture).

## Remediation Cost Guidelines

| Fix Type | Typical Cost |
|----------|-------------|
| Replace string concatenation with StringBuilder | `10min` |
| Add try-with-resources wrapping | `15min` |
| Switch collection type | `15min` |
| Refactor to lazy initialization | `15min` |
| Replace N+1 with batch/join query | `30min` |
| Add connection pool limits and monitoring | `30min` |
| Refactor blocking I/O to async | `1h` |
| Add eviction policy to unbounded collection | `30min` |

## Debt Model

Performance rules primarily use `CONSTANT_ISSUE` debt — most performance fixes have a predictable, fixed effort:

```json
"debt": {
  "function": "CONSTANT_ISSUE",
  "offset": "30min"
}
```

Use `LINEAR` only when the fix effort scales with the number of occurrences (e.g., replacing many string concatenations across a large method).

## Params

Performance rules **may have configurable params** when thresholds govern detection:

```json
"params": [
  {
    "key": "maxPoolSize",
    "name": "Maximum Pool Size",
    "description": "Maximum number of connections in the pool",
    "defaultValue": "10",
    "type": "INTEGER"
  }
]
```

Common params for performance rules:
- `maxPoolSize` — connection pool rules
- `maxIterations` — loop optimization thresholds
- `maxRegexLength` — regex complexity limits
- `maxCollectionSize` — unbounded growth limits

Most performance rules detect patterns rather than thresholds and do **not** need params.

## Distinguishing `BUG` vs `CODE_SMELL`

This is unique to the performance category — use this decision guide:

| Condition | Type |
|-----------|------|
| Can cause application crash, OOM, or data loss | `BUG` |
| Causes resource exhaustion over time | `BUG` |
| Degrades latency or throughput but app stays functional | `CODE_SMELL` |
| Wastes resources without risk of failure | `CODE_SMELL` |

Currently, only `memory-leaks` uses `BUG`. All other performance rules use `CODE_SMELL`.

## Checklist for New Performance Rules

1. `key` is lower-kebab-case and matches the filename
2. `type` is `CODE_SMELL` or `BUG` (see decision guide above)
3. `severity` is `CRITICAL` for high-impact issues, `MAJOR` for localized inefficiencies
4. `defaultSeverity` matches `severity`
5. `tags` includes `"performance"` first, plus relevant sub-tags (database, memory, optimization)
6. `impacts` targets `RELIABILITY` (resource leaks) or `MAINTAINABILITY` (inefficiency)
7. `description` explains the pattern, the performance impact, and the scale at which it manifests
8. `remediation.examples` includes framework-aware before/after pairs
9. `debt` uses `CONSTANT_ISSUE` (most cases)
10. `status` is `"READY"`
11. JSON is valid and well-formed
