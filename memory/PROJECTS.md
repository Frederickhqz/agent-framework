# Active Projects & Tasks
# Auto-managed by AI - Tasks inferred from conversation

## Projects

### Project: QMD Memory Setup
- **Status**: completed
- **Started**: 2026-02-22
- **Ended**: 2026-02-22
- **Summary**: Installed QMD, set up MCP server, configured memory tiers
- **Learnings**: 
  - Use Bun instead of npm (native dependencies)
  - QMD = BM25 + vectors + reranking
  - MCP server: localhost:8181

---

## Task Queue

### Current Task
- None (inferred from conversation when needed)

### Task Inference Rules
When I commit to something in conversation → auto-create:
- "I'll look into X" → task created
- "Let me check Y" → task created  
- User asks for help → task created
- Problem identified → task created

### Status Flow
```
IN_PROGRESS → WAITING_ON → COMPLETED → (infer next)
                    ↓
              BLOCKED → (flag human)
```

---

## Heartbeat Action Log
| Time | Action | Result |
|------|--------|--------|
| 2026-02-22 22:30 | Initial setup | QMD working |
| 2026-02-22 23:40 | Framework review | Proactive model adopted |

## Fluff Management
- **Lightweight**: compact-fluff.sh runs during normal ops
- **Nightly**: memory-janitor.sh at 2-3 AM (only if no tasks pending)
