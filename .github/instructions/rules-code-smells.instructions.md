---
applyTo: "rules/code-smells/**"
---

# Code Smells Rules — Custom Instructions

You are assisting with SonarQube **code smell** rule definitions in `rules/code-smells/`.

## Category Context

Code smell rules detect structural quality issues that indicate poor design, excessive complexity, or accumulated technical debt. They don't represent bugs or vulnerabilities — the code works correctly — but they signal that the codebase is becoming harder to understand, modify, and extend. These rules help teams maintain design discipline and catch architectural drift early.

## Constraints for This Category

- **`type` MUST be `CODE_SMELL`** — these are design/structural issues, not runtime bugs or security vulnerabilities.
- **`severity` is typically `MAJOR`** — use `CRITICAL` only for extreme violations (e.g., a 5000-line god class). Use `MINOR` for stylistic concerns that don't significantly impair comprehension.
- **`impacts[].softwareQuality` MUST include `MAINTAINABILITY`** — code smells primarily affect how easy code is to change and understand.
- **`tags` MUST include `"code-smell"`** — additionally tag with relevant design concerns:
  - `solid` — for Single Responsibility, Open/Closed, Liskov, Interface Segregation, or Dependency Inversion violations
  - `design` — for general OOP/FP design issues
  - `complexity` — for cyclomatic or cognitive complexity
  - `duplication` — for copy-paste or structural duplication
  - `refactoring` — when the fix is a well-known refactoring pattern

## Writing Descriptions

Code smell descriptions should:
1. **What** the problematic pattern is (e.g., "classes exceeding 500 lines with multiple unrelated responsibilities")
2. **Why** it's harmful (e.g., "violates SRP, increases coupling, makes testing difficult")
3. **Consequences** of leaving it unfixed (e.g., "cascading changes, regression risk, onboarding friction")
4. **Threshold** when applicable (e.g., "triggered when cyclomatic complexity exceeds 15")

Descriptions should educate developers — many code smells are subjective, so the rule must justify *why* the pattern is problematic.

## Remediation Examples

For code smell rules, remediation examples must:
- Show a **recognizable bad pattern** — developers should see their own code in it
- Show a **clean refactored version** — using well-known refactoring techniques (Extract Method, Extract Class, Replace Conditional with Polymorphism, etc.)
- Name the **refactoring pattern** being applied when it has a standard name
- Keep examples concise but realistic — use comments to indicate elided code when needed

## Remediation Cost Guidelines

| Fix Complexity | `constantCost` | Example |
|---|---|---|
| Rename / extract variable | `5min` | Replace magic number with named constant |
| Extract method | `15min` | Pull nested logic into a named method |
| Extract class / split | `1h–2h` | Break a god class into focused services |
| Architectural refactoring | `4h` | Eliminate circular dependencies, redesign inheritance |

## Configurable Thresholds (`params`)

Code smell rules frequently benefit from configurable thresholds. Always consider adding `params` for:
- **Line counts** — `maxLines` for god class, long methods
- **Complexity metrics** — `maxComplexity` for cyclomatic/cognitive complexity
- **Counts** — `maxParameters`, `maxMethods`, `maxDepth`
- **Duplication** — `minTokens` for minimum duplication size

Use `"type": "INTEGER"` for numeric thresholds and provide a sensible `defaultValue` based on industry standards (e.g., max cyclomatic complexity of 15, max method length of 30 lines).

## Debt Function Guidelines

- Use `CONSTANT_ISSUE` when every occurrence takes roughly the same effort to fix (e.g., empty catch block — always ~10min).
- Use `LINEAR` when fix effort scales with the size of the smell (e.g., god class — 10min per excess method/responsibility to extract). Set `coefficient` to the per-unit cost and `offset` to `"0min"`.

## Common Tags for Code Smell Rules

`code-smell`, `design`, `solid`, `complexity`, `duplication`, `refactoring`, `maintainability`, `readability`, `coupling`, `cohesion`, `testing`, `naming`

## When Creating New Code Smell Rules

1. Check for overlap with existing rules — this category has 17 rules covering common design anti-patterns.
2. Verify the issue isn't better classified as `performance` (runtime impact) or `maintainability` (readability/convention focus).
3. Reference the original pattern source when applicable (Fowler's *Refactoring*, Kerievsky's *Refactoring to Patterns*, etc.).
4. Consider whether the smell has a measurable threshold — if so, expose it as a `param`.
5. Ensure the rule is language-agnostic or clearly states which languages it applies to.

## Quality Checklist

- [ ] `type` is `CODE_SMELL`
- [ ] `severity` is `MAJOR` (or justified `CRITICAL`/`MINOR`)
- [ ] `impacts` includes `{ "softwareQuality": "MAINTAINABILITY", "severity": "HIGH" or "MEDIUM" }`
- [ ] `tags` includes `"code-smell"` plus at least one design-related tag
- [ ] Description explains what, why, and consequences
- [ ] Remediation example uses a named refactoring technique
- [ ] `params` included if the rule has a measurable threshold
- [ ] `debt` function matches the fix-effort scaling model
- [ ] Filename matches `key` field in lower-kebab-case
