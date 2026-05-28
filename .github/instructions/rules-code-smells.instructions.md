---
applyTo: "rules/code-smells/**"
---

# Code Smells Rules — Copilot Custom Instructions

You are assisting with SonarQube **code smell** rule definitions in the `rules/code-smells/` directory. This category identifies structural quality issues, poor design patterns, and symptoms of technical debt that make code harder to understand, modify, and extend.

---

## Category Context

This directory currently contains **17 rules** covering object-oriented design violations, complexity issues, dead/duplicate code, and anti-patterns. Rules here are rooted in established software engineering principles: SOLID, DRY, YAGNI, Law of Demeter, and Martin Fowler's refactoring catalog.

---

## Rule Authoring Guidelines for Code Smells

### Type & Severity
- **Type** must always be `CODE_SMELL`.
- **Severity** is typically `MAJOR` for design issues that accumulate meaningful tech debt. Use `MINOR` for stylistic preferences or low-impact smells. Use `CRITICAL` sparingly — only when the smell directly leads to bugs or severe maintenance burden (e.g., unsafe concurrent modification).
- Never use `BLOCKER` for code smells.

### Impacts
- The `softwareQuality` field should be `"MAINTAINABILITY"` for most code smells.
- Use severity `"HIGH"` for design violations that affect entire class/module structure (god class, circular dependencies).
- Use severity `"MEDIUM"` for localized issues (magic numbers, long parameter lists).
- Add a secondary `"RELIABILITY"` impact if the smell commonly leads to bugs (e.g., null-pointer dereference, unchecked return values).

### Tags — Required Conventions
- Always include `"code-smell"` as a tag.
- Include the relevant design principle tag: `"solid"`, `"dry"`, `"yagni"`, `"law-of-demeter"`, `"encapsulation"`.
- Include a category-hint tag for cross-reference: `"design"`, `"complexity"`, `"duplication"`, `"dead-code"`, `"refactoring"`.
- Add `"maintainability"` when the smell primarily impacts long-term code health.

### Description Best Practices
- Explain the **structural pattern** being detected — what does the code look like?
- State the **consequence**: why does this smell cause problems? (harder to test, higher bug rate, increased coupling, etc.)
- Reference the relevant design principle or heuristic being violated.
- Avoid vague language like "bad practice" — be specific about the structural problem.

### Remediation Examples
- `before` examples should show a **recognizable anti-pattern** that developers encounter in real codebases.
- `after` examples should demonstrate the **refactoring technique**: Extract Class, Extract Method, Replace Conditional with Polymorphism, Introduce Parameter Object, etc.
- Name the refactoring being applied in a comment (e.g., `// Refactoring: Extract Class`).
- Remediation cost should scale with the refactoring difficulty: rename → `"5min"`, extract method → `"15min"`, extract class → `"2h"`, large restructuring → `"4h"`.

### Parameters (params)
- Code smell rules **frequently benefit from configurable thresholds**. Always consider whether the rule's detection depends on a numeric limit.
- Common params: `maxLines`, `maxMethods`, `maxParameters`, `maxDepth`, `maxComplexity`, `maxDuplicateLines`.
- Provide sensible defaults based on industry norms (e.g., max method lines: 30, max class lines: 500, max parameters: 5).
- Use `"type": "INTEGER"` for numeric thresholds and `"type": "BOOLEAN"` for feature toggles.

### Debt Estimation
- Use `LINEAR` debt when remediation cost scales with the size of the smell (e.g., splitting a 2000-line class takes longer than a 600-line one). Set `coefficient` to the per-unit cost.
- Use `CONSTANT_ISSUE` when the fix is atomic regardless of severity (e.g., removing dead code, adding a null check).

### Common Pitfalls to Avoid
- Do NOT set type to `VULNERABILITY` or `BUG` — code smells are quality/design issues, not security flaws or functional defects.
- Do NOT set severity higher than `MAJOR` unless the smell has demonstrated reliability impact.
- Do NOT write rules that overlap significantly with existing ones — check whether the smell is a subset of an existing rule.
- Do NOT omit `params` when the rule clearly has a configurable threshold.

---

## When Creating New Code Smell Rules

1. Verify the smell isn't already covered — many smells overlap (e.g., "long methods" vs. "complex methods").
2. Identify which refactoring from Fowler's catalog addresses this smell.
3. Name the `key` after the smell pattern, not the fix (e.g., `"god-class"` not `"split-class"`).
4. Include at least one `params` entry if the detection relies on any numeric threshold.
5. Ensure the description references the violated principle (SRP, DRY, etc.).

---

## Existing Rules Reference

anemic-domain-model, complex-methods, data-clumps, dead-code, duplicate-code, empty-catch-block, feature-envy, god-class, long-parameter-list, magic-numbers, message-chains, null-pointer-dereference, primitive-obsession, refused-bequest, speculative-generality, unchecked-return-value, unsafe-concurrent-modification
