#!/usr/bin/env python3
"""
Evaluate the token consumption of GitHub Copilot customization files in this repository.

Scans copilot-instructions.md, instruction files, skills, agents, and prompts,
then produces a CLI report estimating token usage and context load.
"""

import os
import sys
import glob
import math
from pathlib import Path

# Approximate tokens per character for English text (GPT-family models)
CHARS_PER_TOKEN = 4.0

# Thresholds for warnings
ALWAYS_ON_WARN_TOKENS = 8000
ALWAYS_ON_CRITICAL_TOKENS = 15000
TOTAL_WARN_TOKENS = 30000
TOTAL_CRITICAL_TOKENS = 60000


def estimate_tokens(text: str) -> int:
    """Estimate token count from character length."""
    return math.ceil(len(text) / CHARS_PER_TOKEN)


def read_file_safe(path: str) -> str:
    """Read file contents, returning empty string on failure."""
    try:
        with open(path, "r", encoding="utf-8") as f:
            return f.read()
    except (OSError, UnicodeDecodeError):
        return ""


def find_repo_root() -> Path:
    """Find the repository root by looking for .github directory."""
    current = Path(__file__).resolve().parent
    while current != current.parent:
        if (current / ".github").is_dir():
            return current
        current = current.parent
    # Fallback to script's parent's parent
    return Path(__file__).resolve().parent.parent


def scan_files(base_path: Path, pattern: str) -> list[dict]:
    """Scan files matching a glob pattern and return metadata."""
    results = []
    for filepath in sorted(glob.glob(str(base_path / pattern), recursive=True)):
        content = read_file_safe(filepath)
        rel_path = os.path.relpath(filepath, base_path)
        results.append({
            "path": rel_path,
            "bytes": len(content.encode("utf-8")),
            "tokens": estimate_tokens(content),
            "lines": content.count("\n") + 1 if content else 0,
        })
    return results


def has_apply_to(filepath: str) -> bool:
    """Check if an instruction file has applyTo frontmatter (scoped loading)."""
    content = read_file_safe(filepath)
    return "applyTo" in content[:500]


def print_section(title: str, files: list[dict], indent: str = "  "):
    """Print a formatted section of the report."""
    if not files:
        print(f"\n{'─' * 60}")
        print(f"  {title}: (none found)")
        return

    total_tokens = sum(f["tokens"] for f in files)
    total_bytes = sum(f["bytes"] for f in files)

    print(f"\n{'─' * 60}")
    print(f"  {title}")
    print(f"  {len(files)} file(s) | {total_tokens:,} tokens | {total_bytes:,} bytes")
    print(f"{'─' * 60}")
    print(f"{indent}{'File':<50} {'Tokens':>8} {'Bytes':>8}")
    print(f"{indent}{'─' * 50} {'─' * 8} {'─' * 8}")
    for f in files:
        name = f["path"] if len(f["path"]) <= 49 else "..." + f["path"][-46:]
        print(f"{indent}{name:<50} {f['tokens']:>8,} {f['bytes']:>8,}")
    print(f"{indent}{'─' * 50} {'─' * 8} {'─' * 8}")
    print(f"{indent}{'TOTAL':<50} {total_tokens:>8,} {total_bytes:>8,}")
    return total_tokens


def severity_indicator(tokens: int, warn: int, critical: int) -> str:
    """Return a severity indicator based on token count."""
    if tokens >= critical:
        return "🔴 CRITICAL"
    elif tokens >= warn:
        return "🟡 WARNING"
    else:
        return "🟢 OK"


