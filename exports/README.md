# SonarQube Rules Export Utilities

This directory contains tools for exporting rules to SonarQube instances.

## Export Formats

### Quality Profile XML

Export rules as a SonarQube Quality Profile for easy import:

```bash
./export-quality-profile.sh --category security --output security-profile.xml
```

### Custom Rules Plugin

For integrating as a custom rules plugin, see the [SonarQube Plugin Development Guide](https://docs.sonarsource.com/sonarqube/latest/extension-guide/developing-a-plugin/supporting-new-languages/).

## Import Instructions

### Via Web UI

1. Navigate to **Quality Profiles** in SonarQube
2. Click **Restore** 
3. Upload the exported XML file

### Via API

```bash
curl -u admin:password \
  -F "backup=@security-profile.xml" \
  "http://localhost:9000/api/qualityprofiles/restore"
```

## Mapping to SonarQube API

| Our Field | SonarQube API Field |
|-----------|---------------------|
| key | ruleKey |
| name | name |
| description | markdownDescription |
| severity | severity |
| type | type |
| tags | sysTags |
| status | status |
| debt | debtRemediationFunction |
