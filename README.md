# sonar-cube-rule-demo

An example of how Copilot can be leveraged to assist with creating and managing SonarQube Rules Files

## Overview

This repository contains a collection of SonarQube rule definitions organized by category. Each rule is defined in JSON format following SonarQube's rule specification standards.

## Directory Structure

```
rules/
├── security/              # Security rules (25 rules)
│   ├── command-injection.json
│   ├── csrf-vulnerability.json
│   ├── disabled-certificate-validation.json
│   ├── hardcoded-credentials.json
│   ├── insecure-cookie.json
│   ├── insecure-deserialization.json
│   ├── insecure-random.json
│   ├── integer-overflow.json
│   ├── jwt-misconfiguration.json
│   ├── ldap-injection.json
│   ├── log-injection.json
│   ├── mass-assignment.json
│   ├── missing-authorization-check.json
│   ├── open-redirect.json
│   ├── path-traversal.json
│   ├── permissive-cors.json
│   ├── prototype-pollution.json
│   ├── sensitive-data-exposure.json
│   ├── server-side-request-forgery.json
│   ├── sql-injection.json
│   ├── timing-attack.json
│   ├── unsafe-reflection.json
│   ├── weak-cryptography.json
│   ├── xml-external-entity.json
│   └── xss-vulnerability.json
├── code-smells/           # Code Smells rules (16 rules)
│   ├── anemic-domain-model.json
│   ├── complex-methods.json
│   ├── data-clumps.json
│   ├── dead-code.json
│   ├── duplicate-code.json
│   ├── empty-catch-block.json
│   ├── feature-envy.json
│   ├── god-class.json
│   ├── long-parameter-list.json
│   ├── magic-numbers.json
│   ├── message-chains.json
│   ├── null-pointer-dereference.json
│   ├── primitive-obsession.json
│   ├── refused-bequest.json
│   ├── speculative-generality.json
│   └── unchecked-return-value.json
├── performance/           # Performance rules (17 rules)
│   ├── connection-pool-exhaustion.json
│   ├── excessive-object-creation.json
│   ├── inefficient-collection-usage.json
│   ├── inefficient-loops.json
│   ├── memory-leaks.json
│   ├── missing-batch-operations.json
│   ├── missing-lazy-initialization.json
│   ├── n-plus-one-query.json
│   ├── race-condition.json
│   ├── resource-leak.json
│   ├── string-concatenation-in-loop.json
│   ├── synchronous-io-in-async.json
│   ├── thread-pool-starvation.json
│   ├── unbounded-collection-growth.json
│   ├── unclosed-resources.json
│   ├── unnecessary-boxing.json
│   └── unoptimized-regex.json
└── maintainability/       # Maintainability rules (15 rules)
    ├── boolean-blindness.json
    ├── circular-dependencies.json
    ├── deep-nesting.json
    ├── excessive-comments.json
    ├── hardcoded-urls.json
    ├── hidden-dependencies.json
    ├── inconsistent-naming.json
    ├── long-methods.json
    ├── missing-javadoc.json
    ├── missing-null-check.json
    ├── mutable-static-state.json
    ├── race-condition.json
    ├── shotgun-surgery.json
    ├── swallowed-exceptions.json
    └── too-many-parameters.json
```

## Rule Categories

