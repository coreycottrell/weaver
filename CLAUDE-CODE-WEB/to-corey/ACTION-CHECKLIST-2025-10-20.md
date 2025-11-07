# Action Checklist: Telegram Fix Handoff

**Date**: 2025-10-20
**From**: tg-bridge
**Status**: Ready for execution

---

## Immediate Actions (Primary or Corey)

### 1. Push Git Commit ⏳
```bash
cd /home/corey/projects/AI-CIV/grow_openai
git push origin master
```
**Why**: Commit `0c6863f` (17 files, 4,687 lines) needs remote backup
**Status**: Committed locally, NOT pushed to remote

---

### 2. Verify Process Health ⏳
```bash
ps aux | grep -E "openai_telegram" | grep -v grep
```
**Expected**: Two processes running
- `openai_telegram_bridge_diagnostic.py` (PID ~91727)
- `openai_telegram_jsonl_monitor.py` (PID ~92167)

**If processes down**: Follow wake-up procedure in `TELEGRAM-QUICK-REFERENCE.md`

---

### 3. Test Telegram (Optional) ⏳
Send message from Telegram bot to Corey's phone
**Expected**: Single injection to tmux, zero duplicates

---

## Session Actions (Primary)

### 4. Apply Agent Manifest Update ⏳
**File**: `to-corey/TG-BRIDGE-AGENT-UPDATED-2025-10-20.md`

**Location**: `.claude/agents/tg-bridge.md`

**Action**: Add "Recent Achievements" section before "Closing Wisdom"

**Why**: Documents tg-bridge's first major production fix

---

### 5. Update tg-bridge Manifest (Clarify Tools) ⏳
**Issue**: Manifest claims Bash tool, but tg-bridge doesn't have it

**Section**: "Tools & Delegation Pattern" → "Tools I Use"

**Change needed**:
- Remove "Bash" from available tools
- Add note: "Cannot execute commands - can only prepare documentation"
- Update examples to reflect actual capabilities

**Why**: Future sessions need accurate tool expectations

---

## Future Actions (30 Days)

### 6. Archive Diagnostic Files ⏳
**When**: After 2025-11-20 (30 days retention)

**Procedure**: `to-corey/ARCHIVE-MANIFEST-2025-10-20.md`

**Files to archive** (6 diagnostic files):
- DUPLICATE-MESSAGE-DIAGNOSTIC-READY.md
- TG-DUPLICATE-FINAL-DIAGNOSIS.md
- DUPLICATE-DIAGNOSTIC-PROCEDURE.md
- TELEGRAM-DUPLICATE-QUICKSTART.md
- deploy_diagnostic_bridge.sh
- check_telegram_health.sh

**Keep** (9 production files):
- TELEGRAM-WAKEUP-PROCEDURE.md
- TELEGRAM-QUICK-REFERENCE.md
- TELEGRAM-REBOOT-HANDOFF.md
- TELEGRAM-PRODUCTION-STATUS.md
- TELEGRAM-ISSUE-RESOLVED.md
- SESSION-SUMMARY-2025-10-20-TELEGRAM-FIX.md
- HANDOFF-FINAL-2025-10-20.md
- TG-BRIDGE-FINAL-STATUS.md
- ACTION-CHECKLIST-2025-10-20.md

---

## Post-Reboot Actions (Corey)

### 7. Restart Telegram Infrastructure
**Guide**: `to-corey/TELEGRAM-QUICK-REFERENCE.md`

**Three commands**:
```bash
# 1. Start bridge
cd /home/corey/projects/AI-CIV/grow_openai
nohup python3 tools/openai_telegram_bridge_diagnostic.py > /tmp/openai_telegram_bridge_diagnostic.log 2>&1 &

# 2. Start monitor
nohup python3 tools/openai_telegram_jsonl_monitor.py > /tmp/openai_telegram_jsonl_monitor.log 2>&1 &

# 3. Verify
ps aux | grep -E "openai_telegram" | grep -v grep
```

---

### 8. Verify Zero Duplicates
Send test message from Telegram
**Expected**: Single injection, no duplicates

**If duplicates occur**: Check logs
```bash
tail -20 /tmp/openai_telegram_bridge_diagnostic.log
```

---

## Documentation Reference

**Quick Start**: `TELEGRAM-QUICK-REFERENCE.md` (essential commands)
**Complete Context**: `TELEGRAM-REBOOT-HANDOFF.md` (full history)
**Session Summary**: `SESSION-SUMMARY-2025-10-20-TELEGRAM-FIX.md` (comprehensive)
**Final Status**: `TG-BRIDGE-FINAL-STATUS.md` (tool limitations, achievements)
**This Checklist**: `ACTION-CHECKLIST-2025-10-20.md` (you are here)

---

## Status Summary

| Task | Status | Owner | Urgency |
|------|--------|-------|---------|
| Push git commit | ⏳ PENDING | Primary/Corey | High |
| Verify processes | ⏳ PENDING | Primary/Corey | Medium |
| Test Telegram | ⏳ PENDING | Corey | Low |
| Apply manifest update | ⏳ PENDING | Primary | Medium |
| Update tool limitations | ⏳ PENDING | Primary | Low |
| Archive diagnostics | ⏳ PENDING | Anyone | Low (30 days) |
| Restart post-reboot | ⏳ PENDING | Corey | High (after reboot) |
| Verify zero duplicates | ⏳ PENDING | Corey | High (after reboot) |

---

## Success Criteria

✅ **Complete** when:
1. Git pushed to remote
2. Processes verified running (or restarted post-reboot)
3. Zero duplicates confirmed via test
4. Agent manifest updated
5. Tool limitations documented

---

## Questions or Issues?

**Documentation**: Start with `TELEGRAM-QUICK-REFERENCE.md`
**Technical Issues**: Check logs in `/tmp/openai_telegram_*.log`
**Root Cause Reference**: `TELEGRAM-ISSUE-RESOLVED.md`
**Complete History**: `TELEGRAM-REBOOT-HANDOFF.md`

---

**END ACTION CHECKLIST**

**Total actions**: 8
**Immediate**: 3
**Session**: 2
**Future**: 1
**Post-reboot**: 2

**Ready for execution. 🚀**
