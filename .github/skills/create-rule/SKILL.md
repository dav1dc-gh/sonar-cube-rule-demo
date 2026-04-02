---
name: create-rule
description: "Create new SonarQube rule JSON files following repository conventions. Use when: adding a new rule, scaffolding a rule from a description, generating rules for a specific vulnerability or code pattern, or expanding rule coverage in any category."
argument-hint: "Describe the rule to create: what it detects, which category, and severity"
---

# Create Rule

## Keywords

create, add, new rule, scaffold, generate, rule file, vulnerability, code smell, performance rule, maintainability rule, security rule, OWASP, injection, XSS, SSRF, god class, dead code, N+1, memory leak, naming convention, nesting, template, JSON, category

## When to Use

- Adding a new SonarQube rule to any category
- Scaffolding a rule from a natural-language description
- Generating a rule for a specific vulnerability, code smell, performance issue, or maintainability concern
- Expanding coverage in a category

## Procedure

### 1. Determine Category

Ask or infer which category the rule belongs to:

| Category | Directory | When to Use |
|----------|-----------|-------------|
| Security | `rules/security/` | Exploitable vulnerabilities (injection, XSS, SSRF, auth issues) |
| Code Smells | `rules/code-smells/` | Structural quality issues (bad design, complexity, duplication) |
| Performance | `rules/performance/` | Runtime efficiency problems (N+1 queries, memory leaks, blocking I/O) |
| Maintainability | `rules/maintainability/` | Long-term code health (naming, nesting, documentation, dependencies) |

**Ambiguous?** Choose by primary concern, then use `tags` to cross-reference.

### 2. Choose Key and Filename

- Format: `lower-kebab-case`
- Must clearly convey what the rule detects
- Filename: `<key>.json`
- **Check for duplicates**: search existing rules to ensure no overlap

### 3. Read Category Instructions

Before creating, read the appropriate `.github/instructions/` file for category-specific constraints:
- `security-rules.instructions.md` for `rules/security/`
- `code-smells-rules.instructions.md` for `rules/code-smells/`
- `performance-rules.instructions.md` for `rules/performance/`
- `maintainability-rules.instructions.md` for `rules/maintainability/`

### 4. Build the Rule JSON

Use this template, filling in all fields according to category constraints:

```json
{
  "key": "<lower-kebab-case-key>",
  "name": "<Human-Readable Name>",
  "description": "<What it detects, why it's a problem, and the consequences.>",
  "severity": "<BLOCKER|CRITICAL|MAJOR|MINOR|INFO>",
  "type": "<BUG|VULNERABILITY|CODE_SMELL>",
  "tags": ["<category-tag>", "<additional-tags>"],
  "remediation": {
    "constantCost": "<Nmin|Nh>",
    "examples": [
      {
        "before": "<Realistic bad code>",
        "after": "<Fixed code using best practices>"
      }
    ]
  },
  "impacts": [
    {
      "softwareQuality": "<SECURITY|RELIABILITY|MAINTAINABILITY>",
      "severity": "<HIGH|MEDIUM|LOW>"
    }
  ],
  "defaultSeverity": "<must match severity>",
  "status": "READY",
  "debt": {
    "function": "CONSTANT_ISSUE",
    "offset": "<Nmin|Nh>"
  }
}
```

### 5. Category-Specific Constraints Quick Reference

| Constraint | Security | Code Smells | Performance | Maintainability |
|-----------|----------|-------------|-------------|-----------------|
| `type` | `VULNERABILITY` | `CODE_SMELL` | `CODE_SMELL` or `BUG` | `CODE_SMELL` |
| `severity` | `CRITICAL`/`BLOCKER` | Usually `MAJOR` | `CRITICAL`/`MAJOR` | `MAJOR`/`MINOR` |
| `impacts.softwareQuality` | `SECURITY` | `MAINTAINABILITY` | `RELIABILITY` | `MAINTAINABILITY` |
| Required first tag | `security` | `code-smell` | `performance` | `maintainability` |
| `params` | Rare (no thresholds) | Common (thresholds) | Sometimes | Common (thresholds) |
| `debt` model | `CONSTANT_ISSUE` | Either | Either | Either |

### 6. Add Params (if threshold-based)

If the rule's detection depends on a measurable quantity, add `params`:

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

Use `LINEAR` debt when params exist and fix cost scales with the measured value.

### 7. Validate

After creating the file:
1. Confirm valid JSON (no trailing commas, proper quoting)
2. Confirm `key` matches filename
3. Confirm `severity` === `defaultSeverity`
4. Confirm category tag is present in `tags`
5. Confirm `type` matches category constraints
6. Run `python scripts/validate_rules.py` if available

### 8. Update Documentation

- Update README.md rule tables if needed
- Update `.github/copilot-instructions.md` rule counts and tables
- Log the addition in AI-HISTORY.md

## Remediation Example Quality Standards

- **`before`**: Realistic code a developer would write — not pseudocode
- **`after`**: Industry best-practice fix with specific APIs/patterns
- Java is the primary target language; language-agnostic when possible
- Include comments explaining why the fix works when non-obvious
