---
applyTo: rules/security/**
---

# Security Rules — Custom Instructions

You are assisting with SonarQube **security vulnerability** rule definitions in `rules/security/`.

## Category Context

These rules detect exploitable vulnerabilities — injection flaws, authentication weaknesses, cryptographic misuse, and data exposure. They protect applications from active attackers.

## Key Constraints

- **`type`** must always be `"VULNERABILITY"`.
- **`severity`** should be `CRITICAL` or `BLOCKER` for most security rules. Use `MAJOR` only for low-exploitability findings.
- **`impacts[].softwareQuality`** must be `"SECURITY"` (primary). Add `"RELIABILITY"` only if the flaw also causes crashes.
- **`impacts[].severity`** should be `"HIGH"` for most vulnerabilities.
- **Tags**: Always include `"security"`. Add `"owasp-top-10"` when the rule maps to an OWASP Top 10 category. Use specific tags like `"injection"`, `"authentication"`, `"cryptography"`, `"xss"`, `"ssrf"` as appropriate.

## Description Guidelines

- Explain the **attack vector** — how can an attacker exploit this?
- State the **impact** — what happens if exploited (data breach, RCE, privilege escalation)?
- Reference relevant standards (OWASP, CWE) in the description when applicable.

## Remediation Examples

- The `before` example must show realistic vulnerable code (e.g., unsanitized user input flowing into a dangerous sink).
- The `after` example must show a proper fix (parameterized queries, input validation, allowlists, encoding).
- Use Java as the default language for examples unless the user specifies otherwise.

## Remediation Cost

- Simple fixes (adding a flag, using a built-in safe API): `"15min"` to `"30min"`
- Architectural changes (implementing CSRF framework, redesigning auth flow): `"2h"` to `"4h"`

## Naming

- Keys should name the vulnerability class in lower-kebab-case: `sql-injection`, `xss-vulnerability`, `hardcoded-credentials`.
- Prefer specific names over generic ones (e.g., `ldap-injection` not `injection-flaw`).
