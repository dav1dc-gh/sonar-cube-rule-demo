---
applyTo: "rules/code-smells/**"
---

# Code Smells Rules — Path-Specific Custom Instructions

You are working inside `rules/code-smells/`, which contains **13 SonarQube rule definitions** that detect design and quality problems in application code. These rules flag patterns that aren't bugs or vulnerabilities but erode maintainability, readability, and testability over time.

---

## Purpose of This Category

Code smell rules identify anti-patterns rooted in poor object-oriented design, duplication, excessive complexity, and violation of fundamental principles (SOLID, DRY, Law of Demeter, YAGNI). They help teams keep technical debt visible and manageable. Every rule in this directory has `"type": "CODE_SMELL"`.

---

## Current Rules Inventory (13 rules)

| File | Key | Severity | Debt Model | Params? | What It Detects |
|---|---|---|---|---|---|
| `complex-methods.json` | `complex-methods` | MAJOR | LINEAR (1min/unit) | `threshold` (15) | Methods with high cyclomatic complexity |
| `data-clumps.json` | `data-clumps` | MINOR | CONSTANT (30min) | — | Groups of variables that always appear together across methods |
| `dead-code.json` | `dead-code` | MINOR | CONSTANT (5min) | — | Unreachable code, unused variables, methods, or classes |
| `duplicate-code.json` | `duplicate-code` | MAJOR | CONSTANT (15min) | — | Copy-pasted or structurally identical code blocks |
| `empty-catch-block.json` | `empty-catch-block` | MAJOR | CONSTANT (10min) | — | Catch blocks that silently swallow exceptions |
| `feature-envy.json` | `feature-envy` | MINOR | CONSTANT (20min) | — | Methods that use other classes' features more than their own |
| `god-class.json` | `god-class` | MAJOR | LINEAR (10min/unit) | `maxLines` (500), `maxMethods` (20) | Oversized classes violating Single Responsibility |
| `long-parameter-list.json` | `long-parameter-list` | MINOR | CONSTANT (30min) | `maxParams` (5) | Methods with too many parameters |
| `magic-numbers.json` | `magic-numbers` | MINOR | CONSTANT (5min) | — | Unnamed numerical constants in code |
| `message-chains.json` | `message-chains` | MINOR | CONSTANT (20min) | `maxChainLength` (3) | Long method-call chains (Law of Demeter violation) |
| `primitive-obsession.json` | `primitive-obsession` | MINOR | CONSTANT (30min) | — | Overuse of primitives instead of domain value objects |
| `refused-bequest.json` | `refused-bequest` | MAJOR | CONSTANT (45min) | — | Subclasses that nullify inherited behavior (LSP violation) |
| `speculative-generality.json` | `speculative-generality` | MINOR | CONSTANT (20min) | — | Unused abstractions built for hypothetical futures (YAGNI) |

---

## Category-Specific Conventions

### Type & Severity Patterns

- **Type** is always `"CODE_SMELL"` — no exceptions. If a code smell has reliability implications (e.g., empty catch blocks hiding errors), it's still `CODE_SMELL` in this directory — the `impacts` field captures the reliability aspect.
- **Severity** follows a clear split:
  - `MAJOR` for issues with significant structural impact: `complex-methods`, `duplicate-code`, `empty-catch-block`, `god-class`, `refused-bequest`.
  - `MINOR` for lower-impact style/design issues: `data-clumps`, `dead-code`, `feature-envy`, `long-parameter-list`, `magic-numbers`, `message-chains`, `primitive-obsession`, `speculative-generality`.
- Never use `BLOCKER` or `CRITICAL` for code smells — those are reserved for security and critical bugs.

### Impacts

- `softwareQuality` is almost always `"MAINTAINABILITY"`. The one exception is `empty-catch-block` which uses `"RELIABILITY"` because swallowed exceptions cause silent failures.
- `severity` ranges from `"LOW"` (naming, dead code, magic numbers) through `"MEDIUM"` (complexity, duplication, primitive obsession, refused bequest) to `"HIGH"` (god class).

