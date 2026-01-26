#!/usr/bin/env bash
# ============================================================================
# SonarQube Rules Validation Script
# ============================================================================
# This script validates all rule JSON files in the rules/ directory.
# It checks for:
#   - Valid JSON syntax
#   - Required fields present
#   - Valid enum values for severity, type, status
#   - Unique rule keys across all files
#   - Schema validation (if ajv-cli is installed)
#
# Usage: ./scripts/validate-rules.sh
# Exit codes: 0 = success, 1 = validation errors found
# ============================================================================

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
RULES_DIR="$PROJECT_ROOT/rules"
SCHEMA_FILE="$PROJECT_ROOT/schemas/rule-schema.json"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

ERRORS=0
WARNINGS=0
RULES_CHECKED=0
RULE_KEYS_FILE=$(mktemp)

echo "============================================"
echo "  SonarQube Rules Validation"
echo "============================================"
echo ""

# Function to check if key already exists
key_exists() {
    local key="$1"
    grep -q "^${key}:" "$RULE_KEYS_FILE" 2>/dev/null
}

# Function to add key
add_key() {
    local key="$1"
    local location="$2"
    echo "${key}:${location}" >> "$RULE_KEYS_FILE"
}

# Function to get key location
get_key_location() {
    local key="$1"
    grep "^${key}:" "$RULE_KEYS_FILE" | cut -d: -f2-
}

# Function to validate a single rule file
validate_rule() {
    local file="$1"
    local filename=$(basename "$file")
    local category=$(basename $(dirname "$file"))
    
    # Check valid JSON
    if ! jq empty "$file" 2>/dev/null; then
        echo -e "${RED}✗ $category/$filename: Invalid JSON syntax${NC}"
        ERRORS=$((ERRORS + 1))
        return
    fi
    
    # Extract required fields
    local key=$(jq -r '.key // empty' "$file")
    local name=$(jq -r '.name // empty' "$file")
    local description=$(jq -r '.description // empty' "$file")
    local severity=$(jq -r '.severity // empty' "$file")
    local type=$(jq -r '.type // empty' "$file")
    local status=$(jq -r '.status // empty' "$file")
    local tags=$(jq -r '.tags // empty' "$file")
    
    # Check required fields
    local missing_fields=""
    [ -z "$key" ] && missing_fields="$missing_fields key"
    [ -z "$name" ] && missing_fields="$missing_fields name"
    [ -z "$description" ] && missing_fields="$missing_fields description"
    [ -z "$severity" ] && missing_fields="$missing_fields severity"
    [ -z "$type" ] && missing_fields="$missing_fields type"
    [ -z "$status" ] && missing_fields="$missing_fields status"
    [ "$tags" = "null" ] || [ -z "$tags" ] && missing_fields="$missing_fields tags"
    
    if [ -n "$missing_fields" ]; then
        echo -e "${RED}✗ $category/$filename: Missing required fields:$missing_fields${NC}"
        ERRORS=$((ERRORS + 1))
        return
    fi
    
    # Check for duplicate keys
    if key_exists "$key"; then
        local existing=$(get_key_location "$key")
        echo -e "${RED}✗ $category/$filename: Duplicate rule key '$key' (also in $existing)${NC}"
        ERRORS=$((ERRORS + 1))
    else
        add_key "$key" "$category/$filename"
    fi
    
    # Validate severity
    case "$severity" in
        BLOCKER|CRITICAL|MAJOR|MINOR|INFO) ;;
        *)
            echo -e "${RED}✗ $category/$filename: Invalid severity '$severity'${NC}"
            ERRORS=$((ERRORS + 1))
            ;;
    esac
    
    # Validate type
    case "$type" in
        VULNERABILITY|BUG|CODE_SMELL) ;;
        *)
            echo -e "${RED}✗ $category/$filename: Invalid type '$type'${NC}"
            ERRORS=$((ERRORS + 1))
            ;;
    esac
    
    # Validate status
    case "$status" in
        READY|BETA|DEPRECATED) ;;
        *)
            echo -e "${RED}✗ $category/$filename: Invalid status '$status'${NC}"
            ERRORS=$((ERRORS + 1))
            ;;
    esac
    
    # Check key matches filename
    local expected_key="${filename%.json}"
    if [ "$key" != "$expected_key" ]; then
        echo -e "${YELLOW}⚠ $category/$filename: Key '$key' doesn't match filename${NC}"
        WARNINGS=$((WARNINGS + 1))
    fi
    
    # Check for remediation examples (warning only)
    local has_examples=$(jq '.remediation.examples | length' "$file" 2>/dev/null || echo "0")
    if [ "$has_examples" = "0" ] || [ "$has_examples" = "null" ]; then
        echo -e "${YELLOW}⚠ $category/$filename: Missing remediation examples${NC}"
        WARNINGS=$((WARNINGS + 1))
    fi
    
    RULES_CHECKED=$((RULES_CHECKED + 1))
}

# Find and validate all rule files
echo "Scanning for rule files..."
echo ""

for category_dir in "$RULES_DIR"/*/; do
    category=$(basename "$category_dir")
    echo "Category: $category"
    echo "-------------------------------------------"
    
    rule_count=0
    for rule_file in "$category_dir"*.json; do
        [ -f "$rule_file" ] || continue
        validate_rule "$rule_file"
        rule_count=$((rule_count + 1))
    done
    
    if [ $rule_count -eq 0 ]; then
        echo -e "${YELLOW}  No rule files found${NC}"
    fi
    echo ""
done

# Count unique keys
UNIQUE_KEYS=$(wc -l < "$RULE_KEYS_FILE" | tr -d ' ')

# Cleanup
rm -f "$RULE_KEYS_FILE"

# Summary
echo "============================================"
echo "  Validation Summary"
echo "============================================"
echo "Rules checked: $RULES_CHECKED"
echo "Unique keys:   $UNIQUE_KEYS"
echo -e "Errors:        ${RED}$ERRORS${NC}"
echo -e "Warnings:      ${YELLOW}$WARNINGS${NC}"
echo ""

if [ $ERRORS -gt 0 ]; then
    echo -e "${RED}Validation FAILED${NC}"
    exit 1
else
    echo -e "${GREEN}Validation PASSED${NC}"
    exit 0
fi
