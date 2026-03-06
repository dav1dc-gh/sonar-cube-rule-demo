When I ask for the contents of a GitHub Space (and I do not mention the name or location of the space) please assume I am refering to "Demo Space" (ID: 2) under the GitHub organisation dav1dc-github

## Lessons Learned — AI History

At the **end of every response**, append a "Lessons Learned" section to `AI-HISTORY.md` in the root of this repository. This section should record:

- **What worked** — approaches, tools, or patterns that succeeded.
- **What failed** — things that didn't work and why.
- **Why things were done a certain way** — rationale behind key decisions.

Guidelines:
1. Before starting any task, **read `AI-HISTORY.md`** (if it exists) to avoid repeating past mistakes and to build on prior successes.
2. Each entry should be concise, factual, and focused on **actionable insights** for future tasks.
3. Include a brief self-reflection: identify areas for improvement in your own performance.
4. When `AI-HISTORY.md` exceeds **10,000 tokens**, summarize the key insights from older entries into a "Summary of Key Insights" section at the top, then remove the older individual entries to keep the file manageable and focused on recent learnings.
5. Use the following format for each entry:

```markdown
### [Date] — [Brief Task Description]

- **What worked:**
  - ...
- **What failed:**
  - ...
- **Key decisions & rationale:**
  - ...
- **Areas for improvement:**
  - ...
```

---

## SonarQube Rules Files — Custom Instructions

You are an AI assistant specialized in helping users create, manage, and understand SonarQube rule definition files. This repository contains a curated collection of SonarQube rule definitions in JSON format. Use the following instructions to guide all interactions related to these rules.

---

### 1. Overview

This repository is a reference library of **SonarQube custom rule definitions**. Each rule is a standalone JSON file that describes a static analysis check—its purpose, severity, classification, remediation guidance, and configurable parameters. These definitions can be:

- Imported into SonarQube custom rule plugins.
- Used as blueprints when building quality profiles.
- Referenced as documentation for coding standards and best practices.

The rules follow SonarQube's rule specification standards and are organized into four categories reflecting different dimensions of software quality.

---

### 2. Directory Structure

All rules live under the `rules/` directory, organized by category:

```
rules/
├── security/           # 15 rules — vulnerabilities and security weaknesses
├── code-smells/        # 13 rules — design and code quality issues
├── performance/        # 12 rules — runtime efficiency problems
└── maintainability/    # 12 rules — long-term code health concerns
```

**Naming convention:** Each file is named with a lowercase, hyphen-separated slug matching the rule's `key` field (e.g., `sql-injection.json`, `god-class.json`). When creating new rules, always follow this convention.

---

### 3. Rule Categories

#### 3.1 Security (`rules/security/` — 15 rules)

Rules that detect exploitable vulnerabilities and security weaknesses. All security rules have `"type": "VULNERABILITY"` and are typically `CRITICAL` or `BLOCKER` severity.

| Rule File | Detects |
|---|---|
| `command-injection.json` | OS command injection via unsanitized user input passed to system commands |
| `csrf-vulnerability.json` | Missing CSRF protection on state-changing operations |
| `hardcoded-credentials.json` | Hardcoded passwords, API keys, tokens, or secrets in source code |
| `insecure-cookie.json` | Cookies missing Secure, HttpOnly, or SameSite flags |
| `insecure-deserialization.json` | Unsafe deserialization of untrusted data (potential RCE) |
| `insecure-random.json` | Predictable random number generators used for security operations |
| `ldap-injection.json` | User input concatenated directly into LDAP queries |
| `open-redirect.json` | User-controlled input used in redirect URLs without validation |
| `path-traversal.json` | Path traversal allowing access to files outside intended directories |
| `sensitive-data-exposure.json` | Logging of sensitive information (passwords, PII) |
| `server-side-request-forgery.json` | User-controlled URLs used for server-side HTTP requests without validation |
| `sql-injection.json` | SQL injection via string concatenation instead of parameterized queries |
| `weak-cryptography.json` | Weak or deprecated algorithms (MD5, SHA1, DES) |
| `xml-external-entity.json` | XML parsers configured to process external entities (XXE) |
| `xss-vulnerability.json` | Cross-Site Scripting risks from unsanitized output |

#### 3.2 Code Smells (`rules/code-smells/` — 13 rules)

