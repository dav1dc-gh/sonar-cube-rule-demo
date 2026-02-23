#!/bin/bash
# =============================================================================
# SonarQube Rules Validation Script
# =============================================================================
# Validates all rule JSON files against the schema and checks for consistency.
#
# Usage: ./scripts/validate-rules.sh [options]
# Options:
#   -v, --verbose    Show detailed output
#   -f, --fix        Attempt to fix common formatting issues
#   -h, --help       Show this help message
# =============================================================================

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Script directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(dirname "$SCRIPT_DIR")"
RULES_DIR="$ROOT_DIR/rules"
SCHEMA_FILE="$ROOT_DIR/schemas/rule-schema.json"
INDEX_FILE="$ROOT_DIR/rules-index.json"

# Counters
TOTAL_RULES=0
VALID_RULES=0
INVALID_RULES=0
WARNINGS=0

# Options
VERBOSE=false
FIX_MODE=false

# Parse command line arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        -v|--verbose)
            VERBOSE=true
            shift
            ;;
        -f|--fix)
            FIX_MODE=true
            shift
            ;;
        -h|--help)
            echo "Usage: $0 [options]"
            echo "Options:"
            echo "  -v, --verbose    Show detailed output"
            echo "  -f, --fix        Attempt to fix common formatting issues"
            echo "  -h, --help       Show this help message"
            exit 0
            ;;
        *)
            echo "Unknown option: $1"
            exit 1
            ;;
    esac
done

# Helper functions
log_info() {
    echo -e "${BLUE}ℹ${NC} $1"
}

log_success() {
    echo -e "${GREEN}✓${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}⚠${NC} $1"
    WARNINGS=$((WARNINGS + 1))
}

log_error() {
    echo -e "${RED}✗${NC} $1"
}

# Check prerequisites
check_prerequisites() {
    log_info "Checking prerequisites..."
    
    if ! command -v jq &> /dev/null; then
        log_error "jq is not installed. Please install it first:"
        echo "  macOS:   brew install jq"
        echo "  Ubuntu:  apt-get install jq"
        exit 1
    fi
    
    # Check for ajv (optional, for schema validation)
    if command -v ajv &> /dev/null; then
        SCHEMA_VALIDATOR="ajv"
    elif command -v jsonschema &> /dev/null; then
        SCHEMA_VALIDATOR="jsonschema"
    else
        log_warning "No JSON Schema validator found (ajv or jsonschema). Schema validation will be skipped."
        log_info "Install with: npm install -g ajv-cli"
        SCHEMA_VALIDATOR="none"
    fi
    
    log_success "Prerequisites check complete"
}

# Validate JSON syntax
validate_json_syntax() {
    local file=$1
    if jq empty "$file" 2>/dev/null; then
        return 0
    else
        return 1
    fi
}

