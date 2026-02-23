## Task

Create a GitHub Actions workflow that automatically validates all SonarQube rule definition JSON files in this repository whenever changes are pushed or a pull request is opened.

---

## File to Create

Create the workflow file at: `.github/workflows/validate-rules.yml`

---

## Workflow Triggers

The workflow must run on:
- `push` to the `main` branch (only when files under `rules/` change)
- `pull_request` targeting the `main` branch (only when files under `rules/` change)

Use path filters so the workflow only triggers on changes to `rules/**/*.json`.

---

## Workflow Steps

### Step 1: Checkout the repository

Use `actions/checkout@v4`.

### Step 2: Set up Node.js

Use `actions/setup-node@v4` with Node.js version `20`.

### Step 3: Create the validation script

Create an inline Node.js script (using `run: node << 'EOF' ... EOF` syntax) OR create a separate script file at `.github/scripts/validate-rules.js` and run it. The script must perform **all** of the following checks on every `.json` file found recursively under the `rules/` directory:

#### Check 1 — Valid JSON Syntax
- Parse each file with `JSON.parse()`. If parsing fails, report the filename and error message. Mark the file as **FAILED**.

#### Check 2 — Required Fields Present
Every rule file must contain **all** of these top-level fields:
- `key` (string)
- `name` (string)
- `description` (string)
- `severity` (string)
- `type` (string)
- `tags` (array)
- `remediation` (object)
- `impacts` (array)
- `defaultSeverity` (string)
- `status` (string)
- `debt` (object)

Report each missing field as an error.

#### Check 3 — Enum Value Validation
Validate that fields use only these allowed values:
- `severity` and `defaultSeverity`: `"INFO"`, `"MINOR"`, `"MAJOR"`, `"CRITICAL"`, `"BLOCKER"`
- `type`: `"CODE_SMELL"`, `"BUG"`, `"VULNERABILITY"`, `"SECURITY_HOTSPOT"`
- `status`: `"READY"`, `"BETA"`, `"DEPRECATED"`, `"REMOVED"`
- `impacts[].softwareQuality`: `"MAINTAINABILITY"`, `"RELIABILITY"`, `"SECURITY"`
- `impacts[].severity`: `"LOW"`, `"MEDIUM"`, `"HIGH"`
- `debt.function`: `"LINEAR"`, `"CONSTANT_ISSUE"`, `"LINEAR_OFFSET"`
- `params[].type` (if params exist): `"INTEGER"`, `"FLOAT"`, `"BOOLEAN"`, `"STRING"`, `"TEXT"`

#### Check 4 — Cross-Field Consistency
- `severity` must exactly equal `defaultSeverity`. Report mismatch as error.
- `key` must exactly match the filename without the `.json` extension. For example, file `sql-injection.json` must have `"key": "sql-injection"`. Report mismatch as error.
- `tags` must be a non-empty array. Report empty array as error.
- `impacts` must be a non-empty array. Report empty array as error.
- `remediation` must contain `constantCost` (string matching pattern `^\d+(min|h|d)$`) and `examples` (non-empty array where each entry has `before` and `after` strings). Report missing/invalid as error.
- `debt` object: when `function` is `"LINEAR"`, `coefficient` is required; when `"CONSTANT_ISSUE"`, `offset` is required; when `"LINEAR_OFFSET"`, both `coefficient` and `offset` are required. Report missing required sub-fields as error.

#### Check 5 — Naming Conventions
- `key` must be kebab-case (match regex `^[a-z][a-z0-9]*(-[a-z0-9]+)*$`). Report violation as error.
- All `tags` entries must be lowercase kebab-case. Report violations as warnings.

### Step 4: Report results

The script must:
1. Print a summary table to stdout showing each file and its pass/fail status.
2. Exit with code `0` if all files pass, or code `1` if any file has errors — this ensures the GitHub Action fails the check on validation errors.

---

## Expected Output Format

The script should print output like this:

```
Validating SonarQube rule files...

✓ rules/security/sql-injection.json — PASS
✗ rules/code-smells/god-class.json — FAIL
    ERROR: severity ("MAJOR") does not match defaultSeverity ("CRITICAL")
✓ rules/performance/memory-leaks.json — PASS

Results: 48 passed, 1 failed, 49 total
```

---

## Example of a Valid Rule File (for reference)

```json
{
  "key": "sql-injection",
  "name": "SQL Injection Prevention",
  "description": "Detects potential SQL injection vulnerabilities where user input is directly concatenated into SQL queries.",
  "severity": "CRITICAL",
  "type": "VULNERABILITY",
  "tags": ["security", "sql", "injection", "owasp-top-10"],
  "remediation": {
    "constantCost": "30min",
    "examples": [
      {
        "before": "String query = \"SELECT * FROM users WHERE id = \" + userId;",
        "after": "PreparedStatement stmt = conn.prepareStatement(\"SELECT * FROM users WHERE id = ?\"); stmt.setString(1, userId);"
      }
    ]
  },
  "impacts": [
    {
      "softwareQuality": "SECURITY",
      "severity": "HIGH"
    }
  ],
  "defaultSeverity": "CRITICAL",
  "status": "READY",
  "debt": {
    "function": "CONSTANT_ISSUE",
    "offset": "30min"
  }
}
```

---

## Constraints

- Do NOT install any third-party npm packages. Use only Node.js built-in modules (`fs`, `path`).
- The workflow must work on `ubuntu-latest`.
- Keep everything in a single workflow file if using inline script, or at most two files (workflow YAML + script JS).
- Add a descriptive `name` to the workflow (e.g., `"Validate SonarQube Rule Definitions"`).
- The rule files live in four subdirectories: `rules/code-smells/`, `rules/maintainability/`, `rules/performance/`, `rules/security/`. The script must discover files recursively — do not hardcode filenames.