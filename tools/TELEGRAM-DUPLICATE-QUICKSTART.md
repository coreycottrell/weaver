# Telegram Duplicate Diagnostic - Quick Start Card

**Problem**: Messages appear twice in Claude Code with ~25s delay
**Solution**: Diagnostic bridge with trace IDs
**Time**: 15-30 minutes
**Risk**: LOW (easy rollback)

---

## Deploy (Pick One)

**Option A - Automated** (Recommended)
```bash
cd /home/corey/projects/AI-CIV/grow_openai
bash tools/deploy_diagnostic_bridge.sh
```

**Option B - Manual**
```bash
# Stop production
ps aux | grep "tools/prod/tg/openai_telegram_bridge.py" | awk '{print $2}' | xargs kill

# Start diagnostic
cd /home/corey/projects/AI-CIV/grow_openai
nohup python3 tools/openai_telegram_bridge_diagnostic.py >> /tmp/openai_telegram_bridge_diagnostic.log 2>&1 &
```

---

## Test

**Terminal 1**: Watch log
```bash
tail -f /tmp/openai_telegram_bridge_diagnostic.log
```

**Terminal 2 (Telegram)**: Send messages
```
Test 1
[wait 30s]
Test 2
[wait 30s]
/status
```

---

## What to Look For

**✅ Good (No Duplicates)**:
```
📨 MESSAGE RECEIVED
✓ Injection successful
```

**⚠️ Duplicate Detected (Telegram API)**:
```
📨 MESSAGE RECEIVED (update: 100500)
[25s later]
⚠️ DUPLICATE UPDATE_ID DETECTED!
```

**❌ Duplicate Detected (Bridge)**:
```
🔍 INJECTION ATTEMPT (trace: abc-123)
[25s later]
⚠️ DUPLICATE INJECTION ATTEMPT!
```

---

## Rollback (If Needed)

```bash
# Stop diagnostic
ps aux | grep diagnostic | awk '{print $2}' | xargs kill

# Restart production
cd /home/corey/projects/AI-CIV/grow_openai
./tools/prod/tg/start_telegram_infrastructure.sh
```

---

## Full Documentation

- **User Guide**: `to-corey/DUPLICATE-MESSAGE-DIAGNOSTIC-READY.md`
- **Testing Protocol**: `tools/DUPLICATE-DIAGNOSTIC-PROCEDURE.md`
- **Session Summary**: `to-corey/TG-BRIDGE-SESSION-COMPLETE.md`
- **Health Check**: `bash tools/check_telegram_health.sh`

---

## Expected Result

**After 5-10 test messages**: Root cause identified (Telegram API vs Bridge vs tmux)

**After fix implemented**: No more duplicates, messages appear once

**Total time**: 30-60 minutes (deploy + test + fix + validate)

---

**Questions?** Invoke tg-bridge or check comprehensive docs above.
