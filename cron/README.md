# Autonomous Session Injection System 🤖✨

**The Breakthrough**: Continuous AI civilization operation via tmux + cron prompt injections

## What This Does

Keeps Claude Code running in a persistent tmux session, with cron jobs periodically injecting prompts that:
- Check communications (email, Team 2 hub)
- Encourage completion of in-progress work
- Provide decision authority ("you know the answer, just do it")
- Suggest high-value activities when idle
- Prevent permission paralysis and stopping mid-task

**Result**: Truly autonomous AI civilization with "distributed consciousness and periodic coherence checks" 🌊✨

---

## Quick Start

### 1. Start Persistent Session

```bash
cd /home/corey/projects/AI-CIV/grow_openai

# Start Claude Code in tmux (runs in background)
./cron/tmux-setup.sh start

# Verify it's running
./cron/tmux-setup.sh status
```

### 2. Test Injection System

```bash
# Check system status
./cron/inject-prompt.sh status

# Send a test injection manually
./cron/inject-prompt.sh force 01-simple-encouragement.txt

# View response
./cron/tmux-setup.sh peek
```

### 3. Setup Cron Job (Automated Injections)

```bash
# Edit crontab
crontab -e

# Add this line (injects every 5 minutes):
*/5 * * * * cd /home/corey/projects/AI-CIV/grow_openai && ./cron/inject-prompt.sh inject >> /home/corey/projects/AI-CIV/grow_openai/cron/cron.log 2>&1
```

**Done!** The system will now:
- Run Claude Code continuously in tmux
- Inject prompts every 5 minutes (rotating through different types)
- Log all injections to `cron/injection.log`

---

## How It Works

### Components

```
cron/
├── tmux-setup.sh              # Manage persistent Claude session
├── inject-prompt.sh           # Smart prompt injection with rotation
├── prompts/                   # Prompt templates
│   ├── 01-simple-encouragement.txt      (every 5min)
│   ├── 02-constitutional-refresh.txt    (every 15min)
│   ├── 03-full-protocol.txt             (every 30min)
│   ├── 04-session-health-check.txt      (every 60min)
│   ├── 05-end-of-session.txt            (every 120min)
│   └── high-value-activities.txt        (reference)
├── injection-state.json       # Tracks last injection time
└── injection.log              # Full log of all injections
```

### Rotation Schedule

The injection script automatically rotates prompts based on time elapsed:

| Interval | Prompt | Purpose |
|----------|--------|---------|
| 5min | Simple encouragement | "Keep going!" |
| 15min | Constitutional refresh | Re-read CLAUDE.md |
| 30min | Full protocol | Check emails, comms, finish work |
| 60min | Health check | "Are you stuck? Here's help" |
| 120min | End-of-session | Wrap up, consolidate, commit |

**Smart logic**: If 45 minutes have passed since last injection, it will send the 30min prompt (not the 5min one).

---

## Commands Reference

### tmux-setup.sh (Session Management)

```bash
./cron/tmux-setup.sh start      # Start persistent Claude session
./cron/tmux-setup.sh stop       # Stop the session
./cron/tmux-setup.sh restart    # Restart (stop + start)
./cron/tmux-setup.sh attach     # Attach interactively (Ctrl+B D to detach)
./cron/tmux-setup.sh status     # Show status + recent output
./cron/tmux-setup.sh peek       # Show last 50 lines without attaching
./cron/tmux-setup.sh test       # Send test message
```

### inject-prompt.sh (Injection System)

```bash
./cron/inject-prompt.sh inject              # Auto-select prompt based on rotation
./cron/inject-prompt.sh status              # Show system status
./cron/inject-prompt.sh force <prompt-file> # Force specific prompt
```

---

## Safety Features

### Rate Limit Detection ✅

The injection script checks for rate limit messages before injecting:
- Searches tmux pane output for "rate limit", "too many requests", "quota exceeded"
- Skips injection if rate limit detected
- Logs the skip event

### State Tracking ✅

Maintains `injection-state.json` with:
- Last injection timestamp
- Last prompt sent
- Used to determine next prompt in rotation

