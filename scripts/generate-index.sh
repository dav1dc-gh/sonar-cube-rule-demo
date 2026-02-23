#!/bin/bash
# =============================================================================
# SonarQube Rules Index Generator
# =============================================================================
# Generates the rules-index.json file from all rule files in the repository.
#
# Usage: ./scripts/generate-index.sh [options]
# Options:
#   -o, --output FILE    Output file (default: rules-index.json)
#   -p, --pretty         Pretty print output (default: true)
#   -h, --help           Show this help message
# =============================================================================

set -e

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m'

# Script directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(dirname "$SCRIPT_DIR")"
RULES_DIR="$ROOT_DIR/rules"
OUTPUT_FILE="$ROOT_DIR/rules-index.json"
PRETTY=true

# Parse command line arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        -o|--output)
            OUTPUT_FILE="$2"
            shift 2
            ;;
        -p|--pretty)
            PRETTY=true
            shift
            ;;
        --no-pretty)
            PRETTY=false
            shift
            ;;
        -h|--help)
            echo "Usage: $0 [options]"
            echo "Options:"
            echo "  -o, --output FILE    Output file (default: rules-index.json)"
            echo "  -p, --pretty         Pretty print output (default: true)"
            echo "  -h, --help           Show this help message"
            exit 0
            ;;
        *)
            echo "Unknown option: $1"
            exit 1
            ;;
    esac
done

log_info() {
    echo -e "${BLUE}ℹ${NC} $1"
}

log_success() {
    echo -e "${GREEN}✓${NC} $1"
}

# Check prerequisites
if ! command -v jq &> /dev/null; then
    echo "Error: jq is required but not installed."
    exit 1
fi

log_info "Generating rules index..."

# Build categories object
CATEGORIES='{}'
for category_dir in "$RULES_DIR"/*/; do
    if [ -d "$category_dir" ]; then
        category_name=$(basename "$category_dir")
        rule_count=$(find "$category_dir" -name "*.json" | wc -l | tr -d ' ')
        
        # Generate description based on category name
        case $category_name in
            "security")
                description="Security vulnerability detection rules"
                ;;
            "code-smells")
                description="Code quality and design issue rules"
                ;;
            "performance")
                description="Performance optimization rules"
                ;;
            "maintainability")
                description="Code maintainability rules"
                ;;
            *)
                description="$category_name rules"
                ;;
        esac
        
        CATEGORIES=$(echo "$CATEGORIES" | jq --arg name "$category_name" \
            --arg desc "$description" \
            --argjson count "$rule_count" \
            '. + {($name): {"description": $desc, "ruleCount": $count}}')
    fi
done

# Build rules array
RULES='[]'
for category_dir in "$RULES_DIR"/*/; do
    if [ -d "$category_dir" ]; then
        category_name=$(basename "$category_dir")
        
        for rule_file in "$category_dir"*.json; do
            if [ -f "$rule_file" ]; then
                relative_path="${rule_file#$ROOT_DIR/}"
                
                # Extract rule metadata
                rule_entry=$(jq --arg category "$category_name" \
                    --arg file "$relative_path" \
                    '{
                        key: .key,
                        name: .name,
                        category: $category,
                        severity: .severity,
                        type: .type,
                        status: .status,
                        tags: .tags,
                        file: $file
                    }' "$rule_file")
                
                RULES=$(echo "$RULES" | jq --argjson rule "$rule_entry" '. + [$rule]')
            fi
        done
    fi
done

# Sort rules by category then by key
RULES=$(echo "$RULES" | jq 'sort_by(.category, .key)')

# Get version from existing index or use 1.0.0
if [ -f "$OUTPUT_FILE" ]; then
    VERSION=$(jq -r '.version // "1.0.0"' "$OUTPUT_FILE")
else
    VERSION="1.0.0"
fi

# Generate timestamp
TIMESTAMP=$(date -u +"%Y-%m-%dT%H:%M:%SZ")

# Build final index
INDEX=$(jq -n \
    --arg version "$VERSION" \
    --arg timestamp "$TIMESTAMP" \
    --argjson categories "$CATEGORIES" \
    --argjson rules "$RULES" \
    '{
        version: $version,
        generatedAt: $timestamp,
        categories: $categories,
        rules: $rules
    }')

# Output
if $PRETTY; then
    echo "$INDEX" | jq '.' > "$OUTPUT_FILE"
else
    echo "$INDEX" | jq -c '.' > "$OUTPUT_FILE"
fi

# Summary
total_rules=$(echo "$RULES" | jq 'length')
log_success "Generated index with $total_rules rules"
log_success "Output written to: $OUTPUT_FILE"
