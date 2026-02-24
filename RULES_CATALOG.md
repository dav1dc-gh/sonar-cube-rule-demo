# SonarQube Rules Catalog

> Auto-generated on 2026-02-24 by `scripts/generate-catalog.js`.  
> **52 rules** across 4 categories.

## Summary

| Category | Rules | Blocker | Critical | Major | Minor | Info |
|----------|------:|--------:|---------:|------:|------:|-----:|
| **security** | 15 | 4 | 9 | 2 | 0 | 0 |
| **code-smells** | 13 | 0 | 0 | 5 | 8 | 0 |
| **performance** | 12 | 0 | 5 | 5 | 2 | 0 |
| **maintainability** | 12 | 0 | 0 | 7 | 5 | 0 |
| **TOTAL** | **52** | **4** | **14** | **19** | **15** | **0** |

## All Rules

| # | Key | Name | Severity | Type | Tags | Params | Status |
|--:|-----|------|----------|------|------|-------:|--------|
| 1 | [`command-injection`](rules/security/command-injection.json) | Command Injection Vulnerability | 🟠 CRITICAL | VULNERABILITY | `security` `injection` `owasp-top-10` `command-execution` | 0 | READY |
| 2 | [`csrf-vulnerability`](rules/security/csrf-vulnerability.json) | Cross-Site Request Forgery (CSRF) | 🟡 MAJOR | VULNERABILITY | `security` `csrf` `owasp-top-10` `web` | 0 | READY |
| 3 | [`hardcoded-credentials`](rules/security/hardcoded-credentials.json) | Hardcoded Credentials Detection | 🔴 BLOCKER | VULNERABILITY | `security` `credentials` `secrets` `owasp-top-10` | 0 | READY |
| 4 | [`insecure-cookie`](rules/security/insecure-cookie.json) | Insecure Cookie Configuration | 🟠 CRITICAL | VULNERABILITY | `security` `owasp-top-10` `cookies` `session-management` | 0 | READY |
| 5 | [`insecure-deserialization`](rules/security/insecure-deserialization.json) | Insecure Deserialization | 🟠 CRITICAL | VULNERABILITY | `security` `deserialization` `owasp-top-10` `rce` | 0 | READY |
| 6 | [`insecure-random`](rules/security/insecure-random.json) | Insecure Random Number Generator | 🟡 MAJOR | VULNERABILITY | `security` `random` `cryptography` `tokens` | 0 | READY |
| 7 | [`ldap-injection`](rules/security/ldap-injection.json) | LDAP Injection Vulnerability | 🔴 BLOCKER | VULNERABILITY | `security` `owasp-top-10` `injection` `ldap` `authentication` | 0 | READY |
| 8 | [`open-redirect`](rules/security/open-redirect.json) | Open Redirect Vulnerability | 🟠 CRITICAL | VULNERABILITY | `security` `owasp-top-10` `redirect` `phishing` | 0 | READY |
| 9 | [`path-traversal`](rules/security/path-traversal.json) | Path Traversal Vulnerability | 🟠 CRITICAL | VULNERABILITY | `security` `path-traversal` `owasp-top-10` `file-access` | 0 | READY |
| 10 | [`sensitive-data-exposure`](rules/security/sensitive-data-exposure.json) | Sensitive Data Exposure in Logs | 🟠 CRITICAL | VULNERABILITY | `security` `logging` `pii` `gdpr` `owasp-top-10` | 0 | READY |
| 11 | [`server-side-request-forgery`](rules/security/server-side-request-forgery.json) | Server-Side Request Forgery (SSRF) | 🔴 BLOCKER | VULNERABILITY | `security` `owasp-top-10` `ssrf` `network` | 0 | READY |
| 12 | [`sql-injection`](rules/security/sql-injection.json) | SQL Injection Prevention | 🟠 CRITICAL | VULNERABILITY | `security` `sql` `injection` `owasp-top-10` | 0 | READY |
| 13 | [`weak-cryptography`](rules/security/weak-cryptography.json) | Weak Cryptographic Algorithm | 🟠 CRITICAL | VULNERABILITY | `security` `cryptography` `encryption` `owasp-top-10` | 0 | READY |
| 14 | [`xml-external-entity`](rules/security/xml-external-entity.json) | XML External Entity (XXE) Injection | 🔴 BLOCKER | VULNERABILITY | `security` `owasp-top-10` `injection` `xxe` `xml` | 0 | READY |
| 15 | [`xss-vulnerability`](rules/security/xss-vulnerability.json) | Cross-Site Scripting (XSS) Prevention | 🟠 CRITICAL | VULNERABILITY | `security` `xss` `cross-site-scripting` `owasp-top-10` | 0 | READY |
| 16 | [`complex-methods`](rules/code-smells/complex-methods.json) | High Cyclomatic Complexity | 🟡 MAJOR | CODE_SMELL | `code-smell` `complexity` `maintainability` `testing` | 1 | READY |
| 17 | [`data-clumps`](rules/code-smells/data-clumps.json) | Data Clumps | 🔵 MINOR | CODE_SMELL | `code-smell` `design` `refactoring` `cohesion` | 0 | READY |
| 18 | [`dead-code`](rules/code-smells/dead-code.json) | Dead Code Detection | 🔵 MINOR | CODE_SMELL | `code-smell` `unused` `cleanup` `maintainability` | 0 | READY |
| 19 | [`duplicate-code`](rules/code-smells/duplicate-code.json) | Duplicate Code Blocks | 🟡 MAJOR | CODE_SMELL | `code-smell` `duplication` `maintainability` `dry-principle` | 0 | READY |
| 20 | [`empty-catch-block`](rules/code-smells/empty-catch-block.json) | Empty Catch Block | 🟡 MAJOR | CODE_SMELL | `code-smell` `error-handling` `exceptions` `debugging` | 0 | READY |
| 21 | [`feature-envy`](rules/code-smells/feature-envy.json) | Feature Envy | 🔵 MINOR | CODE_SMELL | `code-smell` `design` `refactoring` `oop` | 0 | READY |
| 22 | [`god-class`](rules/code-smells/god-class.json) | God Class Detection | 🟡 MAJOR | CODE_SMELL | `code-smell` `design` `solid` `maintainability` | 2 | READY |
| 23 | [`long-parameter-list`](rules/code-smells/long-parameter-list.json) | Long Parameter List | 🔵 MINOR | CODE_SMELL | `code-smell` `design` `refactoring` `readability` | 1 | READY |
| 24 | [`magic-numbers`](rules/code-smells/magic-numbers.json) | Avoid Magic Numbers | 🔵 MINOR | CODE_SMELL | `code-smell` `readability` `maintainability` | 0 | READY |
| 25 | [`message-chains`](rules/code-smells/message-chains.json) | Message Chains (Law of Demeter Violation) | 🔵 MINOR | CODE_SMELL | `code-smell` `design` `coupling` `law-of-demeter` | 1 | READY |
| 26 | [`primitive-obsession`](rules/code-smells/primitive-obsession.json) | Primitive Obsession | 🔵 MINOR | CODE_SMELL | `code-smell` `design` `domain-driven-design` `refactoring` | 0 | READY |
| 27 | [`refused-bequest`](rules/code-smells/refused-bequest.json) | Refused Bequest | 🟡 MAJOR | CODE_SMELL | `code-smell` `design` `solid` `inheritance` `lsp` | 0 | READY |
| 28 | [`speculative-generality`](rules/code-smells/speculative-generality.json) | Speculative Generality | 🔵 MINOR | CODE_SMELL | `code-smell` `design` `yagni` `refactoring` | 0 | READY |
| 29 | [`connection-pool-exhaustion`](rules/performance/connection-pool-exhaustion.json) | Connection Pool Exhaustion Risk | 🟠 CRITICAL | BUG | `performance` `database` `resource-leak` `connection-pool` | 0 | READY |
| 30 | [`excessive-object-creation`](rules/performance/excessive-object-creation.json) | Excessive Object Creation in Hot Path | 🟡 MAJOR | CODE_SMELL | `performance` `memory` `gc` `optimization` | 0 | READY |
| 31 | [`inefficient-collection-usage`](rules/performance/inefficient-collection-usage.json) | Inefficient Collection Usage | 🔵 MINOR | CODE_SMELL | `performance` `collections` `data-structures` `optimization` | 0 | READY |
| 32 | [`inefficient-loops`](rules/performance/inefficient-loops.json) | Inefficient Loop Operations | 🟡 MAJOR | CODE_SMELL | `performance` `optimization` `loops` | 0 | READY |
| 33 | [`memory-leaks`](rules/performance/memory-leaks.json) | Potential Memory Leak Detection | 🟠 CRITICAL | BUG | `performance` `memory` `resource-management` | 0 | READY |
| 34 | [`missing-lazy-initialization`](rules/performance/missing-lazy-initialization.json) | Missing Lazy Initialization | 🟡 MAJOR | CODE_SMELL | `performance` `memory` `initialization` `optimization` | 0 | READY |
| 35 | [`n-plus-one-query`](rules/performance/n-plus-one-query.json) | N+1 Query Problem | 🟠 CRITICAL | CODE_SMELL | `performance` `database` `orm` `optimization` | 0 | READY |
| 36 | [`string-concatenation-in-loop`](rules/performance/string-concatenation-in-loop.json) | String Concatenation in Loop | 🟡 MAJOR | CODE_SMELL | `performance` `memory` `strings` `optimization` | 0 | READY |
| 37 | [`synchronous-io-in-async`](rules/performance/synchronous-io-in-async.json) | Synchronous I/O in Async Context | 🟡 MAJOR | CODE_SMELL | `performance` `async` `reactive` `concurrency` | 0 | READY |
| 38 | [`unbounded-collection-growth`](rules/performance/unbounded-collection-growth.json) | Unbounded Collection Growth | 🟠 CRITICAL | BUG | `performance` `memory` `memory-leak` `cache` | 0 | READY |
| 39 | [`unnecessary-boxing`](rules/performance/unnecessary-boxing.json) | Unnecessary Boxing/Unboxing | 🔵 MINOR | CODE_SMELL | `performance` `memory` `primitives` `optimization` | 0 | READY |
| 40 | [`unoptimized-regex`](rules/performance/unoptimized-regex.json) | Unoptimized Regular Expression | 🟠 CRITICAL | BUG | `performance` `regex` `redos` `security` | 0 | READY |
| 41 | [`boolean-blindness`](rules/maintainability/boolean-blindness.json) | Boolean Blindness | 🔵 MINOR | CODE_SMELL | `maintainability` `readability` `api-design` `clean-code` | 1 | READY |
| 42 | [`circular-dependencies`](rules/maintainability/circular-dependencies.json) | Circular Dependencies Between Modules | 🟡 MAJOR | CODE_SMELL | `maintainability` `design` `architecture` `coupling` | 0 | READY |
| 43 | [`deep-nesting`](rules/maintainability/deep-nesting.json) | Deeply Nested Code | 🟡 MAJOR | CODE_SMELL | `maintainability` `complexity` `readability` `refactoring` | 1 | READY |
| 44 | [`excessive-comments`](rules/maintainability/excessive-comments.json) | Excessive or Redundant Comments | 🔵 MINOR | CODE_SMELL | `maintainability` `documentation` `readability` `clean-code` | 0 | READY |
| 45 | [`hardcoded-urls`](rules/maintainability/hardcoded-urls.json) | Hardcoded URLs and Endpoints | 🔵 MINOR | CODE_SMELL | `maintainability` `configuration` `deployment` `best-practices` | 0 | READY |
| 46 | [`hidden-dependencies`](rules/maintainability/hidden-dependencies.json) | Hidden Dependencies | 🟡 MAJOR | CODE_SMELL | `maintainability` `design` `testability` `dependency-injection` | 0 | READY |
| 47 | [`inconsistent-naming`](rules/maintainability/inconsistent-naming.json) | Inconsistent Naming Convention | 🔵 MINOR | CODE_SMELL | `maintainability` `naming` `conventions` `readability` | 0 | READY |
| 48 | [`long-methods`](rules/maintainability/long-methods.json) | Method Length Limit | 🟡 MAJOR | CODE_SMELL | `maintainability` `readability` `method-length` | 1 | READY |
| 49 | [`missing-javadoc`](rules/maintainability/missing-javadoc.json) | Missing Documentation | 🔵 MINOR | CODE_SMELL | `maintainability` `documentation` `javadoc` `readability` | 0 | READY |
| 50 | [`missing-null-check`](rules/maintainability/missing-null-check.json) | Missing Null Check | 🟡 MAJOR | BUG | `maintainability` `null-safety` `defensive-programming` `reliability` | 0 | READY |
| 51 | [`shotgun-surgery`](rules/maintainability/shotgun-surgery.json) | Shotgun Surgery | 🟡 MAJOR | CODE_SMELL | `maintainability` `design` `cohesion` `refactoring` | 0 | READY |
| 52 | [`too-many-parameters`](rules/maintainability/too-many-parameters.json) | Too Many Method Parameters | 🟡 MAJOR | CODE_SMELL | `maintainability` `readability` `parameters` `design` | 1 | READY |

