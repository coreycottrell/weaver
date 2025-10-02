# AI-CIV Component Interface Reference

Quick reference guide for internal APIs

---

## Observatory State Management

**File**: `.claude/observatory/observatory.py`

### State Lifecycle
```python
# Initialize
dep_id = start_deployment(task: str, agents: List[str]) -> str

# Update
update_agent_status(agent: str, status: str, progress: int, activity: str)
log_agent_activity(agent: str, message: str)

# Complete
complete_agent(agent: str, findings: List[str])
complete_deployment(dep_id: str, synthesis: str)
```

### Queries
```python
get_active_deployment() -> Optional[Dict]
get_deployment_history(limit: int = 20) -> List[Dict]
get_stats() -> Dict[str, int]
```

### Side Effects
- ✍️ Writes to `dashboard-state.json` on all mutations
- 📖 Reads from `dashboard-state.json` on all queries
- ⚠️ Raises `ValueError` on invalid operations

---

## Mission Orchestrator

**File**: `tools/conductor_tools.py`

### Basic Usage
```python
# Create mission
mission = Mission("Task description",
                 email_updates=True,
                 github_backup=True)

# Add agents
mission.add_agent("code-archaeologist")
mission.add_agent("api-architect")

# Start
mission.start()  # Returns deployment_id

# Update agents
mission.update_agent("code-archaeologist", "working", 50, "Analyzing...")
mission.log_activity("code-archaeologist", "Found 20 files")
mission.complete_agent("code-archaeologist", ["Finding 1", "Finding 2"])

# Complete mission
mission.complete("Synthesis of findings")
```

### Quick Mission
```python
quick_mission(
    task="Analyze API",
    agents=["api-architect"],
    synthesis="Found 5 endpoints",
    findings_per_agent={
        "api-architect": ["REST API", "Good docs"]
    }
)
```

### Side Effects
- 📊 Updates Observatory state
- 📧 Sends emails (if enabled)
- 📦 Commits to GitHub (if enabled)
- 🖨️ Prints to console

---

## Email Reporter

**File**: `tools/email_reporter.py`

### Public Functions
```python
# Send custom email
send_email(subject: str, body_html: str,
           attachments: List[str] = None) -> bool

# Send deployment report
send_deployment_report(deployment: Dict) -> bool

# Send agent update
send_agent_update(agent_name: str, status: str,
                 activity: str, findings: List[str] = None) -> bool

# Send weekly summary
send_collective_summary() -> bool
```

### Configuration
```bash
# .env file
GMAIL_USERNAME=your-email@gmail.com
GOOGLE_APP_PASSWORD=your-app-password
```

### Side Effects
- 🌐 Connects to smtp.gmail.com
- 📧 Sends email to `coreycmusic@gmail.com`
- 📎 Reads attachment files
- 📖 Reads Observatory state

---

## GitHub Backup

**File**: `tools/github_backup.py`

### Setup (One-time)
```python
setup_github_backup()  # Creates repo, initializes git, first push
```

### Auto Backup
```python
# After mission completion
auto_backup(message="Mission complete: Task name")

# Custom backup
auto_backup(message="Custom commit message")
```

### Manual Operations
```python
# Create GitHub repository
create_github_repo() -> Optional[str]

# Initialize local git
init_git_repo() -> git.Repo

# Commit and push changes
commit_and_push(repo: git.Repo, message: str) -> bool
```

### Configuration
```bash
# .env file
PAT=github_personal_access_token
GITHUB_USERNAME=your-github-username
```

### Side Effects
- 🌐 Makes GitHub API calls
- 📦 Creates commits and pushes
- ✍️ Writes .gitignore file
- ⚠️ **Force pushes to main** (be careful!)

---

## Web Dashboard

**File**: `web/app.py`

### Routes
```python
# Main dashboard
GET /

# API endpoint
GET /api/state -> JSON
```

### WebSocket Events
```javascript
// Connect
socket.on('connect', () => {
  // Receives state_update immediately
})

// State updates
socket.on('state_update', (state) => {
  // Real-time state changes
})
```

### Side Effects
- 📖 Reads Observatory state every second
- 📡 Broadcasts via WebSocket
- 🌐 Serves HTTP on port 5000

---

## Data Structures

