#!/usr/bin/env python3
"""
change_detector.py — Autonomous Change Detection & Documentation

Detects code changes since a reference point, classifies them by impact,
and optionally auto-documents them into software-factory/memory/.

Usage:
    python3 change_detector.py --since HEAD~1
    python3 change_detector.py --since $(git merge-base HEAD main) --document
    python3 change_detector.py --since HEAD~5 --scope integral-expert-backend/
    python3 change_detector.py --watch          # re-run on file save
"""

from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
import time
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

ROOT = Path(__file__).parent.parent.parent  # project root
SF_ROOT = Path(__file__).parent.parent      # software-factory root
MEMORY_DIR = SF_ROOT / "memory" / "decisions"
API_SNAPSHOT_DIR = SF_ROOT / "memory" / "api-snapshots"

# ── Change classification ──────────────────────────────────────────────────────

@dataclass
class DetectedChange:
    filepath: str
    change_type: str        # added | modified | deleted | renamed
    category: str           # api | schema | type | security | config | test | logic | cosmetic
    impact: str             # breaking | non-breaking | cosmetic
    description: str
    action_required: str = ""


# Patterns that indicate different change categories
CATEGORY_PATTERNS = {
    "schema": [
        r"alembic/versions/.*\.py$",
        r"app/models/.*\.py$",
        r"\.sql$",
    ],
    "api": [
        r"app/api/v1/endpoints/.*\.py$",
        r"app/api/.*router.*\.py$",
    ],
    "type": [
        r"app/schemas/.*\.py$",
        r"src/.*types.*\.ts$",
        r"src/shared/api/types/.*\.ts$",
    ],
    "security": [
        r"app/core/security.*\.py$",
        r"app/core/auth.*\.py$",
        r"\.env",
        r"cors.*",
    ],
    "config": [
        r"app/core/config.*\.py$",
        r"docker-compose.*\.yml$",
        r"Dockerfile",
        r"vite\.config\.ts$",
        r"requirements\.txt$",
        r"package\.json$",
    ],
    "test": [
        r"tests/.*\.py$",
        r"e2e/.*\.spec\.ts$",
        r"\.spec\.(ts|tsx|py)$",
    ],
}

BREAKING_PATTERNS = [
    r"def .+\(",           # function signature (may have removed params)
    r"class .+:",          # class definition change
    r"Column\(",           # SQLAlchemy column change
    r"ForeignKey\(",       # FK change
    r"@router\.(get|post|put|delete|patch)",  # route change
    r"interface .+\{",    # TypeScript interface change
    r"op\.drop_column",   # migration dropping column
    r"op\.drop_table",    # migration dropping table
]


def git_diff_files(since: str, scope: Optional[str] = None) -> list[str]:
    """Get list of changed files since reference point."""
    cmd = ["git", "diff", "--name-status", since, "HEAD"]
    if scope:
        cmd.append(scope)
    result = subprocess.run(cmd, capture_output=True, text=True, cwd=ROOT)
    if result.returncode != 0:
        print(f"Git error: {result.stderr}", file=sys.stderr)
        return []
    return result.stdout.strip().splitlines()


def git_diff_content(filepath: str, since: str) -> str:
    """Get actual diff content for a file."""
    cmd = ["git", "diff", since, "HEAD", "--", filepath]
    result = subprocess.run(cmd, capture_output=True, text=True, cwd=ROOT)
    return result.stdout


def classify_file(filepath: str) -> str:
    """Determine change category from file path."""
    for category, patterns in CATEGORY_PATTERNS.items():
        for pattern in patterns:
            if re.search(pattern, filepath):
                return category
    return "logic"


def assess_impact(filepath: str, diff_content: str) -> str:
    """Assess whether change is breaking, non-breaking, or cosmetic."""
    if classify_file(filepath) in ("test", ):
        return "cosmetic"
    for pattern in BREAKING_PATTERNS:
        if re.search(pattern, diff_content):
            # Check if it's a deletion (breaking) or addition (non-breaking)
            deleted_lines = [l for l in diff_content.split("\n") if l.startswith("-") and not l.startswith("---")]
            if any(re.search(pattern, line) for line in deleted_lines):
                return "breaking"
            return "non-breaking"
    if not diff_content.strip():
        return "cosmetic"
    return "non-breaking"


