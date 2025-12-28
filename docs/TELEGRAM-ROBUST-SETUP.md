# WEAVER Telegram Bot - Robust Setup

**Created**: 2025-12-27
**Status**: Production-Ready

## Overview

The WEAVER Telegram bot provides bidirectional communication between Telegram and Claude sessions. This document describes the robust infrastructure that ensures the bot runs reliably.

## Key Features

1. **Auto Session Detection** - Always picks the latest `weaver-primary-*` tmux session
2. **Periodic Session Refresh** - Detects new sessions every 60 seconds while running
3. **3x Enter Retry** - Robust tmux injection with retry logic
4. **Cron Health Check** - Every 5 minutes, auto-recovers if bot crashes
5. **Systemd Service** - Auto-starts on boot, restarts on failure
6. **Management Script** - Easy start/stop/restart/status/health commands

## Quick Commands

```bash
# Management script
/home/corey/projects/AI-CIV/WEAVER/tools/telegram_service.sh start
/home/corey/projects/AI-CIV/WEAVER/tools/telegram_service.sh stop
/home/corey/projects/AI-CIV/WEAVER/tools/telegram_service.sh restart
/home/corey/projects/AI-CIV/WEAVER/tools/telegram_service.sh status
/home/corey/projects/AI-CIV/WEAVER/tools/telegram_service.sh health
/home/corey/projects/AI-CIV/WEAVER/tools/telegram_service.sh logs
/home/corey/projects/AI-CIV/WEAVER/tools/telegram_service.sh recover

# Or via systemd
systemctl --user start weaver-telegram
systemctl --user stop weaver-telegram
systemctl --user restart weaver-telegram
systemctl --user status weaver-telegram
```

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    ROBUST TELEGRAM SETUP                     │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐  │
│  │   Telegram   │◄──►│  Bot Python  │◄──►│ tmux Session │  │
│  │     API      │    │   Process    │    │   (Claude)   │  │
│  └──────────────┘    └──────────────┘    └──────────────┘  │
│                             ▲                               │
│                             │                               │
│         ┌───────────────────┼───────────────────┐          │
│         │                   │                   │          │
│         ▼                   ▼                   ▼          │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐  │
│  │   Systemd    │    │ Cron Health  │    │  Management  │  │
│  │   Service    │    │    Check     │    │    Script    │  │
│  │ (boot start) │    │  (5 min)     │    │  (manual)    │  │
│  └──────────────┘    └──────────────┘    └──────────────┘  │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

## Files

| File | Purpose |
|------|---------|
| `tools/telegram_unified.py` | Main bot code |
| `tools/telegram_service.sh` | Management script |
| `tools/telegram_health_cron.sh` | Cron-based health check |
| `config/telegram_config.json` | Bot configuration |
| `~/.config/systemd/user/weaver-telegram.service` | Systemd service |

## Session Detection

The bot automatically detects the latest WEAVER tmux session:

1. Lists all tmux sessions
2. Filters for `weaver-primary-*` pattern
3. Sorts by name (timestamp) and picks latest
4. Falls back to config file only if no sessions found
5. Re-checks every 60 seconds while running

**No hardcoded session names** - always auto-detects.

## Recovery Mechanisms

### Cron (Every 5 Minutes)
```
*/5 * * * * /home/corey/projects/AI-CIV/WEAVER/tools/telegram_health_cron.sh
```

Checks:
- Is bot process running?
- Is log file fresh (< 5 min old)?
- If either fails → restart bot

### Systemd (On Failure)
```ini
Restart=always
RestartSec=10
```

If bot crashes, systemd restarts it within 10 seconds.

### Manual Recovery
```bash
./tools/telegram_service.sh recover
```

Runs health check and auto-restarts if issues found.

## Health Check Details

The health check verifies:

1. **Bot Process** - Is python3 telegram_unified.py running?
2. **tmux Sessions** - Are there any weaver-primary-* sessions?
3. **Log Freshness** - Has the log been updated recently?
4. **Config File** - Is telegram_config.json valid JSON?
5. **Telegram API** - Can we reach Telegram's API?

## Troubleshooting

### Bot Not Running
```bash
./tools/telegram_service.sh status
./tools/telegram_service.sh start
```

### Wrong Session
The bot auto-detects. If it picked wrong session:
```bash
./tools/telegram_service.sh restart
```

### Messages Not Injecting
Check tmux session exists:
```bash
tmux list-sessions | grep weaver
```

Check bot logs:
```bash
./tools/telegram_service.sh logs
```

### Enter Key Not Working
The bot has 3x retry built-in. If still failing, check:
```bash
# Manual test
tmux send-keys -t weaver-primary-XXXXXX "test" Enter
```

## Log Files

| File | Purpose |
|------|---------|
| `/tmp/telegram_weaver.log` | Main bot log |
| `/tmp/telegram_health_cron.log` | Health check log |
| `/tmp/weaver_telegram.pid` | PID file |

## Configuration

Edit `config/telegram_config.json`:

```json
{
  "bot_token": "YOUR_BOT_TOKEN",
  "authorized_users": {
    "USER_ID": {
      "name": "Corey",
      "role": "creator",
      "admin": true
    }
  },
  "tmux_session": "weaver-primary-XXXXXXXX",  // Optional fallback
  "working_directory": "/home/corey/projects/AI-CIV/WEAVER"
}
```

**Note**: `tmux_session` is now a fallback only. Bot auto-detects latest session.
