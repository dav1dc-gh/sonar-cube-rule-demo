#!/usr/bin/env node

/**
 * SonarQube Rule Catalog Generator
 *
 * Reads all rule JSON files and generates a RULES_CATALOG.md file
 * with a searchable, sortable summary of every rule in the repository.
 *
 * Usage:
 *   node scripts/generate-catalog.js
 *
 * This is useful for:
 *   - Quick reference without opening individual JSON files
 *   - Onboarding new contributors
 *   - Reviewing rule coverage before importing into SonarQube
 *   - Spotting gaps or overlaps across categories
 */

const fs = require("fs");
const path = require("path");

const RULES_DIR = path.resolve(__dirname, "..", "rules");
const OUTPUT = path.resolve(__dirname, "..", "RULES_CATALOG.md");
const CATEGORIES = ["security", "code-smells", "performance", "maintainability"];

function loadRules() {
  const rules = [];
  for (const category of CATEGORIES) {
    const dir = path.join(RULES_DIR, category);
    if (!fs.existsSync(dir)) continue;
    for (const file of fs.readdirSync(dir).filter((f) => f.endsWith(".json"))) {
      const filepath = path.join(dir, file);
      const rule = JSON.parse(fs.readFileSync(filepath, "utf-8"));
      rules.push({ ...rule, _category: category, _file: `rules/${category}/${file}` });
    }
  }
  return rules;
}

function severityBadge(severity) {
  const map = {
    BLOCKER: "🔴",
    CRITICAL: "🟠",
    MAJOR: "🟡",
    MINOR: "🔵",
    INFO: "⚪",
  };
  return `${map[severity] || "❓"} ${severity}`;
}

function generateMarkdown(rules) {
  const now = new Date().toISOString().split("T")[0];
  let md = `# SonarQube Rules Catalog\n\n`;
  md += `> Auto-generated on ${now} by \`scripts/generate-catalog.js\`.  \n`;
  md += `> **${rules.length} rules** across ${CATEGORIES.length} categories.\n\n`;

  // Summary table
  md += `## Summary\n\n`;
  md += `| Category | Rules | Blocker | Critical | Major | Minor | Info |\n`;
  md += `|----------|------:|--------:|---------:|------:|------:|-----:|\n`;

  for (const cat of CATEGORIES) {
    const catRules = rules.filter((r) => r._category === cat);
    const count = (sev) => catRules.filter((r) => r.severity === sev).length;
    md += `| **${cat}** | ${catRules.length} | ${count("BLOCKER")} | ${count("CRITICAL")} | ${count("MAJOR")} | ${count("MINOR")} | ${count("INFO")} |\n`;
  }

  const total = rules.length;
  const gc = (sev) => rules.filter((r) => r.severity === sev).length;
  md += `| **TOTAL** | **${total}** | **${gc("BLOCKER")}** | **${gc("CRITICAL")}** | **${gc("MAJOR")}** | **${gc("MINOR")}** | **${gc("INFO")}** |\n\n`;

  // Full rule table
  md += `## All Rules\n\n`;
  md += `| # | Key | Name | Severity | Type | Tags | Params | Status |\n`;
  md += `|--:|-----|------|----------|------|------|-------:|--------|\n`;

  rules.forEach((r, i) => {
    const paramCount = r.params ? r.params.length : 0;
    const tags = r.tags.map((t) => `\`${t}\``).join(" ");
    md += `| ${i + 1} | [\`${r.key}\`](${r._file}) | ${r.name} | ${severityBadge(r.severity)} | ${r.type} | ${tags} | ${paramCount} | ${r.status} |\n`;
  });

  md += `\n`;

  // Per-category detail sections
  for (const cat of CATEGORIES) {
    const catRules = rules.filter((r) => r._category === cat);
    md += `## ${cat.charAt(0).toUpperCase() + cat.slice(1)} (${catRules.length} rules)\n\n`;

    for (const rule of catRules) {
      md += `### ${rule.name}\n\n`;
      md += `- **Key:** \`${rule.key}\`\n`;
      md += `- **File:** [\`${rule._file}\`](${rule._file})\n`;
      md += `- **Severity:** ${severityBadge(rule.severity)}\n`;
      md += `- **Type:** ${rule.type}\n`;
      md += `- **Tags:** ${rule.tags.map((t) => `\`${t}\``).join(", ")}\n`;
      md += `- **Remediation cost:** ${rule.remediation.constantCost}\n`;
      md += `- **Debt:** ${rule.debt.function}${rule.debt.offset ? ` (offset: ${rule.debt.offset})` : ""}${rule.debt.coefficient ? ` (coefficient: ${rule.debt.coefficient})` : ""}\n`;
      md += `- **Impacts:** ${rule.impacts.map((i) => `${i.softwareQuality}: ${i.severity}`).join(", ")}\n`;

      if (rule.params && rule.params.length > 0) {
        md += `- **Parameters:**\n`;
        for (const p of rule.params) {
          md += `  - \`${p.key}\` (${p.type}) — ${p.description} *(default: ${p.defaultValue})*\n`;
        }
      }

      md += `\n> ${rule.description}\n\n`;
    }
  }

  return md;
}

function main() {
  const rules = loadRules();
  const markdown = generateMarkdown(rules);
  fs.writeFileSync(OUTPUT, markdown, "utf-8");
  console.log(`✓ Generated ${OUTPUT} with ${rules.length} rules`);
}

main();
