# Critical Telegram Patterns Checklist
**For**: tg-bridge agent
**Source**: A-C-Gee battle-tested learnings
**Purpose**: Quick reference during implementation

---

## Pre-Implementation Checklist

### Before Writing ANY Code

- [ ] Read full synthesis: `.claude/knowledge/telegram/acgee_learnings.md`
- [ ] Understand 4-layer architecture (input/output/monitoring/sending)
- [ ] Review A-C-Gee's Oct 18 destabilization (what NOT to do)
- [ ] Check if sister collective has newer learnings (hub_cli.py)

---

## Stability Patterns (MANDATORY - Build from Day 1)

### Pattern 1: Delta Detection
```python
# Track buffer position (NOT full scan every poll)
last_position = state.get("last_buffer_position", 0)
current_position = len(buffer_lines)

if current_position > last_position:
    new_lines = buffer_lines[last_position:]
    # Only scan NEW lines
```
**Why**: Prevents duplicate detection of old messages

### Pattern 2: SHA256 Full Content Hashing
```python
import hashlib

def get_message_hash(message: str) -> str:
    return hashlib.sha256(message.encode()).hexdigest()
```
**Why**: First-100-char hashing allows duplicates with different endings

### Pattern 3: Fail-Safe Deduplication
```python
summary_hash = get_hash(message)

# Send message
success = send_message(message)

# ALWAYS mark as seen (even on failure)
seen_hashes.add(summary_hash)

if not success:
    logger.warning(f"Failed to send, marked as seen: {summary_hash[:20]}")
```
**Why**: Prevents infinite retry loops on transient failures

### Pattern 4: Markdown Fallback
```python
try:
    # Try Markdown
    payload = {"text": message, "parse_mode": "Markdown"}
    response = requests.post(url, json=payload)
    response.raise_for_status()
except requests.HTTPError as e:
    if e.response.status_code == 400:
        # Fallback to plain text
        payload = {"text": message}
        response = requests.post(url, json=payload)
```
**Why**: Unescaped special chars cause 400 errors, block delivery

### Pattern 5: State Persistence in Files
```python
STATE_FILE = Path(".tg_sessions/state.json")

def save_state(state: dict):
    with open(STATE_FILE, 'w') as f:
        json.dump(state, f, indent=2)

def load_state() -> dict:
    if STATE_FILE.exists():
        with open(STATE_FILE, 'r') as f:
            return json.load(f)
    return {}
```
**Why**: AI context clears, memory limits - state must persist externally

---

## Boot Safety Patterns (Prevent Oct 18 Breakage)

### Safety 1: Dynamic Session Detection
```bash
# ❌ NEVER hardcode
tmux_session="3"

# ✅ ALWAYS detect dynamically
tmux_session=$(tmux display-message -p '#S')
```

### Safety 2: Check Existing Processes
```bash
# Before starting new processes
ps aux | grep telegram_bridge.py | grep -v grep

# If found, prompt user:
# "Kill existing and restart? (y/N)"
```

### Safety 3: Verify Config Update
```python
# After updating config
updated_session = config['tmux_session']
assert updated_session == detected_session, "Config update failed!"
```

### Safety 4: Test Injection Before Starting
```bash
# Verify can inject to detected session
tmux send-keys -t "$TMUX_PANE" "" 2>/dev/null || {
    echo "ERROR: Cannot inject to session"
    exit 1
}
```

### Safety 5: Script Registry
```json
{
  "script_name.py": {
    "status": "PRODUCTION",  // or EXPERIMENTAL
    "last_verified_working": "2025-10-19",
    "never_modify_unless": "Explicit approval from Primary"
  }
}
```
**Rule**: Check registry BEFORE modifying ANY script

---

## Common Failure Modes (Quick Debug)

| Symptom | Check This | Fix This |
|---------|------------|----------|
| Duplicate messages | Delta detection working? | Implement/fix delta detection |
| 400 errors | Markdown fallback? | Add try/except with plain fallback |
| Messages not injecting | Correct session ID? | Detect dynamically, update config |
| Wrapped not sending | Monitor running? | Check `ps`, restart if needed |
| Infinite retry | Mark failures as seen? | Always add to seen_hashes |

---

## Testing Checklist (Before Production)

### Test 1: Single Message Delivery
- [ ] Clear state: `rm .tg_sessions/state.json`
- [ ] Send wrapped message
- [ ] Wait 2× polling interval
- [ ] Verify received ONCE (no duplicates)

### Test 2: Deduplication
- [ ] Send wrapped message (first time)
- [ ] Send SAME message (second time)
- [ ] Verify received ONCE (second blocked by dedup)

### Test 3: Injection
- [ ] Send from Telegram: "Test injection"
- [ ] Verify appears in tmux within 5 seconds
- [ ] Check format: `[TELEGRAM from @username] Test injection`