## Security (15 rules)

### Command Injection Vulnerability

- **Key:** `command-injection`
- **File:** [`rules/security/command-injection.json`](rules/security/command-injection.json)
- **Severity:** 🟠 CRITICAL
- **Type:** VULNERABILITY
- **Tags:** `security`, `injection`, `owasp-top-10`, `command-execution`
- **Remediation cost:** 30min
- **Debt:** CONSTANT_ISSUE (offset: 30min)
- **Impacts:** SECURITY: HIGH

> Detects potential OS command injection vulnerabilities where user input is passed to system commands without proper sanitization.

### Cross-Site Request Forgery (CSRF)

- **Key:** `csrf-vulnerability`
- **File:** [`rules/security/csrf-vulnerability.json`](rules/security/csrf-vulnerability.json)
- **Severity:** 🟡 MAJOR
- **Type:** VULNERABILITY
- **Tags:** `security`, `csrf`, `owasp-top-10`, `web`
- **Remediation cost:** 30min
- **Debt:** CONSTANT_ISSUE (offset: 30min)
- **Impacts:** SECURITY: MEDIUM

> Detects missing CSRF protection on state-changing operations, which could allow attackers to trick users into performing unintended actions.

### Hardcoded Credentials Detection

- **Key:** `hardcoded-credentials`
- **File:** [`rules/security/hardcoded-credentials.json`](rules/security/hardcoded-credentials.json)
- **Severity:** 🔴 BLOCKER
- **Type:** VULNERABILITY
- **Tags:** `security`, `credentials`, `secrets`, `owasp-top-10`
- **Remediation cost:** 15min
- **Debt:** CONSTANT_ISSUE (offset: 15min)
- **Impacts:** SECURITY: HIGH

