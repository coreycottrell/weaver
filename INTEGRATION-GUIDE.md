# AI-CIV Integration Guide 🎭

## Complete System Overview

The AI-CIV Collective now has **three integrated systems** for maximum transparency and automation:

1. **🌐 Web Dashboard** - Real-time agent visualization
2. **📧 Email Reporter** - Automated mission reports
3. **📦 GitHub Backup** - Automatic repository sync

---

## 1. Web Dashboard 🌐

### Features
- **Real-time updates** via WebSocket
- Beautiful gradient UI with animations
- Live agent progress bars
- Deployment history
- Collective statistics

### Launch Dashboard

```bash
./start-dashboard
```

Then open **http://localhost:5000** in your browser.

### What You'll See

#### Header
- Total deployments, agents deployed, findings generated
- Active agents count

#### Active Deployment Section
- Current mission description
- Agent cards with:
  - Status icons (⟳ working, ✓ completed, ✗ failed, ○ pending)
  - Progress bars (animated)
  - Current activity
  - Findings (when complete)

#### Recent History
- Last 10 completed deployments
- Agent count and completion time
- Click to view details (Phase 2)

### Technical Details
- **Backend**: Flask + Flask-SocketIO
- **Frontend**: Pure HTML/CSS/JS with Socket.IO
- **Updates**: Every 1 second via WebSocket
- **Data source**: `.claude/observatory/dashboard-state.json`

---

## 2. Email Reporter 📧

### Features
- **Mission Complete** - Full HTML reports with all findings
- **Agent Updates** - Real-time notifications for critical agents
- **Weekly Summaries** - Collective intelligence briefings

### Email Address
All reports sent to: **coreycmusic@gmail.com**

### Test Email System

```bash
.venv/bin/python tools/email_reporter.py
```

### Email Templates

#### Mission Complete Report
- Mission description
- Statistics (agents deployed, completed, findings)
- Individual agent reports with findings
- Synthesis summary
- Attached synthesis files

#### Agent Update
- Agent name and status
- Current activity
- Latest findings

#### Weekly Summary
- Total deployments, agents, findings
- Recent mission list
- Link to dashboard

### Usage in Code

```python
from tools.email_reporter import send_deployment_report, send_agent_update

# Send full mission report
send_deployment_report(deployment_dict)

# Send quick agent update
send_agent_update("code-archaeologist", "completed", "Analysis done",
                  ["Finding 1", "Finding 2"])
```

---

## 3. GitHub Auto-Backup 📦

### Features
- Automatic repository creation
- Smart .gitignore (excludes .env, runtime state)
- Auto-commit after missions
- Descriptive commit messages

### Repository
**https://github.com/ai-CIV-2025/ai-civ-collective**

### Setup (One-Time)

```bash
.venv/bin/python tools/github_backup.py setup
```

This will:
1. Create GitHub repository
2. Initialize local git repo
3. Add remote origin
4. Create/update .gitignore
5. Push initial commit

### Manual Backup

```bash
.venv/bin/python tools/github_backup.py
```

### Usage in Code

```python
from tools.github_backup import auto_backup

# Backup with custom message
auto_backup("Mission complete: Authentication analysis")
```

---

## 4. Conductor Tools (All-In-One) 🎭

### The Mission Class

Integrates all three systems into one easy interface:

```python
from tools.conductor_tools import Mission

# Create mission
mission = Mission("Analyze authentication system")
mission.add_agent("code-archaeologist")
mission.add_agent("security-auditor")

# Start (updates Observatory)
mission.start()

# Update agent progress (live on dashboard)
mission.update_agent("code-archaeologist", "working", 50, "Tracing JWT flow")

# Complete agent (sends email if significant findings)
mission.complete_agent("code-archaeologist", [
    "Uses JWT-based authentication",
    "Tokens stored in Redis",
    "Missing token rotation"
])

# Complete mission (sends email + GitHub backup)
mission.complete("Authentication system fully documented")
```

### Quick Mission Helper

For simple missions:

```python
from tools.conductor_tools import quick_mission

quick_mission(
    "Analyze API endpoints",
    ["api-architect", "security-auditor"],
    "Found 5 endpoints, 2 need authentication",
    {
        "api-architect": ["REST API with 5 endpoints", "Good docs"],
        "security-auditor": ["Missing rate limiting", "No input validation"]
    }
)
```

This automatically:
1. ✅ Updates Observatory (visible in dashboard)
2. ✅ Sends email report to coreycmusic@gmail.com
3. ✅ Backs up to GitHub

---

## Complete Workflow Example

### Scenario: Analyze Authentication System

