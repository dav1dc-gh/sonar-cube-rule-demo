---
name: sonarcube-linter
description: Lints and validates SonarQube rule definition JSON files for syntax errors, schema compliance, and human readability. Use when reviewing, creating, editing, or troubleshooting SonarQube/SonarCloud custom rule configuration files. Keywords: sonarqube, sonar, lint, linter, rule, json, validate, format, code-smell, vulnerability, security, maintainability, performance, quality-profile.
---

# SonarQube Rule Definition Linter

## Purpose

This skill validates and lints SonarQube rule definition JSON files (`.json`) stored under the `rules/` directory hierarchy. It detects syntax errors, enforces the required schema, checks for semantic inconsistencies, and recommends formatting improvements to maximise human readability and maintainability of rule configurations.

Activate this skill whenever the user:
- Creates, edits, or reviews a SonarQube rule JSON file
- Asks to validate or lint rule definitions
- Requests formatting or readability improvements to rule configs
- Encounters errors or unexpected behaviour related to rule configuration
- Wants to bulk-audit all rules for consistency

---

## Rule JSON Schema Reference

Every rule definition file **must** be valid JSON and conform to the schema below. Fields marked **(required)** must be present; others are optional but recommended.

### Top-Level Fields

| Field | Type | Required | Allowed Values / Constraints |
|---|---|---|---|
| `key` | `string` | **Yes** | Unique kebab-case identifier (e.g. `"sql-injection"`, `"god-class"`). Must match the filename without `.json`. |
| `name` | `string` | **Yes** | Human-readable display name. Title-case, concise. |
| `description` | `string` | **Yes** | One or two sentences explaining what the rule detects and why it matters. |
| `severity` | `string` | **Yes** | One of: `"INFO"`, `"MINOR"`, `"MAJOR"`, `"CRITICAL"`, `"BLOCKER"` |
| `type` | `string` | **Yes** | One of: `"CODE_SMELL"`, `"BUG"`, `"VULNERABILITY"`, `"SECURITY_HOTSPOT"` |
| `tags` | `string[]` | **Yes** | Non-empty array of lowercase kebab-case tags relevant to the rule. |
| `remediation` | `object` | **Yes** | See **Remediation Object** below. |
| `impacts` | `object[]` | **Yes** | See **Impacts Array** below. |
| `defaultSeverity` | `string` | **Yes** | Must match the top-level `severity` value. |
| `status` | `string` | **Yes** | One of: `"READY"`, `"BETA"`, `"DEPRECATED"`, `"REMOVED"` |
| `debt` | `object` | **Yes** | See **Debt Object** below. |
| `params` | `object[]` | No | See **Params Array** below. Only include when the rule exposes configurable thresholds. |

### Remediation Object

```jsonc
{
  "constantCost": "<duration>",   // Required. Estimated fix time, e.g. "30min", "1h", "4h"
  "examples": [                   // Required. At least one before/after example.
    {
      "before": "<string>",       // Code or description of the problematic pattern
      "after": "<string>"         // Code or description of the corrected pattern
    }
  ]
}
```

**Lint rules for `remediation`:**
- `constantCost` must be a non-empty string matching the pattern `^\d+(min|h|d)$`.
- `examples` must contain at least one entry; each entry must have both `before` and `after` as non-empty strings.

### Impacts Array

```jsonc
[
  {
    "softwareQuality": "<quality>",  // Required. One of: "MAINTAINABILITY", "RELIABILITY", "SECURITY"
    "severity": "<level>"            // Required. One of: "LOW", "MEDIUM", "HIGH"
  }
]
```

**Lint rules for `impacts`:**
- Must contain at least one impact entry.
- `softwareQuality` and `severity` must use the exact allowed enum values (uppercase).

### Debt Object

```jsonc
{
  "function": "<type>",       // Required. One of: "LINEAR", "CONSTANT_ISSUE", "LINEAR_OFFSET"
  "coefficient": "<duration>", // Required when function is "LINEAR" or "LINEAR_OFFSET"
  "offset": "<duration>"      // Required when function is "CONSTANT_ISSUE" or "LINEAR_OFFSET"
}
```

**Lint rules for `debt`:**
- When `function` is `"LINEAR"`: `coefficient` is required, `offset` is optional (defaults to `"0min"`).
- When `function` is `"CONSTANT_ISSUE"`: `offset` is required, `coefficient` should be absent.
- When `function` is `"LINEAR_OFFSET"`: both `coefficient` and `offset` are required.
- Duration values must match the pattern `^\d+(min|h|d)$`.

### Params Array (Optional)

```jsonc
[
  {
    "key": "<string>",           // Required. camelCase identifier
    "name": "<string>",          // Required. Human-readable label
    "description": "<string>",   // Required. Explains the parameter
    "defaultValue": "<string>",  // Required. Default as a string (even for numeric types)
    "type": "<string>"           // Required. One of: "INTEGER", "FLOAT", "BOOLEAN", "STRING", "TEXT"
  }
]
```

---

## Linting Checks

When linting a rule file, perform **all** of the following checks in order and report every finding.

### 1. JSON Syntax Validation
- The file must be well-formed JSON (no trailing commas, no comments, no single quotes, no unquoted keys).
- Report the exact line/character position of any parse error.

### 2. Required Field Presence
- Verify every **(required)** field from the schema above is present.
- Report each missing field as an **error**.

### 3. Enum / Type Validation
- `severity` and `defaultSeverity` must be one of the allowed severity values.
- `type` must be one of the allowed type values.
- `status` must be one of the allowed status values.
- `impacts[].softwareQuality` and `impacts[].severity` must use exact allowed values.
- `debt.function` must be one of the allowed function types.
- `params[].type` (if present) must be one of the allowed param types.
- Report violations as **errors**.

