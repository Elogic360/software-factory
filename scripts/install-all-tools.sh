#!/bin/bash
# ================================================================
# SOFTWARE FACTORY — FULL TOOL INSTALLATION SCRIPT
# ================================================================
# Run this script to install all tools referenced in software-factoryBuild.md
# Usage: bash software-factory/scripts/install-all-tools.sh
# ================================================================

set -e

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

log() { echo -e "${BLUE}[SF]${NC} $1"; }
success() { echo -e "${GREEN}[OK]${NC} $1"; }
warn() { echo -e "${YELLOW}[WARN]${NC} $1"; }
fail() { echo -e "${RED}[FAIL]${NC} $1"; }

SF_DIR="$(cd "$(dirname "$0")/.." && pwd)"
INTEGRATIONS_DIR="$SF_DIR/integrations"

mkdir -p "$INTEGRATIONS_DIR"

# ================================================================
# PHASE 1: System Prerequisites
# ================================================================
log "Phase 1: Checking prerequisites..."

# Node.js
if ! command -v node &> /dev/null; then
    warn "Node.js not found. Installing via nvm..."
    curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.0/install.sh | bash
    export NVM_DIR="$HOME/.nvm"
    [ -s "$NVM_DIR/nvm.sh" ] && . "$NVM_DIR/nvm.sh"
    nvm install 20
fi
success "Node.js $(node --version)"

# Python
if ! command -v python3 &> /dev/null; then
    warn "Python3 not found"
    fail "Please install Python 3.10+ manually"
    exit 1
fi
success "Python $(python3 --version)"

# Git
if ! command -v git &> /dev/null; then
    fail "Git not found. Please install git."
    exit 1
fi
success "Git $(git --version)"

# ================================================================
# PHASE 2: Code Intelligence
# ================================================================
log "Phase 2: Installing code intelligence tools..."

# CodeGraph
if ! command -v codegraph &> /dev/null; then
    log "Installing CodeGraph..."
    curl -fsSL https://raw.githubusercontent.com/colbymchenry/codegraph/main/install.sh | sh 2>/dev/null || warn "CodeGraph install failed — install manually"
else
    success "CodeGraph already installed"
fi

# Gortex
if ! command -v gortex &> /dev/null; then
    log "Installing Gortex..."
    curl -fsSL https://get.gortex.dev | sh 2>/dev/null || warn "Gortex install failed — install manually"
else
    success "Gortex already installed"
fi

# ================================================================
# PHASE 3: Token Optimization
# ================================================================
log "Phase 3: Installing token optimization tools..."

# RTK
if ! command -v rtk &> /dev/null; then
    log "Installing RTK..."
    curl -fsSL https://raw.githubusercontent.com/rtk-ai/rtk/refs/heads/master/install.sh | sh 2>/dev/null || warn "RTK install failed — install manually"
else
    success "RTK already installed"
fi

# Caveman
if [ ! -d "$HOME/.claude/skills/caveman" ]; then
    log "Installing Caveman..."
    curl -fsSL https://raw.githubusercontent.com/JuliusBrussee/caveman/main/install.sh | bash 2>/dev/null || warn "Caveman install failed — install manually"
else
    success "Caveman already installed"
fi

# OpenWolf
if ! command -v openwolf &> /dev/null; then
    log "Installing OpenWolf..."
    npm install -g openwolf 2>/dev/null || warn "OpenWolf install failed"
else
    success "OpenWolf already installed"
fi

# ================================================================
# PHASE 4: Memory System
# ================================================================
log "Phase 4: Installing memory system..."

# Claude-Mem
if [ ! -d "$HOME/.claude-mem" ]; then
    log "Installing Claude-Mem..."
    npx claude-mem install 2>/dev/null || warn "Claude-Mem install failed"
else
    success "Claude-Mem already installed"
fi

# ================================================================
# PHASE 5: Security Tools
# ================================================================
log "Phase 5: Installing security tools..."

# Prowler
if ! command -v prowler &> /dev/null; then
    log "Installing Prowler..."
    pip3 install prowler 2>/dev/null || warn "Prowler install failed"
else
    success "Prowler already installed"
fi

# Pentest-ai
if ! command -v ptai &> /dev/null; then
    log "Installing Pentest-ai..."
    pip3 install ptai 2>/dev/null || warn "Pentest-ai install failed"
else
    success "Pentest-ai already installed"
fi

