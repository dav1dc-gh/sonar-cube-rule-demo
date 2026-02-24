# AI History — Lessons Learned

This file records what worked, what failed, and why decisions were made during AI-assisted tasks. The assistant reads this at the start of every new task to avoid repeating mistakes and build on past successes.

---

## 2026-02-24 — Added Lessons Learned Custom Instructions

- **Task**: Add custom instructions so the assistant writes a "lessons learned" entry to `AI-HISTORY.md` at the end of every response, and reads it at the start of every new task.
- **What Worked**: Created `.github/copilot-instructions.md` as the standard custom instructions file for GitHub Copilot, and initialized `AI-HISTORY.md` at the repo root for easy discovery.
- **What Failed**: N/A.
- **Why**: Centralizing lessons in a persistent file ensures continuity across sessions and prevents repeated mistakes.
- **Actionable Insights**: Always check for existing `.github/copilot-instructions.md` before creating one. Keep `AI-HISTORY.md` at the repo root so it's obvious and accessible.

---

## 2026-02-24 — Expanded CI Workflow Prompt for Low-Capability Models

- **Task**: Add exhaustive detail to a terse one-line prompt (`a-really-simple.prompt.md`) so that any model — even a small/cheap one — could implement a GitHub Actions CI workflow without ambiguity.
- **What Worked**: Studied the actual repo structure, JSON schema (from multiple rule files across all 4 categories), and README to derive the exact validation rules. Used tables for schema constraints, explicit YAML snippets for trigger/permissions blocks, and a "What NOT to Do" section to prevent common model hallucinations (installing npm, adding SonarQube scanning, etc.). Specified exact file path, job names, dependency graph, step implementations, output formats, and exit code behavior.
- **What Failed**: N/A.
- **Why**: Weak models fail on ambiguous prompts by hallucinating irrelevant steps (Node.js installs, SonarQube scanners, matrix builds). Eliminating every decision point and providing exact constraints, allowed values, and copy-paste YAML fragments removes the need for the model to "think" and reduces variance to near-zero.
- **Actionable Insights**: For idiot-proof prompts: (1) specify exact file paths, (2) enumerate every allowed value in tables, (3) provide literal code/YAML for tricky parts, (4) explicitly list what NOT to do, (5) describe output format and exit code behavior for every step, (6) state job dependency graph explicitly. The more decisions you remove from the model, the more consistent the output.

---

## 2026-02-24 — Generated Comprehensive Custom Instructions from Repository Contents

- **Task**: Use the repository's full contents to create a comprehensive set of custom instructions in `.github/copilot-instructions.md` covering overview, directory structure, rule categories, JSON schema, and best practices.
- **What Worked**: Read AI-HISTORY.md first for past lessons. Sampled representative rule files from each category (security, code-smells, performance, maintainability) to capture all schema variations — CONSTANT_ISSUE vs LINEAR debt, rules with and without `params`, all three `type` values (VULNERABILITY, BUG, CODE_SMELL), and all severity levels (BLOCKER through MINOR). Combined findings with README content to produce a single authoritative document with tables, annotated JSON schema, severity guidelines, and user-interaction guidance.
- **What Failed**: N/A.
- **Why**: A comprehensive custom instructions file ensures the assistant can handle any rule-related task without needing to re-derive the schema or conventions each time. Sampling diverse rules across categories confirmed that the schema was consistent and revealed all field variations (e.g., `coefficient` only in LINEAR debt, `params` only on threshold-based rules).
- **Actionable Insights**: When generating instructions from a repo, always read actual data files (not just docs) to verify the schema matches reality. Sample from every category to catch edge cases. Preserve the existing Lessons Learned section when replacing custom instructions content.

---

## 2026-02-24 — Generated Path-Specific Custom Instructions for Each Rule Category

- **Task**: Create 4 path-specific Copilot instruction files (one per rule category) in `.github/instructions/` with `applyTo` frontmatter targeting `rules/security/**`, `rules/code-smells/**`, `rules/performance/**`, and `rules/maintainability/**`.
- **What Worked**: Read every single rule file (all 52 across 4 categories) to extract exact conventions per category — type distributions, severity patterns, tag conventions, debt model usage, params presence, impact quality mappings. This revealed category-specific patterns invisible from sampling: performance is the only category mixing `BUG` and `CODE_SMELL` types; code-smells has the highest params ratio; `shotgun-surgery` in maintainability is missing its `offset` field (an anomaly); `too-many-parameters` in maintainability overlaps with `long-parameter-list` in code-smells. Each instruction file documents these nuances precisely.
- **What Failed**: N/A.
- **Why**: Path-specific instructions allow the assistant to apply category-specific conventions automatically when working within a particular directory, without needing to load the global instructions or re-derive conventions from examples. The `applyTo` glob pattern in frontmatter is the standard VS Code Copilot mechanism for scoped instructions.
- **Actionable Insights**: (1) Always read ALL files in a category, not just samples — edge cases and anomalies only surface with exhaustive reads. (2) Document observed anomalies (like missing `offset`) so the assistant can warn about them. (3) Note cross-category overlaps explicitly (too-many-parameters vs long-parameter-list) to prevent accidental duplication. (4) Use `.github/instructions/*.instructions.md` with `applyTo` frontmatter for path-scoped Copilot instructions.
