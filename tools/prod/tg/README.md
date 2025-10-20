# 🔒 Production Telegram Infrastructure

**⚠️ WARNING: DO NOT MODIFY FILES IN THIS DIRECTORY ⚠️**

This directory contains production-tested, operational Telegram infrastructure for grow_openai.

## 🚨 Production Lock Rules

1. **NEVER edit files in `tools/prod/tg/` directly**
2. **To make changes**:
   - Create variant in `tools/` (e.g., `openai_telegram_jsonl_monitor_v2.py`)
   - Test thoroughly
   - Only after validation, copy to `tools/prod/tg/`
3. **All files have 🔒 headers** - agents must respect these markers

## Files in Production

### Core Infrastructure
- `openai_telegram_jsonl_monitor.py` - Watches Claude Code JSONL logs for wrapped messages
- `openai_telegram_bridge.py` - Receives Telegram messages, injects into tmux
- `send_telegram_plain.py` - Direct Telegram message sender
- `send_telegram_direct.py` - Simple Telegram send utility

### Management Scripts
- `start_telegram_infrastructure.sh` - Start monitor + bridge
- `stop_telegram_infrastructure.sh` - Stop all Telegram processes
- `status_telegram_infrastructure.sh` - Check status and recent activity

## Usage

### Start Infrastructure
```bash
cd /home/corey/projects/AI-CIV/grow_openai
./tools/prod/tg/start_telegram_infrastructure.sh
```

### Check Status
```bash
./tools/prod/tg/status_telegram_infrastructure.sh
```

### Stop Infrastructure
```bash
./tools/prod/tg/stop_telegram_infrastructure.sh
```

## Why Production Lock?

**Problem**: Multiple collisions where agents:
- Accidentally killed ACG's (grow_gemini) processes
- Overwrote working code during debugging
- Created multiple duplicate monitors

**Solution**: Spatial isolation
- `tools/prod/tg/` = Production lock (never touch)
- `tools/` = Development workspace (agents can work here)
- Process names include full path (`tools/prod/tg/...`) for safety

## Architecture

```
grow_openai/
├── tools/
│   ├── prod/
│   │   └── tg/              ← 🔒 PRODUCTION (this directory)
│   │       ├── openai_telegram_jsonl_monitor.py
│   │       ├── openai_telegram_bridge.py
│   │       ├── send_telegram_plain.py
│   │       ├── send_telegram_direct.py
│   │       ├── start_telegram_infrastructure.sh
│   │       ├── stop_telegram_infrastructure.sh
│   │       └── status_telegram_infrastructure.sh
│   │
│   └── *.py                 ← Development workspace
│
├── config/
│   └── telegram_config.json
│
└── .tg_sessions/
    └── jsonl_monitor_state.json
```

## Key Features

### Process Naming
- `openai_` prefix prevents collision with ACG (grow_gemini)
- Full path matching: `tools/prod/tg/openai_telegram_jsonl_monitor.py`
- Cross-context safe (names survive session clears)

### JSONL Monitoring
- Watches `~/.claude/projects/-home-corey-projects-AI-CIV-grow_openai/*.jsonl`
- Detects messages wrapped with `🤖🎯📱 ... ✨🔚` markers
- 3-second polling (20x faster than old tmux approach)
- Deduplication via SHA256 hashing

### Telegram Bridge
- Receives messages from Telegram
- Injects into tmux session 5
- Two-way communication with Claude Code

## Logs

- JSONL Monitor: `/tmp/openai_telegram_jsonl_monitor.log`
- JSONL Errors: `/tmp/openai_telegram_jsonl_monitor_error.log`
- Bridge: `/tmp/openai_telegram_bridge.log`

## Configuration

See `config/telegram_config.json`:
- `tmux_session`: Which tmux session to target
- `jsonl_monitor.poll_interval_seconds`: How often to check logs (3s)
- `jsonl_monitor.project_name`: Claude Code project slug

## History

- **2025-10-20**: Created production lock after multiple collisions with ACG
- **2025-10-20**: Fixed process name collision (added `openai_` prefix)
- **2025-10-20**: Migrated from tmux buffer to JSONL monitoring (20x faster)
- **2025-10-19**: Copied from ACG's working implementation

## Emergency Recovery

If infrastructure breaks:

1. **Check what's running**:
   ```bash
   ps aux | grep "openai_telegram" | grep -v grep
   ```

2. **Kill everything safely** (only grows_openai processes):
   ```bash
   pkill -f "tools/prod/tg/openai_telegram"
   ```

3. **Restart from production**:
   ```bash
   ./tools/prod/tg/start_telegram_infrastructure.sh
   ```

4. **Never restart from `tools/` directly** - use production lock

## Last Updated

**Date**: 2025-10-20
**By**: The Primary (Team 1)
**Reason**: Initial production lock creation after ACG collision incident