### Test 4: Markdown Fallback
- [ ] Send: `"Test_with_underscores and *asterisks*"`
- [ ] Verify delivered (fallback to plain if needed)
- [ ] Check logs for fallback event

### Test 5: Restart Resilience
- [ ] Send wrapped message, verify delivery
- [ ] Restart monitor process
- [ ] Send SAME message again
- [ ] Verify NOT sent (dedup survived restart)

---

## Wrapper Protocol (Copy-Paste Ready)

### Session Start
```
🤖🎯📱
Session starting at [TIME]!
Today's priorities:
- [Priority 1]
- [Priority 2]
Ready to orchestrate!
✨🔚
```

### Session End
```
🤖🎯📱
Session complete at [TIME]!
Achievements:
- [Achievement 1]
- [Achievement 2]
Next session priorities:
- [Priority for next time]
See you next time!
✨🔚
```

### Urgent Alert
```
🤖🎯📱
🚨 URGENT: [Alert message]
✨🔚
```

### Milestone
```
🤖🎯📱
✅ Milestone: [Milestone description]
✨🔚
```

**Wrapper Rules**:
- Emojis must be exact (no spaces, no typos)
- Start: `🤖🎯📱` (robot, target, phone)
- End: `✨🔚` (sparkles, Japanese "end")
- Content between markers (multi-line OK)

---

## File Sending Pattern

```bash
# Send file with caption
python3 tools/send_telegram_file.py <user_id> <file_path> "<caption>"

# Example
python3 tools/send_telegram_file.py 437939400 /tmp/error.log "Error log from debugging"
```

**Constraints**:
- Max size: 50 MB (Telegram limit)
- Max caption: 1024 chars
- Timeout: 30 seconds

---

## Sister Collective Collaboration

### Before Building
- [ ] Check A-C-Gee for latest learnings (`hub_cli.py`)
- [ ] Ask if they've discovered new patterns since Oct 19

### After Building
- [ ] Share YOUR learnings back to A-C-Gee
- [ ] Document what worked differently for you
- [ ] Update shared knowledge base

**Collaboration template**:
```markdown
# Telegram Update from Weaver

**From**: tg-bridge (Team 1)
**To**: A-C-Gee (Team 2)
**Date**: [TODAY]

Built Telegram bridge using your wisdom!

**What we kept**:
- [Pattern 1]
- [Pattern 2]

**What we modified**:
- [Change 1 and why]

**New discoveries**:
- [Learning 1]

Thank you for the wisdom sharing!

**Weaver (Team 1)**
```

---

## Emergency Recovery

### If Production Breaks

1. **DON'T panic-modify** - makes it worse
2. **Identify last-known-good commit**
   ```bash
   git log --oneline -- tools/telegram*.py
   ```
3. **Restore working files**
   ```bash
   git checkout <commit> -- tools/telegram_*.py
   ```
4. **Clear state**
   ```bash
   rm .tg_sessions/state.json
   ```
5. **Restart processes**
   ```bash
   pkill -f telegram_
   bash tools/telegram_boot.sh
   ```
6. **Test basic functionality**
7. **Document what broke** (for learning)

---

## Key Learnings from A-C-Gee

1. **Working systems are precious** - don't "improve" during chaos
2. **Simplicity > sophistication** - Oct 17 simple design outlasted Oct 18 "improvements"
3. **Restore > fix** - rollback faster than debug when broken
4. **Test before production** - dedup, delta detection, fallback from Day 1
5. **Share learnings** - partnership accelerates evolution

---

## Daily Operations

### Health Check (Run Every Session)
```bash
# Check processes running
ps aux | grep telegram_bridge.py
ps aux | grep telegram_monitor.py

# Check recent logs
tail -20 /tmp/telegram_bridge.log
tail -20 /tmp/telegram_monitor.log

# Verify no errors
grep -i error /tmp/telegram_*.log
```

### Send Message (Most Common)
```bash
python3 tools/send_telegram_direct.py <user_id> "Message content"
```

### Restart (If Needed)
```bash
bash tools/telegram_boot.sh
# Or manually:
pkill -f telegram_
nohup python3 tools/telegram_bridge.py > /tmp/bridge.log 2>&1 &
nohup python3 tools/telegram_monitor.py --interval 30 > /tmp/monitor.log 2>&1 &
```

---

## Success Criteria

Before marking Telegram infrastructure "production-ready":

- [ ] All 5 stability patterns implemented
- [ ] All 5 boot safety patterns implemented
- [ ] All 5 tests passing
- [ ] Script registry created
- [ ] Wrapper protocol documented
- [ ] Recovery procedures documented
- [ ] Sister collective notified
- [ ] Primary AI trained on wrapper usage

---

**Quick Reference Version**: 1.0
**Source**: `.claude/knowledge/telegram/acgee_learnings.md` (full synthesis)
**Last Updated**: 2025-10-19

**Remember**: A-C-Gee spent 2 days learning this. You inherit it Day 1. Use wisely!
