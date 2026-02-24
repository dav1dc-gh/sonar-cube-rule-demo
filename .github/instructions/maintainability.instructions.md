---
applyTo: "rules/maintainability/**"
---

# Maintainability Rules — Path-Specific Custom Instructions

You are working inside `rules/maintainability/`, which contains **12 SonarQube rule definitions** that promote long-term code health, readability, and developer experience. These rules address structural concerns that affect how easily code can be understood, modified, and extended.

---

## Purpose of This Category

Maintainability rules detect patterns that make code harder to work with over time — deep nesting, hidden dependencies, poor naming, missing documentation, excessive coupling, and lack of null safety. While these issues don't cause immediate failures, they slow down development, increase onboarding time, and raise the cost of every future change. Fixing them is an investment in the long-term velocity of the team.

---

## Current Rules Inventory (12 rules)

| File | Key | Type | Severity | Debt Model | Params? | What It Detects |
|---|---|---|---|---|---|---|
| `boolean-blindness.json` | `boolean-blindness` | CODE_SMELL | MINOR | CONSTANT (25min) | `maxBooleanParams` (2) | Methods with multiple unclear boolean params |
| `circular-dependencies.json` | `circular-dependencies` | CODE_SMELL | MAJOR | CONSTANT (60min) | — | Circular deps between packages/modules/classes |
| `deep-nesting.json` | `deep-nesting` | CODE_SMELL | MAJOR | CONSTANT (20min) | `maxDepth` (4) | Excessive nesting levels in control flow |
| `excessive-comments.json` | `excessive-comments` | CODE_SMELL | MINOR | CONSTANT (15min) | — | Redundant comments that restate the code |
| `hardcoded-urls.json` | `hardcoded-urls` | CODE_SMELL | MINOR | CONSTANT (10min) | — | URLs/endpoints that should be externalized to config |
| `hidden-dependencies.json` | `hidden-dependencies` | CODE_SMELL | MAJOR | CONSTANT (30min) | — | Dependencies not explicit in method signatures |
| `inconsistent-naming.json` | `inconsistent-naming` | CODE_SMELL | MINOR | CONSTANT (5min) | — | Identifiers violating naming conventions |
| `long-methods.json` | `long-methods` | CODE_SMELL | MAJOR | LINEAR (2min/unit) | `max` (100) | Methods exceeding length thresholds |
| `missing-javadoc.json` | `missing-javadoc` | CODE_SMELL | MINOR | CONSTANT (10min) | — | Public APIs without documentation comments |
| `missing-null-check.json` | `missing-null-check` | BUG | MAJOR | CONSTANT (10min) | — | Potential null-pointer dereferences |
| `shotgun-surgery.json` | `shotgun-surgery` | CODE_SMELL | MAJOR | LINEAR (20min/unit) | — | Changes requiring edits in many unrelated classes |
| `too-many-parameters.json` | `too-many-parameters` | CODE_SMELL | MAJOR | CONSTANT (15min) | `max` (7) | Methods with excessive parameter counts |

---

## Category-Specific Conventions

### Type — Mostly `CODE_SMELL`, One `BUG`

- **`CODE_SMELL`** (11 of 12 rules): Structural issues that affect long-term health but don't cause immediate runtime failures.
- **`BUG`** (1 rule: `missing-null-check`): This is the only `BUG` in the category because null-pointer dereferences cause runtime crashes, not just design concerns.

**Guideline**: Use `BUG` only when the pattern will cause a runtime exception or incorrect behavior. Everything else is `CODE_SMELL`.

### Severity Patterns

- `MAJOR` for high-impact structural issues: `circular-dependencies`, `deep-nesting`, `hidden-dependencies`, `long-methods`, `missing-null-check`, `shotgun-surgery`, `too-many-parameters`.
- `MINOR` for lower-impact readability/style concerns: `boolean-blindness`, `excessive-comments`, `hardcoded-urls`, `inconsistent-naming`, `missing-javadoc`.
- Never use `BLOCKER` or `CRITICAL` — maintainability issues don't warrant emergency-level severity.

### Impacts

- `softwareQuality` is `"MAINTAINABILITY"` for 10 of 12 rules.
- `"RELIABILITY"` is used for `missing-null-check` (NPE crashes) and the `impacts.severity` field for `missing-null-check` is `"MEDIUM"`.
- Impact severity ranges: `"LOW"` (naming, comments, URLs, docs, boolean blindness), `"MEDIUM"` (nesting, methods, null checks, hidden deps, parameters, shotgun surgery), `"HIGH"` (circular dependencies).

