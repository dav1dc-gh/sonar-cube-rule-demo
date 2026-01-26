# SonarQube Rules Files - AI Assistant Custom Instructions

You are an expert assistant for creating, managing, and understanding SonarQube Rules Files. Use these instructions to help users effectively work with this repository.

---

## Overview

This repository contains a collection of SonarQube rule definitions in JSON format. These rules are used to detect code quality issues, security vulnerabilities, performance problems, and maintainability concerns. Each rule follows SonarQube's rule specification standards and can be imported into custom rule plugins or used as references for quality profiles.

---

## Directory Structure

Rules are organized into four main categories under the `rules/` directory:

```
rules/
├── security/           # 15 security vulnerability rules
├── code-smells/        # 13 code quality and design issue rules
├── performance/        # 12 performance-related rules
└── maintainability/    # 12 code maintainability rules
```

When creating new rules, always place them in the appropriate category directory based on their primary concern.

---

## Rule Categories

### Security Rules (15 rules)
Security rules detect vulnerabilities that could be exploited by attackers. These typically have `CRITICAL` or `BLOCKER` severity and type `VULNERABILITY`.

| Rule | Description |
|------|-------------|
| `command-injection` | OS command injection via user input passed to system commands |
| `csrf-vulnerability` | Missing Cross-Site Request Forgery protection |
| `hardcoded-credentials` | Hardcoded passwords, API keys, and secrets |
| `insecure-cookie` | Cookies missing Secure, HttpOnly, or SameSite flags |
| `insecure-deserialization` | Unsafe deserialization of untrusted data (potential RCE) |
| `insecure-random` | Predictable random number generators in security contexts |
| `ldap-injection` | User input concatenated into LDAP queries |
| `open-redirect` | User-controlled redirect URLs without validation |
| `path-traversal` | Access to files outside intended directories |
| `sensitive-data-exposure` | Logging of passwords, PII, and sensitive information |
| `server-side-request-forgery` | User-controlled URLs in server-side HTTP requests |
| `sql-injection` | User input directly concatenated into SQL queries |
| `weak-cryptography` | Usage of MD5, SHA1, DES, and other weak algorithms |
| `xml-external-entity` | XML parsers processing external entities (XXE) |
| `xss-vulnerability` | User data rendered in HTML without encoding |

### Code Smells Rules (13 rules)
Code smell rules detect design issues and patterns that indicate deeper problems. These typically have type `CODE_SMELL`.

| Rule | Description |
|------|-------------|
| `complex-methods` | Methods with high cyclomatic complexity |
| `data-clumps` | Variable groups frequently appearing together |
| `dead-code` | Unreachable code, unused variables, methods, or classes |
| `duplicate-code` | Code duplication across the codebase |
| `empty-catch-block` | Catch blocks that silently swallow exceptions |
| `feature-envy` | Methods using more features from other classes |
| `god-class` | Classes too large with too many responsibilities |
| `long-parameter-list` | Methods with too many parameters |
| `magic-numbers` | Unnamed numerical constants |
| `message-chains` | Long method call chains (Law of Demeter violations) |
| `primitive-obsession` | Overuse of primitives instead of domain objects |
| `refused-bequest` | Subclasses overriding methods to do nothing |
| `speculative-generality` | Unused abstractions for hypothetical requirements |

### Performance Rules (12 rules)
Performance rules detect patterns that cause slowdowns, memory issues, or resource exhaustion. These often have type `CODE_SMELL` or `BUG`.

| Rule | Description |
|------|-------------|
| `connection-pool-exhaustion` | Connections not properly closed or returned to pool |
| `excessive-object-creation` | Unnecessary allocations in hot code paths |
| `inefficient-collection-usage` | Improper collection use, missing initial capacity |
| `inefficient-loops` | Performance anti-patterns in loops |
| `memory-leaks` | Unclosed resources, listener accumulation, GC prevention |
| `missing-lazy-initialization` | Eager initialization of potentially unused resources |
| `n-plus-one-query` | Database queries executed inside loops |
| `string-concatenation-in-loop` | String + operator inside loops |
| `synchronous-io-in-async` | Blocking I/O in async methods |
| `unbounded-collection-growth` | Collections growing without eviction policies |
| `unnecessary-boxing` | Unnecessary primitive/wrapper conversions |
| `unoptimized-regex` | Repeated regex compilation or catastrophic backtracking |

### Maintainability Rules (12 rules)
Maintainability rules detect patterns that make code harder to understand, modify, or extend.

| Rule | Description |
|------|-------------|
| `boolean-blindness` | Multiple boolean parameters with unclear meaning |
| `circular-dependencies` | Circular dependencies between modules/classes |
| `deep-nesting` | Excessive nesting levels reducing readability |
| `excessive-comments` | Redundant comments explaining "what" not "why" |
| `hardcoded-urls` | URLs and endpoints that should be externalized |
| `hidden-dependencies` | Dependencies not explicit in method signatures |
| `inconsistent-naming` | Violations of naming conventions |
| `long-methods` | Methods exceeding length thresholds |
| `missing-javadoc` | Public APIs lacking documentation |
| `missing-null-check` | Potential null pointer dereferences |
| `shotgun-surgery` | Changes requiring modifications across many classes |
| `too-many-parameters` | Methods with excessive parameter counts |

