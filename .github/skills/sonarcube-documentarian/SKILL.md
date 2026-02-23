---
name: sonarcube-documentarian
description: Keeps repository documentation (README.md, CONTRIBUTING.md, and any supplementary docs) accurate, up-to-date, and well-formatted by auditing doc content against the actual rule files on disk. Use when rule counts are wrong, file listings are stale, descriptions are missing or inaccurate, or after adding/removing/renaming rules. Keywords: sonarqube, sonar, documentation, docs, readme, contributing, update, sync, audit, drift, counts, listing, description, format, markdown, current, stale, category.
---

# SonarQube Documentarian

## Purpose

This skill keeps every documentation file in the repository accurate and well-formatted. It treats the rule files on disk as the source of truth and updates `README.md`, `CONTRIBUTING.md`, and any other docs to match reality.

Activate this skill whenever the user:
- Asks to update, refresh, or sync the documentation
- Notices that rule counts or file listings in the README are wrong
- Has just added, removed, or renamed one or more rule files
- Wants to add a description for a new rule in the README
- Asks to audit documentation for staleness or drift
- Wants to improve the formatting or clarity of any doc file
- Asks what documentation needs updating after a bulk operation

---

## Key Documentation Files

| File | Purpose | What can drift |
|---|---|---|
| `README.md` | Project overview, directory structure, category summaries | Rule counts, file listings in the directory tree, category rule-by-rule descriptions |
| `CONTRIBUTING.md` | Contributor guide, field reference, category table | Category table rows, field constraint tables, example code |

---

## Step 1: Audit — Discover Documentation Drift

Before making any changes, collect the ground truth from the filesystem.

### 1a. Get accurate counts per category

```bash
for dir in rules/*/; do
  [[ "$dir" == "rules/schema/" ]] && continue
  count=$(find "$dir" -maxdepth 1 -name '*.json' | wc -l | tr -d ' ')
  echo "$dir → $count rules"
done
```

### 1b. List all rule files per category

```bash
for dir in rules/*/; do
  [[ "$dir" == "rules/schema/" ]] && continue
  echo "=== $dir ==="
  find "$dir" -maxdepth 1 -name '*.json' | sort | xargs -I{} basename {} .json
done
```

### 1c. Extract the `name` and `description` for each rule

This is the canonical source for README category descriptions:

```bash
# For a single category (e.g. security):
for f in rules/security/*.json; do
  echo "$(jq -r '.name' "$f"): $(jq -r '.description' "$f")"
done

# For all categories:
find rules -name '*.json' -not -path 'rules/schema/*' -print0 | sort -z | \
  xargs -0 -I{} sh -c 'echo "$(jq -r .name {}): $(jq -r .description {})"'
```

### 1d. Compare against existing README entries

After collecting the ground-truth data, compare it with the current README content:

- **Count mismatch** — README says "N rules" but `find` returns a different number
- **Missing file entry** — a `.json` file exists but has no entry in the README directory tree or description list
- **Stale file entry** — the README lists a file that no longer exists on disk
- **Stale description** — the README description doesn't match the rule's current `description` field
- **Missing description** — a rule has no bullet point in the README category section

---

## Step 2: Update `README.md`

### 2a. Directory Structure Section

The `## Directory Structure` code block lists every rule file per category with the count in the category comment. Update it to exactly match the filesystem:

**Format per category:**
```
├── <category>/          # <Category display name> (<N> rules)
│   ├── <rule-key-1>.json
│   ├── <rule-key-2>.json
│   └── <rule-key-N>.json
```

Rules:
- Files must be listed in **alphabetical order** within each category
- The comment must show the **exact current count** (e.g. `# Security rules (22 rules)`)
- `schema/` is excluded from directory structure (it is not a rule category)
- The last file in each category uses `└──`; all others use `├──`

### 2b. Rule Categories Section

Each category has a heading like `### Security (N rules)` followed by a bullet list:

```markdown
### Security (22 rules)
- **Rule Name**: One-sentence description taken directly from the rule's `description` field.
- **Another Rule**: Its description.
```

Rules:
- Update the heading count to the current number of rules in that category
- Add a bullet for every new rule file, using `name` from JSON as the bold label and the first sentence of `description` as the text
- Remove bullets for rules that no longer exist on disk
- Keep bullets in **alphabetical order** by rule name
- Descriptions should be **trimmed to one sentence** if the JSON `description` field contains more than one

### 2c. Counts elsewhere in README

Search for any other references to rule counts (e.g. in the `## Overview` paragraph) and update them to match:

```bash
grep -n '\brules\b' README.md | grep -E '[0-9]+'
```

---

## Step 3: Update `CONTRIBUTING.md`

### 3a. Category Table

The `### Choosing the Right Category` table must list all current categories. If a category was added or removed, update the table:

| Rule Type | Impact Focus | Directory |
|---|---|---|
| `CODE_SMELL` | General quality | `code-smells/` |
| `CODE_SMELL` | Maintainability | `maintainability/` |
| `CODE_SMELL` / `BUG` | Performance | `performance/` |
| `VULNERABILITY` / `SECURITY_HOTSPOT` | Security | `security/` |