def describe_change(filepath: str, change_type: str, diff_content: str) -> tuple[str, str]:
    """Generate human-readable description and recommended action."""
    category = classify_file(filepath)
    fname = Path(filepath).name

    if category == "schema":
        added_cols = re.findall(r"\+.*op\.add_column.*'(\w+)'", diff_content)
        dropped_cols = re.findall(r"\+.*op\.drop_column.*'(\w+)'", diff_content)
        desc = f"Schema change in {fname}"
        if added_cols:
            desc += f" — added columns: {', '.join(added_cols)}"
        if dropped_cols:
            desc += f" — DROPPED columns: {', '.join(dropped_cols)}"
        action = "Verify migration ran: alembic upgrade head && alembic check"
        if dropped_cols:
            action = "⚠️  BREAKING: Column removed — ensure no code reads it before removing"
        return desc, action

    if category == "api":
        added_routes = re.findall(r'\+.*@router\.(get|post|put|delete|patch)\("([^"]+)"', diff_content)
        removed_routes = re.findall(r'-.*@router\.(get|post|put|delete|patch)\("([^"]+)"', diff_content)
        desc = f"API change in {fname}"
        if added_routes:
            desc += f" — added routes: {[r[1] for r in added_routes]}"
        if removed_routes:
            desc += f" — REMOVED routes: {[r[1] for r in removed_routes]}"
        action = "Update TypeScript types + OpenAPI snapshot"
        if removed_routes:
            action = "⚠️  BREAKING: Route removed — update frontend before deploying"
        return desc, action

    if category == "type":
        desc = f"Schema/type change in {fname} — check TypeScript sync"
        action = "Run pnpm type-check to verify frontend still compiles"
        return desc, action

    if category == "security":
        desc = f"⚠️  SECURITY: Change in {fname}"
        action = "Load skills/security-audit/SKILL.md and review immediately"
        return desc, action

    if category == "config":
        desc = f"Config change in {fname}"
        action = "Verify all environments updated (.env.example if needed)"
        return desc, action

    return f"{change_type} in {fname}", ""


def analyze_changes(since: str, scope: Optional[str] = None) -> list[DetectedChange]:
    """Analyze all changes and return structured list."""
    raw_files = git_diff_files(since, scope)
    changes = []

    for line in raw_files:
        if not line.strip():
            continue
        parts = line.split("\t")
        status = parts[0][0]  # M, A, D, R
        filepath = parts[-1]

        change_type = {
            "M": "modified", "A": "added", "D": "deleted", "R": "renamed"
        }.get(status, "modified")

        diff = git_diff_content(filepath, since)
        category = classify_file(filepath)
        impact = assess_impact(filepath, diff)
        desc, action = describe_change(filepath, change_type, diff)

        changes.append(DetectedChange(
            filepath=filepath,
            change_type=change_type,
            category=category,
            impact=impact,
            description=desc,
            action_required=action,
        ))

    return sorted(changes, key=lambda c: (
        {"breaking": 0, "non-breaking": 1, "cosmetic": 2}[c.impact],
        {"security": 0, "schema": 1, "api": 2, "type": 3}.get(c.category, 4),
    ))


def print_report(changes: list[DetectedChange], since: str) -> None:
    """Print formatted change report."""
    breaking = [c for c in changes if c.impact == "breaking"]
    non_breaking = [c for c in changes if c.impact == "non-breaking"]
    cosmetic = [c for c in changes if c.impact == "cosmetic"]

    print(f"\n{'='*70}")
    print(f"  🔍 Change Detective Report — since: {since}")
    print(f"  {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')}")
    print(f"{'='*70}")
    print(f"  Total changes: {len(changes)}  |  "
          f"🔴 Breaking: {len(breaking)}  |  "
          f"🟡 Non-breaking: {len(non_breaking)}  |  "
          f"⚪ Cosmetic: {len(cosmetic)}")
    print()

    if breaking:
        print("🔴 BREAKING CHANGES (action required before merging):")
        for c in breaking:
            print(f"  [{c.category.upper()}] {c.filepath}")
            print(f"    → {c.description}")
            if c.action_required:
                print(f"    ⚡ {c.action_required}")
        print()

    if non_breaking:
        print("🟡 NON-BREAKING CHANGES:")
        for c in non_breaking:
            print(f"  [{c.category.upper()}] {c.filepath}")
            print(f"    → {c.description}")
            if c.action_required:
                print(f"    ℹ️  {c.action_required}")
        print()

    if cosmetic:
        print(f"⚪ Cosmetic changes: {len(cosmetic)} files (tests, comments, formatting)")
    print()


