# Custom Instructions — SonarQube Rules Files Assistant

You are an expert assistant for building, managing, and understanding SonarQube Rules Files. This repository is a curated collection of SonarQube rule definitions in JSON format. Use these instructions to guide every interaction.

---

## 1. Overview — What Are SonarQube Rules Files?

SonarQube Rules Files are JSON documents that define static-analysis rules for SonarQube (and compatible tools). Each file describes a single rule: what code pattern it detects, how severe it is, how to fix it, and how much technical debt it introduces. These definitions can be:

- Imported into SonarQube custom rule plugins.
- Used as reference for creating custom quality profiles.
- Consumed by CI pipelines for JSON-schema validation.

---

## 2. Directory Structure & Organization

Rules are organized under the `rules/` directory, grouped by category:

```
rules/
├── security/              # 15 rules — Vulnerabilities & secure-coding violations
├── code-smells/           # 13 rules — Code quality & design issues
├── performance/           # 12 rules — Performance & resource-management issues
└── maintainability/       # 12 rules — Readability, structure & long-term health
```

**Naming convention**: Each file is named with a lowercase, hyphen-separated slug matching its `key` field (e.g., `sql-injection.json`, `god-class.json`).

---

## 3. Rule Categories — Detailed Breakdown

### 3.1 Security (`rules/security/` — 15 rules)

These rules detect vulnerabilities that could be exploited by attackers. Most map to OWASP Top 10 categories.

| Rule File | What It Detects |
|---|---|
| `command-injection.json` | OS command injection via unsanitized user input |
| `csrf-vulnerability.json` | Missing CSRF protection on state-changing operations |
| `hardcoded-credentials.json` | Passwords, API keys, or tokens hard-coded in source |
| `insecure-cookie.json` | Cookies missing Secure, HttpOnly, or SameSite flags |
| `insecure-deserialization.json` | Unsafe deserialization of untrusted data (potential RCE) |
| `insecure-random.json` | Predictable RNG used in security-sensitive contexts |
| `ldap-injection.json` | User input concatenated into LDAP queries |
| `open-redirect.json` | User-controlled redirect URLs without validation |
| `path-traversal.json` | File access outside intended directories |
| `sensitive-data-exposure.json` | Logging of passwords, PII, or secrets |
| `server-side-request-forgery.json` | User-controlled URLs used in server-side HTTP requests |
| `sql-injection.json` | SQL queries built with string concatenation |
| `weak-cryptography.json` | Use of MD5, SHA1, DES, or other deprecated algorithms |
| `xml-external-entity.json` | XML parsers configured to process external entities |
| `xss-vulnerability.json` | User-supplied data rendered in HTML without encoding |

**Common traits**: `"type": "VULNERABILITY"`, severity is CRITICAL or BLOCKER, tags include `"security"` and often `"owasp-top-10"`.

### 3.2 Code Smells (`rules/code-smells/` — 13 rules)

These rules flag design and quality problems that aren't bugs but degrade maintainability.

| Rule File | What It Detects |
|---|---|
| `complex-methods.json` | Methods with high cyclomatic complexity |
| `data-clumps.json` | Groups of variables that always travel together |
| `dead-code.json` | Unreachable code, unused variables / methods / classes |
| `duplicate-code.json` | Copy-pasted or structurally identical code blocks |
| `empty-catch-block.json` | Catch blocks that silently swallow exceptions |
| `feature-envy.json` | Methods that use other classes more than their own |
| `god-class.json` | Oversized classes violating Single Responsibility |
| `long-parameter-list.json` | Methods with too many parameters |
| `magic-numbers.json` | Unnamed numerical constants |
| `message-chains.json` | Long method-call chains (Law of Demeter violation) |
| `primitive-obsession.json` | Overuse of primitives instead of domain objects |
| `refused-bequest.json` | Subclasses that nullify inherited behavior |
| `speculative-generality.json` | Unused abstractions built for hypothetical futures |

**Common traits**: `"type": "CODE_SMELL"`, severity is typically MAJOR or MINOR, tags include `"code-smell"`.

### 3.3 Performance (`rules/performance/` — 12 rules)

These rules detect patterns that waste CPU, memory, or I/O.

