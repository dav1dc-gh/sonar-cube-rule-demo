#!/usr/bin/env node

/**
 * SonarQube Rule Index Generator
 *
 * Reads all rule JSON files and generates a machine-readable index at
 * rules/index.json. This provides a single-file manifest that tooling
 * can consume without globbing the filesystem.
 *
 * Usage:
 *   node .github/skills/catalog-index-refresh/generate-index.js
 */

const fs = require("fs");
const path = require("path");

const RULES_DIR = path.resolve(__dirname, "..", "..", "..", "rules");
const OUTPUT = path.resolve(RULES_DIR, "index.json");
const CATEGORIES = ["security", "code-smells", "performance", "maintainability"];

function loadRules() {
  const rules = [];
  for (const category of CATEGORIES) {
    const dir = path.join(RULES_DIR, category);
    if (!fs.existsSync(dir)) continue;
    for (const file of fs.readdirSync(dir).filter((f) => f.endsWith(".json"))) {
      // Skip the index file itself
      if (file === "index.json") continue;
      try {
        const filepath = path.join(dir, file);
        const rule = JSON.parse(fs.readFileSync(filepath, "utf-8"));
        rules.push({
          key: rule.key,
          name: rule.name,
          category: category,
          severity: rule.severity,
          type: rule.type,
          tags: rule.tags || [],
          status: rule.status || "READY",
          paramCount: rule.params ? rule.params.length : 0,
          remediationCost: rule.remediation
            ? rule.remediation.constantCost
            : null,
          file: `rules/${category}/${file}`,
        });
      } catch (e) {
        console.error(`  ⚠ Skipping ${category}/${file}: ${e.message}`);
      }
    }
  }
  return rules;
}

// ─── Main ───────────────────────────────────────────────────────────
const rules = loadRules();

// Sort by category then key for stable output
rules.sort((a, b) => {
  if (a.category !== b.category) return a.category.localeCompare(b.category);
  return a.key.localeCompare(b.key);
});

fs.writeFileSync(OUTPUT, JSON.stringify(rules, null, 2) + "\n", "utf-8");

// Summary
const byCat = {};
for (const r of rules) {
  byCat[r.category] = (byCat[r.category] || 0) + 1;
}
const breakdown = Object.entries(byCat)
  .map(([cat, count]) => `${cat}: ${count}`)
  .join(", ");

console.log(
  `✅ Generated index with ${rules.length} rules across ${Object.keys(byCat).length} categories (${breakdown})`
);
console.log(`   → ${OUTPUT}`);
