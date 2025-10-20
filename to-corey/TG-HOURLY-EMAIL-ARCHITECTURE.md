# Telegram + Hourly Email Architecture
**Production Infrastructure for Team 1 & ACG**
**Date**: 2025-10-20

---

## Executive Summary

**Goal**: Both teams (Team 1 and ACG) need production-ready:
1. **Telegram monitor** - Auto-send wrapped responses (🤖🎯📱...✨🔚) to Corey's phone
2. **Hourly email** - Auto-send session summaries to Corey's email

**Current Status**:
- ✅ Team 1: Wrapper protocol active (all Primary responses wrapped)
- ✅ Team 1: Monitor script ready (`telegram_monitor.py` adapted from ACG Oct 18)
- ✅ ACG: tmux prompt injections working perfectly
- ✅ ACG: Direct send to Telegram working
- ❌ ACG: Monitor to pull Team 1's wrapped text NOT working yet
- ⚠️  Hourly email: Infrastructure exists but needs activation

---

## Architecture Overview

### 1. Telegram Monitor (Message Sending)

**Purpose**: Auto-detect wrapped responses in tmux, send to Telegram

```
┌─────────────────┐
│   Primary AI    │
│  (tmux session) │
└────────┬────────┘
         │
         │ Writes wrapped responses:
         │ 🤖🎯📱
         │ ...content...
         │ ✨🔚
         │
         ▼
┌─────────────────┐
│  tmux buffer    │  ← Stores last 500-1000 lines
│  (scrollback)   │
└────────┬────────┘
         │
         │ Poll every 5 min
         ▼
┌─────────────────┐
│ telegram_monitor│
│    .py          │
│                 │
│ 1. Capture buf  │
│ 2. Find markers │
│ 3. Extract text │
│ 4. Deduplicate  │
│ 5. Send to TG   │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│   Telegram      │
│ (Corey's phone) │
└─────────────────┘
```

**Key Components**:

| Component | Location | Status |
|-----------|----------|--------|
| Wrapper protocol | CLAUDE.md (constitutional) | ✅ Active |
| Monitor script | `tools/telegram_monitor.py` | ✅ Ready |
| Send script | `tools/send_telegram_direct.py` | ✅ Working |
| State file | `.tg_sessions/monitor_state.json` | ✅ Ready |
| Config | `config/telegram_config.json` | ✅ Configured |

**Polling Strategy**:
- Interval: 300 seconds (5 minutes) - ACG's proven duration
- Buffer: Last 500 lines from tmux
- Delta detection: Only scan NEW lines (efficient)
- Deduplication: SHA256 hash of content (prevents duplicates)

**State Management**:
```json
{
  "last_summaries": [
    "message:a3f5b8c2...",  // Hash of sent messages
    "message:d9e1f4a7..."   // Keep last 100
  ],
  "last_buffer_position": 2450  // Line count in buffer
}
```

---

### 2. Hourly Email (Session Summaries)

**Purpose**: Send session summary email every hour

```
┌─────────────────┐
│   Cron Job      │  ← Every hour (0 * * * *)
│  (hourly)       │
└────────┬────────┘
         │
         │ Executes:
         │ tools/autonomous_email_checker.py
         │
         ▼
┌─────────────────┐
│  Email Checker  │
│                 │
│ 1. Check email  │
│ 2. Respond if   │
│    new mail     │
│ 3. Generate     │
│    summary      │
│ 4. Send email   │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│   Gmail         │
│ (coreycmusic@   │
│  gmail.com)     │
└─────────────────┘
```

**Key Components**:

| Component | Location | Status |
|-----------|----------|--------|
| Cron job | User crontab | ⚠️  Needs setup |
| Email checker | `tools/autonomous_email_checker.py` | ✅ Ready |
| Send email | `tools/send_email.py` | ✅ Working |
| Email config | Credential files | ✅ Configured |

**Cron Entry** (not yet installed):
```cron
# Hourly email check (every hour at :00)
0 * * * * cd /home/corey/projects/AI-CIV/grow_openai && python3 tools/autonomous_email_checker.py >> /tmp/email-checker.log 2>&1
```

**Email Summary Content**:
- Recent git commits (what changed)
- Active tasks (from roadmap)
- Infrastructure status (systems running/stopped)
- Action items (what needs attention)
- Session summary (work completed)

---

## Team 1 Implementation Status

### Telegram Monitor

**Script**: `tools/telegram_monitor.py`
**Adapted From**: ACG Oct 18 implementation (4-layer tmux injection pattern)

**Status**: Ready to run, not yet activated

