# Maintainability Rules - AI Assistant Custom Instructions

You are an expert assistant for creating, managing, and understanding **Maintainability Rules** in this SonarQube Rules repository. This directory contains rules that detect patterns making code harder to understand, modify, or extend.

---

## Directory Purpose

The `rules/maintainability/` directory contains **12 maintainability rules** that identify code patterns affecting readability, documentation, API design, and long-term code health.

---

## Maintainability Rules Overview

| Rule | Key | Severity | Description |
|------|-----|----------|-------------|
| Boolean Blindness | `boolean-blindness` | MINOR | Multiple boolean parameters with unclear meaning |
| Circular Dependencies | `circular-dependencies` | MAJOR | Circular dependencies between modules/classes |
| Deep Nesting | `deep-nesting` | MAJOR | Excessive nesting levels reducing readability |
| Excessive Comments | `excessive-comments` | MINOR | Redundant comments explaining "what" not "why" |
| Hardcoded URLs | `hardcoded-urls` | MINOR | URLs/endpoints that should be externalized |
| Hidden Dependencies | `hidden-dependencies` | MAJOR | Dependencies not explicit in method signatures |
| Inconsistent Naming | `inconsistent-naming` | MINOR | Violations of naming conventions |
| Long Methods | `long-methods` | MAJOR | Methods exceeding length thresholds |
| Missing Javadoc | `missing-javadoc` | MINOR | Public APIs lacking documentation |
| Missing Null Check | `missing-null-check` | MAJOR | Potential null pointer dereferences |
| Shotgun Surgery | `shotgun-surgery` | MAJOR | Changes requiring modifications across many classes |
| Too Many Parameters | `too-many-parameters` | MINOR | Methods with excessive parameter counts |

---

## Maintainability Rule Characteristics

### Required Configuration

Maintainability rules in this directory **MUST** use:

- **type**: Always `CODE_SMELL`
- **severity**: Typically `MAJOR` or `MINOR`
- **tags**: Must include `maintainability`, often include `readability`, `documentation`, `naming`
- **impacts.softwareQuality**: Always `MAINTAINABILITY`
- **impacts.severity**: Usually `MEDIUM` or `LOW`

### Severity Guidelines for Maintainability Rules

| Severity | Use When |
|----------|----------|
| `MAJOR` | Significant readability issues, hidden complexity, architectural problems |
| `MINOR` | Style issues, documentation gaps, naming inconsistencies |
| `INFO` | Best practice suggestions, style preferences |

### Required Tags

All maintainability rules should include these tags where applicable:

- `maintainability` - Required for all rules in this directory
- `readability` - For code clarity issues
- `documentation` - For documentation-related issues
- `naming` - For naming convention violations
- `api-design` - For public API concerns
- `clean-code` - For clean code principles
- `refactoring` - When refactoring is needed

---

## Maintainability Rule Template

Use this template for new maintainability rules:

```json
{
  "key": "maintainability-issue-name",
  "name": "Maintainability Issue Display Name",
  "description": "Clear description of what makes this code hard to maintain, understand, or modify. Explain the cognitive load it imposes on developers.",
  "severity": "MAJOR",
  "type": "CODE_SMELL",
  "tags": ["maintainability", "readability", "specific-tag"],
  "remediation": {
    "constantCost": "15min",
    "examples": [
      {
        "before": "// Code that's hard to understand or maintain",
        "after": "// Refactored code that's clear and self-documenting"
      }
    ]
  },
  "impacts": [
    {
      "softwareQuality": "MAINTAINABILITY",
      "severity": "MEDIUM"
    }
  ],
  "defaultSeverity": "MAJOR",
  "status": "READY",
  "debt": {
    "function": "CONSTANT_ISSUE",
    "offset": "15min"
  }
}
```

### Template with Configurable Parameters

Many maintainability rules benefit from configurable thresholds:

```json
{
  "key": "configurable-rule",
  "name": "Configurable Maintainability Rule",
  "description": "Description with configurable threshold.",
  "severity": "MAJOR",
  "type": "CODE_SMELL",
  "tags": ["maintainability"],
  "params": [
    {
      "key": "max",
      "name": "Maximum Allowed",
      "description": "Maximum value before triggering the rule",
      "defaultValue": "100",
      "type": "INTEGER"
    }
  ],
  "debt": {
    "function": "LINEAR",
    "coefficient": "2min",
    "offset": "0min"
  }
}
```

---

## Best Practices for Maintainability Rules

### Writing Descriptions

