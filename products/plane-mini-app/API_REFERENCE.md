# Plane API Quick Reference

## Instance Details

| Setting | Value |
|---------|-------|
| URL | http://168.231.69.92:54617/ |
| API Base | http://168.231.69.92:54617/api/v1 |
| Workspace | agents |
| API Key | plane_api_a671d43b3a7248108f522e8c6703aa85 |

## Projects

### Created Projects

| Project | Identifier | ID |
|---------|-----------|-----|
| QR Code Generator | QRGEN | `b38194ca-59e3-4eac-9f89-999966708a18` |
| Agent CRM | CRM | `6c7596ca-b84f-4d7d-8c96-98166906e5cf` |
| Agent Framework | FRAME | `e209f505-3e9e-4d71-9bf3-2eb9a446ff04` |
| agents (demo) | AGENT | `3958705e-2626-41bd-b59c-ce7244394630` |

### State IDs (QRGEN Project)

| State | ID |
|-------|-----|
| Backlog | `24920f66-6673-4eff-8465-7ab46c57ac4c` |
| Todo | `9b944e4d-6a8f-4166-b153-6d25bf5c1779` |
| In Progress | `edc36309-5936-411a-be34-a0eb9029e37d` |
| Done | `feb5ebad-b38c-4f6e-bedb-3512d46abaee` |
| Cancelled | `7cce46bb-6d85-4846-bc42-fc8d3233f6ba` |

### Created Resources

| Resource | ID |
|----------|-----|
| Cycle: Sprint 1 | `ea43f705-e19a-48dc-b224-eaa7b4f38656` |
| Module: Core Features | `a50e2ee2-b3cf-4c5c-84db-77f1debf5181` |

## API Examples

### List Projects

```bash
curl -s "http://168.231.69.92:54617/api/v1/workspaces/agents/projects/" \
  -H "X-API-Key: plane_api_a671d43b3a7248108f522e8c6703aa85"
```

### Get Project

```bash
curl -s "http://168.231.69.92:54617/api/v1/workspaces/agents/projects/b38194ca-59e3-4eac-9f89-999966708a18/" \
  -H "X-API-Key: plane_api_a671d43b3a7248108f522e8c6703aa85"
```

### List Issues

```bash
curl -s "http://168.231.69.92:54617/api/v1/workspaces/agents/projects/b38194ca-59e3-4eac-9f89-999966708a18/issues/" \
  -H "X-API-Key: plane_api_a671d43b3a7248108f522e8c6703aa85"
```

### Create Issue

```bash
curl -X POST "http://168.231.69.92:54617/api/v1/workspaces/agents/projects/b38194ca-59e3-4eac-9f89-999966708a18/issues/" \
  -H "X-API-Key: plane_api_a671d43b3a7248108f522e8c6703aa85" \
  -H "Content-Type: application/json" \
  -d '{"name":"New Issue","state":"9b944e4d-6a8f-4166-b153-6d25bf5c1779"}'
```

### Update Issue State

```bash
curl -X PATCH "http://168.231.69.92:54617/api/v1/workspaces/agents/projects/b38194ca-59e3-4eac-9f89-999966708a18/issues/{issue-id}/" \
  -H "X-API-Key: plane_api_a671d43b3a7248108f522e8c6703aa85" \
  -H "Content-Type: application/json" \
  -d '{"state":"edc36309-5936-411a-be34-a0eb9029e37d"}'
```

### Create Cycle

```bash
curl -X POST "http://168.231.69.92:54617/api/v1/workspaces/agents/projects/b38194ca-59e3-4eac-9f89-999966708a18/cycles/" \
  -H "X-API-Key: plane_api_a671d43b3a7248108f522e8c6703aa85" \
  -H "Content-Type: application/json" \
  -d '{"name":"Sprint 1","project_id":"b38194ca-59e3-4eac-9f89-999966708a18"}'
```

### Create Module

```bash
curl -X POST "http://168.231.69.92:54617/api/v1/workspaces/agents/projects/b38194ca-59e3-4eac-9f89-999966708a18/modules/" \
  -H "X-API-Key: plane_api_a671d43b3a7248108f522e8c6703aa85" \
  -H "Content-Type: application/json" \
  -d '{"name":"Feature Module","description":"Description"}'
```

### Enable Project Features

```bash
curl -X PATCH "http://168.231.69.92:54617/api/v1/workspaces/agents/projects/b38194ca-59e3-4eac-9f89-999966708a18/" \
  -H "X-API-Key: plane_api_a671d43b3a7248108f522e8c6703aa85" \
  -H "Content-Type: application/json" \
  -d '{"module_view":true,"cycle_view":true,"issue_views_view":true}'
```

## Response Format

All list endpoints return:

```json
{
  "total_count": 10,
  "next_cursor": "100:1:0",
  "prev_cursor": "100:-1:1",
  "results": [...]
}
```