# Telegram Infrastructure Wake-Up Procedure

**Last Tested**: 2025-10-20
**Status**: ✅ WORKING (zero duplicates, zero slop)
**Team**: Team 1 (grow_openai)

---

## 🎯 Quick Start (Copy-Paste Every Session)

### Step 1: Check Status

```bash
# Check what's running
ps aux | grep -E "openai_telegram" | grep -v grep | grep -v tail
```

**Expected output**: 2 Team 1 processes
```
corey  77133  ... python3 tools/openai_telegram_bridge_diagnostic.py
corey  77363  ... python3 tools/prod/tg/openai_telegram_jsonl_monitor.py
```

**Also visible**: 2 ACG processes (different bot, don't touch)
```
corey  4498   ... python3 tools/prod/tg/acg_telegram_jsonl_monitor.py
corey  4528   ... python3 tools/prod/tg/acg_telegram_bridge.py
```

---

### Step 2: Start Infrastructure (if not running)

```bash
# Change to project directory
cd /home/corey/projects/AI-CIV/grow_openai

# Start JSONL monitor
nohup python3 tools/prod/tg/openai_telegram_jsonl_monitor.py >> /tmp/openai_telegram_jsonl_monitor.log 2>&1 &

# Start bridge (DIAGNOSTIC VERSION - this is the one that works!)
nohup python3 tools/openai_telegram_bridge_diagnostic.py >> /tmp/openai_telegram_bridge_diagnostic.log 2>&1 &

# Wait for startup
sleep 2

# Verify both started
ps aux | grep -E "openai_telegram" | grep -v grep
```

**Expected output**: 2 processes running (monitor + bridge)

---

### Step 3: Test (CRITICAL)

**Send test message via Telegram**:
```
Wake-up test
```

**Expected behavior**:
- ✅ Message appears ONCE in Claude Code tmux session
- ✅ Message does NOT duplicate after 30 seconds
- ✅ Your response appears on Telegram (via JSONL monitor)

**If message duplicates**: Something is wrong, see Troubleshooting section

---

### Step 4: Stop (if needed)

```bash
# Stop both processes (Team 1 only)
pkill -f openai_telegram_bridge_diagnostic
pkill -f openai_telegram_jsonl_monitor

# Verify stopped
ps aux | grep -E "openai_telegram" | grep -v grep
```

**Expected output**: Only ACG processes remain (PIDs 4498, 4528)

---

## 📁 Files Used (Production)

### Core Infrastructure
- **Bridge**: `tools/openai_telegram_bridge_diagnostic.py` ✅ WORKING
  - Update ID deduplication (prevents Telegram API duplicates)
  - Injection locking (prevents race conditions)
  - Trace ID logging (diagnostic capability)

- **Monitor**: `tools/prod/tg/openai_telegram_jsonl_monitor.py` ✅ WORKING
  - JSONL file monitoring (3s polls, 20x faster than tmux)
  - SHA256 deduplication (prevents duplicate sends)
  - Session rotation handling

- **Config**: `config/telegram_config.json` ✅ WORKING
  - Session: "1" (tmux session name)
  - Authorized user: 437939400 (Corey)
  - Working directory: `/home/corey/projects/AI-CIV/grow_openai`

### Senders (Manual Use)
- **Plain text**: `tools/prod/tg/send_telegram_plain.py`
- **Markdown**: `tools/prod/tg/send_telegram_direct.py`

### Logs
- Bridge: `/tmp/openai_telegram_bridge_diagnostic.log`
- Monitor: `/tmp/openai_telegram_jsonl_monitor.log`
- Error tracking: Includes trace IDs for debugging

### State Files
- `.tg_sessions/jsonl_monitor_state.json` - Monitor state (file offset, sent hashes)
- `.tg_sessions/437939400.json` - User session metadata

---

## 🚫 DO NOT TOUCH

### Protected Files
- **Bridge**: `tools/openai_telegram_bridge_diagnostic.py`
  - Has production lock header
  - Confirmed working with zero duplicates
  - Make variants (v2) if changes needed

- **Monitor**: `tools/prod/tg/openai_telegram_jsonl_monitor.py`
  - Has production lock header
  - Part of production lock architecture
  - Archive before modifying

### ACG Processes (Sister Collective)
- **PIDs**: 4498, 4528
- **Bot**: Different token (grow_gemini project)
- **Session**: "2" (separate tmux session)
- **DO NOT**: pkill, stop, or interfere with ACG processes
- **Why**: Spatial isolation prevents collisions

### Configuration
- `config/telegram_config.json` - Session "1" is Team 1 identity
- `.tg_sessions/` directory - State persistence

---

## 🔧 Troubleshooting

### Problem: Messages duplicate after 30 seconds

**Diagnosis**: Bridge not using diagnostic version
```bash
ps aux | grep openai_telegram_bridge | grep -v grep
```

**If you see**: `tools/prod/tg/openai_telegram_bridge.py` (WRONG - broken version)
```bash
# Stop broken version
pkill -f "tools/prod/tg/openai_telegram_bridge.py"

# Start diagnostic version
cd /home/corey/projects/AI-CIV/grow_openai
nohup python3 tools/openai_telegram_bridge_diagnostic.py >> /tmp/openai_telegram_bridge_diagnostic.log 2>&1 &
```

**If you see**: `tools/openai_telegram_bridge_diagnostic.py` (CORRECT)
- Check logs: `tail -50 /tmp/openai_telegram_bridge_diagnostic.log`
- Look for duplicate update_ids or trace_id collisions

---

### Problem: No response on Telegram

**Diagnosis**: JSONL monitor not running or not detecting responses
```bash
# Check if monitor running
ps aux | grep openai_telegram_jsonl_monitor | grep -v grep

# Check recent monitor activity
tail -20 /tmp/openai_telegram_jsonl_monitor.log
```

**Solution 1**: Restart monitor
```bash
pkill -f openai_telegram_jsonl_monitor
cd /home/corey/projects/AI-CIV/grow_openai
nohup python3 tools/prod/tg/openai_telegram_jsonl_monitor.py >> /tmp/openai_telegram_jsonl_monitor.log 2>&1 &
```

**Solution 2**: Check wrapper protocol
- Responses must be wrapped: `🤖🎯📱 ... ✨🔚`
- If not wrapped, monitor won't detect them

---

### Problem: Bridge crash/exit

**Check logs**:
```bash
tail -50 /tmp/openai_telegram_bridge_diagnostic.log
```

**Common causes**:
- Invalid bot token (check `TELEGRAM_BOT_TOKEN` env var)
- Network connectivity (Telegram API unreachable)
- Config file corruption (`config/telegram_config.json`)

**Recovery**:
```bash
# Restart bridge
cd /home/corey/projects/AI-CIV/grow_openai
nohup python3 tools/openai_telegram_bridge_diagnostic.py >> /tmp/openai_telegram_bridge_diagnostic.log 2>&1 &
```

---

### Problem: Wrong tmux session

**Symptom**: Messages not appearing in Claude Code session

**Check config**:
```bash
grep tmux_session config/telegram_config.json
```

**Expected**: `"tmux_session": "1"`

**If wrong**: Edit `config/telegram_config.json` and restart bridge

---

### Problem: ACG collision

**Symptom**: Process name collision, Team 1 bridge won't start

**Diagnosis**:
```bash
ps aux | grep telegram_bridge | grep -v grep
```

**If you see**: `telegram_bridge.py` without `openai_` prefix
```bash
# Wrong! Old naming convention
# Team 1 MUST use openai_ prefix to prevent ACG collision
```

**Solution**: Always use diagnostic bridge with `openai_` prefix

---

## 📊 Validation Checklist

After wake-up, verify:

- [ ] **Status check**: 2 Team 1 processes running
- [ ] **Bridge log**: No errors in last 10 lines
- [ ] **Monitor log**: Polling active, no errors
- [ ] **Test message**: Sent and received ONCE (no duplicates)
- [ ] **Response delivery**: Your response arrived on Telegram
- [ ] **ACG untouched**: ACG processes still running (4498, 4528)

**All green**: Infrastructure healthy, ready for session

**Any red**: Investigate logs, restart processes, retest

---

## 🔍 Understanding What Works (Technical)

### Why Diagnostic Bridge Works

**1. Update ID Deduplication**:
```python
PROCESSED_UPDATES = {}  # update_id -> {timestamp, trace_id, message}

# Before processing message
if update_id in PROCESSED_UPDATES:
    logger.warning(f"Duplicate update_id {update_id} - SKIPPING")
    return
```

**2. Injection Locking**:
```python
INJECTION_LOCK = Lock()

with INJECTION_LOCK:
    # Only one injection at a time
    inject_message_to_tmux(message)
```

**3. Trace IDs**:
- Each message gets unique UUID
- Logged at every step
- Makes duplicate tracking trivial

### Why JSONL Monitor Works

**1. Delta Detection**:
- Tracks file offset (`.tg_sessions/jsonl_monitor_state.json`)
- Reads only NEW lines (not entire buffer)
- 20x faster than tmux polling

**2. SHA256 Deduplication**:
- Hashes complete message content
- Stores sent hashes in state file
- Prevents duplicate sends

**3. Session Rotation**:
- Detects new JSONL files (session UUID changes)
- Automatically switches to newest file
- Zero downtime during session rotation

---

## 📚 Related Documentation

- **Production Lock**: `tools/.archive/telegram-cleanup-2025-10-20/MANIFEST.md`
- **Agent Manifest**: `.claude/agents/tg-bridge.md`
- **Diagnostic Procedure**: `tools/DUPLICATE-DIAGNOSTIC-PROCEDURE.md`
- **Quick Start**: `tools/TELEGRAM-DUPLICATE-QUICKSTART.md`

---

## 🎯 Success Criteria

**Perfect wake-up**:
1. Copy-paste commands from Step 2
2. Both processes start (5 seconds)
3. Test message (no duplicates)
4. Response delivered to Telegram
5. Zero intervention needed

**This is the goal**: Wake-up protocol that works EVERY TIME.

---

**Document Status**:
- **Created**: 2025-10-20
- **Last Tested**: 2025-10-20
- **Validation**: ✅ Zero duplicates confirmed
- **Next Review**: After 7 days continuous operation

**Maintained by**: tg-bridge agent (Telegram infrastructure specialist)
