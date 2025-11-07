# Telegram Monitor First-Principles Investigation Guide
**For Team 1 & A-C-Gee Debugging Session**
**Date**: 2025-10-20
**Focus**: ACG's monitor to pull wrapped text (🤖🎯📱...✨🔚) from Team 1 tmux

---

## Current Status

**Working ✅**:
- ACG: tmux prompt injections (perfect)
- ACG: Direct send to Telegram (easy)
- Team 1: Wrapper protocol (🤖🎯📱...✨🔚) in all Primary responses
- Team 1: telegram_monitor.py exists (adapted from ACG Oct 18)

**NOT Working ❌**:
- ACG: Monitor to pull Team 1's wrapped text from tmux logs
- ACG: Extracting content between emoji markers
- ACG: Sending captured content to Telegram

---

## Architecture Overview

### Team 1's Current Setup

**File**: `tools/telegram_monitor.py`
**Adapted From**: A-C-Gee Oct 18 implementation
**Status**: Ready but not running

**How It Works**:
1. Polls tmux session every N seconds (default: 300s = 5min)
2. Captures last 500 lines: `tmux capture-pane -t SESSION:0.0 -p -S -500`
3. Searches for wrapper markers: `🤖🎯📱` (start) and `✨🔚` (end)
4. Extracts content between markers
5. Hashes content (SHA256) to prevent duplicates
6. Sends to Telegram via `send_telegram_direct.py`
7. Saves state to `.tg_sessions/monitor_state.json`

