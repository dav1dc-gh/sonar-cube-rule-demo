# Copilot Custom Instructions — SonarQube Rules Files

This repo contains SonarQube rule definition JSON files under `rules/`, grouped
into four categories. Help users **create, manage, understand, and extend** them.

## Layout

```
rules/
├── security/         # VULNERABILITY rules (CRITICAL/BLOCKER typical)
├── code-smells/      # CODE_SMELL — design/structural issues
├── performance/      # CODE_SMELL or BUG — runtime efficiency
├── maintainability/  # CODE_SMELL — readability / long-term health
└── schema/           # JSON Schema + rule template (authoritative)
```

The directory comments above are the category placement rule. Pick by primary
concern; cross-reference others via `tags`.

**Filename convention**: lower-kebab-case, matching the `key` field
(`sql-injection.json` → `"key": "sql-injection"`). One rule per file.

## Rule schema

Authoritative: [rules/schema/sonarqube-rule.schema.json](rules/schema/sonarqube-rule.schema.json)
+ template [rules/schema/rule-template.json](rules/schema/rule-template.json).
Read once per session; trust thereafter.

Non-obvious rules (not in the schema):
- `severity` and `defaultSeverity` must stay in sync.
- Always include the category name (e.g. `"security"`) as a tag.
- Use SonarQube's standard severity semantics. Reserve `BLOCKER` for directly
  exploitable security issues.
- `status`: `"READY"` for active, `"DEPRECATED"` only when superseded. **Never
  change a published `key`** — it breaks quality profiles.
- `debt.function`: `CONSTANT_ISSUE` (uses `offset`) or `LINEAR`
  (uses `coefficient` + `offset`).
- `remediation.examples` must be realistic, compilable before/after snippets.

## Tool & output economy

- The workspace structure in context already lists every rule file; don't
  re-list `rules/` with `list_dir`.
- Filenames equal rule keys — use `file_search`/`read_file`, not
  `semantic_search`, for rule lookups.
- Read the schema at most once per session.
- For multi-file work, delegate to the matching subagent (`create-rule`,
  `lint-rules`, `validate-rules`, `audit-rules`, `document-repo`, `fix-ci`)
  instead of chaining tool calls inline.
- Single-rule lint: `python3 scripts/validate-rules.py <path>`.
- Do **not** create change-summary markdown files (`CHANGES.md`, `SUMMARY.md`,
  per-task reports). Confirm edits in one sentence; record durable lessons in
  `AI-HISTORY.md`.
- Don't paste edited JSON back in chat or transcribe schema fields — link to
  the file instead.

## Common task shortcuts

- New rule        → `create-rule` subagent
- Bulk audit      → `audit-rules` subagent
- Doc drift fix   → `document-repo` subagent
- CI failure      → `fix-ci` subagent
- Single lint     → `python3 scripts/validate-rules.py <path>`

## Lessons Learned tracking

At the **start** of any task, read `AI-HISTORY.md` — but only the
"Summary of Key Insights" section plus the last 5 entries.

At the **end** of any task involving changes, research, or investigation,
append a concise entry: Date, Task, What Worked, What Failed, Why,
Actionable Insights.

When `AI-HISTORY.md` exceeds ~5k tokens (~20KB), or has more than 10 verbatim
entries, collapse older ones into one-line bullets under "Summary of Key
Insights" at the top.