def write_memory_entry(changes: list[DetectedChange], since: str, output_file: Optional[str]) -> str:
    """Write structured memory entry for these changes."""
    MEMORY_DIR.mkdir(parents=True, exist_ok=True)

    date_str = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    month_str = datetime.now(timezone.utc).strftime("%Y-%m")

    branch_result = subprocess.run(
        ["git", "rev-parse", "--abbrev-ref", "HEAD"],
        capture_output=True, text=True, cwd=ROOT
    )
    branch = branch_result.stdout.strip()

    entry = f"""
## {date_str} — Auto-detected changes [branch: {branch}]
*Generated by change_detector.py — since: {since}*

"""
    breaking = [c for c in changes if c.impact == "breaking"]
    if breaking:
        entry += "### ⚠️  Breaking Changes\n"
        for c in breaking:
            entry += f"- **[{c.category.upper()}]** `{c.filepath}` — {c.description}\n"
            if c.action_required:
                entry += f"  - Action: {c.action_required}\n"
        entry += "\n"

    by_category: dict[str, list[DetectedChange]] = {}
    for c in [ch for ch in changes if ch.impact != "breaking"]:
        by_category.setdefault(c.category, []).append(c)

    for category, items in sorted(by_category.items()):
        entry += f"### {category.title()} Changes\n"
        for c in items:
            entry += f"- `{c.filepath}` — {c.description} ({c.change_type})\n"
        entry += "\n"

    target = output_file or str(MEMORY_DIR / f"{month_str}.md")
    with open(target, "a") as f:
        f.write(entry)

    print(f"📝 Memory entry written to: {target}")
    return target


def watch_mode(since_ref: str, scope: Optional[str]) -> None:
    """Re-run detection every 3 seconds watching for file changes."""
    print(f"👁️  Watch mode active — monitoring changes since {since_ref}")
    print("     Press Ctrl+C to stop.\n")
    last_count = 0
    try:
        while True:
            changes = analyze_changes(since_ref, scope)
            if len(changes) != last_count:
                print_report(changes, since_ref)
                last_count = len(changes)
            time.sleep(3)
    except KeyboardInterrupt:
        print("\nWatch mode stopped.")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Detect, classify, and document code changes.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("--since", "-s", default="HEAD~1",
                        help="Git reference to diff from (default: HEAD~1)")
    parser.add_argument("--scope", help="Limit to path prefix (e.g., integral-expert-backend/)")
    parser.add_argument("--document", "-d", action="store_true",
                        help="Write changes to software-factory/memory/")
    parser.add_argument("--output", "-o", help="Custom output file for memory entry")
    parser.add_argument("--watch", "-w", action="store_true",
                        help="Watch for new changes every 3 seconds")
    parser.add_argument("--json", action="store_true",
                        help="Output raw JSON (for CI integration)")

    args = parser.parse_args()

    if args.watch:
        watch_mode(args.since, args.scope)
        return

    changes = analyze_changes(args.since, args.scope)

    if args.json:
        print(json.dumps([vars(c) for c in changes], indent=2))
        return

    print_report(changes, args.since)

    if args.document:
        write_memory_entry(changes, args.since, args.output)

    # Exit non-zero if breaking changes found (useful in CI)
    breaking = [c for c in changes if c.impact == "breaking"]
    if breaking:
        print(f"⛔ {len(breaking)} breaking change(s) detected. Review before merging.")
        sys.exit(1)


if __name__ == "__main__":
    main()
