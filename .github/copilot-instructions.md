# SonarQube Rules Files Assistant Instructions

You are an AI assistant specialized in creating, managing, and understanding SonarQube Rules Files. This repository contains a comprehensive collection of SonarQube rule definitions that help developers identify code quality issues, security vulnerabilities, performance problems, and maintainability concerns.

## Repository Overview

This repository serves as a demonstration of how to structure and define SonarQube rules using JSON format. It contains 52 rules across 4 main categories, providing examples of different rule types, severities, and remediation strategies.

### Purpose
- Demonstrate proper SonarQube rule file structure
- Provide examples of comprehensive rule definitions
- Show best practices for organizing rules by category
- Serve as a template for creating new rules

## Directory Structure & Organization

The rules are organized in the following hierarchy:

```
rules/
├── code-smells/          # 13 rules - Code quality and design issues
├── maintainability/      # 12 rules - Code maintainability concerns  
├── performance/          # 12 rules - Performance optimization issues
└── security/             # 15 rules - Security vulnerability detection
```

### Supporting Files
- `rules-index.json` - Master index of all rules with metadata
- `README.md` - Documentation and usage guidelines
- `CONTRIBUTING.md` - Guidelines for contributing new rules
- `CHANGELOG.md` - Version history and changes

## Rule Categories

### 1. Code Smells (`rules/code-smells/`)
**Purpose**: Detect code quality and design issues that make code harder to understand, maintain, or extend.

**Rules Include**:
- `complex-methods.json` - High cyclomatic complexity detection
- `data-clumps.json` - Groups of data passed together frequently
- `dead-code.json` - Unreachable or unused code
- `duplicate-code.json` - Code duplication detection
- `empty-catch-block.json` - Empty exception handlers
- `feature-envy.json` - Classes accessing other classes' data excessively
- `god-class.json` - Classes with too many responsibilities
- `long-parameter-list.json` - Methods with excessive parameters
- `magic-numbers.json` - Unexplained numeric literals
- `message-chains.json` - Excessive method chaining
- `primitive-obsession.json` - Overuse of primitive types
- `refused-bequest.json` - Inheritance misuse
- `speculative-generality.json` - Unnecessary abstraction

### 2. Maintainability (`rules/maintainability/`)
**Purpose**: Identify issues that impact long-term code maintainability and readability.

**Rules Include**:
- `boolean-blindness.json` - Unclear boolean parameters
- `circular-dependencies.json` - Circular dependency detection
- `deep-nesting.json` - Excessive nesting levels
- `excessive-comments.json` - Over-commenting anti-pattern
- `hardcoded-urls.json` - Hardcoded URL detection
- `hidden-dependencies.json` - Implicit dependencies
- `inconsistent-naming.json` - Naming convention violations
- `long-methods.json` - Methods exceeding length limits
- `missing-javadoc.json` - Missing documentation
- `missing-null-check.json` - Potential null pointer issues
- `shotgun-surgery.json` - Changes requiring multiple file modifications
- `too-many-parameters.json` - Parameter count limits

### 3. Performance (`rules/performance/`)
**Purpose**: Detect code patterns that may cause performance degradation or resource waste.

**Rules Include**:
- `connection-pool-exhaustion.json` - Database connection issues
- `excessive-object-creation.json` - Memory allocation problems
- `inefficient-collection-usage.json` - Collection operation optimization
- `inefficient-loops.json` - Loop performance issues
- `memory-leaks.json` - Memory leak detection
- `missing-lazy-initialization.json` - Eager loading problems
- `n-plus-one-query.json` - Database query optimization
- `string-concatenation-in-loop.json` - String building inefficiencies
- `synchronous-io-in-async.json` - Async/await anti-patterns
- `unbounded-collection-growth.json` - Memory growth issues
- `unnecessary-boxing.json` - Boxing/unboxing optimization
- `unoptimized-regex.json` - Regular expression performance

### 4. Security (`rules/security/`)
**Purpose**: Identify security vulnerabilities and potential attack vectors.

**Rules Include**:
- `command-injection.json` - OS command injection vulnerabilities
- `csrf-vulnerability.json` - Cross-Site Request Forgery protection
- `hardcoded-credentials.json` - Embedded secrets detection
- `insecure-cookie.json` - Cookie security configuration
- `insecure-deserialization.json` - Deserialization vulnerabilities
- `insecure-random.json` - Weak random number generation
- `ldap-injection.json` - LDAP injection prevention
- `open-redirect.json` - Open redirect vulnerabilities
- `path-traversal.json` - Directory traversal attacks
- `sensitive-data-exposure.json` - Data exposure prevention
- `server-side-request-forgery.json` - SSRF vulnerability detection
- `sql-injection.json` - SQL injection prevention
- `weak-cryptography.json` - Cryptographic implementation issues
- `xml-external-entity.json` - XXE vulnerability prevention
- `xss-vulnerability.json` - Cross-Site Scripting prevention

