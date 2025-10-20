# Telegram Duplicate Message Diagnosis - Pre-Reboot Handoff

**Date**: 2025-10-20
**Status**: UNRESOLVED - Awaiting clean reboot test
**Next Session**: Start production infrastructure and test for duplicates

---

## Problem Statement

User receiving **TWO Telegram messages** for every wrapped response:
1. **Clean message**: Correct content only
2. **Sloppy message**: Same content + CLI UI elements (status bars `────────`, prompt `>`, status text)

---

## Diagnostic Summary

### What We Ruled Out

✅ **Multiple Monitor Processes**:
- Only ONE grow_openai monitor running (PID 590654)
- ACG's monitor (PID 593185) watching different JSONL files (grow_gemini, not grow_openai)
- Old tmux-based monitor (PID 465025) was killed mid-session

✅ **JSONL File Duplication**:
- Verified: Wrapped messages appear **ONCE** in JSONL file
- Example: "Beep boop test" response exists in single location
- Claude Code writing correctly (not duplicating at source)

✅ **Send Script Issues**:
- `tools/send_telegram_plain.py` verified clean (simple API call)
- No duplication logic in send path
- Config points to correct sender script

✅ **Code Path Analysis**:
- Traced: JSONL → extract_wrapped_message → send_to_telegram → send_telegram_plain.py
- Only ONE call to `send_to_telegram()` per wrapped message
- Deduplication enabled (SHA256 hashing)

### What We Found (Suspicious but Not Confirmed Root Cause)

⚠️ **Dual Logging Handler Issue**:

```python
# tools/openai_telegram_jsonl_monitor.py lines 70-76
logging.basicConfig(
    handlers=[
        logging.FileHandler(LOG_FILE),  # Writes to /tmp/openai_telegram_jsonl_monitor.log
        logging.StreamHandler()          # Writes to stdout
    ]
)
```

**Combined with shell redirect**:
```bash
nohup python3 tools/openai_telegram_jsonl_monitor.py >> /tmp/openai_telegram_jsonl_monitor.log 2>&1 &
```

**Result**: Every log line appears TWICE in log file (same millisecond timestamp)
- Once from FileHandler (direct to file)
- Once from StreamHandler → stdout → shell redirect to same file

**BUT**: This explains duplicate LOGGING, not duplicate SENDING.

### Current Hypothesis

One of these scenarios:

1. **Logging artifact causing double processing somehow** (unclear mechanism)
2. **Hidden second monitor process** we haven't found yet
3. **Bug in monitoring loop** calling send twice despite single log entry
4. **Telegram Bot API issue** (unlikely - would affect all bots)

---

## System State Before Reboot

### Running Processes (Killed Before Reboot)
```
590654: python3 tools/openai_telegram_jsonl_monitor.py (JSONL monitor)
584102: python3 tools/openai_telegram_bridge.py (bridge)
593185: ACG_telegram_jsonl_monitor (ACG's - different project)
```

### Configuration
```json
// config/telegram_config.json
{
  "jsonl_monitor": {
    "sender_script": "tools/send_telegram_plain.py",
    "poll_interval_seconds": 3,
    "deduplication_enabled": true,
    "wrapper_markers": {
      "start": "🤖🎯📱",
      "end": "✨🔚"
    }
  }
}
```

### File Locations

**Production Lock** (use these post-reboot):
```
tools/prod/tg/
├── openai_telegram_jsonl_monitor.py  (🔒 production)
├── openai_telegram_bridge.py         (🔒 production)
├── send_telegram_plain.py            (🔒 production)
├── send_telegram_direct.py           (🔒 production)
├── start_telegram_infrastructure.sh  (🔒 startup script)
├── stop_telegram_infrastructure.sh   (🔒 shutdown script)
└── status_telegram_infrastructure.sh (🔒 status check)
```

**Development** (monitoring copies, identical to production except headers):
```
tools/
├── openai_telegram_jsonl_monitor.py  (identical to prod)
├── send_telegram_plain.py            (identical to prod)
└── (various old test scripts)
```

### Logs
```
/tmp/openai_telegram_jsonl_monitor.log       (main log - duplicate entries)
/tmp/openai_telegram_jsonl_monitor_error.log (errors only)
/tmp/openai_telegram_bridge.log              (bridge log)
```

### State Files
```
.tg_sessions/jsonl_monitor_state.json  (tracks JSONL offset, sent message hashes)
```

---

## Post-Reboot Action Plan

### 1. Start Clean Infrastructure

```bash
cd /home/corey/projects/AI-CIV/grow_openai

# Start from production directory only
./tools/prod/tg/start_telegram_infrastructure.sh

# Verify status
./tools/prod/tg/status_telegram_infrastructure.sh
```

**Expected Output**:
```
✅ JSONL Monitor: RUNNING (PID: XXXXX)
✅ Telegram Bridge: RUNNING (PID: XXXXX)
```

### 2. Verify Clean State

```bash
# Should show ONLY 2 processes (monitor + bridge)
ps aux | grep telegram | grep -v grep

# Should show clean single-line logs (not duplicates)
tail -f /tmp/openai_telegram_jsonl_monitor.log
```

