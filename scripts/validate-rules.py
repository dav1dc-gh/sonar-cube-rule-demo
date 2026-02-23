#!/usr/bin/env python3
"""
SonarQube Rule Definition Validator

Validates all JSON rule files under rules/ against the project schema
and cross-field consistency rules. Designed for local use and CI pipelines.

Usage:
    python3 scripts/validate-rules.py              # Validate all rules
    python3 scripts/validate-rules.py rules/security/sql-injection.json  # Validate one file
    python3 scripts/validate-rules.py --strict      # Treat warnings as errors
"""

import json
import os
import re
import sys
from pathlib import Path

# ── Constants ──────────────────────────────────────────────────────────────────

VALID_SEVERITIES = {"INFO", "MINOR", "MAJOR", "CRITICAL", "BLOCKER"}
VALID_TYPES = {"CODE_SMELL", "BUG", "VULNERABILITY", "SECURITY_HOTSPOT"}
VALID_STATUSES = {"READY", "BETA", "DEPRECATED", "REMOVED"}
VALID_IMPACT_QUALITIES = {"MAINTAINABILITY", "RELIABILITY", "SECURITY"}
VALID_IMPACT_SEVERITIES = {"LOW", "MEDIUM", "HIGH"}
VALID_DEBT_FUNCTIONS = {"LINEAR", "CONSTANT_ISSUE", "LINEAR_OFFSET"}
VALID_PARAM_TYPES = {"INTEGER", "FLOAT", "BOOLEAN", "STRING", "TEXT"}
DURATION_PATTERN = re.compile(r"^\d+(min|h|d)$")
KEBAB_CASE_PATTERN = re.compile(r"^[a-z][a-z0-9]*(-[a-z0-9]+)*$")
CAMEL_CASE_PATTERN = re.compile(r"^[a-z][a-zA-Z0-9]*$")

REQUIRED_FIELDS = [
    "key", "name", "description", "severity", "type", "tags",
    "remediation", "impacts", "defaultSeverity", "status", "debt"
]

CANONICAL_FIELD_ORDER = [
    "key", "name", "description", "severity", "type", "tags",
    "remediation", "impacts", "defaultSeverity", "status", "debt", "params"
]


# ── Helpers ────────────────────────────────────────────────────────────────────

class LintResult:
    def __init__(self, filepath: str):
        self.filepath = filepath
        self.errors: list[str] = []
        self.warnings: list[str] = []
        self.infos: list[str] = []

    def error(self, msg: str):
        self.errors.append(msg)

    def warning(self, msg: str):
        self.warnings.append(msg)

    def info(self, msg: str):
        self.infos.append(msg)

    @property
    def passed(self) -> bool:
        return len(self.errors) == 0

    def print_report(self):
        filename = os.path.basename(self.filepath)
        print(f"\n## Lint Results: {filename}")

        if not self.errors and not self.warnings and not self.infos:
            print("\nAll checks passed. No issues found.\n")
            return

        if self.errors:
            print("\n### Errors (must fix)")
            for e in self.errors:
                print(f"  - [ ] {e}")

        if self.warnings:
            print("\n### Warnings (should fix)")
            for w in self.warnings:
                print(f"  - [ ] {w}")

        if self.infos:
            print("\n### Info (suggestions)")
            for i in self.infos:
                print(f"  - [ ] {i}")

        print(f"\n### Summary")
        print(f"  Errors:   {len(self.errors)}")
        print(f"  Warnings: {len(self.warnings)}")
        print(f"  Info:     {len(self.infos)}")
        print(f"  Status:   {'FAIL' if self.errors else 'PASS'}")


# ── Lint Logic ─────────────────────────────────────────────────────────────────