### 4. Cross-Field Consistency
- `severity` must equal `defaultSeverity`. If they differ, report as a **warning** and suggest aligning them.
- `key` must match the filename (without `.json`). For example, a file named `sql-injection.json` must have `"key": "sql-injection"`. Report mismatches as **errors**.
- If `type` is `"VULNERABILITY"` or `"SECURITY_HOTSPOT"`, at least one impact should have `"softwareQuality": "SECURITY"`. Report mismatches as **warnings**.
- If `type` is `"CODE_SMELL"`, at least one impact should have `"softwareQuality": "MAINTAINABILITY"`. Report mismatches as **warnings**.
- The `debt` object fields must be consistent with the `debt.function` value (see schema above). Report inconsistencies as **errors**.

### 5. Convention & Style Checks
- `key` must be kebab-case (`/^[a-z][a-z0-9]*(-[a-z0-9]+)*$/`). Report violations as **errors**.
- `tags` entries must be lowercase kebab-case. Report violations as **warnings**.
- `params[].key` must be camelCase. Report violations as **warnings**.
- `description` should not exceed 300 characters. Report as an **info** suggestion if exceeded.
- `name` should be title-case. Report as an **info** suggestion if not.

### 6. Readability & Formatting
- JSON must be indented with **2 spaces** (no tabs).
- Top-level keys should appear in the canonical order defined in the schema table above: `key`, `name`, `description`, `severity`, `type`, `tags`, `remediation`, `impacts`, `defaultSeverity`, `status`, `debt`, `params`.
- No trailing whitespace on any line.
- File must end with a single newline character.
- Report formatting deviations as **info** suggestions and offer to auto-fix.

---

## Output Format

When reporting lint results, use the following structure:

```
## Lint Results: <filename>

### Errors (must fix)
- [ ] `<field>`: <description of the error>

### Warnings (should fix)
- [ ] `<field>`: <description of the warning>

### Info (suggestions)
- [ ] `<field>`: <description of the suggestion>

### Summary
- Errors: <count>
- Warnings: <count>
- Info: <count>
- Status: PASS | FAIL (FAIL if any errors exist)
```

If no issues are found, report:

```
## Lint Results: <filename>

All checks passed. No issues found.
```

---

## Auto-Fix Capabilities

When the user requests a fix or when offering corrections, the skill can automatically:

1. **Reorder keys** to match canonical field order.
2. **Re-indent** the file to 2-space indentation.
3. **Align `defaultSeverity`** with `severity`.
4. **Strip trailing whitespace** and ensure a final newline.
5. **Normalise enum values** to their correct uppercase form (e.g. `"major"` → `"MAJOR"`).
6. **Add missing fields** with sensible placeholder values, clearly marked with `TODO` comments that the user should fill in.

Always show a diff or summary of proposed changes and apply them only after confirmation, or immediately if the user explicitly asked for auto-fix.

---

## Bulk Linting

When asked to lint all rules or audit the repository:

1. Recursively discover all `.json` files under `rules/`.
2. Lint each file individually using the checks above.
3. Produce a summary table:

```
| File | Errors | Warnings | Info | Status |
|------|--------|----------|------|--------|
| rules/security/sql-injection.json | 0 | 0 | 1 | PASS |
| rules/code-smells/god-class.json  | 0 | 1 | 0 | PASS |
| ...                                | ... | ... | ... | ... |
```

4. Conclude with aggregate totals and an overall PASS/FAIL verdict.

---

## Examples

### Example 1: Linting a valid rule file

Given `rules/security/sql-injection.json` with all required fields present, correct enums, matching key/filename, and proper formatting:

```
## Lint Results: sql-injection.json

All checks passed. No issues found.
```

### Example 2: Linting a file with errors

Given a file `rules/code-smells/my_rule.json`:
```json
{
  "key": "myRule",
  "name": "my rule",
  "severity": "high",
  "type": "CODE_SMELL",
  "tags": [],
  "remediation": { "constantCost": "30min" },
  "impacts": [],
  "defaultSeverity": "MAJOR",
  "status": "READY",
  "debt": { "function": "CONSTANT_ISSUE" }
}
```

Expected output:

```
## Lint Results: my_rule.json

### Errors (must fix)
- [ ] `key`: Must be kebab-case. Found "myRule", expected "my-rule".
- [ ] `key`: Does not match filename. File is "my_rule.json", key is "myRule".
- [ ] `description`: Required field is missing.
- [ ] `severity`: Invalid value "high". Must be one of: INFO, MINOR, MAJOR, CRITICAL, BLOCKER.
- [ ] `tags`: Must contain at least one tag.
- [ ] `remediation.examples`: Required field is missing. At least one before/after example must be provided.
- [ ] `impacts`: Must contain at least one impact entry.
- [ ] `debt.offset`: Required when function is "CONSTANT_ISSUE".

### Warnings (should fix)
- [ ] `severity`/`defaultSeverity`: Values do not match ("high" vs "MAJOR"). Align them.

### Info (suggestions)
- [ ] `name`: Should be title-case. Found "my rule", consider "My Rule".

### Summary
- Errors: 8
- Warnings: 1
- Info: 1
- Status: FAIL
```

---

## Important Notes

- Always read the full file content before linting; do not rely on partial reads.
- When creating new rule files, use this schema as the template and validate immediately.
- Rule files live under `rules/<category>/` where category is one of: `code-smells`, `maintainability`, `performance`, `security`.
- Filenames must be kebab-case and match the `key` field exactly (plus `.json` extension).