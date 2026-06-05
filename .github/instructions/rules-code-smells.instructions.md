---
applyTo: rules/code-smells/**
---

# Code Smells Rules — Custom Instructions

You are assisting with SonarQube **code smell** rule definitions in `rules/code-smells/`. These rules detect structural quality issues that indicate poor design, accumulated technical debt, or violations of established software engineering principles.

## Category Constraints

- **`type` MUST be `CODE_SMELL`** — every rule in this directory represents a design or structural issue, not a runtime bug or exploitable vulnerability.
- **`severity` is typically `MAJOR` or `MINOR`** — code smells are quality issues, not immediate threats. Use `CRITICAL` only for severe design violations that actively block development (e.g., massive god classes in shared code).
- **`tags` MUST include `"code-smell"`** as the first tag. Add design principle tags: `"solid"`, `"dry"`, `"design"`, `"coupling"`, `"cohesion"`, `"refactoring"` where applicable.
- **`impacts` should target `"MAINTAINABILITY"`** with severity `HIGH` or `MEDIUM` depending on how severely the smell impairs future changes.

## Writing Code Smell Descriptions

Descriptions must clearly communicate:
1. **What the smell is** — the structural pattern detected (e.g., "a class with more than 500 lines handling multiple unrelated responsibilities").
2. **Why it's problematic** — the engineering consequence (e.g., "violates Single Responsibility Principle, making the class difficult to test, understand, and modify independently").
3. **The accumulation effect** — how the smell compounds over time (e.g., "attracts more responsibilities as developers default to adding features to the existing large class").

Reference design principles (SOLID, DRY, YAGNI, Law of Demeter, Tell Don't Ask) to ground the rationale.

## Remediation Examples

Code smell remediation examples should show:
- **Before**: A recognizable code pattern that developers commonly write (realistic class/method sizes, naming, structure).
- **After**: The refactored version applying the appropriate design pattern or extraction.

Common refactoring patterns to reference:
- God Class → Extract Class, Extract Interface
- Long Method → Extract Method, Replace Temp with Query
- Feature Envy → Move Method to the class whose data it uses
- Data Clumps → Introduce Parameter Object / Value Object
- Primitive Obsession → Replace Primitive with Domain Object
- Long Parameter List → Introduce Parameter Object, Builder Pattern
- Duplicate Code → Extract Method, Template Method Pattern
- Message Chains → Hide Delegate, introduce wrapper method
- Speculative Generality → Remove unused abstractions, Collapse Hierarchy

## Remediation Cost Guidelines

| Refactoring Scope | `constantCost` | Examples |
|---|---|---|
| Rename / inline | `5min` | Fix naming, inline trivial method |
| Extract single method | `15min` | Pull out one responsibility |
| Extract class / introduce object | `1h` | Break up god class, create value object |
| Redesign module boundaries | `4h` | Resolve circular dependencies, restructure packages |

## Configurable Parameters (`params`)

Code smell rules frequently benefit from configurable thresholds. Always consider whether the rule should expose `params`:

| Common Parameter | Type | Typical Default | Use When |
|---|---|---|---|
| `maxLines` | `INTEGER` | `500` | Classes/methods exceeding line counts |
| `maxMethods` | `INTEGER` | `20` | Classes with too many methods |
| `maxParameters` | `INTEGER` | `5` | Long parameter lists |
| `maxComplexity` | `INTEGER` | `10` | Cyclomatic complexity thresholds |
| `maxDepth` | `INTEGER` | `4` | Nesting or inheritance depth |
| `minDuplicateLines` | `INTEGER` | `6` | Duplicate code block size |

## Debt Function Selection

- **`CONSTANT_ISSUE`** — use when every instance takes roughly the same effort to fix (e.g., empty catch block, magic number).
- **`LINEAR`** — use when fix effort scales with the size of the violation (e.g., god class fix time scales with excess lines, duplicate code scales with duplicated block count).

For LINEAR debt, set `coefficient` to the per-unit fix time and `offset` to `"0min"`.

## Severity Decision Matrix

| Design Impact | Frequency | Severity |
|---|---|---|
| Blocks independent testing/deployment | Common in codebase | `CRITICAL` |
| Significantly impairs readability or change velocity | Moderate | `MAJOR` |
| Minor inconvenience, style-level | Localized | `MINOR` |

## Key Principles

- Code smells are about **maintainability cost**, not correctness — the code works but is expensive to evolve.
- Focus on **observable developer pain**: difficulty testing, difficulty understanding, difficulty changing without side effects.
- Avoid overly strict thresholds that generate noise — defaults should catch genuine problems, not penalize every slightly-long method.
- Remediation advice should name the specific refactoring technique (Martin Fowler's catalog is the reference).
- Acknowledge that not all smells warrant immediate action — the rule flags the issue; severity and context determine priority.
