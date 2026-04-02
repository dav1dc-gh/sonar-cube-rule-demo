---
name: validate-rules
description: "Validate SonarQube rule JSON files against the schema and repository conventions. Use when: checking rule correctness, running validation, building JSON Schema, creating validation scripts, setting up CI pipelines for rule validation, or auditing rules for consistency issues."
---

# Validate Rules

## Keywords

validate, validation, schema, JSON Schema, rule-schema.json, validate_rules.py, jsonschema, CI, GitHub Actions, pipeline, check, lint, audit, consistency, cross-check, requirements.txt, .gitignore, correctness

## When to Use

- Validating one or more rule JSON files for correctness
- Creating or updating the JSON Schema (`schema/rule-schema.json`)
- Creating or updating the Python validation script (`scripts/validate_rules.py`)
- Setting up GitHub Actions CI for automated validation
- Auditing the full rule set for consistency issues

## JSON Schema Specification

The schema must enforce these constraints for every rule file under `rules/`:

### Required Fields

| Field | Type | Constraints |
|-------|------|-------------|
| `key` | string | Lower-kebab-case, non-empty, pattern: `^[a-z][a-z0-9]*(-[a-z0-9]+)*$` |
| `name` | string | Non-empty, human-readable |
| `description` | string | Non-empty, min 20 characters |
| `severity` | string | Enum: `BLOCKER`, `CRITICAL`, `MAJOR`, `MINOR`, `INFO` |
| `type` | string | Enum: `BUG`, `VULNERABILITY`, `CODE_SMELL` |
| `tags` | array | Min 1 item, items are non-empty strings |
| `remediation` | object | See below |
| `impacts` | array | Min 1 item, see below |
| `defaultSeverity` | string | Same enum as `severity` |
| `status` | string | Enum: `READY`, `DEPRECATED` |
| `debt` | object | See below |

### Optional Fields

| Field | Type | Constraints |
|-------|------|-------------|
| `params` | array | Items have `key`, `name`, `description`, `defaultValue`, `type` |

### Nested Object Schemas

**`remediation`** — required fields:
- `constantCost` (string, pattern: `^\d+(min|h|d)$`)
- `examples` (array, min 1 item, each with `before` and `after` strings)

**`impacts[]`** — each item:
- `softwareQuality` ∈ `SECURITY`, `RELIABILITY`, `MAINTAINABILITY`
- `severity` ∈ `HIGH`, `MEDIUM`, `LOW`

**`debt`** — conditional:
- If `function` = `CONSTANT_ISSUE` → requires `offset` (string, time pattern)
- If `function` = `LINEAR` → requires `coefficient` (string, time pattern) AND `offset` (string, time pattern)

**`params[]`** — each item:
- `key` (string), `name` (string), `description` (string), `defaultValue` (string), `type` ∈ `INTEGER`, `STRING`, `BOOLEAN`

## Cross-Validation Rules

Beyond schema validation, the validation script must check:

1. **Filename ↔ key match**: `<filename>.json` must have `"key": "<filename>"`
2. **severity ↔ defaultSeverity sync**: These two fields must be identical
3. **Category tag present**: The parent directory name determines the expected tag:
   - `rules/security/` → tags must include `"security"`
   - `rules/code-smells/` → tags must include `"code-smell"`
   - `rules/performance/` → tags must include `"performance"`
   - `rules/maintainability/` → tags must include `"maintainability"`
4. **Category-type consistency**:
   - `rules/security/` → `type` must be `VULNERABILITY`
   - `rules/code-smells/` → `type` must be `CODE_SMELL`
   - `rules/maintainability/` → `type` must be `CODE_SMELL`
   - `rules/performance/` → `type` must be `CODE_SMELL` or `BUG`
5. **No duplicate keys**: No two rule files across all categories share the same `key`

## Validation Script Structure

File: `scripts/validate_rules.py`
Dependencies: `jsonschema>=4.0` (listed in `requirements.txt`)

```
scripts/validate_rules.py
├── load_schema()          → reads schema/rule-schema.json
├── find_rule_files()      → glob rules/**/*.json
├── validate_schema(file)  → jsonschema.validate against schema
├── validate_cross(file)   → filename/key match, severity sync, category tag, type
├── validate_uniqueness()  → no duplicate keys across all files
├── main()                 → orchestrate, collect errors, exit(1) if any
```

Output format: `ERROR: <filepath>: <message>` on stderr, exit code 0 = pass, 1 = fail.

## GitHub Actions CI

File: `.github/workflows/validate-rules.yml`

```yaml
name: Validate Rules
on:
  push:
    branches: [main]
    paths: ['rules/**', 'schema/**', 'scripts/**']
  pull_request:
    branches: [main]
    paths: ['rules/**', 'schema/**', 'scripts/**']

jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: '3.11'
      - run: pip install -r requirements.txt
      - run: python scripts/validate_rules.py
```

## File Inventory

| File | Purpose |
|------|---------|
| `schema/rule-schema.json` | JSON Schema definition |
| `scripts/validate_rules.py` | Python validation script |
| `requirements.txt` | Python dependencies |
| `.github/workflows/validate-rules.yml` | CI pipeline |
| `.gitignore` | Python ignores |
