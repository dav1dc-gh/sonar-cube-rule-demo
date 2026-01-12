# SonarQube Rules Files - AI Assistant Custom Instructions

## Overview

This repository contains a collection of SonarQube rule definitions designed to detect code quality issues, security vulnerabilities, performance problems, and maintainability concerns. Each rule is defined in JSON format following SonarQube's rule specification standards. Your role is to help users create, manage, understand, and contribute to these rule files effectively.

## Directory Structure

The rules are organized by category in the `rules/` directory:

```
rules/
├── security/          # Security vulnerability rules (10 rules)
├── code-smells/       # Code quality and maintainability issues (8 rules)
├── performance/       # Performance-related rules (7 rules)
└── maintainability/   # Code maintainability rules (7 rules)
```

When creating new rules, always place them in the appropriate category directory. If uncertain about categorization, consider the primary concern the rule addresses.

---

## Rule Categories

### 1. Security Rules (`rules/security/`)

Security rules detect vulnerabilities that could be exploited by attackers. These are typically the highest priority rules.

| Rule File | Description |
|-----------|-------------|
| `command-injection.json` | OS command injection vulnerabilities |
| `csrf-vulnerability.json` | Missing CSRF protection |
| `hardcoded-credentials.json` | Hardcoded passwords, API keys, tokens |
| `insecure-deserialization.json` | Unsafe deserialization leading to RCE |
| `insecure-random.json` | Predictable random number generators |
| `path-traversal.json` | File path traversal vulnerabilities |
| `sensitive-data-exposure.json` | Logging of sensitive information |
| `sql-injection.json` | SQL injection vulnerabilities |
| `weak-cryptography.json` | Weak/deprecated cryptographic algorithms |
| `xss-vulnerability.json` | Cross-Site Scripting risks |

**Typical Properties:**
- Severity: `BLOCKER` or `CRITICAL`
- Type: `VULNERABILITY`
- Tags: Include `security`, `owasp-top-10` when applicable

### 2. Code Smells (`rules/code-smells/`)

Code smells indicate design problems that may not be bugs but reduce code quality and maintainability.

| Rule File | Description |
|-----------|-------------|
| `complex-methods.json` | High cyclomatic complexity |
| `dead-code.json` | Unreachable/unused code |
| `duplicate-code.json` | Code duplication |
| `empty-catch-block.json` | Silent exception swallowing |
| `feature-envy.json` | Methods using other classes' features excessively |
| `god-class.json` | Classes with too many responsibilities |
| `long-parameter-list.json` | Methods with too many parameters |
| `magic-numbers.json` | Unnamed numerical constants |

**Typical Properties:**
- Severity: `MAJOR` or `MINOR`
- Type: `CODE_SMELL`
- Tags: Include `code-smell`, relevant design principle tags

### 3. Performance Rules (`rules/performance/`)

Performance rules identify code patterns that cause runtime inefficiencies.

| Rule File | Description |
|-----------|-------------|
| `inefficient-collection-usage.json` | Improper collection usage |
| `inefficient-loops.json` | Loop performance issues |
| `memory-leaks.json` | Memory leak patterns |
| `n-plus-one-query.json` | Database queries in loops |
| `string-concatenation-in-loop.json` | String `+` operator in loops |
| `synchronous-io-in-async.json` | Blocking I/O in async contexts |
| `unnecessary-boxing.json` | Primitive/wrapper conversions |

**Typical Properties:**
- Severity: `CRITICAL` or `MAJOR`
- Type: `BUG` or `CODE_SMELL`
- Tags: Include `performance`

### 4. Maintainability Rules (`rules/maintainability/`)

Maintainability rules detect patterns that make code harder to understand, modify, or extend.

| Rule File | Description |
|-----------|-------------|
| `deep-nesting.json` | Excessive nesting levels |
| `hardcoded-urls.json` | URLs that should be externalized |
| `inconsistent-naming.json` | Naming convention violations |
| `long-methods.json` | Methods exceeding length thresholds |
| `missing-javadoc.json` | Missing documentation comments |
| `missing-null-check.json` | Potential null pointer dereferences |
| `too-many-parameters.json` | Excessive method parameters |

**Typical Properties:**
- Severity: `MAJOR` or `MINOR`
- Type: `CODE_SMELL`
- Tags: Include `maintainability`

---

## Rule File Structure

Every rule file must be valid JSON and follow this structure:

### Required Fields

```json
{
  "key": "unique-rule-identifier",
  "name": "Human-Readable Rule Name",
  "description": "Detailed explanation of what the rule detects and why it matters.",
  "severity": "CRITICAL",
  "type": "VULNERABILITY",
  "tags": ["relevant", "tags"],
  "status": "READY"
}
```

### Optional Fields

```json
{
  "remediation": {
    "constantCost": "30min",
    "examples": [
      {
        "before": "// Problematic code example",
        "after": "// Corrected code example"
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
  "debt": {
    "function": "CONSTANT_ISSUE",
    "offset": "30min"
  },
  "params": [
    {
      "key": "paramKey",
      "name": "Parameter Name",
      "description": "What this parameter controls",
      "defaultValue": "100",
      "type": "INTEGER"
    }
  ]
}
```

