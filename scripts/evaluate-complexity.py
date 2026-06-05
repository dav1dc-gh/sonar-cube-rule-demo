#!/usr/bin/env python3
"""
Copilot Configuration Complexity Evaluator

Analyzes the custom instructions, skills, agents, and prompts configured
in this workspace and produces a report estimating context overhead and
identifying potential clutter impacting AI assistant performance.

Usage:
    python3 scripts/evaluate-complexity.py          # Full report
    python3 scripts/evaluate-complexity.py --json   # JSON output
"""

import json
import os
import sys
from pathlib import Path
from dataclasses import dataclass, field
from typing import Optional

# ── Constants ──────────────────────────────────────────────────────────────────

# Approximate tokens-per-character ratio for English text/code
CHARS_PER_TOKEN = 4

# Thresholds for concern levels
TOKEN_BUDGET_ESTIMATE = 128_000  # Typical model context window
OVERHEAD_WARNING_PCT = 10        # Warn if overhead exceeds this % of budget
OVERHEAD_CRITICAL_PCT = 20       # Critical if overhead exceeds this %

# Known irrelevant extension patterns (skills/agents from extensions not
# related to this repo's purpose)
IRRELEVANT_EXTENSION_PATTERNS = [
    "migrate-java-to-azure",
    "modernize-azure",
    "modernize-java",
    "modernize-rearchitecture",
    "modernize-dotnet",
    "appmod-hooks",
    "building-java-knowledge-graph",
    "analyzing-architecture",
    "creating-implementation-plan",
    "implementing-code",
    "feature-inventory",
    "quality-gates",
    "runtime-validation",
    "dag-generation",
    "team-charters",
    "project-decomposition",
    "project-recon",
    "setting-up-constitution",
    "sharing-learnings",
    "clarifying-scenarios",
    "guidelines",
    "list-plans",
    "modernization-integration-tests",
    "assessment",
    "create-modernization-plan",
]

# ── Data Classes ───────────────────────────────────────────────────────────────


@dataclass
class ConfigItem:
    """Represents a single configuration component."""
    name: str
    category: str           # instructions, skills, agents, prompts, copilot-instructions
    file_path: str
    char_count: int
    token_estimate: int
    always_loaded: bool     # Whether it's always in context vs on-demand
    scoped: bool            # Whether it uses applyTo or similar scoping
    scope_pattern: Optional[str] = None
    description_tokens: int = 0  # Tokens from description alone (for skills/agents)


@dataclass
class AnalysisReport:
    """Full analysis report."""
    items: list = field(default_factory=list)
    total_always_loaded_tokens: int = 0
    total_on_demand_tokens: int = 0
    total_description_tokens: int = 0
    warnings: list = field(default_factory=list)
    recommendations: list = field(default_factory=list)


# ── Analysis Functions ─────────────────────────────────────────────────────────


def estimate_tokens(text: str) -> int:
    """Estimate token count from character length."""
    return len(text) // CHARS_PER_TOKEN


def extract_frontmatter(content: str) -> dict:
    """Extract YAML frontmatter fields from a markdown file."""
    frontmatter = {}
    if content.startswith("---"):
        parts = content.split("---", 2)
        if len(parts) >= 3:
            for line in parts[1].strip().split("\n"):
                if ":" in line:
                    key, _, value = line.partition(":")
                    frontmatter[key.strip()] = value.strip()
    return frontmatter


def scan_copilot_instructions(root: Path) -> list:
    """Find and analyze copilot-instructions.md."""
    items = []
    ci_path = root / ".github" / "copilot-instructions.md"
    if ci_path.exists():
        content = ci_path.read_text(encoding="utf-8")
        tokens = estimate_tokens(content)
        items.append(ConfigItem(
            name="copilot-instructions.md",
            category="copilot-instructions",
            file_path=str(ci_path.relative_to(root)),
            char_count=len(content),
            token_estimate=tokens,
            always_loaded=True,
            scoped=False,
        ))
    return items


