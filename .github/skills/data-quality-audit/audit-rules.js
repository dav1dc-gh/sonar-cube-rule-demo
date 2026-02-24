#!/usr/bin/env node

/**
 * SonarQube Rule Quality Auditor
 *
 * Performs deep consistency analysis beyond what the schema validator checks:
 *   - Near-duplicate detection (name/description similarity)
 *   - Impact classification vs category alignment
 *   - Tag count and first-tag convention
 *   - Remediation cost outlier detection
 *   - Field redundancy drift (severity vs defaultSeverity, constantCost vs debt.offset)
 *
 * Outputs structured JSON: { errors: [], warnings: [], suggestions: [] }
 *
 * Usage:
 *   node .github/skills/data-quality-audit/audit-rules.js
 *   node .github/skills/data-quality-audit/audit-rules.js --json   # JSON-only output
 */

const fs = require("fs");
const path = require("path");

const RULES_DIR = path.resolve(__dirname, "..", "..", "..", "rules");
const CATEGORIES = ["security", "code-smells", "performance", "maintainability"];
const jsonOnly = process.argv.includes("--json");

// ─── Load all rules ─────────────────────────────────────────────────
function loadAllRules() {
  const rules = [];
  for (const category of CATEGORIES) {
    const dir = path.join(RULES_DIR, category);
    if (!fs.existsSync(dir)) continue;
    for (const file of fs.readdirSync(dir).filter((f) => f.endsWith(".json"))) {
      try {
        const filepath = path.join(dir, file);
        const rule = JSON.parse(fs.readFileSync(filepath, "utf-8"));
        rules.push({
          ...rule,
          _category: category,
          _file: `rules/${category}/${file}`,
          _filepath: filepath,
        });
      } catch (e) {
        // JSON parse errors are caught by the validator, skip here
      }
    }
  }
  return rules;
}

// ─── Similarity helpers ─────────────────────────────────────────────
function tokenize(text) {
  return text
    .toLowerCase()
    .replace(/[^a-z0-9\s]/g, " ")
    .split(/\s+/)
    .filter((t) => t.length > 2);
}

function jaccardSimilarity(a, b) {
  const setA = new Set(tokenize(a));
  const setB = new Set(tokenize(b));
  const intersection = new Set([...setA].filter((x) => setB.has(x)));
  const union = new Set([...setA, ...setB]);
  return union.size === 0 ? 0 : intersection.size / union.size;
}

