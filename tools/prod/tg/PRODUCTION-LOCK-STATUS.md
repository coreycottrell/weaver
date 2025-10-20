# Telegram Production Lock Status

**Last Updated**: 2025-10-20
**Status**: ✅ LOCKED (working files protected)

---

## 🔒 Production Lock Architecture

This document tracks the production lock status of all Telegram infrastructure files.

### Why Production Lock Exists

**Problem**: Multiple collisions and accidental overwrites
- Duplicate message bugs (fixed 2025-10-20)
- ACG process name collisions (fixed 2025-10-20)
- Agents modifying working files (prevented by lock)

**Solution**: Spatial isolation + file protection
- Production files in `tools/prod/tg/` (protected)
- Working bridge at `tools/openai_telegram_bridge_diagnostic.py` (protected)
- Archive for broken versions (`tools/.archive/telegram-cleanup-2025-10-20/`)
- Modification requires explicit variant creation (v2, v3, etc.)

---

## 🔒 Protected Files (Production Lock ACTIVE)

### Core Infrastructure

#### 1. Bridge (Team 1 Primary)
**File**: `tools/openai_telegram_bridge_diagnostic.py`
**Status**: 🔒 LOCKED ✅ WORKING
**Lock Date**: 2025-10-20
**Validation**: Zero duplicates confirmed
**Features**:
- Update ID deduplication ✅
- Injection locking ✅
- Trace ID logging ✅

**Protection Header**: YES (added 2025-10-20)

**To modify**:
```bash
# Create variant
cp tools/openai_telegram_bridge_diagnostic.py tools/openai_telegram_bridge_v2.py

# Test thoroughly
python3 tools/openai_telegram_bridge_v2.py

# Get Corey approval before replacing production
```

---

#### 2. JSONL Monitor (Team 1 Primary)
**File**: `tools/prod/tg/openai_telegram_jsonl_monitor.py`
**Status**: 🔒 LOCKED ✅ WORKING
**Lock Date**: 2025-10-20 (created with lock)
**Validation**: Sends responses reliably
**Features**:
- Delta detection (file offset tracking) ✅
- SHA256 deduplication ✅
- Session rotation handling ✅

**Protection Header**: YES (original creation)

**To modify**:
```bash
# Create variant
cp tools/prod/tg/openai_telegram_jsonl_monitor.py tools/openai_telegram_jsonl_monitor_v2.py

# Test in isolation
python3 tools/openai_telegram_jsonl_monitor_v2.py

# Get approval before replacing
```

---

#### 3. Plain Text Sender
**File**: `tools/prod/tg/send_telegram_plain.py`
**Status**: 🔒 LOCKED ✅ WORKING
**Lock Date**: 2025-10-20 (created with lock)
**Validation**: Never fails on special chars

**Protection Header**: YES

---

#### 4. Markdown Sender
**File**: `tools/prod/tg/send_telegram_direct.py`
**Status**: 🔒 LOCKED ✅ WORKING
**Lock Date**: 2025-10-20 (created with lock)
**Validation**: Fallback to plain text works

**Protection Header**: YES

---

### Management Scripts

#### 5. Start Script
**File**: `tools/prod/tg/start_telegram_infrastructure.sh`
**Status**: 🔒 LOCKED (needs update - currently launches broken bridge)
**Lock Date**: 2025-10-20
**Issue**: Still references `tools/prod/tg/openai_telegram_bridge.py` (broken)
**Fix needed**: Update to launch diagnostic bridge

**Protection Header**: YES

---

#### 6. Stop Script
**File**: `tools/prod/tg/stop_telegram_infrastructure.sh`
**Status**: 🔒 LOCKED ✅ WORKING
**Lock Date**: 2025-10-20

**Protection Header**: YES

---

#### 7. Status Script
**File**: `tools/prod/tg/status_telegram_infrastructure.sh`
**Status**: 🔒 LOCKED (needs update - checks wrong bridge)
**Lock Date**: 2025-10-20
**Issue**: Checks for `openai_telegram_bridge.py`, should check diagnostic
**Fix needed**: Update process checks

**Protection Header**: YES

---

#### 8. README
**File**: `tools/prod/tg/README.md`
**Status**: 🔒 LOCKED (needs update - references broken bridge)
**Lock Date**: 2025-10-20
**Issue**: Documentation references old broken bridge
**Fix needed**: Update to reference diagnostic bridge

**Protection Header**: YES

---

## 📁 Configuration Files

### Telegram Config
**File**: `config/telegram_config.json`
**Status**: ✅ WORKING (not locked - configuration may need updates)
**Current Settings**:
- Session: "1" (Team 1 tmux session)
- Authorized user: 437939400 (Corey)
- Working directory: `/home/corey/projects/AI-CIV/grow_openai`

**Lock**: NO (configuration files need flexibility)

---

