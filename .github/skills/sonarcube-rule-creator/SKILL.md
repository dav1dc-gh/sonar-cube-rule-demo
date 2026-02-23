---
name: sonarcube-rule-creator
description: Scaffolds new SonarQube rule definition JSON files from the project template, ensures correct category placement, populates all required fields, and validates the result. Use when creating, adding, or scaffolding new SonarQube rules. Keywords: sonarqube, sonar, create, new, rule, scaffold, template, add, generate, json, code-smell, vulnerability, security, maintainability, performance.
---

# SonarQube Rule Creator

## Purpose

This skill guides the creation of new SonarQube rule definition JSON files. It uses the project's rule template at `rules/schema/rule-template.json`, places the file in the correct category directory, ensures all required fields are populated with valid values, and runs validation to catch errors before a PR is opened.

Activate this skill whenever the user:
- Asks to create, add, or scaffold a new SonarQube rule
- Wants to generate a rule definition for a specific code pattern
- Needs help deciding which category a rule belongs to
- Asks how to get started adding rules to this repository

---

## Workflow

### Step 1: Determine the Category

Choose the correct directory based on the rule's type and focus:

| Rule Type | Impact Focus | Directory |
|---|---|---|
| `CODE_SMELL` | General quality | `rules/code-smells/` |
| `CODE_SMELL` | Maintainability | `rules/maintainability/` |
| `CODE_SMELL` / `BUG` | Performance | `rules/performance/` |
| `VULNERABILITY` / `SECURITY_HOTSPOT` | Security | `rules/security/` |

**Decision guide:**
- If the rule detects a security flaw → `security/`
- If the rule detects a performance bottleneck → `performance/`
- If the rule detects a maintainability concern (naming, documentation, structure) → `maintainability/`
- If the rule detects a general code smell (duplication, complexity, design) → `code-smells/`

### Step 2: Choose the Rule Key

The rule key must:
- Be **kebab-case**: `^[a-z][a-z0-9]*(-[a-z0-9]+)*$`
- **Exactly match the filename** (without `.json`)
- Be **unique** across all categories

Before creating, check for key conflicts:
```bash
find rules -name '*.json' | xargs grep -l '"key"' | sort
```

### Step 3: Create the File from Template

Start from the template at `rules/schema/rule-template.json`:

```json
{
  "key": "rule-key-here",
  "name": "Rule Name in Title Case",
  "description": "One or two sentences explaining what the rule detects and why it matters.",
  "severity": "MAJOR",
  "type": "CODE_SMELL",
  "tags": ["tag-one", "tag-two"],
  "remediation": {
    "constantCost": "30min",
    "examples": [
      {
        "before": "// Problematic code pattern",
        "after": "// Corrected code pattern"
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
    "offset": "30min"
  }
}
```

### Step 4: Populate All Fields

Follow these rules precisely:

#### Required Fields

| Field | Constraints |
|---|---|
| `key` | Kebab-case, matches filename |
| `name` | Title Case, concise display name |
| `description` | 1–2 sentences, ≤ 300 characters |
| `severity` | One of: `INFO`, `MINOR`, `MAJOR`, `CRITICAL`, `BLOCKER` |
| `type` | One of: `CODE_SMELL`, `BUG`, `VULNERABILITY`, `SECURITY_HOTSPOT` |
| `tags` | ≥ 1 kebab-case tag |
| `remediation.constantCost` | Duration: `^\d+(min\|h\|d)$` (e.g. `30min`, `1h`, `4h`) |
| `remediation.examples` | ≥ 1 before/after pair with non-empty strings |
| `impacts` | ≥ 1 entry (see alignment rules below) |
| `defaultSeverity` | **Must exactly match `severity`** |
| `status` | One of: `READY`, `BETA`, `DEPRECATED`, `REMOVED` |
| `debt` | See debt function rules below |

#### Type ↔ Impact Alignment (Critical)

These must be consistent or validation will warn/fail:

- `VULNERABILITY` or `SECURITY_HOTSPOT` → **must** include `{ "softwareQuality": "SECURITY", ... }` in impacts
- `CODE_SMELL` → **must** include `{ "softwareQuality": "MAINTAINABILITY", ... }` in impacts
- `BUG` → should include `{ "softwareQuality": "RELIABILITY", ... }` in impacts

You may include additional impacts (e.g. a `CODE_SMELL` can also impact `RELIABILITY`), but the primary alignment must be present.

#### Debt Function Rules

| `debt.function` | Required fields |
|---|---|
| `CONSTANT_ISSUE` | `offset` (e.g. `"30min"`) |
| `LINEAR` | `coefficient` (e.g. `"10min"`) |
| `LINEAR_OFFSET` | Both `coefficient` and `offset` |

Duration values must match: `^\d+(min|h|d)$`

#### Optional: `params` Array

Only include when the rule has configurable thresholds:

```json
"params": [
  {
    "key": "maxLines",
    "name": "Maximum Lines",
    "description": "Maximum number of lines allowed",
    "defaultValue": "500",
    "type": "INTEGER"
  }
]
```

- `key`: camelCase
- `type`: One of `INTEGER`, `FLOAT`, `BOOLEAN`, `STRING`, `TEXT`
- `defaultValue`: Always a string, even for numeric types

### Step 5: Validate Immediately

After creating the file, always run validation:

```bash
# Validate the new file
python3 scripts/validate-rules.py rules/<category>/<rule-key>.json

# Or validate everything
python3 scripts/validate-rules.py
```

Fix any errors before considering the rule complete.

### Step 6: Formatting

Ensure the file:
- Uses **2-space indentation** (no tabs)
- Has **no trailing whitespace**
- Ends with a **single newline character**
- Has fields in **canonical order**: `key`, `name`, `description`, `severity`, `type`, `tags`, `remediation`, `impacts`, `defaultSeverity`, `status`, `debt`, `params`

---

## Severity Selection Guide

Use this to help choose the appropriate severity:

| Severity | When to use |
|---|---|
| `BLOCKER` | Prevents the application from working or causes data loss |
| `CRITICAL` | Security vulnerabilities, potential crashes, data corruption |
| `MAJOR` | Significant quality issues affecting maintenance or reliability |
| `MINOR` | Minor quality issues, style violations |
| `INFO` | Informational, suggestions for improvement |

---

## Examples

### Example 1: Creating a Security Rule

User asks: "Create a rule for detecting hardcoded API keys"

1. Category: `security/` (it's a vulnerability)
2. Key: `hardcoded-api-keys`
3. File: `rules/security/hardcoded-api-keys.json`

```json
{
  "key": "hardcoded-api-keys",
  "name": "Hardcoded API Keys",
  "description": "Detects API keys, tokens, and secrets hardcoded directly in source code instead of using environment variables or secret management.",
  "severity": "CRITICAL",
  "type": "VULNERABILITY",
  "tags": ["security", "credentials", "secrets", "owasp-top-10"],
  "remediation": {
    "constantCost": "15min",
    "examples": [
      {
        "before": "private static final String API_KEY = \"sk-abc123def456\";",
        "after": "private static final String API_KEY = System.getenv(\"API_KEY\");"
      }
    ]
  },
  "impacts": [
    {
      "softwareQuality": "SECURITY",
      "severity": "HIGH"
    }
  ],
  "defaultSeverity": "CRITICAL",
  "status": "READY",
  "debt": {
    "function": "CONSTANT_ISSUE",
    "offset": "15min"
  }
}
```

### Example 2: Creating a Performance Rule with Parameters

User asks: "Create a rule for detecting methods that are too slow"

1. Category: `performance/` 
2. Key: `slow-method-detection`
3. File: `rules/performance/slow-method-detection.json`

```json
{
  "key": "slow-method-detection",
  "name": "Slow Method Detection",
  "description": "Detects methods containing patterns known to cause poor performance, such as nested loops over large collections or repeated database calls.",
  "severity": "MAJOR",
  "type": "CODE_SMELL",
  "tags": ["performance", "optimization", "complexity"],
  "remediation": {
    "constantCost": "1h",
    "examples": [
      {
        "before": "for (Item a : listA) {\n  for (Item b : listB) {\n    if (a.getId().equals(b.getId())) { ... }\n  }\n}",
        "after": "Map<String, Item> mapB = listB.stream().collect(Collectors.toMap(Item::getId, identity()));\nfor (Item a : listA) {\n  Item b = mapB.get(a.getId());\n}"
      }
    ]
  },
  "impacts": [
    {
      "softwareQuality": "MAINTAINABILITY",
      "severity": "LOW"
    },
    {
      "softwareQuality": "RELIABILITY",
      "severity": "MEDIUM"
    }
  ],
  "defaultSeverity": "MAJOR",
  "status": "READY",
  "debt": {
    "function": "LINEAR",
    "coefficient": "15min"
  },
  "params": [
    {
      "key": "maxNestingDepth",
      "name": "Maximum Loop Nesting",
      "description": "Maximum allowed loop nesting depth before flagging",
      "defaultValue": "2",
      "type": "INTEGER"
    }
  ]
}
```

---

## Important Notes

- Always use the template at `rules/schema/rule-template.json` as your starting point.
- Never place rule files in `rules/schema/` — that directory is reserved for the schema and template.
- The JSON Schema at `rules/schema/sonarqube-rule.schema.json` provides real-time VS Code validation; red squiggles will appear on invalid fields when the `.vscode/settings.json` is active.
- Run `python3 scripts/validate-rules.py` after creating any rule — it catches cross-field consistency issues that the JSON Schema alone cannot detect (e.g. key↔filename match, type↔impact alignment).
- When creating multiple related rules, validate each one individually before bulk-validating the entire repository.
