---
applyTo: "rules/performance/**"
---

# Performance Rules — Custom Instructions

You are assisting with **performance anti-pattern detection rules** in the `rules/performance/` directory. These rules identify patterns that cause unnecessary resource consumption, latency, memory pressure, or scalability bottlenecks.

---

## Category Conventions

### Type — BUG vs CODE_SMELL Decision

Performance rules uniquely split across two types. The distinction is critical:

| Type | When to Use | Rationale | Examples |
|---|---|---|---|
| **`BUG`** | The pattern causes observable failures under load — resource exhaustion, OOM errors, crashes, hangs | These are defects that will break the application given enough traffic or time | connection-pool-exhaustion, memory-leaks, unbounded-collection-growth, unoptimized-regex |
| **`CODE_SMELL`** | The pattern wastes resources or adds latency but doesn't cause failures | These are inefficiencies that degrade performance without breaking correctness | excessive-object-creation, inefficient-collection-usage, inefficient-loops, missing-lazy-initialization, n-plus-one-query, string-concatenation-in-loop, synchronous-io-in-async, unnecessary-boxing |

**Decision rule**: Ask "Can this pattern cause the application to crash, hang, or run out of resources?" If yes → `BUG`. If it just makes things slower → `CODE_SMELL`.

### Severity

Performance rules use a three-tier severity model:

| Severity | When to Use | Examples |
|---|---|---|
| **CRITICAL** | Resource exhaustion, crashes, or denial-of-service risk under production load | connection-pool-exhaustion, memory-leaks, unbounded-collection-growth, unoptimized-regex (ReDoS) |
| **MAJOR** | Significant performance degradation affecting user experience or scalability | excessive-object-creation, inefficient-loops, missing-lazy-initialization, n-plus-one-query, string-concatenation-in-loop, synchronous-io-in-async |
| **MINOR** | Low-impact inefficiencies, micro-optimizations | inefficient-collection-usage, unnecessary-boxing |

BLOCKER and INFO are **not used** for performance rules.

### Impact

Performance rules map to two software qualities:

| Impact Quality | When to Use | Impact Severity | Examples |
|---|---|---|---|
| **RELIABILITY** | Patterns that can cause failures, data loss, or service outages | HIGH for resource exhaustion (connection-pool, memory-leaks, unbounded-collection, unoptimized-regex); MEDIUM for potential instability (excessive-object-creation, missing-lazy-initialization) | 7/12 rules |
| **MAINTAINABILITY** | Inefficient patterns that make code harder to optimize or reason about | HIGH for systemic issues (n-plus-one-query); MEDIUM for moderate inefficiencies (inefficient-loops, string-concatenation, synchronous-io); LOW for minor style issues (inefficient-collection-usage) | 5/12 rules |

**Guideline**: If the type is `BUG`, the impact quality should be `RELIABILITY` with `HIGH` severity. For `CODE_SMELL` rules, choose based on whether the primary concern is reliability risk or code quality.

### Debt Model

- **Always use `CONSTANT_ISSUE`**. All 12 existing performance rules use this model.
- Performance fixes are typically discrete: swap an API, add a `try-with-resources`, move an allocation outside a loop. Fix time doesn't scale with the number of occurrences.
- **Typical offsets**: 5min–45min:
  - 5–10min: Simple swaps (StringBuilder instead of `+`, initial capacity hint, autoboxing removal)
  - 15–20min: Restructuring loops, adding resource management, lazy initialization
  - 30–45min: Architectural fixes (N+1 query resolution, async refactoring, connection pool configuration)

### Parameters

- Performance rules **do not** use configurable `params`. Performance anti-patterns are pattern-based detections, not threshold-based measurements.
- If you find yourself wanting a threshold (e.g., "max allocations per method"), consider whether the rule belongs in `code-smells/` instead.

### Tags

Always include:
- `"performance"` — mandatory for every performance rule

Add domain-specific tags from these established conventions:
- Resource types: `database`, `memory`, `memory-leak`, `gc`, `resource-leak`, `connection-pool`, `cache`
- Code patterns: `loops`, `strings`, `collections`, `data-structures`, `primitives`, `regex`, `initialization`, `optimization`
- Architecture: `async`, `reactive`, `concurrency`, `orm`
- Cross-cutting: `security` (when the pattern also has security implications, e.g., ReDoS)

### Code Examples

- **Language**: Always Java.
- **Before**: Show the anti-pattern in a realistic context — a database query in a loop, a string concatenation in a hot path, an unclosed resource. Include a comment naming the anti-pattern.
- **After**: Show the optimized version using the correct Java idiom (PreparedStatement with batch, StringBuilder, try-with-resources, `List.of()`, etc.).
- For database-related rules, show the ORM/JDBC pattern, not raw SQL strings.
- For async rules, show the blocking vs non-blocking equivalent.

---

## Existing Rules Reference

The following 12 rules exist in `rules/performance/`:

