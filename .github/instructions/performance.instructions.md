---
applyTo: "rules/performance/**"
---

# Performance Rules — Path-Specific Custom Instructions

You are working inside `rules/performance/`, which contains **12 SonarQube rule definitions** that detect patterns wasting CPU, memory, I/O, or database resources. These rules focus on runtime efficiency and resource management.

---

## Purpose of This Category

Performance rules identify code that runs correctly but inefficiently — causing slow response times, excessive garbage collection, memory exhaustion, connection pool starvation, or database overload. Unlike code smells (which are about design quality), performance rules directly address measurable runtime characteristics. Fixing these yields tangible improvements in throughput, latency, and resource utilization.

---

## Current Rules Inventory (12 rules)

| File | Key | Type | Severity | What It Detects |
|---|---|---|---|---|
| `connection-pool-exhaustion.json` | `connection-pool-exhaustion` | BUG | CRITICAL | DB/HTTP connections not closed or returned to pool |
| `excessive-object-creation.json` | `excessive-object-creation` | CODE_SMELL | MAJOR | Unnecessary allocations in hot paths (loops, high-traffic methods) |
| `inefficient-collection-usage.json` | `inefficient-collection-usage` | CODE_SMELL | MINOR | Wrong collection type or missing initial capacity hints |
| `inefficient-loops.json` | `inefficient-loops` | CODE_SMELL | MAJOR | Invariant computations or repeated method calls inside loops |
| `memory-leaks.json` | `memory-leaks` | BUG | CRITICAL | Unclosed resources, listener accumulation, retained references |
| `missing-lazy-initialization.json` | `missing-lazy-initialization` | CODE_SMELL | MAJOR | Eager initialization of expensive, possibly unused resources |
| `n-plus-one-query.json` | `n-plus-one-query` | CODE_SMELL | CRITICAL | Database queries executed inside loops (N+1 problem) |
| `string-concatenation-in-loop.json` | `string-concatenation-in-loop` | CODE_SMELL | MAJOR | String `+` operator inside loops instead of StringBuilder |
| `synchronous-io-in-async.json` | `synchronous-io-in-async` | CODE_SMELL | MAJOR | Blocking I/O calls inside async methods or reactive streams |
| `unbounded-collection-growth.json` | `unbounded-collection-growth` | BUG | CRITICAL | Collections/caches growing without eviction policies |
| `unnecessary-boxing.json` | `unnecessary-boxing` | CODE_SMELL | MINOR | Needless primitive ↔ wrapper conversions in hot paths |
| `unoptimized-regex.json` | `unoptimized-regex` | BUG | CRITICAL | Regex compiled per-call instead of cached, or patterns vulnerable to ReDoS |

---

## Category-Specific Conventions

### Type — Mixed: `BUG` and `CODE_SMELL`

This is the **only category that uses both `BUG` and `CODE_SMELL` types**. The distinction matters:

- **`BUG`** (4 rules): For issues that will cause runtime failures under load — connection pool exhaustion, memory leaks, unbounded growth, ReDoS. These aren't design preferences; they're defects that _will_ manifest in production.
- **`CODE_SMELL`** (8 rules): For inefficiencies that degrade performance but don't cause outright failures — suboptimal loops, wrong collection types, unnecessary boxing, blocking in async.

**Guideline**: Use `BUG` when the pattern will eventually cause a crash, hang, or DoS. Use `CODE_SMELL` when it merely wastes resources.

### Severity Patterns

- `CRITICAL` for all `BUG`-type rules and for `n-plus-one-query` (which can cause database meltdown).
- `MAJOR` for most `CODE_SMELL`-type rules (loops, strings, objects, init, async).
- `MINOR` for low-impact optimizations (`inefficient-collection-usage`, `unnecessary-boxing`).

### Impacts

