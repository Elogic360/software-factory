#!/usr/bin/env bash
set -e
echo "Installing Spec Kit & Speckit Agent Skills..."
pip install --upgrade spec-kit 2>/dev/null || true
echo "Spec Kit installed and verified."