def scan_instructions(root: Path) -> list:
    """Find and analyze .instructions.md files."""
    items = []
    instructions_dir = root / ".github" / "instructions"
    if not instructions_dir.exists():
        return items

    for f in sorted(instructions_dir.glob("*.instructions.md")):
        content = f.read_text(encoding="utf-8")
        frontmatter = extract_frontmatter(content)
        scope_pattern = frontmatter.get("applyTo")
        tokens = estimate_tokens(content)
        items.append(ConfigItem(
            name=f.name,
            category="instructions",
            file_path=str(f.relative_to(root)),
            char_count=len(content),
            token_estimate=tokens,
            always_loaded=False,  # Only loaded when applyTo matches
            scoped=bool(scope_pattern),
            scope_pattern=scope_pattern,
        ))
    return items


def scan_skills(root: Path) -> list:
    """Find and analyze skill definitions."""
    items = []
    skills_dir = root / ".github" / "skills"
    if not skills_dir.exists():
        return items

    for skill_dir in sorted(skills_dir.iterdir()):
        if not skill_dir.is_dir():
            continue
        skill_file = skill_dir / "SKILL.md"
        if not skill_file.exists():
            continue

        content = skill_file.read_text(encoding="utf-8")
        frontmatter = extract_frontmatter(content)
        description = frontmatter.get("description", "")
        desc_tokens = estimate_tokens(description)
        total_tokens = estimate_tokens(content)

        items.append(ConfigItem(
            name=skill_dir.name,
            category="skills",
            file_path=str(skill_file.relative_to(root)),
            char_count=len(content),
            token_estimate=total_tokens,
            always_loaded=False,  # Body loaded on demand
            scoped=False,
            description_tokens=desc_tokens,
        ))
    return items


def scan_agents(root: Path) -> list:
    """Find and analyze agent definitions."""
    items = []
    agents_dir = root / ".github" / "agents"
    if not agents_dir.exists():
        return items

    for f in sorted(agents_dir.glob("*.md")):
        content = f.read_text(encoding="utf-8")
        frontmatter = extract_frontmatter(content)
        description = frontmatter.get("description", "")
        desc_tokens = estimate_tokens(description)
        total_tokens = estimate_tokens(content)

        items.append(ConfigItem(
            name=f.stem,
            category="agents",
            file_path=str(f.relative_to(root)),
            char_count=len(content),
            token_estimate=total_tokens,
            always_loaded=False,  # Body loaded on invocation
            scoped=False,
            description_tokens=desc_tokens,
        ))
    return items


def scan_prompts(root: Path) -> list:
    """Find and analyze prompt files."""
    items = []
    prompts_dir = root / ".github" / "prompts"
    if not prompts_dir.exists():
        return items

    for f in sorted(prompts_dir.glob("*.prompt.md")):
        content = f.read_text(encoding="utf-8")
        tokens = estimate_tokens(content)
        items.append(ConfigItem(
            name=f.stem,
            category="prompts",
            file_path=str(f.relative_to(root)),
            char_count=len(content),
            token_estimate=tokens,
            always_loaded=False,  # Only loaded when explicitly invoked
            scoped=False,
        ))
    return items


