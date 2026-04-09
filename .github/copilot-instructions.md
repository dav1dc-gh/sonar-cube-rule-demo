# Copilot Custom Instructions — SonarQube Rules Files

## Overview

This repository contains a collection of SonarQube rule definitions in JSON format, organized by category. Each rule file encodes a single static analysis rule following SonarQube's rule specification standards. Your role is to help users **create, manage, understand, and extend** these rule files.

---

## Directory Structure & Organization

Rules live under the `rules/` directory, grouped into four categories:

```
rules/
├── security/          # 15 rules — vulnerability detection (injection, XSS, SSRF, etc.)
├── code-smells/       # 13 rules — structural quality issues (god class, dead code, etc.)
├── performance/       # 12 rules — runtime efficiency problems (N+1, memory leaks, etc.)
└── maintainability/   # 12 rules — long-term code health (naming, nesting, javadoc, etc.)
```

**Naming convention**: Files are named with lower-kebab-case matching the rule `key` (e.g., `sql-injection.json` → `"key": "sql-injection"`).

When creating a new rule, place it in the category that best matches its **primary concern**. If a rule spans categories, choose the dominant one and use `tags` to cross-reference.

---

## Rule Categories

### Security (`rules/security/`) — 15 rules
Detects vulnerabilities that could be exploited by attackers. Typical severities: CRITICAL or BLOCKER. Type is always `VULNERABILITY`.

| Rule | Description |
|------|-------------|
| `command-injection` | OS command injection via unsanitized user input |
| `csrf-vulnerability` | Missing CSRF protection on state-changing operations |
| `hardcoded-credentials` | Hardcoded passwords, API keys, or tokens in source |
| `insecure-cookie` | Cookies missing Secure, HttpOnly, or SameSite flags |
| `insecure-deserialization` | Unsafe deserialization of untrusted data |
| `insecure-random` | Predictable RNG used for security-sensitive operations |
| `ldap-injection` | User input concatenated into LDAP queries |
| `open-redirect` | User-controlled redirect URLs without validation |
| `path-traversal` | File access outside intended directories |
| `sensitive-data-exposure` | Logging of passwords, PII, or other secrets |
| `server-side-request-forgery` | User-controlled URLs in server-side HTTP requests |
| `sql-injection` | SQL queries built via string concatenation with user input |
| `weak-cryptography` | Use of deprecated algorithms (MD5, SHA1, DES) |
| `xml-external-entity` | XML parsers configured to process external entities |
| `xss-vulnerability` | Cross-Site Scripting via unescaped user output |

### Code Smells (`rules/code-smells/`) — 13 rules
Structural quality issues that indicate poor design or maintainability debt. Type is `CODE_SMELL`.

| Rule | Description |
|------|-------------|
| `complex-methods` | Methods with high cyclomatic complexity |
| `data-clumps` | Groups of variables that appear together across multiple locations |
| `dead-code` | Unreachable code, unused variables, methods, or classes |
| `duplicate-code` | Repeated code blocks that should be extracted |
| `empty-catch-block` | Catch blocks that silently swallow exceptions |
| `feature-envy` | Methods that use more features from other classes than their own |
| `god-class` | Oversized classes violating Single Responsibility Principle |
| `long-parameter-list` | Methods with too many parameters |
| `magic-numbers` | Unnamed numerical constants in logic |
| `message-chains` | Long method call chains violating Law of Demeter |
| `primitive-obsession` | Overuse of primitives instead of small domain objects |
| `refused-bequest` | Subclasses that ignore inherited behavior |
| `speculative-generality` | Abstractions created for hypothetical future needs |

### Performance (`rules/performance/`) — 12 rules
Runtime efficiency problems that degrade throughput, latency, or resource usage. Type is `CODE_SMELL` or `BUG`.

| Rule | Description |
|------|-------------|
| `connection-pool-exhaustion` | Database connections not returned to the pool |
| `excessive-object-creation` | Unnecessary object allocation in hot paths |
| `inefficient-collection-usage` | Wrong collection type for the access pattern |
| `inefficient-loops` | Loops with avoidable overhead |
| `memory-leaks` | Unclosed resources or references preventing GC |
| `missing-lazy-initialization` | Eager initialization of rarely used heavy objects |
| `n-plus-one-query` | Database queries inside loops |
| `string-concatenation-in-loop` | String `+` instead of StringBuilder in loops |
| `synchronous-io-in-async` | Blocking I/O inside async contexts |
| `unbounded-collection-growth` | Collections that grow without eviction or limits |
| `unnecessary-boxing` | Redundant boxing/unboxing of primitives |
| `unoptimized-regex` | Regex patterns with catastrophic backtracking risk |

### Maintainability (`rules/maintainability/`) — 12 rules
Long-term code health and readability concerns. Type is `CODE_SMELL`.

| Rule | Description |
|------|-------------|
| `boolean-blindness` | Boolean parameters that obscure meaning at call sites |
| `circular-dependencies` | Mutual dependencies between classes or packages |
| `deep-nesting` | Excessive nesting of control structures |
| `excessive-comments` | Comments that restate obvious code instead of explaining why |
| `hardcoded-urls` | URLs and endpoints embedded in source code |
| `hidden-dependencies` | Dependencies acquired internally instead of injected |
| `inconsistent-naming` | Variables/methods not following naming conventions |
| `long-methods` | Methods that exceed a reasonable line count |
| `missing-javadoc` | Public API elements without documentation |
| `missing-null-check` | Potential null dereferences on unchecked values |
| `shotgun-surgery` | Changes that require modifications across many classes |
| `too-many-parameters` | Methods/constructors with excessive parameter counts |

