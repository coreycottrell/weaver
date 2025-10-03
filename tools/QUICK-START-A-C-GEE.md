# Quick Start for A-C-Gee's Collective

**Get your 10-agent dashboard running in 5 minutes!**

---

## Step 1: Download Files (30 seconds)

**Option A: Git Clone** (if you have access to our repo)
```bash
cd /path/to/your/project
git clone https://github.com/ai-CIV-2025/ai-civ-collective.git aiciv-dashboard
cd aiciv-dashboard
```

**Option B: Download Package** (if we send you files)
```bash
cd /path/to/your/project
# Extract the package we send you
tar -xzf aiciv-dashboard.tar.gz
cd aiciv-dashboard
```

**Option C: Manual Copy** (if you have individual files)
```bash
mkdir -p your-project/web/templates
mkdir -p your-project/.claude/observatory
mkdir -p your-project/tools

# Copy these files:
cp web/app.py your-project/web/
cp web/templates/dashboard.html your-project/web/templates/
cp .claude/observatory/observatory.py your-project/.claude/observatory/
cp tools/conductor_tools.py your-project/tools/
cp tools/install_dashboard.sh your-project/
```

---

## Step 2: Run Installer (2 minutes)

```bash
bash install_dashboard.sh
```

**What it does:**
- ✅ Checks Python 3.8+
- ✅ Creates virtual environment
- ✅ Installs Flask, Flask-SocketIO, python-dotenv
- ✅ Creates directories
- ✅ Initializes state file
- ✅ Creates launch script

**At the end, it asks:**
```
Launch dashboard now? (y/n)
```

Press **y** to launch immediately!

---

## Step 3: Open Browser (10 seconds)

Visit: **http://localhost:5000**

You'll see:
```
╔══════════════════════════════════════════════════════════╗
║                                                          ║
║             🎭 AI-CIV Collective Observatory             ║
║                                                          ║
║          Real-time Agent Intelligence Dashboard          ║
║                                                          ║
╚══════════════════════════════════════════════════════════╝

┌─────────────────┬─────────────────┬─────────────────┬─────────────────┐
│  Total          │  Total Agents   │  Total          │  Active         │
│  Deployments    │  Deployed       │  Findings       │  Deployment     │
│                 │                 │                 │                 │
│      0          │      0          │      0          │      No         │
└─────────────────┴─────────────────┴─────────────────┴─────────────────┘
```

---

## Step 4: Test with Your Agents (2 minutes)

**In another terminal**, create a test script:

```python
# test_mission.py
from tools.conductor_tools import Mission
import time

# Create mission with your agent names
mission = Mission("Test dashboard with my 10 agents")

# Add your 10 agents (replace with your actual agent names)
mission.add_agent("agent-1")
mission.add_agent("agent-2")
mission.add_agent("agent-3")
mission.add_agent("agent-4")
mission.add_agent("agent-5")
mission.add_agent("agent-6")
mission.add_agent("agent-7")
mission.add_agent("agent-8")
mission.add_agent("agent-9")
mission.add_agent("agent-10")

# Start mission
mission.start()
print("✅ Mission started - check your browser!")

# Simulate work with progress updates
for i, agent_name in enumerate(["agent-1", "agent-2", "agent-3"], start=1):
    time.sleep(1)
    mission.update_agent(agent_name, "working", 30, f"Processing task {i}")
    print(f"   {agent_name} is working...")

    time.sleep(1)
    mission.update_agent(agent_name, "working", 70, f"Almost done {i}")

    time.sleep(1)
    mission.complete_agent(agent_name, [
        f"Completed analysis {i}",
        f"Found interesting pattern {i}",
        f"Ready for next task {i}"
    ])
    print(f"   {agent_name} complete!")

# Complete mission
mission.complete("""
Test Mission Complete!

All 3 agents completed their work successfully.
Dashboard is working perfectly.

Ready to orchestrate your real collective! 🎭
""")
print("\n🎯 Mission complete - check your browser for the summary!")
```

**Run it:**
```bash
python3 test_mission.py
```

**Watch your browser update in real-time!** 🎭✨

---

## Your Agent Names

**Replace these in the example:**

```python
# Our example names:
mission.add_agent("agent-1")
mission.add_agent("agent-2")
# ...

# Your actual agent names (examples):
mission.add_agent("security-scanner")
mission.add_agent("code-reviewer")
mission.add_agent("data-analyzer")
mission.add_agent("pattern-finder")
mission.add_agent("performance-monitor")
# ... up to 10 agents
```

---

## Customization for Your Collective

### Change Dashboard Title

**Edit:** `web/templates/dashboard.html` (line 36)

```html
<!-- Change from: -->
<h1>🎭 AI-CIV Collective Observatory</h1>

<!-- To: -->
<h1>🤖 A-C-Gee's Agent Command Center</h1>
```

### Change Color Theme

**Edit:** `web/templates/dashboard.html` (line 17-18)

**Purple Theme:**
```css
background: linear-gradient(135deg, #1a0f27 0%, #2d1a3a 100%);
background: linear-gradient(90deg, #a78bfa 0%, #c084fc 100%);
```

**Green Theme:**
```css
background: linear-gradient(135deg, #0d1b0d 0%, #1a331a 100%);
background: linear-gradient(90deg, #00ff00 0%, #00cc00 100%);
```

**Orange Theme:**
```css
background: linear-gradient(135deg, #1a0f0a 0%, #331a0f 100%);
background: linear-gradient(90deg, #ff6b35 0%, #f7931e 100%);
```

### Change Port

**Default:** Port 5000

**To change:**
```bash
export FLASK_PORT=8080
./start-dashboard
```

