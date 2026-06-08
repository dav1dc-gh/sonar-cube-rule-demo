# Copilot Instructions — SonarQube Rules

## Response Style

Be extremely concise. No preamble, no summaries, no restating the question. Output only what's needed: code, commands, or direct answers. Use bullet points over paragraphs. Skip explanations unless asked. When generating files, output only the file — no commentary.

## Purpose

Repository of SonarQube rule definitions (JSON). Help users create, manage, and extend these files.

## Structure

Rules live in `rules/` grouped by category. Discover current rules via directory listing at runtime.

| Category | Type | Typical Severity |
|----------|------|-----------------|
| `security/` | `VULNERABILITY` | CRITICAL, BLOCKER |
| `code-smells/` | `CODE_SMELL` | MAJOR, MINOR |
| `performance/` | `CODE_SMELL` or `BUG` | CRITICAL, MAJOR |
| `maintainability/` | `CODE_SMELL` | MAJOR, MINOR |

**Naming**: lower-kebab-case filename must match the `key` field (e.g., `sql-injection.json` → `"key": "sql-injection"`).

## Rule Schema

Required fields: `key`, `name`, `description`, `severity` (BLOCKER|CRITICAL|MAJOR|MINOR|INFO), `type` (BUG|VULNERABILITY|CODE_SMELL), `tags` (include category name first), `remediation`, `impacts`, `defaultSeverity` (same as severity), `status` ("READY"), `debt`. Optional: `params`.

```json
{
  "key": "example-rule",
  "name": "Example Rule",
  "description": "What it detects and why it matters.",
  "severity": "MAJOR",
  "type": "CODE_SMELL",
  "tags": ["code-smell", "design"],
  "remediation": {
    "constantCost": "30min",
    "examples": [{ "before": "// bad", "after": "// good" }]
  },
  "impacts": [{ "softwareQuality": "MAINTAINABILITY", "severity": "HIGH" }],
  "defaultSeverity": "MAJOR",
  "status": "READY",
  "debt": { "function": "CONSTANT_ISSUE", "offset": "30min" }
}
```

**`debt` variants**: `CONSTANT_ISSUE` (with `offset`) or `LINEAR` (with `coefficient` + `offset`).
**`params`**: `{ "key", "name", "description", "defaultValue", "type": "INTEGER|STRING|BOOLEAN" }` — add when thresholds are configurable.

## Severity Guide

- **BLOCKER**: Direct data breach / RCE risk
- **CRITICAL**: High-impact exploitable issue or severe performance bug
- **MAJOR**: Significant tech debt (design violations, structural issues)
- **MINOR**: Low-impact style/convention violations
- **INFO**: Suggestions only

## Rules for Creating Rules

1. Place in the category matching the primary concern
2. Key = lower-kebab-case, must match filename
3. Description: explain what, why, and consequences
4. Include realistic before/after code in `remediation.examples`
5. Remediation cost: `5min` (renames) → `4h` (architecture changes)
6. Tags: category name first, then cross-cutting concerns (`owasp-top-10`, `solid`, `orm`)
7. Add `params` when detection sensitivity is configurable
8. Keep `severity` and `defaultSeverity` in sync
9. Validate JSON before committing; one rule per file
10. Update `README.md` when adding/removing rules

## Lessons Learned Tracking

After changes/research/tasks, append to `AI-HISTORY.md`: Date, Task, What Worked, What Failed, Why, Actionable Insights. Read it at the start of new tasks. Summarize when it exceeds ~10KB.
