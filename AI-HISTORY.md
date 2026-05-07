# AI History — Lessons Learned

<!-- agent: read only the "Summary of Key Insights" section (if present) plus the last 5 entries below. Skip older verbatim entries unless explicitly relevant. -->

This file tracks what worked, what failed, and why decisions were made across AI-assisted tasks in this repository. Read this at the start of every new task.

---

## 2026-05-06 — Auto-generated `rules/INDEX.md` + slim `README.md` + AI-HISTORY agent marker

**Task**: User approved the two follow-up suggestions: (1) move per-rule listings out of README into an auto-generated `rules/INDEX.md`, (2) add an agent marker to `AI-HISTORY.md` for partial-read guidance.

**What Worked**:
- Added `--write-index` flag to `scripts/validate-rules.py`. It scans `rules/`, groups by category, and emits a Markdown table with key, name, severity, type, and one-line description per rule. Idempotent — safe to re-run.
- Added a CI step (`Verify rules/INDEX.md is current`) that runs `--write-index` then `git diff --exit-code rules/INDEX.md`. Fails the build with a clear remediation message if the committed index is stale.
- Trimmed `README.md` from 230 → 85 lines by replacing the giant ASCII directory tree and four per-category bullet listings with a 5-line directory block and a link to `rules/INDEX.md`.
- Added an HTML comment marker at the top of `AI-HISTORY.md` instructing agents to read only the summary section + last 5 entries — belt-and-braces alongside the same instruction in `copilot-instructions.md`.

**What Failed**:
- First README replacement attempt left a `_PLACEHOLDER_REMOVED` marker because I wrote a too-narrow `oldString` that didn't extend through the entire legacy block. Had to do a follow-up replace with the full legacy content as `oldString`. Lesson: when bulk-deleting a large region, anchor the `oldString` from a unique start to a unique end rather than relying on a placeholder splice.

**Why**:
- The per-rule listings in README were the largest source of drift in the repo (already had stale counts). Generating from disk eliminates the maintenance burden entirely.
- A CI check is the only reliable enforcement — relying on contributor discipline always loses.

**Actionable Insights**:
- For any "list of things on disk" in docs, prefer a generator + CI freshness check over hand-maintained content.
- When using `replace_string_in_file` to remove a large region, prefer one big replacement with anchored start/end over splice-with-placeholder.
- `git diff --exit-code <file>` is the canonical CI pattern for "this file must match generator output".

---

## 2026-05-06 — Add token-economy guidance to `copilot-instructions.md`

**Task**: User asked for further suggestions to reduce per-prompt token usage, then approved applying them.

**What Worked**:
- Added a "Tool & output economy" section: bans re-listing `rules/`, bans `semantic_search` for rule lookups (filenames = keys), caps schema reads at once per session, forbids change-summary markdown files, forbids pasting edited JSON back in chat.
- Added a "Common task shortcuts" table mapping intents to existing subagents (`create-rule`, `audit-rules`, `document-repo`, `fix-ci`) so the agent delegates instead of chaining tool calls.
- Collapsed the 5-row severity table into one sentence (SonarQube semantics are well-known; only the BLOCKER caveat is repo-specific).
- Folded category-placement bullets into the directory-comments block they already duplicated.
- Lowered AI-HISTORY summarisation threshold from 15k/60KB to 5k/20KB and added a "last 5 entries only" read rule, since the file is loaded every task.
- Final size: 76 lines / 3.3 KB (down from original 235 lines / 11.4 KB ≈ 71% reduction overall).

**What Failed**: Nothing.

**Why**: Custom instructions ride on every prompt. Bans on expensive tool patterns (full-repo `semantic_search`, redundant `list_dir`, multi-file inline tool chains) compound over many sessions far more than the prose savings.

**Actionable Insights**:
- Prefer "don't do X, delegate to subagent Y" over re-explaining workflows.
- Treat AI-HISTORY as append-only with aggressive summarisation; instruct partial reads, not full reads.
- Look for prose that the directory tree, schema, or filenames already encode — and delete it.

---

## 2026-05-06 — Shrink `copilot-instructions.md`

**Task**: User asked to reduce the size of `.github/copilot-instructions.md` by removing obvious/redundant content.

**What Worked**:
- Deleted per-rule inventory tables (~70 lines): they duplicate the file system and drift the moment a rule is added/renamed. Replaced with "list the directory".
- Deleted full schema field documentation: pointed at the authoritative `rules/schema/sonarqube-rule.schema.json` + `rule-template.json` instead, keeping only non-obvious rules (severity sync, never-rename-keys, debt function shapes).
- Removed generic engineering platitudes ("validate JSON", "write thorough descriptions") that the schema/lint already enforce.
- Kept judgement-call content the agent actually needs: severity table and category placement heuristic.
- Result: 235 → 66 lines (~75% reduction).

