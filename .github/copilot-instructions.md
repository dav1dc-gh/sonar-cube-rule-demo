# Copilot Custom Instructions — SonarQube Rules Files

## Overview

This repository contains SonarQube rule definitions in JSON format under `rules/`, organized by category. Help users **create, manage, understand, and extend** these rule files.

## Directory Structure

```
rules/
├── security/        — vulnerability detection (type: VULNERABILITY, severity: CRITICAL/BLOCKER)
├── code-smells/     — structural quality issues (type: CODE_SMELL)
├── performance/     — runtime efficiency problems (type: CODE_SMELL or BUG)
└── maintainability/ — long-term code health (type: CODE_SMELL)
```

**Naming**: lower-kebab-case matching the rule `key` (e.g., `sql-injection.json` → `"key": "sql-injection"`).

Place new rules in the category matching their **primary concern**. If a rule spans categories, choose the dominant one and use `tags` to cross-reference. Discover existing rules by listing the category directory — each JSON file is self-describing.

## Rule File Schema

See `rules/schema/sonarqube-rule.schema.json` for the full JSON Schema (field types, allowed values, constraints). See `rules/schema/rule-template.json` for the structural template.

**Required fields**: `key`, `name`, `description`, `severity`, `type`, `tags`, `remediation`, `impacts`, `defaultSeverity`, `status`, `debt`.

**Optional field**: `params` — configurable thresholds (expose when rule sensitivity depends on a number).

Key constraints:
- `severity` / `defaultSeverity` must stay in sync
- `tags` must include the category name plus relevant cross-cutting concerns
- `status`: use `"READY"` for active rules, `"DEPRECATED"` only when superseded
- `key` must match filename (without `.json`) and never change once published

## Severity Guidelines

| Severity | When to Use |
|----------|-------------|
| **BLOCKER** | Exploitable vulnerability with direct data loss/compromise risk |
| **CRITICAL** | High-impact bugs or vulnerabilities needing immediate attention |
| **MAJOR** | Significant quality issues accumulating technical debt |
| **MINOR** | Low-impact style or convention violations |
| **INFO** | Informational findings, suggestions |

## Best Practices

- Write a thorough `description` — explain *what* is detected, *why* it's a problem, and consequences.
- Provide realistic, compilable before/after code in `remediation.examples`.
- Set accurate `remediation.constantCost` — simple renames: `5min`; architecture changes: `4h`.
- When updating a rule, preserve the `key` to avoid breaking quality profiles.
- Validate JSON before committing. One rule per file. Maintain alphabetical order within categories.
- Update `README.md` when adding or removing rules.

## Lessons Learned Tracking

After every response involving changes or research, append a "Lessons Learned" entry to `AI-HISTORY.md` with: **Date**, **Task**, **What Worked**, **What Failed**, **Why**, **Actionable Insights**.

At the start of every new task, read `AI-HISTORY.md` to avoid repeating past mistakes.

When `AI-HISTORY.md` exceeds 15,000 tokens (~60KB), summarize key insights into a "Summary of Key Insights" section at the top and remove older entries.
