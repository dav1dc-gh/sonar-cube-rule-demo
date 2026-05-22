---
applyTo: rules/code-smells/**
---

# Code Smells Rules — Custom Instructions

You are assisting with SonarQube **code smell** rule definitions in `rules/code-smells/`.

## Category Context

These rules detect structural quality issues — poor design patterns, excessive complexity, and violations of clean code principles. They indicate technical debt that makes code harder to understand, modify, and extend.

## Key Constraints

- **`type`** must always be `"CODE_SMELL"`.
- **`severity`** is typically `MAJOR` for significant design issues, `MINOR` for style/convention violations, and `CRITICAL` only for severe structural problems (e.g., god classes exceeding 2000 lines).
- **`impacts[].softwareQuality`** must be `"MAINTAINABILITY"` (primary). Add `"RELIABILITY"` if the smell commonly leads to bugs.
- **Tags**: Always include `"code-smell"`. Add design-principle tags like `"solid"`, `"dry"`, `"clean-code"`, `"design-pattern"` as relevant.

## Description Guidelines

- Explain **what** the code smell looks like in practice.
- Explain **why** it's problematic — what maintenance burden or risk does it create?
- Reference design principles (SRP, DRY, Law of Demeter) when applicable.

## Remediation Examples

- The `before` example should show a recognizable, realistic instance of the smell.
- The `after` example should show the refactored version applying the appropriate design pattern or principle.
- Keep examples concise but complete enough to demonstrate the transformation.

## Remediation Cost

- Simple refactors (extract method, rename): `"15min"` to `"30min"`
- Moderate refactors (extract class, introduce parameter object): `"1h"` to `"2h"`
- Large refactors (decompose god class, eliminate duplication): `"2h"` to `"4h"`

## Parameters

- Code smell rules commonly have configurable thresholds. Include `params` for numeric limits like max lines, max complexity, max parameters, etc.
- Always provide sensible `defaultValue` entries that align with industry standards.

## Naming

- Keys should describe the smell in lower-kebab-case: `god-class`, `dead-code`, `magic-numbers`.
- Use established refactoring terminology from Fowler's catalog when possible.
