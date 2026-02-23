---
name: sonarcube-repo-organizer
description: Manages the repository structure, category organisation, naming conventions, and contributing guidelines for SonarQube rule definitions. Use when reorganising rules, adding categories, renaming files, onboarding contributors, or performing bulk operations on the rule repository. Keywords: sonarqube, sonar, repository, organize, structure, category, directory, rename, move, bulk, convention, naming, contributing, onboarding, schema, template, vscode, ide.
---

# SonarQube Repository Organiser

## Purpose

This skill manages the overall structure and conventions of the SonarQube rule definition repository. It covers directory organisation, naming conventions, IDE configuration, the contributing guide, and bulk operations for maintaining consistency at scale.

Activate this skill whenever the user:
- Asks about the repository structure or conventions
- Wants to reorganise, move, or rename rule files
- Asks about adding a new category directory
- Wants to perform bulk operations (rename, re-categorise, audit)
- Needs help onboarding new contributors
- Asks about IDE setup, the template, or the contributing guide
- Wants to understand how the schema, template, and tooling fit together

---

## Repository Structure

```
.
├── .github/
│   ├── prompts/                # Copilot prompt files
│   ├── skills/                 # Agent skill definitions
│   │   ├── sonarcube-linter/          # Rule linting skill
│   │   ├── sonarcube-rule-creator/    # Rule creation skill
│   │   ├── sonarcube-validator/       # Validation script skill
│   │   ├── sonarcube-ci-pipeline/     # CI workflow skill
│   │   └── sonarcube-repo-organizer/  # This skill
│   └── workflows/
│       └── validate-rules.yml         # CI validation pipeline
├── .vscode/
│   └── settings.json                  # IDE schema mapping
├── rules/
│   ├── code-smells/            # General code quality rules
│   ├── maintainability/        # Maintainability-focused rules
│   ├── performance/            # Performance-focused rules
│   ├── security/               # Security vulnerability rules
│   └── schema/                 # Schema + template (NOT for rules)
│       ├── sonarqube-rule.schema.json
│       └── rule-template.json
├── scripts/
│   └── validate-rules.py       # Validation script
├── CONTRIBUTING.md              # Contributor guide
└── README.md                    # Project overview
```

---

## Category Directories

### Current Categories

| Directory | Purpose | Typical `type` | Required Impact |
|---|---|---|---|
| `rules/code-smells/` | General code quality issues | `CODE_SMELL` | `MAINTAINABILITY` |
| `rules/maintainability/` | Maintainability-focused issues | `CODE_SMELL` | `MAINTAINABILITY` |
| `rules/performance/` | Performance bottlenecks | `CODE_SMELL` / `BUG` | `MAINTAINABILITY` or `RELIABILITY` |
| `rules/security/` | Security vulnerabilities | `VULNERABILITY` / `SECURITY_HOTSPOT` | `SECURITY` |

### Adding a New Category

If a new category is needed (e.g. `rules/reliability/`):

1. **Create the directory:**
   ```bash
   mkdir rules/<new-category>
   ```

2. **Update the validation script** if needed — the script auto-discovers `.json` files under `rules/` recursively (excluding `rules/schema/`), so no code changes are needed unless you want to enforce category-specific rules.

3. **Update documentation:**
   - Add the new category to `README.md` (Directory Structure + Rule Categories sections)
   - Add it to `CONTRIBUTING.md` (Directory Structure + Choosing the Right Category sections)
   - Update the repo-organiser skill (this file)

4. **Update the CI path filter** if the new directory is outside `rules/` (unlikely but possible):
   ```yaml
   # .github/workflows/validate-rules.yml
   paths:
     - 'rules/**/*.json'
   ```

### Reserved Directory: `rules/schema/`

This directory contains infrastructure files, **not rules**:
- `sonarqube-rule.schema.json` — JSON Schema for IDE validation
- `rule-template.json` — Starter template for new rules

The validation script explicitly excludes this directory from rule discovery.

---

## Naming Conventions

### File Names
- **Format:** kebab-case with `.json` extension
- **Pattern:** `^[a-z][a-z0-9]*(-[a-z0-9]+)*\.json$`
- **Examples:** `sql-injection.json`, `god-class.json`, `n-plus-one-query.json`

