---
name: custom-instructions-sync
description: Synchronize all copilot-instructions.md files with the current state of rule files. Use when rules have been added, removed, or modified and instructions need updating.
---

# Custom Instructions Sync

Follow this process to detect and fix drift between the actual rule files and the documented `.copilot-instructions.md` files.

## Step 1 — Detect drift

Run the drift detection script to get a structured diff:

```bash
node .github/skills/custom-instructions-sync/detect-drift.js
```

This outputs a JSON report showing, for each category:
- **added**: Rules that exist as files but are not mentioned in the instructions
- **removed**: Rules mentioned in the instructions but no longer exist as files
- **changed**: Rules whose severity, type, or other key metadata has changed

## Step 2 — Assess the scope

Review the drift report and determine what needs updating:

1. **Path-specific instructions** (`rules/<category>/.copilot-instructions.md`) — These contain rule inventory tables and category-specific conventions. Update them if rules were added, removed, or had severity/type changes.
2. **Root instructions** (`.github/copilot-instructions.md`) — This contains overall rule counts and category summaries. Update it if total rule counts changed.

## Step 3 — Update path-specific instructions

For each category with drift:

1. Read the current `.copilot-instructions.md` file for that category.
2. Update the rule inventory table to reflect current files:
   - Add rows for new rules with their key, severity, type, and notes.
   - Remove rows for deleted rules.
   - Update metadata for changed rules.
3. Update the rule count in the header/summary.
4. Preserve all other content (conventions, pitfalls, cost calibration) unless the changes require adjusting those sections too.

## Step 4 — Update root instructions

If the total rule count or category counts changed:

1. Read `.github/copilot-instructions.md`.
2. Update the category listing (e.g., "15 rules" → "16 rules" for security).
3. Update the total rule count if mentioned.

## Step 5 — Validate

Run validation to confirm changes didn't break anything:

```bash
node scripts/validate-rules.js --verbose
```

## Step 6 — Record lessons learned

Append a dated entry to `HISTORY.md` documenting:
- Which instruction files were updated and why
- How many rules were added/removed/changed
- Any convention changes that were necessary
