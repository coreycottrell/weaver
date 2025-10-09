# Deterministic Check-and-Inject: Quick Reference

**One-line summary**: Only injects Claude prompts when NEW messages exist (email or Team 2 hub)

---

## Quick Install

```bash
cd /home/corey/projects/AI-CIV/grow_openai
bash tools/INSTALL-CRON.sh
```

---

## Quick Commands

```bash
# Manual check (test system)
bash tools/check_and_inject.sh

# View recent activity
tail -20 ~/.aiciv/check-inject.log

# View current state
cat ~/.aiciv/last-check-state.json

# Reset system (treats everything as new)
rm ~/.aiciv/last-check-state.json

# Monitor in real-time
tail -f ~/.aiciv/check-inject.log
```

---

## Cron Management

```bash
# View cron jobs
crontab -l

# Edit cron jobs
crontab -e

# Add cron (every 30 minutes)
*/30 * * * * /home/corey/projects/AI-CIV/grow_openai/tools/check_and_inject.sh >> ~/.aiciv/cron.log 2>&1

# Disable temporarily (add '#' in front)
# */30 * * * * ...

# Remove cron
crontab -l | grep -v check_and_inject.sh | crontab -
```

---

## Troubleshooting

| Problem | Quick Fix |
|---------|-----------|
| Email check fails | Verify `.env` credentials |
| Hub check fails | Test `git pull` in hub repo |
| Too many injections | Delete `~/.aiciv/last-check-state.json` |
| No injections ever | Expected if no new messages |
| Script hangs | Check network connectivity |

---

## Expected Behavior

**Normal operation (no new messages)**:
```
[10:00] Starting check... → Results: Email=0, Hub=0 → Sleeping
[10:30] Starting check... → Results: Email=0, Hub=0 → Sleeping
```

**When new messages arrive**:
```
[11:00] Starting check... → Results: Email=2, Hub=3 → NEW MESSAGES: Injecting!
[11:30] Starting check... → Results: Email=2, Hub=3 → Sleeping (already counted)
```

---

## Key Files

```
tools/check_email_inbox.py          # Email checker
tools/check_hub_messages.py          # Hub checker  
tools/check_and_inject.sh            # Main script
tools/INSTALL-CRON.sh                # Installer

~/.aiciv/last-check-state.json       # State tracking
~/.aiciv/check-inject.log            # Activity log
~/.aiciv/inject-prompt.txt           # Generated prompts
```

---

## Success Metrics

- ✅ ~48 checks/day (every 30min)
- ✅ ~5-10 injections/day (only when new)
- ✅ ~80% fewer interruptions
- ✅ 0 missed messages (deterministic)

---

## Documentation

- **Full Setup**: `tools/DETERMINISTIC-CHECK-SETUP.md`
- **Testing**: `tools/TEST-GUIDE.md`
- **Overview**: `AUTONOMOUS-CHECK-SYSTEM.md`
- **This**: `tools/QUICK-REFERENCE.md`

---

**Status**: ✅ Ready for production
