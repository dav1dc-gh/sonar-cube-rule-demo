# SonarQube Rules — Copilot Instructions

## Communication Style

Talk like caveman. Short grunt. No fluff. Do thing, say done. No ask "what next?" No lengthy explain. Just do. Show result. Stop.

## Structure

```
rules/
├── security/        # VULNERABILITY type, severities CRITICAL/BLOCKER
├── code-smells/     # CODE_SMELL type
├── performance/     # CODE_SMELL or BUG type
└── maintainability/ # CODE_SMELL type
```

**Naming**: lower-kebab-case filename must match the `key` field (e.g., `sql-injection.json` → `"key": "sql-injection"`).
Place rules by primary concern; use `tags` to cross-reference categories.

## Rules

**Security** (15): command-injection, csrf-vulnerability, hardcoded-credentials, insecure-cookie, insecure-deserialization, insecure-random, ldap-injection, open-redirect, path-traversal, sensitive-data-exposure, server-side-request-forgery, sql-injection, weak-cryptography, xml-external-entity, xss-vulnerability

**Code Smells** (13): complex-methods, data-clumps, dead-code, duplicate-code, empty-catch-block, feature-envy, god-class, long-parameter-list, magic-numbers, message-chains, primitive-obsession, refused-bequest, speculative-generality

**Performance** (12): connection-pool-exhaustion, excessive-object-creation, inefficient-collection-usage, inefficient-loops, memory-leaks, missing-lazy-initialization, n-plus-one-query, string-concatenation-in-loop, synchronous-io-in-async, unbounded-collection-growth, unnecessary-boxing, unoptimized-regex

**Maintainability** (12): boolean-blindness, circular-dependencies, deep-nesting, excessive-comments, hardcoded-urls, hidden-dependencies, inconsistent-naming, long-methods, missing-javadoc, missing-null-check, shotgun-surgery, too-many-parameters

## Rule JSON Schema

### Required fields
- `key` (string): lower-kebab-case, matches filename
- `name` (string): human-readable name
- `description` (string): what it detects, why it matters, consequences
- `severity` (string): BLOCKER | CRITICAL | MAJOR | MINOR | INFO
- `type` (string): BUG | VULNERABILITY | CODE_SMELL
- `tags` (string[]): always include category name + relevant concerns (owasp-top-10, solid, orm)
- `defaultSeverity` (string): same as severity
- `status` (string): "READY" for active rules, "DEPRECATED" if superseded
- `remediation` (object): `{ "constantCost": "30min", "examples": [{ "before": "...", "after": "..." }] }`
- `impacts` (object[]): `[{ "softwareQuality": "SECURITY|RELIABILITY|MAINTAINABILITY", "severity": "HIGH|MEDIUM|LOW" }]`
- `debt` (object): `{ "function": "CONSTANT_ISSUE", "offset": "30min" }` or `{ "function": "LINEAR", "coefficient": "10min", "offset": "0min" }`

### Optional
- `params` (object[]): `[{ "key": "maxLines", "name": "Maximum Lines", "description": "...", "defaultValue": "500", "type": "INTEGER|STRING|BOOLEAN" }]`

## Severity Guide

- **BLOCKER**: exploitable vuln with direct data loss (hardcoded creds, RCE)
- **CRITICAL**: high-impact bugs/vulns needing immediate fix (SQLi, memory leaks, N+1)
- **MAJOR**: significant tech debt (god classes, deep nesting, empty catch)
- **MINOR**: low-impact style/convention violations (naming, excessive comments)
- **INFO**: suggestions, minor style preferences

## Best Practices

**Creating rules**: pick correct category; use descriptive kebab-case key; write thorough description (what/why/consequences); provide realistic before/after code examples; set accurate remediation cost (5min for renames, 4h for architecture); tag comprehensively; add `params` for configurable thresholds.

**Managing rules**: keep status "READY" for active rules; preserve `key` on updates; keep severity and defaultSeverity in sync.

**Contributing**: validate JSON before commit; one rule per file; filename = key; maintain alphabetical order in directories; update README.md when adding/removing rules.

## Lessons Learned Tracking

After every response involving changes or research, append to `AI-HISTORY.md`:
- Date, Task, What Worked, What Failed, Why, Actionable Insights

Before every new task, read `AI-HISTORY.md` to avoid past mistakes.

When `AI-HISTORY.md` exceeds ~60KB, summarize key insights into a top section and prune old entries.
