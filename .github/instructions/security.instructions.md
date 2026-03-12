---
applyTo: "rules/security/**"
---

# Security Rules — Custom Instructions

You are assisting with **security vulnerability detection rules** in the `rules/security/` directory. These rules identify exploitable weaknesses in application code, aligned with industry standards like the OWASP Top 10.

---

## Category Conventions

Security rules in this repository follow strict, uniform conventions. Adhere to these exactly:

### Type & Impact

- **Type**: Always `"VULNERABILITY"`. Never use `"BUG"` or `"CODE_SMELL"` for security rules.
- **Impact**: Always `{ "softwareQuality": "SECURITY", "severity": "HIGH" }`. Security findings are always high-severity impacts on the SECURITY quality dimension.

### Severity

Choose severity based on exploitability and blast radius:

| Severity | When to Use | Examples |
|---|---|---|
| **BLOCKER** | Direct RCE, credential exposure, server-side injection allowing full system compromise | hardcoded-credentials, ldap-injection, server-side-request-forgery, xml-external-entity |
| **CRITICAL** | Injection, XSS, path traversal, insecure deserialization — high-risk but typically require specific conditions | command-injection, sql-injection, xss-vulnerability, path-traversal, insecure-deserialization, open-redirect, weak-cryptography, insecure-cookie, sensitive-data-exposure |
| **MAJOR** | Defense-in-depth issues, missing protections that raise risk but are not directly exploitable alone | csrf-vulnerability, insecure-random |

MINOR and INFO are **not used** for security rules.

### Debt Model

- **Always** use `"function": "CONSTANT_ISSUE"`. Security fixes are discrete actions (swap an API call, add a flag, use parameterized queries), so fix time does not scale with code size.
- **Never** use `LINEAR` for security rules.
- **Typical offsets**: 10min–45min. Choose based on the complexity of the remediation:
  - 10–15min: Simple flag additions (e.g., setting `HttpOnly` on a cookie)
  - 20–30min: Switching to a safe API or adding input validation
  - 30–45min: Architectural changes (e.g., refactoring deserialization, implementing CSRF tokens)

### Parameters

- Security rules **do not** use configurable `params`. There are no thresholds to tune — a vulnerability is either present or not.

### Tags

Always include these base tags:
- `"security"` — mandatory for every security rule
- `"owasp-top-10"` — include when the vulnerability maps to an OWASP Top 10 category

Add specific attack/domain tags for discoverability. Use existing tag conventions:
- Attack types: `injection`, `sql`, `xss`, `cross-site-scripting`, `csrf`, `xxe`, `rce`, `command-execution`, `ldap`, `deserialization`, `phishing`
- Domains: `cryptography`, `encryption`, `cookies`, `credentials`, `secrets`, `tokens`, `authentication`, `session-management`, `random`, `logging`, `pii`, `gdpr`, `path-traversal`, `file-access`, `web`, `network`, `ssrf`, `xml`

### Code Examples

- **Language**: Always Java. SonarQube is Java-centric and all existing security rules use Java examples.
- **Before example**: Show the vulnerable pattern with a comment explaining the risk (e.g., `// Vulnerable: user input concatenated directly`).
- **After example**: Show the secure fix using the recommended API or pattern (e.g., parameterized queries, sanitization, safe configuration).
- Keep examples minimal — just enough code to demonstrate the vulnerability and fix. No boilerplate imports or class wrappers unless essential for clarity.

---

## Existing Rules Reference

The following 15 rules exist in `rules/security/`. Check this list before creating a new rule to avoid duplication:

| File | Key | Severity | Detects |
|---|---|---|---|
| `command-injection.json` | command-injection | CRITICAL | OS command injection via unsanitized input |
| `csrf-vulnerability.json` | csrf-vulnerability | MAJOR | Missing CSRF protection on state-changing endpoints |
| `hardcoded-credentials.json` | hardcoded-credentials | BLOCKER | Passwords, API keys, tokens hardcoded in source |
| `insecure-cookie.json` | insecure-cookie | CRITICAL | Cookies missing Secure/HttpOnly/SameSite flags |
| `insecure-deserialization.json` | insecure-deserialization | CRITICAL | Unsafe deserialization of untrusted data |
| `insecure-random.json` | insecure-random | MAJOR | Predictable RNG in security-sensitive contexts |
| `ldap-injection.json` | ldap-injection | BLOCKER | User input concatenated into LDAP queries |
| `open-redirect.json` | open-redirect | CRITICAL | User-controlled redirect URLs |
| `path-traversal.json` | path-traversal | CRITICAL | File path manipulation outside intended directories |
| `sensitive-data-exposure.json` | sensitive-data-exposure | CRITICAL | Logging of passwords, PII, or sensitive data |
| `server-side-request-forgery.json` | server-side-request-forgery | BLOCKER | User-controlled URLs in server-side HTTP requests |
| `sql-injection.json` | sql-injection | CRITICAL | SQL query string concatenation with user input |
| `weak-cryptography.json` | weak-cryptography | CRITICAL | Weak/deprecated algorithms (MD5, SHA1, DES) |
| `xml-external-entity.json` | xml-external-entity | BLOCKER | XML parsers processing external entities |
| `xss-vulnerability.json` | xss-vulnerability | CRITICAL | Unescaped user input rendered in output |

---

## Creating a New Security Rule

When creating a new security rule:

1. **Verify it doesn't overlap** with the 15 existing rules above.
2. **Identify the OWASP category** — most security rules map to an OWASP Top 10 item. Include the `owasp-top-10` tag if applicable.
3. **Describe the attack vector clearly** — the `description` field should explain both *what the vulnerability is* and *how an attacker can exploit it*.
4. **Show realistic vulnerable code** — the `before` example should be code a developer might actually write, not a contrived edge case.
5. **Show the canonical fix** — the `after` example should use the industry-standard remediation (e.g., PreparedStatement for SQL injection, not a regex-based sanitizer).
6. **Set severity by exploitability**: BLOCKER if it enables RCE or full data compromise; CRITICAL for injection/XSS/traversal; MAJOR for defense-in-depth gaps.
7. **Filename must match key**: `my-rule-name.json` → `"key": "my-rule-name"`.

### Template

```json
{
  "key": "new-security-rule",
  "name": "New Security Rule Name",
  "description": "Detects <vulnerability> which allows attackers to <impact>.",
  "severity": "CRITICAL",
  "type": "VULNERABILITY",
  "tags": ["security", "owasp-top-10", "<specific-tag>"],
  "remediation": {
    "constantCost": "20min",
    "examples": [
      {
        "before": "// Vulnerable: <explain risk>\n<vulnerable Java code>",
        "after": "// Fixed: <explain fix>\n<secure Java code>"
      }
    ]
  },
  "impacts": [
    {
      "softwareQuality": "SECURITY",
      "severity": "HIGH"
    }
  ],
  "defaultSeverity": "CRITICAL",
  "status": "READY",
  "debt": {
    "function": "CONSTANT_ISSUE",
    "offset": "20min"
  }
}
```

---

## Common Mistakes to Avoid

- **Don't use `CODE_SMELL` or `BUG`** for security rules — always `VULNERABILITY`.
- **Don't add `params`** — security rules are binary (vulnerable or not).
- **Don't use `LINEAR` debt** — security fixes are discrete, not proportional to code size.
- **Don't set impact to MEDIUM or LOW** — security vulnerabilities are always `HIGH` impact.
- **Don't forget both `severity` and `defaultSeverity`** — they must match.
- **Don't use non-Java examples** — maintain consistency with all existing rules.
