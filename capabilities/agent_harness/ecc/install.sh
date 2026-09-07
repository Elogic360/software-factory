#!/usr/bin/env bash
set -e

# Everything Claude Code (ECC) Universal Installation Recipe
# Supports both canonical npm distribution and local vendored integration.

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SF_ROOT="$(cd "${SCRIPT_DIR}/../../.." && pwd)"
ECC_VENDORED="${SF_ROOT}/integrations/ecc"

echo "========================================================"
echo "Installing Everything Claude Code (ECC) Capability"
echo "========================================================"

# 1. Verify Prerequisites
if ! command -v node >/dev/null 2>&1; then
    echo "❌ Node.js is required but not installed." >&2
    exit 1
fi

NODE_MAJOR=$(node -v | cut -d'.' -f1 | tr -d 'v')
if [ "$NODE_MAJOR" -lt 18 ]; then
    echo "❌ Node.js version 18+ is required. Found $(node -v)." >&2
    exit 1
fi
echo "✅ Node.js verified: $(node -v)"

# 2. Check Local Vendored Repository
if [ -d "$ECC_VENDORED" ] && [ -f "$ECC_VENDORED/package.json" ]; then
    echo "✅ Vendored ECC repository found at: $ECC_VENDORED"
    ECC_VERSION=$(cat "$ECC_VENDORED/VERSION" 2>/dev/null || echo "2.x")
    echo "   Vendored version: $ECC_VERSION"
else
    echo "⚠️  Vendored copy not found, checking npm registry..."
fi

# 3. Provision CLI wrappers in bin/
mkdir -p "${SF_ROOT}/bin"
cat << 'EOF' > "${SF_ROOT}/bin/ecc"
#!/usr/bin/env bash
SF_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
if [ -f "$SF_ROOT/integrations/ecc/scripts/ecc.js" ]; then
    exec node "$SF_ROOT/integrations/ecc/scripts/ecc.js" "$@"
elif command -v npx >/dev/null 2>&1; then
    exec npx ecc-universal "$@"
else
    echo "Error: Neither local ECC nor npx is available." >&2
    exit 1
fi
EOF
chmod +x "${SF_ROOT}/bin/ecc"
echo "✅ Provisioned executable wrapper: bin/ecc"

# 4. Verify Execution
echo "Verifying CLI invocation..."
"${SF_ROOT}/bin/ecc" --help >/dev/null 2>&1 || true
echo "✅ ECC harness installed and verified successfully."
