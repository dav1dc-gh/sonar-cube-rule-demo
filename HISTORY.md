# Lessons Learned

## 2026-02-23 — Initial setup of lessons-learned protocol

**What was done:** Created `.github/copilot-instructions.md` with a directive requiring the assistant to append a "Lessons Learned" entry to `HISTORY.md` at the end of every response, and to read `HISTORY.md` at the start of every new task.

**What worked:** Straightforward file creation — no existing custom instructions or HISTORY.md to conflict with.

**What failed:** Nothing.

**Why:** This protocol ensures institutional memory across conversations. By recording what worked, what failed, and the reasoning behind decisions, the assistant can avoid repeating mistakes and build on past successes without relying on conversation history.

## 2026-02-23 — Generated comprehensive custom instructions from repo contents

**What was done:** Replaced the minimal `.github/copilot-instructions.md` (which only had the lessons-learned protocol) with a full set of custom instructions covering: repo overview, directory structure, all four rule categories with their contents, the complete rule JSON schema (required and optional fields), two annotated examples (minimal rule and rule with params), best practices for creating/modifying rules, and the lessons-learned protocol.

**What worked:** Reading the README, sampling one rule from each category (sql-injection, god-class, n-plus-one-query, deep-nesting), and examining the existing README gave a complete picture of the repo's conventions. The two examples chosen (one without params, one with) cover both rule shapes that exist in the repo.

**What failed:** Nothing.

**Why:** A comprehensive instructions file means the assistant can orient itself immediately in any future conversation without needing to re-explore the repo. The structure mirrors the README but adds prescriptive guidance (severity calibration, tag conventions, JSON schema table) that a README wouldn't typically include. The lessons-learned protocol was preserved at the end to maintain the directive from the prior task.

## 2026-02-23 — Generated path-specific custom instructions for all four rule categories

**What was done:** Created `.copilot-instructions.md` files in each of the four `rules/` subdirectories:
- `rules/security/.copilot-instructions.md` — 15 rules, VULNERABILITY-only guidance, OWASP tagging, severity/type conventions, remediation cost calibration.
- `rules/code-smells/.copilot-instructions.md` — 13 rules, design-principle cross-references (SOLID, DRY, Law of Demeter, YAGNI), LINEAR vs CONSTANT_ISSUE debt guidance, overlap warnings with maintainability.
- `rules/performance/.copilot-instructions.md` — 12 rules, BUG vs CODE_SMELL type decision tree, resource-domain tagging, concurrency context notes.
- `rules/maintainability/.copilot-instructions.md` — 12 rules, relationship table distinguishing from code-smells, parameter threshold conventions, BUG exception for missing-null-check.

Each file includes: category conventions table, complete rule inventory with key metadata, creation guidance, cost calibration, and common pitfalls.

**What worked:** Reading all 52 rule files in parallel batches (6 at a time) gave complete metadata for accurate inventory tables. Analyzing cross-category patterns (e.g., long-parameter-list vs too-many-parameters overlap, BUG type usage in non-security categories) added unique value beyond what generic instructions would provide. The type decision tree for performance rules was a useful synthesis.

**What failed:** Nothing.

**Why:** Path-specific instructions ensure the assistant gets category-appropriate guidance automatically when working in a particular directory, without needing to parse the entire root-level instructions. Each file is self-contained with its own severity calibration, type conventions, and pitfall warnings tailored to that specific category. The root `.github/copilot-instructions.md` was left unchanged since it already covers the global schema and cross-category concerns — the path-specific files complement it without duplication.

## 2026-02-23 — Long-term maintainability improvements: schema, validation, CI, catalog

**What was done:** Comprehensive audit of all 52 rule files and implementation of six maintainability improvements:

1. **JSON Schema** (`schema/sonarqube-rule.schema.json`) — Formal JSON Schema (draft-07) defining all required/optional fields, enum constraints, regex patterns for keys/tags, and conditional debt validation (CONSTANT_ISSUE requires offset, LINEAR requires coefficient). Enables IDE autocompletion and inline validation.

2. **Validation script** (`scripts/validate-rules.js`) — Node.js CLI tool that checks all rules for: valid JSON, required fields, enum values, key-filename match, severity-defaultSeverity consistency, tag format, remediation examples, impact validity, debt structure, duplicate keys across the repo, and category conventions. Supports `--verbose` flag. Exit code 1 on errors for CI.

3. **Catalog generator** (`scripts/generate-catalog.js`) — Generates `RULES_CATALOG.md` with: summary table (rules per category by severity), full rule table with links, and per-rule detail sections. Provides a single-file overview of all 52 rules without opening individual JSONs.

4. **GitHub Actions CI** (`.github/workflows/validate-rules.yml`) — Runs on every push/PR touching `rules/`, `schema/`, or `scripts/`. Validates JSON syntax, runs the validator, checks key-filename consistency. On main branch pushes, auto-generates and commits the catalog.