### Tags

- Always include `"maintainability"` as the first tag.
- Add concern-specific tags: `"readability"`, `"design"`, `"architecture"`, `"coupling"`, `"cohesion"`, `"complexity"`, `"refactoring"`.
- Add practice tags: `"clean-code"`, `"conventions"`, `"defensive-programming"`, `"dependency-injection"`, `"api-design"`.
- Include cross-cutting tags when the issue affects other qualities: `"testability"`, `"reliability"`, `"null-safety"`.

### Debt Model

This category uses **both** models, plus a notable edge case:

- **`CONSTANT_ISSUE`** (9 rules): Fixed-cost fixes (rename, add null check, add docs, extract config).
- **`LINEAR`** (2 rules):
  - `long-methods`: `coefficient: "2min"`, `offset: "0min"` — each line over the threshold adds 2 minutes of refactoring.
  - `shotgun-surgery`: `coefficient: "20min"` — each additional class touched adds 20 minutes. **Note**: `shotgun-surgery` is missing its `offset` field, which is an anomaly in this repo. When creating new LINEAR rules, always include both `coefficient` and `offset`.

### Configurable Parameters (`params`)

4 of 12 rules have `params`:

| Rule | Param | Default | What It Controls |
|---|---|---|---|
| `boolean-blindness` | `maxBooleanParams` | 2 | Max boolean parameters before triggering |
| `deep-nesting` | `maxDepth` | 4 | Max nesting depth of control structures |
| `long-methods` | `max` | 100 | Max lines per method |
| `too-many-parameters` | `max` | 7 | Max parameters per method |

**Note the overlap with `code-smells/`**: `too-many-parameters` (max: 7) in this directory and `long-parameter-list` (maxParams: 5) in `code-smells/` address similar concerns with different thresholds. Be aware of this when creating new rules to avoid further duplication.

### Remediation Examples

- Show the hard-to-maintain pattern in `before` and the improved version in `after`.
- This category spans a wide range of concerns, so examples vary significantly:
  - **Structural**: Circular dependency → interface extraction; shotgun surgery → consolidated annotations.
  - **Readability**: Deep nesting → early returns/guard clauses; excessive comments → self-documenting code.
  - **Configuration**: Hardcoded URLs → externalized properties; hidden deps → constructor injection.
  - **Documentation**: Missing Javadoc → complete `@param`/`@return` docs.
  - **Safety**: Missing null check → explicit validation with named exception.
- Use Java examples for consistency, but some rules (naming, nesting, params) apply cross-language.

---

## Guidelines for Creating New Maintainability Rules

1. **Distinguish from code-smells**: If the rule is about an OOP anti-pattern from Fowler's catalogue (Feature Envy, God Class, Data Clumps), it belongs in `code-smells/`. If it's about general code health, readability, or structure (naming, nesting, documentation), it belongs here.
2. **Distinguish from performance**: If the primary concern is runtime speed or resource consumption, it belongs in `performance/` even if poor maintainability is a secondary effect.
3. **Set thresholds conservatively**: Default `params` should be mainstream values that most teams would agree on. Allow teams to tighten them via configuration.
4. **Write actionable descriptions**: Explain not just _what_ the problem is but _why_ it hurts maintainability and _how_ to fix it (in 1–3 sentences).
5. **Pair structural rules with specific refactoring techniques**: Reference Extract Method, Introduce Parameter Object, Replace Inheritance with Delegation, Guard Clause, etc.
6. **Consider the "bus factor"**: Maintainability rules protect against knowledge silos. If a rule makes code easier for a new team member to understand, it fits here.

---

## Common Pitfalls to Avoid

- **Don't use `"type": "VULNERABILITY"`** — maintainability issues are never security vulnerabilities.
- **Don't set severity to BLOCKER or CRITICAL** — even circular dependencies, the most impactful rule here, is only MAJOR.
- **Don't duplicate `code-smells/` rules**: Check for overlap before adding rules about method length, parameter counts, or complexity — similar rules may already exist in the sibling directory.
- **Don't forget the `offset` field in LINEAR debt** — `shotgun-surgery` is missing it, which is an anomaly. New rules should always include both `coefficient` and `offset`.
- **Don't use `"SECURITY"` as `softwareQuality`** — that belongs exclusively in `rules/security/`.
- **Don't over-parameterize** — only add configurable `params` when the threshold is genuinely context-dependent and teams would benefit from tuning it.
