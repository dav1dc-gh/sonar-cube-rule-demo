#!/usr/bin/env python3
"""
SonarQube Rule Deployment Script

Reads rule definition JSON files and deploys them to a SonarQube instance
via the Web API (api/rules/create and api/rules/update).

Usage:
    python3 scripts/deploy-rules.py                                        # Deploy all rules
    python3 scripts/deploy-rules.py rules/security/sql-injection.json      # Deploy one rule
    python3 scripts/deploy-rules.py --dry-run                              # Preview without deploying

Environment Variables:
    SONARQUBE_URL           - Base URL of the SonarQube server (e.g. https://sonar.example.com)
    SONARQUBE_TOKEN         - Authentication token with 'Administer Quality Profiles' permission
    SONARQUBE_TEMPLATE_KEY  - Template rule key for creating custom rules (optional)
"""

import base64
import json
import os
import sys
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path


# ── API Helpers ────────────────────────────────────────────────────────────────

def make_auth_header(token: str) -> dict[str, str]:
    """Create Basic auth header using the token as username (SonarQube convention)."""
    credentials = base64.b64encode(f"{token}:".encode()).decode()
    return {"Authorization": f"Basic {credentials}"}


def api_request(
    base_url: str,
    endpoint: str,
    params: dict,
    headers: dict[str, str],
    method: str = "POST",
) -> tuple[int, dict]:
    """Make an HTTP request to the SonarQube Web API. Returns (status_code, body_dict)."""
    url = f"{base_url.rstrip('/')}/{endpoint.lstrip('/')}"

    if method == "GET":
        qs = urllib.parse.urlencode(params)
        req = urllib.request.Request(f"{url}?{qs}", headers=headers, method="GET")
    else:
        data = urllib.parse.urlencode(params).encode("utf-8")
        req = urllib.request.Request(url, data=data, headers=headers, method="POST")

    try:
        with urllib.request.urlopen(req) as resp:
            body = json.loads(resp.read().decode("utf-8"))
            return resp.status, body
    except urllib.error.HTTPError as e:
        body: dict = {}
        try:
            body = json.loads(e.read().decode("utf-8"))
        except Exception:
            pass
        return e.code, body


# ── Rule Operations ───────────────────────────────────────────────────────────

def rule_exists(base_url: str, rule_key: str, headers: dict[str, str]) -> bool:
    """Check if a rule already exists in SonarQube."""
    status, _ = api_request(base_url, "api/rules/show", {"key": rule_key}, headers, method="GET")
    return status == 200


def create_rule(
    base_url: str,
    template_key: str,
    rule_data: dict,
    headers: dict[str, str],
) -> tuple[bool, str]:
    """Create a new custom rule from a template."""
    params: dict[str, str] = {
        "custom_key": rule_data["key"],
        "template_key": template_key,
        "name": rule_data["name"],
        "markdown_description": rule_data["description"],
        "severity": rule_data["severity"],
        "type": rule_data["type"],
        "status": rule_data.get("status", "READY"),
    }

    # Flatten rule params to the SonarQube semicolon-separated format
    rule_params = rule_data.get("params", [])
    if rule_params:
        pairs = [f"{p['key']}={p['defaultValue']}" for p in rule_params]
        params["params"] = ";".join(pairs)

    status, body = api_request(base_url, "api/rules/create", params, headers)
    if status == 200:
        return True, "Created"
    errors = body.get("errors", [])
    msg = errors[0].get("msg", f"HTTP {status}") if errors else f"HTTP {status}"
    return False, msg


def update_rule(
    base_url: str,
    rule_key: str,
    rule_data: dict,
    headers: dict[str, str],
) -> tuple[bool, str]:
    """Update an existing rule's metadata."""
    params: dict[str, str] = {
        "key": rule_key,
        "name": rule_data["name"],
        "markdown_description": rule_data["description"],
        "severity": rule_data["severity"],
        "status": rule_data.get("status", "READY"),
    }

    tags = rule_data.get("tags", [])
    if tags:
        params["tags"] = ",".join(tags)

    status, body = api_request(base_url, "api/rules/update", params, headers)
    if status == 200:
        return True, "Updated"
    errors = body.get("errors", [])
    msg = errors[0].get("msg", f"HTTP {status}") if errors else f"HTTP {status}"
    return False, msg


