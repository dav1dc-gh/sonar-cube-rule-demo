---
applyTo: "rules/code-smells/**"
---

# Code Smells Rules — Custom Instructions

You are assisting with **code smell detection rules** in the `rules/code-smells/` directory. These rules identify design and structural problems that degrade code quality, readability, and maintainability — but are not bugs or security vulnerabilities.

---

## Category Conventions

### Type & Impact

- **Type**: Always `"CODE_SMELL"`. Code smells are quality issues, not functional defects or security holes.
- **Impact softwareQuality**: Almost always `"MAINTAINABILITY"`. The one exception is `empty-catch-block`, which uses `"RELIABILITY"` because swallowing exceptions masks runtime failures.
  - Use `"RELIABILITY"` only when the smell directly risks incorrect program behavior (e.g., silent exception swallowing).
  - Use `"MAINTAINABILITY"` for all other design/structural issues.

### Severity

Code smells use a two-tier severity model:

| Severity | When to Use | Examples |
|---|---|---|
| **MAJOR** | Significant design problems that actively impede understanding, reuse, or safe modification of the code | complex-methods, duplicate-code, empty-catch-block, god-class, refused-bequest |
| **MINOR** | Lower-impact issues that reduce clarity or elegance but don't block productive work | data-clumps, dead-code, feature-envy, long-parameter-list, magic-numbers, message-chains, primitive-obsession, speculative-generality |

BLOCKER, CRITICAL, and INFO are **not used** for code smell rules.

### Impact Severity

Match impact severity to the scope and difficulty of the smell:

| Impact Severity | When to Use | Examples |
|---|---|---|
| **HIGH** | Large-scale structural problems requiring major refactoring | god-class |
| **MEDIUM** | Moderate issues requiring targeted refactoring | complex-methods, duplicate-code, empty-catch-block, primitive-obsession, refused-bequest |
| **LOW** | Localized issues fixable with simple, low-risk changes | data-clumps, dead-code, feature-envy, long-parameter-list, magic-numbers, message-chains, speculative-generality |

### Debt Model

Code smells use two debt models:

- **`CONSTANT_ISSUE`** (default, 11/13 rules): When every occurrence takes roughly the same time to fix. Use this for most smells.
- **`LINEAR`** (2/13 rules): When fix time scales with the size of the issue. Use this only when the smell's magnitude varies and directly affects remediation time.
  - `complex-methods`: coefficient `"1min"` per unit of excess complexity
  - `god-class`: coefficient `"10min"` per excess method/line

**When to choose LINEAR**: If the rule measures a quantitative metric (lines, complexity score, method count) and the fix grows proportionally, use LINEAR with an appropriate coefficient. Otherwise, default to CONSTANT_ISSUE.

**Typical offsets**: 5min–45min. Choose realistically:
- 5–10min: Simple deletions or renames (dead-code, magic-numbers)
- 15–20min: Extract method/class, introduce parameter object
- 30–45min: Major structural refactoring (god-class, duplicate-code)

### Parameters

Code smells are the **most parameterized** category. Use `params` when the rule detects threshold-based violations — this lets teams tune sensitivity to their codebase.

**Current parameterized rules:**
| Rule | Param Key | Default | What It Controls |
|---|---|---|---|
| complex-methods | `threshold` | 15 | Max cyclomatic complexity |
| god-class | `maxLines` | 500 | Max lines per class |
| god-class | `maxMethods` | 20 | Max methods per class |
| long-parameter-list | `maxParams` | 5 | Max parameters per method |
| message-chains | `maxChainLength` | 3 | Max chained method calls |

**When to add params:**
- The rule compares a measurable quantity against a threshold (complexity, count, length, depth).
- Different teams reasonably disagree on the right threshold.
- The param type is almost always `INTEGER`. Use descriptive `camelCase` key names.

**When NOT to add params:**
- The smell is binary (present or not) — e.g., dead-code, empty-catch-block.
- Adding a threshold would make the rule confusing or meaningless.

### Tags

Always include:
- `"code-smell"` — mandatory for every code smell rule

Add contextual tags from these established conventions:
- Design patterns: `design`, `refactoring`, `oop`, `solid`, `inheritance`, `lsp`, `coupling`
- Quality dimensions: `complexity`, `readability`, `maintainability`, `maintenance`
- Specific concerns: `unused`, `cleanup`, `duplication`, `dry-principle`, `error-handling`, `exceptions`, `debugging`, `law-of-demeter`, `domain-driven-design`, `yagni`, `testing`

### Code Examples

- **Language**: Always Java.
- **Before**: Show the smelly pattern in realistic, recognizable code. Include a brief comment identifying the smell.
- **After**: Show the refactored version using the recommended design improvement (extract method, introduce parameter object, remove dead code, etc.).
- Keep examples focused — demonstrate only the smell and its fix, not surrounding application logic.

---

## Existing Rules Reference

The following 13 rules exist in `rules/code-smells/`:

| File | Key | Severity | Impact Sev. | Params? | Detects |
|---|---|---|---|---|---|
| `complex-methods.json` | complex-methods | MAJOR | MEDIUM | Yes (threshold) | High cyclomatic complexity |
| `data-clumps.json` | data-clumps | MINOR | LOW | No | Variable groups appearing together repeatedly |
| `dead-code.json` | dead-code | MINOR | LOW | No | Unreachable code, unused variables/methods |
| `duplicate-code.json` | duplicate-code | MAJOR | MEDIUM | No | Code duplication |
| `empty-catch-block.json` | empty-catch-block | MAJOR | MEDIUM | No | Silent exception swallowing |
| `feature-envy.json` | feature-envy | MINOR | LOW | No | Methods using other classes more than their own |
| `god-class.json` | god-class | MAJOR | HIGH | Yes (maxLines, maxMethods) | SRP-violating oversized classes |
| `long-parameter-list.json` | long-parameter-list | MINOR | LOW | Yes (maxParams) | Methods with too many parameters |
| `magic-numbers.json` | magic-numbers | MINOR | LOW | No | Unnamed numerical constants |
| `message-chains.json` | message-chains | MINOR | LOW | Yes (maxChainLength) | Law of Demeter violations |
| `primitive-obsession.json` | primitive-obsession | MINOR | MEDIUM | No | Overuse of primitives instead of domain types |
| `refused-bequest.json` | refused-bequest | MAJOR | MEDIUM | No | Subclasses overriding inherited methods to throw/no-op |
| `speculative-generality.json` | speculative-generality | MINOR | LOW | No | Unused abstractions for hypothetical future needs |

---

## Creating a New Code Smell Rule

1. **Verify no overlap** with the 13 existing rules. Many code smells are related — ensure the new rule detects a distinct pattern.
2. **Decide if it's threshold-based**: If so, add `params` with sensible defaults. Study existing defaults for calibration.
3. **Choose CONSTANT_ISSUE or LINEAR debt**: If the smell's remediation time scales with a measurable quantity, use LINEAR with a coefficient. Otherwise, CONSTANT_ISSUE.
4. **Distinguish from bugs**: If the pattern causes *incorrect behavior* at runtime, it might belong in `performance/` (as BUG) or might use RELIABILITY impact. Pure design/quality issues stay as MAINTAINABILITY.
5. **Reference established design principles**: When applicable, tag with `solid`, `dry-principle`, `law-of-demeter`, `yagni`, etc.

### Template

```json
{
  "key": "new-code-smell",
  "name": "New Code Smell Name",
  "description": "Detects <pattern> which makes code harder to <understand|maintain|change|test>.",
  "severity": "MINOR",
  "type": "CODE_SMELL",
  "tags": ["code-smell", "<specific-tag>"],
  "remediation": {
    "constantCost": "15min",
    "examples": [
      {
        "before": "// Bad: <explain the smell>\n<smelly Java code>",
        "after": "// Good: <explain the improvement>\n<refactored Java code>"
      }
    ]
  },
  "impacts": [
    {
      "softwareQuality": "MAINTAINABILITY",
      "severity": "LOW"
    }
  ],
  "defaultSeverity": "MINOR",
  "status": "READY",
  "debt": {
    "function": "CONSTANT_ISSUE",
    "offset": "15min"
  }
}
```

### Template with Parameters

```json
{
  "key": "new-threshold-smell",
  "name": "New Threshold-Based Smell",
  "description": "Detects <metric> exceeding <threshold>, which indicates <problem>.",
  "severity": "MAJOR",
  "type": "CODE_SMELL",
  "tags": ["code-smell", "complexity", "<specific-tag>"],
  "remediation": {
    "constantCost": "30min",
    "examples": [
      {
        "before": "// Bad: <metric> exceeds threshold\n<example>",
        "after": "// Good: refactored to reduce <metric>\n<fixed example>"
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
    "function": "LINEAR",
    "offset": "10min",
    "coefficient": "5min"
  },
  "params": [
    {
      "key": "maxThreshold",
      "name": "Maximum Allowed Threshold",
      "description": "The maximum value of <metric> before the rule triggers",
      "defaultValue": "10",
      "type": "INTEGER"
    }
  ]
}
```

---

## Common Mistakes to Avoid

- **Don't use `VULNERABILITY` or `BUG` type** — code smells are always `CODE_SMELL`.
- **Don't set severity to BLOCKER or CRITICAL** — those are reserved for security and critical bugs.
- **Don't add params for binary smells** — dead-code is either dead or not; a threshold makes no sense.
- **Don't confuse feature-envy with shotgun-surgery** — feature-envy is in code-smells (a method using another class too much); shotgun-surgery is in maintainability (a change requiring edits everywhere).
- **Don't forget to match `severity` and `defaultSeverity`**.
- **Don't use LINEAR debt without a coefficient** — if the debt function is LINEAR, you must specify what the time scales with.
