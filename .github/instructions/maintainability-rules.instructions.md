---
description: "Use when creating, editing, or reviewing SonarQube maintainability rules in rules/maintainability/. Covers naming conventions, nesting depth, method length, javadoc, null checks, dependencies, URLs, and parameter counts."
applyTo: "rules/maintainability/**"
---

# Maintainability Rules — Authoring Guidelines

## Category Overview

The `rules/maintainability/` directory contains **long-term code health rules** — rules that detect patterns making code harder to read, understand, and safely modify over time. These focus on readability, discoverability, and change safety rather than structural design (code-smells) or runtime behavior (performance).

Currently contains **12 rules** covering: readability (deep nesting, long methods, excessive comments, boolean blindness), conventions (inconsistent naming, missing javadoc), dependencies (circular dependencies, hidden dependencies, hardcoded URLs), safety (missing null check), and change impact (shotgun surgery, too many parameters).

## Mandatory Constraints

- **`type` must be `CODE_SMELL`** — maintainability rules are never `BUG` or `VULNERABILITY`.
- **`severity` ranges from `MINOR` to `MAJOR`**:
  - Use `MAJOR` for issues that substantially impair readability or change safety (deep nesting, long methods, circular dependencies, shotgun surgery, hidden dependencies).
  - Use `MINOR` for convention-based or stylistic issues (inconsistent naming, excessive comments, missing javadoc).
- **`impacts[].softwareQuality` must be `MAINTAINABILITY`**.
  - Use `HIGH` for architectural issues that compound across the codebase (circular dependencies, shotgun surgery).
  - Use `MEDIUM` for localized readability issues (deep nesting, long methods, boolean blindness).
  - Use `LOW` for pure convention violations (inconsistent naming, excessive comments).
- **`tags` must include `"maintainability"`** as the first tag.
- **`severity` and `defaultSeverity` must match.**

## Distinguishing Maintainability from Code Smells

These two categories overlap — use this guide:

| Belongs in `maintainability/` | Belongs in `code-smells/` |
|-------------------------------|---------------------------|
| Readability and comprehension (naming, nesting, comments) | Structural design flaws (god class, feature envy) |
| Convention adherence (javadoc, naming standards) | SOLID principle violations (SRP, LSP, DIP) |
| Dependency management (circular deps, hidden deps) | Refactoring opportunities (duplicate code, dead code) |
| Change safety (shotgun surgery, null checks) | Design pattern anti-patterns (primitive obsession, data clumps) |

**Rule of thumb**: If the fix is "rewrite/restructure the class," it's a code smell. If the fix is "rename, restructure control flow, add documentation, or reorganize dependencies," it's a maintainability issue.

## Tag Conventions

Always include these tags where applicable:

| Tag | When to Use |
|-----|-------------|
| `maintainability` | Every rule (required) |
| `readability` | Issues that make code harder to read (nesting, naming, comments) |
| `conventions` | Naming standards, documentation standards |
| `complexity` | Cognitive complexity issues (nesting, long methods) |
| `refactoring` | Issues with well-known refactoring remedies |
| `dependencies` | Dependency structure issues (circular, hidden) |
| `documentation` | Missing or misleading documentation |
| `null-safety` | Null dereference risks |

## Writing Descriptions

Maintainability rule descriptions must explain:
1. **What** the pattern detects (the specific readability or health issue)
2. **Why** it hurts maintainability (increased cognitive load, change risk, onboarding difficulty)
3. **How** it manifests in practice (e.g., "reduces readability and increases cognitive complexity")

Example: *"Detects code with excessive nesting levels (if statements, loops, try blocks), which reduces readability and increases cognitive complexity."*

## Remediation Examples

Maintainability remediation examples should:
- **`before`**: Show code that a developer would struggle to read, understand, or safely modify.
- **`after`**: Show the improved version using well-known techniques (early returns, guard clauses, dependency injection, extract method).

Prefer examples that demonstrate the specific readability improvement — the "after" should be noticeably easier to scan.

## Remediation Cost Guidelines

Maintainability fixes are generally low-cost:

| Fix Type | Typical Cost |
|----------|-------------|
| Rename variable/method | `5min` |
| Add javadoc to public API | `10min` |
| Add null check / guard clause | `10min` |
| Flatten nesting with early returns | `20min` |
| Extract method from long method | `20min` |
| Remove hardcoded URL to config | `15min` |
| Refactor to remove excessive comments | `10min` |
| Break circular dependency | `2h` |
| Reduce shotgun surgery via extraction | `2h` |

## Debt Model

Maintainability rules predominantly use `CONSTANT_ISSUE` debt:

```json
"debt": {
  "function": "CONSTANT_ISSUE",
  "offset": "20min"
}
```

Use `LINEAR` only for rules where fix cost clearly scales with the size of the violation (e.g., a method that's 500 lines vs 100 lines could justify linear debt, though current rules use constant).

## Params

Maintainability rules **commonly have configurable `params`** — many are threshold-based:

```json
"params": [
  {
    "key": "maxDepth",
    "name": "Maximum Nesting Depth",
    "description": "Maximum allowed nesting depth",
    "defaultValue": "4",
    "type": "INTEGER"
  }
]
```

Common params for maintainability rules:
- `maxDepth` — deep nesting
- `maxLines` — long methods
- `maxParameters` — too many parameters
- `maxNestingDepth` — control flow depth

Set defaults based on widely accepted standards:
- Max nesting depth: `4`
- Max method lines: `30–50`
- Max parameters: `4–5`

## Severity Calibration

Maintainability is the category most prone to severity inflation. Apply this test:

- **Would a senior developer flag this in code review?** → `MAJOR`
- **Would it only show up in a style guide audit?** → `MINOR`
- **Could a junior developer miss a bug because of this?** → `MAJOR`
- **Is it annoying but harmless?** → `MINOR`

Never use `CRITICAL` or `BLOCKER` for maintainability rules. These severities are reserved for security vulnerabilities and critical bugs.

## Checklist for New Maintainability Rules

1. `key` is lower-kebab-case and matches the filename
2. `type` is `CODE_SMELL`
3. `severity` is `MAJOR` or `MINOR` (never `CRITICAL` or `BLOCKER`)
4. `defaultSeverity` matches `severity`
5. `tags` includes `"maintainability"` first, plus relevant sub-tags (readability, conventions, dependencies)
6. `impacts` targets `MAINTAINABILITY` with appropriate severity (`HIGH`, `MEDIUM`, or `LOW`)
7. `description` explains the pattern and its impact on readability or change safety
8. `remediation.examples` shows a clear before/after with visible readability improvement
9. `params` are provided for threshold-based rules with sensible defaults
10. `debt` uses `CONSTANT_ISSUE` with realistic offset
11. `status` is `"READY"`
12. JSON is valid and well-formed
