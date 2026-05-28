---
applyTo: "rules/security/**"
---

# Security Rules — Copilot Custom Instructions

You are assisting with SonarQube **security vulnerability** rule definitions in the `rules/security/` directory. This category focuses on detecting exploitable weaknesses that could be leveraged by attackers to compromise confidentiality, integrity, or availability.

---

## Category Context

This directory currently contains **28 rules** covering injection attacks, authentication/authorization flaws, cryptographic weaknesses, data exposure, and configuration vulnerabilities. Rules here map closely to industry standards such as the OWASP Top 10, CWE, and SANS Top 25.

---

## Rule Authoring Guidelines for Security

### Type & Severity
- **Type** must always be `VULNERABILITY`.
- **Severity** is typically `CRITICAL` or `BLOCKER`. Use `CRITICAL` for remotely exploitable issues (injection, SSRF, XSS). Use `BLOCKER` only when exploitation leads to direct data breach or full system compromise with minimal effort.
- Avoid `MAJOR` or lower unless the finding is informational (e.g., weak algorithm usage in non-sensitive context).

### Impacts
- The `softwareQuality` field must be `"SECURITY"` with severity `"HIGH"` for all exploitable vulnerabilities.
- Add a secondary impact of `"RELIABILITY"` if the vulnerability can cause crashes or data corruption.

### Tags — Required Conventions
- Always include `"security"` as the first tag.
- Include `"owasp-top-10"` when the rule maps to an OWASP Top 10 category (most will).
- Include the specific attack vector tag (e.g., `"injection"`, `"xss"`, `"ssrf"`, `"cryptography"`, `"authentication"`).
- Include the CWE identifier tag when known (e.g., `"cwe-89"` for SQL injection).

### Description Best Practices
- Lead with **what** the rule detects, then explain **why** it's dangerous.
- Reference the specific attack scenario: who is the attacker, what input do they control, and what damage can they cause.
- Mention the trust boundary being violated (e.g., "user input reaches a SQL query without sanitization").
- Keep descriptions between 1–3 sentences — concise but threat-aware.

### Remediation Examples
- `before` examples must show **realistic vulnerable code** — not trivially obvious. Show real framework patterns (Spring, Jakarta EE, Express, Django).
- `after` examples must show the **canonical secure fix**: parameterized queries for injection, output encoding for XSS, allowlist validation for redirects, etc.
- Include the language/framework context in comments when the fix is framework-specific.
- Remediation cost should reflect the actual migration effort: simple parameterization → `"30min"`, architecture changes (e.g., adding an auth layer) → `"2h"`–`"4h"`.

### Debt Estimation
- Most security fixes are `CONSTANT_ISSUE` since they involve a localized code change.
- Use `LINEAR` only when remediation scales with the number of occurrences (e.g., replacing all usages of a deprecated crypto API).

### Common Pitfalls to Avoid
- Do NOT set type to `CODE_SMELL` or `BUG` — security rules are always `VULNERABILITY`.
- Do NOT underestimate severity — if code can be exploited remotely, it's at least `CRITICAL`.
- Do NOT write generic descriptions like "this is a security issue" — be specific about the attack vector.
- Do NOT forget to include `"owasp-top-10"` when applicable.

---

## When Creating New Security Rules

1. Verify the vulnerability isn't already covered by an existing rule (check for overlapping attack vectors).
2. Ensure the `key` clearly identifies the attack type (e.g., `"nosql-injection"`, not `"database-issue"`).
3. Cross-reference OWASP, CWE, and SANS to confirm severity classification.
4. Provide at least one remediation example showing vulnerable → secure transformation.
5. Consider whether the rule needs `params` (rare for security rules — most are binary detect/don't-detect).

---

## Existing Rules Reference

command-injection, csrf-vulnerability, disabled-certificate-validation, hardcoded-credentials, improper-error-disclosure, insecure-cookie, insecure-deserialization, insecure-random, integer-overflow, jwt-misconfiguration, ldap-injection, log-injection, mass-assignment, missing-authorization-check, missing-input-validation, open-redirect, path-traversal, permissive-cors, prototype-pollution, sensitive-data-exposure, server-side-request-forgery, sql-injection, timing-attack, uncontrolled-resource-consumption, unsafe-reflection, weak-cryptography, xml-external-entity, xss-vulnerability
