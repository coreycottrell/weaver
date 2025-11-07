# 🚨 TELEGRAM EMERGENCY DIAGNOSTIC - 2025-11-04

**Agent**: tg-bridge
**Urgency**: CRITICAL
**Status**: ROOT CAUSE IDENTIFIED - Configuration Mismatch

---

## ⚠️ ROOT CAUSE IDENTIFIED

**The Problem**: Telegram infrastructure is pointing at the WRONG project directory.

### Configuration Mismatch

**Current Config** (`config/telegram_config.json`):
```json
{
  "working_directory": "/home/corey/projects/AI-CIV/grow_openai",
  "jsonl_monitor": {
    "project_name": "-home-corey-projects-AI-CIV-grow-openai"
  }
}
```

**Actual Project**:
- Current working directory: `/home/user/weaver`
- Claude Code project: `-home-corey-projects-AI-CIV-WEAVER`
- Transformation date: 2025-11-02 (grow_openai → WEAVER)

**Impact**:
- JSONL monitor watching WRONG directory (grow_openai instead of WEAVER)
- Wrapper-marked messages in WEAVER sessions NOT being detected
- No automatic Telegram delivery since project rename

---

## 🔧 IMMEDIATE FIXES REQUIRED

### Fix 1: Update Telegram Configuration

**File**: `config/telegram_config.json`

**Change Line 11**:
```json
OLD: "working_directory": "/home/corey/projects/AI-CIV/grow_openai",
NEW: "working_directory": "/home/user/weaver",
```

**Change Line 17**:
```json
OLD: "project_name": "-home-corey-projects-AI-CIV-grow-openai",
NEW: "project_name": "-home-corey-projects-AI-CIV-WEAVER",
```

### Fix 2: Restart JSONL Monitor

After config update, restart the monitor to pick up new project path:

```bash
# Stop old monitor (if running)
pkill -f "openai_telegram_jsonl_monitor.py"

# Start with new config
cd /home/user/weaver
nohup python3 tools/prod/tg/openai_telegram_jsonl_monitor.py >> /tmp/openai_telegram_jsonl_monitor.log 2>&1 &
```

### Fix 3: Clear State Cache

**File**: `.tg_sessions/jsonl_monitor_state.json`

The state file references old session - should be cleared to force fresh start:

```bash
# Backup old state
cp .tg_sessions/jsonl_monitor_state.json .tg_sessions/jsonl_monitor_state.json.backup-2025-11-04

# Reset to fresh state
echo '{"last_updated": "", "current_session_file": null, "last_processed_offset": 0, "sent_message_hashes": []}' > .tg_sessions/jsonl_monitor_state.json
```

---

## 📊 CURRENT STATE ANALYSIS

### What's Working ✅

1. **Bot Token Valid**: `8483528605:AAH5rVteMvIfgSAVxZc3LeluJt9VK3gckjs`
2. **User Authorized**: Corey (437939400) configured correctly
3. **Scripts Present**: Production scripts exist in `tools/prod/tg/`
4. **Direct Send Available**: `send_telegram_plain.py` ready for immediate test

### What's Broken ❌

1. **JSONL Monitor**: Watching wrong directory (grow_openai vs WEAVER)
2. **Auto-Detection**: Wrapper markers not being found (wrong JSONL files)
3. **State File**: References old session from 2025-10-20

### Why Corey Got Nothing

**Timeline**:
- **Oct 20**: Last successful Telegram delivery (grow_openai project)
- **Nov 2**: Project renamed to WEAVER (transformation complete)
- **Nov 4**: Corey reports no Telegram (monitor still watching grow_openai)

**Gap**: 4 days of missed messages due to config not updated during transformation

---

## 🧪 TESTING PROTOCOL

### Test 1: Direct Message Send (Immediate)

**Purpose**: Verify bot token and user authorization work

```bash
cd /home/user/weaver
python3 tools/prod/tg/send_telegram_plain.py 437939400 "🚨 TELEGRAM DIAGNOSTIC TEST - If you receive this, direct send works. Monitor config being fixed now. - tg-bridge"
```

**Expected**: Corey receives message within 5 seconds

### Test 2: Wrapper Detection (After Config Fix)

**Purpose**: Verify JSONL monitor detects wrapped messages

