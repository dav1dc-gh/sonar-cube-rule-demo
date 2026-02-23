## Description

<!-- Briefly describe the changes in this PR -->

## Type of Change

<!-- Mark the appropriate option with an 'x' -->

- [ ] 🆕 New rule(s) added
- [ ] 📝 Existing rule(s) modified
- [ ] 🗑️ Rule(s) deprecated/removed
- [ ] 📚 Documentation update
- [ ] 🔧 Scripts/tooling update
- [ ] 🐛 Bug fix

## Rules Changed

<!-- List the rules added, modified, or removed -->

| Rule Key | Category | Action | Severity |
|----------|----------|--------|----------|
| `example-rule` | security | Added | CRITICAL |

## Checklist

### For New Rules

- [ ] Rule key follows kebab-case naming convention
- [ ] Filename matches the rule key
- [ ] Description is clear and at least 50 characters
- [ ] Appropriate severity level assigned
- [ ] Correct type selected (BUG, VULNERABILITY, CODE_SMELL, SECURITY_HOTSPOT)
- [ ] Relevant tags included
- [ ] Remediation section with code examples provided
- [ ] Impacts array included with software quality and severity
- [ ] Rule added to `rules-index.json`
- [ ] CHANGELOG.md updated

### For All Changes

- [ ] JSON syntax is valid (`jq empty <file>`)
- [ ] Validation script passes (`./scripts/validate-rules.sh`)
- [ ] No duplicate rule keys
- [ ] Changes are documented in CHANGELOG.md

## Testing

<!-- Describe how you tested these changes -->

- [ ] Ran `./scripts/validate-rules.sh`
- [ ] Ran `./scripts/generate-index.sh` to verify index
- [ ] Verified JSON syntax with `jq`

## Additional Notes

<!-- Any additional information reviewers should know -->
