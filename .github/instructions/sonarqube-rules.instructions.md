---
applyTo: "rules/**/*.json"
description: "Guidance for creating, managing, and understanding SonarQube Rules Files in this repository."
---

# SonarQube Rules — Custom Instructions

These instructions guide the assistant when helping users create, edit, review, or explain SonarQube rule definitions stored in this repository.

## 1. Overview

SonarQube Rules Files are JSON documents that define static-analysis rules consumed by SonarQube custom rule plugins or used as a reference for building custom quality profiles. Each file defines exactly **one rule** and describes:

- What the rule detects
- How severe it is and what kind of issue it represents
- How to remediate violations (with before/after code examples)
- The rule's impact on software quality attributes (security, reliability, maintainability)
- Estimated technical debt and any configurable parameters

Rules in this repo are intended as authoritative, copy-pasteable specifications. Treat them as production artifacts: changes must remain valid JSON and conform to the conventions below.

## 2. Directory Structure

All rules live under `rules/` and are organized by category. **One rule per file.** The filename is the rule's kebab-case `key` plus `.json`.

```
rules/
├── security/         # Vulnerabilities and security weaknesses
├── code-smells/      # Design and code-quality smells
├── performance/      # Runtime and resource-efficiency issues
└── maintainability/  # Readability, modularity, and long-term upkeep
```

When adding a rule, place it in the directory whose theme best matches its **primary** impact. If a rule legitimately spans categories (e.g., a security issue with major performance implications), pick the dominant concern and reflect the secondary concern via `tags` and additional `impacts` entries.

## 3. Rule Categories and Contents

### 3.1 `rules/security/` (15 rules) — `type: VULNERABILITY`

Rules that detect exploitable weaknesses. Severity skews `CRITICAL` or `BLOCKER`. Tags typically include `security` and an OWASP reference (e.g., `owasp-top-10`).

- `command-injection` — User input passed to OS commands.
- `csrf-vulnerability` — Missing CSRF protection on state-changing endpoints.
- `hardcoded-credentials` — Passwords, API keys, or tokens in source.
- `insecure-cookie` — Cookies missing `Secure`, `HttpOnly`, or `SameSite`.
- `insecure-deserialization` — Unsafe deserialization of untrusted data.
- `insecure-random` — Predictable RNGs in security contexts.
- `ldap-injection` — Unsanitized input concatenated into LDAP filters.
- `open-redirect` — User-controlled redirect targets.
- `path-traversal` — Filesystem access escaping intended directories.
- `sensitive-data-exposure` — Logging of secrets or PII.
- `server-side-request-forgery` — User-controlled URLs in server-side requests.
- `sql-injection` — Unsanitized input in SQL queries.
- `weak-cryptography` — MD5, SHA1, DES, etc.
- `xml-external-entity` — XML parsers with external entity processing enabled.
- `xss-vulnerability` — Cross-site scripting risks.

### 3.2 `rules/code-smells/` (13 rules) — `type: CODE_SMELL`

Rules that flag designs that work but harm quality. Severity is usually `MAJOR` or `MINOR`.

- `complex-methods`, `data-clumps`, `dead-code`, `duplicate-code`, `empty-catch-block`, `feature-envy`, `god-class`, `long-parameter-list`, `magic-numbers`, `message-chains`, `primitive-obsession`, `refused-bequest`, `speculative-generality`.

### 3.3 `rules/performance/` (12 rules) — `type: CODE_SMELL` (occasionally `BUG`)

Rules targeting runtime efficiency, memory, I/O, and database access patterns.

- `connection-pool-exhaustion`, `excessive-object-creation`, `inefficient-collection-usage`, `inefficient-loops`, `memory-leaks`, `missing-lazy-initialization`, `n-plus-one-query`, `string-concatenation-in-loop`, `synchronous-io-in-async`, `unbounded-collection-growth`, `unnecessary-boxing`, `unoptimized-regex`.

### 3.4 `rules/maintainability/` (12 rules) — `type: CODE_SMELL`

Rules focused on long-term readability, cohesion, and change cost.

- `boolean-blindness`, `circular-dependencies`, `deep-nesting`, `excessive-comments`, `hardcoded-urls`, `hidden-dependencies`, `inconsistent-naming`, `long-methods`, `missing-javadoc`, `missing-null-check`, `shotgun-surgery`, `too-many-parameters`.

## 4. Rule File Schema

Every rule file is a single JSON object with the following fields. Required fields are marked with **(required)**.

| Field | Type | Notes |
|---|---|---|
| `key` **(required)** | string | Unique kebab-case ID. Must match the filename (without `.json`). |
| `name` **(required)** | string | Short human-readable title (Title Case). |
| `description` **(required)** | string | One- or two-sentence explanation of what the rule detects and why it matters. |
| `severity` **(required)** | enum | `BLOCKER` \| `CRITICAL` \| `MAJOR` \| `MINOR` \| `INFO`. |
| `type` **(required)** | enum | `VULNERABILITY` \| `BUG` \| `CODE_SMELL`. |
| `tags` **(required)** | string[] | Lowercase, kebab-case. Always include the category and any standards refs (e.g., `owasp-top-10`, `cwe`). |
| `remediation` **(required)** | object | See below. |
| `impacts` **(required)** | object[] | One or more `{ softwareQuality, severity }` entries. |
| `defaultSeverity` **(required)** | enum | Same enum as `severity`; usually identical. |
| `status` **(required)** | enum | Typically `READY`. Other valid values: `BETA`, `DEPRECATED`, `REMOVED`. |
| `debt` **(required)** | object | Technical-debt model. See below. |
| `params` | object[] | Optional configurable parameters. Include only when the rule is tunable. |