| File | Key | Severity | Type | Impact | Detects |
|---|---|---|---|---|---|
| `connection-pool-exhaustion.json` | connection-pool-exhaustion | CRITICAL | BUG | RELIABILITY/HIGH | Connections not returned to pool |
| `excessive-object-creation.json` | excessive-object-creation | MAJOR | CODE_SMELL | RELIABILITY/MEDIUM | Unnecessary allocations in hot paths |
| `inefficient-collection-usage.json` | inefficient-collection-usage | MINOR | CODE_SMELL | MAINTAINABILITY/LOW | Wrong collection type, missing capacity hints |
| `inefficient-loops.json` | inefficient-loops | MAJOR | CODE_SMELL | MAINTAINABILITY/MEDIUM | Avoidable work inside loops |
| `memory-leaks.json` | memory-leaks | CRITICAL | BUG | RELIABILITY/HIGH | Unclosed resources, listener accumulation |
| `missing-lazy-initialization.json` | missing-lazy-initialization | MAJOR | CODE_SMELL | RELIABILITY/MEDIUM | Eager init of expensive, conditionally-used resources |
| `n-plus-one-query.json` | n-plus-one-query | CRITICAL | CODE_SMELL | MAINTAINABILITY/HIGH | DB queries executed inside loops |
| `string-concatenation-in-loop.json` | string-concatenation-in-loop | MAJOR | CODE_SMELL | MAINTAINABILITY/MEDIUM | String `+` operator inside loops |
| `synchronous-io-in-async.json` | synchronous-io-in-async | MAJOR | CODE_SMELL | MAINTAINABILITY/MEDIUM | Blocking I/O in async methods |
| `unbounded-collection-growth.json` | unbounded-collection-growth | CRITICAL | BUG | RELIABILITY/HIGH | Collections growing without eviction |
| `unnecessary-boxing.json` | unnecessary-boxing | MINOR | CODE_SMELL | MAINTAINABILITY/LOW | Needless primitive ↔ wrapper conversions |
| `unoptimized-regex.json` | unoptimized-regex | CRITICAL | BUG | RELIABILITY/HIGH | ReDoS-susceptible or repeatedly compiled regex |

---

## Creating a New Performance Rule

1. **Classify BUG vs CODE_SMELL first**: Can the pattern crash/hang/exhaust resources? → BUG. Just slow? → CODE_SMELL.
2. **Verify no overlap** with the 12 existing rules. Performance rules can be subtle — an "inefficient loop" might overlap with "N+1 query" if the loop contains DB calls.
3. **Measure real impact**: Performance rules should target patterns with measurable overhead, not micro-optimizations that JIT compilers handle. Focus on I/O, memory, resource lifecycle, and algorithmic inefficiency.
4. **Consider the production context**: A pattern that's fine in a CLI tool might be catastrophic in a high-throughput server. Describe the risk in production terms.
5. **Tag with resource domain**: Always indicate what resource is affected (memory, database, network, CPU, etc.).

### Template (BUG — Resource Exhaustion)

```json
{
  "key": "new-performance-bug",
  "name": "New Performance Bug Name",
  "description": "Detects <pattern> which causes <resource> exhaustion under load, leading to <failure mode>.",
  "severity": "CRITICAL",
  "type": "BUG",
  "tags": ["performance", "resource-leak", "<domain-tag>"],
  "remediation": {
    "constantCost": "30min",
    "examples": [
      {
        "before": "// Anti-pattern: <resource> not properly managed\n<vulnerable Java code>",
        "after": "// Fixed: <resource> properly managed with <technique>\n<safe Java code>"
      }
    ]
  },
  "impacts": [
    {
      "softwareQuality": "RELIABILITY",
      "severity": "HIGH"
    }
  ],
  "defaultSeverity": "CRITICAL",
  "status": "READY",
  "debt": {
    "function": "CONSTANT_ISSUE",
    "offset": "30min"
  }
}
```

### Template (CODE_SMELL — Inefficiency)

```json
{
  "key": "new-performance-smell",
  "name": "New Performance Smell Name",
  "description": "Detects <pattern> which causes unnecessary <resource consumption|latency> in <context>.",
  "severity": "MAJOR",
  "type": "CODE_SMELL",
  "tags": ["performance", "optimization", "<domain-tag>"],
  "remediation": {
    "constantCost": "15min",
    "examples": [
      {
        "before": "// Inefficient: <explain the waste>\n<slow Java code>",
        "after": "// Optimized: <explain the improvement>\n<fast Java code>"
      }
    ]
  },
  "impacts": [
    {
      "softwareQuality": "MAINTAINABILITY",
      "severity": "MEDIUM"
    }
  ],
  "defaultSeverity": "MAJOR",
  "status": "READY",
  "debt": {
    "function": "CONSTANT_ISSUE",
    "offset": "15min"
  }
}
```

---

## Common Mistakes to Avoid

- **Don't use `VULNERABILITY`** — even if a performance issue has security implications (e.g., ReDoS), the primary type is `BUG`, not `VULNERABILITY`. Add a `"security"` tag instead.
- **Don't add `params`** — performance rules detect patterns, not threshold violations. If you need a configurable threshold, the rule probably belongs in `code-smells/`.
- **Don't use `LINEAR` debt** — all performance rules use CONSTANT_ISSUE. The fix is a discrete code change, not something that scales.
- **Don't conflate BUG and CODE_SMELL** — the distinction matters for SonarQube quality gates. Resource exhaustion = BUG; inefficiency = CODE_SMELL.
- **Don't target JIT-optimizable patterns** — focus on I/O, resource lifecycle, and algorithmic issues the JVM can't optimize away.
- **Don't forget to match `severity` and `defaultSeverity`**.
