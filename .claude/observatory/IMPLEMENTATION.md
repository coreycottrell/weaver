# Collective Observatory - Implementation Guide

## Phase 1: Terminal Dashboard MVP

### Goal
Create a terminal-based real-time dashboard showing active agent deployments.

### Components

#### 1. State Management (`dashboard-state.json`)
**Status**: ✅ Complete

Tracks current and historical agent deployments with status updates.

#### 2. State Update Functions
**Status**: 📋 To Implement

Required functions:
```python
# Pseudo-code for implementation

def start_deployment(task_description, agent_list):
    """Initialize new deployment in state file"""
    deployment_id = generate_id()
    state = load_state()
    state['currentDeployment'] = {
        'id': deployment_id,
        'task': task_description,
        'startTime': now(),
        'agents': [init_agent(name) for name in agent_list]
    }
    save_state(state)
    return deployment_id

def update_agent_status(agent_name, status, progress, activity):
    """Update agent's current status"""
    state = load_state()
    agent = find_agent(state['currentDeployment']['agents'], agent_name)
    agent['status'] = status
    agent['progress'] = progress
    agent['currentActivity'] = activity
    save_state(state)

def log_agent_activity(agent_name, message):
    """Add log entry for agent"""
    state = load_state()
    agent = find_agent(state['currentDeployment']['agents'], agent_name)
    agent['logs'].append({
        'time': now(),
        'message': message
    })
    save_state(state)

def complete_agent(agent_name, findings):
    """Mark agent as complete with findings"""
    state = load_state()
    agent = find_agent(state['currentDeployment']['agents'], agent_name)
    agent['status'] = 'completed'
    agent['progress'] = 100
    agent['findings'] = findings
    agent['completedAt'] = now()
    save_state(state)

def complete_deployment(deployment_id, synthesis):
    """Finalize deployment and move to history"""
    state = load_state()
    deployment = state['currentDeployment']
    deployment['status'] = 'completed'
    deployment['completedAt'] = now()
    deployment['synthesis'] = synthesis

    # Move to history
    state['history'].insert(0, deployment)
    state['currentDeployment'] = None

    # Update stats
    state['stats']['totalDeployments'] += 1
    state['stats']['totalAgentsDeployed'] += len(deployment['agents'])

    save_state(state)

    # Archive to permanent storage
    archive_deployment(deployment)
```

#### 3. Dashboard Rendering (Terminal UI)
**Status**: 📋 To Implement

**Technology options**:
- Python: Use `rich` library for terminal UI
- Node.js: Use `blessed` or `ink` for React-like terminal UI
- Bash: Use ANSI escape codes directly

**Recommended**: Python with `rich` (easiest, most features)

```python
# Pseudo-code example with rich

from rich.console import Console
from rich.table import Table
from rich.live import Live
from rich.progress import Progress

def render_dashboard(state):
    """Render dashboard UI"""
    console = Console()

    # Header
    console.print("[bold]AI-CIV Collective Observatory[/bold]")
    console.print(f"[dim]Active Deployments: {count_active(state)}[/dim]\n")

    # Current deployment
    if state['currentDeployment']:
        deployment = state['currentDeployment']
        console.print(f"[bold]Task:[/bold] {deployment['task']}")
        console.print(f"[dim]Started: {format_time(deployment['startTime'])}[/dim]\n")

        # Agent table
        table = Table(title="Active Agents")
        table.add_column("Agent", style="cyan")
        table.add_column("Status", style="magenta")
        table.add_column("Progress", style="green")
        table.add_column("Activity", style="yellow")

        for agent in deployment['agents']:
            status_icon = get_status_icon(agent['status'])
            progress_bar = render_progress_bar(agent['progress'])
            table.add_row(
                agent['name'],
                f"{status_icon} {agent['status']}",
                progress_bar,
                agent['currentActivity']
            )

        console.print(table)
    else:
        console.print("[dim]No active deployments[/dim]")

    # Footer
    console.print("\n[dim]Press 'q' to close | Tab for history | ? for help[/dim]")

def get_status_icon(status):
    """Get emoji/symbol for status"""
    return {
        'working': '⟳',
        'completed': '✓',
        'failed': '✗',
        'pending': '○'
    }.get(status, '?')

def render_progress_bar(progress):
    """Render ASCII progress bar"""
    filled = int(progress / 10)
    empty = 10 - filled
    return f"[{'█' * filled}{'░' * empty}] {progress}%"
```

#### 4. Live Updates
**Status**: 📋 To Implement

```python
# Pseudo-code for live dashboard

from rich.live import Live
import time

def live_dashboard():
    """Display dashboard with live updates"""
    with Live(render_dashboard(), refresh_per_second=1) as live:
        while True:
            state = load_state()
            live.update(render_dashboard(state))
            time.sleep(1)  # Update every second

            # Exit condition
            if should_exit():
                break
```

#### 5. Keyboard Input Handling
**Status**: 📋 To Implement

```python
# Pseudo-code for input handling

import keyboard  # or use `curses` for cross-platform

def handle_input():
    """Handle keyboard input"""
    if keyboard.is_pressed('q'):
        exit_dashboard()
    elif keyboard.is_pressed('tab'):
        switch_view('history')
    elif keyboard.is_pressed('enter'):
        expand_selected_agent()
    elif keyboard.is_pressed('up'):
        navigate_up()
    elif keyboard.is_pressed('down'):
        navigate_down()
```

