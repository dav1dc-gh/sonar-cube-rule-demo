---
name: data-quality-audit
description: Audit all SonarQube rule files for consistency issues, duplicates, and drift. Use when asked to audit, check quality, find duplicates, or review rule consistency.
---

# Data Quality Audit

Follow this process to audit all rule files for quality and consistency issues.

## Step 1 — Run the audit script

Execute the bundled audit script to collect structured findings:

```bash
node .github/skills/data-quality-audit/audit-rules.js
```

This outputs a JSON report with `errors`, `warnings`, and `suggestions` arrays.

## Step 2 — Run schema validation

Also run the standard validator to catch schema-level issues:

```bash
node scripts/validate-rules.js --verbose
```

## Step 3 — Interpret findings

The audit script checks for:

### Errors (must fix)
- Schema violations detected by the validator
- `severity` ≠ `defaultSeverity`
- `remediation.constantCost` ≠ `debt.offset` (for CONSTANT_ISSUE rules)
- Missing required fields

### Warnings (should fix)
- **Near-duplicate rules**: Rules with similar names or descriptions across categories (e.g., `long-parameter-list` vs `too-many-parameters`)
- **Impact misclassifications**: Performance rules with `softwareQuality: "MAINTAINABILITY"` that should arguably be `"RELIABILITY"`
- **Tag inconsistencies**: First tag not matching directory name, tag count ≠ 4
- **Cross-category tag leakage**: Tags from another category without justification

### Suggestions (consider)
- **Remediation cost outliers**: Rules of similar severity with very different `constantCost` values (>2× the median for that severity)
- **Missing parameters**: Rules that describe thresholds in their description but have no `params` array
- **Thin descriptions**: Descriptions under 50 characters

## Step 4 — Present the report

Format findings as a categorized Markdown report:

```markdown
## Audit Report — <date>

### ❌ Errors (<count>)
- [file](path): description

### ⚠️ Warnings (<count>)
- [file](path): description

### 💡 Suggestions (<count>)
- [file](path): description

### ✅ Summary
N rules checked, X errors, Y warnings, Z suggestions
```

Include direct file paths so the user can navigate to each issue.

## Step 5 — Offer to fix (if appropriate)

If this skill is used by an agent with edit permissions, offer to fix each issue with user confirmation. If the agent is read-only, explicitly state: "Switch to the repo-maintainer agent to apply fixes."

## Step 6 — Record lessons learned

Append a dated entry to `HISTORY.md` documenting:
- How many issues were found across each category
- Any patterns observed (e.g., "performance rules consistently mis-classify impacts")
- Whether findings were fixed or deferred