**What Failed**: Nothing functional — but spotted that the old per-rule tables had become inaccurate (e.g. miscategorised rules), which is itself evidence that hard-coded inventories in instructions are an anti-pattern.

**Why**: Custom instructions are loaded into every prompt's context; bloat costs tokens on every interaction. Anything discoverable via the file system or schema doesn't belong there.

**Actionable Insights**:
- Don't enumerate filesystem contents in `copilot-instructions.md` — instruct the agent to list the directory instead.
- Don't duplicate JSON Schema fields in prose — link to the schema file.
- Reserve custom instructions for: directory layout, naming conventions, judgement calls (severity/category), and workflow rules (e.g. AI-HISTORY tracking).

---

## 2026-04-02 — Initial Setup of Lessons Learned Tracking

**Task**: Created `.github/copilot-instructions.md` and `AI-HISTORY.md` to enable continuous learning across sessions.

**What Worked**:
- Checked for existing custom instructions and history files before creating new ones to avoid overwriting work.
- Kept the custom instructions concise and actionable.

**What Failed**: Nothing — straightforward setup task.

**Why**: The prompt file `lessons-learned.prompt.md` requested this workflow to help the assistant avoid repeating mistakes and build on past successes.

**Actionable Insights**:
- Always check for existing files before creating new ones.
- Keep `AI-HISTORY.md` entries brief and focused on actionable takeaways.
- Monitor file size and summarize when it exceeds 15,000 tokens.

---

## 2026-04-02 — Generated Comprehensive Custom Instructions

**Task**: Replaced the minimal `copilot-instructions.md` with a full custom-instructions document covering overview, directory structure, all 52 rules across 4 categories, JSON schema details, severity guidelines, and best practices.

**What Worked**:
- Read representative rule files from each category (security, code-smells, performance, maintainability) to confirm the actual JSON schema before documenting it.
- Verified both `CONSTANT_ISSUE` and `LINEAR` debt models, and optional `params` fields by reading files that use them (`god-class.json`, `deep-nesting.json`).
- Preserved the existing "Lessons Learned Tracking" section at the bottom of the instructions.

**What Failed**: Nothing — the existing file was small and the prompt was clear about what to generate.

**Why**: The `gen-custom-instructions.prompt.md` prompt requested a comprehensive instructions file derived from the actual repository contents, not a generic template.

**Actionable Insights**:
- Always read real rule files to confirm schema rather than relying solely on README descriptions — `memory-leaks.json` uses type `BUG` while most performance rules use `CODE_SMELL`.
- When regenerating instructions, check for existing content to preserve (like the Lessons Learned section) to avoid losing configuration.

---

## 2026-04-02 — Generated Path-Based Custom Instructions for All Four Rule Categories

**Task**: Created four `.instructions.md` files in `.github/instructions/`, one per rule category (`security`, `code-smells`, `performance`, `maintainability`), each scoped via `applyTo` to its corresponding `rules/<category>/**` path.

**What Worked**:
- Read the agent-customization SKILL.md and its instructions reference to confirm the correct file format (`applyTo` in YAML frontmatter, placement in `.github/instructions/`).
- Examined representative rule files from each category (sql-injection, hardcoded-credentials, xss-vulnerability, god-class, empty-catch-block, n-plus-one-query, memory-leaks, deep-nesting, inconsistent-naming) to derive category-specific constraints from real data.
- Key differentiators discovered per category:
  - **Security**: Always `VULNERABILITY`, always `CRITICAL`/`BLOCKER`, no params, `CONSTANT_ISSUE` debt only.
  - **Code Smells**: Always `CODE_SMELL`, often `MAJOR`, frequently has `params`, supports `LINEAR` debt for size-dependent issues.
  - **Performance**: Mixed `CODE_SMELL`/`BUG` (only `memory-leaks` is `BUG`), impact can be `RELIABILITY` or `MAINTAINABILITY`.
  - **Maintainability**: Always `CODE_SMELL`, `MAJOR`/`MINOR` only (never `CRITICAL`), threshold-based params common.

**What Failed**: Nothing — the skill reference was clear on the format.

**Why**: The prompt `gen-path-based-custom-instructions.prompt.md` requested category-specific instructions, so each file needed unique guidance reflecting actual patterns found in the existing rules.

**Actionable Insights**:
- Path-based instructions use `applyTo` in YAML frontmatter and live in `.github/instructions/`.
- Include a keyword-rich `description` for on-demand discovery.
- Keep each instruction file focused on one concern (one category) — don't combine multiple categories.
- Differentiate similar categories explicitly (maintainability vs code-smells decision guide was essential).