### 3. Test for Duplicates

Send a wrapped test message to Corey's Telegram:

```
🤖🎯📱
Clean reboot test - checking for duplicates.
If you receive this ONCE, problem solved.
If TWICE, deeper code issue.
✨🔚
```

### 4. Outcome Analysis

**If SINGLE message received**: ✅ SOLVED
- Root cause: Zombie processes from old sessions
- Solution: Always use production scripts, clean tmux sessions between tests

**If DUPLICATE messages received**: ⚠️ CODE BUG
- Need to investigate monitoring loop logic
- Possible fix: Remove StreamHandler from logging config
- Alternative: Add unique send ID to trace actual API calls

---

## Code Investigation Plan (If Duplicates Persist)

### Option A: Fix Dual Logger

**Edit**: `tools/openai_telegram_jsonl_monitor.py` lines 70-76

**Change**:
```python
# OLD (has both handlers)
logging.basicConfig(
    handlers=[
        logging.FileHandler(LOG_FILE),
        logging.StreamHandler()  # REMOVE THIS
    ]
)

# NEW (file only)
logging.basicConfig(
    handlers=[
        logging.FileHandler(LOG_FILE)
    ]
)
```

**Then**: Kill monitor, restart, test again

### Option B: Add Send Tracing

Add unique ID to each send call to trace if send_telegram_plain.py is actually called twice:

```python
# In send_to_telegram() method
send_id = uuid.uuid4().hex[:8]
logger.info(f"SEND_TRACE [{send_id}]: Calling send script")

result = subprocess.run(
    ["python3", str(sender_script), str(user_id), message],
    capture_output=True,
    timeout=30,
    text=True
)

logger.info(f"SEND_TRACE [{send_id}]: Result code {result.returncode}")
```

Check logs - if same send_id appears twice, we're calling send twice.

### Option C: Check Telegram Bot API Logs

Use Telegram Bot API's `getUpdates` endpoint to see actual messages sent:

```bash
curl "https://api.telegram.org/bot<TOKEN>/getUpdates?offset=-10"
```

This shows if we're SENDING twice or if something else is duplicating.

---

## Key Files Reference

### Production Scripts (Use These)

**Start**:
```bash
./tools/prod/tg/start_telegram_infrastructure.sh
```

**Stop**:
```bash
./tools/prod/tg/stop_telegram_infrastructure.sh
```

**Status**:
```bash
./tools/prod/tg/status_telegram_infrastructure.sh
```

### Configuration

**Main Config**: `config/telegram_config.json`
```json
{
  "bot_token": "<REDACTED>",
  "authorized_users": {
    "437939400": {"name": "Corey", "role": "creator"}
  },
  "tmux_session": "5",
  "jsonl_monitor": {
    "enabled": true,
    "poll_interval_seconds": 3,
    "project_name": "-home-corey-projects-AI-CIV-grow-openai",
    "sender_script": "tools/send_telegram_plain.py",
    "deduplication_enabled": true
  }
}
```

**State File**: `.tg_sessions/jsonl_monitor_state.json`
```json
{
  "session_file": "6c380f81-29ba-4240-a87f-77bab63a2b09.jsonl",
  "last_offset": 5123456,
  "sent_messages": {
    "abc123def456": "2025-10-20T13:54:17.143Z"
  }
}
```

---

## Documentation Updated

✅ **Agent Updated**: `.claude/agents/tg-bridge.md`
- Added production lock architecture
- Added JSONL monitoring details
- Added process naming conventions
- File size: 29KB → 35KB

✅ **Summary Created**: `to-corey/TG-BRIDGE-AGENT-UPDATED-2025-10-20.md`

✅ **Production Backup**: `corey_tg_interface_backup.tar.gz`
- Contains all 8 production files
- Created before any modifications

---

## Next Session Immediate Actions

1. **Verify clean state** post-reboot (2 processes max)
2. **Start production infrastructure** using production scripts
3. **Send test message** with wrapper
4. **Check for duplicates** on Corey's Telegram

**If still duplicating**: Proceed to Code Investigation Plan (Option A first)

**If solved**: Document root cause was zombie processes, update production README with reboot guidance

---

## Critical Reminders

⚠️ **NEVER modify files in `tools/prod/tg/`** (production lock)
⚠️ **Always use production scripts** to start/stop infrastructure
⚠️ **Check for zombies**: `ps aux | grep telegram` before starting new processes
⚠️ **Process naming**: All grow_openai processes should have `openai_` prefix

---

## Timeline

- **08:17**: Old tmux monitor (PID 465025) last known activity
- **09:24-09:31**: Multiple monitors started/killed during debugging
- **09:31**: Current JSONL monitor started (PID 590654)
- **09:53**: Diagnostic report sent (duplicate received)
- **09:54**: Test message sent (duplicate received)
- **09:56**: User requested reboot and clean slate

---

**END OF HANDOFF**

Ready for clean reboot and fresh start with production scripts only.
