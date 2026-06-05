---
applyTo: rules/security/**
---

# Security Rules — Custom Instructions

You are assisting with SonarQube **security vulnerability** rule definitions in `rules/security/`. These rules detect exploitable weaknesses that could be leveraged by attackers to compromise confidentiality, integrity, or availability.

## Category Constraints

- **`type` MUST be `VULNERABILITY`** — every rule in this directory represents an exploitable security flaw.
- **`severity` should be `CRITICAL` or `BLOCKER`** — security vulnerabilities are high-impact by definition. Use `MAJOR` only for low-exploitability issues with limited blast radius.
- **`tags` MUST include `"security"`** as the first tag. Add relevant standards tags: `"owasp-top-10"`, `"cwe"`, `"sans-top-25"`, `"pci-dss"` where applicable.
- **`impacts` MUST include `{"softwareQuality": "SECURITY", "severity": "HIGH"}`** — security rules always have a HIGH security impact.

## Writing Security Rule Descriptions

Descriptions must clearly communicate:
1. **The attack vector** — how an attacker exploits the vulnerability (e.g., "unsanitized user input concatenated into SQL queries").
2. **The consequence** — what an attacker gains (e.g., "arbitrary data exfiltration, authentication bypass, remote code execution").
3. **The root cause** — the programming mistake that enables it (e.g., "missing input validation", "disabled certificate checking").

Use precise security terminology: injection, traversal, deserialization, SSRF, XSS, CSRF, etc. Reference CWE IDs or OWASP categories in descriptions when applicable.

## Remediation Examples

Security remediation examples MUST show:
- **Before**: A realistic vulnerable code pattern (not pseudocode) demonstrating the flaw.
- **After**: The secure alternative using proper mitigation (parameterized queries, input validation, encoding, secure defaults).

Prefer language-specific idiomatic fixes:
- SQL injection → `PreparedStatement` / parameterized queries
- XSS → context-aware output encoding / template auto-escaping
- Path traversal → canonical path validation / allowlisting
- SSRF → URL allowlisting / blocking internal ranges
- Command injection → avoiding shell execution / using argument arrays
- Deserialization → type allowlisting / using safe formats (JSON)

## Remediation Cost Guidelines

| Fix Complexity | `constantCost` | Examples |
|---|---|---|
| Simple parameter swap | `15min` | Switching to parameterized query |
| Add validation layer | `30min` | Input sanitization, URL allowlisting |
| Architectural change | `2h` | Redesigning auth flow, adding CSRF framework |
| Crypto/protocol upgrade | `4h` | Replacing deprecated algorithms, TLS configuration |

## Severity Decision Matrix

| Exploitability | Data Impact | Severity |
|---|---|---|
| Remotely exploitable, no auth required | Data breach / RCE | `BLOCKER` |
| Requires authenticated access | Data leak / privilege escalation | `CRITICAL` |
| Requires specific conditions / chaining | Limited information exposure | `MAJOR` |

## Common Tags for Security Rules

`security`, `owasp-top-10`, `cwe`, `injection`, `authentication`, `authorization`, `cryptography`, `xss`, `csrf`, `ssrf`, `deserialization`, `input-validation`, `configuration`, `sensitive-data`, `access-control`

## Key Principles

- Always assume user input is hostile — rules should flag any path where untrusted data reaches a sensitive sink without sanitization.
- Prefer allowlisting over denylisting in remediation advice.
- Reference defense-in-depth: multiple layers of validation are better than one.
- Never recommend security-through-obscurity as a remediation.
- Avoid false sense of security — if a fix is partial, note the remaining risk.