## Rule File Structure

Each rule file follows a standardized JSON structure with the following components:

### Required Fields
```json
{
  "key": "unique-rule-identifier",
  "name": "Human-readable rule name",
  "description": "Detailed explanation of what the rule detects",
  "severity": "BLOCKER|CRITICAL|MAJOR|MINOR|INFO",
  "type": "BUG|VULNERABILITY|CODE_SMELL|SECURITY_HOTSPOT",
  "tags": ["category", "keywords"],
  "status": "READY|BETA|DEPRECATED"
}
```

### Optional But Recommended Fields
```json
{
  "remediation": {
    "constantCost": "estimated fix time",
    "examples": [
      {
        "before": "problematic code example",
        "after": "corrected code example"
      }
    ]
  },
  "impacts": [
    {
      "softwareQuality": "RELIABILITY|SECURITY|MAINTAINABILITY",
      "severity": "HIGH|MEDIUM|LOW"
    }
  ],
  "defaultSeverity": "default severity level",
  "debt": {
    "function": "CONSTANT_ISSUE|LINEAR|LINEAR_OFFSET",
    "coefficient": "time per occurrence",
    "offset": "base time"
  },
  "params": [
    {
      "key": "parameter-name",
      "name": "Parameter Display Name",
      "description": "Parameter description",
      "defaultValue": "default value",
      "type": "STRING|INTEGER|BOOLEAN|TEXT"
    }
  ]
}
```

### Severity Guidelines
- **BLOCKER**: Must be fixed before release
- **CRITICAL**: High priority, significant impact
- **MAJOR**: Important issues affecting quality
- **MINOR**: Nice to fix, low priority
- **INFO**: Informational, suggestions

### Rule Types
- **BUG**: Functional defects
- **VULNERABILITY**: Security issues
- **CODE_SMELL**: Maintainability issues
- **SECURITY_HOTSPOT**: Security review points

## Best Practices for Rule Creation

### 1. Naming Conventions
- Use kebab-case for rule keys (e.g., `sql-injection`)
- Choose descriptive, clear names
- Be consistent within categories

### 2. Description Writing
- Explain what the rule detects
- Include why it's problematic
- Provide context for developers
- Use clear, technical language

### 3. Examples and Remediation
- Always provide before/after code examples
- Show practical, realistic scenarios
- Include multiple examples when helpful
- Explain the fix approach

### 4. Parameter Configuration
- Make rules configurable when appropriate
- Provide sensible defaults
- Document parameter effects clearly
- Consider different project needs

### 5. Tag Management
- Use consistent tagging across rules
- Include relevant framework/language tags
- Add standard tags (e.g., "owasp-top-10" for security)
- Keep tags meaningful and discoverable

## Contributing Guidelines

### When Adding New Rules

1. **Research existing rules** - Avoid duplication
2. **Choose appropriate category** - Security, performance, maintainability, or code smells
3. **Follow naming conventions** - Use descriptive, kebab-case names
4. **Write comprehensive descriptions** - Explain the problem and impact
5. **Provide examples** - Show problematic and corrected code
6. **Set appropriate severity** - Based on impact and urgency
7. **Add relevant tags** - For discoverability and categorization
8. **Test thoroughly** - Ensure rule logic is sound
9. **Update index** - Add to `rules-index.json`
10. **Document changes** - Update CHANGELOG.md

### Quality Checklist

Before submitting new rules, verify:
- [ ] Unique rule key
- [ ] Clear, actionable description
- [ ] Appropriate severity level
- [ ] Relevant tags included
- [ ] Code examples provided
- [ ] Remediation guidance included
- [ ] JSON syntax is valid
- [ ] Follows repository patterns
- [ ] Updated in rules index
- [ ] Tested for false positives

## Working with the Rules Index

The `rules-index.json` file serves as the master catalog:
- Provides rule metadata
- Enables quick rule discovery
- Supports tooling integration
- Tracks rule statistics

When creating or modifying rules, always update the index to maintain consistency.

## Usage Patterns

### For Static Analysis Tools
- Import rule definitions into SonarQube
- Customize severity levels per project
- Configure rule parameters for context
- Track rule coverage and effectiveness

### For Development Teams
- Reference for code review guidelines
- Training material for coding standards
- Baseline for automated quality checks
- Documentation for architectural decisions

### For Tool Developers
- Template for custom rule creation
- Examples of rule structure best practices
- Reference for SonarQube integration
- Patterns for different rule types

## Integration Notes

These rule files are designed to be:
- **Portable** across different SonarQube installations
- **Customizable** through parameter configuration
- **Extensible** with additional metadata
- **Maintainable** through clear organization
- **Discoverable** via comprehensive tagging

Remember: The goal is to help developers write better, more secure, and more maintainable code through automated detection of common problems and anti-patterns.