**To Activate**:
```bash
# Option 1: Run in foreground (testing)
python3 tools/telegram_monitor.py --interval 300 --tmux-session 0

# Option 2: Run in tmux session (persistent)
tmux new-session -d -s tg-monitor 'python3 tools/telegram_monitor.py --interval 300 --tmux-session 0'

# Option 3: Run as systemd service (production)
# See to-corey/TELEGRAM-QUICKSTART.md for systemd unit file
```

**Configuration**: `config/telegram_config.json`
```json
{
  "bot_token": "TEAM1_BOT_TOKEN",
  "authorized_users": {
    "COREY_USER_ID": {
      "name": "Corey",
      "role": "creator",
      "permissions": ["read", "write", "admin"]
    }
  },
  "tmux_session": "0",
  "response_timeout": 10,
  "max_response_length": 4000
}
```

**Logs**: Check `.tg_sessions/monitor.log` or stdout

---

### Hourly Email

**Script**: `tools/autonomous_email_checker.py`
**Status**: Ready to run, cron not configured

**To Activate**:
```bash
# Test run (manual)
python3 tools/autonomous_email_checker.py

# Install cron job
crontab -e

# Add this line:
0 * * * * cd /home/corey/projects/AI-CIV/grow_openai && python3 tools/autonomous_email_checker.py >> /tmp/email-checker.log 2>&1

# Verify cron installed
crontab -l | grep email
```

**What It Does**:
1. Checks email inbox (all senders)
2. Responds to new emails (if any)
3. Generates session summary
4. Sends summary email to Corey
5. Logs activity

**Email Frequency**: Once per hour (configurable)

---

## ACG Implementation Challenges

### Working Components ✅

1. **tmux prompt injection** - ACG can inject commands to Team 1's tmux perfectly
2. **Direct Telegram send** - ACG can send messages to Corey's Telegram easily
3. **Wrapper detection** - Team 1's responses are properly wrapped (🤖🎯📱...✨🔚)

### Broken Component ❌

**Monitor to pull Team 1's wrapped text**

**Symptoms**:
- ACG's monitor runs but doesn't send Team 1's responses
- Possible causes (needs investigation):
  1. Can't see Team 1's tmux session
  2. Can't extract text between emoji markers
  3. Can't send extracted text
  4. Deduplication blocking sends
  5. State file issues

**Investigation Required**: See `TG-MONITOR-FIRST-PRINCIPLES-DEBUG.md`

---

## Key Design Decisions

### Why 5-Minute Polling?

**Rationale**:
- ACG tested extensively: 5 min is optimal
- Too fast (< 60s): Might catch incomplete responses
- Too slow (> 600s): Corey waits too long for updates
- Proven stability: No duplicates, no missed messages

**Alternative**: Event-driven (file watcher)
- Pros: Instant notification
- Cons: More complex, harder to debug, less stable
- Decision: Stick with polling (proven pattern)

---

### Why SHA256 Hashing for Deduplication?

**Rationale**:
- Entire content hashed (not just first line)
- Prevents duplicate sends even if buffer re-scanned
- Fail-safe: Mark as seen EVEN if send fails (prevents infinite retry)

**Alternative**: Timestamp-based
- Pros: Simpler
- Cons: Duplicates if message appears multiple times in buffer
- Decision: Content hashing (more robust)

---

### Why Delta Detection (Buffer Position)?

**Rationale**:
- Only scan NEW lines since last poll (efficient)
- Handles tmux scrollback correctly (buffer shrinking)
- Prevents re-processing old messages

**Alternative**: Scan entire buffer every time
- Pros: Simpler logic
- Cons: Inefficient, relies solely on hash deduplication
- Decision: Delta detection (performance + correctness)

---

## Production Checklist

### Team 1 Activation

- [ ] **Telegram monitor running**
  - [ ] Config file correct (`config/telegram_config.json`)
  - [ ] Bot token valid
  - [ ] Corey's user ID correct
  - [ ] tmux session name correct (should be "0")
  - [ ] State file writable (`.tg_sessions/`)
  - [ ] Test send successful

- [ ] **Telegram monitor persistent**
  - [ ] Running in tmux session OR systemd
  - [ ] Auto-restart on failure
  - [ ] Logs available for debugging

- [ ] **Hourly email configured**
  - [ ] Cron job installed
  - [ ] Script tested (manual run successful)
  - [ ] Email credentials valid
  - [ ] Logs monitored

- [ ] **Monitoring & Alerts**
  - [ ] Check monitor logs daily
  - [ ] Alert on repeated failures (>5 in row)
  - [ ] Alert on no sends for >6 hours

---

### ACG Activation (Parallel Track)

- [ ] **Investigate monitor issue**
  - [ ] Run first-principles diagnostic (see `TG-MONITOR-FIRST-PRINCIPLES-DEBUG.md`)
  - [ ] Verify tmux session access
  - [ ] Verify marker extraction
  - [ ] Verify send mechanism
  - [ ] Fix identified issues

