---
applyTo: "rules/maintainability/**/*.json"
description: "Authoring and review guidance for SonarQube maintainability rules (readability, modularity, change cost)."
---

# Maintainability Rules — Custom Instructions

Scope: every JSON file under `rules/maintainability/`. These rules target **long-term cost of change** — readability, naming, documentation, coupling, and the friction a future engineer will feel touching this code.

> Read [sonarqube-rules.instructions.md](.github/instructions/sonarqube-rules.instructions.md) first for the shared schema. This file only documents what is **specific to maintainability rules**.

## 2. Maintainability vs. code-smells — pick the right home

This is the most common mis-categorization in the repo. Use this split:

- `rules/code-smells/` → the code has a **named structural anti-pattern** (god class, feature envy, primitive obsession, message chains, refused bequest, data clumps).
- `rules/maintainability/` → the code has a **readability, documentation, naming, coupling, or null-safety friction** that increases the cost of future change without necessarily matching a classic smell name (deep nesting, inconsistent naming, missing javadoc, hardcoded URLs, hidden dependencies, missing null checks, shotgun surgery, too many parameters, boolean blindness, excessive comments, circular dependencies, long methods).

When in doubt: if the fix is a **rename / extract / document / inject / null-guard**, it belongs here. If the fix is a **named refactoring** of structure, it belongs in `code-smells/`.

## 1. Mandatory field values

| Field | Required value for this category |
|---|---|
| `type` | `CODE_SMELL`. Never `VULNERABILITY`. Use `BUG` only for `missing-null-check` style rules where the absence of the check is a demonstrable defect, not just a smell. |
| `severity` / `defaultSeverity` | `MAJOR` by default. `MINOR` for stylistic rules (`inconsistent-naming`, `excessive-comments`, `missing-javadoc` on non-public APIs). `CRITICAL` only for `circular-dependencies` and `shotgun-surgery` where change-amplification is severe. Avoid `BLOCKER` and `INFO`. |
| `impacts` | Must include `{ "softwareQuality": "MAINTAINABILITY", "severity": "..." }`. Add `RELIABILITY: MEDIUM` for `missing-null-check` and `hidden-dependencies` (both produce real defects). |
| `status` | `READY`. |
| `debt.function` | `LINEAR` for rules whose cost scales (`long-methods`, `deep-nesting`, `too-many-parameters`, `excessive-comments`, `missing-javadoc` across many APIs). `CONSTANT_ISSUE` for site-local fixes (`hardcoded-urls`, `missing-null-check`, `boolean-blindness` per call). |
| `debt.coefficient` (LINEAR) | `1min`–`5min` per unit (per excess line, per nesting level, per excess parameter). |
| `debt.offset` (CONSTANT_ISSUE) | `5min`–`30min`. Externalizing one URL ≈ `10min`; adding a null guard ≈ `5min`; introducing a parameter object ≈ `30min`. |

## 3. Required tags

Every maintainability rule must include, in this order:

1. `"maintainability"` — the category tag.
2. A **friction lens** the rule reduces: `"readability"`, `"naming"`, `"documentation"`, `"coupling"`, `"cohesion"`, `"modularity"`, `"null-safety"`, `"configurability"`, `"testability"`, `"change-cost"`.
3. A **specific concern** when applicable: `"javadoc"`, `"nesting"`, `"parameters"`, `"method-length"`, `"hardcoded"`, `"dependency-injection"`, `"cyclic-dependency"`.
4. Optional **scope tag**: `"public-api"` when the rule applies only to externally visible code (common for `missing-javadoc`).

Do not add `"security"`, `"performance"`, or `"code-smell"` tags — keep this category about long-term change cost.

## 4. Description guidance

- One or two sentences. State **what is detected**, then **what future-engineer pain it causes** (re-reading time, onboarding cost, silent NPEs, ripple-effect changes, hidden coupling).
- Cite thresholds inline when present (lines, parameters, nesting depth) and align them with `params.defaultValue`.
- Prefer change-cost language ("harder to test in isolation", "obscures the contract", "amplifies the blast radius of changes") over aesthetic language ("ugly", "messy").

