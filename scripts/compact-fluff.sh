#!/bin/bash
# Lightweight Fluff Compactor - Runs during normal operation
# Purpose: Compress conversational fluff without heavy processing

MEMORY_DIR="/data/.openclaw/workspace/memory"
INSTANT_DIR="$MEMORY_DIR/instant"

# Quick check - skip if recent activity
RECENT_FILES=$(find "$INSTANT_DIR" -type f -mmin -30 2>/dev/null)
if [ -n "$RECENT_FILES" ]; then
    echo "Recent activity detected, skipping lightweight compaction"
    exit 0
fi

# Find old session files (last 2+ hours) that are just fluff
find "$INSTANT_DIR" -type f -mmin +120 -name "*.md" 2>/dev/null | while read file; do
    # Check if file is mostly fluff (greetings, acknowledgments)
    LINES=$(wc -l < "$file")
    if [ "$LINES" -lt 10 ]; then
        # Small file - check content
        if grep -qi "heartbeat\|hearthbeat_ok\|thanks\|ok\|got it\|sure\|yes" "$file" 2>/dev/null; then
            rm -v "$file" 2>/dev/null
            echo "Removed fluff: $file"
        fi
    fi
done

# Re-index if files changed
/data/.openclaw/bin/qmd update --collection memory 2>/dev/null

echo "Lightweight compaction complete"