def main():
    repo_root = find_repo_root()
    github_dir = repo_root / ".github"

    if not github_dir.is_dir():
        print("Error: Could not find .github directory.", file=sys.stderr)
        sys.exit(1)

    print("=" * 60)
    print("  COPILOT CONTEXT CONSUMPTION REPORT")
    print(f"  Repository: {repo_root.name}")
    print(f"  Scanned:    {github_dir}")
    print("=" * 60)

    # ─── 1. Always-loaded: copilot-instructions.md ───
    copilot_instructions = []
    ci_path = github_dir / "copilot-instructions.md"
    if ci_path.exists():
        content = read_file_safe(str(ci_path))
        copilot_instructions.append({
            "path": ".github/copilot-instructions.md",
            "bytes": len(content.encode("utf-8")),
            "tokens": estimate_tokens(content),
            "lines": content.count("\n") + 1,
        })

    print_section("ALWAYS LOADED — copilot-instructions.md", copilot_instructions)

    # ─── 2. Instruction files (.instructions.md) ───
    instructions_dir = github_dir / "instructions"
    instruction_files = []
    if instructions_dir.is_dir():
        for fp in sorted(instructions_dir.glob("*.instructions.md")):
            content = read_file_safe(str(fp))
            scoped = has_apply_to(str(fp))
            instruction_files.append({
                "path": os.path.relpath(str(fp), repo_root),
                "bytes": len(content.encode("utf-8")),
                "tokens": estimate_tokens(content),
                "lines": content.count("\n") + 1,
                "scoped": scoped,
            })

    scoped_count = sum(1 for f in instruction_files if f.get("scoped"))
    unscoped_count = len(instruction_files) - scoped_count

    print(f"\n{'─' * 60}")
    print(f"  INSTRUCTION FILES (.instructions.md)")
    total_inst_tokens = sum(f["tokens"] for f in instruction_files)
    total_inst_bytes = sum(f["bytes"] for f in instruction_files)
    print(f"  {len(instruction_files)} file(s) | {total_inst_tokens:,} tokens | {total_inst_bytes:,} bytes")
    print(f"  Scoped (applyTo): {scoped_count} | Unscoped (always loaded): {unscoped_count}")
    print(f"{'─' * 60}")
    print(f"  {'File':<44} {'Tokens':>7} {'Bytes':>7} {'Load':<10}")
    print(f"  {'─' * 44} {'─' * 7} {'─' * 7} {'─' * 10}")
    for f in instruction_files:
        name = f["path"] if len(f["path"]) <= 43 else "..." + f["path"][-40:]
        load = "on-demand" if f.get("scoped") else "ALWAYS"
        print(f"  {name:<44} {f['tokens']:>7,} {f['bytes']:>7,} {load:<10}")
    print(f"  {'─' * 44} {'─' * 7} {'─' * 7} {'─' * 10}")
    print(f"  {'TOTAL':<44} {total_inst_tokens:>7,} {total_inst_bytes:>7,}")

    # ─── 3. Skills ───
    skills_dir = github_dir / "skills"
    skill_files = []
    if skills_dir.is_dir():
        for skill_md in sorted(skills_dir.glob("*/SKILL.md")):
            content = read_file_safe(str(skill_md))
            skill_files.append({
                "path": os.path.relpath(str(skill_md), repo_root),
                "bytes": len(content.encode("utf-8")),
                "tokens": estimate_tokens(content),
                "lines": content.count("\n") + 1,
            })

    print_section("SKILLS (loaded on-demand when invoked)", skill_files)

    # ─── 4. Agents ───
    agents_dir = github_dir / "agents"
    agent_files = []
    if agents_dir.is_dir():
        for agent_md in sorted(agents_dir.glob("*.md")):
            content = read_file_safe(str(agent_md))
            agent_files.append({
                "path": os.path.relpath(str(agent_md), repo_root),
                "bytes": len(content.encode("utf-8")),
                "tokens": estimate_tokens(content),
                "lines": content.count("\n") + 1,
            })

    # Agent descriptions are always loaded (short stubs), full content on invocation
    agent_desc_tokens = 0
    for agent_md in sorted((agents_dir or Path()).glob("*.md")) if agents_dir and agents_dir.is_dir() else []:
        content = read_file_safe(str(agent_md))
        # Extract description line from frontmatter (typically short)
        for line in content.split("\n"):
            if line.startswith("description:"):
                agent_desc_tokens += estimate_tokens(line)
                break

    print_section("AGENTS (description always loaded; full body on invocation)", agent_files)
    print(f"  ℹ️  Always-on cost from agent descriptions: ~{agent_desc_tokens:,} tokens")

    # ─── 5. Prompt files ───
    prompts_dir = github_dir / "prompts"
    prompt_files = []
    if prompts_dir.is_dir():
        for prompt_md in sorted(prompts_dir.glob("*.prompt.md")):
            content = read_file_safe(str(prompt_md))
            prompt_files.append({
                "path": os.path.relpath(str(prompt_md), repo_root),
                "bytes": len(content.encode("utf-8")),
                "tokens": estimate_tokens(content),
                "lines": content.count("\n") + 1,
            })

    print_section("PROMPT FILES (user-triggered, never auto-loaded)", prompt_files)

    # ─── SUMMARY ───
    always_on_tokens = sum(f["tokens"] for f in copilot_instructions)
    always_on_tokens += sum(f["tokens"] for f in instruction_files if not f.get("scoped"))
    always_on_tokens += agent_desc_tokens  # agent descriptions

    on_demand_tokens = sum(f["tokens"] for f in instruction_files if f.get("scoped"))
    on_demand_tokens += sum(f["tokens"] for f in skill_files)
    on_demand_tokens += sum(f["tokens"] for f in agent_files)  # full agent bodies

    user_triggered_tokens = sum(f["tokens"] for f in prompt_files)

    total_all = always_on_tokens + on_demand_tokens + user_triggered_tokens

    print(f"\n{'=' * 60}")
    print(f"  SUMMARY")
    print(f"{'=' * 60}")
    print()
    print(f"  {'Category':<35} {'Tokens':>10} {'Status':<12}")
    print(f"  {'─' * 35} {'─' * 10} {'─' * 12}")
    print(f"  {'Always-on (every request)':<35} {always_on_tokens:>10,} {severity_indicator(always_on_tokens, ALWAYS_ON_WARN_TOKENS, ALWAYS_ON_CRITICAL_TOKENS)}")
    print(f"  {'On-demand (scoped/invoked)':<35} {on_demand_tokens:>10,} {'(not in base cost)'}")
    print(f"  {'User-triggered (prompts)':<35} {user_triggered_tokens:>10,} {'(not in base cost)'}")
    print(f"  {'─' * 35} {'─' * 10} {'─' * 12}")
    print(f"  {'TOTAL (if everything loaded)':<35} {total_all:>10,} {severity_indicator(total_all, TOTAL_WARN_TOKENS, TOTAL_CRITICAL_TOKENS)}")
    print()

    # ─── RECOMMENDATIONS ───
    print(f"  {'─' * 56}")
    print(f"  RECOMMENDATIONS")
    print(f"  {'─' * 56}")

    recommendations = []

    if always_on_tokens >= ALWAYS_ON_CRITICAL_TOKENS:
        recommendations.append(
            "🔴 Always-on context is very high. Consider trimming\n"
            "     copilot-instructions.md or scoping more content with applyTo."
        )
    elif always_on_tokens >= ALWAYS_ON_WARN_TOKENS:
        recommendations.append(
            "🟡 Always-on context is moderately high. Review\n"
            "     copilot-instructions.md for content that could be moved to skills."
        )

    if unscoped_count > 0:
        recommendations.append(
            f"🟡 {unscoped_count} instruction file(s) lack applyTo patterns and load\n"
            f"     on every request. Add applyTo to scope them."
        )

    if total_all >= TOTAL_CRITICAL_TOKENS:
        recommendations.append(
            "🔴 Total context is very large. If all files load simultaneously,\n"
            "     this may degrade response quality. Consider consolidating."
        )

    # Check for large individual files
    all_files = copilot_instructions + instruction_files + skill_files + agent_files
    large_files = [f for f in all_files if f["tokens"] > 3000]
    if large_files:
        names = ", ".join(os.path.basename(f["path"]) for f in large_files[:3])
        recommendations.append(
            f"ℹ️  {len(large_files)} file(s) exceed 3,000 tokens: {names}\n"
            f"     Consider splitting or trimming if they contain redundant content."
        )

    if not recommendations:
        recommendations.append(
            "🟢 Your setup looks well-optimized! No issues detected."
        )

    for i, rec in enumerate(recommendations, 1):
        print(f"  {i}. {rec}")

    print()
    print(f"{'=' * 60}")
    print(f"  Note: Token estimates use ~4 chars/token approximation.")
    print(f"  Actual tokenization varies by model.")
    print(f"{'=' * 60}")


if __name__ == "__main__":
    main()
