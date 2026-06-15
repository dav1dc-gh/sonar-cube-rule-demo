---
applyTo: "rules/maintainability/**"
---

# Maintainability Rules — Custom Instructions

You are assisting with SonarQube **maintainability** rule definitions in `rules/maintainability/`.

## Category Context

Maintainability rules target long-term code health, readability, and developer ergonomics. They detect patterns that make code harder to read, reason about, test, or safely modify over time. Unlike code smells (which focus on design/structural anti-patterns), maintainability rules focus on **conventions, clarity, and cognitive load** — the day-to-day friction developers experience when working with a codebase.

## Constraints for This Category

- **`type` MUST be `CODE_SMELL`** — maintainability issues are quality concerns, not runtime bugs or exploitable vulnerabilities.
- **`severity` ranges from `MINOR` to `MAJOR`** — use `MAJOR` for issues that significantly impair understanding or create defect risk (missing null checks, hidden dependencies). Use `MINOR` for convention violations (naming, comments). Rarely use `CRITICAL` — only when the issue consistently causes downstream bugs.
- **`impacts[].softwareQuality` MUST include `MAINTAINABILITY`** — severity should be `MEDIUM` for most rules, `HIGH` for issues that frequently cause bugs (e.g., missing null checks, circular dependencies).
- **`tags` MUST include `"maintainability"`** — additionally tag with:
  - `readability` — for issues that impair code comprehension
  - `naming` — for identifier naming convention violations
  - `documentation` — for missing or misleading docs
  - `complexity` — for cognitive complexity issues
  - `convention` — for team/language convention violations
  - `refactoring` — when the fix involves a known refactoring
  - `coupling` — for dependency-related issues
  - `testing` — when the issue makes code harder to test

## Writing Descriptions

Maintainability rule descriptions should:
1. **What** the problematic pattern is (e.g., "public methods without Javadoc on API-facing classes")
2. **Why** it hurts maintainability (e.g., "forces developers to read implementation details to understand behavior")
3. **Who** is affected (e.g., "new team members, future maintainers, API consumers")
4. **When** the rule applies vs. when it can be reasonably suppressed

Descriptions should appeal to team productivity and defect prevention — maintainability rules need to justify their existence since developers often view them as "noise." Connect the pattern to concrete pain points.

## Remediation Examples

For maintainability rules, remediation examples must:
- Show a **relatable bad pattern** that developers commonly write under time pressure
- Show the **improved version** emphasizing clarity and intent
- Keep examples **minimal but complete** — the improvement should be immediately obvious
- For convention rules, show both the **violation** and the **correct form** side by side
- For documentation rules, show what **good documentation** looks like (not just "add a comment")

## Remediation Cost Guidelines

| Fix Complexity | `constantCost` | Example |
|---|---|---|
| Rename identifier | `5min` | Fix inconsistent naming |
| Add/fix documentation | `10min` | Write Javadoc for a public method |
| Reduce nesting / simplify | `20min` | Apply early return, extract guard clauses |
| Break dependency | `1h` | Inject dependency instead of internal instantiation |
| Resolve circular dependency | `2h–4h` | Introduce interface, restructure packages |

## Distinguishing from Code Smells

The line between `code-smells/` and `maintainability/` can be subtle. Use this heuristic:

| Belongs in `code-smells/` | Belongs in `maintainability/` |
|---|---|
| Design anti-patterns (God Class, Feature Envy) | Convention violations (naming, documentation) |
| Structural duplication | Readability issues (nesting, parameter confusion) |
| OOP/SOLID violations | Dependency clarity (hidden deps, circular deps) |
| Patterns from Fowler's catalog | Cognitive load reducers (null checks, boolean clarity) |

If a rule is about **architectural design quality**, it's a code smell. If it's about **daily developer experience and defect prevention**, it's maintainability.

## Configurable Thresholds (`params`)

Maintainability rules frequently benefit from `params` for:
- **Depth limits** — `maxDepth` for nesting rules
- **Length limits** — `maxLines` for method length, `maxParameters` for parameter counts
- **Naming patterns** — `pattern` (regex) for naming convention rules
- **Scope control** — `checkPublicOnly` (boolean) to limit documentation rules to public APIs

## Common Tags for Maintainability Rules

`maintainability`, `readability`, `naming`, `documentation`, `complexity`, `convention`, `refactoring`, `coupling`, `testing`, `cognitive-complexity`, `null-safety`, `dependency-injection`

## When Creating New Maintainability Rules

1. Check the existing 15 rules plus the `code-smells/` category for overlap.
2. Verify the issue is about **developer experience** rather than design patterns (→ code-smells) or runtime behavior (→ performance).
3. Consider if the rule is **language-specific** — naming conventions and documentation standards vary by ecosystem.
4. Ensure the rule has an **objective trigger** — avoid rules that are purely subjective preference.
5. Set a reasonable threshold that avoids false positives — maintainability rules that fire too often get ignored.
6. Consider whether the rule should have a `checkPublicOnly` or similar scope parameter to reduce noise.

## Quality Checklist

- [ ] `type` is `CODE_SMELL`
- [ ] `severity` is `MAJOR` or `MINOR` (justified if `CRITICAL`)
- [ ] `impacts` includes `{ "softwareQuality": "MAINTAINABILITY", "severity": "MEDIUM" or "HIGH" }`
- [ ] `tags` includes `"maintainability"` plus at least one specific concern tag
- [ ] Description explains what, why, and who is affected
- [ ] Description justifies the rule's value (connects to real developer pain)
- [ ] Remediation example shows clear before/after with obvious improvement
- [ ] `params` included for any measurable threshold
- [ ] Rule is distinguishable from code-smell rules (see heuristic table)
- [ ] Filename matches `key` field in lower-kebab-case
