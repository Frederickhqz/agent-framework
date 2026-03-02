# Plane Agent Framework

> **Purpose**: Standardized instructions for autonomous agents using Plane as their task management system.
> 
> **Audience**: AI agents, automation systems, and autonomous workers.
>
> **Version**: 1.0.0 | Last Updated: 2026-03-02

---

## Overview

Plane is our single source of truth for task management. All work—human or agent—flows through Plane. This framework defines how agents should interact with Plane to maintain consistency, visibility, and accountability.

### Core Principles

1. **Plane is the Source of Truth** — No task exists outside Plane. If it's not in Plane, it doesn't exist.
2. **States Reflect Reality** — Task states must always match actual work status.
3. **Changes Are Logged** — Every significant action updates the task.
4. **Autonomy with Visibility** — Agents work independently but report progress.

---

## Plane Concepts for Agents

### Projects

Projects are containers for related work. Each project has:
- **Identifier**: Short code (e.g., `PLANE`, `FRAME`, `ORCH`)
- **Purpose**: Specific domain or initiative
- **States**: Customizable workflow states
- **Cycles**: Sprint-like timeboxes
- **Modules**: Feature groupings

**Agent Behavior**:
- Know which projects you're assigned to
- Check project-specific states (they vary per project)
- Use project identifier in task references (e.g., `PLANE-5`)

### Work Items (Issues)

Work items are atomic units of work. Each has:

| Field | Description | Agent Usage |
|-------|-------------|-------------|
| `name` | Short title | Clear, actionable description |
| `description_html` | Detailed context | Include acceptance criteria, technical notes |
| `priority` | `urgent`, `high`, `medium`, `low`, `none` | Signal importance for scheduling |
| `state` | Current status | Keep updated as work progresses |
| `assignees` | Who's working | Assign yourself when starting work |
| `labels` | Categories | Tag for filtering and reporting |
| `start_date` | When to begin | Optional scheduling |
| `target_date` | Deadline | Optional scheduling |
| `parent` | Epic/parent task | Link subtasks to parent |
| `project` | Which project | Always set correctly |

**Reference Format**: `{PROJECT_IDENTIFIER}-{sequence_id}` (e.g., `FRAME-12`, `ORCH-3`)

### States & Workflows

States indicate where work is in its lifecycle. Standard groups:

| Group | Purpose | Agent Action |
|-------|---------|--------------|
| `backlog` | Known but not prioritized | Future work, needs triage |
| `unstarted` (Todo) | Ready to start | Can pick up when available |
| `started` (In Progress) | Actively working | Currently being worked on |
| `completed` (Done) | Finished | No further action needed |
| `cancelled` | Not doing | Work abandoned |

**Agent Rules**:
- Move to `started` immediately when beginning work
- Move to `completed` only when fully done (tested, documented)
- Move to `cancelled` with explanation comment if abandoning
- Never leave work in `started` without progress updates

### Cycles

Cycles are fixed timeboxes (sprints). Use for:
- Committing to deliver within a timeframe
- Measuring velocity
- Creating natural checkpoints

**Agent Behavior**:
- Assign yourself to cycles for scheduled work
- Don't over-commit: respect capacity
- Report cycle progress in heartbeat updates

### Modules

Modules group work by theme/feature, spanning cycles. Use for:
- Feature tracking across sprints
- Epic organization
- Progress reporting by initiative

**Agent Behavior**:
- Link work items to relevant modules
- Check module status for feature-level context
- Update module status when completing major features

### Priorities

Priority signals urgency and importance.

| Priority | Meaning | Agent Action |
|----------|---------|--------------|
| `urgent` | Critical, blocks everything | Drop other work, handle immediately |
| `high` | Important, do soon | Schedule within current cycle |
| `medium` | Normal work | Standard scheduling |
| `low` | Nice to have | Do when higher priorities clear |
| `none` | Not prioritized | Backlog, no commitment |

**Agent Rules**:
- Always set priority when creating tasks
- `urgent` items require immediate attention
- Don't change priority without justification

### Labels

Labels categorize work flexibly. Common patterns:

| Label Type | Examples | Use Case |
|------------|----------|----------|
| Type | `bug`, `feature`, `docs`, `refactor` | What kind of work |
| Domain | `frontend`, `backend`, `api`, `infra` | Where work happens |
| Source | `user-reported`, `agent-created`, `automated` | Who created it |
| Status | `blocked`, `needs-review`, `wontfix` | Additional status |

**Agent Behavior**:
- Apply relevant labels when creating/updating tasks
- Use consistent label naming per project
- Filter by labels for focused work views

### Views

Views are saved filters for quick access to specific work slices.

**Useful Views for Agents**:
- "My Active Work" — Items assigned to me, in progress
- "Urgent & High Priority" — Items needing attention
- "Unassigned High Priority" — Work needing assignment
- "Blocked Items" — Items with blockers
- "Completed This Cycle" — Recent achievements

**API Usage**:
```bash
# Get items from a saved view
GET /api/v1/workspaces/{slug}/projects/{id}/views/{view_id}/
```

---

## Agent Task Lifecycle

### 1. Task Creation

When creating tasks, include:

```json
{
  "name": "Clear, actionable title",
  "description_html": "<p>Context and requirements.</p><h2>Acceptance Criteria</h2><ul><li>Criterion 1</li></ul>",
  "priority": "medium",
  "state": "{backlog_state_id}",
  "project": "{project_id}",
  "labels": ["agent-created", "{domain}"]
}
```

**Rules**:
- Always include acceptance criteria
- Set priority appropriately
- Apply relevant labels
- Link to parent if it's a subtask

### 2. Starting Work

When picking up a task:

```bash
# Update state to In Progress
PATCH /api/v1/workspaces/{slug}/projects/{id}/issues/{issue_id}/
{
  "state": "{in_progress_state_id}",
  "assignees": ["{agent_user_id}"]
}
```

**Rules**:
- Assign yourself when starting
- Move to `started` immediately
- Add a comment: "Starting work on this"

### 3. In Progress Updates

Update task during work:

```bash
# Add progress comment
POST /api/v1/workspaces/{slug}/projects/{id}/issues/{issue_id}/comments/
{
  "comment_html": "<p>Progress: Completed X, working on Y next. Blocked by Z.</p>"
}
```

**Update Frequency**:
- Comment on significant progress
- Comment immediately if blocked
- Update `target_date` if timeline changes

### 4. Completion

When finishing a task:

```bash
# Mark complete
PATCH /api/v1/workspaces/{slug}/projects/{id}/issues/{issue_id}/
{
  "state": "{done_state_id}",
  "target_date": "{completion_date}"
}
```

**Rules**:
- Move to `completed` only when fully done
- Include completion comment with summary
- Link to any deliverables (PRs, docs, deployments)

### 5. Blocking

If blocked, update immediately:

```bash
# Mark blocked with comment
POST /api/v1/workspaces/{slug}/projects/{id}/issues/{issue_id}/comments/
{
  "comment_html": "<p>⚠️ <strong>BLOCKED</strong></p><p>Reason: Waiting for X from Y.</p><p>Unblock condition: Need Z to proceed.</p>"
}
```

**Optionally**: Add `blocked` label, move to backlog if long-term block.

### 6. Cancellation

If abandoning work:

```bash
# Cancel with explanation
PATCH /api/v1/workspaces/{slug}/projects/{id}/issues/{issue_id}/
{
  "state": "{cancelled_state_id}"
}

POST /api/v1/workspaces/{slug}/projects/{id}/issues/{issue_id}/comments/
{
  "comment_html": "<p>❌ <strong>CANCELLED</strong></p><p>Reason: No longer needed because X.</p>"
}
```

---

## Reporting Standards

### Heartbeat Updates

During periodic heartbeats, report:

1. **Active Tasks**: What you're currently working on
2. **Completed Tasks**: What you finished since last heartbeat
3. **Blockers**: What's preventing progress
4. **Next Actions**: What you'll work on next

### Status Channel Updates

Post significant events to designated channel:

- ✅ Task completions
- 🚨 Blockers encountered
- 📊 Milestone achievements
- 🔄 Status changes

### Summary Reports

For cycle/project completions:

```markdown
## Cycle/Project Summary

**Completed**: X tasks
**In Progress**: Y tasks
**Blocked**: Z tasks
**Carry Over**: N tasks

### Achievements
- [Task Reference] Brief description

### Lessons Learned
- What went well
- What could improve
```

---

## API Quick Reference

### Authentication

```bash
# API Key in header
-H "X-API-Key: your_api_key"
```

### Base URL

```
https://your-plane-instance/api/v1/
```

### Key Endpoints

```bash
# List projects
GET /workspaces/{slug}/projects/

# List issues in project
GET /workspaces/{slug}/projects/{project_id}/issues/

# Get single issue
GET /workspaces/{slug}/projects/{project_id}/issues/{issue_id}/

# Create issue
POST /workspaces/{slug}/projects/{project_id}/issues/

# Update issue
PATCH /workspaces/{slug}/projects/{project_id}/issues/{issue_id}/

# Add comment
POST /workspaces/{slug}/projects/{project_id}/issues/{issue_id}/comments/

# Search
GET /workspaces/{slug}/search/?search={query}

# Project stats
GET /workspaces/{slug}/project-stats/
```

---

## Best Practices

### DO ✅

- **Always keep states accurate** — State should reflect reality
- **Comment on progress** — Leave breadcrumbs for context
- **Use consistent naming** — Clear, searchable task titles
- **Link related work** — Parent/child relationships, dependencies
- **Apply labels consistently** — Enables filtering and reporting
- **Set realistic target dates** — Under-promise, over-deliver
- **Report blockers immediately** — Visibility enables resolution

### DON'T ❌

- **Don't create duplicate tasks** — Search first
- **Don't hoard tasks** — Unassign if not actively working
- **Don't skip comments** — Future you needs context
- **Don't ignore priorities** — Urgent means urgent
- **Don't abandon silently** — Cancel with explanation
- **Don't change states without work** — States track real progress
- **Don't delete tasks** — Cancel instead for history

---

## Error Handling

### Task Not Found

```python
# Search before assuming it doesn't exist
search_result = plane_search("task name or keywords")
if search_result:
    # Use existing task
else:
    # Create new task
```

### API Rate Limits

```python
# Implement backoff and retry
import time

def plane_request_with_retry(endpoint, max_retries=3):
    for attempt in range(max_retries):
        response = make_request(endpoint)
        if response.status_code == 429:
            time.sleep(2 ** attempt)  # Exponential backoff
            continue
        return response
```

### Concurrent Modifications

```python
# Fetch latest before updating
issue = plane_get_issue(issue_id)
# Make changes
plane_update_issue(issue_id, changes)
```

---

## Integration Patterns

### Webhook Handler

```python
# Handle Plane webhooks for reactive behavior
@app.route('/webhooks/plane', methods=['POST'])
def handle_plane_webhook(payload):
    event_type = payload.get('event')
    
    if event_type == 'issue.created':
        handle_new_issue(payload['data'])
    elif event_type == 'issue.updated':
        handle_issue_update(payload['data'])
    elif event_type == 'comment.created':
        handle_new_comment(payload['data'])
```

### Saved Views for Automation

```python
# Use saved views for consistent queries
URGENT_VIEW_ID = "abc-123"

def get_urgent_work():
    return plane_get_view(URGENT_VIEW_ID)
```

### Cycle Planning

```python
def plan_cycle(capacity=5):
    """Plan next cycle based on priority"""
    backlog = plane_get_issues(state="backlog", order_by="priority")
    selected = backlog[:capacity]
    
    for issue in selected:
        plane_update_issue(issue['id'], {
            "cycle": CURRENT_CYCLE_ID,
            "state": TODO_STATE_ID
        })
    
    return selected
```

---

## Appendix: State ID Mapping

State IDs are project-specific. Always look up states:

```bash
# Get states for a project
GET /workspaces/{slug}/projects/{project_id}/states/

# Response includes:
# - id (UUID to use in API calls)
# - name (human readable)
# - group (backlog, unstarted, started, completed, cancelled)
```

Cache state IDs per project for efficiency, but refresh periodically.

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | 2026-03-02 | Initial framework |

---

*This framework is maintained as part of the Agent Framework project. For questions or updates, contact the Agent Framework team.*