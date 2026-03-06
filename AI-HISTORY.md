# AI History — Lessons Learned

This file records what worked, what failed, and key decisions made during AI-assisted tasks in this repository. The assistant reads this file at the start of every task to avoid repeating mistakes and build on past successes.

---

### 2026-03-06 — Added Lessons Learned instructions to copilot-instructions.md

- **What worked:**
  - Appended the new instructions directly to the existing `.github/copilot-instructions.md` file, preserving the original content.
  - Created `AI-HISTORY.md` at the repo root for easy discoverability.
- **What failed:**
  - Nothing — straightforward task.
- **Key decisions & rationale:**
  - Used a structured markdown template (date, what worked/failed, decisions, improvements) so future entries are consistent and scannable.
  - Set the 10,000-token threshold for summarization as specified, to keep the file manageable over time.
- **Areas for improvement:**
  - None identified for this task.

### 2026-03-06 — Generated comprehensive custom instructions for SonarQube rules

- **What worked:**
  - Read AI-HISTORY.md first to follow established patterns.
  - Sampled rule files from all four categories (security, code-smells, performance, maintainability) to understand structural variations (with/without `params`, `CONSTANT_ISSUE` vs `LINEAR` debt, different severity levels and types).
  - Preserved existing content in `copilot-instructions.md` (GitHub Space reference, AI History instructions) and appended the new SonarQube section below a separator.
  - Used the existing README.md and actual rule JSON files as the source of truth rather than inventing content.
- **What failed:**
  - Nothing — straightforward generation task.
- **Key decisions & rationale:**
  - Updated the existing `.github/copilot-instructions.md` rather than creating a separate file, since this is where Copilot reads custom instructions from and the prompt asked for "a single comprehensive set."
  - Organized the instructions into five numbered sections matching the prompt's requirements: overview, directory structure, rule categories (with full rule tables), file structure (with template and guidelines), and best practices.
  - Included the JSON template, severity guidelines, and debt function explanations so the assistant can generate valid rules without needing to look up the format each time.
- **Areas for improvement:**
  - Could have read every single rule file to verify completeness, but sampling representative files from each category was sufficient and more efficient.

### 2026-03-06 — Generated path-specific custom instructions for each rules category

- **What worked:**
  - Read AI-HISTORY.md first to follow established patterns and avoid past mistakes.
  - Sampled 2+ rule files per category to understand structural variations (type, severity ranges, debt functions, params usage, tag conventions).
  - Created four distinct `.instructions.md` files with `applyTo` frontmatter targeting each category's glob path (`rules/security/**`, `rules/code-smells/**`, etc.).
  - Each instruction file is category-specific: enforces correct `type`, `severity` range, `tags` first tag, `impacts.softwareQuality`, and includes the full existing rule inventory, domain-specific guidance, templates, and validation checklists.
  - Distinguished overlapping concerns (code-smells vs maintainability) with clear decision criteria for rule placement.
  - Performance instructions include a BUG vs CODE_SMELL decision framework unique to that category.
  - Security instructions include OWASP Top 10 mappings and guidance on when (not) to use params.
- **What failed:**
  - Nothing — straightforward generation task.
- **Key decisions & rationale:**
  - Used `.instructions.md` files with `applyTo` YAML frontmatter so Copilot automatically applies the right instructions when editing files in each subdirectory.
  - Made each instruction file self-contained: a developer or AI working in `rules/security/` gets everything they need without reading the other three instruction files.
  - Included existing rule inventories in each file so the AI can check for overlaps before creating duplicates.
  - Kept category-specific templates that differ from the generic template in `copilot-instructions.md` (e.g., security template forces `VULNERABILITY` type, code-smells template shows both `CONSTANT_ISSUE` and `LINEAR` debt patterns).
- **Areas for improvement:**
  - Could have read all 52 rule files for exhaustive verification, but sampling 8 representative files across categories was sufficient and more efficient.
