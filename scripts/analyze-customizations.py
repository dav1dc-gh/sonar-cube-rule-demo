#!/usr/bin/env python3
"""
analyze-customizations.py
=========================

Static analyzer for VS Code Copilot customization files (instructions, skills,
agents, prompts, AGENTS.md, memory files).

Goal: estimate the *context-window cost* of your customization surface and
flag clutter/redundancy WITHOUT making any GenAI calls.

What it measures
----------------
1. File inventory by surface (instructions / skills / agents / prompts / memory).
2. Approximate token cost (bytes / 4 heuristic, configurable).
3. Always-loaded vs on-demand classification.
4. Overlap / redundancy between surfaces (skill vs agent name similarity,
   duplicated keyword sets, near-duplicate descriptions).
5. Conflicting or duplicated `applyTo` globs.
6. Empty or near-empty stub files.
7. Bloated files that exceed recommended thresholds.

Exit codes
----------
0 = clean
1 = warnings present
2 = errors / over-budget

Usage
-----
    python3 scripts/analyze-customizations.py
    python3 scripts/analyze-customizations.py --root . --json
    python3 scripts/analyze-customizations.py --budget 6000

No third-party dependencies. Python 3.8+.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
from dataclasses import dataclass, field, asdict
from pathlib import Path
from typing import Dict, List, Optional, Tuple

# --- Heuristics / thresholds (tweak as needed) -------------------------------

CHARS_PER_TOKEN = 4  # rough OpenAI/Anthropic average for English+code

# Token budget (always-loaded surface) above which performance typically degrades
DEFAULT_BUDGET_TOKENS = 6000
HARD_BUDGET_TOKENS = 15000  # instructions start being ignored above this

# File-level "too big" thresholds
SKILL_MAX_LINES = 400
AGENT_MAX_LINES = 250
INSTRUCTION_MAX_LINES = 300

# Stub / empty
STUB_MAX_LINES = 5

# Description similarity (Jaccard on token sets)
SIM_WARN = 0.55
SIM_DUPE = 0.80


# --- Data model --------------------------------------------------------------

@dataclass
class FileEntry:
    path: str
    surface: str               # instructions | skill | agent | prompt | memory | agents-md | unknown
    lines: int
    bytes: int
    tokens: int
    always_loaded: bool
    frontmatter: Dict[str, object] = field(default_factory=dict)
    name: str = ""
    description: str = ""
    apply_to: Optional[str] = None
    notes: List[str] = field(default_factory=list)


@dataclass
class Report:
    root: str
    files: List[FileEntry]
    always_loaded_tokens: int
    on_demand_tokens: int
    total_tokens: int
    budget_tokens: int
    warnings: List[str]
    errors: List[str]
    suggestions: List[str]


# --- Discovery ---------------------------------------------------------------

def classify(path: Path) -> str:
    p = str(path).replace(os.sep, "/")
    name = path.name.lower()

    if name == "copilot-instructions.md":
        return "instructions"
    if name == "agents.md":
        return "agents-md"
    if "/skills/" in p and name == "skill.md":
        return "skill"
    if "/agents/" in p and name.endswith(".md"):
        return "agent"
    if "/prompts/" in p and name.endswith(".prompt.md"):
        return "prompt"
    if name.endswith(".instructions.md"):
        return "instructions"
    if "/memories/" in p and name.endswith(".md"):
        return "memory"
    return "unknown"


def is_always_loaded(surface: str, frontmatter: Dict[str, object]) -> bool:
    """Approximate: which surfaces sit in the system prompt every turn."""
    if surface in ("instructions", "agents-md"):
        return True
    if surface == "memory":
        # User memory first 200 lines auto-loaded; session/repo only listed.
        return True
    if surface in ("skill", "agent"):
        # Only metadata (name + description) is always loaded; body is on-demand.
        # We model that separately below; the file itself is on-demand.
        return False
    return False


FRONTMATTER_RE = re.compile(r"^---\s*\n(.*?)\n---\s*\n", re.DOTALL)


def parse_frontmatter(text: str) -> Tuple[Dict[str, object], str]:
    m = FRONTMATTER_RE.match(text)
    if not m:
        return {}, text
    raw = m.group(1)
    body = text[m.end():]
    fm: Dict[str, object] = {}
    # Tiny YAML subset: key: value (string), no nesting.
    for line in raw.splitlines():
        if ":" in line and not line.lstrip().startswith("#"):
            k, _, v = line.partition(":")
            fm[k.strip()] = v.strip().strip("'\"")
    return fm, body


def default_scan_roots(workspace_root: Path) -> List[Path]:
    """All locations VS Code Copilot reads customization files from."""
    home = Path.home()
    roots: List[Path] = [
        workspace_root / ".github",
        workspace_root / "AGENTS.md",
    ]
    # macOS user profile
    user_base = home / "Library" / "Application Support" / "Code" / "User"
    for sub in ("prompts", "agents", "instructions", "skills"):
        roots.append(user_base / sub)
    # Linux/Windows fallbacks
    roots.append(home / ".config" / "Code" / "User")
    roots.append(home / "AppData" / "Roaming" / "Code" / "User")
    # Installed-extension contributed skills/agents/prompts
    roots.append(home / ".vscode" / "extensions")
    return roots


def collect_files(roots: List[Path]) -> List[Path]:
    targets: List[Path] = []
    for c in roots:
        if not c.exists():
            continue
        if c.is_file():
            targets.append(c)
            continue
        # Bound the depth on extensions dir to avoid scanning whole node_modules trees
        if c.name == "extensions":
            for p in c.glob("*/skills/**/*.md"):
                targets.append(p)
            for p in c.glob("*/.github/skills/**/*.md"):
                targets.append(p)
            for p in c.glob("*/agents/**/*.md"):
                targets.append(p)
            for p in c.glob("*/prompts/**/*.md"):
                targets.append(p)
            for p in c.glob("*/copilot-cli-plugin/skills/**/*.md"):
                targets.append(p)
            for p in c.glob("*/resources/skills/**/*.md"):
                targets.append(p)
            continue
        for p in c.rglob("*.md"):
            targets.append(p)
    return sorted(set(targets))


# --- Analysis ----------------------------------------------------------------

WORD_RE = re.compile(r"[A-Za-z][A-Za-z0-9_-]+")


def tokenize(text: str) -> set:
    return {w.lower() for w in WORD_RE.findall(text) if len(w) > 2}


def jaccard(a: set, b: set) -> float:
    if not a or not b:
        return 0.0
    return len(a & b) / len(a | b)


def analyze(workspace_root: Path, budget: int, extra_roots: List[Path]) -> Report:
    entries: List[FileEntry] = []
    warnings: List[str] = []
    errors: List[str] = []
    suggestions: List[str] = []

    roots = default_scan_roots(workspace_root) + extra_roots
    files = collect_files(roots)

    for path in files:
        try:
            text = path.read_text(encoding="utf-8")
        except Exception as e:
            warnings.append(f"Could not read {path}: {e}")
            continue

        surface = classify(path)
        fm, body = parse_frontmatter(text)
        nbytes = len(text.encode("utf-8"))
        nlines = text.count("\n") + (0 if text.endswith("\n") else 1)
        tokens = max(1, nbytes // CHARS_PER_TOKEN)

        # Display path: relative to workspace if inside, else absolute
        try:
            disp = str(path.relative_to(workspace_root))
            scope = "workspace"
        except ValueError:
            disp = str(path)
            if "/.vscode/extensions/" in disp:
                scope = "extension"
            elif "/Code/User/" in disp:
                scope = "user"
            else:
                scope = "external"

        entry = FileEntry(
            path=disp,
            surface=surface,
            lines=nlines,
            bytes=nbytes,
            tokens=tokens,
            always_loaded=is_always_loaded(surface, fm),
            frontmatter=fm,
            name=str(fm.get("name", path.stem)),
            description=str(fm.get("description", "")),
            apply_to=str(fm.get("applyTo")) if fm.get("applyTo") else None,
        )
        entry.notes.append(f"scope={scope}")

        # Per-file checks
        if nlines <= STUB_MAX_LINES:
            entry.notes.append(f"stub ({nlines} lines) — consider deleting")
            warnings.append(f"Stub file: {entry.path} ({nlines} lines)")

        if surface == "skill" and nlines > SKILL_MAX_LINES:
            entry.notes.append(f"large skill ({nlines} lines > {SKILL_MAX_LINES})")
            warnings.append(f"Large SKILL.md: {entry.path} — consider splitting")

        if surface == "agent" and nlines > AGENT_MAX_LINES:
            entry.notes.append(f"large agent ({nlines} lines > {AGENT_MAX_LINES})")
            warnings.append(f"Large agent: {entry.path}")

        if surface == "instructions" and nlines > INSTRUCTION_MAX_LINES:
            entry.notes.append(f"large instructions file ({nlines} lines > {INSTRUCTION_MAX_LINES})")
            warnings.append(f"Large instructions file: {entry.path} — trim or move detail to skills")

        if surface in ("skill", "agent") and not entry.description:
            entry.notes.append("missing description in frontmatter — invocation routing degraded")
            warnings.append(f"Missing description: {entry.path}")

        entries.append(entry)

    # Always-loaded budget
    # Skill+agent metadata (name+description) is roughly ~50 tokens each.
    metadata_tokens = sum(
        max(1, (len(e.name) + len(e.description)) // CHARS_PER_TOKEN) + 10
        for e in entries if e.surface in ("skill", "agent")
    )
    always_tokens = sum(e.tokens for e in entries if e.always_loaded) + metadata_tokens
    on_demand_tokens = sum(e.tokens for e in entries if not e.always_loaded)
    total_tokens = always_tokens + sum(e.tokens for e in entries if not e.always_loaded)

    # Budget check
    if always_tokens > HARD_BUDGET_TOKENS:
        errors.append(
            f"Always-loaded context = ~{always_tokens} tokens "
            f"(> hard budget {HARD_BUDGET_TOKENS}). Instructions will be ignored."
        )
    elif always_tokens > budget:
        warnings.append(
            f"Always-loaded context = ~{always_tokens} tokens "
            f"(> recommended budget {budget}). Trim copilot-instructions.md."
        )

    # Conflicting applyTo
    apply_buckets: Dict[str, List[str]] = {}
    for e in entries:
        if e.apply_to:
            apply_buckets.setdefault(e.apply_to, []).append(e.path)
    for glob, paths in apply_buckets.items():
        if len(paths) > 1:
            warnings.append(f"Multiple instruction files share applyTo='{glob}': {paths}")

    # Description similarity (skills vs agents vs each other)
    sims: List[Tuple[str, str, float]] = []
    skill_agent = [e for e in entries if e.surface in ("skill", "agent")]
    for i, a in enumerate(skill_agent):
        ta = tokenize(a.description or a.name)
        for b in skill_agent[i + 1:]:
            tb = tokenize(b.description or b.name)
            s = jaccard(ta, tb)
            if s >= SIM_WARN:
                sims.append((a.path, b.path, round(s, 2)))
    sims.sort(key=lambda x: -x[2])
    for a, b, s in sims:
        msg = f"High similarity ({s}): {a}  <->  {b}"
        if s >= SIM_DUPE:
            warnings.append("Likely duplicate: " + msg)
        else:
            suggestions.append("Possible overlap: " + msg)

    # Skill <-> agent name pairing (mirror surfaces)
    skill_names = {Path(e.path).parent.name for e in entries if e.surface == "skill"}
    agent_names = {Path(e.path).stem for e in entries if e.surface == "agent"}
    for s in sorted(skill_names):
        # Crude pairing: 'sonarcube-validator' <-> 'validate-rules' won't catch,
        # but exact / suffix overlap will.
        for a in sorted(agent_names):
            if s == a or s.endswith(a) or a.endswith(s):
                suggestions.append(
                    f"Mirror surfaces: skill '{s}' and agent '{a}' — pick one to reduce drift."
                )

    # Generic suggestions
    stubs = [e for e in entries if e.lines <= STUB_MAX_LINES]
    if stubs:
        suggestions.append(
            f"Delete {len(stubs)} stub file(s) to reduce picker clutter: "
            + ", ".join(e.path for e in stubs)
        )

    big_instructions = [
        e for e in entries
        if e.surface == "instructions" and e.lines > INSTRUCTION_MAX_LINES
    ]
    for e in big_instructions:
        suggestions.append(
            f"{e.path}: move static reference material (tables, listings) out of "
            "always-loaded instructions; keep only behavior rules."
        )

    return Report(
        root=str(workspace_root),
        files=entries,
        always_loaded_tokens=always_tokens,
        on_demand_tokens=on_demand_tokens,
        total_tokens=total_tokens,
        budget_tokens=budget,
        warnings=warnings,
        errors=errors,
        suggestions=suggestions,
    )


# --- Output ------------------------------------------------------------------

def render_text(r: Report) -> str:
    out: List[str] = []
    out.append("Copilot Customization Footprint")
    out.append("=" * 60)
    out.append(f"Root: {r.root}")
    out.append(f"Files scanned: {len(r.files)}")
    out.append("")

    by_surface: Dict[str, List[FileEntry]] = {}
    for e in r.files:
        by_surface.setdefault(e.surface, []).append(e)

    # Group by scope (parsed from notes)
    def scope_of(e: FileEntry) -> str:
        for n in e.notes:
            if n.startswith("scope="):
                return n.split("=", 1)[1]
        return "workspace"

    out.append(f"{'Scope':<12}{'Files':>6}{'Tokens':>10}")
    out.append("-" * 32)
    by_scope: Dict[str, List[FileEntry]] = {}
    for e in r.files:
        by_scope.setdefault(scope_of(e), []).append(e)
    for scope, items in sorted(by_scope.items()):
        out.append(f"{scope:<12}{len(items):>6}{sum(i.tokens for i in items):>10}")
    out.append("")

    out.append(f"{'Surface':<14}{'Files':>6}{'Lines':>8}{'Tokens':>10}{'Always-loaded':>16}")
    out.append("-" * 60)
    for surface, items in sorted(by_surface.items()):
        out.append(
            f"{surface:<14}{len(items):>6}{sum(i.lines for i in items):>8}"
            f"{sum(i.tokens for i in items):>10}"
            f"{sum(i.tokens for i in items if i.always_loaded):>16}"
        )
    out.append("-" * 60)
    out.append(f"{'TOTAL':<14}{len(r.files):>6}"
               f"{sum(i.lines for i in r.files):>8}"
               f"{r.total_tokens:>10}{r.always_loaded_tokens:>16}")
    out.append("")

    pct = (r.always_loaded_tokens / r.budget_tokens * 100) if r.budget_tokens else 0
    out.append(f"Always-loaded budget: {r.always_loaded_tokens} / {r.budget_tokens} "
               f"tokens ({pct:.0f}% of recommended)")
    if r.always_loaded_tokens > HARD_BUDGET_TOKENS:
        verdict = "CRITICAL — instructions will be dropped/ignored"
    elif r.always_loaded_tokens > r.budget_tokens:
        verdict = "WARN — over recommended budget"
    elif r.always_loaded_tokens > r.budget_tokens * 0.66:
        verdict = "OK — getting close to budget"
    else:
        verdict = "HEALTHY"
    out.append(f"Verdict: {verdict}")
    out.append("")

    if r.errors:
        out.append("ERRORS")
        out.append("-" * 60)
        for m in r.errors:
            out.append(f"  ✗ {m}")
        out.append("")

    if r.warnings:
        out.append("WARNINGS")
        out.append("-" * 60)
        for m in r.warnings:
            out.append(f"  ! {m}")
        out.append("")

    if r.suggestions:
        out.append("SUGGESTIONS")
        out.append("-" * 60)
        for m in r.suggestions:
            out.append(f"  - {m}")
        out.append("")

    # Top 10 biggest files
    biggest = sorted(r.files, key=lambda e: -e.tokens)[:10]
    out.append("Top files by token cost")
    out.append("-" * 60)
    for e in biggest:
        flag = "[always]" if e.always_loaded else "[on-demand]"
        out.append(f"  {e.tokens:>6} tok  {flag:<11} {e.path}")
    out.append("")

    return "\n".join(out)


def main(argv: Optional[List[str]] = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--root", default=".", help="Workspace root (default: cwd)")
    ap.add_argument("--budget", type=int, default=DEFAULT_BUDGET_TOKENS,
                    help=f"Recommended always-loaded token budget (default {DEFAULT_BUDGET_TOKENS})")
    ap.add_argument("--extra-root", action="append", default=[],
                    help="Extra path to scan (repeatable)")
    ap.add_argument("--workspace-only", action="store_true",
                    help="Skip user-profile and extension scopes")
    ap.add_argument("--json", action="store_true", help="Emit JSON instead of text report")
    args = ap.parse_args(argv)

    root = Path(args.root).resolve()
    extra = [Path(p).expanduser().resolve() for p in args.extra_root]
    if args.workspace_only:
        # Trick: pass an analyze() that only sees workspace by overriding default_scan_roots
        global default_scan_roots  # noqa: PLW0603
        original = default_scan_roots
        default_scan_roots = lambda r: [r / ".github", r / "AGENTS.md"]  # noqa: E731
        try:
            report = analyze(root, args.budget, extra)
        finally:
            default_scan_roots = original
    else:
        report = analyze(root, args.budget, extra)

    if args.json:
        print(json.dumps({
            **{k: v for k, v in asdict(report).items() if k != "files"},
            "files": [asdict(e) for e in report.files],
        }, indent=2))
    else:
        print(render_text(report))

    if report.errors:
        return 2
    if report.warnings:
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
