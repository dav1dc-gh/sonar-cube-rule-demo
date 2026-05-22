---
applyTo: rules/performance/**
---

# Performance Rules — Custom Instructions

You are assisting with SonarQube **performance** rule definitions in `rules/performance/`.

## Category Context

These rules detect runtime efficiency problems — excessive resource consumption, unnecessary allocations, suboptimal algorithms, and patterns that degrade throughput or latency under load.

## Key Constraints

- **`type`** is typically `"CODE_SMELL"` for inefficiency patterns, or `"BUG"` for performance issues that cause outages (e.g., memory leaks, resource exhaustion).
- **`severity`** should be `CRITICAL` for production-impacting issues (N+1 queries, memory leaks, thread starvation), `MAJOR` for measurable inefficiencies, `MINOR` for micro-optimizations.
- **`impacts[].softwareQuality`** should be `"RELIABILITY"` for issues causing outages/crashes, or `"MAINTAINABILITY"` for inefficiency patterns. Performance itself maps to reliability in SonarQube's model.
- **Tags**: Always include `"performance"`. Add specific tags like `"memory"`, `"cpu"`, `"database"`, `"concurrency"`, `"io"`, `"collections"` as appropriate.

## Description Guidelines

- Explain the **performance characteristic** — what resource is wasted or what bottleneck is created?
- Quantify impact when possible (e.g., "O(n²) instead of O(n)", "one query per loop iteration").
- Describe the **conditions** under which the problem manifests (high load, large datasets, concurrent access).

## Remediation Examples

- The `before` example should show code that performs poorly under realistic conditions.
- The `after` example should show the optimized version with clear performance improvement.
- Include comments indicating the performance difference when helpful.

## Remediation Cost

- Simple fixes (use StringBuilder, close resource): `"15min"` to `"30min"`
- Algorithmic changes (batch queries, add caching, fix collection type): `"1h"` to `"2h"`
- Architectural changes (connection pooling, async redesign): `"2h"` to `"4h"`

## Parameters

- Performance rules often benefit from configurable thresholds: max collection size, batch size limits, timeout values.
- Default values should reflect production-realistic scenarios.

## Naming

- Keys should describe the performance anti-pattern: `n-plus-one-query`, `memory-leaks`, `string-concatenation-in-loop`.
- Be specific about the mechanism, not just the symptom.