If new categories are added, add a row. If categories are renamed or removed, update/delete the row accordingly.

### 3b. Field Reference Tables

The schema reference tables in `CONTRIBUTING.md` must stay in sync with the JSON Schema at `rules/schema/sonarqube-rule.schema.json`. When the schema changes, update:
- The **Required Fields** table (field names, types, constraints)
- The **Common Mistakes** table (add any new cross-field rules)

---

## Step 4: Format and Style

Apply these formatting conventions to all documentation files:

### Markdown Formatting

| Rule | Detail |
|---|---|
| Headings | Use ATX-style (`##`), one blank line before and after |
| Tables | Pipe-delimited, aligned with spaces, header separator row uses `---` |
| Code blocks | Fenced with triple backticks and a language tag (`bash`, `json`, `markdown`) |
| Bullet lists | Hyphen (`-`) leaders with a space; one blank line before and after the list block |
| File paths | Inline code (backticks) for paths and filenames |
| Bold labels | Rule names in category descriptions are bold (`**Name**`) |
| Line endings | Unix LF only, no trailing whitespace, file ends with single newline |

### Tone and Style

- Descriptions should be **factual and concise** — one sentence max per rule entry in the README
- Avoid marketing language ("powerful", "comprehensive", "easy to use")
- Use present tense ("Detects…", "Identifies…", "Flags…")
- Category headings use Title Case
- Rule names quoted from JSON must match the `name` field exactly (Title Case)

---

## Step 5: Validate Documentation Completeness

After updating, verify nothing was missed:

### Coverage check — every rule file has a README description

```bash
# List all rule keys from files
find rules -name '*.json' -not -path 'rules/schema/*' | \
  xargs -I{} basename {} .json | sort > /tmp/rule-keys-on-disk.txt

# List all bold-label entries in README (assumes format: - **Name**: ...)
grep -oP '(?<=\*\*)[^*]+(?=\*\*)' README.md | sort > /tmp/rule-names-in-readme.txt

echo "Rules on disk: $(wc -l < /tmp/rule-keys-on-disk.txt)"
echo "Descriptions in README: $(wc -l < /tmp/rule-names-in-readme.txt)"
```

Note: the above compares keys vs names; manual cross-check may be needed for renamed rules.

### Cross-reference check — counts are self-consistent

```bash
# Counts from headings vs counts from bullet lists
grep -E '^### .* \([0-9]+ rules\)' README.md
# Manually verify that the count in each heading equals the bullets that follow
```

---

## Common Documentation Drift Scenarios

| Scenario | Symptom | Fix |
|---|---|---|
| New rule added | Count N+1, one missing bullet and file listing | Add file to directory tree, add bullet to category section, increment count in heading |
| Rule removed | Count N-1, one stale bullet and file listing | Remove file from directory tree, remove bullet, decrement count |
| Rule renamed | Stale filename in tree, stale name in bullet list | Update filename in tree, update bold label in bullet |
| Rule re-categorised | File under wrong category in tree; described under wrong heading | Move entry in tree, move bullet to correct heading |
| Description updated in JSON | README bullet text is outdated | Re-extract description from JSON and update bullet |
| New category added | Category missing from README and CONTRIBUTING | Add section to both files |

---

## Workflow Summary

```
1. Run disk audit commands (Step 1) → collect ground truth
2. Diff against README.md (Step 1d) → identify exactly what has drifted
3. Update README directory structure section (Step 2a)
4. Update README category descriptions (Step 2b)
5. Update any inline count references (Step 2c)
6. Update CONTRIBUTING.md category table if needed (Step 3a)
7. Check CONTRIBUTING.md field tables if schema changed (Step 3b)
8. Apply formatting fixes (Step 4)
9. Run coverage check (Step 5) to confirm nothing was missed
10. Report a summary of all changes made
```

---

## Example: Adding a Single New Rule

Rule `rules/security/timing-attack.json` was added. The documentarian should:

1. **Audit:**
   ```bash
   find rules/security -name '*.json' | wc -l   # e.g. returns 22
   jq -r '.name, .description' rules/security/timing-attack.json
   ```

2. **Update README directory tree** — insert `timing-attack.json` in alphabetical order under `security/`, update comment to `(22 rules)`

3. **Update README description list** — add:
   ```markdown
   - **Timing Attack**: Detects code patterns susceptible to timing-based side-channel attacks where execution time reveals sensitive information.
   ```
   in alphabetical order under `### Security (22 rules)`, then update the heading count.

4. **No CONTRIBUTING.md change needed** (no new category, no schema change).

5. **Coverage check** — confirm all 22 security files have bullets in the README.

---

## Important Notes

- The **rule files are always the source of truth**. If a rule file and the README disagree, the README is wrong.
- Never modify rule JSON files to fix documentation — edit the docs to match the rules.
- When descriptions are long (>1 sentence), use only the first sentence in README bullets for brevity.
- Always run the validation script after any documentation work to ensure no accidental JSON edits were made:
  ```bash
  python3 scripts/validate-rules.py
  ```
- The `rules/schema/` directory is **not a rule category** and must never appear in rule count totals or category listings.
