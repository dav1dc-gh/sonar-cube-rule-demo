---
name: generate-docs
description: "Generate and update documentation for SonarQube rules. Use when: updating README.md, generating rule tables from JSON files, adding CI badges, writing contributing guides, syncing documentation with rule changes, or creating scripts to auto-generate docs."
---

# Generate Docs

## Keywords

documentation, README, docs, generate, update, rule table, badge, CI badge, contributing guide, auto-generate, generate_readme.py, directory tree, rule count, markdown, sync documentation

## When to Use

- Updating README.md after adding, removing, or modifying rules
- Auto-generating rule tables from the JSON files
- Adding CI status badges
- Writing or updating the contributing guide
- Creating a `scripts/generate_readme.py` script
- Syncing documentation after bulk changes

## README Structure

The README.md follows this structure:

```
# sonar-cube-rule-demo
## Overview
## Directory Structure (tree view)
## Rule Categories
### Security (N rules) — table of rules with descriptions
### Code Smells (N rules)
### Performance (N rules)
### Maintainability (N rules)
## Validation — how to run validation locally
## Contributing — steps for adding new rules
```

## Rule Table Format

Each category section contains a markdown table:

```markdown
### Security (15 rules)
| Rule | Description |
|------|-------------|
| `command-injection` | Detects OS command injection vulnerabilities... |
| `sql-injection` | Detects potential SQL injection vulnerabilities... |
```

**Source of truth**: The `key` and `description` fields from each rule JSON file.

## Auto-Generation Script

File: `scripts/generate_readme.py`

The script should:

1. Scan `rules/` for all category directories
2. For each category, read all `.json` files
3. Extract `key` and `description` from each file
4. Sort rules alphabetically by `key`
5. Count rules per category
6. Generate the markdown tables
7. Either output to stdout or update README.md in-place (preserve non-generated sections)

### Section markers for in-place update:

```markdown
<!-- BEGIN GENERATED RULES -->
...generated content...
<!-- END GENERATED RULES -->
```

## CI Badge

Add at the top of README.md after the title:

```markdown
![Validate Rules](https://github.com/<owner>/<repo>/actions/workflows/validate-rules.yml/badge.svg)
```

Replace `<owner>/<repo>` with the actual GitHub repository path.

## Contributing Section Template

```markdown
## Contributing

### Adding a New Rule

1. Choose the appropriate category directory under `rules/`
2. Create a JSON file named `<rule-key>.json` using lower-kebab-case
3. Follow the schema defined in `schema/rule-schema.json`
4. Include realistic before/after remediation examples
5. Run `python scripts/validate_rules.py` to validate
6. Update this README (or run `python scripts/generate_readme.py`)
7. Submit a pull request

### Validating Rules

```bash
pip install -r requirements.txt
python scripts/validate_rules.py
```
```

## Directory Tree Update

When rules are added or removed, update the directory tree in README.md to reflect the current file listing. Use `find rules/ -name '*.json' | sort` to get the current state.

## Procedure

1. Read all rule JSON files to get current `key` and `description` values
2. Count rules per category
3. Generate/update the rule tables in README.md
4. Update the directory tree if files were added/removed
5. Update rule counts in section headers
6. Verify the README is valid markdown
