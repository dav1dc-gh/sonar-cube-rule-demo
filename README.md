# sonar-cube-rule-demo

An example of how Copilot can be leveraged to assist with creating and managing SonarQube Rules Files

## Overview

This repository contains a collection of SonarQube rule definitions organized by category. Each rule is defined in JSON format following SonarQube's rule specification standards.

## Directory Structure

```
rules/
├── security/              # Security vulnerability rules (15 rules)
│   ├── command-injection.json
│   ├── csrf-vulnerability.json
│   ├── hardcoded-credentials.json
│   ├── insecure-cookie.json
│   ├── insecure-deserialization.json
│   ├── insecure-random.json
│   ├── ldap-injection.json
│   ├── open-redirect.json
│   ├── path-traversal.json
│   ├── sensitive-data-exposure.json
│   ├── server-side-request-forgery.json
│   ├── sql-injection.json
│   ├── weak-cryptography.json
│   ├── xml-external-entity.json
│   └── xss-vulnerability.json
├── code-smells/          # Code quality and maintainability issues (13 rules)
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
│   ├── primitive-obsession.json
│   ├── refused-bequest.json
│   └── speculative-generality.json
├── performance/          # Performance-related rules (12 rules)
│   ├── connection-pool-exhaustion.json
│   ├── excessive-object-creation.json
│   ├── inefficient-collection-usage.json
│   ├── inefficient-loops.json
│   ├── memory-leaks.json
│   ├── missing-lazy-initialization.json
│   ├── n-plus-one-query.json
│   ├── string-concatenation-in-loop.json
│   ├── synchronous-io-in-async.json
│   ├── unbounded-collection-growth.json
│   ├── unnecessary-boxing.json
│   └── unoptimized-regex.json
└── maintainability/      # Code maintainability rules (12 rules)
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
    ├── shotgun-surgery.json
    └── too-many-parameters.json
```

## Rule Categories

### Security (15 rules)
- **Command Injection**: Detects OS command injection vulnerabilities where user input is passed to system commands
- **CSRF Vulnerability**: Detects missing Cross-Site Request Forgery protection on state-changing operations
- **Hardcoded Credentials**: Finds hardcoded passwords and API keys
- **Insecure Cookie**: Detects cookies created without essential security flags (Secure, HttpOnly, SameSite)
- **Insecure Deserialization**: Detects unsafe deserialization of untrusted data leading to potential RCE
- **Insecure Random**: Detects usage of predictable random number generators for security-sensitive operations
- **LDAP Injection**: Detects when user input is concatenated directly into LDAP queries without proper sanitization
- **Open Redirect**: Detects when user-controlled input is used to construct redirect URLs without proper validation
- **Path Traversal**: Identifies path traversal vulnerabilities allowing access to files outside intended directories
- **Sensitive Data Exposure**: Detects logging of sensitive information like passwords and PII
- **Server-Side Request Forgery (SSRF)**: Detects when user-controlled URLs are used to make server-side HTTP requests without validation
- **SQL Injection Prevention**: Detects potential SQL injection vulnerabilities
- **Weak Cryptography**: Detects usage of weak or deprecated cryptographic algorithms (MD5, SHA1, DES)
- **XML External Entity (XXE)**: Detects XML parsers configured to process external entities leading to XXE attacks
- **XSS Vulnerability**: Identifies Cross-Site Scripting risks

### Code Smells (13 rules)
- **Complex Methods**: Flags methods with high cyclomatic complexity
- **Data Clumps**: Detects groups of variables that frequently appear together across multiple methods or classes
- **Dead Code**: Detects unreachable code, unused variables, methods, or classes
- **Duplicate Code**: Identifies code duplication
- **Empty Catch Block**: Detects empty catch blocks that silently swallow exceptions
- **Feature Envy**: Detects methods that use more features from other classes than their own
- **God Class**: Detects classes that are too large and handle too many responsibilities
- **Long Parameter List**: Detects methods with too many parameters
- **Magic Numbers**: Detects unnamed numerical constants
- **Message Chains**: Detects long chains of method calls violating the Law of Demeter
- **Primitive Obsession**: Detects overuse of primitive types instead of small objects for domain concepts
- **Refused Bequest**: Detects subclasses that override inherited methods to do nothing or throw exceptions
- **Speculative Generality**: Detects unused abstractions created for hypothetical future requirements