---

## Implementation Steps

### Step 1: Basic State Tracking (1 hour)
- [x] Create `dashboard-state.json` structure
- [x] Write state update functions
- [x] Test state persistence

### Step 2: Simple Terminal Rendering (2 hours)
- [x] Install `rich` library (`pip install rich`)
- [x] Create basic dashboard layout
- [x] Display current deployment (if any)
- [x] Show agent list with status

### Step 3: Live Updates (1 hour)
- [x] Implement file polling (every 1 second)
- [x] Update UI with new state
- [x] Handle "no active deployments" gracefully

### Step 4: Keyboard Navigation (2 hours)
- [x] Add quit (Ctrl+C) functionality
- [ ] Add up/down navigation (Future enhancement)
- [ ] Add view switching (Tab) (Future enhancement)
- [ ] Add help overlay ('?') (Future enhancement)

### Step 5: Enhanced Display (2 hours)
- [x] Add progress bars for each agent
- [x] Add status icons (⟳ ✓ ✗)
- [x] Add color coding by status
- [x] Format timestamps nicely

### Step 6: History View (2 hours)
- [x] Load deployment history from state
- [x] Display in table format
- [x] Add date/time/agent count
- [ ] Support pagination (Future enhancement)

---

## Quick Start

### Prerequisites
```bash
# Virtual environment with rich library already set up
# Located at: .venv/
```

### Run Observatory

**Option 1: Quick launcher** (Recommended)
```bash
./observatory
```

**Option 2: Direct Python**
```bash
.venv/bin/python .claude/observatory/dashboard.py
```

**Option 3: Test with mock data**
```bash
.venv/bin/python .claude/observatory/test_dashboard.py
```

### Usage
- Dashboard updates every 1 second automatically
- Press `Ctrl+C` to exit
- Shows active deployments with real-time progress
- Displays recent deployment history

---

## Testing Plan

### Manual Testing
1. **Start deployment** - Create mock deployment in state file
2. **View dashboard** - Verify agents display correctly
3. **Update agent** - Change status, see if UI updates
4. **Complete agent** - Mark agent done, verify completion shown
5. **View history** - Switch to history view, verify past deployments

### Test Cases
```python
# Test case 1: Empty state
state = {'currentDeployment': None, 'history': []}
assert render_shows_no_deployments(state)

# Test case 2: Active deployment
state = create_mock_deployment(3_agents)
assert render_shows_3_agents(state)

# Test case 3: Agent progress
update_agent_status('agent1', 'working', 50, 'Analyzing...')
assert render_shows_50_percent_progress(state)

# Test case 4: Completion
complete_agent('agent1', ['Finding 1', 'Finding 2'])
assert render_shows_completed_status(state)
```

---

## Integration with The Conductor

### When Deploying Agents

**Current** (manual):
```
User: "Deploy code-archaeologist to analyze X"
Conductor: [Deploys agent manually]
```

**With Observatory** (automated):
```python
# The Conductor automatically updates state
start_deployment(
    task="Analyze authentication system",
    agents=['code-archaeologist', 'security-auditor']
)

# Then deploys agents via Task tool
# ... agent work happens ...

# Update as agents progress (pseudo-code)
update_agent_status('code-archaeologist', 'working', 25, 'Tracing login flow')
update_agent_status('code-archaeologist', 'working', 50, 'Mapping dependencies')
update_agent_status('code-archaeologist', 'working', 75, 'Documenting findings')

# Mark complete
complete_agent('code-archaeologist', [
    'JWT-based authentication identified',
    'Session stored in Redis',
    'Missing token rotation'
])
```

---

## Future Enhancements

### Phase 2: Enhanced Views
- Detailed agent logs (scrollable)
- Search deployment history
- Filter by agent/date/status
- Export findings to markdown

### Phase 3: Analytics
- Agent performance metrics
- Pattern detection (best agent combos)
- Deployment timeline view
- Relationship graphs (ASCII art)

### Phase 4: Advanced Features
- Web dashboard (optional)
- Real-time WebSocket updates
- Collaborative view (multi-user)
- Predictive agent recommendations

---

## File Structure

```
.claude/observatory/
├── README.md                    # This file
├── IMPLEMENTATION.md            # Implementation guide
├── dashboard-state.json         # Current state (gitignored)
├── config.json                  # User preferences (gitignored)
└── dashboard.py                 # Main dashboard script (to create)
```

---

## Notes

**Why Terminal-First?**
- Stays in developer workflow (no context switching)
- Works over SSH
- Zero external dependencies (beyond Python libs)
- Fast and lightweight
- Keyboard-driven (power user friendly)

**Why JSON State File?**
- Simple to read/write
- Human-readable for debugging
- Git-friendly (can commit deployment history)
- No database setup required
- Easy to inspect manually

**Production Ready?**
- State management: ✅ Yes
- Documentation: ✅ Yes
- UI implementation: 📋 MVP needed (~8 hours)
- Full features: ⏳ Phase 2-3

---

**The Observatory makes the invisible visible. The collective's thoughts, now observable.** 🔭✨
