---
name: sonarcube-ci-pipeline
description: Manages the GitHub Actions CI workflow that validates SonarQube rule definitions on every push and pull request. Use when troubleshooting CI failures, modifying the pipeline, understanding why a PR was rejected, or extending the validation workflow. Keywords: sonarqube, sonar, ci, cd, github-actions, workflow, pipeline, validate, pr, pull-request, push, automation, continuous-integration, strict, formatting.
---

# SonarQube CI Pipeline

## Purpose

This skill manages the GitHub Actions workflow at `.github/workflows/validate-rules.yml` that automatically validates all SonarQube rule definition files on every push and pull request. It covers how the pipeline works, how to troubleshoot failures, and how to extend it.

Activate this skill whenever the user:
- Asks why a PR or push failed CI checks
- Wants to understand the validation pipeline
- Needs to troubleshoot a GitHub Actions failure
- Wants to modify or extend the CI workflow
- Asks about automated validation or quality gates

---

## Workflow Overview

**File:** `.github/workflows/validate-rules.yml`

### Triggers

The workflow runs on:
- **Push to `main`** — when files in `rules/**/*.json`, `scripts/validate-rules.py`, or `rules/schema/**` change
- **Pull requests to `main`** — same path filters
- **Manual dispatch** — can be triggered manually via Actions tab (`workflow_dispatch`)

### Jobs

The workflow runs a single job (`validate`) with three steps:

#### Step 1: Standard Validation
```bash
python3 scripts/validate-rules.py
```
Runs all checks. Fails if any rule file has **errors**.

#### Step 2: Strict Validation
```bash
python3 scripts/validate-rules.py --strict
```
Runs all checks with warnings treated as errors. Fails if any rule file has **errors OR warnings**.

#### Step 3: Formatting Check
Verifies every rule JSON file is formatted with 2-space indentation by comparing the file content to Python's `json.dumps(data, indent=2)` output. Reports formatting deviations as GitHub Actions warnings.

---

## Troubleshooting CI Failures

### "Validate all rule files" step failed

**Cause:** One or more rule files have **errors** (missing fields, invalid enums, key mismatches, etc.)

**How to fix:**
1. Read the step's output log to find which files failed and what errors occurred
2. Run locally to reproduce: `python3 scripts/validate-rules.py`
3. Fix the errors in the reported files
4. Push the fix

### "Strict validation" step failed

**Cause:** One or more rule files have **warnings** (e.g. severity↔defaultSeverity mismatch, type↔impact misalignment)

**How to fix:**
1. Run locally: `python3 scripts/validate-rules.py --strict`
2. Warnings are listed under "### Warnings (should fix)" for each file
3. Fix all warnings — in strict mode they are treated as errors
4. Push the fix

### "Verify JSON formatting" step shows warnings

**Cause:** A rule file is not formatted with consistent 2-space indentation.

**How to fix:**
```bash
python3 -c "import json; d=json.load(open('<file>')); open('<file>','w').write(json.dumps(d, indent=2, ensure_ascii=False)+'\n')"
```

Replace `<file>` with the path shown in the warning.

### Workflow didn't trigger

**Possible causes:**
- The changed files don't match the path filters (`rules/**/*.json`, `scripts/validate-rules.py`, `rules/schema/**`)
- The branch is not `main` and it's not a PR targeting `main`
- GitHub Actions is disabled for the repository

**Fix:** If you need to validate non-matching paths, use the manual trigger (Actions tab → "Validate SonarQube Rules" → "Run workflow").

---

## Workflow File Reference

```yaml
name: Validate SonarQube Rules

on:
  push:
    branches: [main]
    paths:
      - 'rules/**/*.json'
      - 'scripts/validate-rules.py'
      - 'rules/schema/**'
  pull_request:
    branches: [main]
    paths:
      - 'rules/**/*.json'
      - 'scripts/validate-rules.py'
      - 'rules/schema/**'
  workflow_dispatch:

jobs:
  validate:
    name: Lint & Validate Rule Definitions
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: '3.12'
      - run: python3 scripts/validate-rules.py
      - run: python3 scripts/validate-rules.py --strict
      - name: Verify JSON formatting
        run: |
          # Compares each file against json.dumps(indent=2) output
          ...
```

---

## Extending the Pipeline

### Adding a new validation step

Add a new step to the `validate` job in `.github/workflows/validate-rules.yml`:

```yaml
      - name: My new check
        run: |
          # Your validation command here
```

### Adding path triggers

To trigger on additional file changes, add paths to the `paths` arrays:

```yaml
    paths:
      - 'rules/**/*.json'
      - 'scripts/validate-rules.py'
      - 'rules/schema/**'
      - 'your/new/path/**'        # ← add here
```

### Adding branch protection

For maximum safety, configure branch protection rules in GitHub:
1. Go to Settings → Branches → Add rule for `main`
2. Enable "Require status checks to pass before merging"
3. Select the "Lint & Validate Rule Definitions" check
4. Enable "Require branches to be up to date before merging"

This prevents any rule file changes from reaching `main` without passing validation.

### Adding notifications

To notify on failure, add a notification step:

```yaml
      - name: Notify on failure
        if: failure()
        uses: actions/github-script@v7
        with:
          script: |
            github.rest.issues.createComment({
              owner: context.repo.owner,
              repo: context.repo.repo,
              issue_number: context.issue.number,
              body: '❌ Rule validation failed. Please check the Actions log.'
            })
```

---

## Important Notes

- The pipeline uses **Python 3.12** and has **zero pip dependencies** — no package installation step is needed.
- Both standard and strict validation run on every PR. A PR must pass both to merge (if branch protection is enabled).
- The formatting check produces **warnings** (not errors) — it won't block merging but will surface formatting inconsistencies.
- Manual dispatch (`workflow_dispatch`) validates the entire rule set regardless of what files changed. Use it for periodic audits.
- The pipeline only runs when relevant files change. Changes to `README.md`, `CONTRIBUTING.md`, etc. do not trigger it.