### Performance (12 rules)
- **Connection Pool Exhaustion**: Detects database or HTTP connections that are not properly closed or returned to the pool
- **Excessive Object Creation**: Detects unnecessary object allocation in frequently executed code paths
- **Inefficient Collection Usage**: Detects improper use of collections and missing initial capacity
- **Inefficient Loops**: Detects performance issues in loops
- **Memory Leaks**: Identifies potential memory leak patterns
- **Missing Lazy Initialization**: Detects expensive resources that are eagerly initialized but may not always be used
- **N+1 Query Problem**: Detects database queries executed inside loops causing performance degradation
- **String Concatenation in Loop**: Detects string concatenation using + operator inside loops
- **Synchronous I/O in Async Context**: Detects blocking I/O operations within async methods
- **Unbounded Collection Growth**: Detects collections that grow without bounds and lack eviction policies
- **Unnecessary Boxing**: Detects unnecessary conversions between primitives and wrapper classes
- **Unoptimized Regex**: Detects regular expressions compiled repeatedly or susceptible to catastrophic backtracking

### Maintainability (12 rules)
- **Boolean Blindness**: Detects methods with multiple boolean parameters whose meaning is unclear at the call site
- **Circular Dependencies**: Detects circular dependencies between packages, modules, or classes
- **Deep Nesting**: Detects code with excessive nesting levels reducing readability
- **Excessive Comments**: Detects redundant comments that explain what the code does rather than why
- **Hardcoded URLs**: Detects hardcoded URLs and endpoints that should be externalized
- **Hidden Dependencies**: Detects dependencies that are not explicit in method signatures
- **Inconsistent Naming**: Detects variables and methods not following naming conventions
- **Long Methods**: Flags methods exceeding length thresholds
- **Missing Documentation**: Detects public APIs lacking proper documentation comments
- **Missing Null Check**: Detects potential null pointer dereferences
- **Shotgun Surgery**: Detects changes that require many small modifications across multiple classes
- **Too Many Parameters**: Detects methods with excessive parameters

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

## Usage

These rule definitions can be imported into SonarQube custom rule plugins or used as reference for creating custom quality profiles.

### Scripts

| Command | Description |
|---|---|
| `npm run validate` | Validate all rule JSON files against the schema and conventions |
| `npm run validate:verbose` | Same as above with per-file pass/fail output |
| `npm run catalog` | Regenerate `RULES_CATALOG.md` from rule files |
| `npm run index` | Generate `rules/index.json` machine-readable index |
| `npm run audit` | Run deep quality audit (duplicates, tag issues, cost outliers) |
| `npm run drift` | Detect drift between rule files and copilot instructions |
| `npm run check` | Validate + catalog + index in one command |

## Copilot Agents

This repository includes three custom Copilot agents in `.github/agents/` that automate routine operations. Select them from the Copilot agent dropdown in your IDE or on GitHub.com.

### Rule Author (`@rule-author`)

Creates new SonarQube rule files with full validation and artifact refresh.

- **When to use**: Adding a new rule to the repository
- **What it does**: Guides you through category selection, checks for duplicates, generates the JSON file, validates it, refreshes the catalog/index, and syncs instructions
- **Tools**: read, edit, search, execute
- **Example prompts**:
  - "Create a new rule for detecting insecure TLS configurations"
  - "Add a performance rule for detecting excessive database connections"

### Repo Auditor (`@repo-auditor`)

Read-only agent that audits all rules for quality and consistency issues.

- **When to use**: Routine quality checks, before releases, or after batch imports
- **What it does**: Runs the audit script, schema validation, and drift detection, then presents a structured report with errors, warnings, and suggestions
- **Tools**: read, search, execute (no edit — intentionally read-only)
- **Example prompts**:
  - "Run a quality audit on all rules"
  - "Check if anything is out of sync"

### Repo Maintainer (`@repo-maintainer`)

Fixes audit findings, regenerates artifacts, and syncs documentation.

- **When to use**: Regular upkeep, after batch changes, or to fix issues flagged by the auditor
- **What it does**: Runs diagnostics → proposes fixes with confirmation → regenerates catalog/index → syncs instructions → verifies clean state
- **Tools**: read, edit, search, execute
- **Example prompts**:
  - "Fix all the issues from the last audit"
  - "Refresh everything after my recent changes"
  - "Sync the custom instructions with current rules"

## Copilot Skills

The agents are powered by four reusable skills in `.github/skills/`:

| Skill | Description | Key Script |
|---|---|---|
| `rule-creation-wizard` | Guided new rule creation workflow | `validate-new-rule.sh` |
| `data-quality-audit` | Deep consistency analysis | `audit-rules.js` |
| `catalog-index-refresh` | Catalog and index regeneration | `generate-index.js` |
| `custom-instructions-sync` | Drift detection and instruction updates | `detect-drift.js` |

Skills auto-activate when Copilot detects a relevant task. Agents compose these skills into end-to-end workflows.

## Contributing

When adding new rules:
1. Place them in the appropriate category directory
2. Follow the existing JSON structure
3. Include clear descriptions and remediation examples
4. Set appropriate severity and type classifications
