#!/bin/bash
# Memory Janitor Script (Revised)
# Run daily at 3 AM: 0 3 * * * /data/.openclaw/workspace/scripts/memory-janitor.sh
# Purpose: Compress conversational fluff, NEVER delete real things

MEMORY_DIR="/data/.openclaw/workspace/memory"
ARCHIVE_DIR="$MEMORY_DIR/archive"
LOG_FILE="$MEMORY_DIR/.janitor.log"

log() {
    echo "[$(date '+%Y-%m-%d %H:%M')] $1" | tee -a "$LOG_FILE"
}

# Ensure archive directory exists
mkdir -p "$ARCHIVE_DIR"

log "Starting Memory Janitor..."

# P2: Compress old session notes into summaries (never delete)
log "Compressing old P2 session notes (7+ days)..."
find "$MEMORY_DIR/instant" -type f -name "*.md" -mtime +7 | while read file; do
    BASENAME=$(basename "$file")
    DATE_STR=$(echo "$BASENAME" | cut -d'-' -f1-3)
    
    # Create compressed summary
    SUMMARY_FILE="$ARCHIVE_DIR/${DATE_STR}-summary.md"
    
    if [ ! -f "$SUMMARY_FILE" ]; then
        echo "# Session Summary - $DATE_STR" > "$SUMMARY_FILE"
        echo "" >> "$SUMMARY_FILE"
        echo "## Compressed from" >> "$SUMMARY_FILE"
        echo "- $BASENAME" >> "$SUMMARY_FILE"
        echo "" >> "$SUMMARY_FILE"
    fi
    
    # Append any non-fluff content (decisions, learnings, etc.)
    if grep -q "decision\|learning\|solution\|preference\|fact\|important" "$file" 2>/dev/null; then
        echo "" >> "$SUMMARY_FILE"
        echo "### From $BASENAME" >> "$SUMMARY_FILE"
        grep -i "decision\|learning\|solution\|preference\|fact\|important" "$file" >> "$SUMMARY_FILE" 2>/dev/null
    fi
    
    # Move original to archive
    mv -v "$file" "$ARCHIVE_DIR/" 2>/dev/null
    log "Compressed: $file -> $SUMMARY_FILE"
done

# Clean up empty directories
find "$MEMORY_DIR/instant" -type d -empty -delete 2>/dev/null
find "$ARCHIVE_DIR" -type d -empty -delete 2>/dev/null

# P1/Archive: NEVER DELETE - just compress old daily logs
log "Compressing old daily logs into monthly summaries..."
for year in 2025 2026; do
    for month in 01 02 03 04 05 06 07 08 09 10 11 12; do
        MONTH_FILES=$(find "$MEMORY_DIR/short-term" -type f -name "${year}-${month}-*.md" 2>/dev/null)
        if [ -n "$MONTH_FILES" ]; then
            MONTH_SUMMARY="$ARCHIVE_DIR/${year}-${month}-monthly.md"
            
            if [ ! -f "$MONTH_SUMMARY" ]; then
                echo "# Monthly Summary - ${year}-${month}" > "$MONTH_SUMMARY"
                echo "" >> "$MONTH_SUMMARY"
            fi
            
            # Extract key info from each daily file
            for f in $MONTH_FILES; do
                if grep -q "decision\|learning\|solution\|preference\|project\|context" "$f" 2>/dev/null; then
                    echo "" >> "$MONTH_SUMMARY"
                    echo "## $(basename "$f")" >> "$MONTH_SUMMARY"
                    grep -i "decision\|learning\|solution\|preference\|project\|context" "$f" >> "$MONTH_SUMMARY" 2>/dev/null
                fi
            done
        fi
    done
done

# Re-index with QMD
log "Re-indexing memory with QMD..."
/data/.openclaw/bin/qmd update --collection memory 2>/dev/null

log "Memory Janitor complete! (Never deleted real things)"
echo "---"