> Detects hardcoded passwords, API keys, tokens, or other sensitive credentials in source code, which poses a significant security risk.

### Insecure Cookie Configuration

- **Key:** `insecure-cookie`
- **File:** [`rules/security/insecure-cookie.json`](rules/security/insecure-cookie.json)
- **Severity:** 🟠 CRITICAL
- **Type:** VULNERABILITY
- **Tags:** `security`, `owasp-top-10`, `cookies`, `session-management`
- **Remediation cost:** 15min
- **Debt:** CONSTANT_ISSUE (offset: 15min)
- **Impacts:** SECURITY: HIGH

> Detects cookies created without essential security flags (Secure, HttpOnly, SameSite). Missing Secure flag allows cookies to be transmitted over unencrypted connections. Missing HttpOnly flag exposes cookies to XSS attacks. Missing SameSite flag enables CSRF attacks.

### Insecure Deserialization

- **Key:** `insecure-deserialization`
- **File:** [`rules/security/insecure-deserialization.json`](rules/security/insecure-deserialization.json)
- **Severity:** 🟠 CRITICAL
- **Type:** VULNERABILITY
- **Tags:** `security`, `deserialization`, `owasp-top-10`, `rce`
- **Remediation cost:** 45min
- **Debt:** CONSTANT_ISSUE (offset: 45min)
- **Impacts:** SECURITY: HIGH

> Detects unsafe deserialization of untrusted data which can lead to remote code execution, denial of service, or other attacks.

### Insecure Random Number Generator

- **Key:** `insecure-random`
- **File:** [`rules/security/insecure-random.json`](rules/security/insecure-random.json)
- **Severity:** 🟡 MAJOR
- **Type:** VULNERABILITY
- **Tags:** `security`, `random`, `cryptography`, `tokens`
- **Remediation cost:** 10min
- **Debt:** CONSTANT_ISSUE (offset: 10min)
- **Impacts:** SECURITY: MEDIUM

> Detects usage of predictable random number generators (like java.util.Random) for security-sensitive operations such as token generation or cryptographic purposes.

### LDAP Injection Vulnerability

- **Key:** `ldap-injection`
- **File:** [`rules/security/ldap-injection.json`](rules/security/ldap-injection.json)
- **Severity:** 🔴 BLOCKER
- **Type:** VULNERABILITY
- **Tags:** `security`, `owasp-top-10`, `injection`, `ldap`, `authentication`
- **Remediation cost:** 45min
- **Debt:** CONSTANT_ISSUE (offset: 45min)
- **Impacts:** SECURITY: HIGH

> Detects when user input is concatenated directly into LDAP queries without proper sanitization. Attackers can manipulate LDAP queries to bypass authentication, access unauthorized data, or modify directory entries. Always use parameterized LDAP queries or properly escape user input.

### Open Redirect Vulnerability

- **Key:** `open-redirect`
- **File:** [`rules/security/open-redirect.json`](rules/security/open-redirect.json)
- **Severity:** 🟠 CRITICAL
- **Type:** VULNERABILITY
- **Tags:** `security`, `owasp-top-10`, `redirect`, `phishing`
- **Remediation cost:** 30min
- **Debt:** CONSTANT_ISSUE (offset: 30min)
- **Impacts:** SECURITY: HIGH