### Deployment
```python
{
    "id": "dep_20251001_143022",
    "task": "Mission description",
    "startTime": "2025-10-01T14:30:22.123456",
    "status": "active" | "completed",
    "agents": [Agent],
    "completedAt": "2025-10-01T15:00:00.123456" | None,
    "synthesis": "Final synthesis" | None
}
```

### Agent
```python
{
    "name": "code-archaeologist",
    "status": "pending" | "working" | "completed" | "failed",
    "progress": 0-100,
    "currentActivity": "Analyzing codebase...",
    "findings": ["Finding 1", "Finding 2"],
    "logs": [
        {"time": "2025-10-01T14:30:00", "message": "Started analysis"}
    ],
    "startTime": "2025-10-01T14:30:00",
    "completedAt": "2025-10-01T15:00:00" | None
}
```

### State
```python
{
    "version": "1.0.0",
    "currentDeployment": Deployment | None,
    "history": [Deployment],  # Most recent first
    "stats": {
        "totalDeployments": 42,
        "totalAgentsDeployed": 120,
        "totalFindings": 350
    },
    "lastUpdated": "2025-10-01T15:00:00"
}
```

---

## Common Patterns

### Error Handling
```python
try:
    update_agent_status("agent-name", "working", 50, "Analyzing")
except ValueError as e:
    # No active deployment or agent not found
    print(f"Error: {e}")
```

### Conditional Features
```python
# Disable email/backup for testing
mission = Mission("Test task",
                 email_updates=False,
                 github_backup=False)
```

### State Queries
```python
# Check if deployment active
active = get_active_deployment()
if active:
    print(f"Currently running: {active['task']}")

# Get recent missions
history = get_deployment_history(limit=10)
for dep in history:
    print(f"{dep['task']} - {dep['completedAt']}")

# Get statistics
stats = get_stats()
print(f"Total deployments: {stats['totalDeployments']}")
```

---

## Best Practices

### 1. Always Check Active Deployment
```python
active = get_active_deployment()
if active:
    print("Mission in progress, wait for completion")
else:
    # Safe to start new mission
    mission.start()
```

### 2. Handle Email Failures Gracefully
```python
if send_deployment_report(deployment):
    print("Report sent successfully")
else:
    print("Email failed - check logs")
    # Mission still completes
```

### 3. Use Quick Mission for Simple Workflows
```python
# Don't need fine-grained control?
quick_mission(
    task="Simple analysis",
    agents=["agent1"],
    synthesis="Results here"
)
```

### 4. Test Without Side Effects
```python
# Disable external dependencies during testing
mission = Mission("Test",
                 email_updates=False,
                 github_backup=False)
```

---

## Dependency Graph

```
conductor_tools.py (Mission)
    │
    ├─► observatory.py (State)
    │     └─► dashboard-state.json
    │
    ├─► email_reporter.py
    │     ├─► observatory.py
    │     └─► SMTP Server
    │
    └─► github_backup.py
          ├─► observatory.py
          └─► GitHub API

app.py (Web Dashboard)
    └─► observatory.py (Read-only)
```

---

## File Paths

| Component | Path |
|-----------|------|
| Observatory | `.claude/observatory/observatory.py` |
| State File | `.claude/observatory/dashboard-state.json` |
| Mission Tools | `tools/conductor_tools.py` |
| Email Reporter | `tools/email_reporter.py` |
| GitHub Backup | `tools/github_backup.py` |
| Web Dashboard | `web/app.py` |
| Memory | `.claude/memory/` |

---

## Quick Start Example

```python
#!/usr/bin/env python3
from tools.conductor_tools import Mission

# Create mission
mission = Mission("Analyze codebase architecture")
mission.add_agent("code-archaeologist")
mission.add_agent("pattern-detector")

# Start mission
mission.start()

# Simulate work
mission.update_agent("code-archaeologist", "working", 50, "Mapping dependencies")
mission.complete_agent("code-archaeologist", [
    "4-layer architecture detected",
    "Strong separation of concerns"
])

mission.update_agent("pattern-detector", "working", 75, "Analyzing patterns")
mission.complete_agent("pattern-detector", [
    "Consistent naming conventions",
    "Factory pattern used throughout"
])

# Complete mission
mission.complete("System follows clean architecture principles")

# Auto-sent: email report, GitHub backup, Observatory update
```

---

**For detailed API analysis, see**: `mission-2-api-surface-analysis.md`
