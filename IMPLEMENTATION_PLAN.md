# Agent Framework Enhancement Plan
## Integrating Agency-Agents Patterns with QMD + Plane

### Overview

This plan enhances the existing agent-framework by adopting Agency-Agents patterns while leveraging QMD for semantic memory and Plane for task orchestration.

---

## Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                     OpenClaw Main Session                       │
│  • Agent definitions loaded from agent-definitions/             │
│  • Mode switching based on task context                         │
│  • Heartbeat reads from Plane + triggers subagents              │
└─────────────────────────────────────────────────────────────────┘
                              │
         ┌────────────────────┼────────────────────┐
         ▼                    ▼                    ▼
┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐
│   QMD (Memory)  │  │ Plane (Tasks)   │  │  Subagents      │
│                 │  │                 │  │  (Specialists)  │
│ • Semantic      │  │ • Issues = Tasks│  │                 │
│   search        │  │ • Cycles =      │  │ • architect     │
│ • Context       │  │   Sprints       │  │ • builder       │
│ • MCP server    │  │ • Projects      │  │ • reviewer      │
└─────────────────┘  └─────────────────┘  └─────────────────┘
```

---

## Phase 1: Agent Definitions (Week 1)

### 1.1 Create Agent Definition Structure

```
agent-framework/
├── agent-definitions/
│   ├── _schema.md           # Definition format
│   ├── default.md           # General assistant
│   ├── architect.md         # Planning & design
│   ├── builder.md           # Implementation
│   ├── reviewer.md          # QA & validation
│   └── orchestrator.md      # Multi-agent coordination
```

### 1.2 Agent Definition Schema

```markdown
---
name: architect
description: Planning and design specialist
color: blue
triggers:
  - "plan"
  - "design"
  - "architecture"
  - "how should we"
tools:
  - qmd_query
  - plane_create_issue
  - plane_create_cycle
---

# Architect Agent

## 🧠 Identity
- **Role**: Planning, architecture, and design decisions
- **Personality**: Systematic, thorough, documentation-focused
- **Mode Switch Triggers**: User asks to plan, design, or architect

## 🎯 Core Mission
- Break down complex problems into actionable tasks
- Create technical architecture documents
- Define success criteria and quality gates

## 📋 Deliverables
- Architecture Decision Records (ADRs)
- Task breakdowns for Plane
- Success criteria definitions

## 🔄 Workflow
1. Query QMD for relevant context
2. Analyze requirements
3. Create Plane issues with acceptance criteria
4. Define quality gates

## 🎯 Success Metrics
- All tasks have clear acceptance criteria
- Architecture reviewed before implementation
- <5% scope creep during implementation
```

### 1.3 QMD Integration for Agent Context

```bash
# Add agent definitions to QMD collection
qmd collection add /data/.openclaw/workspace/agent-framework/agent-definitions \
  --name agent-definitions \
  --mask "**/*.md"

# Create context for agent lookup
qmd context add qmd://agent-definitions "Agent personality definitions"

# Embed for semantic search
qmd embed --collection agent-definitions
```

---

## Phase 2: Plane Orchestration (Week 2)

### 2.1 Enhanced HEARTBEAT.md

```markdown
# HEARTBEAT.md - Proactive Memory & Task Management

## Primary: Plane Task Management

### On Wake - Check Plane
1. Fetch issues from Plane API
   - Priority: Urgent > High > Medium > Low
   - Filter: State = "unstarted" or "started"
2. Check for:
   - Unassigned agent tasks → Assign or spawn
   - Tasks assigned to current agent → Continue work
   - Blocked tasks → Notify user
   - Active cycle progress → Report status

### Task Assignment Protocol
```javascript
// Plane API Check
GET /workspaces/agents/projects/{project}/issues/
Filters: state=unstarted, labels=agent-task
```

### Orchestration Logic
- New urgent task → Spawn subagent immediately
- Queued tasks → Prioritize by deadline/priority
- Blocked tasks → Escalate to user via Telegram

## Secondary: Sub-Agent Monitoring

### Check Active Sub-Agents
1. List running subagent sessions
2. Check status of each
3. Report progress to Plane (comments)
4. Kill stalled agents if needed

### Sub-Agent States
- running → Active work
- completed → Task done → Update Plane issue
- failed → Error occurred → Retry or escalate
- stalled → No progress > 10 min → Kill and restart