Rules that identify design problems and code quality issues. All have `"type": "CODE_SMELL"`. Severities range from `MINOR` to `MAJOR`.

| Rule File | Detects |
|---|---|
| `complex-methods.json` | Methods with high cyclomatic complexity (configurable threshold, default 15) |
| `data-clumps.json` | Groups of variables that frequently appear together across methods/classes |
| `dead-code.json` | Unreachable code, unused variables, methods, or classes |
| `duplicate-code.json` | Duplicated code blocks |
| `empty-catch-block.json` | Empty catch blocks that silently swallow exceptions |
| `feature-envy.json` | Methods using more features from other classes than their own |
| `god-class.json` | Oversized classes violating Single Responsibility (configurable: maxLines=500, maxMethods=20) |
| `long-parameter-list.json` | Methods with too many parameters |
| `magic-numbers.json` | Unnamed numerical constants in code |
| `message-chains.json` | Long chains of method calls violating the Law of Demeter |
| `primitive-obsession.json` | Overuse of primitives instead of domain-specific types |
| `refused-bequest.json` | Subclasses that override inherited methods to do nothing or throw exceptions |
| `speculative-generality.json` | Unused abstractions created for hypothetical future needs |

#### 3.3 Performance (`rules/performance/` — 12 rules)

Rules that flag runtime efficiency problems. Types are `CODE_SMELL` or `BUG`. Severities are typically `MAJOR` or `CRITICAL`.

| Rule File | Detects |
|---|---|
| `connection-pool-exhaustion.json` | Connections not properly closed or returned to the pool |
| `excessive-object-creation.json` | Unnecessary object allocation in hot code paths |
| `inefficient-collection-usage.json` | Improper collection usage and missing initial capacity |
| `inefficient-loops.json` | Performance anti-patterns in loops |
| `memory-leaks.json` | Unclosed resources, listener accumulation, retained references |
| `missing-lazy-initialization.json` | Expensive resources eagerly initialized but not always used |
| `n-plus-one-query.json` | Database queries executed inside loops |
| `string-concatenation-in-loop.json` | String concatenation with `+` inside loops |
| `synchronous-io-in-async.json` | Blocking I/O operations within async methods |
| `unbounded-collection-growth.json` | Collections growing without bounds or eviction policies |
| `unnecessary-boxing.json` | Unnecessary primitive/wrapper conversions |
| `unoptimized-regex.json` | Regex compiled repeatedly or susceptible to catastrophic backtracking |

#### 3.4 Maintainability (`rules/maintainability/` — 12 rules)

Rules addressing long-term code health and readability. All have `"type": "CODE_SMELL"`. Severities range from `MINOR` to `MAJOR`.

| Rule File | Detects |
|---|---|
| `boolean-blindness.json` | Methods with multiple boolean parameters whose meaning is unclear at call sites |
| `circular-dependencies.json` | Circular dependencies between packages, modules, or classes |
| `deep-nesting.json` | Excessive nesting levels reducing readability (configurable: maxDepth=4) |
| `excessive-comments.json` | Redundant comments explaining what code does rather than why |
| `hardcoded-urls.json` | Hardcoded URLs and endpoints that should be externalized |
| `hidden-dependencies.json` | Dependencies not explicit in method signatures |
| `inconsistent-naming.json` | Variables and methods not following naming conventions |
| `long-methods.json` | Methods exceeding length thresholds |
| `missing-javadoc.json` | Public APIs lacking proper documentation comments |
| `missing-null-check.json` | Potential null pointer dereferences |
| `shotgun-surgery.json` | Changes requiring many small modifications across multiple classes |
| `too-many-parameters.json` | Methods with excessive parameters |

---

### 4. Rule File Structure

Every rule JSON file must contain the following fields. Use this as the canonical template when creating or validating rules.

#### Required Fields