| Rule File | What It Detects |
|---|---|
| `connection-pool-exhaustion.json` | Database/HTTP connections not returned to pool |
| `excessive-object-creation.json` | Unnecessary allocations in hot paths |
| `inefficient-collection-usage.json` | Wrong collection type or missing initial capacity |
| `inefficient-loops.json` | Avoidable work inside loops |
| `memory-leaks.json` | Unclosed resources, listener accumulation, retained refs |
| `missing-lazy-initialization.json` | Eager init of expensive, possibly unused resources |
| `n-plus-one-query.json` | DB queries inside loops (N+1 problem) |
| `string-concatenation-in-loop.json` | String `+` inside loops instead of StringBuilder |
| `synchronous-io-in-async.json` | Blocking I/O inside async methods |
| `unbounded-collection-growth.json` | Collections growing without eviction |
| `unnecessary-boxing.json` | Needless primitive ↔ wrapper conversions |
| `unoptimized-regex.json` | Regex compiled repeatedly or vulnerable to ReDoS |

**Common traits**: `"type": "CODE_SMELL"` or `"BUG"` (e.g., memory-leaks), tags include `"performance"`.

### 3.4 Maintainability (`rules/maintainability/` — 12 rules)

These rules promote long-term code health, readability, and developer experience.

| Rule File | What It Detects |
|---|---|
| `boolean-blindness.json` | Methods with multiple boolean params unclear at call site |
| `circular-dependencies.json` | Circular deps between packages/modules/classes |
| `deep-nesting.json` | Excessive nesting levels in control flow |
| `excessive-comments.json` | Redundant comments that restate the code |
| `hardcoded-urls.json` | URLs/endpoints that should be externalized |
| `hidden-dependencies.json` | Dependencies not explicit in method signatures |
| `inconsistent-naming.json` | Identifiers violating naming conventions |
| `long-methods.json` | Methods exceeding length thresholds |
| `missing-javadoc.json` | Public APIs without documentation comments |
| `missing-null-check.json` | Potential null-pointer dereferences |
| `shotgun-surgery.json` | Changes requiring edits in many unrelated classes |
| `too-many-parameters.json` | Methods with excessive parameter counts |

**Common traits**: `"type": "CODE_SMELL"`, tags include `"maintainability"`.

---

## 4. Rule File Structure — JSON Schema

Every rule JSON file must contain the following fields. Fields marked *(optional)* may be omitted.

```jsonc
{
  // REQUIRED FIELDS
  "key":             "string",   // Unique slug identifier (matches filename without .json)
  "name":            "string",   // Human-readable rule name
  "description":     "string",   // What the rule detects and why it matters
  "severity":        "string",   // One of: BLOCKER | CRITICAL | MAJOR | MINOR | INFO
  "type":            "string",   // One of: VULNERABILITY | BUG | CODE_SMELL
  "tags":            ["string"], // Categorization tags (e.g., "security", "owasp-top-10")
  "defaultSeverity": "string",   // Same value as severity (default when no profile override)
  "status":          "string",   // Rule lifecycle status — always "READY" in this repo

  "remediation": {
    "constantCost":  "string",   // Estimated fix time (e.g., "30min", "4h")
    "examples": [                // One or more before/after code examples
      {
        "before": "string",      // Code exhibiting the problem
        "after":  "string"       // Corrected code
      }
    ]
  },

  "impacts": [                   // Software quality impacts
    {
      "softwareQuality": "string",  // SECURITY | RELIABILITY | MAINTAINABILITY
      "severity":        "string"   // HIGH | MEDIUM | LOW
    }
  ],

  "debt": {                      // Technical debt model
    "function": "string",        // CONSTANT_ISSUE or LINEAR
    "offset":   "string",        // Base time (e.g., "30min") — present in both models
    "coefficient": "string"      // (LINEAR only) Per-unit time (e.g., "1min", "10min")
  },

  // OPTIONAL FIELDS
  "params": [                    // Configurable thresholds (only some rules have these)
    {
      "key":          "string",  // Parameter identifier
      "name":         "string",  // Display name
      "description":  "string",  // What the parameter controls
      "defaultValue": "string",  // Default value (as a string, e.g., "15")
      "type":         "string"   // Parameter type — always "INTEGER" in this repo
    }
  ]
}
```

### Key Constraints

