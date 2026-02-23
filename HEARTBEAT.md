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
If I commit to doing something in conversation → auto-create task in PROJECTS.md
- "I'll look into X" → task created
- "Let me check Y" → task created
- User asks for help → task created if multi-step

### Task Status Flow
```
IN_PROGRESS → WAITING_ON → COMPLETED → (infer next)
                    ↓
              BLOCKED → (flag for human)
```

## Secondary: Fluff Management (Ongoing)

### During Normal Operation - Auto-Compact
Periodically (every ~30 min during active conversation):
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
- **Task inferred**: Add to PROJECTS.md + continue work
- **Task in progress**: Continue + log progress
- **Task completed**: Flush learnings → clear current
- **Session boundary detected**: Run session-flush.sh
- **Nightly + no tasks**: Run memory-janitor.sh
- **Otherwise**: HEARTBEAT_OK