// ─── Audit checks ───────────────────────────────────────────────────
function audit(rules) {
  const errors = [];
  const warnings = [];
  const suggestions = [];

  // 1. Check severity/defaultSeverity match
  for (const rule of rules) {
    if (rule.severity !== rule.defaultSeverity) {
      errors.push({
        file: rule._file,
        check: "severity-mismatch",
        message: `severity "${rule.severity}" ≠ defaultSeverity "${rule.defaultSeverity}"`,
      });
    }
  }

  // 2. Check constantCost vs debt.offset for CONSTANT_ISSUE rules
  for (const rule of rules) {
    if (
      rule.debt &&
      rule.debt.function === "CONSTANT_ISSUE" &&
      rule.remediation &&
      rule.remediation.constantCost
    ) {
      if (rule.remediation.constantCost !== rule.debt.offset) {
        errors.push({
          file: rule._file,
          check: "cost-offset-mismatch",
          message: `remediation.constantCost "${rule.remediation.constantCost}" ≠ debt.offset "${rule.debt.offset}"`,
        });
      }
    }
  }

  // 3. Near-duplicate detection
  for (let i = 0; i < rules.length; i++) {
    for (let j = i + 1; j < rules.length; j++) {
      const nameSim = jaccardSimilarity(rules[i].name, rules[j].name);
      const descSim = jaccardSimilarity(
        rules[i].description,
        rules[j].description
      );
      if (nameSim > 0.5 || descSim > 0.4) {
        warnings.push({
          file: rules[i]._file,
          relatedFile: rules[j]._file,
          check: "near-duplicate",
          message: `Potential duplicate: "${rules[i].name}" ↔ "${rules[j].name}" (name similarity: ${(nameSim * 100).toFixed(0)}%, description similarity: ${(descSim * 100).toFixed(0)}%)`,
        });
      }
    }
  }

  // 4. Impact classification vs category
  const expectedQuality = {
    security: "SECURITY",
    "code-smells": "MAINTAINABILITY",
    performance: "RELIABILITY",
    maintainability: "MAINTAINABILITY",
  };
  for (const rule of rules) {
    if (!rule.impacts || rule.impacts.length === 0) continue;
    const expected = expectedQuality[rule._category];
    const actual = rule.impacts[0].softwareQuality;
    if (expected && actual !== expected) {
      // Performance rules with MAINTAINABILITY are a known issue
      if (rule._category === "performance" && actual === "MAINTAINABILITY") {
        warnings.push({
          file: rule._file,
          check: "impact-misclassification",
          message: `Performance rule has softwareQuality "${actual}" — consider "${expected}" (RELIABILITY) since the primary concern is runtime behavior`,
        });
      }
    }
  }

  // 5. Tag checks
  for (const rule of rules) {
    if (!rule.tags) continue;
    // First tag should match category
    if (rule.tags[0] !== rule._category) {
      warnings.push({
        file: rule._file,
        check: "first-tag-mismatch",
        message: `First tag "${rule.tags[0]}" does not match category "${rule._category}"`,
      });
    }
    // Tag count convention: exactly 4
    if (rule.tags.length !== 4) {
      suggestions.push({
        file: rule._file,
        check: "tag-count",
        message: `Has ${rule.tags.length} tags (convention is 4)`,
      });
    }
  }

  // 6. Remediation cost outliers (by severity)
  const costBySeverity = {};
  for (const rule of rules) {
    if (!rule.remediation || !rule.remediation.constantCost) continue;
    const match = rule.remediation.constantCost.match(/^(\d+)/);
    if (!match) continue;
    const minutes = parseInt(match[1], 10);
    if (!costBySeverity[rule.severity]) costBySeverity[rule.severity] = [];
    costBySeverity[rule.severity].push({ file: rule._file, minutes, name: rule.name });
  }
  for (const [severity, entries] of Object.entries(costBySeverity)) {
    const sorted = entries.map((e) => e.minutes).sort((a, b) => a - b);
    const median = sorted[Math.floor(sorted.length / 2)];
    for (const entry of entries) {
      if (median > 0 && entry.minutes > median * 2) {
        suggestions.push({
          file: entry.file,
          check: "cost-outlier",
          message: `"${entry.name}" costs ${entry.minutes}min but median for ${severity} rules is ${median}min`,
        });
      }
    }
  }

  // 7. Thin descriptions
  for (const rule of rules) {
    if (rule.description && rule.description.length < 50) {
      suggestions.push({
        file: rule._file,
        check: "thin-description",
        message: `Description is only ${rule.description.length} chars — consider expanding`,
      });
    }
  }

  return { errors, warnings, suggestions };
}

// ─── Main ───────────────────────────────────────────────────────────
const rules = loadAllRules();
const results = audit(rules);

if (jsonOnly) {
  console.log(JSON.stringify(results, null, 2));
} else {
  console.log(`\n=== SonarQube Rule Quality Audit ===\n`);
  console.log(`Rules scanned: ${rules.length}`);
  console.log(
    `Errors: ${results.errors.length} | Warnings: ${results.warnings.length} | Suggestions: ${results.suggestions.length}\n`
  );

  if (results.errors.length > 0) {
    console.log("❌ ERRORS:");
    for (const e of results.errors) {
      console.log(`  ${e.file}: [${e.check}] ${e.message}`);
    }
    console.log();
  }

  if (results.warnings.length > 0) {
    console.log("⚠️  WARNINGS:");
    for (const w of results.warnings) {
      console.log(`  ${w.file}: [${w.check}] ${w.message}`);
    }
    console.log();
  }

  if (results.suggestions.length > 0) {
    console.log("💡 SUGGESTIONS:");
    for (const s of results.suggestions) {
      console.log(`  ${s.file}: [${s.check}] ${s.message}`);
    }
    console.log();
  }

  if (
    results.errors.length === 0 &&
    results.warnings.length === 0 &&
    results.suggestions.length === 0
  ) {
    console.log("✅ No issues found. All rules look consistent.\n");
  }
}

process.exit(results.errors.length > 0 ? 1 : 0);