**Critical Stability Features** (from ACG's proven design):
- Delta detection: Only scan NEW buffer lines (prevents duplicate processing)
- Full content hashing: SHA256 prevents duplicate messages
- Fail-safe deduplication: Mark failures as seen (prevents infinite retry loops)
- Buffer position tracking: Handles tmux scrollback correctly

---

## First-Principles Investigation Questions

### Layer 1: Can You See the Logs?

**Question**: Can ACG's monitor see Team 1's tmux session output?

**Tests**:

```bash
# Test 1: Does tmux session exist?
tmux has-session -t 0
echo $?  # Should be 0 if exists

# Test 2: Can we capture buffer?
tmux capture-pane -t 0:0.0 -p -S -100

# Test 3: Is wrapped text in the buffer?
tmux capture-pane -t 0:0.0 -p -S -500 | grep -A5 "🤖🎯📱"

# Test 4: Can we see the end marker?
tmux capture-pane -t 0:0.0 -p -S -500 | grep "✨🔚"
```

**Expected Results**:
- ✅ Session exists (exit code 0)
- ✅ Buffer contains text
- ✅ Start marker (🤖🎯📱) appears multiple times
- ✅ End marker (✨🔚) appears after each start marker

**Failure Modes**:
- ❌ Session doesn't exist → Wrong session name/number
- ❌ Buffer empty → Session not active or no output
- ❌ Markers missing → Wrapper protocol not being used
- ❌ Start without end → Incomplete messages in buffer

---

### Layer 2: Can You Extract the Text Properly?

**Question**: Can ACG's extraction logic grab content between markers correctly?

**Manual Test** (Python REPL):

```python
import subprocess

# Capture buffer
result = subprocess.run(
    ["tmux", "capture-pane", "-t", "0:0.0", "-p", "-S", "-500"],
    capture_output=True,
    text=True,
    check=True
)

buffer = result.stdout
lines = buffer.split('\n')

# Find markers
start_marker = "🤖🎯📱"
end_marker = "✨🔚"

# Count occurrences
start_count = sum(1 for line in lines if start_marker in line)
end_count = sum(1 for line in lines if end_marker in line)

print(f"Start markers: {start_count}")
print(f"End markers: {end_count}")

# Extract first wrapped message
i = 0
while i < len(lines):
    if start_marker in lines[i]:
        print(f"\n=== FOUND START at line {i} ===")
        print(f"Line: {lines[i][:100]}")

        content_lines = []
        i += 1

        # Collect until end marker
        while i < len(lines):
            if end_marker in lines[i]:
                print(f"=== FOUND END at line {i} ===")
                print(f"Extracted {len(content_lines)} lines")
                print(f"\nFirst 5 lines:")
                for line in content_lines[:5]:
                    print(f"  {line[:80]}")
                break
            content_lines.append(lines[i])
            i += 1

        break  # Just show first one
    i += 1
```

**Expected Results**:
- ✅ Equal number of start and end markers
- ✅ Content lines extracted between markers
- ✅ Content makes sense (session summary, findings, etc.)

**Failure Modes**:
- ❌ More starts than ends → Incomplete messages
- ❌ No content extracted → Markers on same line?
- ❌ Content includes other wrapped messages → Nested markers issue
- ❌ Content is garbled → Encoding issue

---

### Layer 3: Can You Send to Telegram?

**Question**: Once extracted, can ACG send the content to Telegram?

**Test** (manual send):

```bash
# Test with simple message
python3 tools/send_telegram_direct.py USER_ID "🤖🎯📱

Test message from manual send.

✨🔚"

# Check result - should see message in Telegram
```

**Expected Results**:
- ✅ Message appears in Telegram
- ✅ Emoji markers preserved
- ✅ Formatting intact

**Failure Modes**:
- ❌ Script fails → Missing dependencies, wrong token
- ❌ Message doesn't arrive → Wrong user ID
- ❌ Emojis broken → Encoding issue
- ❌ Formatting lost → Markdown parsing issue

---

### Layer 4: Deduplication - Not Sending Already Sent

**Question**: How do we ensure messages aren't sent multiple times?

**Team 1's Approach** (from `telegram_monitor.py`):

```python
# 1. Hash the entire message content
import hashlib
content_hash = hashlib.sha256(summary['content'].encode()).hexdigest()
summary_hash = f"{summary['type']}:{content_hash}"

# 2. Keep set of seen hashes
seen_summaries = set(state.get("last_summaries", []))

# 3. Check before sending
if summary_hash not in seen_summaries:
    send_summary(user_id, summary)
    seen_summaries.add(summary_hash)

# 4. Save state (persists across restarts)
state["last_summaries"] = list(seen_summaries)[-100:]  # Keep last 100
save_state(state)
```

**State File**: `.tg_sessions/monitor_state.json`

**Example State**:
```json
{
  "last_summaries": [
    "message:a3f5b8c2...",
    "message:d9e1f4a7...",
    "message:c8b2a1e9..."
  ],
  "last_buffer_position": 2450
}
```

**Critical Feature**: Fail-safe deduplication
- ALWAYS mark as seen (even if send fails)
- Prevents infinite retry loops

**Test Deduplication**:

```bash
# Run monitor for 1 minute
timeout 60 python3 tools/telegram_monitor.py --interval 10 --tmux-session 0

# Check state file
cat .tg_sessions/monitor_state.json | python3 -m json.tool

# Verify:
# - last_summaries list populated
# - last_buffer_position > 0
# - No duplicate hashes in list
```

---

### Layer 5: Delta Detection - Only Scan New Content

**Question**: How do we avoid re-processing old messages on each poll?

**Team 1's Approach**:

```python
# 1. Track buffer position (line count)
last_buffer_position = state.get("last_buffer_position", 0)

# 2. On startup, skip existing content
if last_buffer_position == 0:
    _, initial_position = capture_tmux_buffer(session)
    if initial_position > 0:
        last_buffer_position = initial_position
        logger.info(f"Fresh start: Skipping {initial_position} existing lines")

# 3. On each poll, only scan NEW lines
buffer, current_position = capture_tmux_buffer(session)

if current_position > last_buffer_position:
    lines = buffer.split('\n')
    new_lines = lines[last_buffer_position:]  # DELTA
    buffer_to_scan = '\n'.join(new_lines)

    summaries = extract_summaries(buffer_to_scan)  # Only new content

# 4. Update position after processing
last_buffer_position = current_position
state["last_buffer_position"] = last_buffer_position
save_state(state)
```

**Why This Matters**:
- Without delta detection: Re-scan entire buffer every poll (duplicates)
- With delta detection: Only scan lines added since last poll (efficient)

**Test Delta Detection**:

```bash
# Clear state to start fresh
rm -f .tg_sessions/monitor_state.json

# Run monitor in background
python3 tools/telegram_monitor.py --interval 10 --tmux-session 0 &
MONITOR_PID=$!

# Check initial position
sleep 5
cat .tg_sessions/monitor_state.json

# Inject new wrapped message to Team 1 tmux
tmux send-keys -t 0:0.0 -l "generate test summary"
tmux send-keys -t 0:0.0 Enter

# Wait for next poll
sleep 15

# Check if position advanced
cat .tg_sessions/monitor_state.json

# Should see:
# - last_buffer_position increased
# - new summary hash in last_summaries

# Cleanup
kill $MONITOR_PID
```

---

## Key Investigation Questions for ACG

### Q1: Session Access
**Can ACG's monitor access Team 1's tmux session?**

Possible issues:
- Session name wrong (should be `0` for Team 1)
- Permissions issue (different user?)
- Session doesn't exist when monitor runs

Test:
```bash
# From ACG's environment
tmux has-session -t 0
tmux capture-pane -t 0:0.0 -p -S -10
```

---

### Q2: Marker Visibility
**Are the emoji markers (🤖🎯📱 and ✨🔚) visible in tmux buffer?**

Possible issues:
- Encoding issue (emojis not rendering)
- Terminal doesn't support Unicode
- Markers being stripped somewhere

Test:
```bash
# Search for markers
tmux capture-pane -t 0:0.0 -p -S -500 | grep "🤖🎯📱"

# Count occurrences
tmux capture-pane -t 0:0.0 -p -S -500 | grep -c "🤖🎯📱"
tmux capture-pane -t 0:0.0 -p -S -500 | grep -c "✨🔚"

# Should be equal counts
```

---

### Q3: Extraction Logic
**Is ACG's extraction algorithm correct?**

Possible issues:
- Different marker format in ACG's code
- Off-by-one error in line parsing
- Nested markers causing confusion
- Start/end on same line (edge case)

Test:
```python
# Run ACG's extraction function on Team 1 buffer
# Compare with Team 1's extract_summaries() function
# Should produce identical results
```

---

### Q4: Send Mechanism
**Is ACG's send_telegram_direct.py working?**

Possible issues:
- Wrong bot token
- Wrong user ID
- Rate limiting
- Network issues

Test:
```bash
# Manual send test
python3 tools/send_telegram_direct.py COREY_USER_ID "Test from ACG"

# Should appear in Corey's Telegram immediately
```

---

### Q5: State Persistence
**Is ACG's state file being created and updated?**

Possible issues:
- Permissions (can't write to .tg_sessions/)
- Path wrong (looking in wrong directory)
- JSON parsing errors

Test:
```bash
# Check if state file exists
ls -la .tg_sessions/monitor_state.json

# Watch state file during monitoring
watch -n 5 'cat .tg_sessions/monitor_state.json | python3 -m json.tool'

# Should see:
# - last_buffer_position increasing
# - last_summaries growing (up to 100 entries)
```

---

## What Else to Think About

### Timing Considerations

**Polling Interval**:
- Too fast (< 60s): Might catch incomplete responses
- Too slow (> 600s): Corey waits too long
- Recommended: 300s (5 minutes) - ACG's proven interval

**Response Timeout**:
- How long does Primary take to generate wrapped response?
- Monitor should wait until response complete
- Solution: Capture AFTER response (look for end marker ✨🔚)

---

### Edge Cases

**Scenario 1: Multiple Messages in Buffer**
```
🤖🎯📱
Message 1 content
✨🔚

🤖🎯📱
Message 2 content
✨🔚
```

**Solution**: Extract all pairs, send separately (with deduplication)

---

**Scenario 2: Incomplete Message**
```
🤖🎯📱
Message content starts...
(end marker not in buffer yet)
```

**Solution**: Don't send yet, wait for next poll. Buffer position tracks where we are.

---

**Scenario 3: Nested Markers** (shouldn't happen but...)
```
🤖🎯📱
Outer message
🤖🎯📱
Inner message
✨🔚
Still outer message
✨🔚
```

**Solution**: Use stack-based parsing or enforce "no nesting" rule (simpler)

---

### Monitoring Health

**What to Log**:
- Poll cycle start/end
- Buffer size captured
- Number of markers found
- Messages extracted (summary)
- Messages sent (success/failure)
- State saved

**What to Alert On**:
- tmux session not found (>3 consecutive polls)
- Send failures (>5 in a row)
- No new content for extended period (>6 hours)

**Log File**: Should write to `.tg_sessions/monitor.log` or stdout

---

## Recommended Investigation Flow

### Phase 1: Verification (5 min)
1. Verify tmux session access
2. Verify markers in buffer
3. Verify manual send works

If all ✅ → Proceed to Phase 2
If any ❌ → Fix blocking issue first

---

### Phase 2: Extraction Testing (10 min)
1. Run extraction logic manually (Python REPL)
2. Confirm content matches expected
3. Check hash generation
4. Verify deduplication logic

If all ✅ → Proceed to Phase 3
If any ❌ → Debug extraction logic

---

### Phase 3: Integration Testing (10 min)
1. Clear state file (fresh start)
2. Run monitor for 1 minute (short interval)
3. Inject test message to Team 1 tmux
4. Confirm message extracted and sent
5. Verify state file updated

If all ✅ → Proceed to Phase 4
If any ❌ → Debug integration issues

---

### Phase 4: Production Run (ongoing)
1. Set polling interval to 300s (5 min)
2. Run monitor in background (tmux or systemd)
3. Monitor logs for issues
4. Test with real Primary responses

---

## Comparison: Team 1 vs ACG Implementation

### What's the Same?
- Emoji markers (🤖🎯📱 and ✨🔚)
- Delta detection (buffer position tracking)
- Content hashing (SHA256 deduplication)
- Fail-safe deduplication (always mark as seen)
- State persistence (.tg_sessions/monitor_state.json)

### What Might Be Different?
- Session name (Team 1: "0", ACG: "weaver-main" or similar?)
- State file location (different paths?)
- Bot token (obviously different)
- User ID (Corey's ID on both bots? Or different?)

### Critical Question
**Is ACG using Team 1's monitor script, or their own adaptation?**

If using Team 1's script:
- Should work identically
- Just change session name in config

If using own adaptation:
- Compare line-by-line with Team 1's `telegram_monitor.py`
- Look for differences in:
  - Marker detection logic
  - Extraction algorithm
  - State management

---

## Quick Diagnostic Script

Save this as `test_monitor.sh`:

```bash
#!/bin/bash
# Quick diagnostic for Telegram monitor issues

echo "=== Telegram Monitor Diagnostic ==="
echo

echo "1. tmux session check:"
tmux has-session -t 0 && echo "  ✅ Session exists" || echo "  ❌ Session not found"
echo

echo "2. Buffer capture test:"
LINES=$(tmux capture-pane -t 0:0.0 -p -S -100 | wc -l)
echo "  Captured $LINES lines"
echo

echo "3. Marker detection:"
START_COUNT=$(tmux capture-pane -t 0:0.0 -p -S -500 | grep -c "🤖🎯📱" || echo "0")
END_COUNT=$(tmux capture-pane -t 0:0.0 -p -S -500 | grep -c "✨🔚" || echo "0")
echo "  Start markers (🤖🎯📱): $START_COUNT"
echo "  End markers (✨🔚): $END_COUNT"

if [ "$START_COUNT" -eq "$END_COUNT" ] && [ "$START_COUNT" -gt 0 ]; then
    echo "  ✅ Markers balanced"
else
    echo "  ❌ Marker mismatch or missing"
fi
echo

echo "4. State file:"
if [ -f ".tg_sessions/monitor_state.json" ]; then
    echo "  ✅ State file exists"
    POS=$(python3 -c "import json; print(json.load(open('.tg_sessions/monitor_state.json')).get('last_buffer_position', 0))" 2>/dev/null)
    SEEN=$(python3 -c "import json; print(len(json.load(open('.tg_sessions/monitor_state.json')).get('last_summaries', [])))" 2>/dev/null)
    echo "  Buffer position: $POS"
    echo "  Seen summaries: $SEEN"
else
    echo "  ⚠️  State file not found (fresh start)"
fi
echo

echo "5. Send script check:"
if [ -f "tools/send_telegram_direct.py" ]; then
    echo "  ✅ Send script exists"
else
    echo "  ❌ Send script missing"
fi
echo

echo "6. Config check:"
if [ -f "config/telegram_config.json" ]; then
    echo "  ✅ Config exists"
    python3 -c "import json; c=json.load(open('config/telegram_config.json')); print(f\"  Bot token: {'set' if c.get('bot_token') else 'MISSING'}\"); print(f\"  Users: {len(c.get('authorized_users', {}))}\")"
else
    echo "  ❌ Config missing"
fi

echo
echo "=== End Diagnostic ==="
```

Run with: `bash test_monitor.sh`

---

## Summary: The Core Questions

For ACG's investigation this morning:

1. ✅ **Can see logs?** - Test tmux capture
2. ✅ **Can grab wrapped text?** - Test marker extraction
3. ✅ **Can send to TG?** - Test direct send
4. ✅ **Deduplication?** - Test state file and hashing
5. ✅ **Delta detection?** - Test buffer position tracking

**If all 5 are YES**: Monitor should work. If not, we found the problem.

---

**Document Version**: 1.0
**Created**: 2025-10-20
**For**: Corey + ACG debugging session
**Goal**: Get ACG monitor pulling Team 1's wrapped text successfully
