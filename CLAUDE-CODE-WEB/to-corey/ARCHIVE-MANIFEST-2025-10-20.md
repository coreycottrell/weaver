# Diagnostic Files Archive Manifest - 2025-10-20

## Purpose
Diagnostic documentation from debugging duplicate injection bug (2025-10-20).
These files led to the final fix but are no longer needed for operations.

---

## Files Recommended for Archive

### Diagnostic Documentation (Can Archive After 30 Days)
1. `to-corey/DUPLICATE-MESSAGE-DIAGNOSTIC-READY.md` - Initial diagnostic setup
2. `to-corey/TG-DUPLICATE-FINAL-DIAGNOSIS.md` - Root cause analysis
3. `tools/DUPLICATE-DIAGNOSTIC-PROCEDURE.md` - Test procedures
4. `tools/TELEGRAM-DUPLICATE-QUICKSTART.md` - Quick diagnostic guide

### Diagnostic Tools (Can Archive After 30 Days)
5. `tools/deploy_diagnostic_bridge.sh` - Deployment script
6. `tools/check_telegram_health.sh` - Health check script

---

## Production Files (KEEP - DO NOT ARCHIVE)

### Operational Documentation
1. `to-corey/TELEGRAM-WAKEUP-PROCEDURE.md` - Post-reboot startup (ESSENTIAL)
2. `to-corey/TELEGRAM-QUICK-REFERENCE.md` - Command reference (ESSENTIAL)
3. `to-corey/TELEGRAM-REBOOT-HANDOFF.md` - Complete context (ESSENTIAL)
4. `to-corey/TELEGRAM-PRODUCTION-STATUS.md` - Current state snapshot
5. `to-corey/TELEGRAM-ISSUE-RESOLVED.md` - Resolution summary
6. `to-corey/SESSION-SUMMARY-2025-10-20-TELEGRAM-FIX.md` - Session summary

### Core Infrastructure
7. `tools/openai_telegram_bridge_diagnostic.py` - Fixed bridge (PRODUCTION)
8. `tools/openai_telegram_jsonl_monitor.py` - JSONL monitor (PRODUCTION)
9. `tools/prod/tg/*` - Production lock files (PROTECTED)
10. `config/telegram_config.json` - Configuration (ESSENTIAL)

---

## Recommended Archive Procedure

**When**: After 2025-11-20 (30 days retention for diagnostics)

**How**:
```bash
# Create archive directory
mkdir -p tools/.archive/telegram-diagnostic-2025-10-20

# Move diagnostic files (DO NOT move production files)
mv to-corey/DUPLICATE-MESSAGE-DIAGNOSTIC-READY.md tools/.archive/telegram-diagnostic-2025-10-20/
mv to-corey/TG-DUPLICATE-FINAL-DIAGNOSIS.md tools/.archive/telegram-diagnostic-2025-10-20/
mv tools/DUPLICATE-DIAGNOSTIC-PROCEDURE.md tools/.archive/telegram-diagnostic-2025-10-20/
mv tools/TELEGRAM-DUPLICATE-QUICKSTART.md tools/.archive/telegram-diagnostic-2025-10-20/
mv tools/deploy_diagnostic_bridge.sh tools/.archive/telegram-diagnostic-2025-10-20/
mv tools/check_telegram_health.sh tools/.archive/telegram-diagnostic-2025-10-20/

# Create manifest in archive
cp to-corey/ARCHIVE-MANIFEST-2025-10-20.md tools/.archive/telegram-diagnostic-2025-10-20/MANIFEST.md

# Commit archive
git add tools/.archive/telegram-diagnostic-2025-10-20/
git commit -m "Archive Telegram diagnostic files (2025-10-20)"
```

---

## Why Archive Instead of Delete

**Reasons**:
1. **Historical record** - Shows debugging process and learnings
2. **Lineage wisdom** - Future agents/teams can learn from approach
3. **Reproduction** - If similar bug recurs, diagnostic procedure is preserved
4. **Audit trail** - Complete documentation of infrastructure changes

**Git History**: Even after archiving, full history remains in git commits.

---

## Safe to Delete After

**Date**: 2025-11-20 (30 days from fix)

**Why**: By then, diagnostic files have served their archival purpose. Git history preserves all details.

---

## Current File Count

**Total files created**: 17
- **Production files**: 10 (KEEP)
- **Diagnostic files**: 6 (archive after 30 days)
- **This manifest**: 1 (archive with diagnostics)

---

## Production Status

**Infrastructure**: ✅ WORKING (zero duplicates)
**Documentation**: ✅ COMPLETE (6 operational docs)
**Git Backup**: ✅ COMMITTED (0c6863f)
**Reboot Ready**: ✅ YES (wake-up procedure tested)

---

**END ARCHIVE MANIFEST**
