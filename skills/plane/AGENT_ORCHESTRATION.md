# Multi-Agent Orchestration

Workflow for coordinating multiple agents through Plane project management.

---

## Overview

Instead of running multiple agent instances, we use a single main session that spawns sub-agents for specific tasks. All coordination is tracked in Plane for visibility.

---

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    Main Session                             │
│  - Heartbeat every 10 minutes                              │
│  - Monitors Plane for tasks                                │
│  - Spawns sub-agents for work                              │
│  - Tracks progress in Plane                                │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                    Plane Instance                           │
│  - Projects: Track all work                                │
│  - Modules: Group related tasks                            │
│  - Cycles: Time-boxed sprints                              │
│  - Issues: Individual tasks                                │
│  - Views: Agent dashboards                                 │
└─────────────────────────────────────────────────────────────┘
                              │
              ┌───────────────┼───────────────┐
              ▼               ▼               ▼
        ┌─────────┐     ┌─────────┐     ┌─────────┐
        │  Claude │     │ Agent 2 │     │ Agent 3 │
        │ (sub)   │     │ (sub)   │     │ (sub)   │
        └─────────┘     └─────────┘     └─────────┘
```

---

## Projects

### 1. Agent Framework
Core infrastructure and skills.

**Modules:**
- Core Infrastructure
- Skills System
- Memory Management
- API Integration

### 2. QR Code Generator
QR code generation tool.

**Modules:**
- Features
- Bug Fixes
- Infrastructure

### 3. Agent CRM
Customer relationship management.

### 4. Agent Orchestration
Multi-agent coordination hub.

**Modules:**
- Claude Agent
- Sub-Agent Pool
- Workflow Automation

---

## Task Assignment Protocol

### Issue Format for Agents

```markdown
## Task Description
[Clear description of the task]

## Agent Instructions
- [ ] Step 1
- [ ] Step 2
- [ ] Step 3

## Acceptance Criteria
- [ ] Criteria 1
- [ ] Criteria 2

## Context
[Links to relevant resources]

## Priority: high/medium/low
## Assignee: @claude / @agent-name
```

### Labels for Agent Tasks

| Label | Meaning |
|-------|---------|
| `agent-task` | Task for any agent |
| `claude` | Specifically for Claude |
| `blocked` | Needs human input |
| `review-needed` | Ready for review |

---

## Heartbeat Workflow (Every 10 Minutes)

### 1. Check Plane for Tasks
```javascript
// Pseudocode
async function heartbeat() {
  const issues = await fetchIssuesForAgent('claude');
  const activeCycles = await fetchActiveCycles();
  
  // Check for unassigned tasks
  const unassigned = issues.filter(i => !i.assignee && i.state === 'unstarted');
  
  // Check for assigned but not started
  const pending = issues.filter(i => i.assignee === 'claude' && i.state === 'unstarted');
  
  // Check for in-progress tasks
  const inProgress = issues.filter(i => i.state === 'started');
  
  // Report status
  return { unassigned, pending, inProgress };
}
```

### 2. Spawn Sub-Agent if Needed
- New urgent task → Spawn immediately
- Multiple tasks queued → Prioritize by deadline/priority
- Long-running task → Spawn as persistent session

### 3. Update Plane with Progress
- Move issues between states
- Add comments with updates
- Update cycle progress

---

## Sub-Agent Types

### Claude (Code Agent)
- Primary coding agent
- Handles complex development tasks
- Can spawn additional sub-agents for research

**Triggers:**
- `claude` label on issue
- Priority: urgent/high
- Task type: development

### Research Agent
- Web research
- Documentation review
- Information gathering

**Triggers:**
- `research` label
- Task type: research

### Coordination Agent
- Monitors all sub-agents
- Updates Plane with status
- Manages handoffs

---

## Cycle Management

### Daily Cycle (Agent Orchestration)
- Quick tasks (< 1 hour)
- Immediate responses
- Bug fixes

### Weekly Cycle (All Projects)
- Feature development
- Larger tasks
- Sprint goals

### Monthly Cycle (Roadmap)
- Module completion
- Major milestones

---

## State Transitions

```
Backlog → Todo → In Progress → Done
           ↓           ↓
        Cancelled   Blocked → Todo
```

### When to Transition

| From | To | Trigger |
|------|-----|---------|
| Backlog | Todo | Agent picks up task |
| Todo | In Progress | Agent starts work |
| In Progress | Done | Agent completes task |
| In Progress | Blocked | Agent needs input |
| Blocked | Todo | Human provides input |

---

## Communication Protocol

### Task Updates in Comments
```markdown
## Update from Claude
**Status:** In Progress
**Progress:** 60%
**Next:** Complete API integration

- ✅ Set up project structure
- ✅ Created API endpoints
- 🔄 Building frontend
- ⏳ Testing
```

### Handoff Protocol
```markdown
## Handoff to @claude
**Task:** Implement user auth
**Context:** [link to context]
**Deadline:** 2024-01-15
**Priority:** High
```

---

## Monitoring Dashboard

### Views to Create

1. **Agent Queue** - All unassigned agent tasks
2. **Claude's Tasks** - Tasks assigned to Claude
3. **Active Work** - All in-progress issues
4. **Blocked** - Issues needing attention
5. **Cycle Progress** - Current sprint status

---

## Implementation Checklist

- [ ] Create Agent Orchestration project in Plane
- [ ] Set up modules for each agent type
- [ ] Create daily/weekly cycles
- [ ] Create agent-specific views
- [ ] Set up webhook for real-time updates
- [ ] Update heartbeat to 10 minutes
- [ ] Test sub-agent spawning
- [ ] Document handoff procedures

---

## API Integration

### Fetch Tasks for Agent
```bash
curl -s "http://168.231.69.92:54617/api/v1/workspaces/agents/projects/{project}/issues/?labels=agent-task" \
  -H "X-API-Key: plane_api_xxx"
```

### Update Issue State
```bash
curl -X PATCH "http://168.231.69.92:54617/api/v1/workspaces/agents/projects/{project}/issues/{issue}/" \
  -H "X-API-Key: plane_api_xxx" \
  -H "Content-Type: application/json" \
  -d '{"state": "state-uuid"}'
```

### Add Comment
```bash
curl -X POST "http://168.231.69.92:54617/api/v1/workspaces/agents/projects/{project}/issues/{issue}/comments/" \
  -H "X-API-Key: plane_api_xxx" \
  -H "Content-Type: application/json" \
  -d '{"comment_html": "<p>Update from agent...</p>"}'
```