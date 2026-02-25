#!/bin/bash
# Verify framework installation

set -euo pipefail

ERRORS=0

echo "=== OpenClaw Agent Framework Verification ==="
echo ""

# 1. Check directory structure
echo "Checking directory structure..."
DIRS=(
    "/data/.openclaw/workspace/memory"
    "/data/.openclaw/workspace/memory/stationary"
    "/data/.openclaw/workspace/memory/short-term"
    "/data/.openclaw/workspace/memory/instant"
    "/data/.openclaw/workspace/memory/experiments"
    "/data/.openclaw/workspace/memory/archive"
    "/data/.openclaw/workspace/memory/diary"
    "/data/.openclaw/workspace/scripts"
)

for dir in "${DIRS[@]}"; do
    if [ -d "$dir" ]; then
        echo "  ✓ $dir"
    else
        echo "  ✗ Missing: $dir"
        ((ERRORS++))
    fi
done
echo ""

# 2. Check core files
echo "Checking core files..."
FILES=(
    "/data/.openclaw/workspace/HEARTBEAT.md"
    "/data/.openclaw/workspace/memory/PROJECTS.md"
    "/data/.openclaw/workspace/memory/RETENTION_POLICY.md"
)

for file in "${FILES[@]}"; do
    if [ -f "$file" ]; then
        echo "  ✓ $file"
    else
        echo "  ✗ Missing: $file"
        ((ERRORS++))
    fi
done
echo ""

# 3. Check scripts
echo "Checking scripts..."
SCRIPTS=(
    "/data/.openclaw/workspace/scripts/memory-janitor.sh"
    "/data/.openclaw/workspace/scripts/compact-fluff.sh"
    "/data/.openclaw/workspace/scripts/session-flush.sh"
)

for script in "${SCRIPTS[@]}"; do
    if [ -f "$script" ] && [ -x "$script" ]; then
        echo "  ✓ $script"
    else
        echo "  ✗ Missing or not executable: $script"
        ((ERRORS++))
    fi
done
echo ""

# 4. Check QMD
echo "Checking QMD installation..."
if command -v /data/.openclaw/bin/qmd &> /dev/null; then
    echo "  ✓ QMD found"
    /data/.openclaw/bin/qmd status 2>/dev/null || echo "  ⚠ QMD status check failed"
else
    echo "  ✗ QMD not found at /data/.openclaw/bin/qmd"
    ((ERRORS++))
fi
echo ""

# 5. Check cron jobs
echo "Checking cron jobs..."
if crontab -l 2>/dev/null | grep -q "memory-janitor"; then
    echo "  ✓ Cron jobs configured"
else
    echo "  ⚠ No cron jobs found for memory-janitor"
fi
echo ""

# Summary
echo "==================================="
if [ $ERRORS -eq 0 ]; then
    echo "✅ All checks passed!"
    echo "Framework is ready to use."
    exit 0
else
    echo "❌ Found $ERRORS error(s)"
    echo "See above for details."
    exit 1
fi
