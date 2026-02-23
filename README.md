# OpenClaw Agent Framework

Proactive memory management and task handling system for OpenClaw agents.

## Overview

This framework enables OpenClaw agents to:
- **Self-infer tasks** from conversation (no manual entry needed)
- **Auto-manage memory** - fluff compaction during ops, heavy cleaning at night
- **Detect session boundaries** - know when to flush and start fresh
- **Never lose real learnings** - only conversational fluff gets pruned

## Quick Start

1. **Initialize git** in your agent workspace
2. **Install QMD** (see QMD Setup below)
3. **Add cron jobs** for nightly janitor (2 AM & 3 AM)
4. **Copy scripts** to your scripts folder

## What's Included

| Component | Description |
|-----------|-------------|
| `HEARTBEAT.md` | Task inference & memory management rules |
| `MEMORY_FRAMEWORK.md` | Complete documentation |
| `memory/` | Memory tier templates (P0/P1/P2) |
| `scripts/` | Janitor, fluff compactor, session flush |
| `skills/qmd/` | QMD skill for semantic search |

## QMD Setup

```bash
# Install Bun
curl -fsSL https://bun.sh/install | bash

# Install QMD via Bun
bun add -g @tobilu/qmd

# Create symlink
ln -sf /data/.bun/bin/qmd /data/.openclaw/bin/qmd

# Configure collection
/data/.openclaw/bin/qmd collection add /data/.openclaw/workspace/memory --name memory --mask "**/*.md"
/data/.openclaw/bin/qmd embed --collection memory

# Start MCP server
/data/.openclaw/bin/qmd mcp --http --daemon
```

## Documentation

See [MEMORY_FRAMEWORK.md](./MEMORY_FRAMEWORK.md) for complete documentation.

## Architecture

```
Session → Task Inference → PROJECTS.md
                          ↓
                    Session End → session-flush.sh
                          ↓
                    Memory Tiers
                      P0: stationary/ (permanent)
                      P1: short-term/ (permanent, compress)
                      P2: instant/ (7 days → compress)
                          ↓
              Nightly (2-3 AM, if no tasks)
                          ↓
                    memory-janitor.sh
```

## Key Principles

1. **Never delete real things** - Only fluff gets pruned
2. **Proactive task handling** - Infer from conversation
3. **Nightly is conditional** - Janitor only if no tasks pending
4. **Session boundaries** - Auto-flush on topic change or silence

## Credits

Based on Felix memoryOS framework with QMD for semantic search.