### Key ↔ Filename Matching
The `key` field inside the JSON **must exactly match** the filename (without `.json`):
- File: `sql-injection.json` → `"key": "sql-injection"` ✓
- File: `sql-injection.json` → `"key": "sqlInjection"` ✗ (error)

### Uniqueness
Rule keys must be unique across **all categories**. Check before creating:
```bash
grep -r '"key"' rules/ --include='*.json' | grep -v schema | sort
```

---

## IDE Configuration

### VS Code (Pre-Configured)

The file `.vscode/settings.json` maps the JSON Schema to all rule files:

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

This provides:
- **Red squiggles** on invalid enum values, missing fields, wrong types
- **Autocomplete** for enum values (`severity`, `type`, `status`, etc.)
- **Hover documentation** from schema descriptions

### IntelliJ IDEA / WebStorm

Add a JSON Schema mapping in Settings → Languages & Frameworks → Schemas and DTDs → JSON Schema Mappings:
- Schema file: `rules/schema/sonarqube-rule.schema.json`
- File path pattern: `rules/**/*.json` (exclude `rules/schema/`)

### Other Editors

Any editor supporting JSON Schema (draft-07) can use `rules/schema/sonarqube-rule.schema.json`. Point the schema at `rules/**/*.json` files.

---

## Tooling Overview

The repository has a layered validation approach:

| Layer | Tool | What it catches | When it runs |
|---|---|---|---|
| **IDE** | JSON Schema + `.vscode/settings.json` | Type errors, enum violations, missing required fields | Real-time as you type |
| **Local** | `scripts/validate-rules.py` | All of the above + cross-field consistency (key↔filename, type↔impact, severity alignment) | On demand |
| **CI** | GitHub Actions workflow | All of the above in standard + strict mode, plus formatting checks | Every push/PR |

### How They Complement Each Other

- **JSON Schema** provides instant feedback but can't check key↔filename or type↔impact alignment
- **Validation script** catches everything including cross-field logic, but you have to run it
- **CI pipeline** runs the script automatically so nothing slips through to `main`

---

## Bulk Operations

### Re-categorise a Rule

```bash
# Move the file
mv rules/code-smells/my-rule.json rules/maintainability/my-rule.json

# Validate (key doesn't change, just the directory)
python3 scripts/validate-rules.py rules/maintainability/my-rule.json
```

### Rename a Rule

Both the file AND the `key` field must change:

```bash
# Rename the file
mv rules/security/old-name.json rules/security/new-name.json

# Edit the key field inside the file
# Change: "key": "old-name"  →  "key": "new-name"

# Validate
python3 scripts/validate-rules.py rules/security/new-name.json
```

### Audit All Rules for Consistency

```bash
# Full audit
python3 scripts/validate-rules.py

# Strict audit (warnings = errors)
python3 scripts/validate-rules.py --strict
```

### List All Rules by Category

```bash
find rules -name '*.json' -not -path 'rules/schema/*' | sort
```

### Count Rules per Category

```bash
for dir in rules/*/; do
  [[ "$dir" == "rules/schema/" ]] && continue
  count=$(find "$dir" -name '*.json' | wc -l)
  echo "$dir: $count rules"
done
```

### Find Duplicate Keys

```bash
grep -rh '"key"' rules/ --include='*.json' | grep -v schema | sort | uniq -d
```

---

## Contributing Guide Reference

The file `CONTRIBUTING.md` contains:
- Quick start steps for new contributors
- Category selection guide
- Step-by-step rule creation instructions
- Schema reference table
- Formatting guidelines
- Common mistakes table
- IDE setup instructions

When onboarding a new contributor, point them to `CONTRIBUTING.md` first. It covers everything they need to create a valid rule and open a successful PR.

---

## Important Notes

- The `rules/schema/` directory is infrastructure — never add rule definitions there.
- Rule keys must be globally unique across all categories.
- File names and keys must always be kept in sync. The validator will catch mismatches.
- The `.vscode/settings.json` is committed to the repo so all VS Code users get schema validation automatically.
- When adding new categories, the validation script auto-discovers them — no script changes needed.
- Keep `CONTRIBUTING.md` and `README.md` updated when the structure changes.