Good: *"Detects methods or functions that exceed a reasonable length threshold, making them harder to understand and maintain. Long methods should be refactored into smaller, focused units."*

Bad: *"Long methods are ugly and nobody likes reading them."*

## 5. `remediation.examples` rules

- For threshold-based structural rules (`long-methods`, `deep-nesting`, `too-many-parameters`), a comment placeholder describing the bad shape and the refactored shape is acceptable and matches existing in-repo style.
- For site-local rules, prefer a **literal** before/after snippet:
  - `hardcoded-urls` → before: `String url = "https://api.example.com/v1";` / after: read from config (`@Value("${api.base-url}")` / `System.getenv` / properties file).
  - `missing-null-check` → before: dereferencing a parameter directly; after: `Objects.requireNonNull(...)` or `Optional` chain.
  - `boolean-blindness` → before: `service.send(true, false, true)`; after: introduce an enum, named record, or builder.
  - `inconsistent-naming` → before/after pair showing the convention being enforced (camelCase, no Hungarian prefixes, etc.).
  - `hidden-dependencies` → before: `new Foo()` inside a method; after: constructor-injected `Foo` field.
  - `circular-dependencies` → comment placeholder explaining the cycle and the mediator/inversion that breaks it.
  - `shotgun-surgery` → comment placeholder describing the scattered change set and the consolidation (extract module, introduce a single point of change).
  - `excessive-comments` → before: code overlaid with redundant `//` comments; after: same code with intent-revealing names so the comments become unnecessary.
  - `missing-javadoc` → before: public method with no doc; after: minimal `/** ... @param ... @return ... @throws ... */` block.

## 6. `params` policy

Maintainability rules are heavily threshold-driven. Define `params` whenever a number governs the rule:

- `max` / `maxLines` / `maxNestingLevel` / `maxParameters` / `maxBooleanParameters` (INTEGER).
- `commentRatio` (FLOAT) for `excessive-comments`.
- `requireForVisibility` (STRING enum: `"public"`, `"protected"`, `"package"`) for `missing-javadoc`.
- Defaults to align with: methods ≤ 100 lines, nesting depth ≤ 3, parameters ≤ 5–7, boolean parameters ≤ 1.

Do **not** add a parameter that lets users disable enforcement on whole packages — that is a quality-profile concern, not a rule-definition concern.

## 7. Review checklist

Before approving any change under `rules/maintainability/`:

- [ ] `type` is `CODE_SMELL` (or `BUG` with justification, e.g., `missing-null-check`).
- [ ] Severity is `MAJOR` by default; `CRITICAL` only for change-amplifying rules; `MINOR` for stylistic ones.
- [ ] Impacts include `MAINTAINABILITY`; `RELIABILITY: MEDIUM` is added for null-safety / hidden-dependency rules.
- [ ] Tags include `maintainability` + a friction lens + a specific concern.
- [ ] If threshold-based, `params.defaultValue` matches the threshold cited in `description`.
- [ ] Site-local rules show literal code in the example; structural rules may use a comment placeholder.
- [ ] `key` matches the filename and is kebab-case.
- [ ] Debt model: `LINEAR` for size/nesting/parameter overruns; `CONSTANT_ISSUE` for site-local fixes.
- [ ] The rule does **not** belong in `code-smells/` (no named structural anti-pattern fits better).

## 8. Anti-patterns to flag in review

- Putting a classic smell (`god-class`, `feature-envy`, `primitive-obsession`) here instead of `code-smells/`.
- Severity `BLOCKER` — disproportionate for change-cost rules.
- `missing-javadoc` rule that fires on private methods by default — too noisy; default to `public` visibility.
- Threshold-based rule with no `params` — guarantees pushback from teams.
- `after` snippet that adds more comments to fix a readability problem — usually the wrong direction; recommend renaming and extracting instead.
- Treating `circular-dependencies` as `MINOR` — it blocks modularization and should be at least `MAJOR`.
- Adding `"security"` or `"performance"` tags here without a strong cross-cutting reason.