# ================================================================
# PHASE 6: Web Scraping
# ================================================================
log "Phase 6: Installing web scraping tools..."

# Scrapling
python3 -c "import scrapling" 2>/dev/null || {
    log "Installing Scrapling..."
    pip3 install scrapling 2>/dev/null || warn "Scrapling install failed"
}
success "Scrapling available"

# ================================================================
# PHASE 7: Development Tools
# ================================================================
log "Phase 7: Installing development tools..."

# Zoxide
if ! command -v zoxide &> /dev/null; then
    log "Installing Zoxide..."
    curl -sSfL https://raw.githubusercontent.com/ajeetdsouza/zoxide/main/install.sh | sh 2>/dev/null || warn "Zoxide install failed"
else
    success "Zoxide already installed"
fi

# Starship
if ! command -v starship &> /dev/null; then
    log "Installing Starship..."
    curl -sS https://starship.rs/install.sh | sh 2>/dev/null || warn "Starship install failed"
else
    success "Starship already installed"
fi

# ================================================================
# PHASE 8: Clone Resource Repositories
# ================================================================
log "Phase 8: Cloning resource repositories..."

clone_if_missing() {
    local name=$1
    local url=$2
    local target="$INTEGRATIONS_DIR/$name"
    if [ ! -d "$target" ]; then
        log "Cloning $name..."
        git clone --depth 1 "$url" "$target" 2>/dev/null || warn "Failed to clone $name"
    else
        success "$name already cloned"
    fi
}

clone_if_missing "anthropic-skills" "https://github.com/anthropics/skills.git"
clone_if_missing "ecc" "https://github.com/affaan-m/ECC.git"
clone_if_missing "claude-skills-secondsky" "https://github.com/secondsky/claude-skills.git"
clone_if_missing "claude-skills-jeffallan" "https://github.com/Jeffallan/claude-skills.git"
clone_if_missing "antigravity-skills" "https://github.com/sickn33/antigravity-awesome-skills.git"
clone_if_missing "mercury-skills" "https://github.com/cosmicstack-labs/mercury-agent-skills.git"
clone_if_missing "goose-skills" "https://github.com/gooseworks-ai/goose-skills.git"
clone_if_missing "ui-ux-pro-max" "https://github.com/nextlevelbuilder/ui-ux-pro-max-skill.git"
clone_if_missing "notfair" "https://github.com/nowork-studio/notfair.git"
clone_if_missing "openskills" "https://github.com/numman-ali/openskills.git"
clone_if_missing "prompt-guide" "https://github.com/dair-ai/Prompt-Engineering-Guide.git"
clone_if_missing "genai-guide" "https://github.com/aishwaryanr/awesome-generative-ai-guide.git"

# ================================================================
# PHASE 9: Verification
# ================================================================
log "Phase 9: Verifying installation..."

echo ""
echo "=========================================="
echo "  SOFTWARE FACTORY — INSTALLATION STATUS"
echo "=========================================="
echo ""

check_tool() {
    local name=$1
    local cmd=$2
    if eval "$cmd" &>/dev/null; then
        echo -e "  ${GREEN}✓${NC} $name"
    else
        echo -e "  ${RED}✗${NC} $name (not installed)"
    fi
}

echo "Code Intelligence:"
check_tool "CodeGraph" "command -v codegraph"
check_tool "Gortex" "command -v gortex"

echo ""
echo "Token Optimization:"
check_tool "RTK" "command -v rtk"
check_tool "Caveman" "test -d ~/.claude/skills/caveman"
check_tool "OpenWolf" "command -v openwolf"

echo ""
echo "Memory:"
check_tool "Claude-Mem" "test -d ~/.claude-mem"

echo ""
echo "Security:"
check_tool "Prowler" "command -v prowler"
check_tool "Pentest-ai" "command -v ptai"

echo ""
echo "Development Tools:"
check_tool "Zoxide" "command -v zoxide"
check_tool "Starship" "command -v starship"

echo ""
echo "Resource Repositories:"
for dir in "$INTEGRATIONS_DIR"/*/; do
    if [ -d "$dir/.git" ]; then
        name=$(basename "$dir")
        echo -e "  ${GREEN}✓${NC} $name"
    fi
done

echo ""
echo "=========================================="
echo "  Installation complete!"
echo "  Run: codegraph init (in your project)"
echo "  Run: rtk init -g (for Claude Code)"
echo "=========================================="
