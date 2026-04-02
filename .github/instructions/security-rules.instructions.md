---
description: "Use when creating, editing, or reviewing SonarQube security vulnerability rules in rules/security/. Covers injection, XSS, SSRF, CSRF, cryptography, and OWASP Top 10 rule authoring."
applyTo: "rules/security/**"
---

# Security Rules — Authoring Guidelines

## Category Overview

The `rules/security/` directory contains **vulnerability detection rules** — rules that identify exploitable weaknesses in application code. These rules protect against attackers and map directly to industry standards like the OWASP Top 10.

Currently contains **15 rules** covering: injection (SQL, command, LDAP, XSS), authentication & secrets (hardcoded credentials, insecure cookies, insecure random), data handling (sensitive data exposure, insecure deserialization, XML external entities), and network (SSRF, open redirect, CSRF, path traversal, weak cryptography).

## Mandatory Constraints

- **`type` must be `VULNERABILITY`** — every security rule is a vulnerability, never `CODE_SMELL` or `BUG`.
- **`severity` must be `CRITICAL` or `BLOCKER`** — security issues are never `MAJOR`, `MINOR`, or `INFO`.
  - Use `BLOCKER` for issues leading to direct data compromise or system takeover (e.g., hardcoded credentials, RCE vectors).
  - Use `CRITICAL` for exploitable vulnerabilities requiring specific conditions (e.g., SQL injection, XSS, SSRF).
- **`impacts[].softwareQuality` must be `SECURITY`** with severity `HIGH`.
- **`tags` must include `"security"`** as the first tag. Add `"owasp-top-10"` when the rule maps to an OWASP Top 10 category.
- **`severity` and `defaultSeverity` must match.**

## Tag Conventions

Always include these tags where applicable:

| Tag | When to Use |
|-----|-------------|
| `security` | Every rule (required) |
| `owasp-top-10` | Maps to an OWASP Top 10 category |
| `injection` | Any input-to-interpreter flow (SQL, LDAP, command, XSS) |
| `credentials` | Hardcoded secrets, weak authentication |
| `cryptography` | Weak algorithms, insecure random |
| `xss` | Cross-site scripting variants |
| `csrf` | Cross-site request forgery |
| `ssrf` | Server-side request forgery |

## Writing Descriptions

Security rule descriptions must clearly articulate:
1. **What** the rule detects (the vulnerable pattern)
2. **How** an attacker can exploit it (the threat model)
3. **What data or systems** are at risk (the impact)

Example: *"Detects potential SQL injection vulnerabilities where user input is directly concatenated into SQL queries without proper sanitization or parameterization."*

## Remediation Examples

Security remediation examples must show:
- **`before`**: Realistic vulnerable code — not pseudocode, but something a developer would actually write.
- **`after`**: The secure alternative using industry best practices (parameterized queries, output encoding, secrets managers, etc.).

Keep examples language-agnostic when possible, but Java is the primary target language.

## Remediation Cost Guidelines

| Fix Type | Typical Cost |
|----------|-------------|
| Switch to parameterized API (e.g., PreparedStatement) | `30min` |
| Add output encoding/sanitization | `20min` |
| Move secret to environment variable/vault | `15min` |
| Add CSRF token or cookie flags | `15min` |
| Replace weak crypto algorithm | `30min` |
| Redesign deserialization approach | `1h` |

## Debt Model

Security rules use `CONSTANT_ISSUE` debt — every instance costs a fixed amount to fix regardless of code size.

```json
"debt": {
  "function": "CONSTANT_ISSUE",
  "offset": "30min"
}
```

## Params

Security rules generally **do not** have configurable `params` — a vulnerability is either present or not. Avoid adding thresholds to security rules.

## Checklist for New Security Rules

1. `key` is lower-kebab-case and matches the filename
2. `type` is `VULNERABILITY`
3. `severity` is `CRITICAL` or `BLOCKER`
4. `defaultSeverity` matches `severity`
5. `tags` includes `"security"` first, plus relevant sub-tags
6. `impacts` includes `{ "softwareQuality": "SECURITY", "severity": "HIGH" }`
7. `description` explains the vulnerability, attack vector, and impact
8. `remediation.examples` has at least one realistic before/after pair
9. `status` is `"READY"`
10. JSON is valid and well-formed
