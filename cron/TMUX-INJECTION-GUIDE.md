# Tmux Session Injection Guide

## Quick Setup: Targeting the Correct Session

### Problem
Multiple tmux sessions running (yours vs A-C-Gee's). Scripts need to target the correct session.

### Solution

**1. Find your tmux session number:**
```bash
tmux list-sessions
```

Look for your attached session. Example output:
```
0: 1 windows (created Sun Oct  5 08:22:46 2025)
1: 1 windows (created Sun Oct  5 09:01:46 2025) (attached)
3: 1 windows (created Sun Oct  5 09:21:24 2025) (attached)  <- THIS ONE
claude: 1 windows (created Sun Oct  5 09:10:27 2025)
```

**2. Update the session target in both scripts:**

Edit `cron/tmux-setup.sh`:
```bash
TMUX_SESSION="3"  # Change "claude" to your session number/name
```

Edit `cron/inject-prompt.sh`:
```bash
TMUX_SESSION="3"  # Change "claude" to your session number/name
```

**3. Test it works:**
```bash
./cron/tmux-setup.sh test "Hello from the injection system!"
```

You should receive the message in your Claude Code session.

### How It Works

The injection system sends text to a tmux pane using `tmux send-keys`:

```bash
# The key command:
tmux send-keys -t "${TMUX_SESSION}.0" -l "Your message here"
tmux send-keys -t "${TMUX_SESSION}.0" Enter
```

- `-t "${TMUX_SESSION}.0"` targets session.pane (e.g., "3.0")
- `-l` sends literal text (doesn't interpret special chars)
- `Enter` submits the message

### Files Involved

1. **cron/tmux-setup.sh** - Session management + testing
2. **cron/inject-prompt.sh** - Autonomous prompt injection
3. **cron/injection-state.json** - Tracks last injection time
4. **cron/prompts/*.txt** - Rotating prompt templates

### Quick Commands

```bash
# Check status
./cron/tmux-setup.sh status

# Send test message
./cron/tmux-setup.sh test "Your message"

# View last 50 lines without attaching
./cron/tmux-setup.sh peek

# Run autonomous injection (cron will do this)
./cron/inject-prompt.sh inject

# Force specific prompt
./cron/inject-prompt.sh force 01-simple-encouragement.txt
```

### For Cron Setup

The crontab entry should run the injection script:
```cron
*/5 * * * * cd /path/to/project && ./cron/inject-prompt.sh inject
```

Make sure `TMUX_SESSION` matches your actual session before enabling cron!

---

**TL;DR**: Change `TMUX_SESSION="claude"` to your session number in both scripts, test with `./cron/tmux-setup.sh test`, done.