def deploy_rule(
    base_url: str,
    template_key: str,
    rule_data: dict,
    headers: dict[str, str],
    dry_run: bool = False,
) -> tuple[str, bool, str]:
    """Deploy a single rule — create if missing, update if existing.

    Returns (action, success, message).
    """
    # Build the fully-qualified rule key: <template_repo>:<custom_key>
    repo = template_key.split(":")[0] if ":" in template_key else template_key
    full_key = f"{repo}:{rule_data['key']}"

    exists = False if dry_run else rule_exists(base_url, full_key, headers)

    if dry_run:
        return "Would create/update", True, f"{full_key} (dry-run)"

    if exists:
        ok, msg = update_rule(base_url, full_key, rule_data, headers)
        return "Updated", ok, msg
    else:
        ok, msg = create_rule(base_url, template_key, rule_data, headers)
        return "Created", ok, msg


# ── File Discovery ─────────────────────────────────────────────────────────────

def discover_rule_files(root: str) -> list[str]:
    """Recursively find all .json rule files under rules/, excluding schema/."""
    files: list[str] = []
    rules_dir = os.path.join(root, "rules")
    for dirpath, dirnames, filenames in os.walk(rules_dir):
        dirnames[:] = [d for d in dirnames if d != "schema"]
        for fname in sorted(filenames):
            if fname.endswith(".json"):
                files.append(os.path.join(dirpath, fname))
    return files


# ── Main ───────────────────────────────────────────────────────────────────────

def main() -> None:
    dry_run = "--dry-run" in sys.argv
    args = [a for a in sys.argv[1:] if not a.startswith("--")]

    # Required configuration
    base_url = os.environ.get("SONARQUBE_URL", "")
    token = os.environ.get("SONARQUBE_TOKEN", "")
    template_key = os.environ.get("SONARQUBE_TEMPLATE_KEY", "")

    if not base_url:
        print("Error: SONARQUBE_URL environment variable is required.")
        sys.exit(1)
    if not token and not dry_run:
        print("Error: SONARQUBE_TOKEN environment variable is required.")
        sys.exit(1)
    if not template_key:
        print("Error: SONARQUBE_TEMPLATE_KEY environment variable is required.")
        print("  Set it to the template rule key for your custom rules,")
        print("  e.g. 'java:S001' or 'manual:custom-rule-template'.")
        sys.exit(1)

    # Determine project root
    script_dir = Path(__file__).resolve().parent
    project_root = script_dir.parent

    # Discover files
    if args:
        files = [os.path.abspath(a) for a in args]
    else:
        files = discover_rule_files(str(project_root))

    if not files:
        print("No rule files found.")
        sys.exit(1)

    headers = make_auth_header(token) if token else {}

    if dry_run:
        print("DRY RUN — no changes will be made to SonarQube\n")

    # Deploy each rule
    succeeded = 0
    failed = 0
    results: list[tuple[str, str, bool, str]] = []

    for filepath in files:
        rel = os.path.relpath(filepath, str(project_root))
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                rule_data = json.load(f)
        except (json.JSONDecodeError, OSError) as e:
            results.append((rel, "Error", False, str(e)))
            failed += 1
            continue

        action, ok, msg = deploy_rule(base_url, template_key, rule_data, headers, dry_run)
        results.append((rel, action, ok, msg))
        if ok:
            succeeded += 1
        else:
            failed += 1

    # Print results
    print(f"\n{'=' * 70}")
    print("DEPLOYMENT SUMMARY")
    print(f"{'=' * 70}")
    print(f"\n| {'File':<55} | {'Action':<20} | {'Status':>6} |")
    print(f"|{'-' * 57}|{'-' * 22}|{'-' * 8}|")

    for rel, action, ok, msg in results:
        status = "OK" if ok else "FAIL"
        label = action if ok else f"{action}: {msg}"
        print(f"| {rel:<55} | {label:<20} | {status:>6} |")

    print(f"\n  Total files:  {len(files)}")
    print(f"  Succeeded:    {succeeded}")
    print(f"  Failed:       {failed}")

    if failed:
        print(f"\n  RESULT: FAIL ({failed} file(s) failed to deploy)")
        sys.exit(1)
    else:
        print(f"\n  RESULT: {'DRY RUN OK' if dry_run else 'SUCCESS'} ({succeeded} rule(s) deployed)")
        sys.exit(0)


if __name__ == "__main__":
    main()
