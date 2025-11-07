# Telegram Reboot Validation - Manual Testing Guide

**Date**: 2025-10-20
**Agent**: tg-bridge
**Status**: 🚨 MANUAL EXECUTION REQUIRED (tg-bridge lacks bash tool access)

---

## ⚠️ Important Note

tg-bridge cannot execute bash commands directly in this session. This document provides the complete procedure for **you to execute manually**.

This is the dress rehearsal for a real reboot. Follow these steps exactly to validate the wake-up procedure.

---

## Phase 1: Clean Shutdown (Simulate Reboot)

### Step 1: Verify Current State

```bash
cd /home/corey/projects/AI-CIV/grow_openai

# Check ALL Telegram processes
ps aux | grep -E "openai_telegram|ACG_telegram" | grep -v grep
```

**Expected**:
- 2 Team 1 processes (bridge + monitor)
- 2 ACG processes (PIDs 4498, 4528)

**Document PIDs** - write them down:
- Team 1 Bridge PID: ________
- Team 1 Monitor PID: ________
- ACG Process 1 PID: 4498 (should not change)
- ACG Process 2 PID: 4528 (should not change)

### Step 2: Stop Team 1 Processes ONLY

```bash
# Kill diagnostic bridge
pkill -f openai_telegram_bridge_diagnostic

# Kill JSONL monitor
pkill -f openai_telegram_jsonl_monitor

# Wait for clean shutdown
sleep 2
```

### Step 3: Verify Team 1 Stopped, ACG Still Running

```bash
# Should show NOTHING for Team 1
ps aux | grep openai_telegram | grep -v grep

# Should still show ACG (PIDs 4498, 4528)
ps aux | grep ACG_telegram | grep -v grep
```

**✅ Pass Criteria**:
- Zero Team 1 processes
- Both ACG processes still running
- No errors in terminal

**❌ If ACG processes stopped**: You accidentally killed them - restart ACG infrastructure

---

## Phase 2: Wake-Up Using Documented Procedure

### Step 1: Start JSONL Monitor

```bash
cd /home/corey/projects/AI-CIV/grow_openai

nohup python3 tools/prod/tg/openai_telegram_jsonl_monitor.py >> /tmp/openai_telegram_jsonl_monitor.log 2>&1 &

echo "Monitor started - PID: $!"
```

**Note the PID**: ________

### Step 2: Start Diagnostic Bridge

```bash
nohup python3 tools/openai_telegram_bridge_diagnostic.py >> /tmp/openai_telegram_bridge_diagnostic.log 2>&1 &

echo "Bridge started - PID: $!"
```

**Note the PID**: ________

### Step 3: Wait for Initialization

```bash
sleep 2
```

### Step 4: Verify Both Processes Running

```bash
ps aux | grep -E "openai_telegram" | grep -v grep
```

**Expected output**:
```
corey    [PID1]  ... python3 tools/prod/tg/openai_telegram_jsonl_monitor.py
corey    [PID2]  ... python3 tools/openai_telegram_bridge_diagnostic.py
```

**✅ Pass Criteria**:
- 2 processes running
- Correct script paths
- PIDs are NEW (different from Phase 1)

### Step 5: Check Logs for Clean Startup

```bash
# Monitor log (should show initialization)
tail -20 /tmp/openai_telegram_jsonl_monitor.log

# Bridge log (should show "Telegram bridge started")
tail -20 /tmp/openai_telegram_bridge_diagnostic.log
```

**✅ Pass Criteria**:
- No errors in either log
- Monitor shows "Polling for new content"
- Bridge shows "Telegram bridge started successfully"

---

## Phase 3: Functional Testing

### Test 1: Basic Injection (Single Message)

**Objective**: Verify message appears once, no delayed duplicates

#### Step 1: Send Test Message via Telegram

Send to Team 1 bot:
```
Reboot test 1
```

#### Step 2: Verify Immediate Injection

Check Claude Code session - message should appear ONCE immediately.

**Timestamp received**: __:__:__

#### Step 3: Monitor for Delayed Duplicates

Wait **35 seconds** (past the delayed duplicate window).

**Timestamp at 35s**: __:__:__

**✅ Pass Criteria**:
- Message appears ONCE in Claude Code
- Appears within 2-3 seconds of sending
- NO duplicate after 35 seconds

**❌ Failure modes**:
- Message appears twice → Duplicate injection bug
- Message delayed >10 seconds → Polling issue
- Message doesn't appear → Bridge broken

#### Step 4: Check Diagnostic Log

