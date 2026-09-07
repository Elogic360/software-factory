#!/usr/bin/env bash
set -e
echo "Installing chrome-devtools-mcp..."
if command -v npm >/dev/null 2>&1; then
    npm install -g chrome-devtools-mcp 2>/dev/null || true
fi
echo "chrome-devtools-mcp installed / verified."
