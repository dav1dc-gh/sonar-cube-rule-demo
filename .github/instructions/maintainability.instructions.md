---
applyTo: "rules/maintainability/**"
---

# Maintainability Rules — Custom Instructions

You are assisting with **maintainability rules** in the `rules/maintainability/` directory. These rules detect patterns that make code harder to read, understand, change, and maintain over time — focusing on clarity, structure, documentation, and coupling.

---

## Category Conventions

### Type

- **Primary type**: `"CODE_SMELL"` (11/12 rules). Maintainability issues are quality concerns about how code is structured, not functional defects.
- **Exception**: `missing-null-check` uses `"BUG"` because a missing null check can cause a `NullPointerException` at runtime — a correctness defect, not just a quality issue.

**Decision rule**: If the pattern can cause a runtime exception or incorrect behavior, use `BUG`. If it only makes code harder to read, change, or test, use `CODE_SMELL`.

### Severity

Maintainability rules use a two-tier model:

| Severity | When to Use | Examples |
|---|---|---|
| **MAJOR** | Patterns that significantly impede development velocity — hard to understand, risky to change, or architecturally problematic | circular-dependencies, deep-nesting, hidden-dependencies, long-methods, missing-null-check, shotgun-surgery, too-many-parameters |
| **MINOR** | Lower-impact quality issues that reduce clarity but don't block productive work | boolean-blindness, excessive-comments, hardcoded-urls, inconsistent-naming, missing-javadoc |

BLOCKER, CRITICAL, and INFO are **not used** for maintainability rules.

### Impact

- **Primary quality**: `"MAINTAINABILITY"` (10/12 rules). This is the default — maintainability rules exist to improve long-term code health.
- **Exception**: `missing-null-check` uses `"RELIABILITY"` because the primary concern is preventing runtime crashes.

Impact severity tiers:

| Impact Severity | When to Use | Examples |
|---|---|---|
| **HIGH** | Architectural or cross-cutting issues requiring significant effort to resolve | circular-dependencies, shotgun-surgery |
| **MEDIUM** | Localized but significant issues requiring moderate refactoring | deep-nesting, hidden-dependencies, long-methods, missing-null-check, too-many-parameters |
| **LOW** | Surface-level issues fixable with simple edits | boolean-blindness, excessive-comments, hardcoded-urls, inconsistent-naming, missing-javadoc |

### Debt Model

Maintainability rules use two debt models:

- **`CONSTANT_ISSUE`** (10/12 rules): Default. Use when every occurrence takes roughly the same time to fix.
- **`LINEAR`** (2/12 rules): Use when fix time scales with a measurable dimension of the problem.
  - `long-methods`: coefficient `"2min"` per excess line — longer methods take proportionally more time to decompose.
  - `shotgun-surgery`: coefficient `"20min"` per affected class — more scattered changes mean more refactoring.

**When to choose LINEAR**: If the rule measures something quantitative (line count, number of affected files, nesting depth) and remediation time scales proportionally, use LINEAR. Otherwise, default to CONSTANT_ISSUE.

**Typical offsets**: 5min–60min:
- 5–10min: Renames, adding a null check, extracting a constant (inconsistent-naming, missing-null-check, hardcoded-urls)
- 15–20min: Adding documentation, restructuring parameters (missing-javadoc, boolean-blindness, too-many-parameters)
- 25–30min: Reducing nesting, extracting methods (deep-nesting, long-methods)
- 45–60min: Architectural refactoring (circular-dependencies, shotgun-surgery, hidden-dependencies)

### Parameters

Maintainability rules frequently use `params` for configurable thresholds (4/12 rules). This category has the highest threshold diversity because "too much" depends heavily on team conventions.

**Current parameterized rules:**
| Rule | Param Key | Default | What It Controls |
|---|---|---|---|
| boolean-blindness | `maxBooleanParams` | 2 | Max boolean parameters before the rule triggers |
| deep-nesting | `maxDepth` | 4 | Max nesting depth (if/for/while/try) |
| long-methods | `max` | 100 | Max lines per method |
| too-many-parameters | `max` | 7 | Max parameters per method |