1. **Focus on the reader** - How does this affect someone reading/modifying the code?
2. **Explain cognitive load** - What mental effort is required to understand this?
3. **Describe maintenance burden** - How does this affect future changes?
4. **Reference principles** - Mention Clean Code, SOLID, DRY where applicable

### Writing Remediation Examples

1. **Show before/after clarity** - Demonstrate improved readability
2. **Use meaningful names** - Show proper naming conventions
3. **Add appropriate comments** - Show what good documentation looks like
4. **Demonstrate extraction** - Show method/class extraction patterns

---

## Maintainability Issue Categories

### Readability Issues

**Deep Nesting:**
```json
"remediation": {
  "examples": [
    {
      "before": "if (a) {\n  if (b) {\n    if (c) {\n      if (d) {\n        doSomething();\n      }\n    }\n  }\n}",
      "after": "if (!a || !b || !c || !d) {\n  return;\n}\ndoSomething();"
    }
  ]
}
```

**Long Methods:**
```json
"remediation": {
  "examples": [
    {
      "before": "// 200-line method handling validation, processing, and formatting",
      "after": "public Result process(Input input) {\n  validate(input);\n  Data data = transform(input);\n  return format(data);\n}"
    }
  ]
}
```

### API Design Issues

**Boolean Blindness:**
```json
"remediation": {
  "examples": [
    {
      "before": "createUser(name, true, false, true);",
      "after": "createUser(name, UserOptions.builder()\n  .admin(true)\n  .verified(false)\n  .notifyOnCreate(true)\n  .build());"
    }
  ]
}
```

**Too Many Parameters:**
```json
"remediation": {
  "examples": [
    {
      "before": "void createOrder(String id, String customer, String product, int qty, double price, String address, String city, String zip, boolean express)",
      "after": "void createOrder(OrderRequest request)"
    }
  ]
}
```

### Documentation Issues

**Missing Javadoc:**
```json
"remediation": {
  "examples": [
    {
      "before": "public List<User> findUsers(String query, int limit) { ... }",
      "after": "/**\n * Searches for users matching the query.\n * @param query Search term (name or email)\n * @param limit Maximum results (1-100)\n * @return Matching users, empty list if none found\n * @throws IllegalArgumentException if limit out of range\n */\npublic List<User> findUsers(String query, int limit) { ... }"
    }
  ]
}
```

**Excessive Comments:**
```json
"remediation": {
  "examples": [
    {
      "before": "// Increment counter by 1\ncounter++;\n// Check if counter is greater than 10\nif (counter > 10) { ... }",
      "after": "counter++;\n// Reset batch when threshold exceeded to prevent memory issues\nif (counter > MAX_BATCH_SIZE) { ... }"
    }
  ]
}
```

### Naming Issues

**Inconsistent Naming:**
```json
"remediation": {
  "examples": [
    {
      "before": "String user_name;\nString userEmail;\nString UserPhone;",
      "after": "String userName;\nString userEmail;\nString userPhone;"
    }
  ]
}
```

### Architectural Issues

**Circular Dependencies:**
```json
"remediation": {
  "examples": [
    {
      "before": "// OrderService → UserService → OrderService",
      "after": "// Extract shared logic to new service\n// OrderService → SharedService ← UserService"
    }
  ]
}
```

**Hidden Dependencies:**
```json
"remediation": {
  "examples": [
    {
      "before": "void processOrder() {\n  User user = UserContext.getCurrentUser(); // Hidden!\n}",
      "after": "void processOrder(User currentUser) {\n  // Dependency is explicit\n}"
    }
  ]
}
```

---

## Common Thresholds

Use these industry-standard defaults for configurable parameters:

| Rule | Parameter | Recommended Default |
|------|-----------|---------------------|
| Long Methods | maxLines | 100 |
| Deep Nesting | maxDepth | 4 |
| Too Many Parameters | maxParams | 7 |
| Boolean Blindness | maxBooleanParams | 2 |

---

## How to Help Users with Maintainability Rules

When users ask for help:

1. **Creating a new maintainability rule**: Help identify the cognitive load impact, set appropriate severity, suggest meaningful thresholds

2. **Understanding maintainability issues**: Explain how the pattern affects code comprehension, future modifications, and team productivity

3. **Setting thresholds**: Help choose reasonable defaults based on team preferences and codebase maturity

4. **Prioritizing cleanup**: Help users decide which maintainability issues to address first based on:
   - Code change frequency (hot spots vs. stable code)
   - Team familiarity with the code
   - Upcoming planned changes

5. **Writing better examples**: Help craft before/after examples that clearly demonstrate the improvement in readability and maintainability