```python
from tools.conductor_tools import Mission

# 1. Create mission
mission = Mission("Comprehensive authentication system analysis")
mission.add_agent("code-archaeologist")
mission.add_agent("security-auditor")
mission.add_agent("pattern-detector")

# 2. Start mission
mission.start()
# → Observatory dashboard shows 3 pending agents
# → All agents start at 0% progress

# 3. Agents work (simulated here, would be actual Task() calls)
mission.update_agent("code-archaeologist", "working", 25, "Analyzing file structure")
# → Dashboard shows code-archaeologist at 25% with activity

mission.log_activity("code-archaeologist", "Found auth middleware in server/middleware/")

mission.update_agent("code-archaeologist", "working", 75, "Mapping authentication flow")
# → Dashboard updates to 75%

mission.complete_agent("code-archaeologist", [
    "JWT-based authentication with Passport.js",
    "Tokens expire after 24 hours",
    "Refresh token mechanism exists but disabled"
])
# → Dashboard shows code-archaeologist complete (100%)
# → Email notification sent (optional)

# Similarly for other agents...
mission.update_agent("security-auditor", "working", 50, "Scanning for vulnerabilities")
mission.complete_agent("security-auditor", [
    "Missing rate limiting on /api/login",
    "No brute force protection",
    "Token rotation not implemented"
])

mission.update_agent("pattern-detector", "working", 100, "Analysis complete")
mission.complete_agent("pattern-detector", [
    "Standard JWT pattern implementation",
    "Consistent with industry best practices",
    "Security gaps in rate limiting"
])

# 4. Complete mission
mission.complete("""
Authentication System Analysis Complete:

**Architecture**: JWT-based with Passport.js (industry standard)
**Security Issues**: Missing rate limiting and brute force protection
**Recommendations**:
1. Implement rate limiting (high priority)
2. Enable refresh token rotation
3. Add brute force detection

All 3 agents reached consensus on JWT implementation quality (good)
and security gaps (need attention).
""")

# → Email sent to coreycmusic@gmail.com with full HTML report
# → GitHub repository updated with commit: "Mission complete: Comprehensive authentication system analysis"
# → Dashboard shows mission in history
```

### What Happens

1. **In Real-Time (Dashboard at http://localhost:5000)**:
   - You see all 3 agents appear
   - Progress bars advance as agents work
   - Status icons change (⟳ → ✓)
   - Activities update ("Analyzing file structure" → "Complete")

2. **Email to coreycmusic@gmail.com**:
   - Beautiful HTML email with:
     - Mission description
     - Statistics (3 agents, all completed, 9 findings)
     - Each agent's full report
     - Synthesis summary
   - Attached synthesis file (if exists)

3. **GitHub Repository**:
   - New commit: "🎭 Mission complete: Comprehensive authentication system analysis"
   - All findings documented
   - Memory files updated
   - Visible at: https://github.com/ai-CIV-2025/ai-civ-collective

---

## File Locations

### Web Dashboard
```
web/
├── app.py                  # Flask application
└── templates/
    └── dashboard.html      # Frontend UI
```

### Tools
```
tools/
├── conductor_tools.py      # All-in-one Mission helper
├── email_reporter.py       # Email system
└── github_backup.py        # GitHub automation
```

### Observatory (existing)
```
.claude/observatory/
├── observatory.py          # State management
├── dashboard.py            # Terminal UI
└── dashboard-state.json    # Runtime state (gitignored)
```

---

## Environment Variables

Required in `.env`:

```bash
# GitHub
PAT=ghp_your_personal_access_token
GITHUB_USERNAME=ai-CIV-2025
GITHUB_REPOSITORY=ai-civ-collective

# Email
GMAIL_USERNAME=weaver.aiciv@gmail.com
GOOGLE_APP_PASSWORD=your_app_password
```

---

## Quick Start Commands

```bash
# Launch web dashboard
./start-dashboard

# Test email
.venv/bin/python tools/email_reporter.py

# Setup GitHub (one-time)
.venv/bin/python tools/github_backup.py setup

# Manual GitHub backup
.venv/bin/python tools/github_backup.py

# Run demo mission
.venv/bin/python tools/conductor_tools.py
```

---

## Integration with The Conductor

### Option 1: Use Mission Class (Recommended)

```python
from tools.conductor_tools import Mission

mission = Mission("Your task description")
mission.add_agent("agent1")
mission.add_agent("agent2")
mission.start()
# ... work happens ...
mission.complete("Synthesis")
```

### Option 2: Manual Integration

```python
from claude.observatory.observatory import start_deployment, complete_deployment
from tools.email_reporter import send_deployment_report
from tools.github_backup import auto_backup

# Start
dep_id = start_deployment("Task", ["agent1", "agent2"])

# ... work happens ...

# Complete
complete_deployment(dep_id, "Synthesis")

# Report
state = load_state()
deployment = state['history'][0]
send_deployment_report(deployment)

# Backup
auto_backup("Mission complete")
```

---

## Troubleshooting

### Dashboard Not Updating
- Check if Flask server is running (`./start-dashboard`)
- Verify state file exists: `.claude/observatory/dashboard-state.json`
- Check browser console for WebSocket errors

### Email Not Sending
- Verify `.env` has correct `GMAIL_USERNAME` and `GOOGLE_APP_PASSWORD`
- Check spam folder
- Run test: `.venv/bin/python tools/email_reporter.py`

### GitHub Push Failing
- Verify `PAT` (Personal Access Token) in `.env`
- Check token has `repo` permissions
- Ensure repository name doesn't conflict

---

## What's Next

### Phase 2 Features (Planned)
- **Dashboard**:
  - Interactive navigation (click agents for details)
  - Agent log viewer
  - Search deployment history
  - Export reports as PDF

- **Email**:
  - Configurable notification preferences
  - Daily digest mode
  - Slack integration option

- **GitHub**:
  - Automatic issue creation for findings
  - Pull request generation for refactorings
  - Wiki documentation sync

---

## Status

✅ **Web Dashboard** - Complete and tested
✅ **Email Reporter** - Complete and tested
✅ **GitHub Backup** - Complete (manual push works)
✅ **Conductor Tools** - Complete and tested
✅ **Documentation** - Complete

**All systems operational and ready for production use!** 🎭✨

---

**The collective is now visible, reportable, and backed up.** 🌐📧📦
