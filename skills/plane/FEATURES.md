# Plane Feature Reference

Complete guide to Plane's project management features for agent orchestration.

---

## Core Concepts

### Work Items (Issues)
The fundamental unit of work in Plane. Can be assigned to:
- **Projects**: Container for related work
- **Cycles**: Time-boxed sprints
- **Modules**: Feature groupings / roadmap items
- **Epics**: Long-running containers spanning cycles

### State Groups
| Group | Description | Use Case |
|-------|-------------|----------|
| `backlog` | Not yet prioritized | Future work |
| `unstarted` | Ready to start | Todo |
| `started` | In progress | Active work |
| `completed` | Done | Finished |
| `cancelled` | Cancelled | Won't do |

### Priorities
| Priority | Color | Use Case |
|----------|-------|----------|
| `urgent` | Red | Critical blockers |
| `high` | Orange | Important |
| `medium` | Yellow | Normal |
| `low` | Blue | Low priority |
| `none` | Gray | Not set |

---

## Features

### 1. Cycles (Sprints)
Time-boxed iterations for focused work.

**States:**
- `draft` - Planning phase
- `upcoming` - Scheduled but not started
- `active` - Currently running
- `completed` - Finished
- `paused` - Temporarily stopped

**API Endpoints:**
```bash
# List cycles
GET /workspaces/{slug}/projects/{id}/cycles/

# Create cycle
POST /workspaces/{slug}/projects/{id}/cycles/
{
  "name": "Sprint 1",
  "description": "Description",
  "start_date": "2024-01-01",
  "end_date": "2024-01-14",
  "project_id": "project-uuid"
}

# Get cycle issues
GET /workspaces/{slug}/projects/{id}/cycles/{cycle_id}/cycle-issues/

# Add issue to cycle
POST /workspaces/{slug}/projects/{id}/cycles/{cycle_id}/cycle-issues/
{
  "issue": "issue-uuid"
}
```

**Use for Agent Orchestration:**
- Assign agents to specific cycles
- Track agent work in time-boxed periods
- Burn-down charts for progress visibility

### 2. Modules (Roadmap)
Feature groupings for larger initiatives.

**Statuses:**
- `planned` - Not started
- `in_progress` - Active development
- `completed` - Finished
- `paused` - On hold

**API Endpoints:**
```bash
# List modules
GET /workspaces/{slug}/projects/{id}/modules/

# Create module
POST /workspaces/{slug}/projects/{id}/modules/
{
  "name": "Feature Name",
  "description": "Description",
  "status": "planned",
  "start_date": "2024-01-01",
  "target_date": "2024-03-01"
}

# Get module issues
GET /workspaces/{slug}/projects/{id}/modules/{module_id}/module-issues/
```

**Use for Agent Orchestration:**
- Group related tasks for agents
- Track feature-level progress
- Assign modules to specific agents

### 3. Views
Saved filter collections for work items.

**View Types:**
- `list` - Tabular view
- `kanban` - Board view
- `calendar` - Date-based view
- `spreadsheet` - Table view
- `gantt` - Timeline view

**API Endpoints:**
```bash
# List views
GET /workspaces/{slug}/projects/{id}/views/

# Create view
POST /workspaces/{slug}/projects/{id}/views/
{
  "name": "My Issues",
  "query_data": {
    "filters": {
      "assignees": ["user-uuid"]
    }
  }
}
```

### 4. Workflows
Define how work items transition between states.

**Features:**
- Transition rules
- Guardrails (validation)
- Approvers
- Automation triggers

**API Endpoints:**
```bash
# List workflows
GET /workspaces/{slug}/projects/{id}/workflows/

# Create workflow
POST /workspaces/{slug}/projects/{id}/workflows/
```

### 5. Labels
Tag issues for categorization.

**API Endpoints:**
```bash
# List labels
GET /workspaces/{slug}/projects/{id}/labels/

# Create label
POST /workspaces/{slug}/projects/{id}/labels/
{
  "name": "Bug",
  "color": "#FF0000"
}
```

### 6. Intake
External request submission.

**Features:**
- Intake forms
- Email intake
- External submissions

### 7. Pages (Wiki)
Documentation and knowledge management.

**Features:**
- Nested pages
- Templates
- Real-time collaboration

### 8. Analytics & Dashboards
Cross-project visibility and reporting.

**Features:**
- Custom dashboards
- Widget-based views
- CSV exports

---

## Agent Orchestration Model

### Project Structure for Multi-Agent

```
Workspace: agents
├── Project: Agent Framework
│   ├── Module: Core Infrastructure
│   ├── Module: Skills System
│   ├── Module: Memory Management
│   └── Cycles: Weekly sprints
├── Project: QR Code Generator
│   ├── Module: Features
│   ├── Module: Bug Fixes
│   └── Cycles: Bi-weekly
├── Project: Agent CRM
│   └── Modules & Cycles
└── Project: Agent Orchestration
    ├── Module: Claude Agent
    ├── Module: Sub-Agent Pool
    └── Cycles: Daily coordination
```

### Issue Assignment for Agents

```json
{
  "name": "Task description",
  "description": "## Agent Instructions\n\n...",
  "assignees": ["agent-claude"],
  "labels": ["agent-task", "priority"],
  "state": "started",
  "priority": "high"
}
```

### Cycle-based Agent Coordination

1. **Daily Cycle**: Quick tasks, immediate responses
2. **Weekly Cycle**: Sprint planning, larger tasks
3. **Monthly Cycle**: Roadmap items, modules

---

## Webhook Integration

### Events
- `issue.created`
- `issue.updated`
- `issue.deleted`
- `cycle.created`
- `cycle.completed`
- `module.updated`

### Webhook Payload
```json
{
  "event": "issue.updated",
  "data": {
    "id": "issue-uuid",
    "name": "Issue name",
    "state": "started"
  }
}
```

---

## Rate Limits

- **60 requests/minute** per API key
- Headers: `X-RateLimit-Remaining`, `X-RateLimit-Reset`

---

## Best Practices for Agent Integration

1. **Use modules** to group agent-specific tasks
2. **Use cycles** for time-boxed agent work
3. **Use labels** to identify agent types
4. **Use priorities** for task urgency
5. **Use webhooks** for real-time agent notifications
6. **Use views** for agent-specific dashboards

---

## Instance Configuration

| Setting | Value |
|---------|-------|
| URL | http://168.231.69.92:54617 |
| API Base | http://168.231.69.92:54617/api/v1 |
| Workspace | agents |
| API Key | plane_api_a671d43b3a7248108f522e8c6703aa85 |

---

## Resources

- Docs: https://docs.plane.so/
- API: https://developers.plane.so/api-reference/introduction
- GitHub: https://github.com/makeplane/plane