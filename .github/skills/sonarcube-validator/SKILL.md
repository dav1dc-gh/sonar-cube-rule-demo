---
name: sonarcube-validator
description: Runs and interprets the SonarQube rule validation script (scripts/validate-rules.py), diagnoses validation failures, and applies fixes. Use when validating rules, debugging validation errors, running bulk audits, or fixing rule definition issues. Keywords: sonarqube, sonar, validate, validation, script, check, audit, fix, error, warning, strict, python, lint, bulk, consistency.
---

# SonarQube Rule Validator

## Purpose

This skill operates the project's validation script at `scripts/validate-rules.py`. It knows how to run all validation modes, interpret the output, diagnose failures, and apply targeted fixes to rule definition files.

Activate this skill whenever the user:
- Asks to validate or check one or more rule files
- Encounters validation errors or warnings and needs help understanding them
- Wants to run a bulk audit of all rules
- Wants to fix validation issues automatically
- Asks about the `--strict` flag or CI validation failures
- Asks what the validation script checks

---

## How to Run Validation

### Validate All Rules

```bash
python3 scripts/validate-rules.py
```

Discovers all `.json` files under `rules/` (excluding `rules/schema/`) and validates each one.

### Validate a Single File

```bash
python3 scripts/validate-rules.py rules/security/sql-injection.json
```

### Validate Multiple Specific Files

```bash
python3 scripts/validate-rules.py rules/security/sql-injection.json rules/code-smells/god-class.json
```

### Strict Mode

```bash
python3 scripts/validate-rules.py --strict
```

Treats **warnings as errors** — the script exits with code 1 if any file has errors OR warnings. This is what the CI pipeline runs to enforce full compliance.

---

## What the Validator Checks

The validation script performs these checks in order:

### 1. JSON Syntax Validation
- File must be valid JSON (no trailing commas, no comments, no single quotes)
- Parse errors are reported with position details

### 2. Required Field Presence
All 11 required fields must be present:
`key`, `name`, `description`, `severity`, `type`, `tags`, `remediation`, `impacts`, `defaultSeverity`, `status`, `debt`

### 3. Enum Validation
- `severity` / `defaultSeverity`: `INFO`, `MINOR`, `MAJOR`, `CRITICAL`, `BLOCKER`
- `type`: `CODE_SMELL`, `BUG`, `VULNERABILITY`, `SECURITY_HOTSPOT`
- `status`: `READY`, `BETA`, `DEPRECATED`, `REMOVED`
- `impacts[].softwareQuality`: `MAINTAINABILITY`, `RELIABILITY`, `SECURITY`
- `impacts[].severity`: `LOW`, `MEDIUM`, `HIGH`
- `debt.function`: `LINEAR`, `CONSTANT_ISSUE`, `LINEAR_OFFSET`
- `params[].type`: `INTEGER`, `FLOAT`, `BOOLEAN`, `STRING`, `TEXT`

### 4. Cross-Field Consistency
- `severity` must equal `defaultSeverity` → **warning** if mismatched
- `key` must match the filename (without `.json`) → **error** if mismatched
- `key` must be kebab-case → **error** if not
- `VULNERABILITY`/`SECURITY_HOTSPOT` type must have a `SECURITY` impact → **warning**
- `CODE_SMELL` type must have a `MAINTAINABILITY` impact → **warning**
- `debt` fields must match the `debt.function` value → **error** if inconsistent

### 5. Remediation Validation
- `constantCost` must match `^\d+(min|h|d)$`
- `examples` must have ≥ 1 entry with non-empty `before` and `after`

### 6. Tags & Params
- `tags` must have ≥ 1 entry, all kebab-case
- `params[].key` should be camelCase → **warning** if not
- `params` entries must have all required sub-fields

### 7. Convention & Formatting
- Description should be ≤ 300 characters → **info**
- Fields should be in canonical order → **info**
- File should end with a newline → **info**
- No tabs → **info**
- No trailing whitespace → **info**

---

## Output Format

### Individual File Report

```
## Lint Results: <filename>

### Errors (must fix)
- [ ] `<field>`: <description>

### Warnings (should fix)
- [ ] `<field>`: <description>

### Info (suggestions)
- [ ] `<field>`: <description>

### Summary
  Errors:   <count>
  Warnings: <count>
  Info:     <count>
  Status:   PASS | FAIL
```

### Summary Table (Bulk Mode)

```
| File                                    | Errors | Warnings | Info | Status |
|-----------------------------------------|--------|----------|------|--------|
| rules/security/sql-injection.json       |      0 |        0 |    0 |   PASS |
| rules/code-smells/god-class.json        |      0 |        1 |    0 |   PASS |
```

### Exit Codes
- `0` → All files passed
- `1` → At least one file has errors (or warnings in `--strict` mode)

---

## Diagnosing Common Errors

### Error: `key` does not match filename

```
`key`: does not match filename. File is "my-rule.json", key is "myRule".
```

**Fix:** Edit the `key` field to match the filename exactly (without `.json`), or rename the file to match the key.

### Error: Required field is missing

```
`description`: required field is missing.
```

**Fix:** Add the missing field. Refer to `rules/schema/rule-template.json` for the expected structure.

### Warning: severity/defaultSeverity mismatch

```
`severity`/`defaultSeverity`: values do not match ("CRITICAL" vs "MAJOR"). Align them.
```

**Fix:** Set `defaultSeverity` to the same value as `severity`.

### Warning: Type/Impact mismatch

```
Type is CODE_SMELL but no impact with softwareQuality MAINTAINABILITY found.
```

**Fix:** Add a `MAINTAINABILITY` impact entry to the `impacts` array. The rule can have multiple impacts.

### Error: Debt function mismatch

```
`debt.offset`: required when function is CONSTANT_ISSUE.
```

**Fix:** Add the missing field. The requirements by function type:
- `CONSTANT_ISSUE` → needs `offset`
- `LINEAR` → needs `coefficient`
- `LINEAR_OFFSET` → needs both `coefficient` and `offset`

---

## Applying Fixes

When fixing validation issues:

1. **Read the full validation output first** — understand all errors for a file before making changes.
2. **Fix errors before warnings** — errors block passing; warnings are advisory (except in strict mode).
3. **Re-validate after fixing** — always run the validator again to confirm the fix.
4. **Use the JSON Schema for real-time feedback** — if `.vscode/settings.json` is configured, VS Code provides instant enum validation as you type.

### Auto-Formatting a File

To reformat a file to 2-space indentation:

```bash
python3 -c "import json; d=json.load(open('rules/<category>/<key>.json')); open('rules/<category>/<key>.json','w').write(json.dumps(d, indent=2, ensure_ascii=False)+'\n')"
```

---

## Script Location and Dependencies

- **Script:** `scripts/validate-rules.py`
- **Dependencies:** Python 3 standard library only (no pip packages needed)
- **Discovers rules from:** `rules/` recursively, excluding `rules/schema/`
- **Schema file (for IDE validation):** `rules/schema/sonarqube-rule.schema.json`

---

## Important Notes

- The validator is stricter than the JSON Schema alone — it catches cross-field logic (key↔filename, type↔impact, severity↔defaultSeverity) that JSON Schema cannot express fully.
- In CI, both standard and `--strict` modes run. A PR will not pass if any warnings exist.
- The script has zero external dependencies — it runs on any system with Python 3.
- When bulk-validating, the summary table at the end gives a quick overview. Scroll up for individual file details.
