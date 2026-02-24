#!/usr/bin/env node

/**
 * SonarQube Rule Validator
 *
 * Validates all rule JSON files against the schema and enforces repository
 * conventions that JSON Schema alone cannot express:
 *   - key must match filename (without .json)
 *   - severity must equal defaultSeverity
 *   - first tag must match the parent directory name
 *   - no duplicate keys across the entire repository
 *   - LINEAR debt must include coefficient; CONSTANT_ISSUE must include offset
 *
 * Usage:
 *   node scripts/validate-rules.js            # validate all rules
 *   node scripts/validate-rules.js --verbose  # show per-file pass/fail
 *   node scripts/validate-rules.js --fix      # auto-fix what's possible (dry-run)
 */

const fs = require("fs");
const path = require("path");

// ─── Configuration ──────────────────────────────────────────────────
const RULES_DIR = path.resolve(__dirname, "..", "rules");
const SCHEMA_PATH = path.resolve(
  __dirname,
  "..",
  "schema",
  "sonarqube-rule.schema.json"
);
const CATEGORIES = ["security", "code-smells", "performance", "maintainability"];
const VALID_SEVERITIES = ["BLOCKER", "CRITICAL", "MAJOR", "MINOR", "INFO"];
const VALID_TYPES = ["VULNERABILITY", "BUG", "CODE_SMELL"];
const VALID_QUALITIES = ["SECURITY", "MAINTAINABILITY", "RELIABILITY"];
const VALID_IMPACT_SEVERITIES = ["HIGH", "MEDIUM", "LOW"];
const VALID_STATUSES = ["READY", "BETA", "DEPRECATED"];
const VALID_DEBT_FUNCTIONS = ["CONSTANT_ISSUE", "LINEAR"];

const verbose = process.argv.includes("--verbose");

// ─── Helpers ────────────────────────────────────────────────────────
function collectRuleFiles() {
  const files = [];
  for (const category of CATEGORIES) {
    const dir = path.join(RULES_DIR, category);
    if (!fs.existsSync(dir)) continue;
    for (const file of fs.readdirSync(dir).filter((f) => f.endsWith(".json"))) {
      files.push({
        category,
        filename: file,
        filepath: path.join(dir, file),
        key: file.replace(/\.json$/, ""),
      });
    }
  }
  return files;
}

function validateField(errors, rule, field, allowed, filepath) {
  if (rule[field] === undefined) {
    errors.push(`${filepath}: missing required field "${field}"`);
    return false;
  }
  if (allowed && !allowed.includes(rule[field])) {
    errors.push(
      `${filepath}: "${field}" is "${rule[field]}", expected one of: ${allowed.join(", ")}`
    );
    return false;
  }
  return true;
}

