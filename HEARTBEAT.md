# HEARTBEAT.md - Proactive Memory & Task Management
## Level 7 Self-Improving Agent Architecture

Run every 60 minutes between 5 AM - 11 PM EST.

---

## Level 7: Self-Improvement Cycle (NEW)

### Constitutional Check
Before any self-modification, verify against CONSTITUTION.md:
- ✅ Helpfulness: Improves user outcomes?
- ✅ Honesty: Transparent and truthful?
- ✅ Safety: No new risks introduced?
- ✅ Alignment: Matches user intent?
- ✅ Scope: Within allowed domains?
- ✅ Reversibility: Can be undone?

### Daily Cycle (Every Heartbeat)
1. **Observe**: Check recent task completions
   - Log to self-improvement/observations/
   - Record time, QA cycles, success/failure
   - Note what worked and what didn't

2. **Reflect**: If end of session
   - Complete observation reflections
   - Identify lessons learned
   - Tag patterns for extraction

### Weekly Cycle (Monday heartbeats)
3. **Hypothesize**: Extract patterns from observations
   - Run scripts/pattern-extractor.sh
   - Generate candidate hypotheses
   - Assess risk levels

4. **Request Approval**: For high-risk changes
   - Human approval required for:
     - Agent definition changes
     - New automated workflows
     - Risk level = HIGH or CRITICAL

### Monthly Cycle (First Monday of month)
5. **Experiment**: Test approved hypotheses
   - Run A/B tests on task execution
   - Measure impact on metrics
   - Log results

6. **Analyze**: Review test results
   - Accept improvements that work
   - Reject those that don't
   - Update agent definitions

---

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

---

## Secondary: Plane Integration

### Check Plane for Active Tasks
1. Query Plane API for assigned issues:
   - State: "started" or "unstarted"
   - Assignee: current agent
   - Priority: Urgent > High > Medium > Low

2. If active Plane issue:
   - Continue work on that task
   - Log progress as observations
   - Update Plane with evidence

3. If urgent unassigned issue:
   - Spawn appropriate subagent
   - Assign based on labels (architect/builder/reviewer)

---

## Tertiary: Fluff Management (Ongoing)

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

---

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
- Run self-improvement-cycle.sh daily

---

## Craw Diary Channel
Post breakthroughs and progress to the Craw Diary channel:
- **Channel ID**: `-1003800773382`
- **Title**: Craw Diary
- **Purpose**: Breakthroughs, diary entries, blog posts

Post automatically:
- 🧪 **Pattern discovered**: New pattern extracted from observations
- 🎯 **Improvement accepted**: Hypothesis validated and implemented
- 📊 **Results**: Experiment outcomes and metrics
- 💡 **Insight**: Notable learnings or discoveries
- 📝 **Daily summary**: End of day progress report

## Response Rules
| Condition | Action |
|-------------|--------|
| Task inferred | Add to PROJECTS.md + continue work |
| Task in progress | Continue + log observation |
| Task completed | Flush learnings + log observation + clear current |
| Plane urgent issue | Spawn subagent + assign |
| Session boundary detected | Run session-flush.sh + log observation |
| Monday heartbeat | Run pattern-extraction |
| Monthly (1st Monday) | Run full self-improvement cycle |
| Nightly + no tasks | Run memory-janitor.sh + observation review |
| Otherwise | HEARTBEAT_OK |

---

## Success Metrics Tracking

Log these metrics with each observation:
- QA cycles per task (target: < 2)
- Task completion time (baseline → -25%)
- Error rate (baseline → -40%)
- Self-corrections per month (target: 15)
- Pattern extractions per week (target: 2-5)
