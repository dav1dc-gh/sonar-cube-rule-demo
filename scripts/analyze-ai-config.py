#!/usr/bin/env python3
"""
Analyze GenAI configuration files in this repository and report on token usage.

Scans copilot-instructions.md, skills, agents, and prompt files to estimate
the context window overhead they impose on the AI assistant.
"""

import os
import re
import sys
from pathlib import Path

# Approximate token ratio: ~4 characters per token for English/Markdown text
CHARS_PER_TOKEN = 4

# Typical context window sizes for reference
CONTEXT_WINDOWS = {
    "GPT-4o / Claude Sonnet": 128_000,
    "Claude Opus": 200_000,
}

# Thresholds for health assessment
THRESHOLDS = {
    "healthy_pct": 5.0,       # <5% of context = healthy
    "moderate_pct": 10.0,     # 5-10% = moderate
    # >10% = heavy
    "large_file_tokens": 3000,  # individual file warning threshold
}


def estimate_tokens(text: str) -> int:
    """Estimate token count from character length."""
    return len(text) // CHARS_PER_TOKEN


def extract_frontmatter(text: str) -> dict:
    """Extract YAML frontmatter fields from a markdown file."""
    fields = {}
    match = re.match(r"^---\s*\n(.*?)\n---", text, re.DOTALL)
    if match:
        for line in match.group(1).splitlines():
            if ":" in line:
                key, _, value = line.partition(":")
                fields[key.strip()] = value.strip()
    return fields


def extract_description_from_frontmatter(text: str) -> str:
    """Get the description field from frontmatter."""
    fm = extract_frontmatter(text)
    return fm.get("description", "")


def scan_directory(base_path: Path) -> dict:
    """Scan the .github directory for all AI config files and categorize them."""
    results = {
        "instructions": [],
        "skills": [],
        "agents": [],
        "prompts": [],
    }

    github_dir = base_path / ".github"
    if not github_dir.exists():
        print(f"ERROR: {github_dir} not found.", file=sys.stderr)
        sys.exit(1)

    # 1. copilot-instructions.md (always loaded)
    instructions_file = github_dir / "copilot-instructions.md"
    if instructions_file.exists():
        content = instructions_file.read_text(encoding="utf-8")
        results["instructions"].append({
            "path": str(instructions_file.relative_to(base_path)),
            "chars": len(content),
            "tokens": estimate_tokens(content),
            "loading": "always",
            "description": "Main copilot custom instructions",
        })

    # 2. Skills (deferred — only descriptor loaded always)
    skills_dir = github_dir / "skills"
    if skills_dir.exists():
        for skill_dir in sorted(skills_dir.iterdir()):
            if not skill_dir.is_dir():
                continue
            skill_file = skill_dir / "SKILL.md"
            if skill_file.exists():
                content = skill_file.read_text(encoding="utf-8")
                desc = extract_description_from_frontmatter(content)
                # The descriptor (name + description + path) is always loaded
                descriptor_text = f"{skill_dir.name}: {desc}"
                results["skills"].append({
                    "path": str(skill_file.relative_to(base_path)),
                    "chars": len(content),
                    "tokens": estimate_tokens(content),
                    "descriptor_chars": len(descriptor_text),
                    "descriptor_tokens": estimate_tokens(descriptor_text),
                    "loading": "deferred",
                    "name": skill_dir.name,
                    "description": desc[:80] + "..." if len(desc) > 80 else desc,
                })

    # 3. Agents (deferred — only descriptor loaded always)
    agents_dir = github_dir / "agents"
    if agents_dir.exists():
        for agent_file in sorted(agents_dir.glob("*.md")):
            content = agent_file.read_text(encoding="utf-8")
            desc = extract_description_from_frontmatter(content)
            descriptor_text = f"{agent_file.stem}: {desc}"
            results["agents"].append({
                "path": str(agent_file.relative_to(base_path)),
                "chars": len(content),
                "tokens": estimate_tokens(content),
                "descriptor_chars": len(descriptor_text),
                "descriptor_tokens": estimate_tokens(descriptor_text),
                "loading": "deferred",
                "name": agent_file.stem,
                "description": desc[:80] + "..." if len(desc) > 80 else desc,
            })

    # 4. Prompt files (on-demand only)
    prompts_dir = github_dir / "prompts"
    if prompts_dir.exists():
        for prompt_file in sorted(prompts_dir.glob("*.prompt.md")):
            content = prompt_file.read_text(encoding="utf-8")
            results["prompts"].append({
                "path": str(prompt_file.relative_to(base_path)),
                "chars": len(content),
                "tokens": estimate_tokens(content),
                "loading": "on-demand",
                "name": prompt_file.stem.replace(".prompt", ""),
            })

    return results


