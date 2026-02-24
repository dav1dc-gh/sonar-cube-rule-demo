# Custom Instructions

## Overview

This repository contains a curated collection of **SonarQube rule definitions** in JSON format. The rules serve as reference material and can be imported into SonarQube custom rule plugins or used to build custom quality profiles. Each rule file captures a single static-analysis rule—its identifier, severity, detection description, remediation guidance, and configurable parameters.

The assistant's job is to help users **create, manage, understand, and improve** these rule files.

---

## Repository Structure

All rule definitions live under the `rules/` directory, organized into four category subdirectories:

```
rules/
├── security/           # 15 rules — vulnerabilities (injection, XSS, CSRF, SSRF, etc.)
├── code-smells/        # 13 rules — design & quality issues (god class, dead code, duplication, etc.)
├── performance/        # 12 rules — runtime efficiency (N+1, memory leaks, boxing, regex, etc.)
└── maintainability/    # 12 rules — long-term code health (naming, nesting, null checks, docs, etc.)
```

When creating a new rule, always place it in the most appropriate category directory. If a rule spans multiple concerns, choose the **primary** concern.

---

## Rule Categories

### Security (`rules/security/`)
Rules that detect **vulnerabilities** exploitable by attackers. Typical SonarQube type: `VULNERABILITY`. Common severities: `CRITICAL` or `BLOCKER`.

Covers: SQL injection, command injection, XSS, CSRF, SSRF, path traversal, open redirect, XXE, LDAP injection, insecure deserialization, insecure random, weak cryptography, hardcoded credentials, insecure cookies, and sensitive data exposure.

### Code Smells (`rules/code-smells/`)
Rules that detect **design and quality problems** that make code harder to understand or change. SonarQube type: `CODE_SMELL`.

Covers: god class, complex methods, dead code, duplicate code, data clumps, empty catch blocks, feature envy, long parameter lists, magic numbers, message chains, primitive obsession, refused bequest, and speculative generality.

### Performance (`rules/performance/`)
Rules that detect **runtime inefficiencies**. SonarQube type is typically `CODE_SMELL` (performance sub-category) or `BUG`.

Covers: N+1 queries, connection pool exhaustion, excessive object creation, inefficient collections, inefficient loops, memory leaks, missing lazy initialization, string concatenation in loops, synchronous I/O in async contexts, unbounded collection growth, unnecessary boxing, and unoptimized regex.

### Maintainability (`rules/maintainability/`)
Rules that detect issues affecting **long-term code health and readability**. SonarQube type: `CODE_SMELL`.

Covers: boolean blindness, circular dependencies, deep nesting, excessive comments, hardcoded URLs, hidden dependencies, inconsistent naming, long methods, missing Javadoc, missing null checks, shotgun surgery, and too many parameters.

---

## Rule File Structure

Every rule JSON file **must** include the following top-level fields:

| Field | Type | Description |
|---|---|---|
| `key` | `string` | Unique kebab-case identifier (must match the filename without `.json`). |
| `name` | `string` | Human-readable rule name. |
| `description` | `string` | Detailed explanation of what the rule detects and why it matters. |
| `severity` | `string` | One of: `BLOCKER`, `CRITICAL`, `MAJOR`, `MINOR`, `INFO`. |
| `type` | `string` | One of: `VULNERABILITY`, `BUG`, `CODE_SMELL`. |
| `tags` | `string[]` | Categorization tags (e.g., `["security", "sql", "injection", "owasp-top-10"]`). |
| `remediation` | `object` | Contains `constantCost` (e.g., `"30min"`) and `examples` array. |
| `remediation.examples[]` | `object` | Each with `before` (bad code) and `after` (fixed code) strings. |
| `impacts` | `object[]` | Each with `softwareQuality` (`SECURITY`, `MAINTAINABILITY`, `RELIABILITY`) and `severity` (`HIGH`, `MEDIUM`, `LOW`). |
| `defaultSeverity` | `string` | Same value as `severity` — acts as the default when imported. |
| `status` | `string` | Typically `"READY"`. Other values: `"BETA"`, `"DEPRECATED"`. |
| `debt` | `object` | Technical debt estimate with `function` (`CONSTANT_ISSUE` or `LINEAR`), and `offset` / `coefficient`. |

**Optional fields:**

