# Contributing to SonarQube Rule Definitions

Thank you for contributing! This guide walks you through adding, editing, and validating rule definitions in this repository.

## Quick Start

1. **Copy the template** — Start from [`rules/schema/rule-template.json`](rules/schema/rule-template.json)
2. **Fill in all required fields** — See the [schema reference](#schema-reference) below
3. **Save to the correct category folder** — `rules/{category}/{rule-key}.json`
4. **Run validation** — `python3 scripts/validate-rules.py`
5. **Open a pull request** — CI will automatically validate your changes

## Directory Structure

Rules are organized by category:

```
rules/
├── code-smells/        # CODE_SMELL type rules
├── maintainability/    # CODE_SMELL rules focused on maintainability
├── performance/        # CODE_SMELL/BUG rules focused on performance
├── security/           # VULNERABILITY / SECURITY_HOTSPOT rules
└── schema/             # JSON Schema and template (do not add rules here)
```

### Choosing the Right Category

| Rule Type | Impact Focus | Directory |
|---|---|---|
| `CODE_SMELL` | General quality | `code-smells/` |
| `CODE_SMELL` | Maintainability | `maintainability/` |
| `CODE_SMELL` / `BUG` | Performance | `performance/` |
| `VULNERABILITY` / `SECURITY_HOTSPOT` | Security | `security/` |

## Creating a New Rule

### Step 1: Copy the Template

```bash
cp rules/schema/rule-template.json rules/<category>/<rule-key>.json
```

### Step 2: Fill In the Fields

- **`key`** — Must be kebab-case and **exactly match the filename** (without `.json`).
  - Good: `sql-injection` → `sql-injection.json`
  - Bad: `sqlInjection` → `sql-injection.json`
- **`name`** — Title Case display name.
- **`description`** — 1–2 sentences, max 300 characters, explaining what the rule detects and why.
- **`severity`** and **`defaultSeverity`** — Must be identical. One of: `INFO`, `MINOR`, `MAJOR`, `CRITICAL`, `BLOCKER`.
- **`type`** — One of: `CODE_SMELL`, `BUG`, `VULNERABILITY`, `SECURITY_HOTSPOT`.
- **`tags`** — At least one tag, all lowercase kebab-case.
- **`remediation.constantCost`** — Duration format: `30min`, `1h`, `4h`.
- **`remediation.examples`** — At least one `before`/`after` pair showing the bad pattern and the fix.
- **`impacts`** — At least one entry. Must align with `type`:
  - `VULNERABILITY` / `SECURITY_HOTSPOT` → include a `SECURITY` impact
  - `CODE_SMELL` → include a `MAINTAINABILITY` impact
- **`debt`** — Technical debt function:
  - `CONSTANT_ISSUE` → requires `offset`
  - `LINEAR` → requires `coefficient`
  - `LINEAR_OFFSET` → requires both `coefficient` and `offset`
- **`params`** (optional) — Add only if the rule has configurable thresholds.

### Step 3: Validate

```bash
# Validate a single file
python3 scripts/validate-rules.py rules/security/my-new-rule.json

# Validate everything
python3 scripts/validate-rules.py

# Strict mode (warnings are errors)
python3 scripts/validate-rules.py --strict
```

### Step 4: Open a PR

Push your branch and open a pull request. The [CI workflow](.github/workflows/validate-rules.yml) will automatically run validation on all changed rule files.

## Schema Reference

The full JSON Schema is at [`rules/schema/sonarqube-rule.schema.json`](rules/schema/sonarqube-rule.schema.json).

### Required Fields

| Field | Type | Description |
|---|---|---|
| `key` | `string` | Kebab-case identifier matching the filename |
| `name` | `string` | Title-case display name |
| `description` | `string` | What the rule detects and why (≤300 chars) |
| `severity` | `enum` | `INFO` / `MINOR` / `MAJOR` / `CRITICAL` / `BLOCKER` |
| `type` | `enum` | `CODE_SMELL` / `BUG` / `VULNERABILITY` / `SECURITY_HOTSPOT` |
| `tags` | `string[]` | Kebab-case tags (≥1) |
| `remediation` | `object` | Fix cost + before/after examples |
| `impacts` | `object[]` | Software quality impacts (≥1) |
| `defaultSeverity` | `enum` | Must match `severity` |
| `status` | `enum` | `READY` / `BETA` / `DEPRECATED` / `REMOVED` |
| `debt` | `object` | Technical debt function + durations |

## Formatting Guidelines

- **2-space indentation**, no tabs
- **No trailing whitespace**
- **File ends with a single newline**
- **Fields in canonical order**: `key`, `name`, `description`, `severity`, `type`, `tags`, `remediation`, `impacts`, `defaultSeverity`, `status`, `debt`, `params`

## IDE Integration

### VS Code

Add this to your workspace `.vscode/settings.json` to get in-editor schema validation:

```json
{
  "json.schemas": [
    {
      "fileMatch": ["rules/**/*.json", "!rules/schema/**"],
      "url": "./rules/schema/sonarqube-rule.schema.json"
    }
  ]
}
```

## Common Mistakes

| Mistake | Fix |
|---|---|
| `key` doesn't match filename | Rename file or update `key` so they match |
| `severity` ≠ `defaultSeverity` | Make them identical |
| `VULNERABILITY` type without `SECURITY` impact | Add `{ "softwareQuality": "SECURITY", ... }` to `impacts` |
| `CODE_SMELL` type without `MAINTAINABILITY` impact | Add `{ "softwareQuality": "MAINTAINABILITY", ... }` to `impacts` |
| Empty `tags` array | Add at least one relevant tag |
| Missing `remediation.examples` | Include at least one before/after pair |
| `CONSTANT_ISSUE` debt without `offset` | Add an `offset` duration |

## Questions?

Open an issue or check the [README](README.md) for an overview of all rules and categories.
