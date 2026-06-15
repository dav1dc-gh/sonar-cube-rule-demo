#!/usr/bin/env python3
"""
Analyze token usage of AI coding tool configuration files in this repository.

Scans .github/copilot-instructions.md, .github/agents/, .github/skills/, and
.github/prompts/ to estimate token counts and produce a summary report.

Token estimation uses a simple heuristic of ~4 characters per token (roughly
matching GPT/Claude tokenization for English prose and markdown).
"""

import os
import sys
from pathlib import Path
from dataclasses import dataclass, field

# Approximate characters per token (conservative estimate for English + markdown)
CHARS_PER_TOKEN = 4


@dataclass
class FileReport:
    path: str
    chars: int
    tokens: int
    loading: str  # "always-on" | "on-demand" | "explicit-invoke"


@dataclass
class CategoryReport:
    name: str
    files: list = field(default_factory=list)

    @property
    def total_tokens(self) -> int:
        return sum(f.tokens for f in self.files)

    @property
    def total_chars(self) -> int:
        return sum(f.chars for f in self.files)

    @property
    def always_on_tokens(self) -> int:
        return sum(f.tokens for f in self.files if f.loading == "always-on")


def estimate_tokens(text: str) -> int:
    """Estimate token count from text using chars/4 heuristic."""
    return max(1, len(text) // CHARS_PER_TOKEN)


def count_words(text: str) -> int:
    return len(text.split())


def find_repo_root() -> Path:
    """Walk up from script location to find .github/ directory."""
    current = Path(__file__).resolve().parent
    while current != current.parent:
        if (current / ".github").is_dir():
            return current
        current = current.parent
    # Fallback: assume script is in scripts/ under repo root
    return Path(__file__).resolve().parent.parent


def scan_file(filepath: Path, loading: str, repo_root: Path) -> FileReport:
    """Read a file and produce a token report."""
    text = filepath.read_text(encoding="utf-8", errors="replace")
    chars = len(text)
    tokens = estimate_tokens(text)
    rel_path = str(filepath.relative_to(repo_root))
    return FileReport(path=rel_path, chars=chars, tokens=tokens, loading=loading)


def scan_directory(dirpath: Path, loading: str, repo_root: Path, pattern: str = "*.md") -> list:
    """Scan all matching files in a directory."""
    reports = []
    if not dirpath.exists():
        return reports
    for f in sorted(dirpath.rglob(pattern)):
        if f.is_file():
            reports.append(scan_file(f, loading, repo_root))
    return reports


def extract_frontmatter_description(filepath: Path) -> str:
    """Extract the description field from YAML frontmatter if present."""
    text = filepath.read_text(encoding="utf-8", errors="replace")
    lines = text.split("\n")
    if not lines or lines[0].strip() != "---":
        return ""
    for i, line in enumerate(lines[1:], 1):
        if line.strip() == "---":
            break
        if line.startswith("description:"):
            return line[len("description:"):].strip()
    return ""


def format_tokens(tokens: int) -> str:
    """Format token count with K suffix for readability."""
    if tokens >= 1000:
        return f"{tokens / 1000:.1f}K"
    return str(tokens)


def format_bar(tokens: int, max_tokens: int, width: int = 30) -> str:
    """Create a visual bar chart."""
    if max_tokens == 0:
        return ""
    filled = int((tokens / max_tokens) * width)
    return "█" * filled + "░" * (width - filled)


def print_report(categories: list, repo_root: Path):
    """Print the full analysis report."""
    all_files = [f for cat in categories for f in cat.files]
    total_tokens = sum(f.tokens for f in all_files)
    always_on_tokens = sum(f.tokens for f in all_files if f.loading == "always-on")
    on_demand_tokens = sum(f.tokens for f in all_files if f.loading == "on-demand")
    explicit_tokens = sum(f.tokens for f in all_files if f.loading == "explicit-invoke")

    print("=" * 70)
    print("  AI Configuration Token Usage Analysis")
    print("=" * 70)
    print(f"\n  Repository: {repo_root.name}")
    print(f"  Config root: .github/")
    print(f"  Total config files: {len(all_files)}")
    print(f"  Total estimated tokens: {format_tokens(total_tokens)}")
    print()

    # Loading impact summary
    print("─" * 70)
    print("  CONTEXT LOADING IMPACT")
    print("─" * 70)
    print()
    print(f"  {'Loading Type':<20} {'Tokens':>10} {'% of Total':>12}  Description")
    print(f"  {'─' * 20} {'─' * 10} {'─' * 12}  {'─' * 30}")
    print(f"  {'Always-on':<20} {format_tokens(always_on_tokens):>10} "
          f"{always_on_tokens / total_tokens * 100 if total_tokens else 0:>11.1f}%  "
          f"Loaded into every conversation turn")
    print(f"  {'On-demand':<20} {format_tokens(on_demand_tokens):>10} "
          f"{on_demand_tokens / total_tokens * 100 if total_tokens else 0:>11.1f}%  "
          f"Loaded when skill/agent is activated")
    print(f"  {'Explicit-invoke':<20} {format_tokens(explicit_tokens):>10} "
          f"{explicit_tokens / total_tokens * 100 if total_tokens else 0:>11.1f}%  "
          f"Only loaded when user invokes prompt")
    print()

    # Per-category breakdown
    print("─" * 70)
    print("  PER-CATEGORY BREAKDOWN")
    print("─" * 70)

    max_cat_tokens = max(cat.total_tokens for cat in categories) if categories else 1

    for cat in categories:
        print(f"\n  ┌─ {cat.name} ({len(cat.files)} files, ~{format_tokens(cat.total_tokens)} tokens)")
        print(f"  │  Always-on: ~{format_tokens(cat.always_on_tokens)} tokens")
        print(f"  │  {format_bar(cat.total_tokens, max_cat_tokens)}")
        print(f"  │")
        for f in sorted(cat.files, key=lambda x: x.tokens, reverse=True):
            loading_icon = {"always-on": "●", "on-demand": "◐", "explicit-invoke": "○"}[f.loading]
            print(f"  │  {loading_icon} {f.path:<55} {format_tokens(f.tokens):>6}")
        print(f"  └{'─' * 68}")

    # Recommendations
    print()
    print("─" * 70)
    print("  RECOMMENDATIONS")
    print("─" * 70)
    print()

    # Flag large always-on files
    large_always_on = [f for f in all_files if f.loading == "always-on" and f.tokens > 1000]
    if large_always_on:
        print("  ⚠  Large always-on files (>1K tokens each):")
        for f in sorted(large_always_on, key=lambda x: x.tokens, reverse=True):
            print(f"     • {f.path} ({format_tokens(f.tokens)} tokens)")
        print("     → Consider trimming reference tables or moving detail to on-demand skills")
        print()

    # Flag large skill files
    large_skills = [f for f in all_files if f.loading == "on-demand" and f.tokens > 3000]
    if large_skills:
        print("  ⚠  Large on-demand skill files (>3K tokens each):")
        for f in sorted(large_skills, key=lambda x: x.tokens, reverse=True):
            print(f"     • {f.path} ({format_tokens(f.tokens)} tokens)")
        print("     → Consider splitting into focused sub-skills if content is broad")
        print()

    # Token budget context
    print("  ℹ  Context budget reference:")
    print(f"     • Your always-on cost: ~{format_tokens(always_on_tokens)} tokens/turn")
    print(f"     • Typical model context window: 128K-200K tokens")
    print(f"     • Your config uses {always_on_tokens / 128000 * 100:.2f}% of a 128K window")
    print(f"     • Rule of thumb: keep always-on config under 5K tokens")
    print()

    severity = "LOW"
    if always_on_tokens > 5000:
        severity = "HIGH"
    elif always_on_tokens > 3000:
        severity = "MEDIUM"

    print(f"  Overall impact severity: {severity}")
    print()

    # Legend
    print("─" * 70)
    print("  LEGEND")
    print("─" * 70)
    print("  ● Always-on    — Injected into system prompt every turn")
    print("  ◐ On-demand    — Loaded when the skill/agent is activated")
    print("  ○ Explicit     — Only loaded when user manually invokes the prompt")
    print("  Token estimate — ~4 characters per token (heuristic)")
    print("=" * 70)


def main():
    repo_root = find_repo_root()
    github_dir = repo_root / ".github"

    if not github_dir.exists():
        print(f"Error: .github/ directory not found at {repo_root}", file=sys.stderr)
        sys.exit(1)

    categories = []

    # 1. Custom instructions (always loaded)
    instructions_file = github_dir / "copilot-instructions.md"
    cat_instructions = CategoryReport(name="Custom Instructions (.github/copilot-instructions.md)")
    if instructions_file.exists():
        cat_instructions.files.append(
            scan_file(instructions_file, "always-on", repo_root)
        )
    categories.append(cat_instructions)

    # 2. Agents (on-demand — description in system prompt, body on activation)
    cat_agents = CategoryReport(name="Agents (.github/agents/)")
    agents_dir = github_dir / "agents"
    if agents_dir.exists():
        cat_agents.files = scan_directory(agents_dir, "on-demand", repo_root)
    categories.append(cat_agents)

    # 3. Skills (on-demand — loaded when triggered)
    cat_skills = CategoryReport(name="Skills (.github/skills/)")
    skills_dir = github_dir / "skills"
    if skills_dir.exists():
        cat_skills.files = scan_directory(skills_dir, "on-demand", repo_root)
    categories.append(cat_skills)

    # 4. Prompt files (explicit invoke only)
    cat_prompts = CategoryReport(name="Prompts (.github/prompts/)")
    prompts_dir = github_dir / "prompts"
    if prompts_dir.exists():
        cat_prompts.files = scan_directory(prompts_dir, "explicit-invoke", repo_root)
    categories.append(cat_prompts)

    # Also check for .instructions.md files at repo root or .github
    cat_other = CategoryReport(name="Other Config Files")
    for pattern in [".instructions.md", ".copilot-instructions.md"]:
        f = repo_root / pattern
        if f.exists():
            cat_other.files.append(scan_file(f, "always-on", repo_root))
    # Check for vscode settings with copilot config
    vscode_settings = repo_root / ".vscode" / "settings.json"
    if vscode_settings.exists():
        text = vscode_settings.read_text(encoding="utf-8", errors="replace")
        if "copilot" in text.lower() or "github.copilot" in text.lower():
            cat_other.files.append(scan_file(vscode_settings, "always-on", repo_root))

    if cat_other.files:
        categories.append(cat_other)

    print_report(categories, repo_root)


if __name__ == "__main__":
    main()