def validate_rule_file(filepath: str) -> LintResult:
    result = LintResult(filepath)
    filename = os.path.basename(filepath)
    expected_key = filename.replace(".json", "")

    # 1. JSON Syntax
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            raw = f.read()
        data = json.loads(raw)
    except json.JSONDecodeError as e:
        result.error(f"JSON parse error: {e}")
        return result

    # 6. Formatting checks
    with open(filepath, "rb") as f:
        raw_bytes = f.read()
    if b"\t" in raw_bytes:
        result.info("File contains tabs; use 2-space indentation.")
    if not raw_bytes.endswith(b"\n"):
        result.info("File should end with a single newline character.")
    lines = raw_bytes.decode("utf-8").split("\n")
    for i, line in enumerate(lines):
        if line.rstrip(" ") != line:
            result.info(f"Line {i + 1}: trailing whitespace detected.")
            break  # report once

    # Check canonical field order
    actual_keys = list(data.keys())
    expected_order = [k for k in CANONICAL_FIELD_ORDER if k in actual_keys]
    if actual_keys != expected_order:
        result.info(f"Field order: consider reordering to canonical order: {', '.join(expected_order)}")

    # 2. Required fields
    for field in REQUIRED_FIELDS:
        if field not in data:
            result.error(f"`{field}`: required field is missing.")

    # Short-circuit if critical fields are missing
    if result.errors:
        return result

    # 3. Enum validation
    if data["severity"] not in VALID_SEVERITIES:
        result.error(f"`severity`: invalid value \"{data['severity']}\". Must be one of: {', '.join(sorted(VALID_SEVERITIES))}")

    if data["type"] not in VALID_TYPES:
        result.error(f"`type`: invalid value \"{data['type']}\". Must be one of: {', '.join(sorted(VALID_TYPES))}")

    if data["defaultSeverity"] not in VALID_SEVERITIES:
        result.error(f"`defaultSeverity`: invalid value \"{data['defaultSeverity']}\". Must be one of: {', '.join(sorted(VALID_SEVERITIES))}")

    if data["status"] not in VALID_STATUSES:
        result.error(f"`status`: invalid value \"{data['status']}\". Must be one of: {', '.join(sorted(VALID_STATUSES))}")

    # Impacts validation
    impacts = data.get("impacts", [])
    if not impacts:
        result.error("`impacts`: must contain at least one impact entry.")
    for idx, impact in enumerate(impacts):
        sq = impact.get("softwareQuality", "")
        sv = impact.get("severity", "")
        if sq not in VALID_IMPACT_QUALITIES:
            result.error(f"`impacts[{idx}].softwareQuality`: invalid value \"{sq}\". Must be one of: {', '.join(sorted(VALID_IMPACT_QUALITIES))}")
        if sv not in VALID_IMPACT_SEVERITIES:
            result.error(f"`impacts[{idx}].severity`: invalid value \"{sv}\". Must be one of: {', '.join(sorted(VALID_IMPACT_SEVERITIES))}")

    # Debt validation
    debt = data.get("debt", {})
    debt_func = debt.get("function", "")
    if debt_func not in VALID_DEBT_FUNCTIONS:
        result.error(f"`debt.function`: invalid value \"{debt_func}\". Must be one of: {', '.join(sorted(VALID_DEBT_FUNCTIONS))}")
    else:
        if debt_func == "LINEAR" and "coefficient" not in debt:
            result.error("`debt.coefficient`: required when function is LINEAR.")
        if debt_func == "CONSTANT_ISSUE" and "offset" not in debt:
            result.error("`debt.offset`: required when function is CONSTANT_ISSUE.")
        if debt_func == "LINEAR_OFFSET":
            if "coefficient" not in debt:
                result.error("`debt.coefficient`: required when function is LINEAR_OFFSET.")
            if "offset" not in debt:
                result.error("`debt.offset`: required when function is LINEAR_OFFSET.")

    for duration_field in ["coefficient", "offset"]:
        if duration_field in debt and not DURATION_PATTERN.match(debt[duration_field]):
            result.error(f"`debt.{duration_field}`: must match pattern '^\\d+(min|h|d)$'. Got \"{debt[duration_field]}\".")

    # Remediation validation
    rem = data.get("remediation", {})
    cost = rem.get("constantCost", "")
    if not cost:
        result.error("`remediation.constantCost`: required field is missing.")
    elif not DURATION_PATTERN.match(cost):
        result.error(f"`remediation.constantCost`: must match pattern '^\\d+(min|h|d)$'. Got \"{cost}\".")
    examples = rem.get("examples", [])
    if not examples:
        result.error("`remediation.examples`: at least one before/after example must be provided.")
    for idx, ex in enumerate(examples):
        if not ex.get("before"):
            result.error(f"`remediation.examples[{idx}].before`: must not be empty.")
        if not ex.get("after"):
            result.error(f"`remediation.examples[{idx}].after`: must not be empty.")

    # Tags validation
    tags = data.get("tags", [])
    if not tags:
        result.error("`tags`: must contain at least one tag.")
    for tag in tags:
        if not KEBAB_CASE_PATTERN.match(tag):
            result.warning(f"`tags`: \"{tag}\" is not kebab-case.")

    # Params validation
    params = data.get("params", [])
    for idx, param in enumerate(params):
        for pfield in ["key", "name", "description", "defaultValue", "type"]:
            if pfield not in param:
                result.error(f"`params[{idx}].{pfield}`: required field is missing.")
        ptype = param.get("type", "")
        if ptype and ptype not in VALID_PARAM_TYPES:
            result.error(f"`params[{idx}].type`: invalid value \"{ptype}\". Must be one of: {', '.join(sorted(VALID_PARAM_TYPES))}")
        pkey = param.get("key", "")
        if pkey and not CAMEL_CASE_PATTERN.match(pkey):
            result.warning(f"`params[{idx}].key`: \"{pkey}\" should be camelCase.")

    # 4. Cross-field consistency
    if data["severity"] != data["defaultSeverity"]:
        result.warning(f"`severity`/`defaultSeverity`: values do not match (\"{data['severity']}\" vs \"{data['defaultSeverity']}\"). Align them.")

    if data["key"] != expected_key:
        result.error(f"`key`: does not match filename. File is \"{filename}\", key is \"{data['key']}\".")

    if not KEBAB_CASE_PATTERN.match(data["key"]):
        result.error(f"`key`: must be kebab-case. Got \"{data['key']}\".")

    impact_qualities = {i.get("softwareQuality") for i in impacts}
    if data["type"] in ("VULNERABILITY", "SECURITY_HOTSPOT") and "SECURITY" not in impact_qualities:
        result.warning(f"Type is \"{data['type']}\" but no impact with softwareQuality SECURITY found.")
    if data["type"] == "CODE_SMELL" and "MAINTAINABILITY" not in impact_qualities:
        result.warning(f"Type is CODE_SMELL but no impact with softwareQuality MAINTAINABILITY found.")

    # 5. Convention checks
    desc = data.get("description", "")
    if len(desc) > 300:
        result.info(f"`description`: exceeds 300 characters ({len(desc)} chars). Consider shortening.")

    return result