def compute_summary(results: dict) -> dict:
    """Compute aggregate statistics."""
    always_tokens = 0
    deferred_tokens = 0
    on_demand_tokens = 0
    descriptor_tokens = 0

    # Instructions are always loaded
    for item in results["instructions"]:
        always_tokens += item["tokens"]

    # Skills: descriptor always loaded, full content deferred
    for item in results["skills"]:
        descriptor_tokens += item["descriptor_tokens"]
        deferred_tokens += item["tokens"]

    # Agents: descriptor always loaded, full content deferred
    for item in results["agents"]:
        descriptor_tokens += item["descriptor_tokens"]
        deferred_tokens += item["tokens"]

    # Prompts: fully on-demand
    for item in results["prompts"]:
        on_demand_tokens += item["tokens"]

    always_tokens += descriptor_tokens

    total_content_tokens = (
        sum(i["tokens"] for i in results["instructions"])
        + sum(i["tokens"] for i in results["skills"])
        + sum(i["tokens"] for i in results["agents"])
        + sum(i["tokens"] for i in results["prompts"])
    )

    return {
        "always_loaded_tokens": always_tokens,
        "descriptor_tokens": descriptor_tokens,
        "deferred_tokens": deferred_tokens,
        "on_demand_tokens": on_demand_tokens,
        "total_content_tokens": total_content_tokens,
        "counts": {
            "instructions": len(results["instructions"]),
            "skills": len(results["skills"]),
            "agents": len(results["agents"]),
            "prompts": len(results["prompts"]),
        },
    }


def assess_health(summary: dict) -> str:
    """Return a health assessment based on context usage."""
    always = summary["always_loaded_tokens"]
    assessments = []

    for model, window in CONTEXT_WINDOWS.items():
        pct = (always / window) * 100
        if pct < THRESHOLDS["healthy_pct"]:
            status = "HEALTHY"
        elif pct < THRESHOLDS["moderate_pct"]:
            status = "MODERATE"
        else:
            status = "HEAVY"
        assessments.append((model, window, pct, status))

    return assessments


