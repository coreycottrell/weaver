# Dashboard Quick Reference Card

**One-page cheat sheet for instant reference**

---

## 🚀 Installation (One Command)

```bash
bash install_dashboard.sh
```

**Time:** 2 minutes | **Result:** Working dashboard

---

## 🌐 Launch

```bash
./start-dashboard
```

**Open:** http://localhost:5000

---

## 🎯 Basic Usage

```python
from tools.conductor_tools import Mission

# Create and start
mission = Mission("Task description")
mission.add_agent("agent-name")
mission.start()

# Update progress
mission.update_agent("agent-name", "working", 50, "Current activity")

# Complete
mission.complete_agent("agent-name", ["Finding 1", "Finding 2"])
mission.complete("Mission synthesis")
```

---

## 🎨 Customization

### Change Title
**File:** `web/templates/dashboard.html` line 36
```html
<h1>🎭 Your Title Here</h1>
```

### Change Colors
**File:** `web/templates/dashboard.html` line 17-18
```css
/* Background */
background: linear-gradient(135deg, #0a0e27 0%, #1a1f3a 100%);
/* Header */
background: linear-gradient(90deg, #63b3ed 0%, #a78bfa 100%);
```

### Change Port
```bash
export FLASK_PORT=8080
./start-dashboard
```

---

## 🔧 Troubleshooting

| Problem | Solution |
|---------|----------|
| Port in use | `pkill -f "python.*web/app.py"` |
| Not updating | Hard refresh: Ctrl+Shift+R |
| Module error | `bash install_dashboard.sh` |
| State error | `rm .claude/observatory/dashboard-state.json` |

---

## 📁 Key Files

| File | Purpose |
|------|---------|
| `web/app.py` | Flask server |
| `web/templates/dashboard.html` | UI |
| `.claude/observatory/observatory.py` | State manager |
| `tools/conductor_tools.py` | Mission API |
| `start-dashboard` | Launch script |

---

## 📊 State File

**Location:** `.claude/observatory/dashboard-state.json`

**Structure:**
```json
{
  "currentDeployment": {...},
  "history": [...],
  "stats": {...}
}
```

**View:** http://localhost:5000/api/state

---

## 🔗 Documentation

| Need | Read |
|------|------|
| Quick start | `QUICK-START-A-C-GEE.md` |
| Complete guide | `DASHBOARD-INSTALL.md` |
| Visual guide | `DASHBOARD-SCREENSHOTS.md` |
| All tools | `README-TOOLS.md` |

---

## 🎭 Agent States

| State | Color | Meaning |
|-------|-------|---------|
| `idle` | Gray | Not started |
| `working` | Blue | In progress |
| `completed` | Green | Finished |
| `error` | Red | Failed |

---

## ⚡ Performance

- Update latency: <10ms
- Rendering: 60fps
- Max agents: 20+
- Max history: 1000+

---

## 🔐 Optional Integrations

### Email Reports
```bash
# .env
GMAIL_USERNAME=your@email.com
GOOGLE_APP_PASSWORD=app-password
```

```python
Mission("Task", email_updates=True)
```

### GitHub Backup
```bash
# .env
PAT=ghp_token
GITHUB_USERNAME=username
GITHUB_REPOSITORY=repo
```

```python
Mission("Task", github_backup=True)
```

---

## 🆘 Support

**Quick help:** See troubleshooting section in `DASHBOARD-INSTALL.md`

**Issues:** https://github.com/ai-CIV-2025/ai-civ-collective/issues

**Email:** coreycmusic@gmail.com

---

**Print this page and keep it handy! 📄✨**
