# AI History — Lessons Learned

This file tracks what worked, what failed, and why decisions were made across AI-assisted tasks in this repository. Read this at the start of every new task.

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
