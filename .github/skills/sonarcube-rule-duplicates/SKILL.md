---
name: sonarcube-rule-duplicates
description: Detect overlapping, conflicting, or duplicate SonarQube rule definitions across categories. Identifies rules with identical keys, similar descriptions, overlapping detection scope, or redundant coverage. Use when auditing for duplicates, resolving conflicts, merging rules, or cleaning up redundancy. Keywords: sonarqube, sonar, duplicate, overlap, conflict, merge, deduplicate, redundant, similar, category, cross-reference, audit, cleanup.
---

# SonarQube Rule Duplicates Detector

## Purpose

This skill identifies duplicate, overlapping, or conflicting rule definitions across the `rules/` directory hierarchy. It detects issues that degrade quality profile reliability—such as the same concern covered by multiple rules in different categories, identical keys, or rules with near-identical detection scope that confuse users.

Activate this skill whenever the user:
- Asks to find duplicate or overlapping rules
- Wants to audit cross-category consistency
- Notices the same rule key or concept in multiple directories
- Asks to merge, consolidate, or deduplicate rules
- Requests a conflict or redundancy report

---

## Detection Checks

Perform all checks below and report every finding with severity and recommended action.

### 1. Exact Key Duplicates (ERROR)

Scan all `rules/**/*.json` files. If two or more files produce the same `key` value, report as an error—keys must be globally unique.

**Example:** `rules/performance/race-condition.json` and `rules/maintainability/race-condition.json` both have `"key": "race-condition"`.

**Resolution options:**
- Rename one rule with a disambiguating prefix (e.g., `perf-race-condition`, `maint-race-condition`)
- Merge into a single rule in the most appropriate category and delete the other
- Keep one and deprecate the other (`"status": "DEPRECATED"`)

### 2. Near-Duplicate Descriptions (WARNING)

Compare `description` fields across all rules using semantic similarity. Flag pairs where:
- Descriptions share >70% of significant words (excluding stop words)
- Both rules target the same programming concept but from different angles

**Report format:**
```
WARNING: Near-duplicate descriptions
  → rules/code-smells/long-parameter-list.json
  → rules/maintainability/too-many-parameters.json
  Similarity: Both detect methods with excessive parameters
  Suggestion: Merge into one rule or differentiate scope clearly
```

### 3. Overlapping Tags Without Differentiation (WARNING)

If two rules share ≥80% of their tags AND have the same `type`, flag as potentially redundant.

### 4. Same Concept, Different Categories (INFO)

Identify rules that address the same underlying concern but are placed in different categories. This is acceptable if each emphasizes a distinct impact (e.g., performance vs. correctness), but should be explicitly cross-referenced via tags.

**Check:** If rule names or keys share a common stem (e.g., `race-condition` in two dirs), verify they have different `impacts[].softwareQuality` values and cross-reference each other in `tags`.

### 5. Deprecated Rule Still Has Active Duplicate (WARNING)

If a rule with `"status": "DEPRECATED"` exists alongside an active rule covering the same concern, flag it—deprecated rules should be removed or clearly documented as superseded.

---

## Output Format

Present findings grouped by severity:

```
## Duplicate/Overlap Audit Results

### ERRORS (must fix)
1. **Exact key duplicate**: `race-condition`
   - rules/performance/race-condition.json
   - rules/maintainability/race-condition.json
   - Action: Rename or merge

### WARNINGS (should fix)
1. **Near-duplicate scope**: `long-parameter-list` ↔ `too-many-parameters`
   - Both detect excessive method parameters
   - Action: Merge or differentiate descriptions

### INFO (review)
1. **Cross-category concept**: `race-condition` exists in performance/ and maintainability/
   - Performance version focuses on runtime contention
   - Maintainability version focuses on code structure
   - Action: Add cross-reference tags if intentional
```

---

## Resolution Strategies

When the user asks to resolve a duplicate, offer these strategies:

### Merge
1. Pick the category that best fits the primary concern
2. Combine the best `description`, `remediation.examples`, and `tags` from both files
3. Keep the more established `key` (the one likely already in quality profiles)
4. Delete the redundant file
5. Update README.md

### Rename to Differentiate
1. Add a category-specific prefix or qualifier to the key
2. Update the filename to match the new key
3. Ensure `description` clearly states the unique angle this rule covers
4. Add cross-reference tags pointing to the related rule

### Deprecate
1. Set `"status": "DEPRECATED"` on the superseded rule
2. Add a note in `description` indicating which rule supersedes it
3. Keep the file for backward compatibility with existing quality profiles

---

## Execution Steps

When invoked:

1. **Scan** — Read all `rules/**/*.json` files, parse JSON, extract `key`, `name`, `description`, `type`, `tags`, `impacts`, `status`
2. **Check duplicates** — Run all 5 detection checks above
3. **Report** — Present findings in the output format above
4. **Recommend** — For each finding, suggest the most appropriate resolution strategy
5. **Act** — If the user confirms a resolution, execute it (rename/merge/deprecate) and validate the result

---

## Known Issues in This Repository

Maintain awareness of these known overlaps (update as resolved):

- `race-condition` exists in both `rules/performance/` and `rules/maintainability/`
- `long-parameter-list` (code-smells) and `too-many-parameters` (maintainability) cover similar scope
