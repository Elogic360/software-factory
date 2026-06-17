#!/usr/bin/env bash
# ═══════════════════════════════════════════════════════════════════════════════
#  install_hooks.sh — install Software Factory git hooks.
#
#  Installs the tracked hooks from software-factory/hooks/ into .git/hooks/
#  WITHOUT clobbering existing hooks (e.g. the schema-drift pre-commit). If a hook
#  already exists, the SF hook is appended via a sourced include so both run.
# ═══════════════════════════════════════════════════════════════════════════════
set -euo pipefail

ROOT="$(git rev-parse --show-toplevel)"
SRC="$ROOT/software-factory/hooks"
DST="$ROOT/.git/hooks"
MARKER="# >>> software-factory hook >>>"

mkdir -p "$DST"

install_hook() {
  local name="$1"
  local src="$SRC/$name"
  local dst="$DST/$name"
  [ -f "$src" ] || return 0

  if [ ! -f "$dst" ]; then
    cp "$src" "$dst"
    chmod +x "$dst"
    echo "  installed $name"
    return 0
  fi

  # Existing hook present — append an include guard if not already wired.
  if grep -q "$MARKER" "$dst" 2>/dev/null; then
    echo "  $name already wired — skipped"
    return 0
  fi
  {
    echo ""
    echo "$MARKER"
    echo "bash \"$src\" \"\$@\" || true"
    echo "# <<< software-factory hook <<<"
  } >> "$dst"
  chmod +x "$dst"
  echo "  appended SF include to existing $name"
}

echo "Installing Software Factory hooks…"
install_hook post-commit
echo "Done. Skills/memory/graph will auto-sync after each commit."
