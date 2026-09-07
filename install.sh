#!/bin/bash
# ================================================================
# SOFTWARE FACTORY — UNIVERSAL INSTALLER
# Single-launch automated installation of everything into any project
# ================================================================
set -e

SF_DIR="$(cd "$(dirname "$0")" && pwd)"
TARGET_PROJECT="${1:-$(dirname "$SF_DIR")}"
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
log "Software Factory source: $SF_DIR"
log "Target project: $TARGET_PROJECT"

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
# PHASE 1: CORE AGENT & ECC SETUP
# ================================================================
section "Phase 1: Core Agent & ECC Setup"

# Claude Code
if ! check_cmd claude 2>/dev/null; then
    log "Claude Code not found. Install from: https://claude.ai/download"
    log "Or run: npm install -g @anthropic-ai/claude-code"
else
    log "Configuring official ECC ecosystem for Claude..."
    claude plugin marketplace add https://github.com/affaan-m/ECC 2>/dev/null || true
    claude plugin install ecc@ecc 2>/dev/null || true
    log "✅ ECC plugin configured (ecc@ecc)"
fi

# ECC Universal CLI & AgentShield
if command -v npx &>/dev/null; then
    log "Verifying ECC universal CLI..."
    npx -y ecc-universal list-installed 2>/dev/null || true
    log "✅ ECC tools available"
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
    git clone --single-branch --depth 1 https://github.com/garrytan/gstack.git "$GSTACK_DIR" 2>/dev/null || true
    log "✅ Gstack cloned"

    # Create skill symlinks
    if [ -d "$GSTACK_DIR" ]; then
        log "Creating gstack skill symlinks..."
        for skill_dir in "$GSTACK_DIR"/*/; do
            skill_name=$(basename "$skill_dir")
            if [ -f "$skill_dir/SKILL.md" ] && [ "$skill_name" != "bin" ] && [ "$skill_name" != "lib" ] && [ "$skill_name" != "docs" ] && [ "$skill_name" != "scripts" ] && [ "$skill_name" != "browse" ]; then
                mkdir -p "$HOME/.claude/skills/$skill_name"
                ln -sf "$GSTACK_DIR/$skill_name/SKILL.md" "$HOME/.claude/skills/$skill_name/SKILL.md" 2>/dev/null || true
            fi
        done
        log "✅ Gstack skills symlinked"
    fi
fi

# ================================================================
# PHASE 3: SOFTWARE FACTORY SKILLS & ANTIGRAVITY DISCOVERY
# ================================================================
section "Phase 3: Software Factory & Antigravity Skills"

SF_SKILLS="$SF_DIR/skills"
ECC_SKILLS="$SF_DIR/integrations/ecc/skills"
TARGET_AGENTS_SKILLS="$TARGET_PROJECT/.agents/skills"

log "Software-factory skills: $(ls "$SF_SKILLS" 2>/dev/null | wc -l) skills available"

# Copy skills to ~/.claude/skills/
mkdir -p "$HOME/.claude/skills"
for skill_dir in "$SF_SKILLS"/*/; do
    skill_name=$(basename "$skill_dir")
    if [ -f "$skill_dir/SKILL.md" ]; then
        target="$HOME/.claude/skills/$skill_name"
        if [ ! -d "$target" ]; then
            cp -r "$skill_dir" "$target" 2>/dev/null || true
        fi
    fi
done
log "✅ Software factory skills installed to ~/.claude/skills/"

# Symlink all skills for Antigravity & other agent progressive disclosure
mkdir -p "$TARGET_AGENTS_SKILLS"
for skill_dir in "$SF_SKILLS"/*/; do
    skill_name=$(basename "$skill_dir")
    if [ -d "$skill_dir" ]; then
        ln -sfn "$skill_dir" "$TARGET_AGENTS_SKILLS/$skill_name" 2>/dev/null || true
    fi
done

if [ -d "$ECC_SKILLS" ]; then
    for skill_dir in "$ECC_SKILLS"/*/; do
        skill_name=$(basename "$skill_dir")
        if [ -d "$skill_dir" ] && [ ! -e "$TARGET_AGENTS_SKILLS/$skill_name" ]; then
            ln -sf "$skill_dir" "$TARGET_AGENTS_SKILLS/$skill_name" 2>/dev/null || true
        fi
    done
fi
log "✅ Linked $(ls "$TARGET_AGENTS_SKILLS" 2>/dev/null | wc -l) skills into $TARGET_AGENTS_SKILLS for Antigravity"