```bash
tail -30 /tmp/openai_telegram_bridge_diagnostic.log | grep -A 5 "Reboot test 1"
```

**Look for**:
- Exactly ONE message receipt
- Successful tmux injection
- Correct pane ("1:0.0")
- No errors

### Test 2: Response Delivery (Outbound)

**Objective**: Verify wrapped responses reach Telegram once

#### Step 1: Send Wrapped Response in Claude Code

Type in this session:

```
🤖🎯📱
Reboot test response - bridge operational
✨🔚
```

#### Step 2: Wait for Monitor Detection

**Monitor polls every 3 seconds** - wait up to 5 seconds.

**Timestamp sent in Claude Code**: __:__:__
**Timestamp received on Telegram**: __:__:__
**Delay**: ______ seconds

#### Step 3: Verify Single Delivery

Check Telegram - message should appear ONCE.

**✅ Pass Criteria**:
- Message appears on Telegram
- Appears within 5 seconds
- Appears exactly ONCE (no duplicates)

**❌ Failure modes**:
- Doesn't appear → Monitor not detecting
- Appears twice → Duplicate send bug
- Delayed >10 seconds → Monitor polling issue

#### Step 4: Check Monitor Log

```bash
tail -30 /tmp/openai_telegram_jsonl_monitor.log | grep -B 5 -A 5 "Reboot test response"
```

**Look for**:
- Message detection from JSONL
- SHA256 hash recorded
- Successful send
- No duplicate hash detection

### Test 3: Rapid Message Handling (Stress Test)

**Objective**: Verify no duplicates under rapid fire

#### Step 1: Send 3 Messages Rapid-Fire via Telegram

Send these as fast as you can type:
```
Rapid 1
Rapid 2
Rapid 3
```

**Send timestamps**:
- Rapid 1: __:__:__
- Rapid 2: __:__:__
- Rapid 3: __:__:__

#### Step 2: Verify All 3 Appear ONCE in Claude Code

**✅ Pass Criteria**:
- All 3 messages appear
- Each appears exactly ONCE
- Order preserved (1, 2, 3)
- All within 5 seconds of sending

#### Step 3: Wait for Delayed Duplicate Window

Wait **35 seconds** from last message.

**✅ Pass Criteria**:
- No duplicates after 35 seconds
- Message count remains at 3 total

#### Step 4: Check Diagnostic Log

```bash
tail -50 /tmp/openai_telegram_bridge_diagnostic.log | grep -E "Rapid [1-3]"
```

**Expected**: Exactly 3 message receipts (one per message)

**❌ Failure modes**:
- More than 3 receipts → Duplicate injections
- Messages out of order → Race condition
- Messages missing → Polling miss

---

## Phase 4: Issue Documentation

### If ALL Tests Pass ✅

**Record final state**:

```bash
# Capture process list
ps aux | grep openai_telegram | grep -v grep > /tmp/reboot_validation_processes.txt

# Capture log tails
tail -50 /tmp/openai_telegram_bridge_diagnostic.log > /tmp/reboot_validation_bridge.txt
tail -50 /tmp/openai_telegram_jsonl_monitor.log > /tmp/reboot_validation_monitor.txt

# Archive as proof
tar -czf reboot_validation_success_$(date +%Y%m%d_%H%M%S).tar.gz \
  /tmp/reboot_validation_*.txt
```

**Result**: ✅ VALIDATED - Ready for real reboot

### If ANY Test Fails ❌

**Document failure exactly**:

1. **Which test failed**: ___________________
2. **Failure mode**: ___________________
3. **Error logs**:

```bash
# Full logs
cat /tmp/openai_telegram_bridge_diagnostic.log > failure_bridge_log.txt
cat /tmp/openai_telegram_jsonl_monitor.log > failure_monitor_log.txt
cat /tmp/openai_telegram_jsonl_monitor_error.log > failure_error_log.txt
```

4. **Root cause hypothesis**: ___________________
5. **Fix needed**: ___________________

**Action**: DO NOT proceed with real reboot until issues fixed.

---

## Phase 5: Results Summary

### Test Results Matrix

| Test | Status | Time | Duplicates | Notes |
|------|--------|------|------------|-------|
| Basic Injection | ✅/❌ | __s | Yes/No | _________ |
| Response Delivery | ✅/❌ | __s | Yes/No | _________ |
| Rapid Handling | ✅/❌ | __s | Yes/No | _________ |

### Process Status After Testing

```bash
ps aux | grep openai_telegram | grep -v grep
```