---

## Rule File Structure

Every rule file is a JSON object with the following fields:

### Required Fields

| Field | Type | Description |
|-------|------|-------------|
| `key` | `string` | Unique identifier, lower-kebab-case. Must match the filename (without `.json`). |
| `name` | `string` | Human-readable rule name. |
| `description` | `string` | Detailed explanation of what the rule detects and why it matters. |
| `severity` | `string` | One of: `BLOCKER`, `CRITICAL`, `MAJOR`, `MINOR`, `INFO`. |
| `type` | `string` | One of: `BUG`, `VULNERABILITY`, `CODE_SMELL`. |
| `tags` | `string[]` | Classification tags (e.g., `["security", "owasp-top-10"]`). Always include the category name as a tag. |
| `remediation` | `object` | Fix guidance — see below. |
| `impacts` | `object[]` | Software quality impacts — see below. |
| `defaultSeverity` | `string` | Same as `severity` (the out-of-box default). |
| `status` | `string` | Rule lifecycle status. Use `"READY"` for active rules. |
| `debt` | `object` | Technical debt estimation — see below. |

### Optional Fields

| Field | Type | Description |
|-------|------|-------------|
| `params` | `object[]` | Configurable thresholds (e.g., max nesting depth, max line count). |

### Nested Object Schemas

**`remediation`**
```json
{
  "constantCost": "30min",          // Estimated fix time
  "examples": [
    {
      "before": "// Bad code example",
      "after": "// Fixed code example"
    }
  ]
}
```

**`impacts`** (array of one or more)
```json
{
  "softwareQuality": "SECURITY",    // SECURITY | RELIABILITY | MAINTAINABILITY
  "severity": "HIGH"                // HIGH | MEDIUM | LOW
}
```

**`debt`**
```json
{
  "function": "CONSTANT_ISSUE",     // CONSTANT_ISSUE or LINEAR
  "offset": "30min"                 // For CONSTANT_ISSUE
}
// — or for LINEAR —
{
  "function": "LINEAR",
  "coefficient": "10min",           // Per unit of measure
  "offset": "0min"
}
```

**`params`** (optional, array)
```json
{
  "key": "maxLines",
  "name": "Maximum Lines",
  "description": "Maximum number of lines allowed in a class",
  "defaultValue": "500",
  "type": "INTEGER"                 // INTEGER | STRING | BOOLEAN
}
```

---

## Severity Guidelines

Choose severity based on real-world impact:

| Severity | When to Use | Examples |
|----------|-------------|---------|
| **BLOCKER** | Exploitable vulnerability with direct data loss or compromise risk | Hardcoded credentials, unpatched RCE vectors |
| **CRITICAL** | High-impact bugs or vulnerabilities that need immediate attention | SQL injection, memory leaks, N+1 queries |
| **MAJOR** | Significant quality issues that accumulate technical debt | God classes, deep nesting, empty catch blocks |
| **MINOR** | Low-impact style or convention violations | Naming inconsistencies, excessive comments |
| **INFO** | Informational findings, suggestions | Minor style preferences |

---

## Best Practices

### Creating New Rules
1. **Pick the right category** — security vulnerabilities go in `security/`, design issues in `code-smells/`, runtime problems in `performance/`, readability/health in `maintainability/`.
2. **Use a descriptive `key`** — lower-kebab-case, matching the filename. The key should clearly convey what the rule detects.
3. **Write a thorough `description`** — explain *what* the rule detects, *why* it's a problem, and the potential consequences.
4. **Provide before/after examples** — the `remediation.examples` array should contain realistic, compilable code snippets showing the problem and its fix.
5. **Set accurate remediation cost** — estimate how long a typical fix takes. Simple renames: `5min`. Architecture changes: `4h`.
6. **Tag comprehensively** — always include the category name as a tag, plus relevant cross-cutting concerns (`owasp-top-10`, `solid`, `orm`).
7. **Add `params` when thresholds are configurable** — if the rule's sensitivity depends on a number (max lines, max depth), expose it as a parameter with a sensible default.

### Managing Existing Rules
- Keep `status` as `"READY"` for all active rules. Use `"DEPRECATED"` only when a rule is superseded.
- When updating a rule, preserve the `key` to avoid breaking existing quality profiles.
- Ensure `severity` and `defaultSeverity` stay in sync.

### Contributing
- Validate JSON before committing — every file must be well-formed JSON.
- One rule per file; filename must match the `key` field.
- Maintain alphabetical order within each category directory for easy scanning.
- Update `README.md` when adding or removing rules.

---

## Lessons Learned Tracking

At the end of every response that involves making changes, researching the codebase, or completing a task, append a concise "Lessons Learned" entry to `AI-HISTORY.md` in the root of this repository.

Each entry should include:
- **Date**: The current date
- **Task**: A brief description of what was done
- **What Worked**: Key approaches or decisions that succeeded
- **What Failed**: Any missteps, dead ends, or errors encountered
- **Why**: Reasoning behind decisions made
- **Actionable Insights**: Concrete takeaways for future tasks

At the start of every new task, read `AI-HISTORY.md` to avoid repeating past mistakes and to build on previous successes.

When `AI-HISTORY.md` exceeds 15,000 tokens (~60KB), summarize the key insights into a "Summary of Key Insights" section at the top, remove older individual entries, and keep the file focused on recent and high-value learnings.