> Detects when user-controlled input is used to construct redirect URLs without proper validation. Open redirects can be exploited by attackers to redirect users to malicious websites, facilitating phishing attacks and credential theft. Always validate and whitelist redirect destinations.

### Path Traversal Vulnerability

- **Key:** `path-traversal`
- **File:** [`rules/security/path-traversal.json`](rules/security/path-traversal.json)
- **Severity:** 🟠 CRITICAL
- **Type:** VULNERABILITY
- **Tags:** `security`, `path-traversal`, `owasp-top-10`, `file-access`
- **Remediation cost:** 30min
- **Debt:** CONSTANT_ISSUE (offset: 30min)
- **Impacts:** SECURITY: HIGH

> Detects potential path traversal vulnerabilities where user input is used to construct file paths without proper validation, allowing attackers to access files outside the intended directory.

### Sensitive Data Exposure in Logs

- **Key:** `sensitive-data-exposure`
- **File:** [`rules/security/sensitive-data-exposure.json`](rules/security/sensitive-data-exposure.json)
- **Severity:** 🟠 CRITICAL
- **Type:** VULNERABILITY
- **Tags:** `security`, `logging`, `pii`, `gdpr`, `owasp-top-10`
- **Remediation cost:** 15min
- **Debt:** CONSTANT_ISSUE (offset: 15min)
- **Impacts:** SECURITY: HIGH

> Detects logging of sensitive information such as passwords, credit card numbers, social security numbers, or personal identifiable information (PII).

### Server-Side Request Forgery (SSRF)

- **Key:** `server-side-request-forgery`
- **File:** [`rules/security/server-side-request-forgery.json`](rules/security/server-side-request-forgery.json)
- **Severity:** 🔴 BLOCKER
- **Type:** VULNERABILITY
- **Tags:** `security`, `owasp-top-10`, `ssrf`, `network`
- **Remediation cost:** 45min
- **Debt:** CONSTANT_ISSUE (offset: 45min)
- **Impacts:** SECURITY: HIGH

> Detects when user-controlled URLs are used to make server-side HTTP requests without validation. SSRF allows attackers to make requests to internal services, cloud metadata endpoints, or other protected resources. Always validate and whitelist allowed destinations.

### SQL Injection Prevention

- **Key:** `sql-injection`
- **File:** [`rules/security/sql-injection.json`](rules/security/sql-injection.json)
- **Severity:** 🟠 CRITICAL
- **Type:** VULNERABILITY
- **Tags:** `security`, `sql`, `injection`, `owasp-top-10`
- **Remediation cost:** 30min
- **Debt:** CONSTANT_ISSUE (offset: 30min)
- **Impacts:** SECURITY: HIGH

> Detects potential SQL injection vulnerabilities where user input is directly concatenated into SQL queries without proper sanitization or parameterization.

### Weak Cryptographic Algorithm

- **Key:** `weak-cryptography`
- **File:** [`rules/security/weak-cryptography.json`](rules/security/weak-cryptography.json)
- **Severity:** 🟠 CRITICAL
- **Type:** VULNERABILITY
- **Tags:** `security`, `cryptography`, `encryption`, `owasp-top-10`
- **Remediation cost:** 20min
- **Debt:** CONSTANT_ISSUE (offset: 20min)
- **Impacts:** SECURITY: HIGH

> Detects usage of weak or deprecated cryptographic algorithms such as MD5, SHA1, DES, or RC4 that are vulnerable to attacks.

### XML External Entity (XXE) Injection

- **Key:** `xml-external-entity`
- **File:** [`rules/security/xml-external-entity.json`](rules/security/xml-external-entity.json)
- **Severity:** 🔴 BLOCKER
- **Type:** VULNERABILITY
- **Tags:** `security`, `owasp-top-10`, `injection`, `xxe`, `xml`
- **Remediation cost:** 20min
- **Debt:** CONSTANT_ISSUE (offset: 20min)
- **Impacts:** SECURITY: HIGH

> Detects XML parsers configured to process external entities, which can lead to XXE attacks. Attackers can exploit this to read local files, perform server-side request forgery, or cause denial of service. Always disable external entity processing in XML parsers.

### Cross-Site Scripting (XSS) Prevention

- **Key:** `xss-vulnerability`
- **File:** [`rules/security/xss-vulnerability.json`](rules/security/xss-vulnerability.json)
- **Severity:** 🟠 CRITICAL
- **Type:** VULNERABILITY
- **Tags:** `security`, `xss`, `cross-site-scripting`, `owasp-top-10`
- **Remediation cost:** 20min
- **Debt:** CONSTANT_ISSUE (offset: 20min)
- **Impacts:** SECURITY: HIGH

> Identifies potential XSS vulnerabilities where user-supplied data is rendered in HTML without proper encoding or sanitization.

## Code-smells (13 rules)

### High Cyclomatic Complexity

- **Key:** `complex-methods`
- **File:** [`rules/code-smells/complex-methods.json`](rules/code-smells/complex-methods.json)
- **Severity:** 🟡 MAJOR
- **Type:** CODE_SMELL
- **Tags:** `code-smell`, `complexity`, `maintainability`, `testing`
- **Remediation cost:** 30min
- **Debt:** LINEAR (offset: 0min) (coefficient: 1min)
- **Impacts:** MAINTAINABILITY: MEDIUM
- **Parameters:**
  - `threshold` (INTEGER) — Maximum allowed cyclomatic complexity *(default: 15)*

> Detects methods or functions with high cyclomatic complexity (too many decision points), making them difficult to understand, test, and maintain.

### Data Clumps

- **Key:** `data-clumps`
- **File:** [`rules/code-smells/data-clumps.json`](rules/code-smells/data-clumps.json)
- **Severity:** 🔵 MINOR
- **Type:** CODE_SMELL
- **Tags:** `code-smell`, `design`, `refactoring`, `cohesion`
- **Remediation cost:** 30min
- **Debt:** CONSTANT_ISSUE (offset: 30min)
- **Impacts:** MAINTAINABILITY: LOW