The `softwareQuality` field is mixed in this category:
- `"RELIABILITY"` for rules where the issue can cause failures: `connection-pool-exhaustion`, `memory-leaks`, `excessive-object-creation`, `missing-lazy-initialization`, `unbounded-collection-growth`, `unoptimized-regex`.
- `"MAINTAINABILITY"` for rules that are primarily about code quality with performance implications: `inefficient-collection-usage`, `inefficient-loops`, `n-plus-one-query`, `string-concatenation-in-loop`, `synchronous-io-in-async`, `unnecessary-boxing`.

**Guideline**: Use `"RELIABILITY"` when the issue threatens application stability. Use `"MAINTAINABILITY"` when the issue is about suboptimal coding patterns.

### Tags

- Always include `"performance"` as the first tag.
- Add resource-specific tags: `"memory"`, `"database"`, `"strings"`, `"collections"`, `"regex"`, `"async"`, `"concurrency"`.
- Add concern tags: `"optimization"`, `"resource-management"`, `"resource-leak"`, `"gc"`, `"connection-pool"`, `"cache"`.
- Include `"security"` as an additional tag if the performance issue has security implications (e.g., ReDoS in `unoptimized-regex`).

### Debt Model

- All 12 performance rules use `"function": "CONSTANT_ISSUE"` — each occurrence takes a fixed time to fix.
- `offset` ranges from `"5min"` (simple type swaps like unboxing) to `"45min"` (implementing cache eviction policies or refactoring connection management).
- **No `LINEAR` debt**: Performance fixes are typically localized refactors, not proportional to a measurable quantity.

### No Configurable Parameters

None of the current performance rules have `params`. Performance anti-patterns are generally binary (the pattern is present or it isn't) rather than threshold-based. Only add `params` to a new rule if there's a clear, adjustable numeric threshold (e.g., "maximum loop iterations before warning").

### Remediation Examples

- Performance examples must show the **slow/dangerous pattern** in `before` and the **efficient alternative** in `after`.
- Use Java examples for consistency with the existing rules, often involving loops, streams, database queries, or resource management.
- The `after` example should demonstrate idiomatic Java patterns: try-with-resources, StringBuilder, pre-sized collections, cached regex patterns, lazy initialization, ORM fetch strategies.
- For database rules, show the SQL/ORM-level fix (JOINs, fetch graphs) rather than just application-level workarounds.

---

## Guidelines for Creating New Performance Rules

1. **Ensure it's about runtime performance**: If the primary concern is code readability or design structure, it belongs in `code-smells/` or `maintainability/`.
2. **Decide `BUG` vs `CODE_SMELL` carefully**: Will this cause a crash/hang/OOM under production load? → `BUG`. Is it merely slower than it should be? → `CODE_SMELL`.
3. **Quantify the impact in the description**: Use phrases like "causes N+1 database queries", "creates O(n) garbage objects per iteration", "exhausts the connection pool under concurrent requests".
4. **Show measurable improvements in remediation**: Where possible, describe the performance difference (e.g., "reduces N+1 queries to a single JOIN", "eliminates per-iteration String allocations").
5. **Consider both single-threaded and concurrent scenarios**: Some issues only manifest under load (connection pool exhaustion) or in async contexts (blocking I/O in reactive streams).
6. **Tag with `"security"` when applicable**: Performance issues can be security issues (ReDoS, resource exhaustion attacks).

---

## Common Pitfalls to Avoid

- **Don't use `"type": "VULNERABILITY"`** — performance issues are not security vulnerabilities (even ReDoS is typed as `BUG`, not `VULNERABILITY`).
- **Don't confuse this category with code-smells**: If the issue is about OOP design (Feature Envy, God Class) rather than runtime efficiency, it belongs elsewhere.
- **Don't set all rules to CRITICAL** — reserve CRITICAL for issues that threaten application stability or availability.
- **Don't provide `after` examples that trade readability for micro-optimization** — the fix should be both faster _and_ idiomatic.
- **Don't forget resource cleanup** — when showing `after` examples involving resources (connections, streams, files), always use try-with-resources or explicit close patterns.
