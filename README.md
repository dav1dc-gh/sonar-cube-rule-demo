# sonar-cube-rule-demo

An example of how Copilot can be leveraged to assist with creating and managing SonarQube Rules Files

## Overview

This repository contains a collection of SonarQube rule definitions organized by category. Each rule is defined in JSON format following SonarQube's rule specification standards.

## Directory Structure

```
rules/
├── security/              # Security vulnerability rules
│   ├── sql-injection.json
│   ├── xss-vulnerability.json
│   └── hardcoded-credentials.json
├── code-smells/          # Code quality and maintainability issues
│   ├── magic-numbers.json
│   ├── duplicate-code.json
│   └── complex-methods.json
├── performance/          # Performance-related rules
│   ├── inefficient-loops.json
│   └── memory-leaks.json
└── maintainability/      # Code maintainability rules
    ├── long-methods.json
    └── too-many-parameters.json
```

## Rule Categories

### Security (3 rules)
- **SQL Injection Prevention**: Detects potential SQL injection vulnerabilities
- **XSS Vulnerability**: Identifies Cross-Site Scripting risks
- **Hardcoded Credentials**: Finds hardcoded passwords and API keys

### Code Smells (3 rules)
- **Magic Numbers**: Detects unnamed numerical constants
- **Duplicate Code**: Identifies code duplication
- **Complex Methods**: Flags methods with high cyclomatic complexity

### Performance (2 rules)
- **Inefficient Loops**: Detects performance issues in loops
- **Memory Leaks**: Identifies potential memory leak patterns

### Maintainability (2 rules)
- **Long Methods**: Flags methods exceeding length thresholds
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
