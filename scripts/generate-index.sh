#!/usr/bin/env bash
# ============================================================================
# SonarQube Rules Index Generator
# ============================================================================
# Generates a rules-index.json file containing metadata about all rules.
# This index can be used for:
#   - Quick lookup of available rules
#   - Importing rules into SonarQube
#   - Generating documentation
#   - CI/CD integration
#
# Usage: ./scripts/generate-index.sh
# Output: rules-index.json in project root
# ============================================================================

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
RULES_DIR="$PROJECT_ROOT/rules"
OUTPUT_FILE="$PROJECT_ROOT/rules-index.json"

echo "Generating rules index..."

TIMESTAMP=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
TOTAL_RULES=0

# Build the rules array
RULES_JSON="[]"

for category_dir in "$RULES_DIR"/*/; do
    category=$(basename "$category_dir")
    
    for rule_file in "$category_dir"*.json; do
        [ -f "$rule_file" ] || continue
        
        # Extract rule metadata
        key=$(jq -r '.key' "$rule_file")
        name=$(jq -r '.name' "$rule_file")
        severity=$(jq -r '.severity' "$rule_file")
        type=$(jq -r '.type' "$rule_file")
        status=$(jq -r '.status' "$rule_file")
        tags=$(jq -c '.tags' "$rule_file")
        
        # Build rule entry
        rule_entry=$(jq -n \
            --arg key "$key" \
            --arg name "$name" \
            --arg category "$category" \
            --arg severity "$severity" \
            --arg type "$type" \
            --arg status "$status" \
            --argjson tags "$tags" \
            --arg file "rules/$category/$(basename "$rule_file")" \
            '{
                key: $key,
                name: $name,
                category: $category,
                severity: $severity,
                type: $type,
                status: $status,
                tags: $tags,
                file: $file
            }')
        
        RULES_JSON=$(echo "$RULES_JSON" | jq --argjson rule "$rule_entry" '. += [$rule]')
        TOTAL_RULES=$((TOTAL_RULES + 1))
    done
done

# Generate category counts from the rules array
BY_CATEGORY=$(echo "$RULES_JSON" | jq 'group_by(.category) | map({key: .[0].category, value: length}) | from_entries')
BY_SEVERITY=$(echo "$RULES_JSON" | jq 'group_by(.severity) | map({key: .[0].severity, value: length}) | from_entries')
BY_TYPE=$(echo "$RULES_JSON" | jq 'group_by(.type) | map({key: .[0].type, value: length}) | from_entries')

# Build category metadata
CATEGORIES_JSON=$(echo "$BY_CATEGORY" | jq '
    to_entries | map({
        key: .key,
        value: {
            description: (
                if .key == "security" then "Security vulnerability detection rules"
                elif .key == "code-smells" then "Code quality and design issue rules"
                elif .key == "performance" then "Performance optimization rules"
                elif .key == "maintainability" then "Code maintainability rules"
                else "Custom rules"
                end
            ),
            ruleCount: .value
        }
    }) | from_entries
')

# Assemble final JSON
jq -n \
    --arg version "1.0.0" \
    --arg timestamp "$TIMESTAMP" \
    --argjson categories "$CATEGORIES_JSON" \
    --argjson rules "$RULES_JSON" \
    --argjson total "$TOTAL_RULES" \
    --argjson byCategory "$BY_CATEGORY" \
    --argjson bySeverity "$BY_SEVERITY" \
    --argjson byType "$BY_TYPE" \
    '{
        version: $version,
        generatedAt: $timestamp,
        categories: $categories,
        rules: $rules,
        summary: {
            totalRules: $total,
            byCategory: $byCategory,
            bySeverity: $bySeverity,
            byType: $byType
        }
    }' > "$OUTPUT_FILE"

echo "Generated: $OUTPUT_FILE"
echo ""
echo "Summary:"
echo "  Total rules: $TOTAL_RULES"
echo ""
echo "By Category:"
echo "$BY_CATEGORY" | jq -r 'to_entries[] | "  - \(.key): \(.value)"'
echo ""
echo "By Severity:"
echo "$BY_SEVERITY" | jq -r 'to_entries[] | "  - \(.key): \(.value)"'
echo ""
echo "By Type:"
echo "$BY_TYPE" | jq -r 'to_entries[] | "  - \(.key): \(.value)"'