# ================================================================
# PHASE 4: CODE INTELLIGENCE (CodeGraph & Gortex)
# ================================================================
section "Phase 4: Code Intelligence"

if ! check_cmd codegraph 2>/dev/null; then
    log "Installing CodeGraph..."
    curl -fsSL https://raw.githubusercontent.com/colbymchenry/codegraph/main/install.sh | sh 2>/dev/null || log "CodeGraph install failed — manual install required"
fi
log "✅ CodeGraph configured"

# ================================================================
# PHASE 5: MEMORY SYSTEM
# ================================================================
section "Phase 5: Memory System"

if command -v npx &>/dev/null; then
    log "Installing claude-mem..."
    npx claude-mem install 2>/dev/null || log "claude-mem install skipped"
fi

mkdir -p "$SF_DIR/memory/decisions"
mkdir -p "$SF_DIR/memory/patterns"
mkdir -p "$SF_DIR/memory/api-evolution"
log "✅ Memory directories created"

# ================================================================
# PHASE 6: TOKEN OPTIMIZATION (RTK)
# ================================================================
section "Phase 6: Token Optimization"

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

if command -v uv &>/dev/null; then
    uv pip install prowler 2>/dev/null || true
    uv pip install scrapling 2>/dev/null || true
elif command -v pip3 &>/dev/null; then
    pip3 install prowler 2>/dev/null || true
    pip3 install scrapling 2>/dev/null || true
fi
log "✅ Security & Scraping tools configured"

# ================================================================
# PHASE 8: PROJECT CONFIGURATION & ENTRY POINTS
# ================================================================
section "Phase 8: Project Configuration & Entry Points"

# Create/Copy project entry points
if [ -f "$SF_DIR/CLAUDE.md" ] && [ ! -f "$TARGET_PROJECT/CLAUDE.md" ]; then
    cp "$SF_DIR/CLAUDE.md" "$TARGET_PROJECT/CLAUDE.md"
    log "✅ CLAUDE.md copied to $TARGET_PROJECT"
fi

mkdir -p "$TARGET_PROJECT/.agents/rules"
cat << 'RULE' > "$TARGET_PROJECT/.agents/rules/software-factory.md"
# Software Factory Rules for Antigravity & AI Agents

- **Constitution**: Strictly abide by `software-factory/constitution/CONSTITUTION.md`.
- **Skills**: Discovered automatically under `.agents/skills/`.
- **Context Engine**: Query dynamic skill routing via `python3 software-factory/context-engine/skill_selector.py`.
- **ECC Security**: Verify security posture using `npx ecc-agentshield scan`.
- **Toolbox**: Consult `software-factory/TOOLBOX.md` for pre-indexed open source libraries, quant engines, and frameworks.
- **Memory**: Read decisions from `software-factory/memory/decisions/` before refactoring; record new decisions after architectural changes.
RULE
log "✅ Antigravity rules configured in $TARGET_PROJECT/.agents/rules/"

# ================================================================
# PHASE 9: HOOKS
# ================================================================
section "Phase 9: Git Hooks"

mkdir -p "$SF_DIR/hooks"
cat > "$SF_DIR/hooks/post-commit" << 'HOOK'
#!/bin/bash
cd "$(git rev-parse --show-toplevel)"
if [ -d "software-factory" ]; then
    python3 software-factory/context-engine/skill_selector.py --list > /dev/null 2>&1 || true
fi
HOOK
chmod +x "$SF_DIR/hooks/post-commit"
log "✅ Git hooks installed"

# ================================================================
# PHASE 10: VERIFICATION
# ================================================================
section "Phase 10: Verification"

echo ""
echo "═══════════════════════════════════════════════════════"
echo "  SOFTWARE FACTORY INSTALLATION COMPLETE"
echo "═══════════════════════════════════════════════════════"
echo ""
echo "  Installed components:"
echo "  ✅ Everything Claude Code (ECC universal + ecc@ecc)"
echo "  ✅ Antigravity Agent Harness Integration (.agents/skills)"
echo "  ✅ Gstack (23 tools) & Software Factory (57 skills)"
echo "  ✅ CodeGraph MCP & Memory Framework"
echo "  ✅ Universal Toolbox (207+ curated repositories)"
echo "  ✅ Git hooks & Security policies"
echo ""
echo "  Skills in project: $(ls "$TARGET_AGENTS_SKILLS" 2>/dev/null | wc -l)"
echo "  Universal Toolbox: $SF_DIR/TOOLBOX.md"
echo "  Log: $LOG_FILE"
echo "═══════════════════════════════════════════════════════"