def print_report(results: dict, summary: dict, assessments: list):
    """Print the full analysis report."""
    print("=" * 70)
    print("  GenAI Configuration — Token Usage Analysis")
    print("=" * 70)
    print()

    # --- Summary ---
    print("## Summary")
    print(f"  Instructions files:  {summary['counts']['instructions']}")
    print(f"  Skills:              {summary['counts']['skills']}")
    print(f"  Agents:              {summary['counts']['agents']}")
    print(f"  Prompt files:        {summary['counts']['prompts']}")
    print(f"  Total config files:  {sum(summary['counts'].values())}")
    print()

    # --- Token Budget ---
    print("## Token Budget")
    print(f"  Always-loaded (per turn):    ~{summary['always_loaded_tokens']:,} tokens")
    print(f"    ├─ Instructions content:   ~{sum(i['tokens'] for i in results['instructions']):,} tokens")
    print(f"    └─ Skill/Agent descriptors:~{summary['descriptor_tokens']:,} tokens")
    print(f"  Deferred (on skill/agent invoke): ~{summary['deferred_tokens']:,} tokens")
    print(f"  On-demand (prompt files):    ~{summary['on_demand_tokens']:,} tokens")
    print(f"  Total all content:           ~{summary['total_content_tokens']:,} tokens")
    print()

    # --- Context Window Impact ---
    print("## Context Window Impact")
    print(f"  {'Model':<30} {'Window':>10} {'Used':>8} {'Pct':>7}  Status")
    print(f"  {'-'*30} {'-'*10} {'-'*8} {'-'*7}  {'-'*8}")
    for model, window, pct, status in assessments:
        print(f"  {model:<30} {window:>10,} {summary['always_loaded_tokens']:>8,} {pct:>6.2f}%  {status}")
    print()

    # --- Always-Loaded Breakdown ---
    print("## Always-Loaded Files (embedded every turn)")
    print(f"  {'File':<55} {'Chars':>7} {'~Tokens':>8}")
    print(f"  {'-'*55} {'-'*7} {'-'*8}")
    for item in results["instructions"]:
        print(f"  {item['path']:<55} {item['chars']:>7,} {item['tokens']:>8,}")
    print()

    # --- Skills ---
    print("## Skills (descriptor always loaded; full content deferred)")
    print(f"  {'Name':<30} {'Descriptor':>11} {'Full':>8} {'Full Chars':>11}")
    print(f"  {'-'*30} {'-'*11} {'-'*8} {'-'*11}")
    for item in results["skills"]:
        print(f"  {item['name']:<30} {item['descriptor_tokens']:>8,} tk {item['tokens']:>8,} {item['chars']:>9,} ch")
    total_desc = sum(i["descriptor_tokens"] for i in results["skills"])
    total_full = sum(i["tokens"] for i in results["skills"])
    print(f"  {'TOTAL':<30} {total_desc:>8,} tk {total_full:>8,}")
    print()

    # --- Agents ---
    print("## Agents (descriptor always loaded; full content deferred)")
    print(f"  {'Name':<30} {'Descriptor':>11} {'Full':>8} {'Full Chars':>11}")
    print(f"  {'-'*30} {'-'*11} {'-'*8} {'-'*11}")
    for item in results["agents"]:
        print(f"  {item['name']:<30} {item['descriptor_tokens']:>8,} tk {item['tokens']:>8,} {item['chars']:>9,} ch")
    total_desc = sum(i["descriptor_tokens"] for i in results["agents"])
    total_full = sum(i["tokens"] for i in results["agents"])
    print(f"  {'TOTAL':<30} {total_desc:>8,} tk {total_full:>8,}")
    print()

    # --- Prompts ---
    print("## Prompt Files (loaded only when user invokes)")
    print(f"  {'Name':<40} {'Chars':>7} {'~Tokens':>8}")
    print(f"  {'-'*40} {'-'*7} {'-'*8}")
    for item in results["prompts"]:
        print(f"  {item['name']:<40} {item['chars']:>7,} {item['tokens']:>8,}")
    total_prompt = sum(i["tokens"] for i in results["prompts"])
    print(f"  {'TOTAL':<40} {'':>7} {total_prompt:>8,}")
    print()

    # --- Warnings ---
    print("## Warnings")
    warnings = []
    for item in results["instructions"]:
        if item["tokens"] > THRESHOLDS["large_file_tokens"]:
            warnings.append(
                f"  ⚠ {item['path']} is large ({item['tokens']:,} tokens). "
                f"Consider trimming static content the AI can discover at runtime."
            )
    for item in results["skills"]:
        if item["tokens"] > THRESHOLDS["large_file_tokens"]:
            warnings.append(
                f"  ⚠ Skill '{item['name']}' full content is {item['tokens']:,} tokens. "
                f"This is loaded in full when the skill is invoked."
            )
    for item in results["agents"]:
        if item["tokens"] > THRESHOLDS["large_file_tokens"]:
            warnings.append(
                f"  ⚠ Agent '{item['name']}' is {item['tokens']:,} tokens. "
                f"Consider splitting into smaller focused agents."
            )

    if warnings:
        for w in warnings:
            print(w)
    else:
        print("  None — all files are within recommended size limits.")
    print()

    # --- Health Verdict ---
    worst_status = "HEALTHY"
    for _, _, _, status in assessments:
        if status == "HEAVY":
            worst_status = "HEAVY"
            break
        if status == "MODERATE":
            worst_status = "MODERATE"

    print("## Overall Verdict")
    if worst_status == "HEALTHY":
        print("  ✅ HEALTHY — Custom instructions use <5% of available context.")
        print("     No performance impact expected.")
    elif worst_status == "MODERATE":
        print("  ⚡ MODERATE — Custom instructions use 5-10% of context.")
        print("     Generally fine, but monitor if you add more config.")
    else:
        print("  🔴 HEAVY — Custom instructions use >10% of context.")
        print("     Consider reducing always-loaded content to avoid crowding out")
        print("     working context for complex tasks.")
    print()
    print("=" * 70)


def main():
    # Find repo root (script lives in scripts/)
    script_dir = Path(__file__).resolve().parent
    repo_root = script_dir.parent

    # Allow override via argument
    if len(sys.argv) > 1:
        repo_root = Path(sys.argv[1]).resolve()

    if not (repo_root / ".github").exists():
        print(f"ERROR: No .github directory found in {repo_root}", file=sys.stderr)
        sys.exit(1)

    print(f"Scanning: {repo_root}")
    print()

    results = scan_directory(repo_root)
    summary = compute_summary(results)
    assessments = assess_health(summary)
    print_report(results, summary, assessments)


if __name__ == "__main__":
    main()
