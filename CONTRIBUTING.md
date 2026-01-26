# Contributing to SonarQube Rules

Thank you for your interest in contributing! This document provides guidelines for adding or modifying rules in this repository.

## Table of Contents

- [Getting Started](#getting-started)
- [Adding a New Rule](#adding-a-new-rule)
- [Modifying an Existing Rule](#modifying-an-existing-rule)
- [Validation](#validation)
- [Pull Request Process](#pull-request-process)
- [Rule Quality Checklist](#rule-quality-checklist)

---

## Getting Started

### Prerequisites

- Git
- A JSON editor (VS Code recommended)
- `jq` command-line tool (for validation scripts)
- Node.js (optional, for schema validation)

### Repository Structure

```
rules/
├── security/           # Security vulnerability rules
├── code-smells/        # Code quality rules
├── performance/        # Performance rules
└── maintainability/    # Maintainability rules

schemas/
└── rule-schema.json    # JSON Schema for validation

scripts/
├── validate-rules.sh   # Validation script
└── generate-index.sh   # Index generator
```

---

## Adding a New Rule

### 1. Choose the Right Category

| Category | Use For |
|----------|---------|
| `security/` | Vulnerabilities exploitable by attackers |
| `code-smells/` | Design issues, technical debt |
| `performance/` | Slowdowns, memory issues, resource problems |
| `maintainability/` | Code that's hard to understand or modify |

### 2. Create the Rule File

Create a new `.json` file in the appropriate category directory. The filename should match the rule key.

```bash
# Example: creating a new security rule
touch rules/security/my-new-rule.json
```

### 3. Use the Rule Template

```json
{
  "key": "my-new-rule",
  "name": "My New Rule Name",
  "description": "Clear, detailed description of what this rule detects and why it's a problem. Include the impact and potential consequences.",
  "severity": "MAJOR",
  "type": "CODE_SMELL",
  "tags": ["category-tag", "specific-tag"],
  "remediation": {
    "constantCost": "15min",
    "examples": [
      {
        "before": "// Code that triggers this rule\nproblematicCode();",
        "after": "// Corrected code\nfixedCode();"
      }
    ]
  },
  "impacts": [
    {
      "softwareQuality": "MAINTAINABILITY",
      "severity": "MEDIUM"
    }
  ],
  "defaultSeverity": "MAJOR",
  "status": "READY",
  "debt": {
    "function": "CONSTANT_ISSUE",
    "offset": "15min"
  }
}
```

### 4. Field Guidelines

#### Key
- Lowercase, hyphenated
- Descriptive of the issue
- Must match filename (without `.json`)

#### Severity

| Level | When to Use |
|-------|-------------|
| `BLOCKER` | Critical security flaw, data loss, crashes |
| `CRITICAL` | Security vulnerabilities, major bugs |
| `MAJOR` | Significant code smells, moderate issues |
| `MINOR` | Minor quality issues, style violations |
| `INFO` | Best practice suggestions |

#### Type

| Type | When to Use |
|------|-------------|
| `VULNERABILITY` | Security issues |
| `BUG` | Code that is demonstrably wrong |
| `CODE_SMELL` | Maintainability/design issues |

#### Tags
Include at least:
- Category tag (`security`, `performance`, etc.)
- One or more specific tags

Common tags:
- `owasp-top-10`, `injection`, `authentication` (security)
- `solid`, `design`, `refactoring` (code-smells)
- `memory`, `database`, `optimization` (performance)
- `readability`, `documentation`, `naming` (maintainability)

---

## Modifying an Existing Rule

1. **Never change the `key`** - it may be referenced in quality profiles
2. Update the `description` if needed
3. Keep remediation examples current
4. Update the CHANGELOG

---

## Validation

### Run Local Validation

```bash
# Make scripts executable (first time only)
chmod +x scripts/*.sh

# Validate all rules
./scripts/validate-rules.sh

# Generate/update the rules index
./scripts/generate-index.sh
```

### Schema Validation (Optional)

```bash
# Install ajv-cli
npm install -g ajv-cli

# Validate a single rule
ajv validate -s schemas/rule-schema.json -d rules/security/my-rule.json --strict=false

# Validate all rules
for f in rules/*/*.json; do ajv validate -s schemas/rule-schema.json -d "$f" --strict=false; done
```

---

## Pull Request Process

1. **Fork** the repository
2. **Create a branch** for your changes
   ```bash
   git checkout -b add-rule/my-new-rule
   ```
3. **Add or modify** rule files
4. **Run validation** locally
5. **Update CHANGELOG.md** with your changes
6. **Submit a PR** with a clear description

### PR Title Format

- Adding rules: `feat: add [rule-key] rule`
- Modifying rules: `fix: update [rule-key] description`
- Multiple rules: `feat: add [category] rules for [topic]`

---

## Rule Quality Checklist

Before submitting, verify:

- [ ] JSON is valid (no syntax errors)
- [ ] All required fields are present
- [ ] `key` matches filename
- [ ] `severity` is appropriate for the issue
- [ ] `type` correctly classifies the issue
- [ ] `description` clearly explains the problem and impact
- [ ] `tags` include category and relevant specific tags
- [ ] `remediation.examples` has clear before/after code
- [ ] `debt.offset` is a realistic time estimate
- [ ] Validation script passes
- [ ] CHANGELOG is updated

---

## Questions?

If you're unsure about anything, open an issue to discuss before creating a PR.