### State Files
**Directory**: `.tg_sessions/`
**Status**: ✅ WORKING (not locked - runtime state)
**Files**:
- `jsonl_monitor_state.json` - Monitor state (file offset, sent hashes)
- `437939400.json` - User session metadata

**Lock**: NO (runtime state must be writable)

---

## 🗄️ Archived Files

**Directory**: `tools/.archive/telegram-cleanup-2025-10-20/`

### Broken Production Bridge
**File**: `openai_telegram_bridge_broken.py`
**Original**: `tools/prod/tg/openai_telegram_bridge.py`
**Issue**: Missing update_id deduplication, causes duplicates
**Archived**: 2025-10-20

### Development Versions
**Files**:
- `openai_telegram_bridge_dev.py` - Old development version
- `openai_telegram_jsonl_monitor_dev.py` - Development monitor
- `telegram_monitor_tmux_obsolete.py` - Old tmux architecture
- `telegram_monitor_jsonl_dev.py` - Development version

**Archived**: 2025-10-20
**Safe to delete**: After 2025-11-20 (30 days)

---

## 🔓 Non-Locked Files (Development OK)

### Development Senders
**Files**:
- `tools/send_telegram_plain.py` - Development copy
- `tools/send_telegram_direct.py` - Development copy

**Status**: ⚠️ Duplicates of production, OK to modify for testing
**Note**: Production versions in `tools/prod/tg/`

### Documentation
**Files**:
- `tools/TELEGRAM-DUPLICATE-QUICKSTART.md`
- `tools/DUPLICATE-DIAGNOSTIC-PROCEDURE.md`
- `tools/check_telegram_health.sh`
- `tools/deploy_diagnostic_bridge.sh`
- `tools/test_monitor.sh`

**Status**: ⚠️ Documentation/helpers, OK to update

### Old Management Scripts
**Files**:
- `tools/start_telegram_infrastructure.sh` (superseded by prod/tg/)
- `tools/stop_telegram_infrastructure.sh` (superseded by prod/tg/)
- `tools/status_telegram_infrastructure.sh` (superseded by prod/tg/)

**Status**: ⚠️ Obsolete, should be archived

---

## 🔧 Modification Protocol

### For LOCKED Files

**NEVER modify production files directly.**

**Process**:
1. **Create variant**:
   ```bash
   cp tools/prod/tg/{file}.py tools/{file}_v2.py
   ```

2. **Develop in isolation**:
   - Test thoroughly
   - Validate zero regressions
   - Document changes

3. **Get approval**:
   - Corey approval required
   - Explain what changed and why
   - Demonstrate testing results

4. **Promote to production**:
   ```bash
   # Archive old version
   mv tools/prod/tg/{file}.py tools/.archive/{file}_replaced_$(date +%Y%m%d).py

   # Install new version
   cp tools/{file}_v2.py tools/prod/tg/{file}.py

   # Add production lock header
   # Update PRODUCTION-LOCK-STATUS.md
   ```

5. **Update documentation**:
   - This file (PRODUCTION-LOCK-STATUS.md)
   - Wake-up procedure (if commands changed)
   - Agent manifest (if behavior changed)

---

### For NON-LOCKED Files

**Modify freely** for development/testing.

**But**:
- Don't break working production files
- Document experimental changes
- Test before promoting to production

---

## 📊 Lock Validation Checklist

**Every wake-up, verify**:

- [ ] **Diagnostic bridge**: `tools/openai_telegram_bridge_diagnostic.py` has lock header
- [ ] **JSONL monitor**: `tools/prod/tg/openai_telegram_jsonl_monitor.py` has lock header
- [ ] **Senders**: Both production senders have lock headers
- [ ] **Archive**: Broken versions in `tools/.archive/telegram-cleanup-2025-10-20/`
- [ ] **Process check**: Running processes use correct (locked) files

**If lock violated**:
- Restore from archive
- Investigate who/what modified
- Re-apply lock headers
- Update this document

---

## 🎯 Success Metrics

**Production lock is working if**:
1. Zero accidental modifications to working files
2. All changes go through variant → test → approval flow
3. Archive has complete history of replaced versions
4. Wake-up procedure references correct (locked) files
5. No duplicate bugs reintroduced

**Current status**: ✅ All metrics green (2025-10-20)

---

## 📚 Related Documentation

- **Wake-up procedure**: `to-corey/TELEGRAM-WAKEUP-PROCEDURE.md`
- **Archive manifest**: `tools/.archive/telegram-cleanup-2025-10-20/MANIFEST.md`
- **Agent manifest**: `.claude/agents/tg-bridge.md`
- **Production README**: `tools/prod/tg/README.md`

---

**Document Status**:
- **Created**: 2025-10-20
- **Maintained By**: tg-bridge agent
- **Review Frequency**: Weekly or after any production change
- **Next Review**: 2025-10-27

**Lock Policy**: Immutable without Corey approval