> Detects groups of variables that frequently appear together across multiple methods or classes. Data clumps often indicate a missing class or struct that should encapsulate these related values. Extract data clumps into dedicated classes to improve cohesion and reduce duplication.

### Dead Code Detection

- **Key:** `dead-code`
- **File:** [`rules/code-smells/dead-code.json`](rules/code-smells/dead-code.json)
- **Severity:** 🔵 MINOR
- **Type:** CODE_SMELL
- **Tags:** `code-smell`, `unused`, `cleanup`, `maintainability`
- **Remediation cost:** 5min
- **Debt:** CONSTANT_ISSUE (offset: 5min)
- **Impacts:** MAINTAINABILITY: LOW

> Detects unreachable code, unused variables, methods, or classes that serve no purpose and should be removed to improve code clarity.

### Duplicate Code Blocks

- **Key:** `duplicate-code`
- **File:** [`rules/code-smells/duplicate-code.json`](rules/code-smells/duplicate-code.json)
- **Severity:** 🟡 MAJOR
- **Type:** CODE_SMELL
- **Tags:** `code-smell`, `duplication`, `maintainability`, `dry-principle`
- **Remediation cost:** 15min
- **Debt:** CONSTANT_ISSUE (offset: 15min)
- **Impacts:** MAINTAINABILITY: MEDIUM

> Identifies duplicate or nearly identical code blocks that should be refactored into reusable functions or methods to improve maintainability and reduce technical debt.

### Empty Catch Block

- **Key:** `empty-catch-block`
- **File:** [`rules/code-smells/empty-catch-block.json`](rules/code-smells/empty-catch-block.json)
- **Severity:** 🟡 MAJOR
- **Type:** CODE_SMELL
- **Tags:** `code-smell`, `error-handling`, `exceptions`, `debugging`
- **Remediation cost:** 10min
- **Debt:** CONSTANT_ISSUE (offset: 10min)
- **Impacts:** RELIABILITY: MEDIUM

> Detects empty catch blocks that silently swallow exceptions, hiding potential errors and making debugging difficult.

### Feature Envy

- **Key:** `feature-envy`
- **File:** [`rules/code-smells/feature-envy.json`](rules/code-smells/feature-envy.json)
- **Severity:** 🔵 MINOR
- **Type:** CODE_SMELL
- **Tags:** `code-smell`, `design`, `refactoring`, `oop`
- **Remediation cost:** 20min
- **Debt:** CONSTANT_ISSUE (offset: 20min)
- **Impacts:** MAINTAINABILITY: LOW

> Detects methods that use more features from other classes than from their own class, indicating the method may be misplaced.

### God Class Detection

- **Key:** `god-class`
- **File:** [`rules/code-smells/god-class.json`](rules/code-smells/god-class.json)
- **Severity:** 🟡 MAJOR
- **Type:** CODE_SMELL
- **Tags:** `code-smell`, `design`, `solid`, `maintainability`
- **Remediation cost:** 4h
- **Debt:** LINEAR (offset: 0min) (coefficient: 10min)
- **Impacts:** MAINTAINABILITY: HIGH
- **Parameters:**
  - `maxLines` (INTEGER) — Maximum number of lines allowed in a class *(default: 500)*
  - `maxMethods` (INTEGER) — Maximum number of methods allowed in a class *(default: 20)*

> Detects classes that have grown too large and handle too many responsibilities, violating the Single Responsibility Principle and making the code difficult to understand and maintain.

### Long Parameter List

- **Key:** `long-parameter-list`
- **File:** [`rules/code-smells/long-parameter-list.json`](rules/code-smells/long-parameter-list.json)
- **Severity:** 🔵 MINOR
- **Type:** CODE_SMELL
- **Tags:** `code-smell`, `design`, `refactoring`, `readability`
- **Remediation cost:** 30min
- **Debt:** CONSTANT_ISSUE (offset: 30min)
- **Impacts:** MAINTAINABILITY: LOW
- **Parameters:**
  - `maxParams` (INTEGER) — Maximum number of parameters allowed *(default: 5)*

> Detects methods with too many parameters, which makes them difficult to understand, call correctly, and maintain. Consider using parameter objects or builder patterns.

### Avoid Magic Numbers

- **Key:** `magic-numbers`
- **File:** [`rules/code-smells/magic-numbers.json`](rules/code-smells/magic-numbers.json)
- **Severity:** 🔵 MINOR
- **Type:** CODE_SMELL
- **Tags:** `code-smell`, `readability`, `maintainability`
- **Remediation cost:** 5min
- **Debt:** CONSTANT_ISSUE (offset: 5min)
- **Impacts:** MAINTAINABILITY: LOW

> Detects the use of magic numbers (unnamed numerical constants) in code, which reduces readability and maintainability. Numbers should be replaced with named constants.

### Message Chains (Law of Demeter Violation)

- **Key:** `message-chains`
- **File:** [`rules/code-smells/message-chains.json`](rules/code-smells/message-chains.json)
- **Severity:** 🔵 MINOR
- **Type:** CODE_SMELL
- **Tags:** `code-smell`, `design`, `coupling`, `law-of-demeter`
- **Remediation cost:** 20min
- **Debt:** CONSTANT_ISSUE (offset: 20min)
- **Impacts:** MAINTAINABILITY: LOW
- **Parameters:**
  - `maxChainLength` (INTEGER) — Maximum allowed method chain length before triggering the rule *(default: 3)*

> Detects long chains of method calls like a.getB().getC().getD().doSomething(). Message chains violate the Law of Demeter, creating tight coupling between classes and making code fragile to changes in intermediate objects. Use delegation or provide direct methods.

### Primitive Obsession

- **Key:** `primitive-obsession`
- **File:** [`rules/code-smells/primitive-obsession.json`](rules/code-smells/primitive-obsession.json)
- **Severity:** 🔵 MINOR
- **Type:** CODE_SMELL
- **Tags:** `code-smell`, `design`, `domain-driven-design`, `refactoring`
- **Remediation cost:** 30min
- **Debt:** CONSTANT_ISSUE (offset: 30min)
- **Impacts:** MAINTAINABILITY: MEDIUM