**When to add params:**
- The rule compares a measurable quantity against a configurable limit.
- Teams reasonably disagree on the right threshold (one team's acceptable method length may be another's violation).
- Param type is almost always `INTEGER`. Use short, descriptive `camelCase` keys (`max`, `maxDepth`, `maxBooleanParams`).

**When NOT to add params:**
- The rule detects a structural pattern rather than a measurement (e.g., circular-dependencies, shotgun-surgery).
- A threshold would make the rule meaningless (e.g., "max number of hardcoded URLs" — one is too many).

### Tags

Always include:
- `"maintainability"` — mandatory for every maintainability rule

Add contextual tags from these established conventions:
- Quality concerns: `readability`, `complexity`, `clean-code`, `best-practices`
- Design aspects: `design`, `architecture`, `coupling`, `cohesion`, `refactoring`
- Specific domains: `documentation`, `javadoc`, `naming`, `conventions`, `null-safety`, `defensive-programming`, `configuration`, `deployment`
- Related concerns: `reliability`, `testability`, `dependency-injection`, `method-length`, `parameters`, `api-design`, `yagni`

### Code Examples

- **Language**: Always Java.
- **Before**: Show the maintainability problem in realistic code. Include a comment identifying the issue (e.g., `// Bad: 6 levels of nesting`).
- **After**: Show the improved version using standard refactoring techniques (extract method, introduce parameter object, guard clauses, dependency injection, etc.).
- For documentation rules (missing-javadoc), show the public API before and after adding proper Javadoc.
- For naming rules, show inconsistent naming and the corrected version following Java conventions.
- For architectural rules (circular-dependencies, shotgun-surgery), show simplified class diagrams or multi-class examples when necessary.

---

## Existing Rules Reference

The following 12 rules exist in `rules/maintainability/`:

| File | Key | Severity | Type | Impact | Params? | Detects |
|---|---|---|---|---|---|---|
| `boolean-blindness.json` | boolean-blindness | MINOR | CODE_SMELL | MAINT/LOW | Yes (maxBooleanParams) | Multiple boolean params obscuring call-site meaning |
| `circular-dependencies.json` | circular-dependencies | MAJOR | CODE_SMELL | MAINT/HIGH | No | Circular package/module/class dependencies |
| `deep-nesting.json` | deep-nesting | MAJOR | CODE_SMELL | MAINT/MEDIUM | Yes (maxDepth) | Excessive if/for/while/try nesting levels |
| `excessive-comments.json` | excessive-comments | MINOR | CODE_SMELL | MAINT/LOW | No | Redundant comments explaining *what* not *why* |
| `hardcoded-urls.json` | hardcoded-urls | MINOR | CODE_SMELL | MAINT/LOW | No | URLs/endpoints that should be in configuration |
| `hidden-dependencies.json` | hidden-dependencies | MAJOR | CODE_SMELL | MAINT/MEDIUM | No | Dependencies not explicit in method signatures |
| `inconsistent-naming.json` | inconsistent-naming | MINOR | CODE_SMELL | MAINT/LOW | No | Variables/methods not following naming conventions |
| `long-methods.json` | long-methods | MAJOR | CODE_SMELL | MAINT/MEDIUM | Yes (max) | Methods exceeding line count threshold |
| `missing-javadoc.json` | missing-javadoc | MINOR | CODE_SMELL | MAINT/LOW | No | Public APIs without documentation comments |
| `missing-null-check.json` | missing-null-check | MAJOR | BUG | RELIAB/MEDIUM | No | Potential null pointer dereferences |
| `shotgun-surgery.json` | shotgun-surgery | MAJOR | CODE_SMELL | MAINT/HIGH | No | Changes requiring many small edits across classes |
| `too-many-parameters.json` | too-many-parameters | MAJOR | CODE_SMELL | MAINT/MEDIUM | Yes (max) | Methods with excessive parameter counts |