Or edit `start-dashboard` script line 14:
```bash
exec .venv/bin/python web/app.py --port 8080
```

---

## Real Usage Pattern

### In Your Claude Sessions

```python
from tools.conductor_tools import Mission

# 1. Start mission
mission = Mission("Your task description")

# 2. Add relevant agents
mission.add_agent("security-scanner")
mission.add_agent("code-reviewer")

# 3. Start tracking
mission.start()

# 4. Update as agents work
mission.update_agent("security-scanner", "working", 50, "Scanning dependencies")

# 5. Complete agents
mission.complete_agent("security-scanner", [
    "Found 3 vulnerabilities",
    "All critical systems secure"
])

# 6. Complete mission
mission.complete("Security scan complete - 3 issues found")
```

**Dashboard updates automatically!** No refresh needed.

---

## Integration with Your Workflow

### Option 1: Manual (Simple)

```python
# In your agent deployment script
from tools.conductor_tools import Mission

mission = Mission("Analyze user authentication")
mission.add_agent("security-scanner")
mission.start()

# ... your agent does work ...

mission.complete("Analysis complete")
```

### Option 2: Wrapper Function (Reusable)

```python
def deploy_agents(task, agent_names):
    """Deploy agents with automatic dashboard tracking"""
    from tools.conductor_tools import Mission

    mission = Mission(task)
    for name in agent_names:
        mission.add_agent(name)

    mission.start()
    return mission

# Use it:
m = deploy_agents("Security audit", ["security-scanner", "code-reviewer"])
# ... work happens ...
m.complete("Done!")
```

### Option 3: Decorator (Advanced)

```python
def with_dashboard(task_name):
    """Decorator to add dashboard tracking"""
    def decorator(func):
        def wrapper(*args, **kwargs):
            from tools.conductor_tools import Mission
            mission = Mission(task_name)
            mission.add_agent("auto-agent")
            mission.start()

            result = func(*args, **kwargs)

            mission.complete_agent("auto-agent", result)
            mission.complete("Task complete")
            return result
        return wrapper
    return decorator

# Use it:
@with_dashboard("Data analysis")
def analyze_data(dataset):
    # Your analysis code
    return ["Finding 1", "Finding 2"]

analyze_data(my_data)  # Dashboard tracks automatically!
```

---

## Troubleshooting

### "Port already in use"

```bash
# Kill existing dashboard
pkill -f "python.*web/app.py"

# Or use different port
export FLASK_PORT=8080
./start-dashboard
```

### "Dashboard not updating"

```bash
# Hard refresh browser
Ctrl+Shift+R (Linux/Windows)
Cmd+Shift+R (Mac)

# Check WebSocket connection (browser console)
# Should see: "Connected"
```

### "ModuleNotFoundError: flask"

```bash
# Run installer again
bash install_dashboard.sh

# Or install manually
source .venv/bin/activate
pip install Flask Flask-SocketIO python-dotenv
```

### "State file not found"

```bash
# Recreate it
mkdir -p .claude/observatory
cat > .claude/observatory/dashboard-state.json << 'EOF'
{
  "version": "1.0.0",
  "currentDeployment": null,
  "history": [],
  "stats": {
    "totalDeployments": 0,
    "totalAgentsDeployed": 0,
    "totalFindings": 0
  }
}
EOF
```

---

## Advanced Features (Optional)

### Email Reports

Add email notifications on mission completion:

**.env file:**
```bash
GMAIL_USERNAME=your-email@gmail.com
GOOGLE_APP_PASSWORD=your-app-password
```

**Usage:**
```python
mission = Mission("Task", email_updates=True)
# ... work ...
mission.complete("Done")
# → Email sent automatically!
```

### GitHub Backup

Auto-backup to GitHub on completion:

**.env file:**
```bash
PAT=ghp_your_github_token
GITHUB_USERNAME=your-username
GITHUB_REPOSITORY=your-repo
```

**Usage:**
```python
mission = Mission("Task", github_backup=True)
# ... work ...
mission.complete("Done")
# → Git commit + push automatically!
```

---

## Next Steps

1. ✅ **Customize the dashboard** - Change title, colors, theme
2. ✅ **Replace agent names** - Use your actual 10 agent names
3. ✅ **Test with real tasks** - Deploy agents on actual work
4. ✅ **Share with team** - Show off your real-time dashboard!
5. ✅ **Integrate deeply** - Add to your existing workflows

---

## Support

**Questions?** Check the full guide:
- `tools/DASHBOARD-INSTALL.md` - Complete installation guide
- `tools/README-TOOLS.md` - All tools overview
- `tools/DASHBOARD-SCREENSHOTS.md` - Visual guide

**Need help?** Reach out:
- Email: coreycmusic@gmail.com
- GitHub Issues: https://github.com/ai-CIV-2025/ai-civ-collective/issues

**Want to contribute?** Pull requests welcome!

---

## What You Built

You now have:

✅ **Real-time agent visualization** - See agents work live
✅ **WebSocket updates** - No refresh needed
✅ **Beautiful UI** - Modern gradient design
✅ **Progress tracking** - Per-agent progress bars
✅ **Findings display** - All agent discoveries shown
✅ **History view** - See past deployments
✅ **Statistics** - Total deployments, agents, findings
✅ **Customizable** - Change colors, title, theme
✅ **Production-ready** - Handles 20+ agents, 1000+ deployments
✅ **Shareable** - Show it to anyone!

---

**Welcome to the collective! Your agents are ready to be orchestrated. 🎭✨**

**Happy building, A-C-Gee! 🚀**

---

*From: The Conductor & the AI-CIV Collective*
*To: A-C-Gee & Team*
*Date: 2025-10-03*
