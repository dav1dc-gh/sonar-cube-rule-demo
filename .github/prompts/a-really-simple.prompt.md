## Task

Create a GitHub Actions CI workflow for this repository. The repository contains SonarQube rule definition files (JSON) organized under the `rules/` directory. There is no application code to compile or test — the CI workflow exists to validate the correctness and consistency of these JSON rule files on every push and pull request.

---

## File to Create

Create exactly **one** file at this path:

```
.github/workflows/validate-rules.yml
```

Do NOT create any other workflow files. Do NOT modify any existing files except to create this one new file.

---

## Workflow Requirements

### Workflow Name

```yaml
name: Validate SonarQube Rules
```

### Triggers

The workflow MUST trigger on:

1. **Push** to the `main` branch
2. **Pull request** targeting the `main` branch
3. **Manual dispatch** (`workflow_dispatch`) so it can be run on-demand

```yaml
on:
  push:
    branches: [main]
  pull_request:
    branches: [main]
  workflow_dispatch:
```

### Permissions

Set minimal permissions:

```yaml
permissions:
  contents: read
```

### Jobs

The workflow MUST contain exactly **three** jobs, in this order:

---

#### Job 1: `validate-json`

**Purpose**: Verify every `.json` file under `rules/` is syntactically valid JSON.

- **Runs on**: `ubuntu-latest`
- **Steps**:
  1. **Checkout** the repository using `actions/checkout@v4`.
  2. **Validate JSON syntax** — Run a shell command that:
     - Finds all `*.json` files recursively under the `rules/` directory.
     - Passes each file through `python3 -m json.tool` to validate syntax.
     - Prints `✅ <filename> is valid JSON` for each file that passes.
     - If ANY file fails validation, the step MUST exit with a non-zero exit code and print `❌ <filename> is INVALID JSON` before exiting.
     - At the end, print a summary line: `Validated <N> JSON files.`

**Exact step implementation**:

```yaml
- name: Validate JSON syntax
  run: |
    error=0
    count=0
    for file in $(find rules/ -name '*.json' -type f | sort); do
      count=$((count + 1))
      if python3 -m json.tool "$file" > /dev/null 2>&1; then
        echo "✅ $file is valid JSON"
      else
        echo "❌ $file is INVALID JSON"
        error=1
      fi
    done
    echo ""
    echo "Validated $count JSON files."
    exit $error
```

---

#### Job 2: `check-schema`

**Purpose**: Verify every JSON rule file contains all required fields with correct types and allowed values.

- **Runs on**: `ubuntu-latest`
- **Needs**: `validate-json` (this job depends on Job 1 passing)
- **Steps**:
  1. **Checkout** the repository using `actions/checkout@v4`.
  2. **Set up Python** using `actions/setup-python@v5` with `python-version: '3.12'`.
  3. **Run schema check** — Create an inline Python script (using `python3 << 'EOF'` heredoc syntax) that does the following:

**Schema validation rules** (the Python script MUST enforce ALL of these):

