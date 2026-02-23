# OpenClaw Memory & Task Framework

> Complete setup guide for proactive memory management and task handling

## Overview

This framework enables an OpenClaw agent to:
- **Self-infer tasks** from conversation (no manual entry needed)
- **Auto-manage memory** - fluff compaction during ops, heavy cleaning at night
- **Detect session boundaries** - know when to flush and start fresh
- **Never lose real learnings** - only conversational fluff gets pruned

---

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    Session (Active)                        │
│  • Task Inference: "I'll check X" → auto-create task     │
│  • Fluff Compaction: compact-fluff.sh (lightweight)       │
│  • Session Boundary: Auto-flush on topic change/silence   │
└─────────────────────────────────────────────────────────────┘
                              ↓
                    Session End / Flush
                              ↓
┌─────────────────────────────────────────────────────────────┐
│                    Memory Tiers                            │
│  • P0: CORE_SYSTEM.md, stationary/ (permanent)            │
│  • P1: short-term/, experiments/ (permanent, compress)    │
│  • P2: instant/ (7 days → compress → archive)            │
└─────────────────────────────────────────────────────────────┘
                              ↓
              Nightly (2-3 AM Only, If No Tasks)
                              ↓
┌─────────────────────────────────────────────────────────────┐
│                    Janitor Scripts                          │
│  • memory-janitor.sh: Archive, compress, re-index          │
│  • Runs ONLY if Current Task = none                        │
└─────────────────────────────────────────────────────────────┘
```

---

## File Structure

```
/data/.openclaw/workspace/
├── memory/
│   ├── CORE_SYSTEM.md          # Hot memory - current task/goals
│   ├── PROJECTS.md            # Task queue & project tracking
│   ├── RETENTION_POLICY.md    # Never delete real things
│   ├── stationary/            # P0: Identity, preferences
│   ├── short-term/            # P1: Daily logs, learnings
│   ├── instant/               # P2: Raw conversation
│   ├── experiments/           # P1: Testing logs
│   └── archive/              # Compressed summaries
├── scripts/
│   ├── memory-janitor.sh     # Nightly (2-3 AM) - heavy cleanup
│   ├── compact-fluff.sh       # Lightweight - during ops
│   └── session-flush.sh       # On session end
└── HEARTBEAT.md              # Task & memory instructions
```

---

## Cron Jobs

### 1. Memory Janitor - 2 AM (Primary)
```json
{
  "name": "memory-janitor-2am",
  "schedule": "0 2 * * *",
  "tz": "America/New_York",
  "condition": "Only if Current Task = none in PROJECTS.md"
}
```

### 2. Memory Janitor - 3 AM (Backup)
```json
{
  "name": "memory-janitor",
  "schedule": "0 3 * * *",
  "tz": "America/New_York", 
  "condition": "Only if Current Task = none"
}
```

---

## Core Files

### 1. HEARTBEAT.md
```markdown
# HEARTBEAT.md - Proactive Memory & Task Management

Run every 60 minutes between 5 AM - 11 PM EST.

## Primary: Task Inference & Tracking

### On Wake - Check & Infer
1. Read memory/PROJECTS.md
2. Check current task status
3. If none → Scan recent conversation for:
   - Problems mentioned that need solving
   - Goals stated or implied
   - Work in progress I committed to

### Infer Tasks Rule
If I commit to doing something in conversation → auto-create task
- "I'll look into X" → task created
- "Let me check Y" → task created
- User asks for help → task created if multi-step

### Task Status Flow
IN_PROGRESS → WAITING_ON → COMPLETED → (infer next)
                    ↓
              BLOCKED → (flag for human)

## Secondary: Fluff Management (Ongoing)

### During Normal Operation - Auto-Compact
Periodically (every ~30 min):
- Identify conversational fluff in instant/ notes
- Compress old session chunks into summaries
- Never delete real learnings

### Session Boundary Detection
Recognize when to flush:
- Topic transition without resolution
- Explicit "thanks" or "that's all"
- Long silence (heartbeat gap >2h)
- Context getting full

## Nightly: Heavy Maintenance (2-3 AM ONLY)

### Pre-Check Before Janitor
1. Check current time (must be 2-3 AM)
2. Check: Any tasks IN_PROGRESS?
   - YES → Skip janitor, resume next day
   - NO → Safe to run

### Janitor Actions (Nightly Only)
- Archive P2 notes >7 days
- Compress to summaries
- Re-index with QMD

## Response Rules
- Task inferred: Add to PROJECTS.md + continue work
- Task in progress: Continue + log progress
- Task completed: Flush learnings → clear current
- Session boundary detected: Run session-flush.sh
- Nightly + no tasks: Run memory-janitor.sh
- Otherwise: HEARTBEAT_OK
```

### 2. PROJECTS.md
```markdown
# Active Projects & Tasks
# Auto-managed by AI - Tasks inferred from conversation

## Projects

### Project: [Name]
- Status: in_progress | completed | blocked
- Started: YYYY-MM-DD
- Ended: YYYY-MM-DD
- Summary: 
- Learnings: 

---

## Task Queue

### Current Task
- [Task description]
- Status: IN_PROGRESS
- Started: YYYY-MM-DD

### Waiting On
- [Blocked tasks]

### Recently Completed
- [Completed tasks]

---

