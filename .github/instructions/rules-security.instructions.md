---
applyTo: "rules/security/**"
---

# Security Rules — Custom Instructions

You are assisting with SonarQube **security vulnerability** rule definitions in `rules/security/`.

## Category Context

Security rules detect exploitable vulnerabilities that could be leveraged by attackers to compromise confidentiality, integrity, or availability. These rules carry the highest organizational risk and demand precision in description, severity assignment, and remediation guidance.

## Constraints for This Category

- **`type` MUST be `VULNERABILITY`** — every rule in this directory represents an exploitable security weakness, never a code smell or bug.
- **`severity` is typically `CRITICAL` or `BLOCKER`** — only use `MAJOR` if the issue requires unusual preconditions to exploit. Never use `MINOR` or `INFO` for security rules.
- **`impacts[].softwareQuality` MUST include `SECURITY`** with severity `HIGH` — this is non-negotiable for vulnerability rules.
- **`tags` MUST include `"security"`** — additionally tag with relevant frameworks/standards:
  - `owasp-top-10` — for OWASP Top 10 mapped issues
  - `cwe` — when a specific CWE ID applies
  - `sans-top-25` — for SANS/CWE Top 25 entries
  - `injection`, `authentication`, `cryptography`, `access-control` — as applicable

## Writing Descriptions

Security rule descriptions must clearly articulate:
1. **What** the vulnerable pattern is (e.g., "user input concatenated directly into SQL queries")
2. **How** an attacker exploits it (e.g., "an attacker can inject arbitrary SQL commands")
3. **Impact** of successful exploitation (e.g., "full database compromise, data exfiltration, or deletion")
4. **Scope** — which languages/frameworks are affected when relevant

Avoid vague descriptions. Be specific about the attack vector and its consequences.

## Remediation Examples

For security rules, remediation examples must:
- Show a **realistic vulnerable pattern** in the `before` field — not toy code
- Show the **correct secure fix** in the `after` field — using parameterized queries, encoding functions, validated inputs, or framework-provided safeguards
- Prefer **framework-native solutions** over manual sanitization (e.g., use PreparedStatement, not regex filtering)
- Include language/framework context where the fix differs across ecosystems

## Remediation Cost Guidelines

| Fix Complexity | `constantCost` | Example |
|---|---|---|
| Drop-in API change | `15min` | Replace `Math.random()` with `SecureRandom` |
| Query parameterization | `30min` | Convert string concat SQL to PreparedStatement |
| Input validation layer | `1h` | Add validation/sanitization at entry points |
| Architecture change | `4h` | Implement CSRF token framework, redesign auth flow |

## Common Tags for Security Rules

`security`, `owasp-top-10`, `injection`, `xss`, `authentication`, `authorization`, `cryptography`, `session-management`, `input-validation`, `data-exposure`, `configuration`, `deserialization`, `access-control`, `cwe`

## When Creating New Security Rules

1. Verify the vulnerability isn't already covered by an existing rule (check all 28 files in this directory).
2. Reference the relevant CWE ID and OWASP category in the description when applicable.
3. Ensure the `key` is specific enough to distinguish from related vulnerabilities (e.g., `sql-injection` vs `ldap-injection` vs `command-injection`).
4. Set `debt.function` to `CONSTANT_ISSUE` unless the fix effort scales with the number of occurrences.
5. Consider whether a `params` array is needed (e.g., a list of safe wrapper functions to exclude from detection).

## Quality Checklist

- [ ] `type` is `VULNERABILITY`
- [ ] `severity` and `defaultSeverity` are `CRITICAL` or `BLOCKER`
- [ ] `impacts` includes `{ "softwareQuality": "SECURITY", "severity": "HIGH" }`
- [ ] `tags` includes `"security"` plus at least one specific tag
- [ ] Description explains what, how, and impact
- [ ] Remediation example shows real-world before/after
- [ ] Filename matches `key` field in lower-kebab-case
