---
applyTo: "rules/code-smells/**/*.json"
description: "Authoring and review guidance for SonarQube code-smell (CODE_SMELL) rules."
---

# Code-Smell Rules — Custom Instructions

Scope: every JSON file under `rules/code-smells/`. These rules flag **design and code-quality smells** — code that compiles and runs correctly today but is fragile, opaque, or expensive to change.

> Read [sonarqube-rules.instructions.md](.github/instructions/sonarqube-rules.instructions.md) first for the shared schema. This file only documents what is **specific to code-smell rules**.

## 1. Mandatory field values

| Field | Required value for this category |
|---|---|
| `type` | `CODE_SMELL`. Never `VULNERABILITY` here; never `BUG` (a smell is by definition not a defect — if the code is wrong, file it elsewhere). |
| `severity` / `defaultSeverity` | `MAJOR` by default. `CRITICAL` only for smells that almost always indicate a deeper architectural problem (`god-class`, severe `complex-methods`). `MINOR` for stylistic/naming smells. Avoid `BLOCKER` and `INFO`. |
| `impacts` | Must include `{ "softwareQuality": "MAINTAINABILITY", "severity": "..." }`. Add `RELIABILITY: MEDIUM` for smells that statistically produce bugs (`empty-catch-block`, `dead-code`, `refused-bequest`). |
| `status` | `READY`. |
| `debt.function` | `LINEAR` is preferred for size/complexity smells (`god-class`, `long-parameter-list`, `complex-methods`, `duplicate-code`, `message-chains`). `CONSTANT_ISSUE` for site-local smells (`empty-catch-block`, `magic-numbers` per occurrence). |
| `debt.coefficient` (LINEAR) | `2min`–`10min` per unit (per line, per parameter, per duplicated block, per cyclomatic point). |
| `debt.offset` (CONSTANT_ISSUE) | `5min`–`30min`. Empty catch blocks ≈ `5min`; extracting magic numbers ≈ `10min`. |

## 2. Required tags

Every code-smell rule must include, in this order:

1. `"code-smell"` — the category tag.
2. A **design lens** the smell violates: `"solid"` (SRP/OCP/LSP/ISP/DIP), `"dry"`, `"kiss"`, `"yagni"`, `"cohesion"`, `"coupling"`, `"abstraction"`.
3. A **smell family** when applicable: `"bloater"` (god-class, long-method, long-parameter-list, primitive-obsession, data-clumps), `"object-orientation-abuser"` (refused-bequest, switch-statements), `"change-preventer"` (shotgun-surgery, divergent-change), `"dispensable"` (dead-code, duplicate-code, speculative-generality, excessive-comments), `"coupler"` (feature-envy, message-chains, inappropriate-intimacy).
4. Optional cross-cutting tag `"maintainability"` when the smell's primary cost is upkeep.

Do **not** tag with security/performance unless the smell genuinely also causes those problems — keep categories crisp.

## 3. Description guidance

- One or two sentences. State the **structural pattern** that is detected and the **design principle** it violates.
- Name the threshold inline when the rule has one (e.g., "classes exceeding 500 lines or 20 methods"), and make sure the matching `params.defaultValue` agrees.
- Avoid moralizing ("bad code", "you should know better"). State the consequence: "harder to understand", "increases change cost", "obscures intent".

Good: *"Detects classes that have grown too large and handle too many responsibilities, violating the Single Responsibility Principle and making the code difficult to understand and maintain."*

Bad: *"God classes are evil and should be banned from your codebase."*

## 4. `remediation.examples` rules

- Code-smell rules are typically **structural**. A short comment placeholder describing the bad shape and the refactored shape is acceptable when a literal snippet would be misleadingly small (`god-class`, `long-methods`, `shotgun-surgery`). Match the existing in-repo style:
  - Before: `"// Class with 2000+ lines handling user management, email, reporting, and file operations"`
  - After: `"// Split into UserService, EmailService, ReportingService, and FileService classes"`
- For **site-local** smells (`empty-catch-block`, `magic-numbers`, `message-chains`, `data-clumps`), provide a **literal** before/after snippet. Vague comments are not acceptable when a concrete example fits in 6 lines.
- After snippets should reference the **named refactoring** that fixes the smell (Extract Method, Extract Class, Replace Magic Number with Symbolic Constant, Introduce Parameter Object, Replace Conditional with Polymorphism, Pull Up Method, Hide Delegate). When space permits, mention the refactoring by name.

## 5. `params` policy

Code-smell rules are the **most parameter-heavy** category, because thresholds are inherently project-dependent. Define `params` whenever the rule has a numeric cutoff. Conventions:

- Use `INTEGER` for counts and `defaultValue` as a string.
- Standard keys: `maxLines`, `maxMethods`, `maxParameters`, `maxComplexity`, `maxNestingLevel`, `maxFields`, `minDuplicatedLines`.
- Defaults should match widely cited guidance: methods ≤ 100 lines, parameters ≤ 5–7, cyclomatic complexity ≤ 10–15, class lines ≤ 500, methods per class ≤ 20, duplicated blocks ≥ 6 lines.
- Do **not** add a parameter that disables the rule entirely — use `severity` or `status` for that.

## 6. Review checklist

Before approving any change under `rules/code-smells/`:

- [ ] `type` is `CODE_SMELL` and severity is `MAJOR` (or `CRITICAL`/`MINOR` with justification).
- [ ] Impacts include `MAINTAINABILITY` at an appropriate severity.
- [ ] Tags include `code-smell` + a design lens (SOLID/DRY/etc.) + smell family.
- [ ] Description cites the threshold; if the rule is tunable, the threshold matches `params.defaultValue`.
- [ ] Before/after example uses a comment placeholder only when a literal snippet would be unhelpfully small; otherwise it shows real code.
- [ ] After example references a named refactoring when one applies.
- [ ] `key` matches the filename and is kebab-case.
- [ ] Debt model fits the rule shape: `LINEAR` for size/complexity, `CONSTANT_ISSUE` for site-local.

## 7. Anti-patterns to flag in review

- `type: VULNERABILITY` or `BUG` on a smell — wrong category; move the rule or change the type.
- Severity `BLOCKER` — too aggressive for a smell; use `CRITICAL` at most.
- Missing `params` on a threshold-based rule — every team will fight you about the number; make it tunable.
- Mismatched threshold between `description` text and `params.defaultValue` — pick one source of truth and align.
- Using `CONSTANT_ISSUE` for `god-class`/`long-methods` — remediation cost scales with size; use `LINEAR`.
- Tags that overlap with security/performance categories without a clear cross-cutting reason.