| Field | Type | Description |
|---|---|---|
| `params` | `object[]` | Configurable thresholds. Each entry has `key`, `name`, `description`, `defaultValue`, and `type` (`INTEGER`, `STRING`, `BOOLEAN`, etc.). |

### Example: Minimal Rule

```json
{
  "key": "sql-injection",
  "name": "SQL Injection Prevention",
  "description": "Detects potential SQL injection vulnerabilities where user input is directly concatenated into SQL queries.",
  "severity": "CRITICAL",
  "type": "VULNERABILITY",
  "tags": ["security", "sql", "injection", "owasp-top-10"],
  "remediation": {
    "constantCost": "30min",
    "examples": [
      {
        "before": "String query = \"SELECT * FROM users WHERE id = \" + userId;",
        "after": "PreparedStatement stmt = conn.prepareStatement(\"SELECT * FROM users WHERE id = ?\");\nstmt.setString(1, userId);"
      }
    ]
  },
  "impacts": [{ "softwareQuality": "SECURITY", "severity": "HIGH" }],
  "defaultSeverity": "CRITICAL",
  "status": "READY",
  "debt": { "function": "CONSTANT_ISSUE", "offset": "30min" }
}
```

### Example: Rule with Parameters

```json
{
  "key": "deep-nesting",
  "name": "Deeply Nested Code",
  "description": "Detects code with excessive nesting levels, which reduces readability and increases cognitive complexity.",
  "severity": "MAJOR",
  "type": "CODE_SMELL",
  "tags": ["maintainability", "complexity", "readability", "refactoring"],
  "remediation": {
    "constantCost": "20min",
    "examples": [
      {
        "before": "if (a) {\n  if (b) {\n    if (c) {\n      if (d) { doSomething(); }\n    }\n  }\n}",
        "after": "if (!a || !b || !c || !d) { return; }\ndoSomething();"
      }
    ]
  },
  "impacts": [{ "softwareQuality": "MAINTAINABILITY", "severity": "MEDIUM" }],
  "defaultSeverity": "MAJOR",
  "status": "READY",
  "debt": { "function": "CONSTANT_ISSUE", "offset": "20min" },
  "params": [
    {
      "key": "maxDepth",
      "name": "Maximum Nesting Depth",
      "description": "Maximum allowed nesting depth",
      "defaultValue": "4",
      "type": "INTEGER"
    }
  ]
}
```

---

## Best Practices

### Creating New Rules
1. **Choose the right category.** Place the file in the directory that matches the rule's primary concern.
2. **Use kebab-case for filenames and keys.** The `key` field must match the filename (e.g., `my-new-rule.json` → `"key": "my-new-rule"`).
3. **Write clear descriptions.** Explain *what* the rule detects, *why* it matters, and *when* it applies.
4. **Provide before/after examples.** Remediation examples should be realistic and copy-pasteable.
5. **Set severity appropriately:**
   - `BLOCKER` / `CRITICAL` — security vulnerabilities, data-loss bugs.
   - `MAJOR` — significant code smells impacting maintainability or performance.
   - `MINOR` — style or convention issues.
   - `INFO` — informational, non-actionable.
6. **Add params when thresholds are configurable.** E.g., max line count, max nesting depth.
7. **Tag generously.** Include the category name, sub-domain, and relevant standards (e.g., `owasp-top-10`, `solid`).
8. **Keep JSON valid.** No trailing commas, no comments. Run `jq . file.json` to validate.

### Modifying Existing Rules
- Preserve the `key` — it may be referenced by existing SonarQube profiles.
- When changing severity or type, update both `severity` and `defaultSeverity`.
- Keep the `status` as `READY` unless explicitly deprecating (`DEPRECATED`).

### General Guidelines
- Treat this repo as a **living reference library**. Rules should evolve with standards and best practices.
- When in doubt about a rule's category, check how SonarQube itself categorizes similar rules.
- Ensure consistency across rules in the same category (tag conventions, severity calibration, remediation cost estimates).

---

## Lessons Learned Protocol

At the end of every response, the assistant **must** append a "Lessons Learned" entry to `HISTORY.md` in the root of this repository. Each entry should:

1. Be dated with the current date.
2. Summarize **what was done** (the task/change).
3. Note **what worked** and **what failed** (if anything).
4. Explain **why** decisions were made a certain way.
5. Be concise, factual, and focused on actionable insights for future tasks.

At the **start** of every new task, the assistant should read `HISTORY.md` to avoid repeating past mistakes and to build on prior successes.
