# Collective Observatory

**Real-time agent activity visualization for the AI-CIV Collective**

## What Is This?

The Collective Observatory provides transparency into multi-agent deployments, showing:
- Which agents are currently active
- What each agent is investigating
- Progress and status in real-time
- Historical deployment patterns

## Status: MVP Complete ✅

**Phase 1: Terminal Dashboard** (COMPLETE)
- State tracking system ✅
- Dashboard UI with live updates ✅
- Progress bars and status icons ✅
- Deployment history view ✅
- Timestamp formatting ✅

**Phase 2: Planned**
- Interactive navigation (up/down, Enter to expand)
- Detailed agent logs view
- Search/filter deployment history
- Export findings to markdown

**Phase 3: Planned**
- Agent relationship visualization
- Performance analytics
- Pattern recommendations
- Web dashboard (optional)

## How It Works

### State Management

**File**: `.claude/observatory/dashboard-state.json`

Tracks:
- Current active deployments
- Agent status and progress
- Historical deployment records
- Collective statistics

### Data Structure

```json
{
  "currentDeployment": {
    "id": "dep_20251001_142345",
    "task": "Task description",
    "startTime": "ISO timestamp",
    "agents": [
      {
        "name": "agent-name",
        "status": "working|completed|failed",
        "progress": 0-100,
        "currentActivity": "What agent is doing",
        "findings": ["Finding 1", "Finding 2"],
        "startTime": "ISO timestamp"
      }
    ]
  },
  "history": [
    {
      "id": "dep_id",
      "task": "Task",
      "agents": ["agent1", "agent2"],
      "status": "completed",
      "completedAt": "ISO timestamp"
    }
  ]
}
```

## Usage

### Launch Observatory
```bash
# Quick launcher (recommended)
./observatory

# Or directly with Python
.venv/bin/python .claude/observatory/dashboard.py

# Test with mock deployment
.venv/bin/python .claude/observatory/test_dashboard.py
```

### Controls
- **Ctrl+C** - Exit observatory
- Dashboard auto-updates every 1 second

### Future Navigation (Phase 2)
- `↑↓` - Navigate between agents (planned)
- `Enter` - View agent details (planned)
- `Tab` - Switch views (planned)
- `/` - Search history (planned)

## Implementation Status

✅ **Complete** (Phase 1 MVP):
- State file structure and data schema
- Complete state management API
- Terminal UI rendering with rich library
- Real-time updates (1-second polling)
- Agent status tracking with progress bars
- Deployment history view
- Status icons and color coding
- Timestamp formatting
- Documentation

📋 **Planned** (Phase 2+):
- Interactive navigation (up/down, Enter)
- Agent detail view with logs
- Search and filter functionality
- Export capabilities (markdown)
- Analytics and pattern detection

## Integration

### The Conductor Updates State

When deploying agents:
```javascript
// Pseudo-code
startDeployment(task, agents)
updateAgentStatus(agentName, status, progress, activity)
logAgentActivity(agentName, message)
completeAgent(agentName, findings)
completeDeployment(deploymentId, synthesis)
```

### Dashboard Reads State

When opened:
```javascript
// Pseudo-code
readDashboardState()
displayActiveAgents()
pollForUpdates() // every 1 second
```

## Future Enhancements

### Phase 2 Features
- Search deployment history
- Filter by agent/task/date
- Export findings to markdown
- Deployment comparison

### Phase 3 Features
- Agent relationship graphs (ASCII)
- Performance analytics
- Pattern detection (which agent combos work best)
- Predictive agent recommendations

## Technical Notes

### File Locations
- State: `.claude/observatory/dashboard-state.json` (gitignored)
- History: `.claude/memory/deployments/` (committed)
- Config: `.claude/observatory/config.json` (gitignored)

### Update Frequency
- Real-time: Poll state file every 1 second when dashboard open
- Async: Use file watcher (inotify) for instant updates when available
- Graceful: Fall back to polling if watcher unavailable

### Performance
- Lazy load history (20 entries at a time)
- Cache parsed JSON in memory
- Stream large logs (>10MB) to temp files

## Contributing

When implementing dashboard UI:
1. Follow terminal-first design from feature-designer spec
2. Use ANSI escape codes for colors/layout
3. Implement double-buffering to prevent flicker
4. Support terminal resize gracefully
5. Keep state updates atomic (file locking)

## Resources

- Feature Design: `/docs/examples/` (when created)
- API Spec: From api-architect agent analysis
- Naming Guide: From naming-consultant recommendations

---

**The Observatory brings transparency to the collective's mind.** 🎭✨
