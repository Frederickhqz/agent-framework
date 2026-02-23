#!/bin/bash
# Session End Memory Flush
# Purpose: Save learnings and current state before session ends
# Called: Before context window resets or session closes

MEMORY_DIR="/data/.openclaw/workspace/memory"
CORE_FILE="$MEMORY_DIR/CORE_SYSTEM.md"
DATE=$(date +%Y-%m-%d)

log() {
    echo "[$(date '+%Y-%m-%d %H:%M')] $1"
}

log "Running session-end memory flush..."

# Read current learnings from CORE_SYSTEM.md
LEARNINGS=$(grep -A 10 "## Recent Learnings" "$CORE_FILE" 2>/dev/null | tail -n +2)

if [ -n "$LEARNINGS" ] && [ "$LEARNINGS" != "- " ]; then
    # Save learnings to short-term memory
    LEARNING_FILE="$MEMORY_DIR/short-term/${DATE}-learnings.md"
    
    cat > "$LEARNING_FILE" << EOF
# Session Learnings - $DATE

## Key Learnings
$LEARNINGS

## Session Summary
- Started: $(grep "Session Start" "$CORE_FILE" | cut -d':' -f2-)
- Ended: $(date +%Y-%m-%d)

## Decisions Made
- 

## Solutions Found
- 

EOF
    
    log "Saved learnings to: $LEARNING_FILE"
else
    log "No new learnings to save"
fi

# Update CORE_SYSTEM.md for next session
sed -i "s/## Session Start Time.*/## Session Start Time $DATE/" "$CORE_FILE"
sed -i "s/## Recent Learnings.*/## Recent Learnings\n- /" "$CORE_FILE"

# Re-index with QMD
/data/.openclaw/bin/qmd update --collection memory 2>/dev/null

log "Session flush complete!"