### Security (25 rules)
- **Command Injection Vulnerability**: Detects potential OS command injection vulnerabilities where user input is passed to system commands without proper sanitization.
- **Cross-Site Request Forgery (CSRF)**: Detects missing CSRF protection on state-changing operations, which could allow attackers to trick users into performing unintended actions.
- **Cross-Site Scripting (XSS) Prevention**: Identifies potential XSS vulnerabilities where user-supplied data is rendered in HTML without proper encoding or sanitization.
- **Disabled SSL/TLS Certificate Validation**: Detects code that disables SSL/TLS certificate verification, enabling man-in-the-middle attacks on all HTTPS traffic (CWE-295).
- **Hardcoded Credentials Detection**: Detects hardcoded passwords, API keys, tokens, or other sensitive credentials in source code, which poses a significant security risk.
- **Insecure Cookie Configuration**: Detects cookies created without essential security flags (Secure, HttpOnly, SameSite).
- **Insecure Deserialization**: Detects unsafe deserialization of untrusted data which can lead to remote code execution, denial of service, or other attacks.
- **Insecure Random Number Generator**: Detects usage of predictable random number generators (like java.util.Random) for security-sensitive operations such as token generation or cryptographic purposes.
- **Integer Overflow**: Detects arithmetic operations on integers that can silently overflow or underflow, leading to wrong calculations, security bypasses, or buffer over-reads.
- **JWT Signature Not Verified**: Detects JWT token parsing that skips signature verification or allows the 'none' algorithm, enabling attackers to forge authentication tokens.
- **LDAP Injection Vulnerability**: Detects when user input is concatenated directly into LDAP queries without proper sanitization.
- **Log Injection**: Detects unsanitized user input written directly into log statements, enabling log forging, SIEM evasion, and potential remote code execution via logging frameworks.
- **Mass Assignment Vulnerability**: Detects direct binding of raw HTTP request bodies to domain objects or ORM entities without an explicit allow-list, allowing attackers to set privileged fields such as isAdmin or role.
- **Missing Authorization Check**: Detects endpoints or data-access methods that lack authorization verification, enabling Insecure Direct Object Reference attacks (CWE-862, OWASP A01).
- **Open Redirect Vulnerability**: Detects when user-controlled input is used to construct redirect URLs without proper validation.
- **Overly Permissive CORS Configuration**: Detects CORS configurations that reflect arbitrary Origins or combine a wildcard allow-origin with credentials, enabling cross-origin authenticated requests from any attacker-controlled site.
- **Path Traversal Vulnerability**: Detects potential path traversal vulnerabilities where user input is used to construct file paths without proper validation, allowing attackers to access files outside the intended directory.
- **Prototype Pollution**: Detects unguarded recursive merge or property assignment where attacker-controlled keys such as __proto__ can corrupt Object.prototype, compromising every object in the runtime.
- **Sensitive Data Exposure in Logs**: Detects logging of sensitive information such as passwords, credit card numbers, social security numbers, or personal identifiable information (PII).
- **Server-Side Request Forgery (SSRF)**: Detects when user-controlled URLs are used to make server-side HTTP requests without validation.
- **SQL Injection Prevention**: Detects potential SQL injection vulnerabilities where user input is directly concatenated into SQL queries without proper sanitization or parameterization.
- **Timing Attack on Secret Comparison**: Detects use of standard equality operators to compare secrets, tokens, or HMAC signatures, which leaks timing information and allows attackers to reconstruct the secret byte by byte.
- **Unsafe Reflection from User Input**: Detects use of reflection APIs such as Class.forName() or Method.invoke() with user-controlled input, which can lead to remote code execution (CWE-470).
- **Weak Cryptographic Algorithm**: Detects usage of weak or deprecated cryptographic algorithms such as MD5, SHA1, DES, or RC4 that are vulnerable to attacks.
- **XML External Entity (XXE) Injection**: Detects XML parsers configured to process external entities, which can lead to XXE attacks.

