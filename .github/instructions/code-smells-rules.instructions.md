---
description: "Use when creating, editing, or reviewing SonarQube code smell rules in rules/code-smells/. Covers structural quality issues like god classes, dead code, duplication, design pattern violations, and SOLID principle breaches."
applyTo: "rules/code-smells/**"
---

# Code Smell Rules — Authoring Guidelines

## Category Overview

The `rules/code-smells/` directory contains **structural quality rules** — rules that detect poor design patterns, unnecessary complexity, and violations of established software engineering principles (SOLID, DRY, Law of Demeter). These are not bugs or vulnerabilities but indicators that the code will become increasingly difficult to work with.

Currently contains **13 rules** covering: design issues (god class, feature envy, refused bequest, speculative generality), duplication & waste (duplicate code, dead code), complexity (complex methods, long parameter list), poor practices (empty catch block, magic numbers, message chains, primitive obsession, data clumps).

## Mandatory Constraints

- **`type` must be `CODE_SMELL`** — never `BUG` or `VULNERABILITY`. Code smells indicate quality issues, not functional defects or security holes.
- **`severity` is typically `MAJOR`** — most code smells represent significant technical debt. Use `MINOR` only for purely stylistic issues.
  - Use `MAJOR` for design problems that compound over time (god class, duplicate code, dead code, empty catch blocks).
  - Use `MINOR` for localized issues with low immediate impact (magic numbers in non-critical paths).
- **`impacts[].softwareQuality` is `MAINTAINABILITY`** with severity `HIGH` or `MEDIUM`.
  - Use `HIGH` for issues that substantially erode codebase health (god class, dead code, duplicate code).
  - Use `MEDIUM` for localized smells (empty catch block, magic numbers).
  - Some smells may also impact `RELIABILITY` (e.g., empty catch blocks hiding errors).
- **`tags` must include `"code-smell"`** as the first tag.
- **`severity` and `defaultSeverity` must match.**

## Tag Conventions

Always include these tags where applicable:

| Tag | When to Use |
|-----|-------------|
| `code-smell` | Every rule (required) |
| `design` | Structural/architectural issues (god class, feature envy) |
| `solid` | Violations of SOLID principles (SRP, OCP, LSP, ISP, DIP) |
| `maintainability` | Anything that makes code harder to evolve |
| `refactoring` | Issues with well-known refactoring remedies |
| `error-handling` | Exception handling anti-patterns |
| `duplication` | Repeated code or logic |
| `complexity` | High cyclomatic or cognitive complexity |

## Writing Descriptions

Code smell descriptions must explain:
1. **What** the pattern detects (the structural issue)
2. **Why** it's a problem (the real-world consequence — harder to test, harder to change, error-prone)
3. **Which principle** it violates, if applicable (SRP, DRY, Law of Demeter)

Example: *"Detects classes that have grown too large and handle too many responsibilities, violating the Single Responsibility Principle and making the code difficult to understand and maintain."*

## Remediation Examples

Code smell remediation examples should:
- **`before`**: Show a recognizable anti-pattern that developers commonly write, using comments to indicate scale when showing large structural issues (e.g., "// Class with 2000+ lines handling...").
- **`after`**: Show the refactored result using the appropriate refactoring technique (Extract Class, Extract Method, Replace Conditional with Polymorphism, etc.).

Name the specific refactoring technique in the example when applicable.

## Remediation Cost Guidelines

Code smells span a wide range of fix effort:

| Fix Type | Typical Cost |
|----------|-------------|
| Rename or extract constant (magic numbers) | `5min` |
| Log or rethrow in catch block | `10min` |
| Extract method to reduce complexity | `15min` |
| Remove dead code | `15min` |
| Extract class from god class | `4h` |
| Resolve duplicate code (extract shared method/class) | `30min` |
| Redesign to eliminate feature envy | `1h` |

## Debt Model

Code smell rules use either `CONSTANT_ISSUE` or `LINEAR` debt:

- **`CONSTANT_ISSUE`**: When the fix cost is the same regardless of severity (e.g., empty catch block — always add logging).
- **`LINEAR`**: When the fix cost scales with the size of the problem (e.g., god class — the larger the class, the more work to split it).

```json
// Constant — e.g., empty catch block
"debt": { "function": "CONSTANT_ISSUE", "offset": "10min" }

// Linear — e.g., god class (cost scales with class size)
"debt": { "function": "LINEAR", "coefficient": "10min", "offset": "0min" }
```

## Params

Code smell rules **often benefit from configurable `params`** — many smells are threshold-based. If a rule's detection depends on a measurable quantity, expose it:

```json
"params": [
  {
    "key": "maxLines",
    "name": "Maximum Lines",
    "description": "Maximum number of lines allowed in a class",
    "defaultValue": "500",
    "type": "INTEGER"
  }
]
```

Common params across code smell rules:
- `maxLines` — for god class, long methods
- `maxMethods` — for god class
- `maxComplexity` — for complex methods
- `maxParameters` — for long parameter list
- `maxDepth` — for message chains

Choose sensible defaults based on industry standards and keep param names consistent with existing rules.

## Checklist for New Code Smell Rules

1. `key` is lower-kebab-case and matches the filename
2. `type` is `CODE_SMELL`
3. `severity` is `MAJOR` (or `MINOR` for purely stylistic issues)
4. `defaultSeverity` matches `severity`
5. `tags` includes `"code-smell"` first, plus relevant sub-tags (design, solid, refactoring)
6. `impacts` includes `{ "softwareQuality": "MAINTAINABILITY", "severity": "HIGH" or "MEDIUM" }`
7. `description` explains the pattern, the consequence, and the violated principle
8. `remediation.examples` has at least one before/after pair with realistic code
9. `params` are provided when the rule has configurable thresholds
10. `debt` uses `LINEAR` for size-dependent smells, `CONSTANT_ISSUE` otherwise
11. `status` is `"READY"`
12. JSON is valid and well-formed
