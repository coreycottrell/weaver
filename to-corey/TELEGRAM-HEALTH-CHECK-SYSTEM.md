# Telegram Health Check System

**Created**: 2025-12-27
**Status**: Ready for deployment

---

## Quick Fix (If TG is Down NOW)

```bash
cd /home/corey/projects/AI-CIV/WEAVER
bash tools/telegram_quick_fix.sh
```

This will:
1. Stop any broken processes
2. Verify config
3. Test API connectivity
4. Send test message

---

## Health Check Script

**File**: `/home/corey/projects/AI-CIV/WEAVER/tools/telegram_health_check.py`

### What It Tests

1. **Config validation** - Checks `config/telegram_config.json` exists and has required fields
2. **Bot API connectivity** - Calls `getMe` to verify bot is reachable
3. **Message sending** (optional) - Sends actual test message to verify full pipeline

### Usage

```bash
# Check connectivity only (no message sent)
python3 tools/telegram_health_check.py

# Also send test message to Corey
python3 tools/telegram_health_check.py --send

# Quiet mode (for cron - minimal output)
python3 tools/telegram_health_check.py --quiet
```

### Exit Codes

| Code | Meaning |
|------|---------|
| 0 | All checks passed |
| 1 | Config error (file missing, invalid JSON, missing fields) |
| 2 | Bot API connection failed |
| 3 | Message send failed (only with --send) |

---

## Cron Setup (Recommended)

### Recommended Cadence: Every 30 Minutes

```bash
# Add to crontab
bash tools/telegram_health_cron_setup.sh add

# Or manually: crontab -e and add:
*/30 * * * * /usr/bin/python3 /home/corey/projects/AI-CIV/WEAVER/tools/telegram_health_check.py --quiet >> /tmp/telegram_health_cron.log 2>&1
```

### Why 30 Minutes?

- **Frequent enough**: Catches issues within reasonable time
- **Not too noisy**: Won't flood logs or hit rate limits
- **Good balance**: For non-critical monitoring infrastructure

### Alternative Cadences

```bash
# Every 15 minutes (more aggressive)
*/15 * * * * ...

# Every hour (less aggressive)
0 * * * * ...
```

### View Cron Logs

```bash
tail -20 /tmp/telegram_health_cron.log
```

### Remove from Cron

```bash
bash tools/telegram_health_cron_setup.sh remove
```

---

## Log Files

| Log | Purpose |
|-----|---------|
| `/tmp/telegram_health_check.log` | Health check results (always written) |
| `/tmp/telegram_health_cron.log` | Cron job output |
| `/tmp/openai_telegram_bridge.log` | Bridge process log |

---

## Files Created

1. **`tools/telegram_health_check.py`** - Main health check script
2. **`tools/telegram_health_cron_setup.sh`** - Cron setup helper
3. **`tools/telegram_quick_fix.sh`** - Emergency fix script
4. **`to-corey/TELEGRAM-HEALTH-CHECK-SYSTEM.md`** - This documentation

---

## Sending Messages Directly

When health check passes, you can send messages:

```bash
# Plain text (recommended)
python3 tools/send_telegram_plain.py 437939400 "Your message here"

# With Markdown (may fail on special chars)
python3 tools/send_telegram_direct.py 437939400 "**bold** _italic_"

# File attachment
python3 tools/send_telegram_file.py 437939400 /path/to/file "Caption"
```

---

## Common Issues

### "Chat not found"

**Cause**: Corey hasn't started conversation with bot
**Fix**: Search for the bot in Telegram and send `/start`

### "Unauthorized"

**Cause**: Bot token invalid or revoked
**Fix**: Check `config/telegram_config.json` has valid bot_token

### Bridge Not Running

**Note**: Bridge is only needed for bidirectional (Corey -> AI) messaging.
For outbound-only (AI -> Corey), bridge is not required.

To start bridge:
```bash
nohup python3 tools/openai_telegram_bridge.py > /tmp/openai_telegram_bridge.log 2>&1 &
```

---

## Architecture Summary

```
OUTBOUND (AI -> Corey's Phone):
  send_telegram_plain.py -> Telegram Bot API -> Corey's Phone

INBOUND (Corey's Phone -> AI):
  Corey's Phone -> Telegram Bot API -> openai_telegram_bridge.py -> tmux injection

HEALTH CHECK:
  telegram_health_check.py -> getMe API -> (optional) sendMessage
```

The health check validates the outbound path is working. If Corey can receive messages, the critical infrastructure is functional.

---

## Next Steps

1. Run quick fix to verify current status:
   ```bash
   bash tools/telegram_quick_fix.sh
   ```

2. Add cron for ongoing monitoring:
   ```bash
   bash tools/telegram_health_cron_setup.sh add
   ```

3. Verify cron is running:
   ```bash
   crontab -l | grep telegram
   ```
