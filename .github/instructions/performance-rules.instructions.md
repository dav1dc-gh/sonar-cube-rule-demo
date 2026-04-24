---
applyTo: "rules/performance/**/*.json"
description: "Authoring and review guidance for SonarQube performance rules (runtime, memory, I/O, DB)."
---

# Performance Rules — Custom Instructions

Scope: every JSON file under `rules/performance/`. These rules detect patterns that cause **runtime inefficiency** — wasted CPU, memory pressure, blocked threads, redundant I/O, or pathological database access.

> Read [sonarqube-rules.instructions.md](.github/instructions/sonarqube-rules.instructions.md) first for the shared schema. This file only documents what is **specific to performance rules**.

## 1. Mandatory field values

| Field | Required value for this category |
|---|---|
| `type` | `CODE_SMELL` for inefficiencies that produce correct (just slow) results — the common case. Use `BUG` only when the pattern can cause a functional failure under load (`memory-leaks` that OOM, `connection-pool-exhaustion` that throws, `unbounded-collection-growth` that crashes). |
| `severity` / `defaultSeverity` | `CRITICAL` for issues that scale super-linearly or fail under production load (`n-plus-one-query`, `memory-leaks`, `connection-pool-exhaustion`, `unbounded-collection-growth`, `synchronous-io-in-async`). `MAJOR` for everyday inefficiencies (`string-concatenation-in-loop`, `unnecessary-boxing`, `inefficient-loops`). `MINOR` only for micro-optimizations with negligible real-world impact. |
| `impacts` | Always include `{ "softwareQuality": "MAINTAINABILITY", "severity": "..." }` (matching how this repo models perf cost). Add `RELIABILITY: HIGH` when the pattern can crash or hang the process under load (memory leaks, pool exhaustion, sync I/O on event loops, unbounded growth). |
| `status` | `READY`. |
| `debt.function` | `CONSTANT_ISSUE` for site-local fixes (rewrite one loop, add one index, swap one collection). `LINEAR` only when remediation truly scales (e.g., refactoring many call sites that all leak). |
| `debt.offset` | `15min`–`1h`. N+1 fixes ≈ `30min`. Pool/leak fixes can be `1h`+ because they require profiling and load testing. |

## 2. Required tags

Every performance rule must include, in this order:

1. `"performance"` — the category tag.
2. A **resource** the rule protects: `"cpu"`, `"memory"`, `"io"`, `"network"`, `"database"`, `"gc"`, `"latency"`, `"throughput"`.
3. A **mechanism** when applicable: `"allocation"`, `"boxing"`, `"loop"`, `"regex"`, `"caching"`, `"lazy-init"`, `"connection-pool"`, `"async"`, `"orm"`, `"jdbc"`.
4. Optional **technology tags**: `"jpa"`, `"hibernate"`, `"spring"`, `"reactor"`, `"netty"`, `"jackson"`.

Do not add `"security"` unless the inefficiency itself is a DoS vector (e.g., `unoptimized-regex` → ReDoS, in which case also tag `"redos"`).

## 3. Description guidance

- One or two sentences. State **what pattern is detected**, **why it is slow**, and **the order-of-magnitude consequence** (e.g., "executes one query per row", "allocates a new String on every iteration", "blocks the event loop").
- Prefer concrete cost language ("O(n²)", "linear in input size", "per-request", "per-iteration") over vague claims ("very slow", "huge impact").
- Name the **specific anti-pattern** when there is one: N+1, ReDoS, autoboxing in a hot loop, busy-wait, eager initialization of unused resources.

Good: *"Detects potential N+1 query issues where database queries are executed inside loops, causing severe performance degradation."*

Bad: *"This rule helps make your code faster."*

## 4. `remediation.examples` rules

- Provide a **literal** before/after snippet whenever the fix is site-local (loop bodies, query patterns, regex, collection choice, boxing). Vague comments are acceptable only for genuinely structural problems (e.g., a sweeping connection-pool refactor).
- The `before` snippet must show the actual costly construct (the loop, the `findById` inside the iteration, the `+=` on `String`, the `Vector` use, the `new Pattern(...)` per call).
- The `after` snippet must show the **canonical optimization**:
  - N+1 → batched query / `JOIN FETCH` / `IN (...)` / DataLoader pattern.
  - String concat in loop → `StringBuilder` (Java) or equivalent buffer.
  - Inefficient collection → swap to the appropriate `ArrayList` / `HashMap` / `HashSet` / `ArrayDeque`.
  - Unnecessary boxing → use the primitive specialization (`int[]`, `IntStream`, `Long.parseLong` over `Long.valueOf`).
  - Excessive object creation → reuse, pool, or hoist allocations out of the loop.
  - Memory leak → null out references, use `WeakReference`/`WeakHashMap`, deregister listeners, close resources in `try-with-resources`.
  - Connection-pool exhaustion → ensure `try-with-resources` on `Connection`/`Statement`/`ResultSet`; tune pool size deliberately.
  - Sync I/O in async context → use the async/non-blocking variant (`WebClient` over `RestTemplate`, `CompletableFuture`, reactive APIs).
  - Unoptimized regex → precompile `Pattern`, anchor patterns, avoid catastrophic backtracking (replace nested quantifiers, use possessive quantifiers or atomic groups).
  - Missing lazy init → `Supplier<T>` / double-checked locking / `@Lazy`.
  - Unbounded growth → bounded cache (`Caffeine`, LRU), TTL, or eviction policy.
- Keep snippets ≤ 8 lines. Show the hot path, not the surrounding scaffolding.

## 5. `params` policy

Define `params` when the rule has a meaningful cutoff that varies by project:

- `loopThreshold` (INTEGER) — minimum loop body cost before the rule triggers.
- `regexComplexityThreshold` (INTEGER) — backtracking budget for ReDoS detection.
- `collectionSizeThreshold` (INTEGER) — when "unbounded growth" should trip.
- `maxAllocationsPerCall` (INTEGER) — for `excessive-object-creation`.

Do **not** parameterize fundamental correctness fixes (closing a `ResultSet`, fixing N+1) — there is no defensible knob.

## 6. Review checklist

Before approving any change under `rules/performance/`:

- [ ] `type` is `CODE_SMELL` (or `BUG` with explicit justification — load failure, not just slowness).
- [ ] Severity reflects scaling behavior: `CRITICAL` for super-linear/load-failing patterns, `MAJOR` otherwise.
- [ ] Impacts include `MAINTAINABILITY`; `RELIABILITY: HIGH` is added when load failures are realistic.
- [ ] Tags include `performance` + a resource tag + a mechanism tag.
- [ ] Description names the anti-pattern and the order-of-magnitude cost.
- [ ] Before/after example shows the literal hot path and the canonical optimization.
- [ ] `key` matches the filename and is kebab-case.
- [ ] Debt is `CONSTANT_ISSUE` for site-local fixes; `LINEAR` only when justified.

## 7. Anti-patterns to flag in review

- Severity `MINOR` on N+1, leaks, pool exhaustion, or unbounded growth — production-impacting; should be `CRITICAL`.
- After snippet that "uses parallel streams" as a generic fix — almost never the right answer; recommend the specific data-structure or query change.
- Recommending `String` `+=` over `StringBuilder` in a loop, or `Vector`/`Hashtable` over modern collections.
- Using `LINEAR` debt for a single-site fix (one query, one regex) — overcounts cost.
- Tagging a perf rule with `"security"` without an actual DoS vector.
- Missing `try-with-resources` in any `after` snippet that opens a JDBC/IO resource.