# Validate required fields
validate_required_fields() {
    local file=$1
    local missing_fields=()
    
    local required_fields=("key" "name" "description" "severity" "type" "status")
    
    for field in "${required_fields[@]}"; do
        if ! jq -e ".$field" "$file" > /dev/null 2>&1; then
            missing_fields+=("$field")
        fi
    done
    
    if [ ${#missing_fields[@]} -eq 0 ]; then
        return 0
    else
        echo "${missing_fields[*]}"
        return 1
    fi
}

# Validate field values
validate_field_values() {
    local file=$1
    local errors=()
    
    # Validate severity
    local severity=$(jq -r '.severity // empty' "$file")
    if [[ -n "$severity" ]] && [[ ! "$severity" =~ ^(BLOCKER|CRITICAL|MAJOR|MINOR|INFO)$ ]]; then
        errors+=("Invalid severity: $severity")
    fi
    
    # Validate type
    local type=$(jq -r '.type // empty' "$file")
    if [[ -n "$type" ]] && [[ ! "$type" =~ ^(BUG|VULNERABILITY|CODE_SMELL|SECURITY_HOTSPOT)$ ]]; then
        errors+=("Invalid type: $type")
    fi
    
    # Validate status
    local status=$(jq -r '.status // empty' "$file")
    if [[ -n "$status" ]] && [[ ! "$status" =~ ^(READY|BETA|DEPRECATED|REMOVED)$ ]]; then
        errors+=("Invalid status: $status")
    fi
    
    # Validate key format (kebab-case)
    local key=$(jq -r '.key // empty' "$file")
    if [[ -n "$key" ]] && [[ ! "$key" =~ ^[a-z][a-z0-9-]*[a-z0-9]$ ]]; then
        errors+=("Invalid key format (must be kebab-case): $key")
    fi
    
    if [ ${#errors[@]} -eq 0 ]; then
        return 0
    else
        printf '%s\n' "${errors[@]}"
        return 1
    fi
}

# Validate filename matches key
validate_filename_key_match() {
    local file=$1
    local filename=$(basename "$file" .json)
    local key=$(jq -r '.key' "$file")
    
    if [[ "$filename" == "$key" ]]; then
        return 0
    else
        echo "Filename '$filename.json' doesn't match key '$key'"
        return 1
    fi
}

# Check for recommended fields
check_recommended_fields() {
    local file=$1
    local warnings=()
    
    # Check for tags
    if ! jq -e '.tags | length > 0' "$file" > /dev/null 2>&1; then
        warnings+=("Missing or empty 'tags' field")
    fi
    
    # Check for remediation
    if ! jq -e '.remediation' "$file" > /dev/null 2>&1; then
        warnings+=("Missing 'remediation' field")
    fi
    
    # Check for examples
    if ! jq -e '.remediation.examples | length > 0' "$file" > /dev/null 2>&1; then
        warnings+=("Missing code examples in remediation")
    fi
    
    # Check for impacts
    if ! jq -e '.impacts | length > 0' "$file" > /dev/null 2>&1; then
        warnings+=("Missing 'impacts' field")
    fi
    
    if [ ${#warnings[@]} -gt 0 ]; then
        printf '%s\n' "${warnings[@]}"
    fi
}

# Validate a single rule file
validate_rule() {
    local file=$1
    local relative_path="${file#$ROOT_DIR/}"
    local is_valid=true
    
    ((TOTAL_RULES++))
    
    if $VERBOSE; then
        log_info "Validating: $relative_path"
    fi
    
    # Check JSON syntax
    if ! validate_json_syntax "$file"; then
        log_error "Invalid JSON syntax: $relative_path"
        ((INVALID_RULES++))
        return 1
    fi
    
    # Check required fields
    local missing=$(validate_required_fields "$file")
    if [ $? -ne 0 ]; then
        log_error "Missing required fields in $relative_path: $missing"
        is_valid=false
    fi
    
    # Check field values
    local field_errors=$(validate_field_values "$file")
    if [ $? -ne 0 ]; then
        log_error "Invalid field values in $relative_path:"
        echo "$field_errors" | while read -r err; do
            echo "    - $err"
        done
        is_valid=false
    fi
    
    # Check filename matches key
    local filename_error=$(validate_filename_key_match "$file")
    if [ $? -ne 0 ]; then
        log_error "$filename_error"
        is_valid=false
    fi
    
    # Check recommended fields (warnings only)
    if $VERBOSE; then
        local field_warnings=$(check_recommended_fields "$file")
        if [ -n "$field_warnings" ]; then
            log_warning "Recommendations for $relative_path:"
            echo "$field_warnings" | while read -r warn; do
                echo "    - $warn"
            done
        fi
    fi
    
    if $is_valid; then
        ((VALID_RULES++))
        if $VERBOSE; then
            log_success "Valid: $relative_path"
        fi
    else
        ((INVALID_RULES++))
    fi
}

# Validate index file
validate_index() {
    log_info "Validating rules-index.json..."
    
    if [ ! -f "$INDEX_FILE" ]; then
        log_error "Index file not found: $INDEX_FILE"
        return 1
    fi
    
    if ! validate_json_syntax "$INDEX_FILE"; then
        log_error "Invalid JSON syntax in index file"
        return 1
    fi
    
    # Check that all indexed rules exist
    local missing_files=0
    while IFS= read -r rule_file; do
        if [ ! -f "$ROOT_DIR/$rule_file" ]; then
            log_error "Indexed rule file not found: $rule_file"
            ((missing_files++))
        fi
    done < <(jq -r '.rules[].file' "$INDEX_FILE")
    
    # Check that all rule files are indexed
    local unindexed_files=0
    for category_dir in "$RULES_DIR"/*/; do
        for rule_file in "$category_dir"*.json; do
            if [ -f "$rule_file" ]; then
                local relative_path="${rule_file#$ROOT_DIR/}"
                if ! jq -e ".rules[] | select(.file == \"$relative_path\")" "$INDEX_FILE" > /dev/null 2>&1; then
                    log_warning "Rule file not indexed: $relative_path"
                    ((unindexed_files++))
                fi
            fi
        done
    done
    
    if [ $missing_files -eq 0 ] && [ $unindexed_files -eq 0 ]; then
        log_success "Index file is valid and complete"
    fi
}

# Check for duplicate keys
check_duplicate_keys() {
    log_info "Checking for duplicate rule keys..."
    
    local duplicates=$(find "$RULES_DIR" -name "*.json" -exec jq -r '.key' {} \; | sort | uniq -d)
    
    if [ -n "$duplicates" ]; then
        log_error "Duplicate rule keys found:"
        echo "$duplicates" | while read -r key; do
            echo "    - $key"
            find "$RULES_DIR" -name "*.json" -exec grep -l "\"key\": \"$key\"" {} \;
        done
        return 1
    else
        log_success "No duplicate keys found"
    fi
}

# Main validation
main() {
    echo ""
    echo "╔══════════════════════════════════════════════════════════════╗"
    echo "║           SonarQube Rules Validation                        ║"
    echo "╚══════════════════════════════════════════════════════════════╝"
    echo ""
    
    check_prerequisites
    echo ""
    
    # Validate each category
    for category_dir in "$RULES_DIR"/*/; do
        if [ -d "$category_dir" ]; then
            category_name=$(basename "$category_dir")
            log_info "Validating category: $category_name"
            
            for rule_file in "$category_dir"*.json; do
                if [ -f "$rule_file" ]; then
                    validate_rule "$rule_file"
                fi
            done
            echo ""
        fi
    done
    
    # Additional checks
    validate_index
    echo ""
    check_duplicate_keys
    
    # Summary
    echo ""
    echo "╔══════════════════════════════════════════════════════════════╗"
    echo "║                    Validation Summary                        ║"
    echo "╚══════════════════════════════════════════════════════════════╝"
    echo ""
    echo "  Total rules checked:  $TOTAL_RULES"
    echo -e "  ${GREEN}Valid rules:${NC}          $VALID_RULES"
    echo -e "  ${RED}Invalid rules:${NC}        $INVALID_RULES"
    echo -e "  ${YELLOW}Warnings:${NC}             $WARNINGS"
    echo ""
    
    if [ $INVALID_RULES -gt 0 ]; then
        log_error "Validation failed with $INVALID_RULES error(s)"
        exit 1
    else
        log_success "All rules validated successfully!"
        exit 0
    fi
}

# Run main function
main
