# Memory Retention Policy (Revised)

## Philosophy
**Never forget real things.** Only flush conversational fluff.

## P0: Core Identity (Never Delete)
- **Retention**: Permanent
- **Files**: CORE_SYSTEM.md, stationary/*
- **Description**: Core identity, user never-forget rules, personality

## P1: Project Context (Never Delete)
- **Retention**: Permanent  
- **Files**: short-term/*, experiments/*
- **Description**: Project-specific context, learnings, decisions
- **NEVER auto-delete**: Every real thing is preserved forever

## P2: Session Notes (Fluff Only)
- **Retention**: 7 days (then compress, don't delete)
- **Files**: instant/*
- **Description**: Raw conversation logs
- **Auto-compress**: After 7 days, compress to summary

## Archive (Never Delete)
- **Location**: memory/archive/
- **Retention**: Permanent (compressed summaries)
- **Purpose**: Compressed old daily logs for reference

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

## Janitor Schedule
- **Daily (3 AM)**: Compress P2 notes older than 7 days into summaries
- **Weekly**: Merge similar memories, clean duplicates
- **Never**: Delete real information

## Commands
- `qmd status` - Check index health
- `qmd update` - Re-index after changes
- Memory-Janitor.sh - Run cleanup script
