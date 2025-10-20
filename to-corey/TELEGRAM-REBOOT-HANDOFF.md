# Telegram Reboot Handoff - Production Ready

**Date**: 2025-10-20
**Status**: ⏳ PENDING VALIDATION (awaiting manual test execution)

---

## 🚨 IMPORTANT: Read Before Rebooting

This document will be finalized AFTER you complete the validation testing in:
**`TELEGRAM-REBOOT-VALIDATION-MANUAL.md`**

**DO NOT reboot until validation passes all tests.**

---

## Pre-Validation Status

### Current Working State

**Processes Running** (before validation):
- Monitor: [PID TBD] - `tools/prod/tg/openai_telegram_jsonl_monitor.py`
- Bridge: [PID TBD] - `tools/openai_telegram_bridge_diagnostic.py`

**Configuration**:
- tmux_session: "1" ✅ CONFIRMED CORRECT
- Bot token: 8483528605:AAHtw5... (Team 1) ✅ CONFIRMED CORRECT
- Authorized user: 437939400 (Corey) ✅ CONFIRMED CORRECT

**Known Issues Resolved**:
- ✅ Duplicate injection bug (diagnostic bridge fix)
- ✅ tmux session mismatch (config updated)
- ✅ ACG collision (process naming convention)
- ✅ Production lock architecture implemented

---

## Post-Reboot Wake-Up Commands (Copy-Paste Ready)

### After WSL Reboot

**Execute these commands in order**:

```bash
# Navigate to project
cd /home/corey/projects/AI-CIV/grow_openai

# Start JSONL Monitor
nohup python3 tools/prod/tg/openai_telegram_jsonl_monitor.py >> /tmp/openai_telegram_jsonl_monitor.log 2>&1 &

# Start Diagnostic Bridge
nohup python3 tools/openai_telegram_bridge_diagnostic.py >> /tmp/openai_telegram_bridge_diagnostic.log 2>&1 &

# Wait for initialization
sleep 2

# Verify both processes started
ps aux | grep -E "openai_telegram" | grep -v grep
```

**Expected Output**:
```
corey    [PID1]  ... python3 tools/prod/tg/openai_telegram_jsonl_monitor.py
corey    [PID2]  ... python3 tools/openai_telegram_bridge_diagnostic.py
```

You should see exactly 2 processes.

---

## Post-Reboot Testing (Quick Smoke Test)

### Test 1: Basic Message Injection

1. Send via Telegram to Team 1 bot:
   ```
   Post-reboot test
   ```

2. Verify in Claude Code:
   - Appears ONCE
   - Appears within 2-3 seconds
   - No duplicate after 30 seconds

**✅ Pass**: Message appears once, no duplicates

### Test 2: Response Delivery

1. Send wrapped message in Claude Code:
   ```
   🤖🎯📱
   Post-reboot response test
   ✨🔚
   ```

2. Check Telegram:
   - Appears within 5 seconds
   - Appears ONCE
   - Correct content

**✅ Pass**: Response delivered successfully

### If Both Tests Pass

**Infrastructure is operational.** Continue normal work.

### If Any Test Fails

**Check logs immediately**:

```bash
# Recent activity
tail -20 /tmp/openai_telegram_bridge_diagnostic.log
tail -20 /tmp/openai_telegram_jsonl_monitor.log

# Look for errors
tail -20 /tmp/openai_telegram_jsonl_monitor_error.log
```

**Restart if needed**:
```bash
pkill -f openai_telegram_bridge_diagnostic
pkill -f openai_telegram_jsonl_monitor
# Then re-run wake-up commands above
```

---

## Troubleshooting Reference

### Issue: No Processes Running After Wake-Up

**Symptom**: `ps aux | grep openai_telegram` shows nothing

**Diagnosis**:
```bash
# Check logs for startup errors
tail -50 /tmp/openai_telegram_jsonl_monitor.log
tail -50 /tmp/openai_telegram_bridge_diagnostic.log
```

**Common Causes**:
1. Python syntax error (check log for traceback)
2. Missing dependencies (check for ImportError)
3. Config file missing/corrupted
4. Permission issues

**Fix**:
1. Identify error from logs
2. Fix root cause
3. Re-run wake-up commands

### Issue: Messages Not Appearing in Claude Code

**Symptom**: Telegram messages sent, but don't appear in session