5. **Rule fixes:**
   - `shotgun-surgery.json`: Added missing `"offset": "0min"` to LINEAR debt (was the only LINEAR rule without it).
   - `open-redirect.json`: Replaced incorrect `"injection"` tag with `"redirect"` (open redirects are not injection attacks).

6. **package.json** — Added convenience scripts: `npm run validate`, `npm run catalog`, `npm run check`.

**What worked:** The full audit caught the shotgun-surgery debt inconsistency and the open-redirect tag misclassification — both would have gone unnoticed without systematic checking. The validation script correctly catches all the issues when intentionally broken.

**What failed:** Nothing.

**Why:** A rule-definition repo without automated validation will accumulate inconsistencies as it grows. The schema provides IDE-time feedback, the validator catches issues the schema can't express (like key-filename matching), the CI prevents broken rules from merging, and the catalog gives contributors a quick overview without needing to `grep` across 52 files. These four layers — schema, script, CI, catalog — form a defense-in-depth approach to repo quality.

## 2026-02-23 — Full audit of all 52 rule JSON files

**What was done:** Read and validated all 52 rule JSON files across all four category directories (security/15, code-smells/13, maintainability/12, performance/12). Checked: JSON syntax via `jq`, key-filename match, severity-defaultSeverity match, required fields, remediation examples, impacts validity, debt structure, tag-category alignment, and cross-sibling consistency.

**What worked:** Batch-reading files in parallel (8 at a time) was efficient — 4 rounds covered all 52 files. Using `jq` in terminal for JSON validation and bulk metadata extraction confirmed no syntax errors. The systematic per-check approach caught the shotgun-surgery missing offset that a spot-check would miss.

**What failed:** Nothing failed, but the audit revealed: (1) shotgun-surgery.json has LINEAR debt missing `offset` field, (2) long-parameter-list and too-many-parameters are near-duplicates across categories with conflicting severity/threshold, (3) open-redirect is mis-tagged as "injection", (4) performance rules have an inconsistent MAINTAINABILITY vs RELIABILITY split in impacts, (5) 4 files have only 3 tags while the norm is 4.

**Why:** A full audit establishes baseline quality and catches drift that accumulates as rules are added independently. The structured report with summary tables provides a reference for future rule additions. The recommendations prioritize the one definite bug (missing offset) over the stylistic inconsistencies.

## 2026-02-23 — Implemented Copilot agent skills and custom agents for routine operations

**What was done:** Created a full operational automation layer for the repository using Copilot agent skills and custom agents:

**4 Skills** (`.github/skills/`):
1. `rule-creation-wizard` — Guided new rule creation with `SKILL.md` + `validate-new-rule.sh`
2. `data-quality-audit` — Deep consistency analysis with `SKILL.md` + `audit-rules.js` (detects near-duplicates via Jaccard similarity, impact misclassifications, tag issues, cost outliers)
3. `catalog-index-refresh` — Catalog and machine-readable index generation with `SKILL.md` + `generate-index.js` (produces `rules/index.json`)
4. `custom-instructions-sync` — Drift detection between rule files and `.copilot-instructions.md` files with `SKILL.md` + `detect-drift.js`

**3 Agents** (`.github/agents/`):
1. `rule-author` — Composes skills into an end-to-end rule creation workflow (tools: read, edit, search, execute)
2. `repo-auditor` — Read-only audit agent that reports but never modifies files (tools: read, search, execute — no edit)
3. `repo-maintainer` — Phased maintenance agent that assesses → fixes with confirmation → regenerates artifacts → syncs instructions → verifies (tools: read, edit, search, execute)

**Supporting changes:**
- Added `npm run audit`, `npm run index`, `npm run drift` scripts to `package.json`
- Updated `npm run check` to include index generation
- Generated `rules/index.json` with all 52 rules
- Updated `README.md` with Copilot Agents and Copilot Skills documentation sections

**What worked:** All 4 scripts run cleanly. The audit script correctly identified 21 warnings and 11 suggestions (near-duplicates, impact misclassifications in performance rules, first-tag mismatches in code-smells, tag count variance, cost outliers). The drift detector initially had false positives from schema field names (`type`, `severity`, `tags`) appearing in instruction files — fixed by adding a non-rule term exclusion list and requiring keys to contain hyphens. A second false positive (cross-category reference to `hardcoded-credentials` in maintainability instructions) was fixed by building a global rule key set and skipping "removed" entries that exist in other categories.

**What failed:** The drift detector's regex approach produced false positives on the first run. Two fixes were needed: (1) exclude known schema field names and single-word terms, (2) skip cross-category references from the "removed" list. These fixes made the output accurate (0 drift for all 4 categories).

**Why:** Skills + agents provide a sustainable operational model. Skills auto-load when Copilot detects relevant tasks; agents give team members one-click access to common workflows via the Copilot dropdown. The read-only auditor agent is deliberately separated from the maintainer agent to allow safe assessment without risk of unintended changes — important for a small team where someone might want to review before fixing. Bundled Node.js scripts give Copilot deterministic, parseable output (JSON findings, counts) rather than relying on it to manually read 52+ files each time.
