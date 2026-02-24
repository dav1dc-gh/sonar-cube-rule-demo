---
name: rule-creation-wizard
description: Guided creation of a new SonarQube rule JSON file with full schema compliance and validation. Use this when asked to create, add, or draft a new rule.
---

# Rule Creation Wizard

Follow this process to create a new SonarQube rule JSON file.

## Step 1 — Determine the category

Ask the user what their rule detects, then choose the best-fit category:

| Category | Directory | Primary concern |
|---|---|---|
| Security | `rules/security/` | Exploitable vulnerabilities (injection, auth, crypto) |
| Code Smells | `rules/code-smells/` | Design/quality problems (complexity, duplication, coupling) |
| Performance | `rules/performance/` | Runtime inefficiencies (N+1, leaks, boxing) |
| Maintainability | `rules/maintainability/` | Long-term code health (naming, nesting, documentation) |

If the rule spans multiple concerns, choose the **primary** concern.

## Step 2 — Check for duplicates

Before creating a new rule, search existing rules for overlap:

1. Run `grep -ril "<keywords>" rules/` to find rules with similar terms in their name or description.
2. Read any matches and assess whether the new rule is genuinely distinct.
3. If a near-duplicate exists, inform the user and offer to enhance the existing rule instead.

## Step 3 — Generate the key and filename

- Use **kebab-case** for the key (e.g., `missing-error-handling`).
- The filename must be `<key>.json` and live in the chosen category directory.
- The `key` field inside the JSON must exactly match the filename without `.json`.

## Step 4 — Populate all required fields

Create the JSON file with every required field. Use this template:

```json
{
  "key": "<kebab-case-key>",
  "name": "<Human-Readable Name>",
  "description": "<What the rule detects, why it matters, when it applies>",
  "severity": "<BLOCKER|CRITICAL|MAJOR|MINOR|INFO>",
  "type": "<VULNERABILITY|BUG|CODE_SMELL>",
  "tags": ["<category>", "<tag2>", "<tag3>", "<tag4>"],
  "remediation": {
    "constantCost": "<Nmin>",
    "examples": [
      {
        "before": "<realistic bad code>",
        "after": "<realistic fixed code>"
      }
    ]
  },
  "impacts": [
    {
      "softwareQuality": "<SECURITY|MAINTAINABILITY|RELIABILITY>",
      "severity": "<HIGH|MEDIUM|LOW>"
    }
  ],
  "defaultSeverity": "<must match severity>",
  "status": "READY",
  "debt": {
    "function": "CONSTANT_ISSUE",
    "offset": "<must match constantCost>"
  }
}
```

### Field rules

- **severity** must match **defaultSeverity** exactly.
- **remediation.constantCost** must match **debt.offset** for `CONSTANT_ISSUE` rules.
- **tags** must have exactly 4 entries. The first tag must match the category directory name (e.g., `security`, `code-smells`, `performance`, `maintainability`).
- **type** conventions:
  - Security rules → `VULNERABILITY`
  - Performance rules → `BUG` (if it causes incorrect behavior) or `CODE_SMELL` (if it's just slow)
  - Code smell / maintainability rules → `CODE_SMELL`
- **impacts.softwareQuality** should align with the category:
  - Security → `SECURITY`
  - Performance → `RELIABILITY` (runtime impact) or `MAINTAINABILITY` (readability only)
  - Code Smells / Maintainability → `MAINTAINABILITY`
- **Remediation examples** must be realistic and copy-pasteable. Include before (bad) and after (fixed) code.

### Severity calibration

| Severity | When to use |
|---|---|
| `BLOCKER` | Security vulnerabilities or data-loss bugs (rare) |
| `CRITICAL` | High-impact security vulnerabilities |
| `MAJOR` | Significant code smells, performance issues |
| `MINOR` | Style or convention issues |
| `INFO` | Informational, non-actionable |

### Optional: Add parameters

If the rule has configurable thresholds, add a `params` array:

```json
"params": [
  {
    "key": "maxThreshold",
    "name": "Maximum Threshold",
    "description": "Maximum allowed value",
    "defaultValue": "10",
    "type": "INTEGER"
  }
]
```

## Step 5 — Validate

Run the validation script to confirm the new rule passes all checks:

```bash
node scripts/validate-rules.js --verbose
```

If validation fails, fix the reported issues and re-run until it passes.

## Step 6 — Regenerate the catalog

```bash
node scripts/generate-catalog.js
```

This updates `RULES_CATALOG.md` to include the new rule.

## Step 7 — Record lessons learned

Append a dated entry to `HISTORY.md` documenting:
- What rule was created and why
- Any decisions made (category choice, severity rationale)
- Whether validation passed on first attempt