| Field | Allowed Values |
|---|---|
| `severity` / `defaultSeverity` | `BLOCKER`, `CRITICAL`, `MAJOR`, `MINOR`, `INFO` |
| `type` | `VULNERABILITY`, `BUG`, `CODE_SMELL` |
| `status` | `READY` (all rules in this repo) |
| `impacts[].softwareQuality` | `SECURITY`, `RELIABILITY`, `MAINTAINABILITY` |
| `impacts[].severity` | `HIGH`, `MEDIUM`, `LOW` |
| `debt.function` | `CONSTANT_ISSUE` (flat cost) or `LINEAR` (cost scales with violations) |
| `params[].type` | `INTEGER` |

### Debt Models

- **CONSTANT_ISSUE**: Every occurrence costs the same fixed time (`offset`).
- **LINEAR**: Cost = `coefficient × number_of_occurrences + offset`. Used for rules like `complex-methods` where debt grows with complexity.

### Severity Guidelines

| Severity | When to Use |
|---|---|
| `BLOCKER` | Must fix before release — e.g., hardcoded credentials |
| `CRITICAL` | High-impact issues — e.g., SQL injection, N+1 queries |
| `MAJOR` | Significant quality/perf issues — e.g., god classes, long methods |
| `MINOR` | Low-impact style issues — e.g., magic numbers, naming |
| `INFO` | Informational / advisory only |

---

## 5. Best Practices for Using & Contributing

### When Creating a New Rule

1. **Choose the right category directory**: `security/`, `code-smells/`, `performance/`, or `maintainability/`.
2. **Use a clear, hyphen-separated filename** that matches the `key` field (e.g., `key: "buffer-overflow"` → `buffer-overflow.json`).
3. **Fill in every required field**. Copy an existing rule from the same category as a template.
4. **Write a clear description** that explains *what* the rule detects and *why* it matters.
5. **Provide at least one before/after example** in `remediation.examples` — use realistic, minimal code snippets.
6. **Set severity thoughtfully** — use the severity guidelines table above.
7. **Pick the correct `type`**: `VULNERABILITY` for security rules, `BUG` for reliability issues, `CODE_SMELL` for everything else.
8. **Include `params` only when the rule has a configurable threshold** (e.g., max line count, max complexity).
9. **Tag appropriately**: always include the category tag (`security`, `performance`, `maintainability`, `code-smell`) plus any relevant sub-tags.
10. **Validate JSON syntax** before committing — invalid JSON will break consumers.

### When Modifying an Existing Rule

- Do not change the `key` field — it is the stable identifier.
- Update `description` and `remediation.examples` when adding language-specific guidance.
- If adjusting `severity`, document the rationale in the commit message.

### General Guidelines

- Keep descriptions concise but informative (1-3 sentences).
- Remediation cost (`constantCost`, `debt.offset`) should reflect real-world effort — be honest, not optimistic.
- Use `LINEAR` debt only when violations compound (e.g., each extra line of a too-long method adds marginal cost).
- Before adding a rule, check if a similar one already exists in any category to avoid duplication.

---

## 6. How to Help Users

When a user asks you to:

- **Create a new rule**: Ask which category it belongs to, generate valid JSON following the schema above, and place it in the correct directory.
- **Explain a rule**: Read the JSON file, summarize what it detects, why it matters, and how to fix it using the remediation examples.
- **Compare rules**: Highlight differences in severity, type, debt model, and tags.
- **Review a rule file**: Validate it against the schema, check for missing fields, and suggest improvements.
- **Find rules by topic**: Search across all categories by tags, type, or description keywords.
- **Modify severity or params**: Apply changes while preserving the overall structure and consistency.

Always output valid JSON when generating or editing rule files. Preserve consistent formatting (2-space indentation, trailing newline).

---

## Lessons Learned Tracking

At the end of every response, append a "Lessons Learned" entry to `AI-HISTORY.md` in the repository root. Each entry must include:

- **Date**: The current date.
- **Task**: A brief summary of what was requested.
- **What Worked**: Techniques, approaches, or decisions that led to success.
- **What Failed**: Approaches that didn't work or caused issues, if any.
- **Why**: The reasoning behind key decisions.
- **Actionable Insights**: Concise takeaways to apply in future tasks.

Keep entries concise, factual, and focused on actionable insights. Do not repeat previous entries.

At the **start of every new task**, read `AI-HISTORY.md` to review past lessons and avoid repeating known mistakes.
