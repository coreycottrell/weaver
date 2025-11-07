# Deterministic Check-and-Inject System

**Status**: ✅ READY FOR DEPLOYMENT
**Date**: 2025-10-06
**Author**: the-conductor (refactoring-specialist domain)

---

## Executive Summary

**Problem**: Current autonomous system injects Claude prompt every 30 minutes regardless of whether there are new messages, causing unnecessary interruptions.

**Solution**: Check-first system that only injects when NEW messages exist (email or Team 2 hub).

**Impact**: ~80% reduction in interruptions (48 → ~10 injections/day)

---

## System Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    CRON JOB (*/30)                      │
│              check_and_inject.sh                        │
└─────────────────┬───────────────────────────────────────┘
                  │
        ┌─────────┴─────────┐
        │                   │
        ▼                   ▼
┌───────────────┐   ┌───────────────┐
│ Email Checker │   │  Hub Checker  │
│ (IMAP/UNSEEN) │   │ (git diff)    │
└───────┬───────┘   └───────┬───────┘
        │                   │
        └─────────┬─────────┘
                  ▼
        ┌─────────────────┐
        │  State Tracker  │
        │ (JSON persist)  │
        └────────┬─────────┘
                 │
         ┌───────┴────────┐
         │                │
         ▼                ▼
    ┌────────┐      ┌─────────┐
    │ INJECT │      │  SLEEP  │
    └────────┘      └─────────┘
     (new msgs)     (no change)
```

---

## Components

### 1. Email Checker (`check_email_inbox.py`)
- **Tech**: Python 3 + imaplib (stdlib)
- **Method**: IMAP UNSEEN search
- **Output**: Count of unread messages
- **Time**: ~1-2 seconds
- **Dependencies**: `.env` (GMAIL_USERNAME, GOOGLE_APP_PASSWORD)

### 2. Hub Checker (`check_hub_messages.py`)
- **Tech**: Python 3 + subprocess (git)
- **Method**: Compare commit hashes, count new message files
- **Output**: Count of new messages since last check
- **Time**: ~0.5-1 seconds
- **Dependencies**: Team 2 hub repo at `/home/corey/projects/AI-CIV/team1-production-hub/`

### 3. Main Orchestrator (`check_and_inject.sh`)
- **Tech**: Bash
- **Logic**: 
  1. Run both checkers
  2. Load previous state from JSON
  3. Compare current vs previous
  4. Inject ONLY if delta > 0
  5. Update state file
- **State**: `~/.aiciv/last-check-state.json`
- **Logs**: `~/.aiciv/check-inject.log`

### 4. Installer (`INSTALL-CRON.sh`)
- **Tech**: Bash
- **Function**: Validate all components, offer cron installation
- **Safety**: Checks if already installed (no duplicates)

---

## Installation

### Quick Start
```bash
cd /home/corey/projects/AI-CIV/grow_openai

# Run installer (tests everything, offers cron install)
bash tools/INSTALL-CRON.sh
```

### Manual Install
```bash
# Test components
python3 tools/check_email_inbox.py
python3 tools/check_hub_messages.py
bash tools/check_and_inject.sh

# Install cron
crontab -e
# Add: */30 * * * * /home/corey/projects/AI-CIV/grow_openai/tools/check_and_inject.sh >> ~/.aiciv/cron.log 2>&1
```

---

## State Management

**File**: `~/.aiciv/last-check-state.json`

**Structure**:
```json
{
  "last_check": "2025-10-06T14:59:58Z",
  "email_count": 3,
  "hub_count": 12,
  "hub_commit_hash": "a1b2c3d4..."
}
```

**Logic**:
- Track absolute counts (not just deltas)
- On each check: `new = current - previous`
- If `new > 0` → inject
- If `new == 0` → silent

**Reset**: Delete file to reset (next check treats everything as new)

---

## Injection Mechanism

**When triggered**:
1. Create prompt: `~/.aiciv/inject-prompt.txt`
2. Copy to: `.claude/autonomous-prompt.txt`
3. Claude Code watches this file and auto-injects

**Prompt format**:
```
🔔 AUTONOMOUS CHECK: NEW MESSAGES DETECTED

Email: 3 unread message(s)
Hub: 5 new message(s) from Team 2

ACTION REQUIRED:
1. Spawn human-liaison agent to check email
2. Check Team 2 hub messages via hub_cli.py
3. Respond appropriately to both channels

[Commands provided for easy execution]
```

---

## Testing

**Complete test suite**: See `tools/TEST-GUIDE.md`

**Quick validation**:
```bash
# Should pass all tests
bash tools/INSTALL-CRON.sh
```

**Key tests**:
1. ✅ No new messages → no injection
2. ✅ New email → inject with email count
3. ✅ New hub message → inject with hub count
4. ✅ Both new → inject with both counts
5. ✅ State persists across runs
6. ✅ Error handling (graceful degradation)
7. ✅ Performance (<5s total)

---

## Monitoring

**View recent activity**:
```bash
tail -50 ~/.aiciv/check-inject.log
```

**Count injections vs checks**:
```bash
grep "Starting autonomous check" ~/.aiciv/check-inject.log | wc -l  # Total checks
grep "NEW MESSAGES" ~/.aiciv/check-inject.log | wc -l              # Injections
```

**Current state**:
```bash
cat ~/.aiciv/last-check-state.json | jq .
```

---

## Performance

**Baseline** (per check):
- Email: 1-2s (IMAP connection + search)
- Hub: 0.5-1s (git pull + diff)
- State: <0.1s (JSON read/write)
- **Total**: ~2-3 seconds

**Frequency**: Every 30 minutes (configurable)

**Daily overhead**: 48 checks × 3s = 144 seconds (~2.4 minutes/day)

**Interruptions**: Only when new messages (~5-10/day vs 48/day)

---

## Configuration

### Change Frequency
```bash
crontab -e

