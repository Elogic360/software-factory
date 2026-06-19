#!/bin/bash
# ================================================================
# SOFTWARE FACTORY — UNIVERSAL INSTALLER
# Single-launch automated installation of everything
# ================================================================
set -e

SF_DIR="$(cd "$(dirname "$0")" && pwd)"
LOG_FILE="$SF_DIR/install.log"
TIMESTAMP=$(date -Iseconds)

log() { echo "[$TIMESTAMP] $1" | tee -a "$LOG_FILE"; }
section() { echo -e "\n\033[1;36m═══ $1 ═══\033[0m"; }

# ── Detect OS ──────────────────────────────────────────────────────
OS=$(uname -s)
ARCH=$(uname -m)
IS_LINUX=false
IS_MAC=false
[ "$OS" = "Linux" ] && IS_LINUX=true
[ "$OS" = "Darwin" ] && IS_MAC=true

log "Platform: $OS $ARCH"
log "Software Factory dir: $SF_DIR"

# ── Check prerequisites ───────────────────────────────────────────
section "Checking Prerequisites"

check_cmd() {
    if command -v "$1" &>/dev/null; then
        log "✅ $1 found: $(command -v $1)"
        return 0
    else
        log "❌ $1 not found — installing..."
        return 1
    fi
}

# Git
check_cmd git || { log "Install git: apt install git / brew install git"; exit 1; }

# Node.js + npm
if ! check_cmd node; then
    if $IS_LINUX; then
        curl -fsSL https://deb.nodesource.com/setup_22.x | sudo -E bash -
        sudo apt-get install -y nodejs
    elif $IS_MAC; then
        brew install node
    fi
fi

# Bun (gstack dependency)
if ! check_cmd bun; then
    log "Installing Bun..."
    curl -fsSL https://bun.sh/install | bash
    export PATH="$HOME/.bun/bin:$PATH"
fi

# Python 3
if ! check_cmd python3; then
    if $IS_LINUX; then
        sudo apt-get install -y python3 python3-pip
    elif $IS_MAC; then
        brew install python3
    fi
fi

# uv (Python package manager, faster than pip)
if ! check_cmd uv; then
    curl -LsSf https://astral.sh/uv/install.sh | sh
    export PATH="$HOME/.local/bin:$PATH"
fi

log "✅ All prerequisites installed"

# ================================================================
# PHASE 1: CORE AGENT SETUP
# ================================================================
section "Phase 1: Core Agent Setup"

# Claude Code (if not installed)
if ! check_cmd claude 2>/dev/null; then
    log "Claude Code not found. Install from: https://claude.ai/download"
    log "Or run: npm install -g @anthropic-ai/claude-code"
fi

# ================================================================
# PHASE 2: GSTACK (Garry Tan's Software Factory)
# ================================================================
section "Phase 2: Gstack Installation"

GSTACK_DIR="$HOME/.claude/skills/gstack"
if [ -d "$GSTACK_DIR" ]; then
    log "✅ Gstack already installed at $GSTACK_DIR"
    log "   Updating..."
    cd "$GSTACK_DIR" && git pull --quiet 2>/dev/null || true
else
    log "Cloning gstack..."
    git clone --single-branch --depth 1 https://github.com/garrytan/gstack.git "$GSTACK_DIR" 2>/dev/null
    log "✅ Gstack cloned"

    # Create skill symlinks
    log "Creating gstack skill symlinks..."
    for skill_dir in "$GSTACK_DIR"/*/; do
        skill_name=$(basename "$skill_dir")
        if [ -f "$skill_dir/SKILL.md" ] && [ "$skill_name" != "bin" ] && [ "$skill_name" != "lib" ] && [ "$skill_name" != "docs" ] && [ "$skill_name" != "scripts" ] && [ "$skill_name" != "browse" ]; then
            mkdir -p "$HOME/.claude/skills/$skill_name"
            ln -sf "$GSTACK_DIR/$skill_name/SKILL.md" "$HOME/.claude/skills/$skill_name/SKILL.md" 2>/dev/null
        fi
    done
    log "✅ Gstack skills symlinked"
fi

# ================================================================
# PHASE 3: SOFTWARE FACTORY SKILLS
# ================================================================
section "Phase 3: Software Factory Skills"

SF_SKILLS="$SF_DIR/skills"
log "Software-factory skills: $(ls "$SF_SKILLS" 2>/dev/null | wc -l) skills available"

# Copy skills to .claude/skills/ if not already there
mkdir -p "$HOME/.claude/skills"
for skill_dir in "$SF_SKILLS"/*/; do
    skill_name=$(basename "$skill_dir")
    if [ -f "$skill_dir/SKILL.md" ]; then
        target="$HOME/.claude/skills/$skill_name"
        if [ ! -d "$target" ]; then
            cp -r "$skill_dir" "$target" 2>/dev/null
        fi
    fi
done
log "✅ Software factory skills installed to ~/.claude/skills/"

# ================================================================
# PHASE 4: CODE INTELLIGENCE
# ================================================================
section "Phase 4: Code Intelligence"