---

## Creating a New Maintainability Rule

1. **Verify no overlap** with the 12 existing rules and with `rules/code-smells/`. The boundary between code smells and maintainability can be subtle:
   - **Code smells** focus on *design patterns* and *structural anti-patterns* (God Class, Feature Envy, Refused Bequest).
   - **Maintainability** focuses on *readability, clarity, coupling, and documentation* (naming, nesting, parameter lists, Javadoc).
   - If the rule is primarily about a well-known OOP design anti-pattern, it likely belongs in `code-smells/`.
   - If the rule is about how easy the code is to read, navigate, or safely modify, it belongs here.

2. **Determine if a threshold makes sense**: If different teams would reasonably set different limits, add a `param`. If the pattern is binary (present/absent), omit params.

3. **Choose the right impact quality**: Default to `MAINTAINABILITY`. Only use `RELIABILITY` if the pattern can cause runtime failures.

4. **Consider the reader**: Maintainability rules should be framed from the perspective of the developer who has to understand and modify the code later. The description should explain *why* the pattern makes maintenance harder.

5. **Distinguish from `too-many-parameters` in code-smells**: Note that `long-parameter-list` exists in code-smells with `maxParams: 5`, while `too-many-parameters` exists here with `max: 7`. These have different thresholds and framings. When creating new rules, avoid this kind of duplication.

### Template (CODE_SMELL)

```json
{
  "key": "new-maintainability-rule",
  "name": "New Maintainability Rule Name",
  "description": "Detects <pattern> which makes code harder to <read|understand|modify|test> because <reason>.",
  "severity": "MAJOR",
  "type": "CODE_SMELL",
  "tags": ["maintainability", "readability", "<specific-tag>"],
  "remediation": {
    "constantCost": "20min",
    "examples": [
      {
        "before": "// Bad: <explain the problem>\n<problematic Java code>",
        "after": "// Good: <explain the improvement>\n<improved Java code>"
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
    "offset": "20min"
  }
}
```

### Template with Parameters

```json
{
  "key": "new-threshold-maintainability-rule",
  "name": "New Threshold-Based Maintainability Rule",
  "description": "Detects <metric> exceeding <threshold>, which reduces readability and increases maintenance cost.",
  "severity": "MAJOR",
  "type": "CODE_SMELL",
  "tags": ["maintainability", "complexity", "<specific-tag>"],
  "remediation": {
    "constantCost": "25min",
    "examples": [
      {
        "before": "// Bad: <metric> is too high\n<example>",
        "after": "// Good: refactored to reduce <metric>\n<fixed example>"
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
    "offset": "25min"
  },
  "params": [
    {
      "key": "max",
      "name": "Maximum Allowed Value",
      "description": "The maximum <metric> before the rule triggers",
      "defaultValue": "10",
      "type": "INTEGER"
    }
  ]
}
```

---

## Common Mistakes to Avoid

- **Don't use `VULNERABILITY`** — maintainability issues are never security vulnerabilities.
- **Don't set severity to BLOCKER or CRITICAL** — maintainability rules cap at MAJOR.
- **Don't default to `RELIABILITY` impact** — only use it when the pattern causes runtime failures (like missing-null-check). Everything else is `MAINTAINABILITY`.
- **Don't duplicate code-smells rules** — check `rules/code-smells/` before creating. If `long-parameter-list` already exists there, don't create a similar rule here without distinct justification (note `too-many-parameters` here has a different threshold and framing).
- **Don't use LINEAR debt without a coefficient** — if the function is LINEAR, specify what the time scales with.
- **Don't forget `shotgun-surgery` has LINEAR debt with coefficient `"20min"` but no offset** — when creating new LINEAR debt rules, always include both `offset` and `coefficient`.
- **Don't forget to match `severity` and `defaultSeverity`**.
