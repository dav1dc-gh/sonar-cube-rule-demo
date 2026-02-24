#!/usr/bin/env node

/**
 * Custom Instructions Drift Detector
 *
 * Compares the actual rule files on disk with what's documented in each
 * path-specific .copilot-instructions.md file to detect drift.
 *
 * Outputs a JSON report: { "<category>": { added: [], removed: [], changed: [], ruleCount: N } }
 *
 * Usage:
 *   node .github/skills/custom-instructions-sync/detect-drift.js
 *   node .github/skills/custom-instructions-sync/detect-drift.js --json
 */

const fs = require("fs");
const path = require("path");

const RULES_DIR = path.resolve(__dirname, "..", "..", "..", "rules");
const CATEGORIES = ["security", "code-smells", "performance", "maintainability"];
const jsonOnly = process.argv.includes("--json");

// ─── Load actual rules from disk ────────────────────────────────────
function loadActualRules(category) {
  const dir = path.join(RULES_DIR, category);
  if (!fs.existsSync(dir)) return {};
  const rules = {};
  for (const file of fs.readdirSync(dir).filter((f) => f.endsWith(".json"))) {
    try {
      const rule = JSON.parse(
        fs.readFileSync(path.join(dir, file), "utf-8")
      );
      rules[rule.key] = {
        key: rule.key,
        name: rule.name,
        severity: rule.severity,
        type: rule.type,
        tags: rule.tags,
      };
    } catch (e) {
      // skip invalid JSON
    }
  }
  return rules;
}

// ─── Extract documented rules from instructions ─────────────────────
function loadDocumentedRules(category) {
  const instructionsPath = path.join(
    RULES_DIR,
    category,
    ".copilot-instructions.md"
  );
  if (!fs.existsSync(instructionsPath)) {
    return { found: false, keys: new Set() };
  }
  const content = fs.readFileSync(instructionsPath, "utf-8");

  // Extract rule keys from table rows like "| `sql-injection` |" or
  // from lines mentioning .json files like "sql-injection.json"
  const keys = new Set();

  // Known schema field names and other non-rule terms to exclude
  const NON_RULE_TERMS = new Set([
    "type", "severity", "tags", "key", "name", "description", "status",
    "debt", "params", "impacts", "remediation", "offset", "coefficient",
    "function", "before", "after", "examples", "default-value",
    "software-quality", "constant-cost", "default-severity",
  ]);

  function addIfValid(term) {
    // Rule keys must contain at least one hyphen (all real rule keys do)
    // and must not be a known schema field name
    if (term.includes("-") && !NON_RULE_TERMS.has(term)) {
      keys.add(term);
    }
  }

  // Pattern 1: Markdown table rows with backtick keys
  const tablePattern = /\|\s*`([a-z][a-z0-9-]*)`\s*\|/g;
  let match;
  while ((match = tablePattern.exec(content)) !== null) {
    addIfValid(match[1]);
  }

  // Pattern 2: References to .json files
  const jsonPattern = /([a-z][a-z0-9-]+)\.json/g;
  while ((match = jsonPattern.exec(content)) !== null) {
    addIfValid(match[1]);
  }

  // Pattern 3: Bold rule names in list items like "- **sql-injection**"
  const boldPattern = /[-*]\s+\*\*([a-z][a-z0-9-]*)\*\*/g;
  while ((match = boldPattern.exec(content)) !== null) {
    addIfValid(match[1]);
  }

  return { found: true, keys };
}

// ─── Compute drift per category ─────────────────────────────────────
function computeDrift() {
  const report = {};
  let totalDrift = 0;

  // Build a set of all rule keys across all categories for cross-ref detection
  const allRuleKeys = new Set();
  for (const category of CATEGORIES) {
    const rules = loadActualRules(category);
    for (const key of Object.keys(rules)) {
      allRuleKeys.add(key);
    }
  }

  for (const category of CATEGORIES) {
    const actual = loadActualRules(category);
    const documented = loadDocumentedRules(category);
    const actualKeys = new Set(Object.keys(actual));

    const added = [];
    const removed = [];

    if (documented.found) {
      // Rules on disk but not in instructions
      for (const key of actualKeys) {
        if (!documented.keys.has(key)) {
          added.push({
            key,
            name: actual[key].name,
            severity: actual[key].severity,
          });
        }
      }
      // Rules in instructions but not on disk (skip cross-category references)
      for (const key of documented.keys) {
        if (!actualKeys.has(key) && !allRuleKeys.has(key)) {
          removed.push({ key });
        }
      }
    }

    const hasDrift = added.length > 0 || removed.length > 0 || !documented.found;

    report[category] = {
      instructionsExist: documented.found,
      ruleCount: actualKeys.size,
      documentedCount: documented.keys.size,
      added,
      removed,
      hasDrift,
    };

    if (hasDrift) totalDrift++;
  }

  return { categories: report, totalDrift, totalCategories: CATEGORIES.length };
}

// ─── Main ───────────────────────────────────────────────────────────
const report = computeDrift();

if (jsonOnly) {
  console.log(JSON.stringify(report, null, 2));
} else {
  console.log(`\n=== Custom Instructions Drift Report ===\n`);
  console.log(
    `Categories with drift: ${report.totalDrift}/${report.totalCategories}\n`
  );

  for (const [category, data] of Object.entries(report.categories)) {
    const status = data.hasDrift ? "⚠️  DRIFT" : "✅ IN SYNC";
    console.log(
      `${status}  ${category} (${data.ruleCount} rules on disk, ${data.documentedCount} documented)`
    );

    if (!data.instructionsExist) {
      console.log(
        `         ❌ No .copilot-instructions.md file found`
      );
    }
    if (data.added.length > 0) {
      console.log(`         + Added (not in instructions):`);
      for (const r of data.added) {
        console.log(`           ${r.key} (${r.severity})`);
      }
    }
    if (data.removed.length > 0) {
      console.log(`         - Removed (in instructions but not on disk):`);
      for (const r of data.removed) {
        console.log(`           ${r.key}`);
      }
    }
  }
  console.log();
}

process.exit(report.totalDrift > 0 ? 1 : 0);
