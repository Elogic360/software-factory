#!/bin/bash
# ================================================================
# SOFTWARE FACTORY — TOOL VERIFICATION SCRIPT
# ================================================================
# Verifies all tools are installed and working
# Usage: bash software-factory/scripts/verify-tools.sh
# ================================================================

set -e

GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

SF_DIR="$(cd "$(dirname "$0")/.." && pwd)"
INTEGRATIONS_DIR="$SF_DIR/integrations"

echo ""
echo "=========================================="
echo "  SOFTWARE FACTORY — TOOL VERIFICATION"
echo "=========================================="
echo ""

PASS=0
FAIL=0
WARN=0

check() {
    local name=$1
    local cmd=$2
    local required=${3:-true}
    if eval "$cmd" &>/dev/null; then
        echo -e "  ${GREEN}✓${NC} $name"
        ((PASS++))
    elif [ "$required" = "true" ]; then
        echo -e "  ${RED}✗${NC} $name (REQUIRED — not installed)"
        ((FAIL++))
    else
        echo -e "  ${YELLOW}~${NC} $name (optional — not installed)"
        ((WARN++))
    fi
}

# ================================================================
# CORE TOOLS
# ================================================================
echo "Code Intelligence:"
check "CodeGraph" "command -v codegraph" true
check "Gortex" "command -v gortex" false

echo ""
echo "Token Optimization:"
check "RTK" "command -v rtk" true
check "Caveman" "test -d $HOME/.claude/skills/caveman || test -d $HOME/.claude/skills/caveman-compress" true
check "OpenWolf" "command -v openwolf" false

echo ""
echo "Memory:"
check "Claude-Mem" "test -d $HOME/.claude-mem" true

echo ""
echo "Security:"
check "Prowler" "command -v prowler" false
check "Pentest-ai" "command -v ptai" false

echo ""
echo "Development Tools:"
check "Zoxide" "command -v zoxide" false
check "Starship" "command -v starship" false

echo ""
echo "Python Packages:"
check "Scrapling" "python3 -c 'import scrapling'" false

echo ""
echo "MCP Servers:"
check "CodeGraph MCP" "codegraph status" false

echo ""
echo "Resource Repositories:"
for dir in "$INTEGRATIONS_DIR"/*/; do
    if [ -d "$dir/.git" ]; then
        name=$(basename "$dir")
        echo -e "  ${GREEN}✓${NC} $name"
        ((PASS++))
    fi
done

# ================================================================
# SOFT SKILLS
# ================================================================
echo ""
echo "Software Factory Skills:"
SKILL_COUNT=$(find "$SF_DIR/skills" -name "SKILL.md" 2>/dev/null | wc -l)
echo -e "  ${GREEN}✓${NC} $SKILL_COUNT skills in software-factory/skills/"

# ================================================================
# MEMORY
# ================================================================
echo ""
echo "Memory System:"
check "software-factory/memory/" "test -d $SF_DIR/memory" true
check ".specify/memory/" "test -d .specify/memory" false
check "graphify-out/" "test -d graphify-out" false

# ================================================================
# SUMMARY
# ================================================================
echo ""
echo "=========================================="
echo "  VERIFICATION SUMMARY"
echo "=========================================="
echo -e "  ${GREEN}Passed: $PASS${NC}"
echo -e "  ${RED}Failed: $FAIL${NC}"
echo -e "  ${YELLOW}Warnings: $WARN${NC}"
echo ""

if [ $FAIL -eq 0 ]; then
    echo -e "${GREEN}All required tools are installed!${NC}"
else
    echo -e "${RED}$FAIL required tool(s) missing. Run:${NC}"
    echo "  bash software-factory/scripts/install-all-tools.sh"
fi

echo "=========================================="
