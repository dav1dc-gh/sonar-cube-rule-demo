---
name: fix-data-quality
description: "Fix data quality issues in SonarQube rule JSON files. Use when: fixing wrong impact classifications, correcting malformed debt objects, resolving duplicate rules, syncing severity with defaultSeverity, adding missing required fields, or repairing broken JSON structure."
---

# Fix Data Quality

## Keywords

fix, repair, data quality, impact classification, MAINTAINABILITY, RELIABILITY, SECURITY, softwareQuality, debt, offset, coefficient, LINEAR, CONSTANT_ISSUE, malformed, duplicate, overlap, merge, severity, defaultSeverity, sync, missing field, broken JSON, inconsistency

## When to Use

- Fixing impact classification mismatches (e.g., performance rules with `MAINTAINABILITY` instead of `RELIABILITY`)
- Correcting malformed `debt` objects (missing `offset`, wrong `function` type)
- Resolving duplicate or overlapping rules across categories
- Syncing `severity` and `defaultSeverity` when they diverge
- Adding missing required fields or fixing enum values
- Any bulk repair operation across multiple rule files

## Impact Classification Guide

Correct `softwareQuality` by what the rule actually detects:

| Rule Category | Primary Impact | When to Use Alternative |
|---------------|---------------|------------------------|
| `security/` | `SECURITY` | Always `SECURITY` — no exceptions |
| `code-smells/` | `MAINTAINABILITY` | `RELIABILITY` if the smell can cause runtime errors (e.g., `empty-catch-block`) |
| `performance/` | `RELIABILITY` | `MAINTAINABILITY` only if the issue is purely about code readability, not runtime behavior |
| `maintainability/` | `MAINTAINABILITY` | `RELIABILITY` for null-safety rules (`missing-null-check`) |

### Performance Rules — Common Misclassification

Performance rules that affect **runtime behavior** (latency, throughput, resource usage) must use `RELIABILITY`, not `MAINTAINABILITY`. The code runs but performs poorly — that's a reliability concern.

Rules that should be `RELIABILITY`:
- `n-plus-one-query` — causes database performance degradation at runtime
- `string-concatenation-in-loop` — causes excessive garbage collection at runtime
- `synchronous-io-in-async` — causes thread pool exhaustion at runtime
- `connection-pool-exhaustion` — causes connection failures at runtime
- `memory-leaks` — causes out-of-memory errors at runtime
- `unbounded-collection-growth` — causes memory exhaustion at runtime

## Debt Object Repair

### CONSTANT_ISSUE — Required Fields
```json
{
  "function": "CONSTANT_ISSUE",
  "offset": "30min"        // REQUIRED — the fixed cost
}
```

### LINEAR — Required Fields
```json
{
  "function": "LINEAR",
  "coefficient": "10min",  // REQUIRED — cost per unit
  "offset": "0min"         // REQUIRED — base cost (use "0min" if none)
}
```

**Common error**: LINEAR debt missing `offset`. Always include `"offset": "0min"` even when the base cost is zero.

## Duplicate Rule Resolution

When two rules across categories detect the same issue:

### Decision Process

1. **Compare descriptions** — are they detecting the same pattern?
2. **Compare severities** — is one more strict?
3. **Compare params** — do they have different thresholds?
4. **Decide**: merge (keep one, remove other) or differentiate (clarify distinct scopes)

### If Merging

1. Keep the rule in the category that best fits its **primary concern**
2. Remove the duplicate file
3. Update README.md rule tables and counts
4. Update `.github/copilot-instructions.md` if it lists the removed rule
5. Log the change in AI-HISTORY.md

### If Differentiating

1. Update both descriptions to clearly state their distinct focus
2. Add cross-reference tags (e.g., `"see-also-too-many-parameters"`)
3. Ensure severity and thresholds reflect the different scopes

## Known Issues (as of 2026-04-02)

These are documented data quality issues. When fixing, check if they are still present:

| File | Issue | Fix |
|------|-------|-----|
| `rules/maintainability/shotgun-surgery.json` | LINEAR debt missing `offset` | Add `"offset": "0min"` |
| `rules/performance/n-plus-one-query.json` | Impact is `MAINTAINABILITY` | Change to `RELIABILITY` |
| `rules/performance/string-concatenation-in-loop.json` | Impact is `MAINTAINABILITY` | Change to `RELIABILITY` |
| `rules/performance/synchronous-io-in-async.json` | Impact is `MAINTAINABILITY` | Change to `RELIABILITY` |
| `rules/code-smells/long-parameter-list.json` + `rules/maintainability/too-many-parameters.json` | Duplicate detection | Merge or differentiate |

## Procedure

1. Read the target rule file(s)
2. Identify the specific issue from the categories above
3. Apply the fix following the guide
4. Validate the fixed file (valid JSON, correct enum values, complete objects)
5. Run validation if the validate-rules skill/script is available
6. Update AI-HISTORY.md with what was fixed and why