## Tertiary: Memory Management (QMD)

### Pattern Recognition
1. Query QMD for similar past tasks
2. Check success patterns
3. Apply learnings to current task

## Response Rules
- New task in Plane: Assign or spawn agent
- Task in progress: Continue + update Plane
- Task completed: Update Plane → clear current
- Subagent running: Monitor + report
- Otherwise: HEARTBEAT_OK
```

### 2.2 Plane Issue Template with Quality Gates

```markdown
# Plane Issue Format

## Description
[Task description]

## Acceptance Criteria
- [ ] Criterion 1
- [ ] Criterion 2
- [ ] Criterion 3

## Quality Gates
| Gate | Criteria | Status |
|------|----------|--------|
| Design | Architecture reviewed | ⏳ |
| Build | Implementation complete | ⏳ |
| Review | QA passed with evidence | ⏳ |
| Deploy | Merged to main | ⏳ |

## Retry Policy
- Max retries: 3
- Current attempt: 0
- Last failure reason: -

## Agent Assignment
- Mode: architect | builder | reviewer
- Spawned: [subagent-session-id]

## Evidence
- Screenshots: [links]
- Test results: [links]
- Deployment: [links]
```

### 2.3 Plane API Integration Scripts

```bash
# scripts/plane-orchestrator.sh

PLANE_API="http://168.231.69.92:54617/api/v1"
WORKSPACE="agents"
API_KEY="plane_api_xxx"

# Get unassigned agent tasks
get_unassigned_tasks() {
  curl -s "$PLANE_API/workspaces/$WORKSPACE/issues/?state=unstarted&labels=agent-task" \
    -H "x-api-key: $API_KEY" | jq '.results[]'
}

# Assign task to agent
assign_task() {
  local issue_id=$1
  local agent_mode=$2
  
  curl -X PATCH "$PLANE_API/workspaces/$WORKSPACE/issues/$issue_id" \
    -H "x-api-key: $API_KEY" \
    -H "Content-Type: application/json" \
    -d "{\"assignees\": [\"agent-$agent_mode\"]}"
}

# Update task status
update_task_status() {
  local issue_id=$1
  local state=$2  # started, completed, blocked
  
  curl -X PATCH "$PLANE_API/workspaces/$WORKSPACE/issues/$issue_id" \
    -H "x-api-key: $API_KEY" \
    -H "Content-Type: application/json" \
    -d "{\"state\": \"$state\"}"
}

# Add quality gate evidence
add_gate_evidence() {
  local issue_id=$1
  local gate=$2
  local evidence=$3
  
  curl -X POST "$PLANE_API/workspaces/$WORKSPACE/issues/$issue_id/comments" \
    -H "x-api-key: $API_KEY" \
    -H "Content-Type: application/json" \
    -d "{\"body_html\": \"<h3>$gate Gate</h3><p>$evidence</p>\"}"
}
```

---

## Phase 3: Workflow Orchestration (Week 3)

### 3.1 Orchestrator Agent Definition

```markdown
---
name: orchestrator
description: Multi-agent workflow coordinator
color: cyan
---

# Orchestrator Agent

## 🧠 Identity
- **Role**: Coordinate multiple agents through workflow phases
- **Personality**: Systematic, quality-focused, persistent
- **Triggers**: Complex multi-step projects

## 🔄 Workflow Phases

### Phase 1: Planning (Architect Mode)
1. Spawn architect subagent
2. Create Plane issues with acceptance criteria
3. Define quality gates
4. Wait for planning completion

### Phase 2: Development (Builder Mode)
1. For each Plane issue:
   - Spawn builder subagent
   - Implement with QMD context
   - Update issue progress
2. Quality gate: All tasks implemented

### Phase 3: Review (Reviewer Mode)
1. Spawn reviewer subagent
2. Validate each task with evidence
3. Quality gate: All tasks pass QA
4. Retry loop (max 3) for failures

### Phase 4: Completion
1. Update all Plane issues to "completed"
2. Archive learnings to QMD
3. Generate summary report

## 🚨 Quality Gates

| Phase | Gate | Evidence Required |
|-------|------|-------------------|
| Planning | Architecture reviewed | ADR document |
| Development | Implementation done | Code merged |
| Review | QA passed | Screenshots + tests |
| Deploy | Production ready | Deployment link |