def discover_rule_files(root: str) -> list[str]:
    """Recursively find all .json files under rules/, excluding schema/."""
    files = []
    rules_dir = os.path.join(root, "rules")
    for dirpath, dirnames, filenames in os.walk(rules_dir):
        # Skip the schema directory
        dirnames[:] = [d for d in dirnames if d != "schema"]
        for fname in sorted(filenames):
            if fname.endswith(".json"):
                files.append(os.path.join(dirpath, fname))
    return files


def main():
    strict = "--strict" in sys.argv
    args = [a for a in sys.argv[1:] if not a.startswith("--")]

    # Determine project root
    script_dir = Path(__file__).resolve().parent
    project_root = script_dir.parent

    if args:
        files = [os.path.abspath(a) for a in args]
    else:
        files = discover_rule_files(str(project_root))

    if not files:
        print("No rule files found.")
        sys.exit(1)

    results: list[LintResult] = []
    for filepath in files:
        r = validate_rule_file(filepath)
        results.append(r)

    # Print individual reports
    for r in results:
        r.print_report()

    # Summary table
    total_errors = sum(len(r.errors) for r in results)
    total_warnings = sum(len(r.warnings) for r in results)
    total_infos = sum(len(r.infos) for r in results)

    print("\n" + "=" * 70)
    print("VALIDATION SUMMARY")
    print("=" * 70)
    print(f"\n| {'File':<55} | {'Errors':>6} | {'Warnings':>8} | {'Info':>4} | {'Status':>6} |")
    print(f"|{'-'*57}|{'-'*8}|{'-'*10}|{'-'*6}|{'-'*8}|")

    for r in results:
        rel = os.path.relpath(r.filepath, str(project_root))
        status = "PASS" if r.passed else "FAIL"
        print(f"| {rel:<55} | {len(r.errors):>6} | {len(r.warnings):>8} | {len(r.infos):>4} | {status:>6} |")

    print(f"\n  Total files:    {len(results)}")
    print(f"  Total errors:   {total_errors}")
    print(f"  Total warnings: {total_warnings}")
    print(f"  Total info:     {total_infos}")

    failed = [r for r in results if not r.passed]
    if strict:
        failed_strict = [r for r in results if r.errors or r.warnings]
        if failed_strict:
            print(f"\n  STRICT MODE: {len(failed_strict)} file(s) have errors or warnings.")
            sys.exit(1)

    if failed:
        print(f"\n  RESULT: FAIL ({len(failed)} file(s) with errors)")
        sys.exit(1)
    else:
        print(f"\n  RESULT: PASS (all {len(results)} files valid)")
        sys.exit(0)


if __name__ == "__main__":
    main()