def analyze(root: Path) -> AnalysisReport:
    """Run full analysis and produce report."""
    report = AnalysisReport()

    # Scan all components
    report.items.extend(scan_copilot_instructions(root))
    report.items.extend(scan_instructions(root))
    report.items.extend(scan_skills(root))
    report.items.extend(scan_agents(root))
    report.items.extend(scan_prompts(root))

    # Calculate totals
    for item in report.items:
        if item.always_loaded:
            report.total_always_loaded_tokens += item.token_estimate
        else:
            report.total_on_demand_tokens += item.token_estimate

        if item.description_tokens > 0:
            report.total_description_tokens += item.description_tokens

    # The "always in context" cost = always-loaded files + skill/agent descriptions
    always_in_context = report.total_always_loaded_tokens + report.total_description_tokens

    # Generate warnings
    overhead_pct = (always_in_context / TOKEN_BUDGET_ESTIMATE) * 100

    if overhead_pct > OVERHEAD_CRITICAL_PCT:
        report.warnings.append(
            f"CRITICAL: Always-in-context overhead is {overhead_pct:.1f}% of estimated "
            f"context budget ({always_in_context:,} tokens / {TOKEN_BUDGET_ESTIMATE:,})"
        )
    elif overhead_pct > OVERHEAD_WARNING_PCT:
        report.warnings.append(
            f"WARNING: Always-in-context overhead is {overhead_pct:.1f}% of estimated "
            f"context budget ({always_in_context:,} tokens / {TOKEN_BUDGET_ESTIMATE:,})"
        )

    # Check for unscoped instruction files
    unscoped = [i for i in report.items if i.category == "instructions" and not i.scoped]
    if unscoped:
        report.warnings.append(
            f"WARNING: {len(unscoped)} instruction file(s) lack applyTo scoping — "
            f"they load for ALL files: {', '.join(i.name for i in unscoped)}"
        )

    # Check for large individual files
    for item in report.items:
        if item.always_loaded and item.token_estimate > 3000:
            report.warnings.append(
                f"NOTE: '{item.name}' is large ({item.token_estimate:,} tokens) and "
                f"always loaded. Consider trimming if possible."
            )

    # Generate recommendations
    if overhead_pct <= OVERHEAD_WARNING_PCT:
        report.recommendations.append(
            "Your project configuration is well-sized. No changes needed."
        )

    scoped_count = sum(1 for i in report.items if i.scoped)
    total_instructions = sum(1 for i in report.items if i.category == "instructions")
    if total_instructions > 0 and scoped_count == total_instructions:
        report.recommendations.append(
            "All instruction files use applyTo scoping — good practice."
        )

    # Check for skills with very long descriptions
    verbose_skills = [
        i for i in report.items
        if i.category == "skills" and i.description_tokens > 100
    ]
    if verbose_skills:
        report.recommendations.append(
            f"{len(verbose_skills)} skill(s) have descriptions over 100 tokens. "
            f"Shorter descriptions reduce always-in-context overhead."
        )

    return report


# ── Output Formatting ──────────────────────────────────────────────────────────


