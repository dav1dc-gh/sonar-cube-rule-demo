---
applyTo: rules/maintainability/**
---

# Maintainability Rules — Custom Instructions

You are assisting with SonarQube **maintainability** rule definitions in `rules/maintainability/`. These rules detect patterns that erode long-term code health, readability, and the ability of development teams to safely evolve the codebase over time.

## Category Constraints

- **`type` MUST be `CODE_SMELL`** — maintainability rules flag quality issues that make code harder to read, understand, and change. They are not bugs or vulnerabilities.
- **`severity` is typically `MAJOR` or `MINOR`** — use `MAJOR` for patterns that actively slow down development teams or cause frequent bugs during modifications. Use `MINOR` for style/convention issues.
- **`tags` MUST include `"maintainability"`** as the first tag. Add relevant tags: `"readability"`, `"complexity"`, `"naming"`, `"documentation"`, `"coupling"`, `"testing"`, `"conventions"`, `"refactoring"` where applicable.
- **`impacts` MUST include `{"softwareQuality": "MAINTAINABILITY", ...}`** — this is the primary quality attribute. Set severity to `HIGH` for patterns that cause bugs during changes, `MEDIUM` for friction without direct defect risk.

## Distinction from Code Smells

While both categories use type `CODE_SMELL`, they differ in focus:
- **Code smells** (`rules/code-smells/`) target **design and structural** issues (god classes, feature envy, data clumps) — problems with how responsibilities are distributed.
- **Maintainability** (`rules/maintainability/`) targets **readability, convention adherence, and change safety** — problems with how easily developers can understand and modify code day-to-day.

Place rules here when the primary concern is: "Can a developer who didn't write this code safely modify it?"

## Writing Maintainability Rule Descriptions

Descriptions must clearly communicate:
1. **The readability/change hazard** — what makes the code hard to work with (e.g., "deeply nested control structures require tracking multiple conditions simultaneously, exceeding cognitive load limits").
2. **The maintenance consequence** — what goes wrong when developers modify this code (e.g., "developers frequently introduce bugs when adding new conditions because they misjudge which branch they're modifying").
3. **The team impact** — how it affects collaboration (e.g., "new team members take significantly longer to understand the logic, slowing onboarding and code review").

Reference cognitive complexity, readability studies, or industry conventions to ground the rationale.

## Remediation Examples

Maintainability remediation examples should show:
- **Before**: Code that is functional but hard to read, modify, or understand.
- **After**: The same logic restructured for clarity, with explicit intent and reduced cognitive load.

Common improvement patterns:
- Deep nesting → Guard clauses (early return), Extract Method
- Boolean blindness → Named constants, enums, Builder pattern, Parameter Objects
- Missing null check → Optional, Null Object Pattern, `@NonNull` annotations
- Inconsistent naming → Adopt consistent vocabulary (e.g., `get`/`find`/`fetch` conventions)
- Hidden dependencies → Dependency injection, explicit constructor parameters
- Circular dependencies → Introduce interface, Dependency Inversion Principle
- Excessive comments → Self-documenting code with better naming, remove stale comments
- Long methods → Extract Method, decompose by abstraction level
- Shotgun surgery → Consolidate related logic, apply Information Expert principle
- Missing javadoc → Add meaningful API documentation explaining intent, not just signature

## Remediation Cost Guidelines

| Fix Complexity | `constantCost` | Examples |
|---|---|---|
| Rename / add annotation | `5min` | Fix naming convention, add `@NonNull` |
| Add documentation | `10min` | Write javadoc for public API |
| Restructure single method | `20min` | Extract guard clauses, reduce nesting |
| Introduce explicit dependency | `30min` | Convert hidden dep to constructor injection |
| Break circular dependency | `2h` | Introduce interface, restructure packages |
| Redesign module API surface | `4h` | Consolidate shotgun surgery targets |

## Configurable Parameters (`params`)

Maintainability rules should expose thresholds for team-configurable standards:

| Common Parameter | Type | Typical Default | Use When |
|---|---|---|---|
| `maxDepth` | `INTEGER` | `4` | Maximum nesting depth |
| `maxLines` | `INTEGER` | `30` | Maximum method length |
| `maxParameters` | `INTEGER` | `5` | Maximum parameter count |
| `requireJavadocFor` | `STRING` | `"public"` | Visibility threshold for javadoc requirement |
| `namingPattern` | `STRING` | `"^[a-z][a-zA-Z0-9]*$"` | Regex for naming conventions |
| `maxCognitiveComplexity` | `INTEGER` | `15` | Cognitive complexity threshold |

## Severity Decision Matrix

| Change Risk | Team Impact | Severity |
|---|---|---|
| Frequently causes bugs during modification | Affects shared/core code | `MAJOR` |
| Slows comprehension, increases review time | Moderate reach | `MAJOR` |
| Cosmetic inconsistency, localized | Single file/method | `MINOR` |
| Informational suggestion | Team preference | `INFO` |

## Debt Function Selection

- **`CONSTANT_ISSUE`** — use for issues with a fixed remediation effort regardless of severity (e.g., adding a null check, writing javadoc for one method).
- **`LINEAR`** — use when fix effort scales with violation magnitude (e.g., reducing nesting depth requires more work the deeper it is; untangling circular dependencies grows with the number of involved classes).

## Key Principles

- **Optimize for the reader, not the writer** — code is read 10x more than it is written. Maintainability rules protect future readers.
- **Conventions reduce cognitive load** — consistent naming, structure, and documentation let developers focus on business logic instead of deciphering patterns.
- **Explicit beats implicit** — hidden dependencies, implicit nullability, and undocumented behavior are maintenance hazards even if the code works today.
- **Change safety over elegance** — the goal is not beautiful code but code that can be modified without unintended consequences. Tests, clear contracts, and minimal coupling enable safe change.
- **Team standards vary** — maintainability thresholds (line counts, complexity limits, naming patterns) are team decisions. Always provide `params` for numeric thresholds with sensible defaults that catch genuine problems without generating noise.
- **Complement code smells, don't duplicate** — if a rule is fundamentally about responsibility distribution or structural design, it belongs in `code-smells/`. If it's about day-to-day readability and modification safety, it belongs here.