### Tags

- Always include `"code-smell"` as the first tag.
- Add design-principle tags when applicable: `"solid"`, `"dry-principle"`, `"law-of-demeter"`, `"yagni"`, `"lsp"`.
- Add concern tags: `"design"`, `"refactoring"`, `"complexity"`, `"readability"`, `"error-handling"`, `"oop"`.
- Include `"maintainability"` or `"testing"` when the smell directly hampers those qualities.

### Debt Model

This category uses **both** debt models:

- **`CONSTANT_ISSUE`** (11 of 13 rules): Each occurrence costs a fixed time. Used when a single fix resolves the smell regardless of size (e.g., renaming a magic number, removing dead code).
- **`LINEAR`** (2 rules: `complex-methods`, `god-class`): Cost scales with a measurable unit. The `coefficient` represents per-unit cost (1min per complexity point, 10min per excess method/line). The `offset` is `"0min"` for both.

When choosing between models for a new rule:
- If the rule flags something binary (present or absent), use `CONSTANT_ISSUE`.
- If the rule measures a quantity where each additional unit adds marginal fix cost, use `LINEAR`.

### Configurable Parameters (`params`)

4 of 13 rules have `params` — this is the highest ratio in any category. Code smell rules often have tunable thresholds:

| Rule | Param | Default | What It Controls |
|---|---|---|---|
| `complex-methods` | `threshold` | 15 | Max cyclomatic complexity |
| `god-class` | `maxLines` | 500 | Max lines per class |
| `god-class` | `maxMethods` | 20 | Max methods per class |
| `long-parameter-list` | `maxParams` | 5 | Max parameters per method |
| `message-chains` | `maxChainLength` | 3 | Max chained method calls |

When adding a new rule, include `params` only if the rule has a clear numeric threshold that teams may want to adjust.

### Remediation Examples

- Show the anti-pattern in `before` and the refactored design in `after`.
- Use realistic OOP examples — classes, methods, inheritance hierarchies.
- Comments in examples should explain the design principle being applied (e.g., "Single Responsibility", "Extract Class", "Replace Conditional with Polymorphism").
- Keep examples minimal but representative — don't show full classes when a method snippet suffices.

---

## Guidelines for Creating New Code Smell Rules

1. **Check for overlap**: Several existing rules are related (e.g., `long-parameter-list` vs `data-clumps`, `god-class` vs `complex-methods`). Make sure the new rule detects a distinct pattern.
2. **Name after the established refactoring term**: Use well-known names from Fowler's "Refactoring" catalog when possible (e.g., Feature Envy, Shotgun Surgery, Data Clumps).
3. **Default thresholds should be mainstream**: Use values that align with industry standards (cyclomatic complexity 15, method length 100 lines, parameters 5–7).
4. **Link to design principles**: Reference SOLID, DRY, YAGNI, Law of Demeter, or other principles in the description to give context for _why_ it matters.
5. **Remediation examples should show refactoring techniques**: Extract Method, Extract Class, Replace Primitive with Object, Introduce Parameter Object, etc.

---

## Common Pitfalls to Avoid

- **Don't use `"type": "VULNERABILITY"` or `"type": "BUG"`** — everything here is `CODE_SMELL`.
- **Don't set severity to BLOCKER or CRITICAL** — code smells are structural issues, not emergencies.
- **Don't provide `LINEAR` debt without `coefficient`** — if using LINEAR, both `coefficient` and `offset` are required.
- **Don't add `params` without a clear threshold** — boolean-style detections (dead code exists or doesn't) shouldn't have params.
- **Don't mix this category with performance** — if the primary concern is CPU/memory/I/O, it belongs in `rules/performance/` even if it's typed as `CODE_SMELL`.