> Detects overuse of primitive types instead of small objects for domain concepts. Using primitives for values like money, phone numbers, or email addresses leads to scattered validation logic, reduced type safety, and harder-to-understand code. Wrap primitives in value objects.

### Refused Bequest

- **Key:** `refused-bequest`
- **File:** [`rules/code-smells/refused-bequest.json`](rules/code-smells/refused-bequest.json)
- **Severity:** 🟡 MAJOR
- **Type:** CODE_SMELL
- **Tags:** `code-smell`, `design`, `solid`, `inheritance`, `lsp`
- **Remediation cost:** 45min
- **Debt:** CONSTANT_ISSUE (offset: 45min)
- **Impacts:** MAINTAINABILITY: MEDIUM

> Detects subclasses that override inherited methods to do nothing or throw exceptions, or don't use most inherited functionality. This indicates improper use of inheritance and violates the Liskov Substitution Principle. Consider using composition instead of inheritance.

### Speculative Generality

- **Key:** `speculative-generality`
- **File:** [`rules/code-smells/speculative-generality.json`](rules/code-smells/speculative-generality.json)
- **Severity:** 🔵 MINOR
- **Type:** CODE_SMELL
- **Tags:** `code-smell`, `design`, `yagni`, `refactoring`
- **Remediation cost:** 20min
- **Debt:** CONSTANT_ISSUE (offset: 20min)
- **Impacts:** MAINTAINABILITY: LOW

> Detects unused abstractions, interfaces, or parameters created for hypothetical future requirements. This includes abstract classes with only one subclass, interfaces implemented by only one class, and unused method parameters. Remove unnecessary abstractions and add them when actually needed.

## Performance (12 rules)

### Connection Pool Exhaustion Risk

- **Key:** `connection-pool-exhaustion`
- **File:** [`rules/performance/connection-pool-exhaustion.json`](rules/performance/connection-pool-exhaustion.json)
- **Severity:** 🟠 CRITICAL
- **Type:** BUG
- **Tags:** `performance`, `database`, `resource-leak`, `connection-pool`
- **Remediation cost:** 20min
- **Debt:** CONSTANT_ISSUE (offset: 20min)
- **Impacts:** RELIABILITY: HIGH

> Detects database or HTTP connections that are not properly closed or returned to the pool. Leaked connections exhaust the pool, causing application hangs and failures under load. Always close connections in finally blocks or use try-with-resources.

### Excessive Object Creation in Hot Path

- **Key:** `excessive-object-creation`
- **File:** [`rules/performance/excessive-object-creation.json`](rules/performance/excessive-object-creation.json)
- **Severity:** 🟡 MAJOR
- **Type:** CODE_SMELL
- **Tags:** `performance`, `memory`, `gc`, `optimization`
- **Remediation cost:** 30min
- **Debt:** CONSTANT_ISSUE (offset: 30min)
- **Impacts:** RELIABILITY: MEDIUM

> Detects unnecessary object allocation in frequently executed code paths such as loops or high-traffic methods. Excessive object creation increases garbage collection pressure and degrades performance. Reuse objects, use object pools, or prefer primitive types where possible.

### Inefficient Collection Usage

- **Key:** `inefficient-collection-usage`
- **File:** [`rules/performance/inefficient-collection-usage.json`](rules/performance/inefficient-collection-usage.json)
- **Severity:** 🔵 MINOR
- **Type:** CODE_SMELL
- **Tags:** `performance`, `collections`, `data-structures`, `optimization`
- **Remediation cost:** 10min
- **Debt:** CONSTANT_ISSUE (offset: 10min)
- **Impacts:** MAINTAINABILITY: LOW

> Detects improper use of collections such as using LinkedList for random access, ArrayList for frequent insertions, or not specifying initial capacity for large collections.

### Inefficient Loop Operations

- **Key:** `inefficient-loops`
- **File:** [`rules/performance/inefficient-loops.json`](rules/performance/inefficient-loops.json)
- **Severity:** 🟡 MAJOR
- **Type:** CODE_SMELL
- **Tags:** `performance`, `optimization`, `loops`
- **Remediation cost:** 10min
- **Debt:** CONSTANT_ISSUE (offset: 10min)
- **Impacts:** MAINTAINABILITY: MEDIUM

> Identifies performance issues in loops such as repeated method calls, unnecessary object creation, or operations that should be moved outside the loop.

### Potential Memory Leak Detection

- **Key:** `memory-leaks`
- **File:** [`rules/performance/memory-leaks.json`](rules/performance/memory-leaks.json)
- **Severity:** 🟠 CRITICAL
- **Type:** BUG
- **Tags:** `performance`, `memory`, `resource-management`
- **Remediation cost:** 20min
- **Debt:** CONSTANT_ISSUE (offset: 20min)
- **Impacts:** RELIABILITY: HIGH

> Identifies patterns that may lead to memory leaks such as unclosed resources, event listener accumulation, or references that prevent garbage collection.

### Missing Lazy Initialization

- **Key:** `missing-lazy-initialization`
- **File:** [`rules/performance/missing-lazy-initialization.json`](rules/performance/missing-lazy-initialization.json)
- **Severity:** 🟡 MAJOR
- **Type:** CODE_SMELL
- **Tags:** `performance`, `memory`, `initialization`, `optimization`
- **Remediation cost:** 20min
- **Debt:** CONSTANT_ISSUE (offset: 20min)
- **Impacts:** RELIABILITY: MEDIUM

> Detects expensive resources or objects that are eagerly initialized but may not always be used. This wastes memory and increases startup time. Use lazy initialization patterns to defer creation until first access, especially for database connections, file handles, or large data structures.

### N+1 Query Problem