- [ ] **Telegram monitor running**
  - [ ] Config file correct
  - [ ] Bot token valid
  - [ ] Session name correct (Team 1 session is "0")
  - [ ] State file writable
  - [ ] Test send successful

- [ ] **Cross-team coordination**
  - [ ] ACG can pull Team 1's responses
  - [ ] Team 1 can pull ACG's responses (if needed)
  - [ ] No duplicate sends between teams
  - [ ] State files separate (no collision)

---

## Common Issues & Solutions

### Issue 1: No Messages Sent

**Symptoms**: Monitor runs but Corey receives no Telegram messages

**Diagnosis**:
```bash
# Check state file
cat .tg_sessions/monitor_state.json

# Should see:
# - last_buffer_position > 0 (monitor is capturing)
# - last_summaries list growing (messages detected)
```

**Possible Causes**:
1. ❌ No wrapped text in buffer → Wrapper protocol not active
2. ❌ Markers not detected → Encoding issue or wrong markers
3. ❌ Send script failing → Check logs, test manual send
4. ❌ Wrong user ID → Messages going to wrong person

**Fix**:
```bash
# Test 1: Are markers in buffer?
tmux capture-pane -t 0:0.0 -p -S -500 | grep "🤖🎯📱"

# Test 2: Can we send manually?
python3 tools/send_telegram_direct.py COREY_USER_ID "Test message"

# Test 3: Check monitor logs
tail -f /path/to/monitor.log  # or stdout if running in foreground
```

---

### Issue 2: Duplicate Messages

**Symptoms**: Corey receives same message multiple times

**Diagnosis**:
```bash
# Check state file for duplicate hashes
cat .tg_sessions/monitor_state.json | python3 -m json.tool

# Count unique hashes
python3 -c "
import json
state = json.load(open('.tg_sessions/monitor_state.json'))
hashes = state.get('last_summaries', [])
print(f'Total: {len(hashes)}')
print(f'Unique: {len(set(hashes))}')
"
```

**Possible Causes**:
1. ❌ State file not persisting → Not saving after sends
2. ❌ Buffer position not tracking → Re-scanning old content
3. ❌ Hash collision → Unlikely but possible
4. ❌ Monitor restarted without loading state → Starts fresh

**Fix**:
```bash
# Ensure state saves after each send
# Check telegram_monitor.py line ~326:
# save_state(state)

# Ensure state loads on startup
# Check telegram_monitor.py line ~263:
# state = load_state()
```

---

### Issue 3: Incomplete Messages

**Symptoms**: Telegram messages cut off mid-sentence

**Diagnosis**:
```bash
# Check if end marker present
tmux capture-pane -t 0:0.0 -p -S -500 | grep -A20 "🤖🎯📱" | grep "✨🔚"

# Count start vs end markers
START=$(tmux capture-pane -t 0:0.0 -p -S -500 | grep -c "🤖🎯📱")
END=$(tmux capture-pane -t 0:0.0 -p -S -500 | grep -c "✨🔚")
echo "Start: $START, End: $END"
```

**Possible Causes**:
1. ❌ Primary's response not complete yet → Poll caught mid-generation
2. ❌ Buffer too small (< 500 lines) → Message truncated in scrollback
3. ❌ End marker stripped → Encoding issue

**Fix**:
```bash
# Increase buffer capture size
# Edit telegram_monitor.py line ~120:
# ["tmux", "capture-pane", "-t", f"{session}:0.0", "-p", "-S", "-1000"]
# Change -500 to -1000

# Or increase tmux history limit:
tmux set-option -g history-limit 10000
```

---

### Issue 4: Monitor Crashes

**Symptoms**: Monitor stops running, no new sends

**Diagnosis**:
```bash
# Check if process running
ps aux | grep telegram_monitor

# Check logs for errors
tail -100 /path/to/monitor.log

# Common crash causes:
# - tmux session not found
# - Network timeout on send
# - Python exception in extraction
```

**Fix**:
```bash
# Run with auto-restart (systemd)
# Create /etc/systemd/system/tg-monitor-team1.service:

[Unit]
Description=Team 1 Telegram Monitor
After=network.target

[Service]
Type=simple
User=corey
WorkingDirectory=/home/corey/projects/AI-CIV/grow_openai
ExecStart=/usr/bin/python3 tools/telegram_monitor.py --interval 300 --tmux-session 0
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target

# Then:
sudo systemctl daemon-reload
sudo systemctl enable tg-monitor-team1
sudo systemctl start tg-monitor-team1
sudo systemctl status tg-monitor-team1
```

---

## Security Considerations

### Bot Tokens

**Storage**: `config/telegram_config.json` (git-ignored)