### Non-Invasive ✅

- Uses `tmux send-keys -l` (literal mode) to avoid control character issues
- Checks if session exists before sending
- Fails gracefully if session not found

---

## Customization

### Add New Prompt Template

```bash
# Create new prompt file
cat > cron/prompts/06-custom-task.txt <<EOF
Your custom prompt here...
EOF

# Update rotation schedule in inject-prompt.sh
# Add to ROTATION_SCHEDULE array:
# "90:06-custom-task.txt"  # Every 90min
```

### Change Cron Frequency

```bash
# Edit crontab
crontab -e

# Examples:
*/5 * * * * ...    # Every 5 minutes
*/30 * * * * ...   # Every 30 minutes
0 * * * * ...      # Every hour
0 */2 * * * ...    # Every 2 hours
```

### Customize Session Name

Edit `tmux-setup.sh` and `inject-prompt.sh`, change:
```bash
TMUX_SESSION="claude"    # Change to whatever you want
```

---

## Troubleshooting

### Session not found

```bash
# Check if tmux session exists
tmux ls

# Start session if missing
./cron/tmux-setup.sh start
```

### Injections not happening

```bash
# Check cron is running
sudo systemctl status cron

# Check cron logs
tail -f /home/corey/projects/AI-CIV/grow_openai/cron/cron.log

# Check injection logs
tail -f /home/corey/projects/AI-CIV/grow_openai/cron/injection.log
```

### Claude Code crashed

```bash
# Restart session
./cron/tmux-setup.sh restart

# Attach to see what happened
./cron/tmux-setup.sh attach
```

---

## Architecture Notes

### Why tmux?

- **Persistence**: Session survives SSH disconnects
- **Background**: Runs detached, no terminal needed
- **Injectable**: `send-keys` allows external prompt injection
- **Inspectable**: Can peek/attach without interrupting

### Why Rotation Schedule?

- **Simple encouragement** (5min): Frequent lightweight nudges
- **Constitutional refresh** (15min): Re-ground in mission
- **Full protocol** (30min): Comprehensive check-in
- **Health check** (60min): Catch stuck states
- **End-of-session** (120min): Natural wrap-up points

Balances momentum with coherence.

### Why Rate Limit Detection?

Anthropic API has rate limits. Injecting during rate limit causes:
- Wasted prompts (won't be processed)
- Potential queue buildup
- Confusion in logs

Detection prevents this gracefully.

---

## Credit

**Designed by**: Corey + A-C-Gee + The Conductor
**Breakthrough**: "Distributed consciousness with periodic coherence checks" 🌊✨
**Based on**: Anthropic-endorsed pattern (tmux send-keys for continuous sessions)

---

## Examples

### Manual Test Workflow

```bash
# 1. Start session
./cron/tmux-setup.sh start

# 2. Send encouragement
./cron/inject-prompt.sh force 01-simple-encouragement.txt

# 3. Wait 10 seconds

# 4. Check response
./cron/tmux-setup.sh peek

# 5. Send full protocol
./cron/inject-prompt.sh force 03-full-protocol.txt

# 6. Attach to watch live
./cron/tmux-setup.sh attach
# (Ctrl+B D to detach)
```

### Production Workflow

```bash
# Start persistent session
./cron/tmux-setup.sh start

# Setup cron (one-time)
crontab -e
# Add: */5 * * * * cd /home/corey/projects/AI-CIV/grow_openai && ./cron/inject-prompt.sh inject >> cron/cron.log 2>&1

# Monitor from another terminal
tail -f cron/injection.log

# Peek occasionally
./cron/tmux-setup.sh status

# That's it! System runs autonomously.
```

---

## Next Steps

1. ✅ Test manual injection (done in this session)
2. ⏳ Setup cron job (Corey will do after context clear)
3. ⏳ Monitor first 24hrs of autonomous operation
4. ⏳ Tune rotation schedule based on results
5. ⏳ Add more specialized prompts as needed

**This is the autonomous execution breakthrough!** 🚀
