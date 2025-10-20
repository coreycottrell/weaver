# tg-bridge Agent Documentation Updated

**Date**: 2025-10-20
**File**: `.claude/agents/tg-bridge.md`
**Size**: 29KB → 35KB (+6KB of production infrastructure docs)

---

## What Was Updated

The tg-bridge specialist agent now knows about:

### ✅ 1. Production Lock Architecture

**Location**: `tools/prod/tg/` (8 protected files)

- 🔒 Protection headers on all files
- Clear modification workflow (create _v2 variants in tools/, test, then copy)
- Why it exists (ACG collision prevention)
- Management scripts (start/stop/status)

**Files Protected**:
1. openai_telegram_jsonl_monitor.py
2. openai_telegram_bridge.py
3. send_telegram_plain.py
4. send_telegram_direct.py
5. start_telegram_infrastructure.sh
6. stop_telegram_infrastructure.sh
7. status_telegram_infrastructure.sh
8. README.md

### ✅ 2. JSONL Monitoring Architecture

**Key Details**:
- Replaced tmux buffer monitoring (60s) with JSONL file monitoring (3s)
- 20x faster detection
- Delta detection (file offset tracking - only reads new content)
- Message aggregation (5-20+ JSONL lines per message)
- Full SHA256 hashing (deduplication)
- Session rotation handling

**Technical Specs**:
- Polls `~/.claude/projects/-home-corey-projects-AI-CIV-grow_openai/*.jsonl`
- Looks for `🤖🎯📱 ... ✨🔚` wrapper markers
- State file: `.tg_sessions/jsonl_monitor_state.json`
- Logs: `/tmp/openai_telegram_jsonl_monitor.log`

### ✅ 3. Process Naming Convention

**Safety Pattern**:
- All processes: `openai_` prefix
- Full path matching: `tools/prod/tg/openai_telegram_*`
- Prevents ACG (grow_gemini) collisions
- Safe to `pkill -f "tools/prod/tg/openai_telegram"` without affecting other projects

### ✅ 4. Current State Awareness

**Agent now knows**:
- Production files exist in `tools/prod/tg/` but NOT yet running
- Current processes still use `tools/` directory (old location)
- You will switch when ready
- Health checks look for EITHER location (backward compatible)

### ✅ 5. Backup Information

- Backup file: `corey_tg_interface_backup.tar.gz`
- Location: `/home/corey/projects/AI-CIV/grow_openai/`
- Contents: All 8 production files
- Restore: `tar -xzf corey_tg_interface_backup.tar.gz`

---

## New Sections in Agent Docs

### "Files & Infrastructure" Section Enhanced

**Added**:
1. **🔒 PRODUCTION LOCK ARCHITECTURE** subsection
   - What it is, why it exists, how to use it
   - All 8 protected files listed
   - Usage commands for management scripts

2. **Production Files (Current State)** subsection
   - Complete inventory
   - Process naming convention details
   - Backup information

3. **JSONL Monitoring Architecture** subsection
   - How it works (6-step process)
   - Key features (3s polling, delta detection, SHA256)
   - State file format
   - Log locations
   - Configuration snippet

### "Monitor Infrastructure Health" Section Updated

**Changed**:
- Now checks for EITHER `tools/` OR `tools/prod/tg/` processes
- Backward compatible (works during transition)
- Updated status report includes:
  - Architecture info (JSONL monitoring)
  - Production lock reminder
  - Management script commands
  - Documentation pointer

### "Monitoring" Section Status Changed

**Before**: "Monitoring (BROKEN - FIXING)"
**After**: "Monitoring (FIXED - JSONL Architecture)"

---

## What tg-bridge Can Now Do

When you (or Primary) invoke tg-bridge, the agent now:

1. **Understands production lock**
   - Won't modify `tools/prod/tg/` files directly
   - Knows to create variants in `tools/` for testing
   - Aware of protection header system

2. **Knows current architecture**
   - JSONL monitoring (not tmux)
   - 3-second polling
   - Delta detection mechanics
   - Message aggregation logic

3. **Process naming aware**
   - Uses `openai_` prefix in all commands
   - Full path matching for safety
   - Won't collide with ACG processes

4. **Transition aware**
   - Knows production files exist but aren't running yet
   - Health checks work during transition
   - Will switch commands when you move to production

5. **Has complete operational docs**
   - Management script commands
   - Log file locations
   - Configuration format
   - State file structure

---

## Example: What tg-bridge Would Report Now

If Primary invokes: `Task(tg-bridge): Check health`

**tg-bridge would respond**:

```markdown
# 📱 tg-bridge: Infrastructure Health Check

**Agent**: tg-bridge
**Domain**: Telegram infrastructure
**Date**: 2025-10-20

---

**Health Check Results**:

Bridge process:
✓ RUNNING (tools/telegram_bridge.py, PID 12345)
  Location: Development (not production yet)

JSONL Monitor process:
✓ RUNNING (tools/telegram_jsonl_monitor.py, PID 12389)
  Location: Development (not production yet)
  Architecture: JSONL monitoring (3s polling, 20x faster than tmux)

Recent activity:
- Monitor: Last check 2s ago, scanning session-abc123.jsonl
- Bridge: Last message received 5m ago

===================================
Telegram Infrastructure Status
===================================

Architecture: JSONL monitoring (3s polling, 20x faster)
Production lock: tools/prod/tg/ (protected, ready for switch)
Current running: tools/ (development location)

When ready to switch to production:
1. Stop current: pkill -f "tools/telegram"
2. Start production: ./tools/prod/tg/start_telegram_infrastructure.sh
3. Verify: ./tools/prod/tg/status_telegram_infrastructure.sh

Documentation: tools/prod/tg/README.md
Backup: corey_tg_interface_backup.tar.gz
===================================

All systems operational. Ready for production switch when you are.
```

---

## For Future Sessions

**tg-bridge agent now fully documents**:
- The entire production lock pattern
- JSONL monitoring architecture details
- Process safety conventions
- Transition path from development to production

**Next Primary can**:
- Delegate Telegram work to tg-bridge with full context
- tg-bridge will respect production lock
- tg-bridge will use correct process names
- tg-bridge will work during AND after transition

---

## File Locations

**Agent manifest**: `.claude/agents/tg-bridge.md` (35KB)
**Backup**: `/tmp/tg-bridge-backup.md` (original 29KB)
**Production docs**: `tools/prod/tg/README.md` (comprehensive reference)

---

**Status**: ✅ Complete - tg-bridge agent fully updated with production architecture awareness

**Next**: When you're ready to switch to production, tg-bridge will know exactly what to do.

