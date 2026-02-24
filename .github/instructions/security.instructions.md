---
applyTo: "rules/security/**"
---

# Security Rules — Path-Specific Custom Instructions

You are working inside `rules/security/`, which contains **15 SonarQube rule definitions** that detect exploitable vulnerabilities in application code. These rules are the highest-priority category in the repository — many map directly to OWASP Top 10 weaknesses.

---

## Purpose of This Category

Security rules identify code patterns that could be exploited by attackers to gain unauthorized access, steal data, execute arbitrary code, or disrupt services. Every rule in this directory has `"type": "VULNERABILITY"` and impacts `"softwareQuality": "SECURITY"`.

---

## Current Rules Inventory (15 rules)

| File | Key | Severity | What It Detects |
|---|---|---|---|
| `command-injection.json` | `command-injection` | CRITICAL | OS command injection via unsanitized user input in `Runtime.exec()` or `ProcessBuilder` |
| `csrf-vulnerability.json` | `csrf-vulnerability` | MAJOR | Missing CSRF token validation on state-changing endpoints (POST, PUT, DELETE) |
| `hardcoded-credentials.json` | `hardcoded-credentials` | BLOCKER | Passwords, API keys, tokens, or secrets hard-coded in source |
| `insecure-cookie.json` | `insecure-cookie` | CRITICAL | Cookies missing `Secure`, `HttpOnly`, or `SameSite` flags |
| `insecure-deserialization.json` | `insecure-deserialization` | CRITICAL | Unsafe deserialization of untrusted data (potential RCE via `ObjectInputStream`) |
| `insecure-random.json` | `insecure-random` | MAJOR | `java.util.Random` used for security-sensitive operations instead of `SecureRandom` |
| `ldap-injection.json` | `ldap-injection` | BLOCKER | User input concatenated directly into LDAP filters |
| `open-redirect.json` | `open-redirect` | CRITICAL | User-controlled redirect URLs without domain whitelist validation |
| `path-traversal.json` | `path-traversal` | CRITICAL | User input in file paths allowing `../` traversal outside intended directories |
| `sensitive-data-exposure.json` | `sensitive-data-exposure` | CRITICAL | Logging of passwords, PII, credit cards, or SSNs |
| `server-side-request-forgery.json` | `server-side-request-forgery` | BLOCKER | User-controlled URLs used in server-side HTTP requests (SSRF) |
| `sql-injection.json` | `sql-injection` | CRITICAL | SQL queries built with string concatenation instead of parameterized statements |
| `weak-cryptography.json` | `weak-cryptography` | CRITICAL | Use of MD5, SHA1, DES, RC4, or other deprecated cryptographic algorithms |
| `xml-external-entity.json` | `xml-external-entity` | BLOCKER | XML parsers configured to process external entities (XXE) |
| `xss-vulnerability.json` | `xss-vulnerability` | CRITICAL | User-supplied data rendered in HTML without encoding or sanitization |

---

## Category-Specific Conventions

### Type & Severity Patterns

- **Type** is always `"VULNERABILITY"` — no exceptions for this directory.
- **Severity** is `BLOCKER` or `CRITICAL` for most rules. Use `BLOCKER` for issues that can lead to full system compromise (RCE, auth bypass, SSRF to internal services). Use `CRITICAL` for issues that expose data or enable client-side attacks. `MAJOR` is reserved for lower-risk weaknesses (e.g., missing CSRF, insecure random).
- **`defaultSeverity`** must always match `severity`.

### Impacts

- `softwareQuality` is always `"SECURITY"`.
- `severity` is almost always `"HIGH"`. Use `"MEDIUM"` only for lower-risk items like `csrf-vulnerability` or `insecure-random`.

### Tags

- Always include `"security"` as the first tag.
- Include `"owasp-top-10"` if the vulnerability maps to an OWASP Top 10 category.
- Add the specific attack vector as a tag (e.g., `"injection"`, `"xss"`, `"ssrf"`, `"csrf"`).
- Optionally add context tags (e.g., `"web"`, `"xml"`, `"cryptography"`, `"authentication"`).

### Debt Model

- All current security rules use `"function": "CONSTANT_ISSUE"` — each occurrence takes a fixed time to fix regardless of complexity.
- `offset` values range from `"10min"` (simple replacements like `Random` → `SecureRandom`) to `"45min"` (complex fixes like SSRF, LDAP injection, insecure deserialization).
- Do **not** use `LINEAR` debt for security rules — vulnerability fixes don't scale linearly with a measurable metric.

### Remediation Examples

- Security rule examples must show the **vulnerable pattern** in `before` and the **secure fix** in `after`.
- Use realistic, minimal code — prefer Java examples for consistency with the existing rules.
- The `after` example must demonstrate the correct mitigation (parameterized queries, input validation, secure configuration) — not just error handling.
- Include comments in `after` to explain _why_ the fix works when it's not obvious.

---

## Guidelines for Creating New Security Rules

1. **Verify it doesn't duplicate an existing rule**: Check the 15 rules above. Injection subtypes (SQL, LDAP, command, XSS) are separate rules; don't merge them.
2. **Map to OWASP Top 10 when applicable**: Tag with `"owasp-top-10"` and note the category (A01–A10) in the description if relevant.
3. **Set severity realistically**: RCE-capable → BLOCKER. Data exposure → CRITICAL. Client-side only → CRITICAL. Defense-in-depth issues → MAJOR.
4. **Write an actionable description**: State what the code does wrong, what an attacker can achieve, and the recommended mitigation in 1–3 sentences.
5. **constantCost should reflect real fix time**: Simple API swaps (10–15min), adding validation logic (20–30min), architectural rework (45–60min).
6. **No configurable `params`**: None of the existing security rules have `params` — vulnerability detection is binary (present or not), not threshold-based.

---

## Common Pitfalls to Avoid

- **Don't set security rules to MINOR or INFO** — every vulnerability warrants at least MAJOR.
- **Don't use `"type": "CODE_SMELL"` or `"type": "BUG"`** in this directory — all security rules are `VULNERABILITY`.
- **Don't provide `after` examples that merely suppress the warning** — always show the proper secure fix.
- **Don't forget the `"owasp-top-10"` tag** when the rule maps to a Top 10 category.
- **Don't add `params`** unless the rule genuinely has a configurable threshold (none currently do).