### Field Reference

| Field | Required | Description |
|-------|----------|-------------|
| `key` | Yes | Unique identifier (lowercase, hyphenated) |
| `name` | Yes | Display name for the rule |
| `description` | Yes | Full explanation of the rule's purpose |
| `severity` | Yes | `BLOCKER`, `CRITICAL`, `MAJOR`, `MINOR`, or `INFO` |
| `type` | Yes | `VULNERABILITY`, `BUG`, or `CODE_SMELL` |
| `tags` | Yes | Array of relevant tags for categorization |
| `status` | Yes | `READY`, `BETA`, or `DEPRECATED` |
| `remediation` | No | Fix guidance with time estimate and examples |
| `impacts` | No | Software quality impacts |
| `defaultSeverity` | No | Default severity if overridable |
| `debt` | No | Technical debt calculation method |
| `params` | No | Configurable parameters for the rule |

### Severity Guidelines

| Severity | Use When |
|----------|----------|
| `BLOCKER` | Security vulnerabilities that must be fixed immediately (e.g., hardcoded credentials) |
| `CRITICAL` | Serious issues likely to cause bugs or security problems (e.g., SQL injection, memory leaks) |
| `MAJOR` | Important issues affecting maintainability or reliability (e.g., god classes, long methods) |
| `MINOR` | Issues that should be fixed but have lower impact (e.g., naming conventions) |
| `INFO` | Informational findings, suggestions for improvement |

### Type Guidelines

| Type | Use When |
|------|----------|
| `VULNERABILITY` | Security issues that can be exploited |
| `BUG` | Code that is demonstrably wrong or will fail at runtime |
| `CODE_SMELL` | Design issues that reduce code quality but don't cause immediate failures |

### Technical Debt Functions

| Function | Use When |
|----------|----------|
| `CONSTANT_ISSUE` | Fixed time to fix regardless of scope |
| `LINEAR` | Time scales with issue scope (uses `coefficient`) |

---

## Best Practices

### When Creating New Rules

1. **Choose the correct category** - Place the rule in the most appropriate directory
2. **Use descriptive keys** - Format: `lowercase-hyphenated-descriptive-name`
3. **Write clear descriptions** - Explain what is detected, why it's a problem, and the potential impact
4. **Provide remediation examples** - Include realistic before/after code samples
5. **Assign appropriate severity** - Match severity to actual risk/impact
6. **Add relevant tags** - Help users discover and filter rules
7. **Set realistic debt estimates** - Consider actual time needed to fix issues

### When Modifying Existing Rules

1. **Preserve the key** - Changing keys breaks existing quality profiles
2. **Update description if scope changes** - Keep documentation accurate
3. **Re-evaluate severity** - Ensure severity still matches the rule's scope
4. **Update examples** - Ensure they reflect current best practices

### Common Tags to Use

| Category | Suggested Tags |
|----------|----------------|
| Security | `security`, `owasp-top-10`, `injection`, `authentication`, `encryption` |
| Code Smells | `code-smell`, `design`, `solid`, `maintainability`, `readability` |
| Performance | `performance`, `memory`, `database`, `optimization` |
| Maintainability | `maintainability`, `documentation`, `naming`, `complexity` |

### File Naming Convention

- Use lowercase with hyphens: `rule-name.json`
- Be descriptive but concise
- Match the rule's `key` field

---

## Example: Creating a New Rule

When asked to create a new rule, follow this template:

```json
{
  "key": "new-rule-name",
  "name": "Descriptive Rule Name",
  "description": "Clear explanation of what the rule detects, why it's problematic, and what impact it has on the codebase.",
  "severity": "MAJOR",
  "type": "CODE_SMELL",
  "tags": ["relevant-tag-1", "relevant-tag-2"],
  "remediation": {
    "constantCost": "15min",
    "examples": [
      {
        "before": "// Code that triggers the rule",
        "after": "// Corrected code that follows best practices"
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

---

## Validation Checklist

Before finalizing any rule file, verify:

- [ ] Valid JSON syntax
- [ ] All required fields present (`key`, `name`, `description`, `severity`, `type`, `tags`, `status`)
- [ ] `key` is unique across all rules
- [ ] `key` matches filename (without `.json` extension)
- [ ] `severity` is valid: `BLOCKER`, `CRITICAL`, `MAJOR`, `MINOR`, or `INFO`
- [ ] `type` is valid: `VULNERABILITY`, `BUG`, or `CODE_SMELL`
- [ ] `tags` array is not empty
- [ ] `status` is valid: `READY`, `BETA`, or `DEPRECATED`
- [ ] Remediation examples are realistic and helpful
- [ ] Description clearly explains what and why

---

## Quick Reference Commands

When helping users, you may suggest these operations:

- **List all rules in a category**: Browse the appropriate `rules/[category]/` directory
- **Find rules by tag**: Search for tags in rule JSON files
- **Validate JSON**: Ensure files are valid JSON before committing
- **Check for duplicate keys**: Verify no two rules share the same `key`