### Code Smells (16 rules)
- **Anemic Domain Model**: Detects domain objects that contain only fields and accessors with no business logic, violating OOP encapsulation principles and scattering behaviour across service layers.
- **Avoid Magic Numbers**: Detects the use of magic numbers (unnamed numerical constants) in code, which reduces readability and maintainability.
- **Data Clumps**: Detects groups of variables that frequently appear together across multiple methods or classes.
- **Dead Code Detection**: Detects unreachable code, unused variables, methods, or classes that serve no purpose and should be removed to improve code clarity.
- **Duplicate Code Blocks**: Identifies duplicate or nearly identical code blocks that should be refactored into reusable functions or methods to improve maintainability and reduce technical debt.
- **Empty Catch Block**: Detects empty catch blocks that silently swallow exceptions, hiding potential errors and making debugging difficult.
- **Feature Envy**: Detects methods that use more features from other classes than from their own class, indicating the method may be misplaced.
- **God Class Detection**: Detects classes that have grown too large and handle too many responsibilities, violating the Single Responsibility Principle and making the code difficult to understand and maintain.
- **High Cyclomatic Complexity**: Detects methods or functions with high cyclomatic complexity (too many decision points), making them difficult to understand, test, and maintain.
- **Long Parameter List**: Detects methods with too many parameters, which makes them difficult to understand, call correctly, and maintain.
- **Message Chains (Law of Demeter Violation)**: Detects long chains of method calls like a.getB().getC().getD().doSomething().
- **Null Pointer Dereference**: Detects code paths where a potentially null reference is dereferenced without a null check, which is the most common cause of runtime crashes in production systems.
- **Primitive Obsession**: Detects overuse of primitive types instead of small objects for domain concepts.
- **Refused Bequest**: Detects subclasses that override inherited methods to do nothing or throw exceptions, or don't use most inherited functionality.
- **Speculative Generality**: Detects unused abstractions, interfaces, or parameters created for hypothetical future requirements.
- **Unchecked Return Value**: Detects when return values from methods that indicate success, failure, or resource state are silently ignored, leading to undetected errors and unreliable program behavior.

### Performance (17 rules)
- **Connection Pool Exhaustion Risk**: Detects database or HTTP connections that are not properly closed or returned to the pool.
- **Excessive Object Creation in Hot Path**: Detects unnecessary object allocation in frequently executed code paths such as loops or high-traffic methods.
- **Inefficient Collection Usage**: Detects improper use of collections such as using LinkedList for random access, ArrayList for frequent insertions, or not specifying initial capacity for large collections.
- **Inefficient Loop Operations**: Identifies performance issues in loops such as repeated method calls, unnecessary object creation, or operations that should be moved outside the loop.
- **Missing Batch Operations**: Detects individual database or API calls executed inside loops instead of using batch or bulk operations, causing severe performance degradation under load.
- **Missing Lazy Initialization**: Detects expensive resources or objects that are eagerly initialized but may not always be used.
- **N+1 Query Problem**: Detects potential N+1 query issues where database queries are executed inside loops, causing severe performance degradation.
- **Potential Memory Leak Detection**: Identifies patterns that may lead to memory leaks such as unclosed resources, event listener accumulation, or references that prevent garbage collection.
- **Race Condition on Shared Mutable State**: Detects unsynchronized access to shared mutable state across threads, including check-then-act patterns and non-thread-safe collection usage in concurrent contexts.
- **Resource Leak**: Detects streams, connections, and other closeable resources that are opened but not guaranteed to be closed, risking resource exhaustion and application instability.
- **String Concatenation in Loop**: Detects string concatenation using + operator inside loops, which creates unnecessary string objects and degrades performance.
- **Synchronous I/O in Async Context**: Detects blocking I/O operations within asynchronous methods or reactive streams, which defeats the purpose of async programming and can cause thread pool exhaustion.
- **Thread Pool Starvation from Blocking Calls**: Detects blocking calls such as Thread.sleep, CompletableFuture.get, or synchronous I/O inside shared thread pools, which can exhaust all available threads and cause a full service outage.
- **Unbounded Collection Growth**: Detects collections (caches, queues, lists) that grow without bounds and lack eviction policies.
- **Unclosed Resources**: Detects file handles, database connections, streams, and sockets that are opened but never explicitly closed, leading to resource exhaustion under load.
- **Unnecessary Boxing/Unboxing**: Detects unnecessary conversions between primitive types and their wrapper classes, which impacts performance and memory usage.
- **Unoptimized Regular Expression**: Detects regular expressions that are compiled repeatedly instead of being cached, or patterns susceptible to catastrophic backtracking (ReDoS).

