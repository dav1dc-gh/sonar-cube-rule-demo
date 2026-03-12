# SonarQube Rules Files — AI Assistant Custom Instructions

You are an AI assistant specialized in helping users create, manage, and understand SonarQube rule definition files within this repository. Follow these instructions to provide accurate, consistent, and helpful guidance.

---

## 1. Overview

This repository contains a collection of **SonarQube custom rule definitions** in JSON format. Each file defines a single rule that can be imported into SonarQube custom rule plugins or used as a reference for building custom quality profiles. The rules codify best practices across security, code quality, performance, and maintainability.

---

## 2. Directory Structure

All rule files live under the `rules/` directory, organized into four category subdirectories:

```
rules/
├── security/           # 15 rules — Security vulnerabilities (OWASP, injection, auth, data exposure)
├── code-smells/        # 13 rules — Code quality issues (design problems, duplication, complexity)
├── performance/        # 12 rules — Performance anti-patterns (leaks, N+1, unnecessary allocations)
└── maintainability/    # 12 rules — Maintainability concerns (naming, nesting, documentation, coupling)
```

When creating a new rule, always place it in the most appropriate category directory. If a rule spans categories, choose the category that represents its **primary concern**.

---

## 3. Rule Categories

### 3.1 Security (`rules/security/`) — 15 rules

Rules that detect **security vulnerabilities** as classified by standards like the OWASP Top 10. These rules typically have `"type": "VULNERABILITY"` and severity of CRITICAL or BLOCKER.

| Rule File | What It Detects |
|---|---|
| `command-injection.json` | OS command injection via unsanitized user input passed to system commands |
| `csrf-vulnerability.json` | Missing CSRF protection on state-changing operations |
| `hardcoded-credentials.json` | Hardcoded passwords, API keys, tokens, or secrets in source code |
| `insecure-cookie.json` | Cookies missing Secure, HttpOnly, or SameSite flags |
| `insecure-deserialization.json` | Unsafe deserialization of untrusted data (potential RCE) |
| `insecure-random.json` | Predictable random number generators used in security-sensitive contexts |
| `ldap-injection.json` | User input concatenated directly into LDAP queries |
| `open-redirect.json` | User-controlled input used to construct redirect URLs |
| `path-traversal.json` | File path manipulation allowing access outside intended directories |
| `sensitive-data-exposure.json` | Logging of sensitive information (passwords, PII) |
| `server-side-request-forgery.json` | User-controlled URLs used for server-side HTTP requests (SSRF) |
| `sql-injection.json` | User input concatenated into SQL queries without parameterization |
| `weak-cryptography.json` | Use of weak/deprecated cryptographic algorithms (MD5, SHA1, DES) |
| `xml-external-entity.json` | XML parsers configured to process external entities (XXE) |
| `xss-vulnerability.json` | Cross-Site Scripting risks from unescaped user input in output |

### 3.2 Code Smells (`rules/code-smells/`) — 13 rules

Rules that detect **design and code quality problems** that make code harder to understand, change, or reuse. These rules use `"type": "CODE_SMELL"`.

| Rule File | What It Detects |
|---|---|
| `complex-methods.json` | Methods with high cyclomatic complexity |
| `data-clumps.json` | Groups of variables that frequently appear together across methods/classes |
| `dead-code.json` | Unreachable code, unused variables, methods, or classes |
| `duplicate-code.json` | Code duplication across the codebase |
| `empty-catch-block.json` | Empty catch blocks that silently swallow exceptions |
| `feature-envy.json` | Methods that use more features from other classes than their own |
| `god-class.json` | Classes that are too large and violate the Single Responsibility Principle |
| `long-parameter-list.json` | Methods with too many parameters |
| `magic-numbers.json` | Unnamed numerical constants that reduce readability |
| `message-chains.json` | Long chains of method calls violating the Law of Demeter |
| `primitive-obsession.json` | Overuse of primitive types instead of domain objects |
| `refused-bequest.json` | Subclasses that override inherited methods to do nothing or throw |
| `speculative-generality.json` | Unused abstractions created for hypothetical future requirements |

### 3.3 Performance (`rules/performance/`) — 12 rules

Rules that detect **performance anti-patterns** causing unnecessary resource consumption, latency, or scalability issues. Type is typically `"CODE_SMELL"` or `"BUG"`.

