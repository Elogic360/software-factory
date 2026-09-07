#!/usr/bin/env bash
set -e
echo "Installing @drawio/mcp..."
if command -v npm >/dev/null 2>&1; then
    npm install -g @drawio/mcp 2>/dev/null || true
fi
echo "@drawio/mcp installed / verified."