- **Key:** `n-plus-one-query`
- **File:** [`rules/performance/n-plus-one-query.json`](rules/performance/n-plus-one-query.json)
- **Severity:** 🟠 CRITICAL
- **Type:** CODE_SMELL
- **Tags:** `performance`, `database`, `orm`, `optimization`
- **Remediation cost:** 30min
- **Debt:** CONSTANT_ISSUE (offset: 30min)
- **Impacts:** MAINTAINABILITY: HIGH

> Detects potential N+1 query issues where database queries are executed inside loops, causing severe performance degradation.

### String Concatenation in Loop

- **Key:** `string-concatenation-in-loop`
- **File:** [`rules/performance/string-concatenation-in-loop.json`](rules/performance/string-concatenation-in-loop.json)
- **Severity:** 🟡 MAJOR
- **Type:** CODE_SMELL
- **Tags:** `performance`, `memory`, `strings`, `optimization`
- **Remediation cost:** 10min
- **Debt:** CONSTANT_ISSUE (offset: 10min)
- **Impacts:** MAINTAINABILITY: MEDIUM

> Detects string concatenation using + operator inside loops, which creates unnecessary string objects and degrades performance.

### Synchronous I/O in Async Context

- **Key:** `synchronous-io-in-async`
- **File:** [`rules/performance/synchronous-io-in-async.json`](rules/performance/synchronous-io-in-async.json)
- **Severity:** 🟡 MAJOR
- **Type:** CODE_SMELL
- **Tags:** `performance`, `async`, `reactive`, `concurrency`
- **Remediation cost:** 30min
- **Debt:** CONSTANT_ISSUE (offset: 30min)
- **Impacts:** MAINTAINABILITY: MEDIUM

> Detects blocking I/O operations within asynchronous methods or reactive streams, which defeats the purpose of async programming and can cause thread pool exhaustion.

### Unbounded Collection Growth

- **Key:** `unbounded-collection-growth`
- **File:** [`rules/performance/unbounded-collection-growth.json`](rules/performance/unbounded-collection-growth.json)
- **Severity:** 🟠 CRITICAL
- **Type:** BUG
- **Tags:** `performance`, `memory`, `memory-leak`, `cache`
- **Remediation cost:** 45min
- **Debt:** CONSTANT_ISSUE (offset: 45min)
- **Impacts:** RELIABILITY: HIGH

> Detects collections (caches, queues, lists) that grow without bounds and lack eviction policies. Unbounded collections can consume all available memory over time, leading to OutOfMemoryError. Implement size limits, TTL-based eviction, or use bounded data structures.

### Unnecessary Boxing/Unboxing

- **Key:** `unnecessary-boxing`
- **File:** [`rules/performance/unnecessary-boxing.json`](rules/performance/unnecessary-boxing.json)
- **Severity:** 🔵 MINOR
- **Type:** CODE_SMELL
- **Tags:** `performance`, `memory`, `primitives`, `optimization`
- **Remediation cost:** 5min
- **Debt:** CONSTANT_ISSUE (offset: 5min)
- **Impacts:** MAINTAINABILITY: LOW

> Detects unnecessary conversions between primitive types and their wrapper classes, which impacts performance and memory usage.

### Unoptimized Regular Expression

- **Key:** `unoptimized-regex`
- **File:** [`rules/performance/unoptimized-regex.json`](rules/performance/unoptimized-regex.json)
- **Severity:** 🟠 CRITICAL
- **Type:** BUG
- **Tags:** `performance`, `regex`, `redos`, `security`
- **Remediation cost:** 30min
- **Debt:** CONSTANT_ISSUE (offset: 30min)
- **Impacts:** RELIABILITY: HIGH

> Detects regular expressions that are compiled repeatedly instead of being cached, or patterns susceptible to catastrophic backtracking (ReDoS). Compile patterns once and reuse them. Avoid nested quantifiers and overlapping alternations that cause exponential time complexity.

## Maintainability (12 rules)

### Boolean Blindness

- **Key:** `boolean-blindness`
- **File:** [`rules/maintainability/boolean-blindness.json`](rules/maintainability/boolean-blindness.json)
- **Severity:** 🔵 MINOR
- **Type:** CODE_SMELL
- **Tags:** `maintainability`, `readability`, `api-design`, `clean-code`
- **Remediation cost:** 25min
- **Debt:** CONSTANT_ISSUE (offset: 25min)
- **Impacts:** MAINTAINABILITY: LOW
- **Parameters:**
  - `maxBooleanParams` (INTEGER) — Maximum number of boolean parameters allowed before triggering the rule *(default: 2)*

> Detects methods with multiple boolean parameters or return values whose meaning is unclear at the call site. Boolean parameters make code harder to read and prone to errors. Replace with enums, builder patterns, or separate methods with descriptive names.

### Circular Dependencies Between Modules

- **Key:** `circular-dependencies`
- **File:** [`rules/maintainability/circular-dependencies.json`](rules/maintainability/circular-dependencies.json)
- **Severity:** 🟡 MAJOR
- **Type:** CODE_SMELL
- **Tags:** `maintainability`, `design`, `architecture`, `coupling`
- **Remediation cost:** 60min
- **Debt:** CONSTANT_ISSUE (offset: 60min)
- **Impacts:** MAINTAINABILITY: HIGH

> Detects circular dependencies between packages, modules, or classes where A depends on B and B depends on A (directly or transitively). Circular dependencies make code harder to understand, test, and refactor. Break cycles by introducing interfaces, extracting common code, or using dependency injection.

### Deeply Nested Code

- **Key:** `deep-nesting`
- **File:** [`rules/maintainability/deep-nesting.json`](rules/maintainability/deep-nesting.json)
- **Severity:** 🟡 MAJOR
- **Type:** CODE_SMELL
- **Tags:** `maintainability`, `complexity`, `readability`, `refactoring`
- **Remediation cost:** 20min
- **Debt:** CONSTANT_ISSUE (offset: 20min)
- **Impacts:** MAINTAINABILITY: MEDIUM
- **Parameters:**
  - `maxDepth` (INTEGER) — Maximum allowed nesting depth *(default: 4)*

> Detects code with excessive nesting levels (if statements, loops, try blocks), which reduces readability and increases cognitive complexity.

### Excessive or Redundant Comments

