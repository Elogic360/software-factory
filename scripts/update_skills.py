#!/usr/bin/env python3
"""
update_skills.py — Self-updating skills / memory / graph orchestrator.

The Software Factory skill library must grow and self-modify as the codebase
evolves. This script wires together the three existing primitives:

  1. context-engine/change_detector.py  — detect & classify code changes,
     documenting them into software-factory/memory/.
  2. context-engine/skill_selector.py    — map changed areas to the skills that
     own them, surfacing which skills likely need updating.
  3. graphify                            — refresh the persistent knowledge graph
     so cross-domain dependencies stay queryable.

It then rewrites a clearly-delimited AUTO-SYNC block in SKILLS_REGISTRY.md so the
registry always reflects the latest detected domains and skill-review suggestions.

Designed to be safe in a git hook: never raises, never blocks (best-effort),
deterministic, stdlib-only.

Usage:
    python3 update_skills.py                 # since last sync (or HEAD~1)
    python3 update_skills.py --since HEAD~5
    python3 update_skills.py --seed          # initial seed run (no commit range)
"""
from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

SF_ROOT = Path(__file__).resolve().parent.parent          # software-factory/
ROOT = SF_ROOT.parent                                     # repo root
CE = SF_ROOT / "context-engine"
REGISTRY = SF_ROOT / "SKILLS_REGISTRY.md"
STATE = SF_ROOT / ".skills_sync_state"
GRAPHIFY_DIR = SF_ROOT / "graphify"
PATTERNS_DIR = SF_ROOT / "memory" / "patterns"
GRAPHIFY_OUT = ROOT / "graphify-out"

AUTO_START = "<!-- AUTO-SYNC:START -->"
AUTO_END = "<!-- AUTO-SYNC:END -->"

# Map a top-level path prefix to the skills that own it (for review suggestions).
SCOPE_TO_SKILLS = {
    "app/src/modules/expert": ["frontend-trading-ui", "tradingview-integration", "journal-analytics"],
    "app/src/modules": ["frontend-react", "ui-ux-premium"],
    "app/src/shared": ["frontend-react", "ui-ux-premium"],
    "app/src/core": ["frontend-react", "architect-principal"],
    "integral-expert-backend": ["backend-fastapi", "mt5-integration", "copytrading-engine"],
    "integral-market-backend": ["backend-fastapi", "security-audit"],
    "integral-market-intelligence": ["prompt-engineering", "ai-optimization", "quant-research"],
    "schema_files": ["database-postgresql", "change-detective"],
    "docker-compose": ["devops-engineer", "microservices"],
    "monitoring": ["observability"],
    "software-factory": ["skill-builder"],
}


def run(cmd: list[str], cwd: Path = ROOT, timeout: int = 120) -> tuple[int, str]:
    """Run a command, returning (exit_code, combined_output). Never raises."""
    try:
        p = subprocess.run(
            cmd, cwd=str(cwd), capture_output=True, text=True, timeout=timeout
        )
        return p.returncode, (p.stdout or "") + (p.stderr or "")
    except Exception as exc:  # noqa: BLE001 - best-effort orchestration
        return 1, f"(command failed: {exc})"


def git(*args: str) -> str:
    code, out = run(["git", *args])
    return out.strip() if code == 0 else ""


def resolve_since(explicit: str | None, seed: bool) -> str:
    if explicit:
        return explicit
    if seed:
        # First commit (empty-tree) so the seed run sees the whole tree.
        return git("rev-list", "--max-parents=0", "HEAD").splitlines()[0] if git(
            "rev-list", "--max-parents=0", "HEAD"
        ) else "HEAD~1"
    if STATE.exists():
        ref = STATE.read_text(encoding="utf-8").strip()
        if ref:
            return ref
    return "HEAD~1"


def changed_files(since: str) -> list[str]:
    out = git("diff", "--name-only", f"{since}..HEAD")
    files = [f for f in out.splitlines() if f.strip()]
    if not files:  # fall back to staged (pre-commit context)
        out = git("diff", "--cached", "--name-only")
        files = [f for f in out.splitlines() if f.strip()]
    return files


def skills_for(files: list[str]) -> dict[str, list[str]]:
    """Map changed files to the owning skills via SCOPE_TO_SKILLS."""
    hits: dict[str, list[str]] = {}
    for f in files:
        for prefix, skills in SCOPE_TO_SKILLS.items():
            if f.startswith(prefix):
                for s in skills:
                    hits.setdefault(s, [])
                    if f not in hits[s]:
                        hits[s].append(f)
                break
    return hits


def detect_changes(since: str) -> list[dict]:
    detector = CE / "change_detector.py"
    if not detector.exists():
        return []
    # --document writes to memory/; --json gives us structured data.
    run([sys.executable, str(detector), "--since", since, "--document"])
    code, out = run([sys.executable, str(detector), "--since", since, "--json"])
    try:
        return json.loads(out) if out.strip().startswith("[") else []
    except json.JSONDecodeError:
        return []


def select_skill(query: str) -> str:
    selector = CE / "skill_selector.py"
    if not selector.exists():
        return ""
    code, out = run([sys.executable, str(selector), "--query", query, "--top", "3"])
    return out.strip() if code == 0 else ""