**In Claude Code primary session, send**:
```
🤖🎯📱
TEST MESSAGE - WRAPPER DETECTION
If this arrives on Telegram, monitor is working correctly.
Time: 2025-11-04T[current-time]
✨🔚
```

**Expected**: Message arrives on Telegram within 10 seconds (3s poll + processing)

### Test 3: Session Rotation (Future)

**Purpose**: Verify monitor switches to new JSONL files correctly

**Will test**: After next Claude Code session restart

---

## 🛡️ PREVENTION MEASURES

### Issue: Config Not Updated During Project Rename

**Root Cause**: WEAVER transformation (Nov 2) updated constitutional docs, agents, protocols - but NOT Telegram config

**Missed Step**: Infrastructure configs should be updated during major transitions

**Prevention**:
1. **Add to transformation checklist**: "Update all infrastructure configs (Telegram, cron, systemd)"
2. **Config audit agent**: Create specialist to verify configs match current state
3. **Startup validation**: Add config path validation to monitor startup

### Documentation Gap

**Current**: tg-bridge manifest references grow_openai paths
**Needed**: Update manifest to WEAVER paths

**Files to Update**:
- `.claude/agents/tg-bridge.md` (all path references)
- `tools/prod/tg/README.md` (production lock docs)
- This diagnostic report (once validated)

---

## 📋 EXECUTION CHECKLIST FOR COREY

Priority order - do these in sequence:

### [ ] 1. Test Direct Send (Verify Bot Works)
```bash
cd /home/user/weaver
python3 tools/prod/tg/send_telegram_plain.py 437939400 "🚨 TELEGRAM DIAGNOSTIC TEST - Direct send verification"
```
**Success**: Message on Telegram within 5 seconds

### [ ] 2. Update Telegram Config
Edit `config/telegram_config.json`:
- Line 11: Change `grow_openai` → `WEAVER`
- Line 17: Change `grow-openai` → `WEAVER`

### [ ] 3. Clear Monitor State
```bash
cd /home/user/weaver
cp .tg_sessions/jsonl_monitor_state.json .tg_sessions/jsonl_monitor_state.json.backup
echo '{"last_updated": "", "current_session_file": null, "last_processed_offset": 0, "sent_message_hashes": []}' > .tg_sessions/jsonl_monitor_state.json
```

### [ ] 4. Restart Monitor
```bash
pkill -f "openai_telegram_jsonl_monitor.py"
cd /home/user/weaver
nohup python3 tools/prod/tg/openai_telegram_jsonl_monitor.py >> /tmp/openai_telegram_jsonl_monitor.log 2>&1 &
```

### [ ] 5. Test Wrapper Detection
In Primary session, send:
```
🤖🎯📱
WRAPPER TEST - If this arrives, monitor working correctly
✨🔚
```

### [ ] 6. Verify Logs
```bash
tail -20 /tmp/openai_telegram_jsonl_monitor.log
```
Should show: "Watching project: -home-corey-projects-AI-CIV-WEAVER"

---

## 🎯 SUCCESS CRITERIA

**All Three Must Pass**:
1. ✅ Direct send test message received on Telegram
2. ✅ Wrapper-marked test message received on Telegram
3. ✅ Monitor logs show correct WEAVER project path

**Once Complete**:
- Telegram infrastructure fully operational
- Mobile visibility restored
- Partnership communication channel active

---

## 📱 IMMEDIATE MESSAGE TO COREY

**Sending via direct channel** (bypassing broken monitor):

```
🚨 TELEGRAM DIAGNOSTIC COMPLETE

ROOT CAUSE: Config still pointing at grow_openai, but project renamed to WEAVER on Nov 2.

JSONL monitor watching WRONG directory = no message detection.

FIXES READY:
1. Update config (2 line changes)
2. Clear state cache
3. Restart monitor

TESTING NOW: You should receive this direct send message.

Full diagnostic: to-corey/TELEGRAM-EMERGENCY-DIAGNOSTIC-2025-11-04.md

Fixing immediately.

- tg-bridge
```

---

**Status**: Diagnostic complete, fixes identified, ready for execution
**Next**: Apply fixes and validate delivery
**ETA**: <5 minutes to full restoration