- **Key:** `excessive-comments`
- **File:** [`rules/maintainability/excessive-comments.json`](rules/maintainability/excessive-comments.json)
- **Severity:** 🔵 MINOR
- **Type:** CODE_SMELL
- **Tags:** `maintainability`, `documentation`, `readability`, `clean-code`
- **Remediation cost:** 15min
- **Debt:** CONSTANT_ISSUE (offset: 15min)
- **Impacts:** MAINTAINABILITY: LOW

> Detects code with excessive comments that explain what the code does rather than why. Comments that restate obvious code indicate unclear naming or design. Prefer self-documenting code with clear names. Reserve comments for explaining business rules, non-obvious decisions, or warnings.

### Hardcoded URLs and Endpoints

- **Key:** `hardcoded-urls`
- **File:** [`rules/maintainability/hardcoded-urls.json`](rules/maintainability/hardcoded-urls.json)
- **Severity:** 🔵 MINOR
- **Type:** CODE_SMELL
- **Tags:** `maintainability`, `configuration`, `deployment`, `best-practices`
- **Remediation cost:** 10min
- **Debt:** CONSTANT_ISSUE (offset: 10min)
- **Impacts:** MAINTAINABILITY: LOW

> Detects hardcoded URLs, IP addresses, and endpoints that should be externalized to configuration files for better maintainability and environment flexibility.

### Hidden Dependencies

- **Key:** `hidden-dependencies`
- **File:** [`rules/maintainability/hidden-dependencies.json`](rules/maintainability/hidden-dependencies.json)
- **Severity:** 🟡 MAJOR
- **Type:** CODE_SMELL
- **Tags:** `maintainability`, `design`, `testability`, `dependency-injection`
- **Remediation cost:** 30min
- **Debt:** CONSTANT_ISSUE (offset: 30min)
- **Impacts:** MAINTAINABILITY: MEDIUM

> Detects dependencies that are not explicit in method signatures, such as using global state, singletons, static method calls, or service locators. Hidden dependencies make code harder to test and understand. Use dependency injection to make all dependencies explicit.

### Inconsistent Naming Convention

- **Key:** `inconsistent-naming`
- **File:** [`rules/maintainability/inconsistent-naming.json`](rules/maintainability/inconsistent-naming.json)
- **Severity:** 🔵 MINOR
- **Type:** CODE_SMELL
- **Tags:** `maintainability`, `naming`, `conventions`, `readability`
- **Remediation cost:** 5min
- **Debt:** CONSTANT_ISSUE (offset: 5min)
- **Impacts:** MAINTAINABILITY: LOW

> Detects variables, methods, and classes that don't follow established naming conventions (camelCase, PascalCase, SCREAMING_SNAKE_CASE), reducing code consistency.

### Method Length Limit

- **Key:** `long-methods`
- **File:** [`rules/maintainability/long-methods.json`](rules/maintainability/long-methods.json)
- **Severity:** 🟡 MAJOR
- **Type:** CODE_SMELL
- **Tags:** `maintainability`, `readability`, `method-length`
- **Remediation cost:** 2min
- **Debt:** LINEAR (offset: 0min) (coefficient: 2min)
- **Impacts:** MAINTAINABILITY: MEDIUM
- **Parameters:**
  - `max` (INTEGER) — Maximum allowed lines of code per method *(default: 100)*

> Detects methods or functions that exceed a reasonable length threshold, making them harder to understand and maintain. Long methods should be refactored into smaller, focused units.

### Missing Documentation

- **Key:** `missing-javadoc`
- **File:** [`rules/maintainability/missing-javadoc.json`](rules/maintainability/missing-javadoc.json)
- **Severity:** 🔵 MINOR
- **Type:** CODE_SMELL
- **Tags:** `maintainability`, `documentation`, `javadoc`, `readability`
- **Remediation cost:** 10min
- **Debt:** CONSTANT_ISSUE (offset: 10min)
- **Impacts:** MAINTAINABILITY: LOW

> Detects public classes, methods, and interfaces that lack proper documentation comments, making the code harder to understand and use.

### Missing Null Check

- **Key:** `missing-null-check`
- **File:** [`rules/maintainability/missing-null-check.json`](rules/maintainability/missing-null-check.json)
- **Severity:** 🟡 MAJOR
- **Type:** BUG
- **Tags:** `maintainability`, `null-safety`, `defensive-programming`, `reliability`
- **Remediation cost:** 10min
- **Debt:** CONSTANT_ISSUE (offset: 10min)
- **Impacts:** RELIABILITY: MEDIUM

> Detects potential null pointer dereferences where objects are used without proper null validation, leading to runtime NullPointerExceptions.

### Shotgun Surgery

- **Key:** `shotgun-surgery`
- **File:** [`rules/maintainability/shotgun-surgery.json`](rules/maintainability/shotgun-surgery.json)
- **Severity:** 🟡 MAJOR
- **Type:** CODE_SMELL
- **Tags:** `maintainability`, `design`, `cohesion`, `refactoring`
- **Remediation cost:** 60min
- **Debt:** LINEAR (offset: 0min) (coefficient: 20min)
- **Impacts:** MAINTAINABILITY: HIGH

> Detects changes that require many small modifications across multiple classes or modules. This indicates poor cohesion and scattered responsibilities. When a single change requires editing many files, consolidate related logic into a single class or module.

### Too Many Method Parameters

- **Key:** `too-many-parameters`
- **File:** [`rules/maintainability/too-many-parameters.json`](rules/maintainability/too-many-parameters.json)
- **Severity:** 🟡 MAJOR
- **Type:** CODE_SMELL
- **Tags:** `maintainability`, `readability`, `parameters`, `design`
- **Remediation cost:** 15min
- **Debt:** CONSTANT_ISSUE (offset: 15min)
- **Impacts:** MAINTAINABILITY: MEDIUM
- **Parameters:**
  - `max` (INTEGER) — Maximum allowed number of parameters *(default: 7)*

> Detects methods or functions with too many parameters, which makes the code harder to understand and use. Consider using parameter objects or builder patterns.