---

## Rule File Structure

Every rule file is a JSON document with the following components:

### Required Fields

```json
{
  "key": "rule-key",
  "name": "Human-Readable Rule Name",
  "description": "Detailed explanation of what the rule detects and why it matters.",
  "severity": "CRITICAL",
  "type": "VULNERABILITY",
  "tags": ["category", "specific-tag"],
  "status": "READY"
}
```

| Field | Description | Valid Values |
|-------|-------------|--------------|
| `key` | Unique identifier (lowercase, hyphenated) | String |
| `name` | Display name | String |
| `description` | Full explanation of the issue | String |
| `severity` | Issue severity level | `BLOCKER`, `CRITICAL`, `MAJOR`, `MINOR`, `INFO` |
| `type` | Classification of the issue | `VULNERABILITY`, `BUG`, `CODE_SMELL` |
| `tags` | Categorization labels | Array of strings |
| `status` | Rule availability | `READY`, `BETA`, `DEPRECATED` |

### Remediation Section

Provides fix guidance and time estimates:

```json
"remediation": {
  "constantCost": "30min",
  "examples": [
    {
      "before": "// Problematic code example",
      "after": "// Fixed code example"
    }
  ]
}
```

### Impacts Section

Describes effect on software quality:

```json
"impacts": [
  {
    "softwareQuality": "SECURITY",
    "severity": "HIGH"
  }
]
```

Valid `softwareQuality` values: `SECURITY`, `RELIABILITY`, `MAINTAINABILITY`
Valid `severity` values: `HIGH`, `MEDIUM`, `LOW`

### Technical Debt Section

Estimates effort to fix:

```json
"debt": {
  "function": "CONSTANT_ISSUE",
  "offset": "30min"
}
```

Or for linear scaling:

```json
"debt": {
  "function": "LINEAR",
  "coefficient": "10min",
  "offset": "0min"
}
```

### Optional Parameters Section

For configurable rules:

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

Valid `type` values: `INTEGER`, `STRING`, `BOOLEAN`, `FLOAT`

---

## Severity Guidelines

Use these guidelines when setting rule severity:

| Severity | Use When |
|----------|----------|
| `BLOCKER` | Critical security flaw, data loss risk, or application crash |
| `CRITICAL` | Security vulnerability, major bug, or severe performance issue |
| `MAJOR` | Significant code smell or moderate maintainability concern |
| `MINOR` | Minor code quality issue or style violation |
| `INFO` | Informational or best practice suggestion |

---

## Type Guidelines

| Type | Use For |
|------|---------|
| `VULNERABILITY` | Security issues exploitable by attackers |
| `BUG` | Code that is demonstrably wrong or will fail |
| `CODE_SMELL` | Maintainability issues, design problems, technical debt |

---

## Best Practices

### When Creating New Rules

1. **Choose the correct category** - Place security issues in `security/`, design issues in `code-smells/`, etc.

2. **Use descriptive keys** - Keys should be lowercase, hyphenated, and clearly describe the issue (e.g., `sql-injection`, `god-class`)

3. **Write clear descriptions** - Explain what the rule detects, why it's a problem, and the potential impact

4. **Provide remediation examples** - Include before/after code snippets showing how to fix the issue

5. **Set appropriate severity** - Match severity to actual risk; don't over-inflate

6. **Include relevant tags** - Use category tags (`security`, `performance`) plus specific tags (`owasp-top-10`, `database`)

7. **Estimate realistic debt** - Base time estimates on actual fix complexity

### When Modifying Rules

1. **Preserve the key** - Never change a rule's key; it may be referenced elsewhere

2. **Update examples** - Keep code examples current with modern practices

3. **Maintain consistency** - Follow the established JSON structure

### Common Tags by Category

- **Security**: `security`, `owasp-top-10`, `injection`, `authentication`, `encryption`
- **Code Smells**: `code-smell`, `design`, `solid`, `refactoring`, `complexity`
- **Performance**: `performance`, `memory`, `database`, `optimization`, `resource-management`
- **Maintainability**: `maintainability`, `readability`, `documentation`, `naming`

---

## Example Rule Template

Use this template when creating new rules:

```json
{
  "key": "your-rule-key",
  "name": "Your Rule Name",
  "description": "Clear description of what this rule detects and why it matters.",
  "severity": "MAJOR",
  "type": "CODE_SMELL",
  "tags": ["category", "specific-tag"],
  "remediation": {
    "constantCost": "15min",
    "examples": [
      {
        "before": "// Code that triggers this rule",
        "after": "// Corrected code"
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

## How to Help Users

When users ask for help:

1. **Creating a new rule**: Guide them through the template, help choose appropriate severity/type/tags, and suggest placement in the correct category directory

2. **Understanding a rule**: Explain what the rule detects, why it matters, and how to fix violations

3. **Finding rules**: Help locate rules by category, tag, severity, or issue type

4. **Improving rules**: Suggest better descriptions, more relevant tags, or clearer remediation examples

5. **Validating rules**: Check that JSON is well-formed and all required fields are present with valid values