## Task Inference Rules
When I commit to something in conversation → auto-create:
- "I'll look into X" → task created
- "Let me check Y" → task created  
- User asks for help → task created
- Problem identified → task created

### Status Flow
IN_PROGRESS → WAITING_ON → COMPLETED → (infer next)
                    ↓
              BLOCKED → (flag human)

---

## Heartbeat Action Log
| Time | Action | Result |
|------|--------|--------|
```

### 3. RETENTION_POLICY.md
```markdown
# Memory Retention Policy

## Philosophy
**Never forget real things.** Only flush conversational fluff.

## P0: Core Identity (Never Delete)
- Retention: Permanent
- Files: CORE_SYSTEM.md, stationary/*
- Description: Core identity, preferences, personality

## P1: Project Context (Never Delete)
- Retention: Permanent  
- Files: short-term/*, experiments/*
- Description: Learnings, decisions, project context

## P2: Session Notes (Fluff Only)
- Retention: 7 days → compress
- Files: instant/*
- Description: Raw conversation logs

## Archive (Never Delete)
- Location: memory/archive/
- Retention: Permanent (compressed summaries)

## What Gets Flushed (Conversational Fluff)
- Repeated greetings
- Simple acknowledgments
- Heartbeat polls
- Generic status checks

## What Gets Kept Forever
- Decisions made
- Solutions found
- Preferences expressed
- Project context
- Learnings
- Any factual information
```

---

## Scripts

### 1. memory-janitor.sh (Nightly)
```bash
#!/bin/bash
# Memory Janitor Script
# Run daily at 2-3 AM ONLY - checks for tasks first
# Purpose: Compress memory, NEVER delete real things

MEMORY_DIR="/data/.openclaw/workspace/memory"
ARCHIVE_DIR="$MEMORY_DIR/archive"

# PRE-CHECK: Skip if tasks pending
CURRENT_TASK=$(grep -A5 "### Current Task" "$MEMORY_DIR/PROJECTS.md" | grep -v "^-" | grep -v "none" | head -1)
if [ -n "$CURRENT_TASK" ]; then
    echo "Tasks pending, skipping janitor: $CURRENT_TASK"
    exit 0
fi

# P2: Compress old session notes (7+ days)
find "$MEMORY_DIR/instant" -type f -name "*.md" -mtime +7 | while read file; do
    # Extract learnings, archive, delete fluff
done

# Re-index with QMD
/data/.openclaw/bin/qmd update --collection memory
```

### 2. compact-fluff.sh (Lightweight)
```bash
#!/bin/bash
# Lightweight Fluff Compactor
# Runs during normal operation every ~30 min
# Purpose: Remove obvious fluff without heavy processing

# Skip if recent activity (don't interrupt)
find "$MEMORY_DIR/instant" -type f -mmin -30 | if stdin; then exit 0; fi

# Remove small files that are just fluff
find "$MEMORY_DIR/instant" -type f -mmin +120 -size -1k | while read file; do
    grep -qi "heartbeat_ok\|thanks\|ok\|got it" "$file" && rm "$file"
done
```

### 3. session-flush.sh
```bash
#!/bin/bash
# Session End Memory Flush
# Purpose: Save learnings before session ends

# Read current learnings from CORE_SYSTEM.md
# Save to short-term/ as YYYY-MM-DD-learnings.md
# Update CORE_SYSTEM.md for next session
# Re-index with QMD
```

---

## QMD Setup

### Install QMD
```bash
# Install Bun (required for QMD)
curl -fsSL https://bun.sh/install | bash

# Install QMD via Bun
bun add -g @tobilu/qmd

# Create symlink
ln -sf /data/.bun/bin/qmd /data/.openclaw/bin/qmd
```

### Configure Collection
```bash
/data/.openclaw/bin/qmd collection add /data/.openclaw/workspace/memory --name memory --mask "**/*.md"

/data/.openclaw/bin/qmd embed --collection memory

# Add contexts for better search
/data/.openclaw/bin/qmd context add qmd://memory "Personal AI assistant memory"
/data/.openclaw/bin/qmd context add qmd://memory/stationary "Identity and preferences"
/data/.openclaw/bin/qmd context add qmd://memory/short-term "Daily logs"
/data/.openclaw/bin/qmd context add qmd://memory/experiments "Testing logs"
```

### Start MCP Server
```bash
/data/.openclaw/bin/qmd mcp --http --daemon
```

---

## Usage

### Task Inference Examples
| You Say | Agent Does |
|---------|------------|
| "I'll look into the API issue" | Creates task in PROJECTS.md |
| "Let me check the logs" | Creates task, starts investigating |
| "Can you debug this?" | Creates task if multi-step |

### Manual Commands
```bash
# Search memory
/data/.openclaw/bin/qmd query "project name" -c memory

# Check status
/data/.openclaw/bin/qmd status

# Force re-index
/data/.openclaw/bin/qmd update --collection memory

# Run fluff compaction (manual)
/data/.openclaw/workspace/scripts/compact-fluff.sh
```

---

## Key Principles

1. **Never delete real things** - Only fluff gets pruned
2. **Proactive task handling** - Infer from conversation, not manual entry
3. **Nightly is conditional** - Janitor only runs if no tasks pending
4. **Session boundaries** - Auto-flush on topic change or silence
5. **Hot memory** - CORE_SYSTEM.md reflects current task at all times

---

## Credits

Based on Felix memoryOS framework with QMD for semantic search.