| Field             | Required? | Type          | Allowed Values / Constraints                                                                                      |
|-------------------|-----------|---------------|-------------------------------------------------------------------------------------------------------------------|
| `key`             | YES       | `string`      | Must be non-empty. Must match the filename (without `.json` extension).                                           |
| `name`            | YES       | `string`      | Must be non-empty.                                                                                                |
| `description`     | YES       | `string`      | Must be non-empty. Minimum 20 characters.                                                                         |
| `severity`        | YES       | `string`      | One of: `BLOCKER`, `CRITICAL`, `MAJOR`, `MINOR`, `INFO`                                                          |
| `type`            | YES       | `string`      | One of: `VULNERABILITY`, `BUG`, `CODE_SMELL`                                                                      |
| `tags`            | YES       | `list`        | Must be a non-empty list of strings. Each tag must be lowercase and use only `a-z`, `0-9`, and `-`.               |
| `remediation`     | YES       | `object`      | Must contain `constantCost` (string) and `examples` (non-empty list).                                            |
| `remediation.examples[*]` | — | `object`  | Each example must have `before` (string, non-empty) and `after` (string, non-empty).                              |
| `impacts`         | YES       | `list`        | Must be a non-empty list of objects.                                                                              |
| `impacts[*].softwareQuality` | — | `string` | One of: `MAINTAINABILITY`, `RELIABILITY`, `SECURITY`                                                             |
| `impacts[*].severity`        | — | `string` | One of: `HIGH`, `MEDIUM`, `LOW`                                                                                  |
| `defaultSeverity` | YES       | `string`      | Must match the `severity` field value exactly.                                                                    |
| `status`          | YES       | `string`      | One of: `READY`, `BETA`, `DEPRECATED`                                                                             |
| `debt`            | YES       | `object`      | Must contain `function` (string). If `function` is `CONSTANT_ISSUE`, must also have `offset` (string). If `function` is `LINEAR`, must also have `coefficient` (string). |
| `params`          | NO        | `list`        | If present, each item must have `key` (string), `name` (string), `description` (string), `defaultValue` (string), and `type` (string where allowed values are `INTEGER`, `STRING`, `BOOLEAN`). |

**Script behavior**:
- Find all `*.json` files recursively under `rules/`.
- For each file, load the JSON and check every rule above.
- Collect all errors per file. Print errors in the format: `ERROR [<filepath>]: <description of what's wrong>`
- Print `✅ <filepath> — schema valid` for each file with zero errors.
- At the end, print a summary: `Schema check complete: <passed> passed, <failed> failed out of <total> files.`
- Exit with code 0 if all files pass, exit with code 1 if any file fails.

---

#### Job 3: `check-categories`

**Purpose**: Verify that each JSON file is placed in the correct category directory based on its `type` field.

- **Runs on**: `ubuntu-latest`
- **Needs**: `validate-json` (this job depends on Job 1 passing — it can run in parallel with Job 2)
- **Steps**:
  1. **Checkout** the repository using `actions/checkout@v4`.
  2. **Check category placement** — Run a shell or Python script that enforces these directory-to-type mappings:

| Directory                  | Expected `type` values                |
|----------------------------|---------------------------------------|
| `rules/security/`         | `VULNERABILITY`                       |
| `rules/code-smells/`      | `CODE_SMELL`                          |
| `rules/performance/`      | `BUG`                                 |
| `rules/maintainability/`  | `CODE_SMELL` or `BUG`                |

**Behavior**:
- For each JSON file, read its `type` field and verify it matches the allowed types for the directory it's in.
- Print `❌ <filepath>: type "<actual_type>" not allowed in <directory> (expected: <allowed_types>)` for mismatches.
- Print `✅ <filepath> — correct category` for correct placements.
- Print a summary line at the end.
- Exit with code 1 if any file is miscategorized, exit with code 0 otherwise.

---

## Formatting and Style Rules

1. Use **YAML** format (not JSON) for the workflow file.
2. Use **2-space indentation** throughout the YAML file — no tabs.
3. Every `run:` block that is multi-line MUST use the `|` (literal block scalar) style.
4. Pin all GitHub Actions to a specific major version tag (e.g., `@v4`, `@v5`), not `@latest` or a commit SHA.
5. Include a comment at the top of the file:
   ```yaml
   # This workflow validates SonarQube rule definition JSON files.
   # It runs on push to main, on pull requests targeting main, and on manual dispatch.
   ```

---

## What NOT to Do

- Do NOT install Node.js or npm — this repo has no JavaScript.
- Do NOT install any pip packages — use only Python standard library.
- Do NOT add SonarQube scanning, code coverage, or deployment steps.
- Do NOT create matrix builds or multiple OS targets — `ubuntu-latest` only.
- Do NOT add caching steps — the workflow is lightweight and doesn't need it.
- Do NOT add any secrets or environment variables.
- Do NOT modify the README, rule files, or any other existing file.

---

## Expected Output

After you finish, the repository should have exactly this new file:

```
.github/workflows/validate-rules.yml
```

No other files should be created or modified (except `AI-HISTORY.md` per the custom instructions).