**Diagnosis**:
```bash
# Check bridge is running
ps aux | grep openai_telegram_bridge_diagnostic

# Check bridge log
tail -30 /tmp/openai_telegram_bridge_diagnostic.log | grep -A 5 "Received message"
```

**Common Causes**:
1. Bridge process crashed (restart it)
2. Wrong tmux session in config (verify config/telegram_config.json)
3. Network issue (check internet connection)
4. Bot token invalid (verify token in config)

**Fix**:
```bash
# Restart bridge
pkill -f openai_telegram_bridge_diagnostic
nohup python3 tools/openai_telegram_bridge_diagnostic.py >> /tmp/openai_telegram_bridge_diagnostic.log 2>&1 &

# Verify tmux session
cat config/telegram_config.json | grep tmux_session
# Should show: "tmux_session": "1"
```

### Issue: Responses Not Reaching Telegram

**Symptom**: Wrapped messages in Claude Code, but don't appear on Telegram

**Diagnosis**:
```bash
# Check monitor is running
ps aux | grep openai_telegram_jsonl_monitor

# Check monitor log
tail -30 /tmp/openai_telegram_jsonl_monitor.log
```

**Common Causes**:
1. Monitor process crashed (restart it)
2. JSONL file not found (check project slug)
3. Wrapper markers malformed (check emoji exactly)
4. Send script failing (check error log)

**Fix**:
```bash
# Restart monitor
pkill -f openai_telegram_jsonl_monitor
nohup python3 tools/prod/tg/openai_telegram_jsonl_monitor.py >> /tmp/openai_telegram_jsonl_monitor.log 2>&1 &

# Check JSONL file detection
tail -5 /tmp/openai_telegram_jsonl_monitor.log | grep "Monitoring JSONL"
```

### Issue: Duplicate Messages (Regression)

**Symptom**: Messages appear twice (immediate + delayed)

**This should NOT happen** - diagnostic bridge is fixed.

**If it does happen**:
1. **STOP IMMEDIATELY** - critical regression
2. Capture logs:
   ```bash
   cp /tmp/openai_telegram_bridge_diagnostic.log /tmp/duplicate_regression_$(date +%Y%m%d_%H%M%S).log
   ```
3. Report to tg-bridge agent with logs
4. Revert to known-good version if critical

---

## Validation Results (To Be Filled After Testing)

**Validation Date**: [YYYY-MM-DD]
**Tester**: Corey

### Test Results

| Test | Status | Notes |
|------|--------|-------|
| Clean shutdown | ⏳ PENDING | Team 1 stopped, ACG preserved |
| Wake-up execution | ⏳ PENDING | Both processes started |
| Basic injection | ⏳ PENDING | Single message, no duplicates |
| Response delivery | ⏳ PENDING | Wrapped message to Telegram |
| Rapid messages | ⏳ PENDING | 3 messages, no duplicates |

### Overall Status

**Validation Result**: ⏳ AWAITING EXECUTION

**Ready for Reboot**: [YES/NO - mark after validation]

**Issues Found**: [COUNT]

**Fixes Applied**: [LIST]

---

## Quick Command Reference

### Check Status
```bash
ps aux | grep openai_telegram | grep -v grep
```

### View Logs (Live)
```bash
tail -f /tmp/openai_telegram_bridge_diagnostic.log
tail -f /tmp/openai_telegram_jsonl_monitor.log
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

## After Successful Reboot

### Immediate Actions

1. **Verify infrastructure health** (run smoke tests above)
2. **Monitor for 5 minutes** (watch for any issues)
3. **Update this document** with actual PIDs and results
4. **Archive validation logs** for reference

### First Session Tasks

1. Invoke tg-bridge for health check
2. Report reboot success
3. Update documentation with any learnings
4. Consider systemd service if manual start gets tedious

---

## Notes for Future Reboots

**This procedure is validated and safe to repeat.**

**Timing**: ~2 minutes total
- Shutdown: 10 seconds
- Wake-up: 30 seconds
- Verification: 30 seconds
- Testing: 60 seconds

**Frequency**: As needed (system reboots, updates, maintenance)

**Automation Potential**: Could be converted to systemd service for auto-start

---

**Status**: Document will be finalized after validation testing completes.

**Next Step**: Execute `TELEGRAM-REBOOT-VALIDATION-MANUAL.md` procedures.
