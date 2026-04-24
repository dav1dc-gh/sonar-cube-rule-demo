# AI History — Lessons Learned

This file records what worked, what failed, and why decisions were made across assistant sessions. Read this file at the start of every new task.

---

## 2026-04-24 — Initial setup of lessons-learned workflow

**Task**: Create the custom instructions file and `AI-HISTORY.md` per the `lessons-learned.prompt.md` directive.

**What worked**:
- Searched for existing `copilot-instructions.md` and `AI-HISTORY.md` before creating to avoid clobbering.
- Placed instructions at `.github/copilot-instructions.md` (the standard VS Code Copilot location).

**What failed**:
- Nothing this session.

**Why**:
- `.github/copilot-instructions.md` is auto-loaded by Copilot in VS Code, making it the correct home for repo-wide guidance.
- Kept the instructions short and actionable rather than prescriptive about format, so future entries stay flexible.

**Improvement notes**:
- Future entries should reference specific files/rules touched so patterns become discoverable.

---

## 2026-04-24 — Generated comprehensive SonarQube rules custom instructions

**Task**: Execute `.github/prompts/gen-custom-instructions.prompt.md` — produce a single comprehensive instructions file covering overview, directory structure, categories, rule schema, and best practices.

**What worked**:
- Sampled one representative rule from each category (`security/sql-injection`, `code-smells/god-class`, `maintainability/long-methods`, `performance/n-plus-one-query`, `security/hardcoded-credentials`) plus the existing `README.md` to derive an accurate schema with both `CONSTANT_ISSUE` and `LINEAR` debt shapes and a tunable-`params` example.
- Created `.github/instructions/sonarqube-rules.instructions.md` with `applyTo: "rules/**/*.json"` frontmatter so the guidance is auto-attached when working on rule files (modern VS Code instructions pattern), instead of appending to the global `copilot-instructions.md` and bloating its always-on context.

**What failed**:
- Nothing this session.

**Why**:
- Scoping via `applyTo` keeps the always-loaded instructions lean while still surfacing the SonarQube guidance precisely when rule JSON files are in context.
- Including a canonical full example (SQL injection) plus a per-section schema table makes the file usable both as a reference and as a copy-paste starting point.

**Improvement notes**:
- If/when rule files in this repo start using fields outside the documented schema, revise the "What to Avoid" section rather than silently expanding the schema table.

---

## 2026-04-24 — Generated path-based custom instructions for each rule category

**Task**: Execute `.github/prompts/gen-path-based-custom-instructions.prompt.md` — produce one path-scoped instructions file per major `rules/` subdirectory (security, code-smells, performance, maintainability).

**What worked**:
- Created four sibling files in `.github/instructions/`, each with `applyTo` scoped to its subdirectory glob (`rules/security/**/*.json`, etc.) so each set is auto-attached only when editing files in that category.
- Each file explicitly defers to the existing `sonarqube-rules.instructions.md` for the shared schema and only documents what is *unique* to its category — avoids duplication and keeps the always-loaded global instructions lean.
- Used a consistent five-section spine (mandatory field values table, required tags, description guidance, examples policy, params policy, review checklist, anti-patterns) so the four files feel like a coherent set rather than four ad-hoc documents.
- Differentiated each file with category-specific content: security got CWE/OWASP id mappings and "never let params weaken the rule"; code-smells got the design-lens / smell-family taxonomy and named-refactoring guidance; performance got resource/mechanism tags and the canonical optimization for each anti-pattern; maintainability got an explicit "maintainability vs. code-smells — pick the right home" decision rule that addresses the most likely mis-categorization.

**What failed**:
- Nothing this session.

**Why**:
- Path-scoped `applyTo` globs are the right VS Code mechanism for category-specific guidance — they avoid bloating context for unrelated edits while still firing precisely when needed.
- The "decision rule" section in the maintainability file pre-empts the genuinely ambiguous boundary between code-smells and maintainability, which the existing file structure does not clarify.

**Improvement notes**:
- If a fifth category is added under `rules/`, follow the same template: defer to the shared instructions, then document field defaults, tags, description style, examples policy, params policy, checklist, and anti-patterns specific to that category.

---

## 2026-04-24 — Maintainability recommendations plan (no changes made)

**Task**: Execute `.github/prompts/ask-for-help.prompt.md` — propose long-term maintainability improvements without modifying the repo.

**What worked**:
- Re-read the existing path-scoped instructions and one canonical rule before drafting recommendations, so suggestions build on what's already in place rather than duplicating it.
- Ranked recommendations by payoff and grouped them into an execution order so the user can pick a subset.

**What failed**:
- Nothing this session.

**Why**:
- User explicitly asked for a plan only, so deferred all file creation (schema, lint scripts, CI, exporter) until they choose which items to greenlight.
- Prioritized JSON Schema + `$schema` references first because they unlock IDE-level validation immediately and underpin every later check.

**Improvement notes**:
- When the user approves, start with schema + lint before touching deployment tooling — validation issues found later are cheaper to fix once the schema exists.
