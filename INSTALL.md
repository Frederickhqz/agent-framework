# Installation Guide

Complete setup guide for the OpenClaw Agent Framework.

## Prerequisites

- OpenClaw installed and running
- Git configured
- Bash shell access
- ~500MB free disk space (for QMD models)

## Quick Install

```bash
# 1. Clone the framework
git clone https://github.com/Frederickhqz/agent-framework.git
cd agent-framework

# 2. Copy to your OpenClaw workspace
cp -r * /data/.openclaw/workspace/

# 3. Install QMD (required for semantic search)
./scripts/install-qmd.sh

# 4. Set up cron jobs
./scripts/setup-cron.sh

# 5. Verify installation
./scripts/verify.sh
```

## Manual Setup

### Step 1: Install Bun (for QMD)

```bash
curl -fsSL https://bun.sh/install | bash
```

### Step 2: Install QMD

```bash
bun add -g @tobilu/qmd
ln -sf ~/.bun/bin/qmd /data/.openclaw/bin/qmd
```

### Step 3: Configure QMD Collection

```bash
# Create memory collection
/data/.openclaw/bin/qmd collection add /data/.openclaw/workspace/memory \
  --name memory \
  --mask "**/*.md"

# Initial indexing
/data/.openclaw/bin/qmd embed --collection memory
```

### Step 4: Start MCP Server

```bash
# Start QMD MCP server
/data/.openclaw/bin/qmd mcp --http --daemon

# Or add to systemd/startup
```

### Step 5: Set Up Cron Jobs

```bash
# Add to crontab
crontab -e

# Add these lines:
0 2 * * * /data/.openclaw/workspace/scripts/memory-janitor.sh
0 3 * * * /data/.openclaw/workspace/scripts/memory-janitor.sh
```

Or use the OpenClaw cron system:

```bash
openclaw cron add --name memory-janitor-2am \
  --schedule "0 2 * * *" \
  --command "/data/.openclaw/workspace/scripts/memory-janitor.sh"

openclaw cron add --name memory-janitor-3am \
  --schedule "0 3 * * *" \
  --command "/data/.openclaw/workspace/scripts/memory-janitor.sh"
```

## Verification

Test your installation:

```bash
# Test QMD
/data/.openclaw/bin/qmd status

# Test search
/data/.openclaw/bin/qmd query "test" -c memory

# Test scripts exist
ls -la /data/.openclaw/workspace/scripts/

# Check cron jobs
crontab -l | grep memory-janitor
```

## Troubleshooting

### QMD not found
```bash
# Check if Bun is in PATH
which bun || echo 'Add ~/.bun/bin to PATH'

# Verify symlink
ls -la /data/.openclaw/bin/qmd
```

### Indexing fails
```bash
# Force re-index
/data/.openclaw/bin/qmd update --collection memory

# Check disk space
df -h ~/.cache/qmd
```

### Cron jobs not running
```bash
# Check cron service
systemctl status cron

# Test script manually
/data/.openclaw/workspace/scripts/memory-janitor.sh
```

## Directory Structure After Install

```
/data/.openclaw/workspace/
├── memory/
│   ├── CORE_SYSTEM.md          # Current task/goals
│   ├── PROJECTS.md            # Task queue
│   ├── RETENTION_POLICY.md    # Memory rules
│   ├── stationary/            # P0: Core identity
│   ├── short-term/            # P1: Daily logs
│   ├── instant/               # P2: Session notes
│   ├── experiments/           # Testing logs
│   └── archive/              # Compressed summaries
├── scripts/
│   ├── memory-janitor.sh     # Nightly cleanup
│   ├── compact-fluff.sh       # Lightweight cleanup
│   └── session-flush.sh       # Session end flush
└── HEARTBEAT.md              # Task instructions
```

## Next Steps

1. Read [MEMORY_FRAMEWORK.md](./MEMORY_FRAMEWORK.md) for usage
2. Configure your first task in `memory/PROJECTS.md`
3. Review [HEARTBEAT.md](./HEARTBEAT.md) for rules

## Uninstall

```bash
# Remove cron jobs
crontab -l | grep -v memory-janitor | crontab -

# Remove QMD collection
/data/.openclaw/bin/qmd collection rm memory

# Delete framework files
rm -rf /data/.openclaw/workspace/memory
rm -rf /data/.openclaw/workspace/scripts
rm /data/.openclaw/workspace/HEARTBEAT.md
```

## Support

- GitHub Issues: https://github.com/Frederickhqz/agent-framework/issues
- Documentation: See [README.md](./README.md) and [MEMORY_FRAMEWORK.md](./MEMORY_FRAMEWORK.md)
