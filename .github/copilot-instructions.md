# SonarQube Rules — Copilot Instructions

Repository of SonarQube rule definitions (JSON). Help users create, manage, and extend these rules.

## Structure

```
rules/
├── security/        # VULNERABILITY type, CRITICAL/BLOCKER severity
├── code-smells/     # CODE_SMELL type
├── performance/     # CODE_SMELL or BUG type
└── maintainability/ # CODE_SMELL type
```

Naming: lower-kebab-case filename matching `key` field (e.g., `sql-injection.json` → `"key": "sql-injection"`).
Place rules in category matching primary concern; use `tags` to cross-reference.

## Rule Schema

Required fields: `key`, `name`, `description`, `severity`, `type`, `tags`, `remediation`, `impacts`, `defaultSeverity`, `status`, `debt`.
Optional: `params` (configurable thresholds).

```json
{
  "key": "example-rule",
  "name": "Example Rule",
  "description": "What it detects and why it matters.",
  "severity": "MAJOR",
  "defaultSeverity": "MAJOR",
  "type": "CODE_SMELL",
  "status": "READY",
  "tags": ["category-name", "relevant-tag"],
  "remediation": {
    "constantCost": "30min",
    "examples": [{"before": "// bad", "after": "// fixed"}]
  },
  "impacts": [{"softwareQuality": "MAINTAINABILITY", "severity": "MEDIUM"}],
  "debt": {"function": "CONSTANT_ISSUE", "offset": "30min"},
  "params": [{"key": "max", "name": "Maximum", "description": "...", "defaultValue": "10", "type": "INTEGER"}]
}
```

### Field values
- `severity`/`defaultSeverity`: BLOCKER | CRITICAL | MAJOR | MINOR | INFO
- `type`: BUG | VULNERABILITY | CODE_SMELL
- `status`: READY (active) | DEPRECATED (superseded)
- `impacts[].softwareQuality`: SECURITY | RELIABILITY | MAINTAINABILITY
- `impacts[].severity`: HIGH | MEDIUM | LOW
- `debt.function`: CONSTANT_ISSUE (with `offset`) | LINEAR (with `coefficient` + `offset`)
- `params[].type`: INTEGER | STRING | BOOLEAN

### Severity guide
- BLOCKER: exploitable vuln with direct data loss risk
- CRITICAL: high-impact bugs/vulns needing immediate fix
- MAJOR: significant quality issues accumulating debt
- MINOR: low-impact style/convention violations
- INFO: suggestions

## Rules

### Creating
1. Pick correct category
2. Descriptive kebab-case `key` matching filename
3. Thorough `description` covering what/why/consequences
4. Realistic before/after code in `remediation.examples`
5. Accurate `constantCost` (rename: 5min, architecture: 4h)
6. Always include category name in `tags` plus cross-cutting concerns
7. Add `params` for configurable thresholds with sensible defaults

### Managing
- Keep `severity` and `defaultSeverity` in sync
- Preserve `key` on updates to avoid breaking quality profiles
- Valid JSON, one rule per file, filename = key
- Alphabetical order in directories
- Update README.md when adding/removing rules

## Response Style
- Keep responses concise — prefer bullet points over paragraphs
- Do not repeat back file contents unless asked
- Do not explain changes after making them — just confirm completion
- Omit code examples unless explicitly requested
- Never summarize what was done in more than one sentence

## Lessons Learned

After every change/research/task, append to `AI-HISTORY.md`:
- Date, Task, What Worked, What Failed, Why, Actionable Insights

Read `AI-HISTORY.md` at task start. Summarize when >15K tokens.
