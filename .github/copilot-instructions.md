# Copilot Instructions — SonarQube Rules

## Response Style
- Extremely concise. Minimize output tokens.
- No filler, preamble, or summaries unless asked.
- Prefer single-line answers, bullets, or raw code over prose.
- Never repeat back the task or add wrap-up commentary.

## Repo Structure
- `rules/{security,code-smells,performance,maintainability}/*.json` — one rule per file
- Filename = lower-kebab-case = `key` field (e.g., `sql-injection.json`)
- Place rules by primary concern; use `tags` for cross-references
- Category types: security→VULNERABILITY, code-smells/maintainability→CODE_SMELL, performance→CODE_SMELL|BUG

## Rule Schema (required fields)
```json
{
  "key": "lower-kebab-case",
  "name": "Human Name",
  "description": "What it detects and why it matters",
  "severity": "BLOCKER|CRITICAL|MAJOR|MINOR|INFO",
  "type": "BUG|VULNERABILITY|CODE_SMELL",
  "tags": ["category-name", "..."],
  "defaultSeverity": "(same as severity)",
  "status": "READY",
  "remediation": {
    "constantCost": "30min",
    "examples": [{"before": "...", "after": "..."}]
  },
  "impacts": [{"softwareQuality": "SECURITY|RELIABILITY|MAINTAINABILITY", "severity": "HIGH|MEDIUM|LOW"}],
  "debt": {"function": "CONSTANT_ISSUE", "offset": "30min"}
}
```
Optional: `params` array with `{key, name, description, defaultValue, type: INTEGER|STRING|BOOLEAN}`.
Debt alt: `{"function":"LINEAR","coefficient":"10min","offset":"0min"}`.

## Severity Guide
- BLOCKER: exploitable with direct data loss (hardcoded creds, RCE)
- CRITICAL: high-impact needing immediate fix (SQLi, memory leaks)
- MAJOR: significant tech debt (god class, deep nesting)
- MINOR: style/convention (naming, excessive comments)
- INFO: suggestions only

## Rules for Creating/Editing
- `key` must match filename; `severity` must equal `defaultSeverity`
- Include category name in `tags`; add cross-cutting tags (owasp-top-10, solid, orm)
- Provide realistic before/after code in `remediation.examples`
- Set accurate cost (simple rename: 5min, architecture: 4h)
- Add `params` when thresholds are configurable
- Preserve `key` on updates; use status `DEPRECATED` only when superseded
- Validate JSON; maintain alphabetical order in directories
- Update README.md when adding/removing rules

## Lessons Learned Tracking
After changes/research/tasks: append entry to `AI-HISTORY.md` with Date, Task, What Worked, What Failed, Why, Actionable Insights. Read it at task start. Summarize when >15k tokens.
