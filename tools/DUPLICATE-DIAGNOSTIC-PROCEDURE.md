# Duplicate Message Injection Diagnostic Procedure

**Created**: 2025-10-20
**Agent**: tg-bridge
**Problem**: Telegram messages appearing twice in Claude Code with ~25s delay

---

## Diagnostic Tool Created

**File**: `tools/openai_telegram_bridge_diagnostic.py`

**Key Features**:
1. **Unique Trace IDs**: Each message gets UUID for tracking through pipeline
2. **Update ID Tracking**: Detects if Telegram API sends same update twice
3. **Injection Lock**: Prevents concurrent processing race conditions
4. **Comprehensive Logging**: Every step logged with timestamps
5. **Duplicate Detection**: Blocks re-injection of same trace ID
6. **Status Command**: `/status` shows diagnostic metrics

**Logging**: `/tmp/openai_telegram_bridge_diagnostic.log` (detailed trace)

---

## Deployment Steps

### Step 1: Stop Production Bridge

```bash
# Find and kill production bridge
ps aux | grep "tools/prod/tg/openai_telegram_bridge.py" | grep -v grep
# Note the PID
kill <PID>

# Verify stopped
ps aux | grep telegram_bridge | grep -v grep
# Should show nothing from tools/prod/tg/
```

### Step 2: Start Diagnostic Bridge

```bash
cd /home/corey/projects/AI-CIV/grow_openai

# Start diagnostic version
nohup python3 tools/openai_telegram_bridge_diagnostic.py >> /tmp/openai_telegram_bridge_diagnostic.log 2>&1 &

# Verify running
ps aux | grep openai_telegram_bridge_diagnostic
```

### Step 3: Send Test Messages

**From Telegram** (send to bot):
1. `Test 1` - Simple message
2. Wait 30 seconds - Observe if duplicate appears
3. `Test 2` - Second message
4. `/status` - Get diagnostic metrics

**Watch Log in Real-Time**:
```bash
tail -f /tmp/openai_telegram_bridge_diagnostic.log
```

### Step 4: Analyze Results

**Look for these patterns in log**:

**Pattern A: Duplicate Update ID (Telegram API Issue)**
```
📨 MESSAGE RECEIVED
  Update ID: 12345

[25 seconds later]

⚠️ DUPLICATE UPDATE_ID DETECTED!
  Previous processing: 2025-10-20T10:37:30
  This means Telegram API sent the same update twice!
```
**Diagnosis**: Telegram API is re-sending updates (library bug or network issue)
**Fix**: Update python-telegram-bot library, adjust polling parameters

**Pattern B: Duplicate Injection Attempt (Bridge Bug)**
```
🔍 INJECTION ATTEMPT
  Trace ID: abc-123
  Update ID: 12345

[25 seconds later]

🔍 INJECTION ATTEMPT
  Trace ID: abc-123  ← SAME TRACE ID
⚠️ DUPLICATE INJECTION ATTEMPT DETECTED!
```
**Diagnosis**: Bridge calling inject_to_tmux() twice for same message
**Fix**: Find code path causing duplicate call

**Pattern C: Different Update IDs, Same Content (Not Duplicate)**
```
📨 MESSAGE RECEIVED
  Update ID: 12345
  Message: "Test 1"

📨 MESSAGE RECEIVED
  Update ID: 12346  ← DIFFERENT
  Message: "Test 1"  ← Same text but new update
```
**Diagnosis**: User actually sent message twice
**Fix**: Not a bug - expected behavior

---

## Hypothesis Testing

### Hypothesis 1: Telegram API Sending Duplicates

**Test**: Check if update_id is same for both appearances

**If TRUE**:
- Log will show "DUPLICATE UPDATE_ID DETECTED"
- Diagnostic bridge will block second injection
- Root cause: python-telegram-bot library bug or network retry

**Fix Options**:
1. Update python-telegram-bot to latest version
2. Adjust `run_polling()` parameters (timeout, pool_timeout)
3. Implement persistent update_id tracking across restarts

### Hypothesis 2: Bridge Processing Same Message Twice

**Test**: Check if same trace_id appears in two injection attempts

**If TRUE**:
- Log will show "DUPLICATE INJECTION ATTEMPT DETECTED"
- Means handle_message() or inject_to_tmux() called twice
- Root cause: Async race condition or retry logic

**Fix Options**:
1. Add async lock around message handling
2. Review retry logic (is there any?)
3. Check for duplicate handler registration

### Hypothesis 3: tmux Echoing Input

**Test**: Stop bridge, manually inject message, see if it appears twice

**Command**:
```bash
# With bridge STOPPED
tmux send-keys -t 1:0.0 -l "[TELEGRAM from Test] Manual injection"
tmux send-keys -t 1:0.0 Enter
```

**If message appears twice**: tmux or Claude Code echoing
**If message appears once**: Bridge is causing duplication

### Hypothesis 4: Claude Code JSONL Processing

**Test**: Check if Claude Code writes each message twice to JSONL

**Command**:
```bash
# Get current session JSONL
SESSION_FILE=$(ls -t ~/.claude/projects/-home-corey-projects-AI-CIV-grow_openai/*.jsonl | head -1)
grep "\[TELEGRAM from" "$SESSION_FILE" | tail -10
```

