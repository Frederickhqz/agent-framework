# Plane Telegram Mini App

A full-featured Telegram Mini App for Plane project management.

## Overview

This Mini App provides a native Telegram interface for managing Plane projects, issues, cycles, and modules.

## Features

- 📊 **Dashboard** - Overview of projects and recent activity
- 📋 **Kanban Board** - Drag-and-drop issue management
- ✅ **Issues** - List and detail views for tasks
- 🔄 **Cycles** - Sprint planning and tracking
- 📦 **Modules** - Roadmap and feature grouping
- 📱 **Telegram Native** - Theme-aware styling

## Deployment

### Requirements

- Node.js 18+ with Express support
- Plane instance with API access
- API token with workspace permissions

### Hostinger Deployment

1. Create new website → Select **Express** framework
2. Connect GitHub repo: `Frederickhqz/plane-mini-app`
3. Build command: `npm install && npm run build`
4. Start command: `node server.js`

### Environment Variables

```env
PORT=3000
PLANE_API_URL=http://your-plane-instance:port/api/v1
PLANE_API_KEY=plane_api_your_token
PLANE_WORKSPACE=your-workspace-slug
```

## Configuration

### server.js

The Express server provides:
- Static file serving for Vue frontend
- API proxy to Plane instance (handles CORS)
- Telegram WebApp SDK integration

```javascript
// Key endpoints
GET /api/projects          // List all projects
GET /api/issues/:projectId // Get issues for project
POST /api/issues           // Create issue
PATCH /api/issues/:id      // Update issue
```

### API Configuration

Edit `src/composables/api.js`:

```javascript
const PLANE_API = 'http://your-plane-instance:port/api/v1';
const API_KEY = 'plane_api_your_token';
const WORKSPACE = 'your-workspace-slug';
```

## Project Structure

```
plane-mini-app/
├── src/
│   ├── views/
│   │   ├── Dashboard.vue    # Home screen
│   │   ├── Projects.vue     # Project list
│   │   ├── Project.vue      # Project detail
│   │   ├── Kanban.vue       # Kanban board
│   │   ├── Issues.vue       # Issue list
│   │   ├── IssueDetail.vue  # Issue detail
│   │   ├── Cycles.vue       # Sprint management
│   │   └── Modules.vue      # Module/roadmap
│   ├── composables/
│   │   └── api.js           # Plane API client
│   ├── router.js            # Vue Router config
│   ├── App.vue              # Root component
│   └── main.js              # Entry point
├── dist/                    # Built static files
├── server.js                # Express server
└── package.json
```

## Telegram Integration

### BotFather Setup

1. Message [@BotFather](https://t.me/BotFather)
2. Create or select your bot
3. Go to **Bot Settings → Menu Button**
4. Set button text: `Open Plane`
5. Set URL: `https://your-domain.com/`

### WebApp SDK

The app uses Telegram's WebApp SDK for:

- Theme colors (`tg.themeParams`)
- Safe area insets
- Native back button
- Haptic feedback

```javascript
const tg = window.Telegram?.WebApp;
tg.ready();
tg.expand();

// Theme-aware styling
const themeStyles = {
  '--bg-color': tg?.themeParams?.bg_color,
  '--text-color': tg?.themeParams?.text_color,
  // ...
};
```

## API Endpoints Used

| Endpoint | Purpose |
|----------|---------|
| `GET /workspaces/{slug}/projects/` | List projects |
| `GET /workspaces/{slug}/projects/{id}/` | Get project |
| `GET /workspaces/{slug}/projects/{id}/issues/` | List issues |
| `POST /workspaces/{slug}/projects/{id}/issues/` | Create issue |
| `PATCH /workspaces/{slug}/projects/{id}/issues/{id}/` | Update issue |
| `GET /workspaces/{slug}/projects/{id}/states/` | List states |
| `GET /workspaces/{slug}/projects/{id}/cycles/` | List cycles |
| `POST /workspaces/{slug}/projects/{id}/cycles/` | Create cycle |
| `GET /workspaces/{slug}/projects/{id}/modules/` | List modules |
| `POST /workspaces/{slug}/projects/{id}/modules/` | Create module |

## Feature Roadmap

- [ ] Create/edit issues from Mini App
- [ ] Issue comments
- [ ] Assignee management
- [ ] Time tracking
- [ ] Push notifications
- [ ] Offline support
- [ ] Multiple workspace support
- [ ] Custom views/filters
- [ ] Batch operations

## Troubleshooting

### CORS Issues

The Express server proxies API requests to avoid CORS. Ensure `server.js` is running and accessible.

### Authentication Errors

- Verify API key is valid and not expired
- Check workspace slug matches your Plane instance
- Ensure API key has necessary permissions

### Build Errors

```bash
# Clear cache and rebuild
rm -rf node_modules dist
npm install
npm run build
```

## Repository

- **GitHub**: https://github.com/Frederickhqz/plane-mini-app
- **Live Demo**: https://pink-flamingo-276740.hostingersite.com/

## Related Skills

- [Plane Skill](../skills/plane/SKILL.md) - API reference and integration

## Credits

Built with Vue 3, Vite, and Express. Uses Telegram WebApp SDK.