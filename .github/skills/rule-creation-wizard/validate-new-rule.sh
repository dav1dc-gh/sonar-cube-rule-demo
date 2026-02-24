#!/usr/bin/env bash
# Validates all SonarQube rules and reports pass/fail.
# Used by the rule-creation-wizard skill after creating a new rule.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/../../.." && pwd)"

echo "=== Running SonarQube Rule Validation ==="
echo ""

if node "$REPO_ROOT/scripts/validate-rules.js" --verbose; then
  echo ""
  echo "✅ All rules passed validation."
  exit 0
else
  echo ""
  echo "❌ Validation failed. See errors above."
  exit 1
fi