def print_report(report: AnalysisReport) -> None:
    """Print a formatted terminal report."""
    print()
    print("=" * 70)
    print("  COPILOT CONFIGURATION COMPLEXITY REPORT")
    print("=" * 70)
    print()

    # Summary table
    categories = {}
    for item in report.items:
        cat = item.category
        if cat not in categories:
            categories[cat] = {"count": 0, "tokens": 0, "desc_tokens": 0}
        categories[cat]["count"] += 1
        categories[cat]["tokens"] += item.token_estimate
        categories[cat]["desc_tokens"] += item.description_tokens

    print("┌─────────────────────────┬───────┬──────────┬─────────────────────┐")
    print("│ Component               │ Count │ Tokens   │ Always in Context   │")
    print("├─────────────────────────┼───────┼──────────┼─────────────────────┤")

    for cat, data in categories.items():
        always = data["tokens"] if cat == "copilot-instructions" else data["desc_tokens"]
        always_str = f"{always:,}" if always > 0 else "on-demand"
        print(f"│ {cat:<23} │ {data['count']:>5} │ {data['tokens']:>8,} │ {always_str:>19} │")

    print("├─────────────────────────┼───────┼──────────┼─────────────────────┤")

    total_items = len(report.items)
    total_tokens = sum(i.token_estimate for i in report.items)
    always_in_context = report.total_always_loaded_tokens + report.total_description_tokens
    print(f"│ {'TOTAL':<23} │ {total_items:>5} │ {total_tokens:>8,} │ {always_in_context:>19,} │")
    print("└─────────────────────────┴───────┴──────────┴─────────────────────┘")

    overhead_pct = (always_in_context / TOKEN_BUDGET_ESTIMATE) * 100
    print()
    print(f"  Context budget estimate: {TOKEN_BUDGET_ESTIMATE:,} tokens")
    print(f"  Always-in-context cost:  {always_in_context:,} tokens ({overhead_pct:.1f}%)")
    print(f"  On-demand content:       {report.total_on_demand_tokens:,} tokens (loaded only when needed)")
    print()

    # Detailed breakdown
    print("─" * 70)
    print("  DETAILED BREAKDOWN")
    print("─" * 70)
    print()

    for cat in ["copilot-instructions", "instructions", "skills", "agents", "prompts"]:
        cat_items = [i for i in report.items if i.category == cat]
        if not cat_items:
            continue
        print(f"  [{cat.upper()}]")
        for item in cat_items:
            scope_info = f" (scoped: {item.scope_pattern})" if item.scope_pattern else ""
            load_info = "always" if item.always_loaded else "on-demand"
            desc_info = f", desc={item.description_tokens}tok" if item.description_tokens else ""
            print(f"    • {item.name:<40} {item.token_estimate:>6} tok  [{load_info}{desc_info}]{scope_info}")
        print()

    # Warnings
    if report.warnings:
        print("─" * 70)
        print("  WARNINGS")
        print("─" * 70)
        print()
        for w in report.warnings:
            print(f"  ⚠  {w}")
        print()

    # Recommendations
    if report.recommendations:
        print("─" * 70)
        print("  RECOMMENDATIONS")
        print("─" * 70)
        print()
        for r in report.recommendations:
            print(f"  →  {r}")
        print()

    # Verdict
    print("─" * 70)
    print("  VERDICT")
    print("─" * 70)
    print()
    if overhead_pct <= OVERHEAD_WARNING_PCT:
        print("  ✓  Configuration is lean and well-organized. No performance concerns.")
    elif overhead_pct <= OVERHEAD_CRITICAL_PCT:
        print("  ⚠  Moderate overhead detected. Review warnings above for optimization.")
    else:
        print("  ✗  Significant overhead. Configuration is likely impacting performance.")
    print()
    print("=" * 70)
    print()


def print_json(report: AnalysisReport) -> None:
    """Print report as JSON."""
    always_in_context = report.total_always_loaded_tokens + report.total_description_tokens
    output = {
        "summary": {
            "total_items": len(report.items),
            "total_tokens": sum(i.token_estimate for i in report.items),
            "always_in_context_tokens": always_in_context,
            "on_demand_tokens": report.total_on_demand_tokens,
            "context_budget_estimate": TOKEN_BUDGET_ESTIMATE,
            "overhead_percentage": round(
                (always_in_context / TOKEN_BUDGET_ESTIMATE) * 100, 1
            ),
        },
        "items": [
            {
                "name": i.name,
                "category": i.category,
                "file_path": i.file_path,
                "char_count": i.char_count,
                "token_estimate": i.token_estimate,
                "always_loaded": i.always_loaded,
                "scoped": i.scoped,
                "scope_pattern": i.scope_pattern,
                "description_tokens": i.description_tokens,
            }
            for i in report.items
        ],
        "warnings": report.warnings,
        "recommendations": report.recommendations,
    }
    print(json.dumps(output, indent=2))


# ── Main ───────────────────────────────────────────────────────────────────────


def main():
    json_mode = "--json" in sys.argv

    # Find repo root (where .github/ lives)
    root = Path(__file__).resolve().parent.parent
    if not (root / ".github").is_dir():
        print("ERROR: Cannot find .github/ directory. Run from the repo root.", file=sys.stderr)
        sys.exit(1)

    report = analyze(root)

    if json_mode:
        print_json(report)
    else:
        print_report(report)

    # Exit with non-zero if critical warnings
    has_critical = any("CRITICAL" in w for w in report.warnings)
    sys.exit(1 if has_critical else 0)


if __name__ == "__main__":
    main()
