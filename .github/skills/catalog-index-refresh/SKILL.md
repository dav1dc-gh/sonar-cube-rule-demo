---
name: catalog-index-refresh
description: Regenerate the rules catalog and machine-readable index. Use when asked to update the catalog, refresh documentation, or generate an index.
---

# Catalog & Index Refresh

Follow this process to regenerate all derived documentation and machine-readable artifacts from the rule source files.

## Step 1 — Validate first

Before regenerating artifacts, confirm all rules are valid:

```bash
node scripts/validate-rules.js --verbose
```

If validation fails, fix the issues before proceeding. Invalid rules should not be published to the catalog.

## Step 2 — Regenerate the Markdown catalog

```bash
node scripts/generate-catalog.js
```

This updates `RULES_CATALOG.md` with:
- Summary table showing rules per category by severity
- Full rule table with links to each JSON file
- Per-rule detail sections with description, tags, remediation examples

## Step 3 — Regenerate the machine-readable index

```bash
node .github/skills/catalog-index-refresh/generate-index.js
```

This creates/updates `rules/index.json` — a flat JSON array of all rule metadata that tooling can consume without globbing the filesystem.

The index contains for each rule:
- `key`, `name`, `category`, `severity`, `type`
- `tags`, `status`, `paramCount`, `remediationCost`

## Step 4 — Review the diff

After regeneration, review what changed:

1. Check `git diff RULES_CATALOG.md` to see new, removed, or modified rules in the catalog.
2. Check `git diff rules/index.json` to see the same in machine-readable form.
3. Summarize changes for the user: e.g., "Added 2 new rules, updated severity for 1 rule."

## Step 5 — Record lessons learned

Append a dated entry to `HISTORY.md` documenting:
- How many rules are now in the catalog
- What changed since the last refresh
- Any anomalies noticed during regeneration