### 4.1 `remediation`

```json
"remediation": {
  "constantCost": "30min",
  "examples": [
    { "before": "<bad code>", "after": "<good code>" }
  ]
}
```

- `constantCost` uses SonarQube duration syntax: `Nmin`, `Nh`, `Nd` (e.g., `15min`, `2h`, `1d`).
- Provide at least one before/after example. Keep examples short, idiomatic, and language-appropriate (Java is the default in this repo).

### 4.2 `impacts`

```json
"impacts": [
  { "softwareQuality": "SECURITY", "severity": "HIGH" }
]
```

- `softwareQuality`: `SECURITY` \| `RELIABILITY` \| `MAINTAINABILITY`.
- `severity` (impact): `HIGH` \| `MEDIUM` \| `LOW`.
- Multiple entries are allowed when a rule meaningfully affects more than one quality.

### 4.3 `debt`

Two common shapes:

```json
"debt": { "function": "CONSTANT_ISSUE", "offset": "30min" }
```

```json
"debt": { "function": "LINEAR", "coefficient": "10min", "offset": "0min" }
```

- Use `CONSTANT_ISSUE` for fixed-cost issues (e.g., a single SQL injection site).
- Use `LINEAR` when remediation cost scales with size (e.g., per-method or per-line growth in a god class).
- A `LINEAR_OFFSET` variant exists when both a fixed setup cost and a per-unit cost apply.

### 4.4 `params` (optional)

```json
"params": [
  {
    "key": "max",
    "name": "Maximum Lines",
    "description": "Maximum allowed lines of code per method",
    "defaultValue": "100",
    "type": "INTEGER"
  }
]
```

- `type`: `INTEGER` \| `STRING` \| `BOOLEAN` \| `FLOAT` \| `TEXT`.
- `defaultValue` is always a **string**, even for numeric or boolean params.
- Use `params` only when a threshold or toggle would realistically be tuned per project.

### 4.5 Canonical Example

```json
{
  "key": "sql-injection",
  "name": "SQL Injection Prevention",
  "description": "Detects potential SQL injection vulnerabilities where user input is directly concatenated into SQL queries without proper sanitization or parameterization.",
  "severity": "CRITICAL",
  "type": "VULNERABILITY",
  "tags": ["security", "sql", "injection", "owasp-top-10"],
  "remediation": {
    "constantCost": "30min",
    "examples": [
      {
        "before": "String query = \"SELECT * FROM users WHERE id = \" + userId;",
        "after": "PreparedStatement stmt = connection.prepareStatement(\"SELECT * FROM users WHERE id = ?\");\nstmt.setString(1, userId);"
      }
    ]
  },
  "impacts": [
    { "softwareQuality": "SECURITY", "severity": "HIGH" }
  ],
  "defaultSeverity": "CRITICAL",
  "status": "READY",
  "debt": { "function": "CONSTANT_ISSUE", "offset": "30min" }
}
```

## 5. Best Practices

### Authoring
- **Filename = key.** Always use kebab-case and keep them in sync.
- **One rule per file.** Never bundle multiple rules into a single JSON document.
- **Pick the right type.** `VULNERABILITY` for exploitable security issues, `BUG` for code that is demonstrably wrong, `CODE_SMELL` for design/maintainability issues.
- **Match severity to impact.** `BLOCKER` for issues that should fail a build (hardcoded credentials, RCE-class bugs); `CRITICAL` for high-risk vulnerabilities and severe correctness/perf bugs; `MAJOR` is the default for most smells; `MINOR`/`INFO` for stylistic concerns.
- **Keep descriptions concrete.** Lead with what is detected, then why it matters. Avoid marketing language.
- **Make examples runnable in spirit.** Before/after snippets should be syntactically plausible and demonstrate the actual fix, not a vague comment — except where the rule is structural (e.g., "class with 2000+ lines"), in which case use a clear comment placeholder consistent with existing rules.
- **Tag deliberately.** Include the category, the language ecosystem if relevant (`java`, `spring`, `jpa`), and standards (`owasp-top-10`, `cwe-89`).
- **Estimate debt honestly.** Use `CONSTANT_ISSUE` for site-local fixes; `LINEAR` when remediation scales (per method, per line, per call site).

### Reviewing & Editing
- Validate that the file is well-formed JSON (no trailing commas, all strings double-quoted).
- Confirm `key`, filename, and directory category are consistent.
- Check that `severity` and `defaultSeverity` agree unless there is an intentional reason to diverge.
- Ensure every required field is present (see schema table) and every enum value is from the allowed set.
- When changing thresholds, update both the `description` (if it cites the threshold) and the relevant `params.defaultValue`.

### Contributing
1. Create the file under the correct category directory using the exact `key` as the filename.
2. Follow the canonical example above; copy a sibling rule as a starting point for consistency.
3. Update `README.md` to list the new rule under its category and bump the rule count.
4. Verify JSON validity (`python -m json.tool <file>` or `jq . <file>`).
5. Keep PRs focused: one rule add/change per PR when practical.

### What to Avoid
- Do **not** invent fields outside the schema in §4 — SonarQube ignores unknown fields and they create drift.
- Do **not** use camelCase or snake_case for `key` or `tags`; stick to kebab-case.
- Do **not** copy a rule's `key` from another file; keys must be globally unique within the repo.
- Do **not** leave `examples` empty; a missing example significantly reduces the rule's usefulness for downstream users.