**If same message appears twice with different timestamps**: Claude Code echoing
**If appears once**: Not Claude Code issue

### Hypothesis 5: Multiple Bridge Processes

**Test**: Check for duplicate processes (even with different names)

**Command**:
```bash
ps aux | grep telegram | grep python
# Look for ANY bridge processes, including old names
```

**If multiple found**: Kill extras, restart single diagnostic bridge
**If single found**: Not a process duplication issue

---

## Expected Diagnostic Output

### Good Result (No Duplicates)

**Log Pattern**:
```
10:37:30 - 📨 MESSAGE RECEIVED
10:37:30 -   Update ID: 100500
10:37:30 -   Trace ID: abc-123-def
10:37:30 - 🔍 INJECTION ATTEMPT
10:37:30 -   Trace ID: abc-123-def
10:37:30 - ✓ tmux injection successful
10:37:30 -   Total injections so far: 1
```

**Claude Code**: Message appears ONCE

### Bad Result (Duplicates Detected)

**Log Pattern**:
```
10:37:30 - 📨 MESSAGE RECEIVED
10:37:30 -   Update ID: 100500
10:37:30 -   Trace ID: abc-123-def
10:37:30 - 🔍 INJECTION ATTEMPT
10:37:30 - ✓ tmux injection successful

10:37:55 - 📨 MESSAGE RECEIVED  ← 25 SECONDS LATER
10:37:55 -   Update ID: 100500  ← SAME UPDATE ID
10:37:55 - ⚠️ DUPLICATE UPDATE_ID DETECTED!
10:37:55 -   Time since first: 25.0s
```

**This tells us**: Telegram API re-sent the update after 25 seconds (likely timeout-based retry)

---

## Root Cause Analysis Guide

### If Duplicate is at Telegram API Level

**Evidence**: Same update_id appears twice in log

**Why 25 seconds?**
- python-telegram-bot default `read_timeout` is 6 seconds
- Default `pool_timeout` is 1 second
- Network retry delay could be ~20-25s
- Library may be re-fetching "unacknowledged" updates

**Fix Strategy**:
1. Check library version: `pip show python-telegram-bot`
2. Update to latest: `pip install --upgrade python-telegram-bot`
3. Adjust polling parameters:
   ```python
   application.run_polling(
       allowed_updates=Update.ALL_TYPES,
       drop_pending_updates=True,  # Ignore old updates on startup
       timeout=10,                  # Increase timeout
       pool_timeout=2.0             # Increase pool timeout
   )
   ```
4. Implement persistent update_id tracking (survive restarts)

### If Duplicate is at Bridge Level

**Evidence**: Different update_ids but same trace_id

**Why 25 seconds?**
- Could be retry logic somewhere
- Could be async race condition with delay
- Could be response_timeout (10s) + something else (15s)

**Fix Strategy**:
1. Search for retry logic: `grep -r "retry\|sleep\|timeout" tools/prod/tg/`
2. Review async handlers for race conditions
3. Check if response_timeout causes re-injection
4. Add global message deduplication (SHA256 hash)

### If Duplicate is at tmux/Claude Code Level

**Evidence**: Single injection in log, duplicate appearance in Claude Code

**Why 25 seconds?**
- tmux key binding echoing input?
- Claude Code processing input twice?
- Terminal emulator issue?

**Fix Strategy**:
1. Check tmux config: `tmux show-options -g`
2. Test with bridge stopped (manual injection)
3. Check Claude Code logs for duplicate processing
4. Review terminal setup for input echo

---

## Validation Criteria

**Test is complete when**:
1. ✅ Root cause identified (Telegram API / Bridge / tmux / Claude Code)
2. ✅ Fix implemented in diagnostic version
3. ✅ 10+ test messages sent without duplicates
4. ✅ Trace log confirms single injection per update_id
5. ✅ Claude Code session shows single appearance

**Ready for production promotion when**:
1. ✅ 100+ messages processed without duplicates
2. ✅ 24-hour stability test passed
3. ✅ Fix code reviewed and understood
4. ✅ Production version updated with fix
5. ✅ Rollback procedure documented

---

## Rollback Procedure

**If diagnostic bridge makes things worse**:

```bash
# Stop diagnostic
ps aux | grep openai_telegram_bridge_diagnostic
kill <PID>

# Restart production
cd /home/corey/projects/AI-CIV/grow_openai
nohup python3 tools/prod/tg/openai_telegram_bridge.py >> /tmp/openai_telegram_bridge.log 2>&1 &

# Verify
ps aux | grep "tools/prod/tg/openai_telegram_bridge.py"
```

**Status**: Back to original state (duplicates present but functional)

---

## Next Steps After Diagnosis

1. **Document findings** in to-corey/DUPLICATE-FIX-REPORT.md
2. **Implement fix** in production version
3. **Test thoroughly** (100+ messages)
4. **Update bridge.md** with gotcha entry
5. **Add to memory** (duplicate prevention pattern)
6. **Share with A-C-Gee** (they may have same issue)

---

**Status**: Diagnostic tool ready for deployment
**Estimated diagnosis time**: 15-30 minutes with active testing
**Risk**: Low (diagnostic version is non-destructive, easy rollback)
