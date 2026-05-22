#!/usr/bin/env python3
"""Analyze token consumption of VS Code Copilot customization files."""

import os
import re
import sys
from pathlib import Path

# Approximate token count: ~4 chars per token for English text
CHARS_PER_TOKEN = 4

REPO_ROOT = Path(__file__).resolve().parent.parent


def estimate_tokens(text: str) -> int:
    """Rough token estimate based on character count."""
    return len(text) // CHARS_PER_TOKEN


def scan_files(base: Path, pattern: str = "**/*") -> list[tuple[Path, int, int]]:
    """Return list of (path, bytes, estimated_tokens) for matching files."""
    results = []
    for f in sorted(base.glob(pattern)):
        if f.is_file() and f.suffix in (".md", ".yml", ".yaml", ".json", ".py"):
            content = f.read_text(errors="replace")
            tokens = estimate_tokens(content)
            results.append((f, len(content), tokens))
    return results


def print_section(title: str, files: list[tuple[Path, int, int]], root: Path):
    """Print a table of files with token estimates."""
    if not files:
        return
    total_tokens = sum(t for _, _, t in files)
    print(f"\n{'=' * 60}")
    print(f"  {title} ({len(files)} files, ~{total_tokens:,} tokens)")
    print(f"{'=' * 60}")
    print(f"  {'File':<50} {'Bytes':>7} {'~Tokens':>8}")
    print(f"  {'-'*50} {'-'*7} {'-'*8}")
    for path, size, tokens in sorted(files, key=lambda x: -x[2]):
        rel = path.relative_to(root)
        name = str(rel)
        if len(name) > 50:
            name = "..." + name[-47:]
        print(f"  {name:<50} {size:>7,} {tokens:>8,}")
    print(f"  {'TOTAL':<50} {sum(s for _, s, _ in files):>7,} {total_tokens:>8,}")


def main():
    root = REPO_ROOT
    print(f"Copilot Customization Token Analysis")
    print(f"Repository: {root}")
    print(f"Estimation: ~1 token per {CHARS_PER_TOKEN} characters\n")

    # 1. copilot-instructions.md
    instructions_files = []
    for candidate in [
        root / ".github" / "copilot-instructions.md",
        root / ".copilot-instructions.md",
    ]:
        if candidate.exists():
            content = candidate.read_text()
            instructions_files.append((candidate, len(content), estimate_tokens(content)))

    print_section("Custom Instructions (always loaded)", instructions_files, root)

    # 2. Skills
    skills_dir = root / ".github" / "skills"
    skill_files = []
    if skills_dir.exists():
        skill_files = scan_files(skills_dir)
    print_section("Skills (SKILL.md loaded on-demand, descriptions always in context)", skill_files, root)

    # 3. Prompt files
    prompts_dir = root / ".github" / "prompts"
    prompt_files = []
    if prompts_dir.exists():
        prompt_files = scan_files(prompts_dir)
    print_section("Prompt Files (loaded when invoked)", prompt_files, root)

    # 4. Agent definitions (AGENTS.md or .github/agents/)
    agent_files = []
    for candidate in [root / "AGENTS.md", root / ".github" / "AGENTS.md"]:
        if candidate.exists():
            content = candidate.read_text()
            agent_files.append((candidate, len(content), estimate_tokens(content)))
    agents_dir = root / ".github" / "agents"
    if agents_dir.exists():
        agent_files.extend(scan_files(agents_dir))
    print_section("Agent Definitions", agent_files, root)

    # Summary
    all_files = instructions_files + skill_files + prompt_files + agent_files
    always_loaded = instructions_files  # only instructions are always in context
    on_demand = skill_files + prompt_files + agent_files

    total_always = sum(t for _, _, t in always_loaded)
    total_on_demand = sum(t for _, _, t in on_demand)
    total_all = sum(t for _, _, t in all_files)

    print(f"\n{'=' * 60}")
    print(f"  SUMMARY")
    print(f"{'=' * 60}")
    print(f"  Always in context:  ~{total_always:>8,} tokens")
    print(f"  On-demand:          ~{total_on_demand:>8,} tokens")
    print(f"  Total if all loaded:~{total_all:>8,} tokens")
    print()

    # Guidance
    if total_always > 5000:
        print("  ⚠️  High always-loaded token count. Consider trimming copilot-instructions.md.")
    elif total_always > 3000:
        print("  ℹ️  Moderate always-loaded tokens. Acceptable but could be optimized.")
    else:
        print("  ✅ Always-loaded token count is low. No action needed.")

    if total_all > 20000:
        print("  ⚠️  Total customization is large. Ensure skills/prompts are well-scoped.")
    else:
        print("  ✅ Total customization size is manageable.")

    print()


if __name__ == "__main__":
    main()