def refresh_graph() -> str:
    """Best-effort incremental graph refresh. Never blocks the hook."""
    if not shutil.which("graphify"):
        return "graphify CLI not found — skipped graph refresh"
    code, _ = run(["graphify", str(ROOT), "--update", "--no-viz"], timeout=90)
    graph = GRAPHIFY_OUT / "graph.json"
    if graph.exists():
        GRAPHIFY_DIR.mkdir(parents=True, exist_ok=True)
        try:
            shutil.copy2(graph, GRAPHIFY_DIR / "graph.json")
        except Exception:  # noqa: BLE001
            pass
        return f"graph refreshed → {GRAPHIFY_DIR / 'graph.json'}"
    return "graph build attempted (no graph.json yet — run /graphify once)"


def seed_graphify_manifest(since: str, files: list[str], skill_hits: dict) -> None:
    GRAPHIFY_DIR.mkdir(parents=True, exist_ok=True)
    manifest = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "since": since,
        "head": git("rev-parse", "HEAD"),
        "changed_file_count": len(files),
        "skills_touched": sorted(skill_hits.keys()),
        "graph_json": str((GRAPHIFY_OUT / "graph.json")),
        "note": "Run `/graphify .` (or `graphify . --update`) to (re)build graph.json.",
    }
    (GRAPHIFY_DIR / "graph_manifest.json").write_text(
        json.dumps(manifest, indent=2), encoding="utf-8"
    )


def write_pattern_note(since: str, changes: list[dict], skill_hits: dict) -> None:
    PATTERNS_DIR.mkdir(parents=True, exist_ok=True)
    month = datetime.now(timezone.utc).strftime("%Y-%m")
    date = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    lines = [f"\n## {date} — skill sync (since {since})\n"]
    if skill_hits:
        lines.append("Skills to review (touched domains):\n")
        for skill, fs in sorted(skill_hits.items()):
            lines.append(f"- **{skill}** — {len(fs)} file(s)")
    else:
        lines.append("No skill-owned domains changed in this range.")
    cats: dict[str, int] = {}
    for c in changes:
        cats[c.get("category", "?")] = cats.get(c.get("category", "?"), 0) + 1
    if cats:
        lines.append("\nChange categories: " + ", ".join(f"{k}={v}" for k, v in sorted(cats.items())))
    (PATTERNS_DIR / f"{month}.md").open("a", encoding="utf-8").write("\n".join(lines) + "\n")


def render_auto_block(since: str, files: list[str], changes: list[dict], skill_hits: dict, graph_status: str) -> str:
    now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    head = git("rev-parse", "--short", "HEAD") or "?"
    breaking = [c for c in changes if c.get("impact") == "breaking"]
    rows = []
    for skill, fs in sorted(skill_hits.items(), key=lambda kv: (-len(kv[1]), kv[0])):
        rows.append(f"| `{skill}` | {len(fs)} | {', '.join(fs[:3])}{' …' if len(fs) > 3 else ''} |")
    table = "\n".join(rows) if rows else "| _(no skill-owned domains changed)_ | 0 | — |"
    return f"""{AUTO_START}
## Auto-Sync Status

> This block is regenerated by `scripts/update_skills.py` (wired to the git
> post-commit hook). It tracks how the skill library is auto-scaling with the
> codebase. Do not edit by hand — changes here are overwritten.

- **Last sync:** {now}
- **Commit range:** `{since}..{head}`
- **Files changed:** {len(files)}
- **Breaking changes:** {len(breaking)}
- **Graph:** {graph_status}

### Skills to review (auto-mapped from changed domains)

| Skill | Files touched | Examples |
|-------|---------------|----------|
{table}

*New domains with no owning skill are candidates for `skill-builder` to codify
into a new SKILL.md — keeping the library growing as the project grows.*
{AUTO_END}"""


def update_registry(block: str) -> None:
    if not REGISTRY.exists():
        return
    text = REGISTRY.read_text(encoding="utf-8")
    if AUTO_START in text and AUTO_END in text:
        pre = text.split(AUTO_START)[0]
        post = text.split(AUTO_END)[1]
        text = pre + block + post
    else:
        text = text.rstrip() + "\n\n" + block + "\n"
    REGISTRY.write_text(text, encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="Self-updating skills/memory/graph sync.")
    parser.add_argument("--since", help="Git ref to diff from (default: last sync or HEAD~1)")
    parser.add_argument("--seed", action="store_true", help="Initial seed run over whole tree")
    parser.add_argument("--no-graph", action="store_true", help="Skip graphify graph refresh")
    args = parser.parse_args()

    since = resolve_since(args.since, args.seed)
    files = changed_files(since)
    skill_hits = skills_for(files)
    changes = detect_changes(since)

    graph_status = "skipped" if args.no_graph else refresh_graph()
    seed_graphify_manifest(since, files, skill_hits)
    write_pattern_note(since, changes, skill_hits)
    update_registry(render_auto_block(since, files, changes, skill_hits, graph_status))

    head = git("rev-parse", "HEAD")
    if head:
        STATE.write_text(head, encoding="utf-8")

    print(f"[update_skills] synced {len(files)} files, {len(skill_hits)} skills, "
          f"{len(changes)} classified changes (since {since}).")


if __name__ == "__main__":
    main()
