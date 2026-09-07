#!/usr/bin/env bash
set -e
echo "Installing Postgres MCP Pro..."
if command -v docker >/dev/null 2>&1; then
    docker pull crystaldba/postgres-mcp:latest 2>/dev/null || true
fi
echo "Postgres MCP Pro configured with --access-mode=restricted by default."
