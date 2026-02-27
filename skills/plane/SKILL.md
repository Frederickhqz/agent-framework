# Plane Skill

Plane is an open-source project management tool. This skill provides API integration and self-hosting guidance for Plane instances.

## SKILL.md

---

# Plane Integration

Interact with Plane project management via REST API.

## Configuration

Set these in your environment or workspace:

```bash
PLANE_API_URL=http://your-plane-instance:port/api/v1
PLANE_API_KEY=plane_api_your_token_here
PLANE_WORKSPACE=your-workspace-slug
```

## Authentication

Plane uses API keys passed in the `X-API-Key` header:

```bash
curl -H "X-API-Key: plane_api_xxx" http://plane:port/api/v1/workspaces/
```

Alternatively, OAuth Bearer tokens:

```bash
curl -H "Authorization: Bearer your-oauth-token" http://plane:port/api/v1/workspaces/
```

## API Endpoints

### Base URL
```
{PLANE_INSTANCE}/api/v1
```

### Workspaces

```bash
# List workspaces
GET /workspaces/

# Get workspace
GET /workspaces/{workspace_slug}/
```

### Projects

```bash
# List projects
GET /workspaces/{workspace_slug}/projects/

# Get project
GET /workspaces/{workspace_slug}/projects/{project_id}/

# Create project
POST /workspaces/{workspace_slug}/projects/
{
  "name": "Project Name",
  "identifier": "PROJ",
  "description": "Project description"
}

# Update project
PATCH /workspaces/{workspace_slug}/projects/{project_id}/
{
  "cycle_view": true,
  "module_view": true,
  "issue_views_view": true
}
```

### Issues (Work Items)

```bash
# List issues
GET /workspaces/{workspace_slug}/projects/{project_id}/issues/

# Get issue
GET /workspaces/{workspace_slug}/projects/{project_id}/issues/{issue_id}/

# Create issue
POST /workspaces/{workspace_slug}/projects/{project_id}/issues/
{
  "name": "Issue title",
  "description": "Issue description",
  "state": "state-uuid",
  "priority": "high"  # urgent, high, medium, low, none
}

# Update issue
PATCH /workspaces/{workspace_slug}/projects/{project_id}/issues/{issue_id}/
{
  "state": "new-state-uuid"
}

# Delete issue
DELETE /workspaces/{workspace_slug}/projects/{project_id}/issues/{issue_id}/
```

### States (Workflow)

```bash
# List states
GET /workspaces/{workspace_slug}/projects/{project_id}/states/

# State groups: backlog, unstarted, started, completed, cancelled
```

### Cycles (Sprints)

```bash
# List cycles
GET /workspaces/{workspace_slug}/projects/{project_id}/cycles/

# Create cycle
POST /workspaces/{workspace_slug}/projects/{project_id}/cycles/
{
  "name": "Sprint 1",
  "description": "Sprint description",
  "project_id": "project-uuid"
}

# Get cycle issues
GET /workspaces/{workspace_slug}/projects/{project_id}/cycles/{cycle_id}/cycle-issues/
```

### Modules (Roadmap)

```bash
# List modules
GET /workspaces/{workspace_slug}/projects/{project_id}/modules/

# Create module
POST /workspaces/{workspace_slug}/projects/{project_id}/modules/
{
  "name": "Feature Module",
  "description": "Module description"
}

# Module statuses: planned, in_progress, completed, paused

# Get module issues
GET /workspaces/{workspace_slug}/projects/{project_id}/modules/{module_id}/module-issues/
```

### Labels

```bash
# List labels
GET /workspaces/{workspace_slug}/projects/{project_id}/labels/
```

### Users

```bash
# Get current user
GET /users/me/
```

## Pagination

Plane uses cursor-based pagination:

```json
{
  "next_cursor": "100:1:0",
  "prev_cursor": "100:-1:1",
  "next_page_results": true,
  "prev_page_results": false,
  "count": 100,
  "total_pages": 10,
  "total_results": 1000,
  "results": [...]
}
```

Query parameters:
- `per_page`: Items per page (max 100, default 100)
- `cursor`: Cursor string for navigation

## Rate Limiting

- **Limit**: 60 requests per minute per API key
- **Headers**: `X-RateLimit-Remaining`, `X-RateLimit-Reset`

## Priority Values

| Priority | Value |
|----------|-------|
| Urgent | `urgent` |
| High | `high` |
| Medium | `medium` |
| Low | `low` |
| None | `none` |

## State Groups

| Group | Description |
|-------|-------------|
| `backlog` | Not yet prioritized |
| `unstarted` | Todo, ready to start |
| `started` | In progress |
| `completed` | Done |
| `cancelled` | Cancelled |

## Example: Create and Update Issue

```javascript
const API_URL = 'http://plane:port/api/v1';
const API_KEY = 'plane_api_xxx';
const WORKSPACE = 'my-workspace';

async function createIssue(projectId, name, stateId) {
  const res = await fetch(`${API_URL}/workspaces/${WORKSPACE}/projects/${projectId}/issues/`, {
    method: 'POST',
    headers: {
      'X-API-Key': API_KEY,
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({ name, state: stateId })
  });
  return res.json();
}

async function moveIssue(projectId, issueId, newStateId) {
  const res = await fetch(`${API_URL}/workspaces/${WORKSPACE}/projects/${projectId}/issues/${issueId}/`, {
    method: 'PATCH',
    headers: {
      'X-API-Key': API_KEY,
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({ state: newStateId })
  });
  return res.json();
}
```

## Self-Hosting

### System Requirements

- **CPU**: 2 cores minimum
- **RAM**: 4GB (8GB recommended for production)
- **OS**: Linux (Ubuntu 20.04+), macOS, Windows with WSL2

### Docker Deployment

```bash
git clone https://github.com/makeplane/plane.git
cd plane
docker-compose up -d
```

### Environment Variables

Key configuration in `docker-compose.yml`:

```yaml
environment:
  - WEB_URL=http://your-domain:port
  - CORS_ALLOWED_ORIGINS=http://your-domain:port
  - POSTGRES_USER=plane
  - POSTGRES_PASSWORD=your-password
  - REDIS_URL=redis://redis:6379/
```

### Database & Storage

Plane uses:
- **PostgreSQL**: Primary database
- **Redis**: Caching and queues
- **MinIO** (optional): File storage

## Webhook Integration

Plane supports webhooks for real-time updates:

1. Go to Project Settings → Webhooks
2. Add webhook URL
3. Select events to trigger on

## OAuth Apps

For building Plane apps with user authorization:

1. Register app in Plane Settings → OAuth Apps
2. Use OAuth flow for user consent
3. Access API with Bearer token

### OAuth Scopes

Common scopes:
- `read:project`
- `write:project`
- `read:issue`
- `write:issue`
- `read:workspace`
- `write:workspace`

## Resources

- Official Docs: https://developers.plane.so/
- API Reference: https://developers.plane.so/api-reference/introduction
- Self-Hosting: https://developers.plane.so/self-hosting/overview
- GitHub: https://github.com/makeplane/plane