# sonar-cube-rule-demo

An example of how Copilot can be leveraged to assist with creating and managing SonarQube Rules Files

## Overview

This repository contains a collection of SonarQube rule definitions organized by category. Each rule is defined in JSON format following SonarQube's rule specification standards.

## Directory Structure

```
rules/
├── security/              # Security vulnerability rules (10 rules)
│   ├── command-injection.json
│   ├── csrf-vulnerability.json
│   ├── hardcoded-credentials.json
│   ├── insecure-deserialization.json
│   ├── insecure-random.json
│   ├── path-traversal.json
│   ├── sensitive-data-exposure.json
│   ├── sql-injection.json
│   ├── weak-cryptography.json
│   └── xss-vulnerability.json
├── code-smells/          # Code quality and maintainability issues (8 rules)
│   ├── complex-methods.json
│   ├── dead-code.json
│   ├── duplicate-code.json
│   ├── empty-catch-block.json
│   ├── feature-envy.json
│   ├── god-class.json
│   ├── long-parameter-list.json
│   └── magic-numbers.json
├── performance/          # Performance-related rules (7 rules)
│   ├── inefficient-collection-usage.json
│   ├── inefficient-loops.json
│   ├── memory-leaks.json
│   ├── n-plus-one-query.json
│   ├── string-concatenation-in-loop.json
│   ├── synchronous-io-in-async.json
│   └── unnecessary-boxing.json
└── maintainability/      # Code maintainability rules (7 rules)
    ├── deep-nesting.json
    ├── hardcoded-urls.json
    ├── inconsistent-naming.json
    ├── long-methods.json
    ├── missing-javadoc.json
    ├── missing-null-check.json
    └── too-many-parameters.json
```

## Rule Categories

### Security (10 rules)
- **Command Injection**: Detects OS command injection vulnerabilities where user input is passed to system commands
- **CSRF Vulnerability**: Detects missing Cross-Site Request Forgery protection on state-changing operations
- **Hardcoded Credentials**: Finds hardcoded passwords and API keys
- **Insecure Deserialization**: Detects unsafe deserialization of untrusted data leading to potential RCE
- **Insecure Random**: Detects usage of predictable random number generators for security-sensitive operations
- **Path Traversal**: Identifies path traversal vulnerabilities allowing access to files outside intended directories
- **Sensitive Data Exposure**: Detects logging of sensitive information like passwords and PII
- **SQL Injection Prevention**: Detects potential SQL injection vulnerabilities
- **Weak Cryptography**: Detects usage of weak or deprecated cryptographic algorithms (MD5, SHA1, DES)
- **XSS Vulnerability**: Identifies Cross-Site Scripting risks

### Code Smells (8 rules)
- **Complex Methods**: Flags methods with high cyclomatic complexity
- **Dead Code**: Detects unreachable code, unused variables, methods, or classes
- **Duplicate Code**: Identifies code duplication
- **Empty Catch Block**: Detects empty catch blocks that silently swallow exceptions
- **Feature Envy**: Detects methods that use more features from other classes than their own
- **God Class**: Detects classes that are too large and handle too many responsibilities
- **Long Parameter List**: Detects methods with too many parameters
- **Magic Numbers**: Detects unnamed numerical constants

### Performance (7 rules)
- **Inefficient Collection Usage**: Detects improper use of collections and missing initial capacity
- **Inefficient Loops**: Detects performance issues in loops
- **Memory Leaks**: Identifies potential memory leak patterns
- **N+1 Query Problem**: Detects database queries executed inside loops causing performance degradation
- **String Concatenation in Loop**: Detects string concatenation using + operator inside loops
- **Synchronous I/O in Async Context**: Detects blocking I/O operations within async methods
- **Unnecessary Boxing**: Detects unnecessary conversions between primitives and wrapper classes

### Maintainability (7 rules)
- **Deep Nesting**: Detects code with excessive nesting levels reducing readability
- **Hardcoded URLs**: Detects hardcoded URLs and endpoints that should be externalized
- **Inconsistent Naming**: Detects variables and methods not following naming conventions
- **Long Methods**: Flags methods exceeding length thresholds
- **Missing Documentation**: Detects public APIs lacking proper documentation comments
- **Missing Null Check**: Detects potential null pointer dereferences
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

## Contributing

When adding new rules:
1. Place them in the appropriate category directory
2. Follow the existing JSON structure
3. Include clear descriptions and remediation examples
4. Set appropriate severity and type classifications