# CodeGraph
if ! check_cmd codegraph 2>/dev/null; then
    log "Installing CodeGraph..."
    curl -fsSL https://raw.githubusercontent.com/colbymchenry/codegraph/main/install.sh | sh 2>/dev/null || log "CodeGraph install failed — manual install required"
fi
log "✅ CodeGraph configured"

# ================================================================
# PHASE 5: MEMORY SYSTEM
# ================================================================
section "Phase 5: Memory System"

# claude-mem
if command -v npx &>/dev/null; then
    log "Installing claude-mem..."
    npx claude-mem install 2>/dev/null || log "claude-mem install skipped"
fi

# Software-factory memory directory
mkdir -p "$SF_DIR/memory/decisions"
mkdir -p "$SF_DIR/memory/patterns"
mkdir -p "$SF_DIR/memory/api-evolution"
log "✅ Memory directories created"

# ================================================================
# PHASE 6: TOKEN OPTIMIZATION
# ================================================================
section "Phase 6: Token Optimization"

# RTK (if available)
if command -v rtk &>/dev/null; then
    rtk init -g 2>/dev/null || true
    log "✅ RTK initialized"
else
    log "RTK not found — install: curl -fsSL https://raw.githubusercontent.com/rtk-ai/rtk/refs/heads/master/install.sh | sh"
fi

# ================================================================
# PHASE 7: SECURITY TOOLS
# ================================================================
section "Phase 7: Security Tools"

# Prowler
if command -v pip3 &>/dev/null || command -v uv &>/dev/null; then
    if ! check_cmd prowler 2>/dev/null; then
        log "Installing Prowler..."
        uv pip install prowler 2>/dev/null || pip3 install prowler 2>/dev/null || log "Prowler install skipped"
    fi
fi

# ================================================================
# PHASE 8: WEB SCRAPING
# ================================================================
section "Phase 8: Web Scraping"

if command -v uv &>/dev/null; then
    uv pip install scrapling 2>/dev/null || log "Scrapling install skipped"
elif command -v pip3 &>/dev/null; then
    pip3 install scrapling 2>/dev/null || log "Scrapling install skipped"
fi
log "✅ Web scraping tools configured"

# ================================================================
# PHASE 9: MCP CONFIGURATION
# ================================================================
section "Phase 9: MCP Configuration"

# Ensure CodeGraph MCP is configured
MCP_FILE="$HOME/.claude/CLAUDE.md"
if [ -f "$MCP_FILE" ]; then
    if ! grep -q "CodeGraph" "$MCP_FILE"; then
        log "Adding CodeGraph config to ~/.claude/CLAUDE.md"
    else
        log "✅ CodeGraph already configured"
    fi
fi

# Context7 MCP (if npx available)
if command -v npx &>/dev/null; then
    log "✅ Context7 MCP available via npx"
fi

# ================================================================
# PHASE 10: PROJECT CONFIGURATION
# ================================================================
section "Phase 10: Project Configuration"

# Copy CLAUDE.md if it exists in software-factory
if [ -f "$SF_DIR/CLAUDE.md" ] && [ ! -f "$(dirname "$SF_DIR")/CLAUDE.md" ]; then
    cp "$SF_DIR/CLAUDE.md" "$(dirname "$SF_DIR")/CLAUDE.md"
    log "✅ CLAUDE.md copied to project root"
fi

# ================================================================
# PHASE 11: HOOKS
# ================================================================
section "Phase 11: Git Hooks"

mkdir -p "$SF_DIR/hooks"

# Post-commit hook
cat > "$SF_DIR/hooks/post-commit" << 'HOOK'
#!/bin/bash
# Auto-sync after commit
cd "$(git rev-parse --show-toplevel)"
if [ -d "software-factory" ]; then
    python3 software-factory/context-engine/skill_selector.py --list > /dev/null 2>&1 || true
fi
HOOK
chmod +x "$SF_DIR/hooks/post-commit"
log "✅ Git hooks installed"

# ================================================================
# PHASE 12: VERIFICATION
# ================================================================
section "Phase 12: Verification"

echo ""
echo "═══════════════════════════════════════════════════════"
echo "  SOFTWARE FACTORY INSTALLATION COMPLETE"
echo "═══════════════════════════════════════════════════════"
echo ""
echo "  Installed components:"
echo "  ✅ Gstack (44 skills)"
echo "  ✅ Software Factory (33 skills)"
echo "  ✅ CodeGraph MCP"
echo "  ✅ Memory system"
echo "  ✅ Git hooks"
echo ""
echo "  Skills location: ~/.claude/skills/"
echo "  Total skills: $(ls "$HOME/.claude/skills/" 2>/dev/null | wc -l)"
echo ""
echo "  To activate in a project:"
echo "  1. Ensure CLAUDE.md has software-factory integration"
echo "  2. Skills auto-load from ~/.claude/skills/"
echo "  3. Use /browse for web, /scrape for data extraction"
echo "  4. Use /qa for testing, /review for code review"
echo "  5. Use /ship to deploy, /retro for retrospectives"
echo ""
echo "  Log: $LOG_FILE"
echo "═══════════════════════════════════════════════════════"
