# Archived Telegram Files - 2025-10-20

## Reason
Duplicate injection bug fixed - archived broken versions, keeping working diagnostic as production.

## Context
After extensive debugging on 2025-10-20, confirmed that:
- **Working**: `tools/openai_telegram_bridge_diagnostic.py` (zero duplicates)
- **Broken**: `tools/prod/tg/openai_telegram_bridge.py` (duplicate bug)
- **Old**: Development versions in `tools/` directory

## Files to Archive

### Broken Production Bridge
- **File**: `tools/prod/tg/openai_telegram_bridge.py`
- **Issue**: Missing update_id deduplication, causes duplicate injections
- **Replaced by**: `tools/openai_telegram_bridge_diagnostic.py` (now production)

### Old Development Versions
- **File**: `tools/openai_telegram_bridge.py`
- **Status**: Development version, superseded by diagnostic
- **Note**: May not exist, archive if present

- **File**: `tools/openai_telegram_jsonl_monitor.py`
- **Status**: Development version, superseded by `tools/prod/tg/openai_telegram_jsonl_monitor.py`

### Obsolete Architecture
- **File**: `tools/telegram_monitor.py`
- **Issue**: Old tmux buffer scanning architecture (60s polls)
- **Replaced by**: JSONL monitoring (3s polls, 20x faster)

- **File**: `tools/telegram_monitor_jsonl.py`
- **Status**: Development version of JSONL monitor

### Duplicate Senders (Keep for Now)
- `tools/send_telegram_plain.py` - Development copy
- `tools/send_telegram_direct.py` - Development copy
- **Note**: Production versions in `tools/prod/tg/`, keep dev copies for testing

## Working Production Files

### Bridge (Team 1 Primary)
- `tools/openai_telegram_bridge_diagnostic.py` ✅ WORKING
  - Update ID deduplication ✅
  - Injection locking ✅
  - Zero duplicates confirmed ✅

### Monitor (Team 1 Primary)
- `tools/prod/tg/openai_telegram_jsonl_monitor.py` ✅ WORKING
  - JSONL file monitoring (3s polls)
  - SHA256 deduplication
  - Session rotation handling

### Senders
- `tools/prod/tg/send_telegram_plain.py` ✅ WORKING
- `tools/prod/tg/send_telegram_direct.py` ✅ WORKING

### Configuration
- `config/telegram_config.json` ✅ WORKING (session: "1")

## Archive Instructions

```bash
# Create archive directory
mkdir -p tools/.archive/telegram-cleanup-2025-10-20

# Move broken production bridge
mv tools/prod/tg/openai_telegram_bridge.py tools/.archive/telegram-cleanup-2025-10-20/openai_telegram_bridge_broken.py

# Move old development versions (if they exist)
mv tools/openai_telegram_bridge.py tools/.archive/telegram-cleanup-2025-10-20/openai_telegram_bridge_dev.py 2>/dev/null || true
mv tools/openai_telegram_jsonl_monitor.py tools/.archive/telegram-cleanup-2025-10-20/openai_telegram_jsonl_monitor_dev.py 2>/dev/null || true

# Move obsolete architecture
mv tools/telegram_monitor.py tools/.archive/telegram-cleanup-2025-10-20/telegram_monitor_tmux_obsolete.py 2>/dev/null || true
mv tools/telegram_monitor_jsonl.py tools/.archive/telegram-cleanup-2025-10-20/telegram_monitor_jsonl_dev.py 2>/dev/null || true

# Create archive manifest
cp tools/.archive/telegram-cleanup-2025-10-20/MANIFEST.md tools/.archive/telegram-cleanup-2025-10-20/
```

## Safe to Delete After
2025-11-20 (30 days) if no issues reported

## Restoration Procedure
If diagnostic bridge fails and old version needed:
```bash
# Restore broken production (not recommended - has duplicates)
cp tools/.archive/telegram-cleanup-2025-10-20/openai_telegram_bridge_broken.py tools/prod/tg/openai_telegram_bridge.py

# Or restore development version
cp tools/.archive/telegram-cleanup-2025-10-20/openai_telegram_bridge_dev.py tools/openai_telegram_bridge.py
```

## Validation
- [x] Diagnostic bridge tested (2025-10-20)
- [x] Zero duplicates confirmed
- [x] JSONL monitor working
- [x] Corey approval received
- [ ] 30-day stability validation (complete by 2025-11-20)

---

**Archive Created**: 2025-10-20
**Created By**: tg-bridge agent
**Validated By**: Corey (human founder)
