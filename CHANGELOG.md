# Changelog

All notable changes to the SonarQube rules in this repository will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- JSON Schema for rule validation (`schemas/rule-schema.json`)
- Validation script (`scripts/validate-rules.sh`)
- Index generation script (`scripts/generate-index.sh`)
- GitHub Actions workflow for CI validation
- This CHANGELOG file

## [1.0.0] - 2026-01-12

### Added

#### Security Rules (15 rules)
- `command-injection` - OS command injection via user input
- `csrf-vulnerability` - Missing CSRF protection
- `hardcoded-credentials` - Hardcoded passwords and API keys
- `insecure-cookie` - Cookies missing security flags
- `insecure-deserialization` - Unsafe deserialization of untrusted data
- `insecure-random` - Predictable random number generators
- `ldap-injection` - User input in LDAP queries
- `open-redirect` - User-controlled redirect URLs
- `path-traversal` - Directory traversal vulnerabilities
- `sensitive-data-exposure` - Logging of sensitive information
- `server-side-request-forgery` - SSRF vulnerabilities
- `sql-injection` - SQL injection prevention
- `weak-cryptography` - Weak cryptographic algorithms
- `xml-external-entity` - XXE vulnerabilities
- `xss-vulnerability` - Cross-site scripting risks

#### Code Smells Rules (13 rules)
- `complex-methods` - High cyclomatic complexity
- `data-clumps` - Variable groups appearing together
- `dead-code` - Unreachable or unused code
- `duplicate-code` - Code duplication
- `empty-catch-block` - Silent exception swallowing
- `feature-envy` - Methods using features from other classes
- `god-class` - Classes with too many responsibilities
- `long-parameter-list` - Too many method parameters
- `magic-numbers` - Unnamed numerical constants
- `message-chains` - Long method call chains
- `primitive-obsession` - Overuse of primitives
- `refused-bequest` - Subclasses overriding to do nothing
- `speculative-generality` - Unused abstractions

#### Performance Rules (12 rules)
- `connection-pool-exhaustion` - Unreturned connections
- `excessive-object-creation` - Unnecessary allocations
- `inefficient-collection-usage` - Improper collection use
- `inefficient-loops` - Loop performance anti-patterns
- `memory-leaks` - Resource leaks
- `missing-lazy-initialization` - Eager initialization
- `n-plus-one-query` - Database queries in loops
- `string-concatenation-in-loop` - String + in loops
- `synchronous-io-in-async` - Blocking I/O in async
- `unbounded-collection-growth` - Collections without eviction
- `unnecessary-boxing` - Unnecessary type conversions
- `unoptimized-regex` - Regex performance issues

#### Maintainability Rules (12 rules)
- `boolean-blindness` - Multiple boolean parameters
- `circular-dependencies` - Circular module dependencies
- `deep-nesting` - Excessive nesting levels
- `excessive-comments` - Redundant comments
- `hardcoded-urls` - URLs that should be externalized
- `hidden-dependencies` - Non-explicit dependencies
- `inconsistent-naming` - Naming convention violations
- `long-methods` - Methods exceeding length thresholds
- `missing-javadoc` - Missing API documentation
- `missing-null-check` - Potential null pointer issues
- `shotgun-surgery` - Changes requiring many modifications
- `too-many-parameters` - Excessive parameter counts

---

## Template for Future Entries

```markdown
## [X.Y.Z] - YYYY-MM-DD

### Added
- New rule descriptions

### Changed
- Modified rule descriptions

### Deprecated
- Rules marked for removal

### Removed
- Deleted rules

### Fixed
- Bug fixes in rules

### Security
- Security-related changes
```
