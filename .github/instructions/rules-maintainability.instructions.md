---
applyTo: "rules/maintainability/**"
---

# Maintainability Rules — Copilot Custom Instructions

You are assisting with SonarQube **maintainability** rule definitions in the `rules/maintainability/` directory. This category focuses on long-term code health — readability, modifiability, testability, and the ability for teams to evolve the codebase safely over time.

---

## Category Context

This directory currently contains **15 rules** covering naming conventions, documentation, dependency management, code complexity, and patterns that resist safe modification. Rules here optimize for **developer experience** — reducing cognitive load and change risk.

---

## Rule Authoring Guidelines for Maintainability

### Type & Severity
- **Type** is always `CODE_SMELL` for maintainability rules.
- **Severity** mapping:
  - `MAJOR` — issues that meaningfully increase the cost of change or the risk of introducing bugs during modification (deep nesting, circular dependencies, shotgun surgery, hidden dependencies).
  - `MINOR` — issues that reduce readability but don't significantly increase change risk (inconsistent naming, excessive comments, missing javadoc).
  - `INFO` — purely advisory findings (style suggestions where team conventions vary).
- Never use `CRITICAL` or `BLOCKER` for pure maintainability issues.

### Impacts
- The `softwareQuality` field must be `"MAINTAINABILITY"`.
- Use severity `"HIGH"` for issues that affect architectural boundaries or module coupling (circular dependencies, hidden dependencies, shotgun surgery).
- Use severity `"MEDIUM"` for issues that affect individual methods/classes (deep nesting, long methods, boolean blindness).
- Use severity `"LOW"` for cosmetic or documentation issues (excessive comments, missing javadoc).
- Add a secondary `"RELIABILITY"` impact when the maintainability issue commonly leads to bugs (e.g., missing null checks, mutable static state, race conditions).

### Tags — Required Conventions
- Always include `"maintainability"` as a tag.
- Include the quality attribute: `"readability"`, `"modifiability"`, `"testability"`, `"documentation"`.
- Include the concern area: `"naming"`, `"complexity"`, `"coupling"`, `"cohesion"`, `"encapsulation"`, `"dependencies"`.
- Add `"refactoring"` when the fix involves a well-known refactoring technique.
- Add `"convention"` for rules that enforce team coding standards.

### Description Best Practices
- Explain the **cognitive cost**: why does this pattern make the code harder to understand or change?
- Describe the **change risk**: what goes wrong when someone modifies code that has this problem?
- Be specific about the pattern being detected — "methods exceeding N lines" is better than "long code".
- Reference the maintenance scenario: onboarding new developers, debugging production issues, adding features, code review overhead.

### Remediation Examples
- `before` examples should show **code that looks innocent but causes maintenance pain** — the kind of pattern that creeps in gradually.
- `after` examples should demonstrate the specific improvement: guard clauses for deep nesting, dependency injection for hidden dependencies, Extract Method for long methods.
- Frame the fix in terms of the **benefit gained**: "Now each method has a single level of abstraction" or "Dependencies are now explicit and mockable in tests".
- Remediation cost should reflect incremental improvement: rename → `"5min"`, extract method → `"15min"`, restructure dependencies → `"1h"`–`"2h"`, resolve circular dependencies → `"4h"`.

### Parameters (params)
- Maintainability rules **frequently need configurable thresholds** since acceptable limits vary by team.
- Common params: `maxDepth`, `maxLines`, `maxParameters`, `maxCyclomaticComplexity`, `maxDependencies`.
- Provide moderate defaults that reflect consensus (e.g., max nesting: 4, max method lines: 30, max parameters: 5).
- Include a `"type": "BOOLEAN"` param when the rule has an optional stricter mode.

### Debt Estimation
- Use `CONSTANT_ISSUE` for atomic fixes (adding a null check, renaming a variable, adding javadoc).
- Use `LINEAR` when the effort scales with code size or occurrence count (refactoring a 200-line method vs. a 50-line method).
- Typical offsets: documentation → `"10min"`, simple refactoring → `"15min"`–`"20min"`, structural changes → `"1h"`–`"4h"`.

### Common Pitfalls to Avoid
- Do NOT conflate maintainability with performance — a maintainability rule targets **human comprehension cost**, not runtime efficiency.
- Do NOT set severity too high — maintainability issues are important but rarely urgent. `MAJOR` is the ceiling for most.
- Do NOT write rules that are purely subjective without configurable thresholds — expose the threshold as a `param`.
- Do NOT duplicate concerns already covered by code-smells rules — maintainability rules focus on **readability and change safety**, while code-smells focus on **design pattern violations**.
- Do NOT omit the maintenance scenario — always explain *when* this becomes a problem (during review, during debugging, during onboarding).

---

## When Creating New Maintainability Rules

1. Verify the issue is about **long-term code health**, not a one-time design flaw (that belongs in code-smells) or a runtime issue (that belongs in performance).
2. Ensure the rule targets a pattern that **gets worse over time** if not addressed — maintainability debt compounds.
3. Name the `key` after the symptom developers experience (e.g., `"shotgun-surgery"`, `"deep-nesting"`) rather than the fix.
4. Include `params` with sensible defaults — maintainability standards are team-specific.
5. Describe both the **immediate cost** (harder to read) and the **compounding cost** (harder to modify safely at scale).

---

## Distinguishing from Code Smells

Maintainability rules overlap with code smells but have a distinct focus:
- **Maintainability** → "Can the next developer understand and safely change this?" (readability, clarity, documentation, dependency transparency)
- **Code Smells** → "Does this violate proven design principles?" (SRP, DRY, YAGNI, encapsulation, coupling/cohesion)

When in doubt: if the primary victim is the **reader/modifier** → maintainability. If the primary violation is a **design principle** → code-smell.

---

## Existing Rules Reference

boolean-blindness, circular-dependencies, deep-nesting, excessive-comments, hardcoded-urls, hidden-dependencies, inconsistent-naming, long-methods, missing-javadoc, missing-null-check, mutable-static-state, race-condition, shotgun-surgery, swallowed-exceptions, too-many-parameters