| Rule File | What It Detects |
|---|---|
| `connection-pool-exhaustion.json` | Database/HTTP connections not properly closed or returned to pool |
| `excessive-object-creation.json` | Unnecessary object allocation in hot code paths |
| `inefficient-collection-usage.json` | Improper use of collections, missing initial capacity hints |
| `inefficient-loops.json` | Performance issues within loops |
| `memory-leaks.json` | Unclosed resources, listener accumulation, references preventing GC |
| `missing-lazy-initialization.json` | Expensive resources eagerly initialized but not always used |
| `n-plus-one-query.json` | Database queries executed inside loops (N+1 problem) |
| `string-concatenation-in-loop.json` | String concatenation with `+` inside loops |
| `synchronous-io-in-async.json` | Blocking I/O operations within async methods |
| `unbounded-collection-growth.json` | Collections that grow without bounds or eviction policies |
| `unnecessary-boxing.json` | Unnecessary conversions between primitives and wrapper classes |
| `unoptimized-regex.json` | Regex compiled repeatedly or susceptible to catastrophic backtracking |

### 3.4 Maintainability (`rules/maintainability/`) — 12 rules

Rules that detect patterns making code **harder to read, change, and maintain** over time. Type is typically `"CODE_SMELL"`.

| Rule File | What It Detects |
|---|---|
| `boolean-blindness.json` | Methods with multiple boolean parameters whose meaning is unclear |
| `circular-dependencies.json` | Circular dependencies between packages, modules, or classes |
| `deep-nesting.json` | Excessive nesting levels reducing readability |
| `excessive-comments.json` | Redundant comments that explain *what* instead of *why* |
| `hardcoded-urls.json` | Hardcoded URLs/endpoints that should be externalized to configuration |
| `hidden-dependencies.json` | Dependencies not explicit in method signatures |
| `inconsistent-naming.json` | Variables/methods not following naming conventions |
| `long-methods.json` | Methods exceeding length thresholds |
| `missing-javadoc.json` | Public APIs lacking proper documentation comments |
| `missing-null-check.json` | Potential null pointer dereferences |
| `shotgun-surgery.json` | Changes requiring many small modifications across multiple classes |
| `too-many-parameters.json` | Methods with excessive parameter counts |

---

## 4. Rule File Structure

Every rule file is a single JSON object. Below is the complete schema with all supported fields. Fields marked **(optional)** may be omitted.

```jsonc
{
  // REQUIRED — Unique kebab-case identifier matching the filename (without .json)
  "key": "rule-name",

  // REQUIRED — Human-readable display name
  "name": "Rule Display Name",

  // REQUIRED — Detailed explanation of what the rule detects and why it matters
  "description": "Detects <issue> which causes <problem>.",

  // REQUIRED — Severity level: BLOCKER | CRITICAL | MAJOR | MINOR | INFO
  "severity": "MAJOR",

  // REQUIRED — Rule type: VULNERABILITY | BUG | CODE_SMELL
  "type": "CODE_SMELL",

  // REQUIRED — Array of categorization tags (lowercase, hyphenated)
  "tags": ["category", "subcategory"],

  // REQUIRED — Remediation guidance
  "remediation": {
    "constantCost": "30min",           // Estimated fix time (e.g., "5min", "1h", "4h")
    "examples": [                      // At least one before/after example
      {
        "before": "// Bad code example",
        "after": "// Fixed code example"
      }
    ]
  },

  // REQUIRED — Impact on software quality
  "impacts": [
    {
      "softwareQuality": "SECURITY",   // SECURITY | RELIABILITY | MAINTAINABILITY
      "severity": "HIGH"               // HIGH | MEDIUM | LOW
    }
  ],

  // REQUIRED — Same as severity (confirms the default)
  "defaultSeverity": "MAJOR",

  // REQUIRED — Rule status: READY | BETA | DEPRECATED
  "status": "READY",

  // REQUIRED — Technical debt estimation
  "debt": {
    "function": "CONSTANT_ISSUE",      // CONSTANT_ISSUE | LINEAR
    "offset": "30min",                 // Base time cost
    "coefficient": "10min"             // (optional) Per-occurrence cost (used with LINEAR)
  },

  // OPTIONAL — Configurable thresholds or parameters
  "params": [
    {
      "key": "paramKey",               // camelCase identifier
      "name": "Parameter Display Name",
      "description": "What this parameter controls",
      "defaultValue": "10",            // Default value as a string
      "type": "INTEGER"                // INTEGER | STRING | BOOLEAN
    }
  ]
}
```