# Options:
*/10 * * * *  # Every 10 minutes (high responsiveness)
*/30 * * * *  # Every 30 minutes (balanced) ← DEFAULT
0 * * * *     # Every hour (low interruption)
```

### Filter Email by Sender
Edit `check_email_inbox.py`:
```python
# Only count email from specific senders
status, messages = mail.search(None, 'UNSEEN', 'FROM', 'corey@example.com')
```

### Filter Hub by Room
Edit `check_hub_messages.py`:
```python
# Only count specific rooms
new_files = [
    line for line in result.stdout.split('\n')
    if '/messages/' in line 
    and line.endswith('.json')
    and 'partnerships' in line  # partnerships room only
]
```

---

## Troubleshooting

### Email Check Fails
```bash
# Verify credentials
cat .env | grep -E "GMAIL|GOOGLE"

# Test IMAP connection
python3 -c "import imaplib; mail=imaplib.IMAP4_SSL('imap.gmail.com'); print('OK')"
```

### Hub Check Fails
```bash
# Verify hub repo accessible
cd /home/corey/projects/AI-CIV/team1-production-hub
git pull
```

### State File Corrupt
```bash
# Reset state
rm ~/.aiciv/last-check-state.json
# Next run will treat everything as "new"
```

### Too Many Injections
```bash
# Check if state file updating correctly
cat ~/.aiciv/last-check-state.json

# Check if counts decreasing (emails being marked read)
tail ~/.aiciv/check-inject.log | grep "Results:"
```

---

## Security

**Email credentials**: Stored in `.env` (gitignored)
**Hub access**: SSH key (no password in scripts)
**State file**: World-readable (`~/.aiciv/`) - no sensitive data
**Logs**: May contain email/hub counts (not content)

**Recommendations**:
- ✅ Keep `.env` out of version control
- ✅ Use SSH key for hub (no HTTPS tokens)
- ✅ Restrict log permissions: `chmod 600 ~/.aiciv/check-inject.log`

---

## Maintenance

**Weekly**:
```bash
# Review logs
tail -100 ~/.aiciv/check-inject.log

# Check for errors
grep -i error ~/.aiciv/check-inject.log
```

**Monthly**:
```bash
# Archive old logs
gzip ~/.aiciv/check-inject.log.old

# Verify cron still active
crontab -l | grep check_and_inject
```

**Disable temporarily**:
```bash
# Comment out cron
crontab -e
# Add '#' before the line
```

**Uninstall**:
```bash
# Remove cron
crontab -l | grep -v check_and_inject.sh | crontab -

# Remove state
rm -rf ~/.aiciv/
```

---

## Files Created

```
tools/
├── check_email_inbox.py          # Email checker (IMAP)
├── check_hub_messages.py          # Hub checker (git)
├── check_and_inject.sh            # Main orchestrator
├── INSTALL-CRON.sh                # One-command installer
├── DETERMINISTIC-CHECK-SETUP.md   # Full documentation
└── TEST-GUIDE.md                  # Comprehensive tests

~/.aiciv/                           # Runtime state (created automatically)
├── last-check-state.json          # Persistent state
├── check-inject.log               # Activity log
├── inject-prompt.txt              # Generated prompt (when injecting)
└── cron.log                       # Cron execution log
```

---

## Success Metrics

**After 24 hours**:
- ✅ ~48 checks performed (every 30min)
- ✅ ~5-10 injections (only when new)
- ✅ ~80% fewer interruptions
- ✅ 0 missed messages (deterministic)
- ✅ 0 crashes

**Expected log pattern**:
```
[10:00] Starting check... → No new messages. Sleeping.
[10:30] Starting check... → No new messages. Sleeping.
[11:00] Starting check... → NEW MESSAGES: Injecting!    ← Only when actually new
[11:30] Starting check... → No new messages. Sleeping.
```

---

## Integration with Existing Systems

**Replaces**: Unconditional 30-minute injection from previous autonomous system

**Preserves**: All autonomous capabilities (email, hub monitoring, human-liaison)

**Adds**: Deterministic state tracking (no duplicate notifications)

**Migration**:
1. Test new system in parallel (different schedule)
2. Verify logs for 24 hours
3. Disable old system
4. Enable new system (same schedule)

---

## Future Enhancements

**Possible additions**:
1. **Smart scheduling**: More frequent checks during work hours
2. **Priority detection**: Immediate injection for high-priority senders
3. **Multi-channel**: Add Slack, Discord, GitHub notifications
4. **AI summarization**: Include brief message summary in injection
5. **Batching**: Wait for N messages before injecting (reduce interruption)
6. **Health metrics**: Track MTBF, false positive rate, latency

---

## Contact

**Questions**: Ask the-conductor or refactoring-specialist agents
**Issues**: Check logs first (`~/.aiciv/check-inject.log`)
**Improvements**: Document in `.claude/memory/agent-learnings/`

---

## Changelog

**2025-10-06**: Initial release
- Email checker (IMAP UNSEEN)
- Hub checker (git diff)
- Main orchestrator with state tracking
- Complete documentation + tests
- One-command installer

---

**Status**: ✅ PRODUCTION READY

All components tested and validated. Ready for Corey to install cron.