**Final PIDs**:
- Monitor: ________ (should match Phase 2 PID)
- Bridge: ________ (should match Phase 2 PID)

**Uptime**: ________ minutes (time since Phase 2 restart)

### Overall Assessment

**Status**: [✅ READY FOR REBOOT / ⚠️ NEEDS FIXES / ❌ CRITICAL ISSUES]

**Confidence Level**: [HIGH / MEDIUM / LOW]

**Issues Found**: [COUNT - list below]

1. ___________________
2. ___________________
3. ___________________

**Required Fixes Before Real Reboot**:

- [ ] Fix issue 1: ___________________
- [ ] Fix issue 2: ___________________
- [ ] Fix issue 3: ___________________
- [ ] Re-run validation after fixes

---

## Next Steps

### If Validation Passed ✅

You can safely perform a real reboot using the exact same procedure:

1. **Reboot WSL**:
   ```bash
   # From Windows PowerShell
   wsl --shutdown
   wsl
   ```

2. **After reboot, execute wake-up**:
   ```bash
   cd /home/corey/projects/AI-CIV/grow_openai
   nohup python3 tools/prod/tg/openai_telegram_jsonl_monitor.py >> /tmp/openai_telegram_jsonl_monitor.log 2>&1 &
   nohup python3 tools/openai_telegram_bridge_diagnostic.py >> /tmp/openai_telegram_bridge_diagnostic.log 2>&1 &
   sleep 2
   ps aux | grep openai_telegram | grep -v grep
   ```

3. **Test with simple message**: "Post-reboot test"

### If Validation Failed ❌

**DO NOT REBOOT** until issues are resolved.

1. Report findings to tg-bridge agent
2. Diagnose root causes
3. Implement fixes
4. Re-run this validation
5. Repeat until all tests pass

---

## Quick Command Reference

### Check Status
```bash
ps aux | grep openai_telegram | grep -v grep
```

### View Logs
```bash
tail -f /tmp/openai_telegram_bridge_diagnostic.log
tail -f /tmp/openai_telegram_jsonl_monitor.log
tail -f /tmp/openai_telegram_jsonl_monitor_error.log
```

### Restart Infrastructure
```bash
cd /home/corey/projects/AI-CIV/grow_openai
pkill -f openai_telegram_bridge_diagnostic
pkill -f openai_telegram_jsonl_monitor
nohup python3 tools/prod/tg/openai_telegram_jsonl_monitor.py >> /tmp/openai_telegram_jsonl_monitor.log 2>&1 &
nohup python3 tools/openai_telegram_bridge_diagnostic.py >> /tmp/openai_telegram_bridge_diagnostic.log 2>&1 &
sleep 2
ps aux | grep openai_telegram | grep -v grep
```

### Emergency Stop
```bash
pkill -f openai_telegram
```

---

## Documentation to Update After Validation

If validation passes, update these docs:

1. **TELEGRAM-WAKEUP-PROCEDURE.md**:
   - Mark as "✅ VALIDATED 2025-10-20"
   - Add validation test results

2. **tg-bridge.md** (agent manifest):
   - Update health check section with validated timing
   - Document any edge cases discovered

3. **PRODUCTION-LOCK-STATUS.md**:
   - Mark diagnostic bridge as validated production
   - Update status from EXPERIMENTAL to PRODUCTION

4. **Create TELEGRAM-REBOOT-HANDOFF.md**:
   - Summary for Corey
   - Copy-paste ready commands
   - Expected results
   - Troubleshooting quick reference

---

## Validation Checklist

Before marking as complete:

- [ ] Phase 1: Clean shutdown executed
- [ ] Phase 1: Team 1 stopped, ACG still running
- [ ] Phase 2: Wake-up procedure executed
- [ ] Phase 2: Both processes started successfully
- [ ] Phase 2: Logs show clean initialization
- [ ] Test 1: Basic injection - PASS
- [ ] Test 1: No delayed duplicates - PASS
- [ ] Test 2: Response delivery - PASS
- [ ] Test 2: Single delivery confirmed - PASS
- [ ] Test 3: Rapid messages all appear - PASS
- [ ] Test 3: No duplicates after 35s - PASS
- [ ] Results documented in this file
- [ ] Logs archived for reference
- [ ] Documentation updates identified
- [ ] Handoff document created (if passed)

---

**Execute this validation before attempting real reboot.**

**If all tests pass → Ready for production reboot**
**If any test fails → Fix and re-validate**

Good luck! 📱
