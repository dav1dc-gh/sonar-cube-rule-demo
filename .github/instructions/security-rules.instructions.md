---
applyTo: "rules/security/**/*.json"
description: "Authoring and review guidance for SonarQube security (VULNERABILITY) rules."
---

# Security Rules — Custom Instructions

Scope: every JSON file under `rules/security/`. These rules describe **exploitable weaknesses** in source code. They are the highest-stakes artifacts in this repo; precision and conservative defaults matter more than tunability.

> Read [sonarqube-rules.instructions.md](.github/instructions/sonarqube-rules.instructions.md) first for the shared schema. This file only documents what is **specific to security rules**.

## 1. Mandatory field values

| Field | Required value for this category |
|---|---|
| `type` | `VULNERABILITY` (use `BUG` only for a definite, non-exploitable correctness defect — extremely rare here). |
| `severity` / `defaultSeverity` | `CRITICAL` by default. Use `BLOCKER` for unauthenticated RCE-class issues, hardcoded secrets, or anything that should fail a build outright. `MAJOR` is the floor; never use `MINOR` or `INFO`. |
| `impacts` | Must include `{ "softwareQuality": "SECURITY", "severity": "HIGH" }`. Add a second impact (`RELIABILITY` / `MAINTAINABILITY`) only when the weakness also reliably causes outages or data corruption. |
| `status` | `READY`. Use `BETA` only for detectors with known false-positive rates above ~10%. |
| `debt.function` | `CONSTANT_ISSUE` for the typical site-local fix (parameterize a query, add a header, swap an algorithm). Use `LINEAR` only when remediation realistically scales (e.g., a sweeping cookie-flag rollout across many handlers). |
| `debt.offset` | Minimum `20min`. Most security fixes — including review and regression test — land in `30min`–`1h`. |

## 2. Required tags

Every security rule must include, in this order:

1. `"security"` — the category tag.
2. A **standards reference** — at least one of:
   - `"owasp-top-10"` (preferred when an OWASP A0x category applies)
   - `"sans-top-25"`
   - `"cwe"` plus a specific id like `"cwe-89"` (SQLi), `"cwe-79"` (XSS), `"cwe-22"` (path traversal), `"cwe-78"` (command injection), `"cwe-352"` (CSRF), `"cwe-611"` (XXE), `"cwe-918"` (SSRF), `"cwe-798"` (hardcoded creds), `"cwe-327"` (weak crypto), `"cwe-330"` (insecure RNG), `"cwe-502"` (insecure deserialization), `"cwe-601"` (open redirect), `"cwe-90"` (LDAP injection), `"cwe-200"` / `"cwe-532"` (sensitive-data exposure / log leak).
3. A **technique tag** describing the weakness class: `"injection"`, `"xss"`, `"crypto"`, `"deserialization"`, `"authentication"`, `"authorization"`, `"session"`, `"transport"`, `"ssrf"`, `"csrf"`, `"redirect"`, etc.
4. Optional **technology tags** when the rule is stack-specific: `"jdbc"`, `"jpa"`, `"spring"`, `"servlet"`, `"jaxrs"`, `"jackson"`, `"xml"`.

Do not add marketing tags (`"important"`, `"critical"`) — severity already conveys that.

## 3. Description guidance

- One or two sentences. Lead with **what the rule detects in the code**, then **why it is dangerous**.
- Name the **untrusted source** explicitly when relevant: "user input", "HTTP request parameters", "deserialized data", "external URL".
- Name the **sink** explicitly: SQL query, OS command, LDAP filter, redirect target, deserializer, file path, response body.
- Avoid CVE numbers, vendor names, and prose like "as everyone knows".

Good: *"Detects potential SQL injection vulnerabilities where user input is directly concatenated into SQL queries without proper sanitization or parameterization."*

Bad: *"This very important rule helps you avoid the most common security mistake."*

## 4. `remediation.examples` rules

- Provide at least **one** before/after pair showing the **actual safe API**, not a comment placeholder. Security rules are the one category where vague comments are not acceptable — the example is the fix recipe.
- The `before` snippet must contain the dangerous pattern verbatim (string concatenation into a sink, `Runtime.exec`, `MessageDigest.getInstance("MD5")`, `new Random()`, `ObjectInputStream.readObject()`, etc.).
- The `after` snippet must show the canonical mitigation, e.g.:
  - SQLi → `PreparedStatement` with `setString(...)`.
  - Command injection → `ProcessBuilder` with an argument list, never a single shell string.
  - XSS → context-appropriate output encoding (HTML, JS, URL) or a templating engine's auto-escape.
  - Path traversal → canonicalize and verify against an allow-listed base directory.
  - Weak crypto → SHA-256 / SHA-3 / AES-GCM / Argon2 / bcrypt as appropriate.
  - Insecure RNG → `SecureRandom`.
  - Hardcoded creds → environment variable or secret manager lookup.
  - XXE → `setFeature("http://apache.org/xml/features/disallow-doctype-decl", true)` or equivalent.
  - SSRF → URL allow-list and DNS pinning, never blacklist regex.
  - Open redirect → match against a server-side allow-list of relative paths.
- Keep snippets small (≤ 6 lines). Use `\n` for line breaks inside the JSON string.
- Java is the default language. Add a second example in another language only if the weakness manifests very differently there.

## 5. `params` policy

Security rules should be **non-tunable** by default — making them configurable is a foot-gun. Only define `params` when there is a clear safe knob:

- An **allow-list** of acceptable algorithms / hosts / ciphers (`type: STRING`, comma-separated).
- A **minimum** value (e.g., minimum key length, minimum bcrypt cost) where the default is the safe floor and operators may only raise it.

Never expose a parameter that lets a user **lower** the security threshold.

## 6. Review checklist

Before approving any change under `rules/security/`:

- [ ] `type` is `VULNERABILITY` and severity is `CRITICAL` or `BLOCKER`.
- [ ] Impacts include `SECURITY: HIGH`.
- [ ] Tags include `security` + at least one OWASP/CWE reference + a technique tag.
- [ ] Description names both the untrusted source and the sink.
- [ ] At least one before/after example shows real, idiomatic mitigation code (not a comment).
- [ ] `key` matches the filename and is kebab-case.
- [ ] No `params` that can weaken the rule.
- [ ] Debt is `CONSTANT_ISSUE` with offset ≥ `20min`, or `LINEAR` with justification.

## 7. Anti-patterns to flag in review

- Severity `MAJOR` or lower — almost always wrong for a real vulnerability.
- Missing CWE/OWASP tag — the rule cannot be mapped to compliance reports.
- `after` snippet that "validates" with a regex blacklist — recommend allow-lists instead.
- `after` snippet that hashes passwords with SHA-256 alone — should be bcrypt/scrypt/Argon2.
- Treating a security rule as `CODE_SMELL` because the team is "not ready to enforce it yet" — use `status: BETA` instead, keep `type: VULNERABILITY`.
