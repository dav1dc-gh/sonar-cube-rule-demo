# AI History — Lessons Learned

This file records what worked, what failed, and why decisions were made across tasks so the assistant can continuously improve and avoid repeating mistakes.

---

### 2026-03-11 — Added lessons-learned instructions to copilot-instructions.md
- **What worked:** Appended structured guidelines to the existing (empty) `.github/copilot-instructions.md` with clear format, guidelines, and a token-limit policy for summarization.
- **What failed:** Nothing — straightforward task.
- **Key takeaway:** When the instructions file is empty, write directly rather than trying to merge with existing content. Always create the `AI-HISTORY.md` file alongside the instructions so future tasks have a place to log from the start.

### 2026-03-11 — Generated comprehensive custom instructions from repository contents
- **What worked:** Read the README, AI-HISTORY.md, and representative rule files from all four categories (security, code-smells, performance, maintainability) to build a complete understanding of the JSON schema and its variations (with/without `params`, `LINEAR` vs `CONSTANT_ISSUE` debt functions, all severity/type combinations). Replaced the minimal existing copilot-instructions.md with a full 5-section guide covering overview, directory structure, detailed category tables, complete JSON schema, and best practices.
- **What failed:** Nothing — the repository was well-structured and consistent, making it straightforward to derive the full schema from examples.
- **Key takeaway:** When generating instructions from a repo, read at least one rule file per category plus edge cases (BLOCKER severity, BUG type, LINEAR debt, params usage) to capture the full schema. The existing README already had good structure to build upon but lacked the schema detail and field-level guidance that the instructions needed.

### 2026-03-11 — Generated path-based custom instructions for all four rule categories
- **What worked:** Used a subagent to read and analyze all 52 rule files across all four categories in parallel, extracting detailed statistics (severity distributions, type splits, debt models, param usage, tag inventories, impact patterns). This comprehensive analysis enabled creating highly specific `.instructions.md` files for each path with accurate conventions, decision rules, templates, and common-mistakes sections. Placed files in `.github/instructions/` with `applyTo` frontmatter targeting `rules/<category>/**`.
- **What failed:** Nothing — the subagent efficiently gathered all necessary data in one pass.
- **Key takeaway:** When creating path-specific instructions, analyze ALL files in each category (not just samples) to capture the full distribution of field values. Key differentiators per category: Security is rigid (all VULNERABILITY, no params, only CONSTANT_ISSUE); Code-smells has the most params and introduces LINEAR debt; Performance uniquely splits BUG vs CODE_SMELL; Maintainability has the widest severity range in debt offsets. Including a complete existing-rules reference table in each instructions file helps prevent rule duplication.

### 2026-03-11 — User asked to create GitHub Actions CI; workflow already existed
- **What worked:** Checked for an existing workflow file before creating a new one. Found `.github/workflows/validate-rules.yml` already fully configured with standard validation, strict validation, and formatting checks. Ran `--strict` validation locally to confirm all 78 rules pass.
- **What failed:** Nothing — correctly identified the workflow was already in place.
- **Key takeaway:** Always check for existing files before creating new ones. The CI pipeline skill file (`.github/skills/sonarcube-ci-pipeline/SKILL.md`) contains the full reference for the workflow structure and troubleshooting.