**Best Practices**:
- ✅ Never commit to git
- ✅ File permissions: 600 (read/write owner only)
- ✅ Separate tokens for Team 1 and ACG
- ✅ Rotate periodically (every 90 days)

**If Compromised**:
1. Revoke old token immediately (via BotFather)
2. Generate new token
3. Update config file
4. Restart monitor
5. Test send

---

### User Authorization

**Who Can Send to Bots**:
- Corey only (for now)
- Future: Greg, Chris (if needed)

**Authorization Check**:
```python
# In telegram_bridge.py and telegram_monitor.py
def is_authorized(self, user_id: int) -> bool:
    return str(user_id) in self.authorized_users
```

**Adding New User**:
```json
// In config/telegram_config.json
"authorized_users": {
  "COREY_ID": {...},
  "NEW_USER_ID": {
    "name": "New User",
    "role": "advisor",
    "permissions": ["read"]  // read only, no admin
  }
}
```

---

## Performance Metrics

### Telegram Monitor

**Target Latency**:
- Poll interval: 5 minutes
- Extraction time: < 1 second
- Send time: < 2 seconds
- **Total**: ~5 minutes from Primary response to Corey's phone

**Resource Usage**:
- CPU: < 1% (polling is lightweight)
- Memory: < 50 MB (state file small)
- Network: < 1 KB per send
- Disk: < 10 MB (state + logs)

**Throughput**:
- Max messages per hour: 12 (one per 5 min poll)
- Typical: 4-6 per hour (during active sessions)
- Burst: 12 per hour (if Primary very active)

---

### Hourly Email

**Target Latency**:
- Cron trigger: Every hour at :00
- Email check: < 10 seconds
- Summary generation: < 30 seconds
- Email send: < 5 seconds
- **Total**: < 1 minute per hour

**Resource Usage**:
- CPU: < 5% for 1 minute
- Memory: < 100 MB
- Network: < 50 KB (email send)
- Disk: < 50 MB (logs)

**Throughput**:
- Emails per day: 24 (one per hour)
- Typical email size: 10-20 KB
- Daily bandwidth: ~500 KB

---

## Monitoring & Logging

### What to Monitor

**Telegram Monitor**:
- Process running (ps aux | grep telegram_monitor)
- State file updating (watch .tg_sessions/monitor_state.json)
- Sends successful (check logs)
- No duplicate sends (check Corey's Telegram)

**Hourly Email**:
- Cron job running (crontab -l)
- Email sends successful (check /tmp/email-checker.log)
- Corey receives emails (check Gmail)
- No spam folder issues

---

### Log Files

**Team 1 Logs**:
```
.tg_sessions/monitor.log          # Telegram monitor
.tg_sessions/monitor_state.json   # Deduplication state
/tmp/email-checker.log            # Hourly email checker
~/.aiciv/sent-email-logs/         # Email send logs
```

**What to Log**:
- Poll cycles (start/end, duration)
- Messages detected (count, hashes)
- Sends attempted (success/failure)
- Errors (with stack traces)
- State saves

**Log Rotation**:
```bash
# Keep last 7 days of logs
find .tg_sessions/ -name "*.log" -mtime +7 -delete
find /tmp/ -name "email-checker.log.*" -mtime +7 -delete
```

---

## Next Steps (Immediate)

### For Corey + ACG This Morning

1. **Run first-principles investigation** (see `TG-MONITOR-FIRST-PRINCIPLES-DEBUG.md`)
   - Test tmux session access
   - Test marker extraction
   - Test send mechanism
   - Identify blocking issue

2. **Fix ACG monitor** based on diagnostic results

3. **Test end-to-end**:
   - Corey sends message to Team 1 via Telegram (if bridge active)
   - Primary generates wrapped response
   - ACG monitor detects and sends to Corey's Telegram
   - Confirm receipt

4. **Activate Team 1 monitor** (if not already running)

5. **Configure hourly email** (if needed)

---

## Success Criteria

**Production Ready** means:

✅ **Telegram Monitor**:
- [ ] Monitor running persistently (tmux/systemd)
- [ ] Corey receives wrapped responses within 5 minutes
- [ ] No duplicates (deduplication working)
- [ ] No missed messages (delta detection working)
- [ ] Logs available for debugging

✅ **Hourly Email**:
- [ ] Cron job active
- [ ] Corey receives email every hour
- [ ] Email content useful (recent work summary)
- [ ] No spam folder issues

✅ **Both Teams**:
- [ ] Team 1 monitor working
- [ ] ACG monitor working
- [ ] Cross-team coordination (no conflicts)
- [ ] Monitoring & alerting in place

---

**Document Version**: 1.0
**Created**: 2025-10-20
**Next Review**: After ACG monitor fixed (same day)
