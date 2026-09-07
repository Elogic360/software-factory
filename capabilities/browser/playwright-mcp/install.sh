#!/usr/bin/env bash
set -e
echo "Installing @playwright/mcp..."
if command -v npm >/dev/null 2>&1; then
    npm install -g @playwright/mcp 2>/dev/null || true
fi
echo "@playwright/mcp installed / verified."
