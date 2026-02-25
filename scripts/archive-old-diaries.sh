#!/bin/bash
# Archive old diary entries (older than 30 days)
# Keeps INDEX.md updated

DIARY_DIR="/data/.openclaw/workspace/memory/diary"
ARCHIVE_DIR="$DIARY_DIR/archive"
INDEX_FILE="$DIARY_DIR/INDEX.md"
DAYS_TO_KEEP=30

# Create archive directory
mkdir -p "$ARCHIVE_DIR"

# Find and archive old entries
find "$DIARY_DIR" -maxdepth 1 -name "*-curiosity.md" -type f -mtime +$DAYS_TO_KEEP | while read file; do
    BASENAME=$(basename "$file")
    echo "Archiving: $BASENAME"
    
    # Move to archive
    mv "$file" "$ARCHIVE_DIR/"
    
    # Update INDEX.md - remove entry
    # Extract date from filename (YYYY-MM-DD)
    DATE=$(echo "$BASENAME" | grep -oE '[0-9]{4}-[0-9]{2}-[0-9]{2}')
    
    # Remove line from INDEX.md
    if [ -f "$INDEX_FILE" ]; then
        sed -i "/\[$DATE\]/d" "$INDEX_FILE"
    fi
done

# Compress archive if it gets large
ARCHIVE_SIZE=$(du -sm "$ARCHIVE_DIR" 2>/dev/null | cut -f1)
if [ "$ARCHIVE_SIZE" -gt 10 ]; then
    echo "Archive getting large (${ARCHIVE_SIZE}MB), consider manual cleanup"
fi

echo "Diary archive complete. Archived files in: $ARCHIVE_DIR"