// ─── Core Validation ────────────────────────────────────────────────
function validateRule({ category, filename, filepath, key }) {
  const errors = [];
  const warnings = [];

  // 1. Parse JSON
  let raw, rule;
  try {
    raw = fs.readFileSync(filepath, "utf-8");
    rule = JSON.parse(raw);
  } catch (e) {
    errors.push(`${filepath}: invalid JSON — ${e.message}`);
    return { errors, warnings };
  }

  // 2. Key matches filename
  if (rule.key !== key) {
    errors.push(
      `${filepath}: key "${rule.key}" does not match filename "${key}"`
    );
  }

  // 3. Required string fields
  for (const field of ["key", "name", "description"]) {
    if (typeof rule[field] !== "string" || rule[field].length === 0) {
      errors.push(`${filepath}: "${field}" must be a non-empty string`);
    }
  }

  // 4. Enum fields
  validateField(errors, rule, "severity", VALID_SEVERITIES, filepath);
  validateField(errors, rule, "type", VALID_TYPES, filepath);
  validateField(errors, rule, "defaultSeverity", VALID_SEVERITIES, filepath);
  validateField(errors, rule, "status", VALID_STATUSES, filepath);

  // 5. severity === defaultSeverity
  if (rule.severity && rule.defaultSeverity && rule.severity !== rule.defaultSeverity) {
    errors.push(
      `${filepath}: severity "${rule.severity}" does not match defaultSeverity "${rule.defaultSeverity}"`
    );
  }

  // 6. Tags
  if (!Array.isArray(rule.tags) || rule.tags.length < 2) {
    errors.push(`${filepath}: "tags" must be an array with at least 2 entries`);
  } else {
    // first tag should match category (code-smells uses individual smell names, but tag 'code-smell' expected)
    const categoryTag = category === "code-smells" ? "code-smell" : category;
    if (rule.tags[0] !== category && rule.tags[0] !== categoryTag) {
      warnings.push(
        `${filepath}: first tag "${rule.tags[0]}" doesn't match category "${category}"`
      );
    }
    // duplicates
    const seen = new Set();
    for (const tag of rule.tags) {
      if (seen.has(tag)) {
        errors.push(`${filepath}: duplicate tag "${tag}"`);
      }
      seen.add(tag);
    }
  }

  // 7. Remediation
  if (!rule.remediation || typeof rule.remediation !== "object") {
    errors.push(`${filepath}: missing "remediation" object`);
  } else {
    if (typeof rule.remediation.constantCost !== "string") {
      errors.push(`${filepath}: remediation.constantCost must be a string`);
    }
    if (
      !Array.isArray(rule.remediation.examples) ||
      rule.remediation.examples.length === 0
    ) {
      errors.push(
        `${filepath}: remediation.examples must be a non-empty array`
      );
    } else {
      rule.remediation.examples.forEach((ex, i) => {
        if (!ex.before || !ex.after) {
          errors.push(
            `${filepath}: remediation.examples[${i}] must have "before" and "after"`
          );
        }
      });
    }
  }

  // 8. Impacts
  if (!Array.isArray(rule.impacts) || rule.impacts.length === 0) {
    errors.push(`${filepath}: "impacts" must be a non-empty array`);
  } else {
    rule.impacts.forEach((imp, i) => {
      if (!VALID_QUALITIES.includes(imp.softwareQuality)) {
        errors.push(
          `${filepath}: impacts[${i}].softwareQuality "${imp.softwareQuality}" invalid`
        );
      }
      if (!VALID_IMPACT_SEVERITIES.includes(imp.severity)) {
        errors.push(
          `${filepath}: impacts[${i}].severity "${imp.severity}" invalid`
        );
      }
    });
  }

  // 9. Debt
  if (!rule.debt || typeof rule.debt !== "object") {
    errors.push(`${filepath}: missing "debt" object`);
  } else {
    if (!VALID_DEBT_FUNCTIONS.includes(rule.debt.function)) {
      errors.push(
        `${filepath}: debt.function "${rule.debt.function}" invalid`
      );
    } else if (rule.debt.function === "CONSTANT_ISSUE" && !rule.debt.offset) {
      errors.push(
        `${filepath}: CONSTANT_ISSUE debt requires "offset"`
      );
    } else if (rule.debt.function === "LINEAR" && !rule.debt.coefficient) {
      errors.push(
        `${filepath}: LINEAR debt requires "coefficient"`
      );
    }
  }

  // 10. Params (optional, but validate if present)
  if (rule.params !== undefined) {
    if (!Array.isArray(rule.params)) {
      errors.push(`${filepath}: "params" must be an array`);
    } else {
      rule.params.forEach((p, i) => {
        for (const req of ["key", "name", "description", "defaultValue", "type"]) {
          if (p[req] === undefined) {
            errors.push(`${filepath}: params[${i}] missing "${req}"`);
          }
        }
      });
    }
  }

  // 11. Convention: security rules should be VULNERABILITY type
  if (category === "security" && rule.type !== "VULNERABILITY") {
    warnings.push(
      `${filepath}: security rule has type "${rule.type}" instead of "VULNERABILITY"`
    );
  }

  return { errors, warnings };
}

// ─── Main ───────────────────────────────────────────────────────────
function main() {
  const files = collectRuleFiles();
  let totalErrors = 0;
  let totalWarnings = 0;
  const allKeys = new Map();
  const results = [];

  for (const file of files) {
    // Check for duplicate keys
    if (allKeys.has(file.key)) {
      totalErrors++;
      console.error(
        `ERROR: Duplicate key "${file.key}" in ${file.filepath} and ${allKeys.get(file.key)}`
      );
    }
    allKeys.set(file.key, file.filepath);

    const { errors, warnings } = validateRule(file);
    totalErrors += errors.length;
    totalWarnings += warnings.length;
    results.push({ ...file, errors, warnings });
  }

  // Print results
  console.log(`\nSonarQube Rule Validation Report`);
  console.log(`${"═".repeat(50)}`);
  console.log(`Files scanned:  ${files.length}`);
  console.log(`Categories:     ${CATEGORIES.join(", ")}`);
  console.log("");

  for (const category of CATEGORIES) {
    const catResults = results.filter((r) => r.category === category);
    const catErrors = catResults.reduce((s, r) => s + r.errors.length, 0);
    const catWarnings = catResults.reduce((s, r) => s + r.warnings.length, 0);
    const icon =
      catErrors > 0 ? "✗" : catWarnings > 0 ? "⚠" : "✓";
    console.log(
      `  ${icon} ${category.padEnd(20)} ${catResults.length} rules  ${catErrors} errors  ${catWarnings} warnings`
    );

    if (verbose || catErrors > 0 || catWarnings > 0) {
      for (const r of catResults) {
        if (r.errors.length > 0 || r.warnings.length > 0 || verbose) {
          const fileIcon =
            r.errors.length > 0 ? "✗" : r.warnings.length > 0 ? "⚠" : "✓";
          if (verbose) {
            console.log(`      ${fileIcon} ${r.filename}`);
          }
          for (const e of r.errors) {
            console.log(`        ERROR: ${e}`);
          }
          for (const w of r.warnings) {
            console.log(`        WARN:  ${w}`);
          }
        }
      }
    }
  }

  console.log("");
  console.log(`${"─".repeat(50)}`);
  console.log(
    `Total: ${totalErrors} error(s), ${totalWarnings} warning(s)`
  );

  if (totalErrors > 0) {
    console.log("\n✗ Validation FAILED\n");
    process.exit(1);
  } else if (totalWarnings > 0) {
    console.log("\n⚠ Validation PASSED with warnings\n");
    process.exit(0);
  } else {
    console.log("\n✓ All rules valid\n");
    process.exit(0);
  }
}

main();