## 🔄 Retry Logic
- Max 3 retries per task
- Each retry includes specific feedback
- After 3 failures: Mark blocked, escalate to user
```

### 3.2 Subagent Spawn Templates

```bash
# templates/spawn-architect.md
Spawn architect subagent with:
- Task: "Create technical architecture for [feature]"
- Output: Plane issues with acceptance criteria
- Context: Query QMD for similar architectures
- Timeout: 1800s

# templates/spawn-builder.md  
Spawn builder subagent with:
- Task: "Implement [task] per Plane issue [id]"
- Acceptance: All criteria met
- Context: QMD query for implementation patterns
- Quality gate: Tests pass, code reviewed

# templates/spawn-reviewer.md
Spawn reviewer subagent with:
- Task: "Validate [feature] with evidence"
- Required: Screenshots, test results
- Output: PASS/FAIL with specific feedback
- Default: Find 3-5 issues minimum
```

---

## Phase 4: QMD Pattern Library (Week 4)

### 4.1 Pattern Collection Structure

```
memory/
├── patterns/
│   ├── development-patterns.md
│   ├── qa-patterns.md
│   ├── estimation-patterns.md
│   └── failure-patterns.md
```

### 4.2 Pattern Recognition Integration

```markdown
# memory/patterns/development-patterns.md

## Pattern: Auth Feature Implementation
- Average time: 2-4 hours
- Typical QA cycles: 2
- Common issues: Session persistence, token refresh
- Success indicators: Early test coverage
- Source: 12 implementations

## Pattern: API Endpoint
- Average time: 30-45 minutes
- Typical QA cycles: 1
- Common issues: Validation edge cases
- Success indicators: OpenAPI spec first
- Source: 47 implementations

## Pattern: Mobile Responsive
- Average time: 1-2 hours
- Typical QA cycles: 2-3
- Common issues: Touch targets, overflow
- Success indicators: Mobile-first design
- Source: 23 implementations
```

### 4.3 QMD Queries for Context

```bash
# Before starting a task, query for patterns
qmd query "authentication implementation patterns" -c memory

# During development, query for solutions
qmd query "session persistence solution" -c memory

# After completion, add learnings
qmd add memory/patterns/new-pattern.md --collection memory
```

---

## Implementation Timeline

| Week | Phase | Deliverables |
|------|-------|--------------|
| 1 | Agent Definitions | `agent-definitions/` folder, QMD integration |
| 2 | Plane Orchestration | Enhanced HEARTBEAT.md, API scripts |
| 3 | Workflow Orchestration | Orchestrator agent, spawn templates |
| 4 | Pattern Library | Pattern files, QMD queries |

---

## File Structure After Implementation

```
agent-framework/
├── agent-definitions/
│   ├── _schema.md
│   ├── default.md
│   ├── architect.md
│   ├── builder.md
│   ├── reviewer.md
│   └── orchestrator.md
├── memory/
│   ├── CORE_SYSTEM.md
│   ├── PROJECTS.md
│   ├── PATTERNS.md
│   ├── patterns/
│   │   ├── development-patterns.md
│   │   ├── qa-patterns.md
│   │   └── estimation-patterns.md
│   └── RETENTION_POLICY.md
├── scripts/
│   ├── plane-orchestrator.sh
│   ├── memory-janitor.sh
│   ├── compact-fluff.sh
│   └── session-flush.sh
├── templates/
│   ├── spawn-architect.md
│   ├── spawn-builder.md
│   ├── spawn-reviewer.md
│   ├── quality-gate-checklist.md
│   └── evidence-report.md
├── HEARTBEAT.md
├── MEMORY_FRAMEWORK.md
└── README.md
```

---

## Success Metrics

| Metric | Before | After |
|--------|--------|-------|
| Task completion rate | ~60% | Target: 90% |
| Average QA cycles | Unknown | Track: 1-2 average |
| Pattern reuse | None | Track: 5+ queries/week |
| Subagent coordination | Manual | Automated via Plane |
| Quality gate compliance | None | 100% enforcement |

---

## Next Steps

1. **Immediate**: Create `agent-definitions/` folder with schema
2. **Week 1**: Implement default, architect, builder, reviewer definitions
3. **Week 2**: Integrate Plane API into HEARTBEAT.md
4. **Week 3**: Test orchestrator with real project
5. **Week 4**: Build pattern library from learnings