### Field Guidelines

- **`key`**: Must be kebab-case and match the filename (e.g., `"sql-injection"` → `sql-injection.json`).
- **`severity`**: Use BLOCKER for issues that must be fixed immediately (e.g., hardcoded credentials), CRITICAL for high-risk issues (e.g., SQL injection), MAJOR for significant quality issues, MINOR for low-impact improvements, INFO for informational findings.
- **`type`**: Use VULNERABILITY for security issues, BUG for reliability defects, CODE_SMELL for design/quality issues.
- **`tags`**: Always include the category tag (e.g., `"security"`, `"performance"`). Add specific tags for discoverability (e.g., `"owasp-top-10"`, `"sql"`, `"solid"`).
- **`remediation.examples`**: Provide realistic, minimal code showing the problem and its fix. Use the primary language the rule targets (typically Java).
- **`debt.function`**: Use `CONSTANT_ISSUE` when every occurrence takes roughly the same time to fix. Use `LINEAR` when fix time scales with the size of the issue (e.g., large classes).
- **`params`**: Only include when the rule has user-configurable thresholds (e.g., max nesting depth, max method length).

---

## 5. Best Practices

### Creating New Rules

1. **Choose the right category.** Place the rule file in the directory matching its primary concern: `security/`, `code-smells/`, `performance/`, or `maintainability/`.
2. **Use kebab-case filenames** matching the `key` field (e.g., `missing-null-check.json`).
3. **Write a clear, actionable description.** Start with "Detects…" and explain both *what* is detected and *why* it's problematic.
4. **Provide realistic before/after examples.** Show the minimal code that triggers the rule and the correct fix.
5. **Set severity appropriately.** Security vulnerabilities are typically CRITICAL or BLOCKER. Code smells are MAJOR or MINOR.
6. **Include relevant tags.** At minimum, include the category tag. Add standard tags like `"owasp-top-10"`, `"solid"`, `"readability"` where applicable.
7. **Estimate remediation time honestly.** Simple renames might be 5 minutes; refactoring a God Class could be 4+ hours.
8. **Add `params` only when needed.** If the rule has a configurable threshold (e.g., max lines, max depth), define it with a sensible default.

### Modifying Existing Rules

- Preserve all required fields when editing.
- Keep the `key` field and filename in sync — if you rename one, rename the other.
- When changing severity, update both `severity` and `defaultSeverity` to match.
- Update the `remediation.examples` if the description changes to keep them consistent.

### General Guidance

- Validate JSON syntax before committing. Every file must be valid JSON.
- Do not add trailing commas — JSON does not allow them.
- Keep descriptions language-agnostic where possible, but use Java for code examples since SonarQube is Java-centric.
- When in doubt about severity or type classification, refer to existing rules in the same category for consistency.
- The `status` field should be `"READY"` for production rules, `"BETA"` for experimental rules, and `"DEPRECATED"` for rules being phased out.

---

## Lessons Learned — AI History

At the end of every response, append a "Lessons Learned" section to `AI-HISTORY.md` in the root of this repository. Each entry should record:

- **What worked** — approaches, tools, or patterns that succeeded.
- **What failed** — mistakes, dead ends, or incorrect assumptions.
- **Why** — the reasoning behind decisions so future tasks can build on past context.

### Format

Each entry in `AI-HISTORY.md` should follow this structure:

```
### <Date> — <Brief task description>
- **What worked:** ...
- **What failed:** ...
- **Key takeaway:** ...
```

### Guidelines

- Keep entries concise, factual, and focused on actionable insights.
- Reflect on performance and identify areas for improvement.
- Read `AI-HISTORY.md` at the start of every new task to avoid repeating mistakes and to build on past successes.
- When `AI-HISTORY.md` exceeds **15,000 tokens**, summarize the key insights from older entries into a "Summary of Past Learnings" section at the top of the file, then remove the older individual entries to keep the file manageable and focused on recent learnings.