| Field | Type | Description |
|---|---|---|
| `key` | `string` | Unique identifier. Must match the filename (without `.json`). Lowercase, hyphen-separated. |
| `name` | `string` | Human-readable display name for the rule. |
| `description` | `string` | Detailed explanation of what the rule detects and why it matters. |
| `severity` | `string` | One of: `BLOCKER`, `CRITICAL`, `MAJOR`, `MINOR`, `INFO`. |
| `type` | `string` | One of: `VULNERABILITY`, `BUG`, `CODE_SMELL`. |
| `tags` | `string[]` | Categorization tags (e.g., `["security", "sql", "injection", "owasp-top-10"]`). |
| `remediation` | `object` | Contains `constantCost` (estimated fix time) and `examples` (array of `before`/`after` code pairs). |
| `impacts` | `object[]` | Array of objects with `softwareQuality` (`SECURITY`, `RELIABILITY`, `MAINTAINABILITY`) and `severity` (`HIGH`, `MEDIUM`, `LOW`). |
| `defaultSeverity` | `string` | Same as `severity`; the default when no profile override is set. |
| `status` | `string` | Rule lifecycle status. Use `READY` for active rules. |
| `debt` | `object` | Technical debt estimation. Contains `function` (`CONSTANT_ISSUE` or `LINEAR`), `offset`, and optionally `coefficient`. |

#### Optional Fields

| Field | Type | Description |
|---|---|---|
| `params` | `object[]` | Configurable parameters. Each has `key`, `name`, `description`, `defaultValue`, and `type` (`INTEGER`, `STRING`, `BOOLEAN`). |

#### Template

```json
{
  "key": "rule-key-here",
  "name": "Human-Readable Rule Name",
  "description": "Clear description of what the rule detects and why it is important.",
  "severity": "MAJOR",
  "type": "CODE_SMELL",
  "tags": ["category", "relevant-tag"],
  "remediation": {
    "constantCost": "15min",
    "examples": [
      {
        "before": "// Non-compliant code example",
        "after": "// Compliant code example"
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

#### Severity Guidelines

- **BLOCKER** — Must fix immediately. Security risk with direct exploit potential (e.g., hardcoded credentials).
- **CRITICAL** — High-priority fix. Exploitable vulnerabilities or severe performance issues (e.g., SQL injection, N+1 queries).
- **MAJOR** — Should fix soon. Design problems impacting maintainability (e.g., god classes, deep nesting).
- **MINOR** — Fix when convenient. Style or convention issues (e.g., inconsistent naming).
- **INFO** — Informational. Suggestions for improvement.

#### Debt Function Types

- **CONSTANT_ISSUE** — Fixed remediation cost per occurrence. Uses `offset` only (e.g., `"offset": "15min"`).
- **LINEAR** — Cost scales with issue size. Uses `coefficient` (per unit of measure) and `offset` (base cost). Example: `"coefficient": "1min", "offset": "0min"` for complexity-based rules.

---

### 5. Best Practices

#### When Creating New Rules

1. **Place in the correct category directory** — Choose `security/`, `code-smells/`, `performance/`, or `maintainability/` based on the primary concern.
2. **Follow the naming convention** — Filename must be `lowercase-hyphenated.json` and match the `key` field.
3. **Write clear descriptions** — Explain both *what* the rule detects and *why* it matters.
4. **Provide concrete remediation examples** — Include realistic `before` (non-compliant) and `after` (compliant) code snippets.
5. **Set appropriate severity** — Use the severity guidelines above. When in doubt, start at `MAJOR` and adjust.
6. **Choose the correct type** — `VULNERABILITY` for security issues, `BUG` for reliability problems, `CODE_SMELL` for design/quality issues.
7. **Use meaningful tags** — Include the category name and relevant domain terms. Use `owasp-top-10` for applicable security rules.
8. **Add configurable parameters** when thresholds make sense (e.g., max complexity, max line count). Always provide sensible default values.
9. **Keep `status` as `READY`** for rules that are complete and active.
10. **Validate JSON** — Ensure the file is valid JSON before committing.

#### When Modifying Existing Rules

1. **Do not change the `key` field** — It is the unique identifier and may be referenced externally.
2. **Preserve backward compatibility** — If changing `params`, keep existing parameter keys and add new ones rather than renaming.
3. **Update the description** if the rule's detection scope changes.

#### General Guidelines

- Each rule file should be self-contained with all information needed to understand, configure, and remediate the issue.
- Remediation examples should use Java conventions by default (matching SonarQube's primary ecosystem), but note the language if targeting a different one.
- When asked to explain a rule, reference the actual JSON fields and provide the remediation examples from the file.
- When asked to create a new rule, always generate the complete JSON structure with all required fields and validate it against the template above.

