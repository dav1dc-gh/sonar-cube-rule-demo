---
applyTo: rules/maintainability/**
---

# Maintainability Rules — Custom Instructions

You are assisting with SonarQube **maintainability** rule definitions in `rules/maintainability/`.

## Category Context

These rules detect long-term code health and readability concerns — poor naming, excessive complexity, missing documentation, and architectural coupling that makes code difficult to evolve safely.

## Key Constraints

- **`type`** must always be `"CODE_SMELL"`.
- **`severity`** is typically `MAJOR` for issues that significantly impede comprehension or safe modification, `MINOR` for style and convention issues, `CRITICAL` only for severe coupling or architectural problems.
- **`impacts[].softwareQuality`** must be `"MAINTAINABILITY"` (primary). Add `"RELIABILITY"` if the issue frequently leads to bugs during modification.
- **Tags**: Always include `"maintainability"`. Add tags like `"readability"`, `"naming"`, `"documentation"`, `"coupling"`, `"complexity"`, `"convention"` as relevant.

## Description Guidelines

- Explain **what** makes the code hard to maintain.
- Explain the **consequence** — what goes wrong when someone tries to modify, extend, or debug this code?
- Frame in terms of developer experience: onboarding time, change risk, review difficulty.

## Remediation Examples

- The `before` example should show code that is technically correct but hard to understand or modify.
- The `after` example should show the same logic made clearer, more modular, or better documented.
- Focus on readability and intent clarity in the fix.

## Remediation Cost

- Naming/style fixes: `"5min"` to `"15min"`
- Adding documentation, reducing nesting: `"15min"` to `"30min"`
- Decoupling, breaking circular dependencies: `"1h"` to `"4h"`

## Parameters

- Maintainability rules frequently use thresholds: max nesting depth, max method length, max parameter count.
- Defaults should match widely-adopted standards (e.g., max nesting of 3-4, max method length of 30-50 lines).

## Naming

- Keys should describe the maintainability concern: `deep-nesting`, `inconsistent-naming`, `missing-javadoc`.
- Use terms familiar to code reviewers and style guide authors.