### Maintainability (15 rules)
- **Boolean Blindness**: Detects methods with multiple boolean parameters or return values whose meaning is unclear at the call site.
- **Circular Dependencies Between Modules**: Detects circular dependencies between packages, modules, or classes where A depends on B and B depends on A (directly or transitively).
- **Deeply Nested Code**: Detects code with excessive nesting levels (if statements, loops, try blocks), which reduces readability and increases cognitive complexity.
- **Excessive or Redundant Comments**: Detects code with excessive comments that explain what the code does rather than why.
- **Hardcoded URLs and Endpoints**: Detects hardcoded URLs, IP addresses, and endpoints that should be externalized to configuration files for better maintainability and environment flexibility.
- **Hidden Dependencies**: Detects dependencies that are not explicit in method signatures, such as using global state, singletons, static method calls, or service locators.
- **Inconsistent Naming Convention**: Detects variables, methods, and classes that don't follow established naming conventions (camelCase, PascalCase, SCREAMING_SNAKE_CASE), reducing code consistency.
- **Method Length Limit**: Detects methods or functions that exceed a reasonable length threshold, making them harder to understand and maintain.
- **Missing Documentation**: Detects public classes, methods, and interfaces that lack proper documentation comments, making the code harder to understand and use.
- **Missing Null Check**: Detects potential null pointer dereferences where objects are used without proper null validation, leading to runtime NullPointerExceptions.
- **Mutable Static State**: Detects mutable static fields that introduce global shared state, causing thread-safety issues, hidden dependencies, and making unit testing unreliable.
- **Race Condition on Shared State**: Detects unsynchronized read-write access to shared mutable state across threads, causing intermittent data corruption and hard-to-reproduce bugs.
- **Shotgun Surgery**: Detects changes that require many small modifications across multiple classes or modules.
- **Swallowed Exceptions**: Detects catch blocks that silently discard exceptions without logging, rethrowing, or handling them, masking failures and making debugging extremely difficult.
- **Too Many Method Parameters**: Detects methods or functions with too many parameters, which makes the code harder to understand and use.

## Rule Structure

Each rule file contains:
- `key`: Unique identifier for the rule
- `name`: Human-readable rule name
- `description`: Detailed explanation of what the rule detects
- `severity`: Rule severity (BLOCKER, CRITICAL, MAJOR, MINOR, INFO)
- `type`: Rule type (VULNERABILITY, BUG, CODE_SMELL)
- `tags`: Categorization tags
- `remediation`: Fix examples and estimated time
- `impacts`: Impact on software quality attributes
- `debt`: Technical debt estimation
- `params`: Configurable parameters (when applicable)

## Tooling & Validation

This repository includes infrastructure to keep rules consistent and catch errors early:

### JSON Schema

A formal JSON Schema is provided at [`rules/schema/sonarqube-rule.schema.json`](rules/schema/sonarqube-rule.schema.json). It validates field types, enums, required fields, and conditional requirements (e.g., `debt.coefficient` is required when `debt.function` is `LINEAR`).

**VS Code users** get automatic in-editor validation via the included [`.vscode/settings.json`](.vscode/settings.json) — red squiggles appear instantly on invalid values.

### Validation Script

A Python validator covers everything the JSON Schema does plus cross-field consistency checks (key↔filename match, severity↔defaultSeverity alignment, type↔impact coherence):

```bash
# Validate all rules
python3 scripts/validate-rules.py

# Validate a single file
python3 scripts/validate-rules.py rules/security/sql-injection.json

# Strict mode (treats warnings as errors)
python3 scripts/validate-rules.py --strict
```

### CI Pipeline

The [GitHub Actions workflow](.github/workflows/validate-rules.yml) runs on every push and PR that touches rule files. It runs both standard and strict validation plus a formatting check.

### Rule Template

Start new rules from [`rules/schema/rule-template.json`](rules/schema/rule-template.json) to ensure all required fields are present from the start.

## Usage

These rule definitions can be imported into SonarQube custom rule plugins or used as reference for creating custom quality profiles.

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for the full guide. Quick summary:

1. Copy the template: `cp rules/schema/rule-template.json rules/<category>/<rule-key>.json`
2. Fill in all required fields (key must match filename, severity must match defaultSeverity)
3. Validate: `python3 scripts/validate-rules.py`
4. Open a pull request — CI handles the rest
