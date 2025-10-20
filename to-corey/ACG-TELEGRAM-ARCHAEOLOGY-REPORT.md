# A-C-Gee Telegram Implementation: Archaeological Analysis

**Date**: 2025-10-18
**Analyst**: code-archaeologist  
**Purpose**: Learn from A-C-Gee's patterns before building Team 1 version
**A-C-Gee Repository**: `/home/corey/projects/AI-CIV/grow_gemini_deepresearch` (READ-ONLY)

---

## Executive Summary

A-C-Gee built a sophisticated 4-layer Telegram architecture using **tmux injection** as the core pattern - **NO direct Anthropic API calls**. This zero-cost design reuses existing AI context by injecting Telegram messages into their running tmux session.

### What Worked Well
✅ **Zero API costs** - tmux injection reuses existing AI session  
✅ **Context preservation** - Full conversation history maintained  
✅ **4-layer separation** - Input, output, monitoring, agent specialist clearly defined  
✅ **Automatic summaries** - Monitor detects emoji-wrapped content and auto-sends  
✅ **Graceful fallbacks** - Markdown errors fall back to plain text  
✅ **File attachments** - Send documents, images, logs (50MB limit)

### What Destabilized
❌ **Markdown parsing** - Special characters caused 400 Bad Request errors  
❌ **Duplicate detection** - Weak hashing (first 100 chars) allowed duplicates  
❌ **Buffer scanning** - Scanned entire 500-line history every poll → 12+ duplicate messages  
❌ **Infinite retries** - Failed sends retried forever every poll cycle  
❌ **Context clear vulnerability** - System broke after context clear (likely config/session loss)

### Key Learnings for Team 1
1. **Use plain text by default** - Markdown only when necessary and properly escaped
2. **Hash full content** - SHA256 of entire message prevents duplicates  
3. **Delta detection** - Track buffer position, only scan NEW lines  
4. **Mark failures as seen** - Prevent infinite retry loops  
5. **Build stability from Day 1** - Don't wait for production issues to add deduplication

---

## Component Analysis

### 1. telegram_bridge.py (479 lines)

**Purpose**: Bidirectional Telegram ↔ tmux bridge (runs as daemon)

**Key Implementation**:

```python
class TelegramBridge:
    """Telegram bridge to Primary AI via tmux injection."""
    
    def inject_to_tmux(self, message: str, username: str = "user") -> bool:
        """Inject message to Primary AI tmux session."""
        # Format with Telegram indicator
        formatted = f"[TELEGRAM from @{username}] {message}"
        
        # Send using literal mode (-l) for special characters
        subprocess.run(
            ["tmux", "send-keys", "-t", self.tmux_pane, "-l", formatted],
            check=True, timeout=5
        )
        
        # Press Enter to submit
        subprocess.run(
            ["tmux", "send-keys", "-t", self.tmux_pane, "Enter"],
            check=True, timeout=5
        )
        
    def capture_tmux_response(self, wait_seconds: Optional[int] = None) -> str:
        """Capture response from tmux session after waiting."""
        time.sleep(wait_seconds or self.response_timeout)
        
        # Capture last 100 lines from tmux pane
        result = subprocess.run(
            ["tmux", "capture-pane", "-t", self.tmux_pane, "-p", "-S", "-100"],
            capture_output=True, text=True, check=True, timeout=5
        )
        
        # Extract everything after our injected prompt marker
        lines = result.stdout.split('\n')
        # ... parsing logic ...
```

**Dependencies**:
- `python-telegram-bot>=20.0` - Async Telegram Bot API wrapper
- `python-dotenv>=1.0.0` - Environment variable management
- Standard library: `asyncio`, `subprocess`, `json`, `logging`, `pathlib`

**Key Patterns**:
1. **Literal mode injection** - Uses `tmux send-keys -l` to handle special characters safely
2. **Fixed timeout** - Waits N seconds before capturing (default 10s)
3. **Simple response parsing** - Finds `[TELEGRAM from @...]` marker, captures everything after
4. **Session persistence** - Saves user metadata to `.tg_sessions/{user_id}.json`

**Gotchas**:
- **Fixed timeout may be too short or too long** - No way to detect actual completion
- **Response parsing is fragile** - Captures last 100 lines, may include unrelated output
- **No streaming** - User waits full timeout even if AI responds quickly
- **Single tmux session** - All users share same AI context (privacy concern for multi-user)

**Team 1 Adaptation**:
- ✅ **Keep**: Literal mode injection, session metadata pattern
- 🔄 **Improve**: Add smart completion detection (watch for tool usage end)
- 🔄 **Improve**: Better response boundary detection (unique markers?)
- 🔄 **Improve**: Consider per-user session isolation (security)

---

### 2. telegram_monitor.py (342 lines)

**Purpose**: Polls tmux buffer for emoji-wrapped summaries, auto-sends to Telegram

**Key Implementation**:

```python
# Detection markers
START_MARKER = "🤖🎯📱"
END_MARKER = "✨🔚"

def capture_tmux_buffer(session: str) -> tuple:
    """Capture tmux buffer content."""
    result = subprocess.run(
        ["tmux", "capture-pane", "-t", f"{session}:0.0", "-p", "-S", "-500"],
        capture_output=True, text=True, check=True, timeout=5
    )
    lines = result.stdout.split('\n')
    return result.stdout, len(lines)  # Return buffer AND line count

def extract_summaries(buffer: str) -> list:
    """Extract session summaries from buffer using markers."""
    summaries = []
    lines = buffer.split('\n')
    
    i = 0
    while i < len(lines):
        if START_MARKER in lines[i]:
            content_lines = []
            i += 1
            
            while i < len(lines) and END_MARKER not in lines[i]:
                content_lines.append(lines[i])
                i += 1
                
            if content_lines:
                summary = {
                    "type": "message",
                    "content": '\n'.join(content_lines).strip(),
                    "timestamp": datetime.utcnow().isoformat() + "Z"
                }
                summaries.append(summary)
        i += 1
        
    return summaries

def get_summary_hash(summary: dict) -> str:
    """Generate unique hash for entire summary content."""
    content_hash = hashlib.sha256(summary['content'].encode()).hexdigest()
    return f"{summary['type']}:{content_hash}"

def monitor_loop(interval: int, tmux_session: str, user_id: int):
    """Main monitoring loop with delta detection."""
    state = load_state()
    seen_summaries = set(state.get("last_summaries", []))
    last_buffer_position = state.get("last_buffer_position", 0)
    
    # Initialize position on fresh start
    if last_buffer_position == 0:
        _, initial_position = capture_tmux_buffer(tmux_session)
        if initial_position > 0:
            last_buffer_position = initial_position
            logger.info(f"Fresh start: Skipping {initial_position} existing lines")
    
    while True:
        buffer, current_position = capture_tmux_buffer(tmux_session)
        
        if current_position > last_buffer_position:
            # Only scan NEW lines (delta detection)
            lines = buffer.split('\n')
            new_lines = lines[last_buffer_position:]
            buffer_to_scan = '\n'.join(new_lines)
            
            summaries = extract_summaries(buffer_to_scan)
            
            for summary in summaries:
                if is_new_summary(summary, seen_summaries):
                    success = send_summary(user_id, summary)
                    
                    # ALWAYS mark as seen (even if send failed)
                    summary_hash = get_summary_hash(summary)
                    seen_summaries.add(summary_hash)
            
            # Update position
            last_buffer_position = current_position
            save_state({"last_summaries": list(seen_summaries)[-100:], 
                       "last_buffer_position": last_buffer_position})
        
        time.sleep(interval)
```

**Dependencies**:
- `hashlib` - SHA256 for content deduplication
- `subprocess` - tmux capture-pane
- `json` - State persistence

**Key Patterns**:
1. **Emoji markers** - Simple, visually distinct, unlikely to appear naturally
2. **Delta detection** - Track last buffer position, only scan new content
3. **Full content hashing** - SHA256 prevents duplicates even with similar starts
4. **Fail-safe deduplication** - Mark as seen even on send failure (no infinite retry)
5. **State persistence** - Survives monitor restarts

**Gotchas** (FIXED in Oct 18 update):
- ❌ **Original: Scanned all 500 lines every poll** → Fixed with delta detection
- ❌ **Original: Only hashed first 100 chars** → Fixed with full SHA256
- ❌ **Original: Retried failures infinitely** → Fixed by marking failures as seen
- ❌ **Original: Markdown parse errors blocked delivery** → Fixed with plain text fallback

**Team 1 Adaptation**:
- ✅ **Keep**: Emoji marker pattern, delta detection, full hashing, fail-safe dedup
- ✅ **Keep**: 5-minute polling interval (300s default)
- 🔄 **Improve**: Consider inotify/fswatch instead of polling (real-time detection)
- 🔄 **Improve**: Add retry with exponential backoff for transient failures (but cap retries)

---

### 3. send_telegram_direct.py (187 lines)

**Purpose**: Send formatted messages with Markdown support + fallback

**Key Implementation**:

```python
def send_telegram_message(bot_token: str, user_id: int, message: str) -> bool:
    """Send message via Telegram Bot API."""
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    
    MAX_LENGTH = 4096
    
    # Auto-chunking for long messages
    if len(message) > MAX_LENGTH:
        chunks = []
        current_chunk = ""
        
        for line in message.split('\n'):
            if len(current_chunk) + len(line) + 1 > MAX_LENGTH - 100:
                if current_chunk:
                    chunks.append(current_chunk)
                    current_chunk = line
            else:
                current_chunk += '\n' + line if current_chunk else line
        
        if current_chunk:
            chunks.append(current_chunk)
        
        # Send all chunks with fallback
        for i, chunk in enumerate(chunks):
            if i > 0:
                chunk = f"(continued {i+1}/{len(chunks)})\n\n{chunk}"
            
            payload = {"chat_id": user_id, "text": chunk, "parse_mode": "Markdown"}
            
            try:
                response = requests.post(url, json=payload, timeout=10)
                response.raise_for_status()
            except requests.HTTPError as e:
                if e.response.status_code == 400:
                    # Markdown parse error - fall back to plain text
                    logger.info(f"Markdown failed for chunk {i+1}, retrying plain")
                    payload = {"chat_id": user_id, "text": chunk}
                    response = requests.post(url, json=payload, timeout=10)
                    response.raise_for_status()
    else:
        # Single message with fallback
        payload = {"chat_id": user_id, "text": message, "parse_mode": "Markdown"}
        
        try:
            response = requests.post(url, json=payload, timeout=10)
            response.raise_for_status()
            return True
        except requests.HTTPError as e:
            if e.response.status_code == 400:
                # Markdown parse error - fall back to plain text
                logger.info("Markdown parse failed, retrying as plain text")
                payload = {"chat_id": user_id, "text": message}
                response = requests.post(url, json=payload, timeout=10)
                response.raise_for_status()
                return True
```

**Dependencies**:
- `requests` - HTTP client for Telegram Bot API

**Key Patterns**:
1. **Automatic chunking** - Splits messages >4096 chars at line boundaries
2. **Markdown-first with fallback** - Try Markdown, fall back to plain on 400 error
3. **Continuation markers** - Labels chunks "(continued 2/5)" for multi-part messages
4. **Conservative chunk size** - Uses 4096-100 buffer to prevent edge cases

**Gotchas**:
- ⚠️ **Markdown special characters** - `_`, `*`, `[`, `]`, `(`, `)`, `~`, `` ` `` must be escaped
- ⚠️ **400 errors common** - Unescaped characters or malformed Markdown trigger fallback
- ⚠️ **Fallback loses formatting** - If original intent was **bold**, fallback shows raw asterisks

**Team 1 Adaptation**:
- ✅ **Keep**: Auto-chunking, fallback pattern, continuation markers
- 🔄 **Improve**: Add pre-validation of Markdown syntax before sending
- 🔄 **Improve**: Escape special characters automatically (regex replace)
- 🔄 **Improve**: Log which messages trigger fallback (metrics for debugging)

---

### 4. send_telegram_plain.py (155 lines)

**Purpose**: Safe plain-text sender (no Markdown, never fails on special chars)

**Key Implementation**:

```python
def send_telegram_message(bot_token: str, user_id: int, message: str) -> bool:
    """Send PLAIN TEXT message via Telegram Bot API."""
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    
    MAX_LENGTH = 4096
    
    # Same chunking logic as send_telegram_direct.py
    # ...
    
    payload = {
        "chat_id": user_id,
        "text": message
        # NOTE: No parse_mode - plain text only
    }
    
    response = requests.post(url, json=payload, timeout=10)
    response.raise_for_status()
    return True
```

**Dependencies**:
- `requests` - HTTP client

**Key Patterns**:
1. **Plain text only** - No `parse_mode` parameter
2. **Never fails on special chars** - Emojis, underscores, asterisks all safe
3. **Identical chunking** - Same auto-split logic as send_telegram_direct.py

**Gotchas**:
- None! This is the "safe" script that never fails.

**Team 1 Adaptation**:
- ✅ **Keep**: Entire pattern - this is production-ready
- ✅ **Use as default** - Primary AI should use this for status messages
- 🆕 **Add to skills system** - Make discoverable via capability matrix

---

### 5. send_telegram_file.py (148 lines)

**Purpose**: Send file attachments (documents, images, logs)

**Key Implementation**:

```python
def send_telegram_file(bot_token: str, user_id: int, file_path: str, caption: str = None) -> bool:
    """Send file via Telegram Bot API."""
    url = f"https://api.telegram.org/bot{bot_token}/sendDocument"
    
    file_path_obj = Path(file_path)
    
    # Validate file exists
    if not file_path_obj.exists():
        return False
    
    # Check file size (50 MB limit for bot uploads)
    file_size = file_path_obj.stat().st_size
    max_size = 50 * 1024 * 1024
    if file_size > max_size:
        print(f"ERROR: File too large ({file_size / 1024 / 1024:.2f} MB)")
        return False
    
    # Send with multipart/form-data
    with open(file_path, 'rb') as f:
        files = {
            'document': (file_path_obj.name, f, 'application/octet-stream')
        }
        
        data = {'chat_id': user_id}
        
        if caption:
            if len(caption) > 1024:
                caption = caption[:1020] + "..."
            data['caption'] = caption
            data['parse_mode'] = 'Markdown'
        
        response = requests.post(url, data=data, files=files, timeout=30)
        response.raise_for_status()
```

**Dependencies**:
- `requests` - HTTP client with multipart support

**Key Patterns**:
1. **File size validation** - Checks 50 MB limit before uploading
2. **Caption support** - Optional Markdown-formatted caption (1024 char limit)
3. **Multipart upload** - Standard HTTP multipart/form-data
4. **30s timeout** - Longer than message send (large files need time)

**Gotchas**:
- ⚠️ **50 MB hard limit** - Telegram Bot API restriction (not configurable)
- ⚠️ **Caption can have Markdown errors** - No fallback implemented for caption
- ⚠️ **No progress indication** - Large files may appear to hang

**Team 1 Adaptation**:
- ✅ **Keep**: Size validation, multipart pattern
- 🔄 **Improve**: Add caption Markdown fallback (like send_telegram_direct.py)
- 🔄 **Improve**: Add progress callback for files >5MB
- 🔄 **Improve**: Support multiple file types (photos, videos, audio)

---

### 6. tg-archi.md (Agent Manifest)

**Purpose**: Agent specialist for Telegram infrastructure

**Key Responsibilities**:
1. Send messages on behalf of Primary/other agents
2. Maintain bridge/monitor health
3. Explore new Telegram capabilities
4. Maintain canonical script registry
5. Remind Primary of wrapper protocol on every boot

**Tools**: `[Bash, Read, Write, Edit, Grep, Glob]`

**Key Patterns**:
1. **Automatic health checks** - Runs on every invocation
2. **Auto-restart dead processes** - Self-healing infrastructure
3. **Protocol reminders** - Teaching Primary best practices
4. **Memory-driven** - Maintains script registry in agent memory

**Gotchas**:
- ⚠️ **Bash tool restriction discovered** - Agent expected Bash access but didn't have it (manifest vs reality mismatch)
- ⚠️ **Breaking production systems** - Modified scripts without checking registry first

**Team 1 Adaptation**:
- ✅ **Keep**: Agent specialist pattern, health check automation
- ✅ **Keep**: Script registry concept (track PRODUCTION vs EXPERIMENTAL)
- 🔄 **Improve**: Verify tool permissions in manifest match reality
- 🔄 **Improve**: Add pre-modification checks (read registry FIRST)

---

## Destabilization Analysis

### What Happened

**Timeline** (inferred from teaching reports):
1. **Initial system working** - Bridge, monitor, send scripts all functional
2. **Context clear event** - Primary AI session restarted/cleared
3. **System destabilization** - Monitor started sending duplicate messages (12+)
4. **Markdown errors appeared** - 400 Bad Request on messages with special chars
5. **Emergency fixes** - Created send_telegram_plain.py, fixed monitor deduplication

### Root Causes

**1. Context Clear Vulnerability**
- **Hypothesis**: Session state lost when Primary AI context cleared
- **Evidence**: Teaching report mentions "destabilized after context clear"
- **Impact**: Configuration or session metadata may have been lost
- **Lesson**: Persist critical state OUTSIDE AI context (files, not memory)

**2. Weak Deduplication**
- **Original logic**: Only hashed first 100 chars of message
- **Problem**: Similar messages with different endings seen as same
- **Fix**: SHA256 hash of full content

**3. Full Buffer Scanning**
- **Original logic**: Scanned last 500 lines every poll
- **Problem**: Detected ALL wrapped messages in history, not just new ones
- **Fix**: Track buffer position, delta detection (only scan new lines)

**4. Infinite Retry Loop**
- **Original logic**: Retry failed sends forever
- **Problem**: Network blip → retry forever every 30s
- **Fix**: Mark failures as seen (fail-safe deduplication)

**5. Markdown Parse Errors**
- **Original logic**: Always use `parse_mode: "Markdown"`
- **Problem**: Special chars (`_`, `*`, etc.) cause 400 errors
- **Fix**: Fallback to plain text on 400, create plain-only variant

### Their Fixes

**Fix #1: Delta Detection** (Oct 18)
```python
# Track buffer position
last_buffer_position = state.get("last_buffer_position", 0)

# Only scan new lines since last poll
if current_position > last_buffer_position:
    new_lines = lines[last_buffer_position:]
    buffer_to_scan = '\n'.join(new_lines)
```

**Fix #2: Full Content Hashing** (Oct 18)
```python
import hashlib

def get_summary_hash(summary: dict) -> str:
    content_hash = hashlib.sha256(summary['content'].encode()).hexdigest()
    return f"{summary['type']}:{content_hash}"
```

**Fix #3: Fail-Safe Deduplication** (Oct 18)
```python
# ALWAYS mark as seen, even on failure
summary_hash = get_summary_hash(summary)
seen_summaries.add(summary_hash)

if not success:
    logger.warning(f"Failed to send, marked as seen: {summary_hash[:20]}")
```

**Fix #4: Markdown Fallback** (Oct 18)
```python
try:
    response = requests.post(url, json=payload, timeout=10)
    response.raise_for_status()
except requests.HTTPError as e:
    if e.response.status_code == 400:
        # Fallback to plain text
        payload = {"chat_id": user_id, "text": message}
        response = requests.post(url, json=payload, timeout=10)
```

**Fix #5: Plain Text Variant** (Oct 18)
- Created `send_telegram_plain.py` - no Markdown, never fails on special chars
- Recommended as default for Primary AI status messages

### Prevention for Team 1

**Build stability from Day 1 (don't wait for production issues):**

1. **Full content hashing** - Use SHA256 from first implementation
2. **Delta detection** - Track buffer position from Day 1
3. **Fail-safe deduplication** - Mark failures as seen (cap retries at 3 max)
4. **Plain text default** - Use send_telegram_plain.py unless formatting needed
5. **Pre-validate Markdown** - Check syntax before sending with parse_mode
6. **State persistence** - Store ALL critical state in files, not AI memory
7. **Health monitoring** - Auto-restart dead processes, alert on repeated failures
8. **Graceful degradation** - Fallbacks at every layer (Markdown→plain, retry→skip, etc.)

**Context clear resilience:**
- Config in files: `config/telegram_config.json`
- State in files: `.tg_sessions/monitor_state.json`, `.tg_sessions/{user_id}.json`
- Documentation in files: Quick reference guides, setup docs
- Never rely on AI memory for critical infrastructure state

---

## Adaptation Recommendations

### Keep These Patterns

**1. tmux Injection Architecture** ⭐
- **Why**: Zero API costs, reuses existing context, simple integration
- **How**: `tmux send-keys -t {pane} -l {message}` + `tmux send-keys Enter`
- **Team 1**: Adapt to our tmux session name, add completion detection

**2. Emoji Marker Protocol** ⭐
- **Why**: Visually distinct, unlikely natural occurrence, easy to detect
- **Markers**: `🤖🎯📱` (start) and `✨🔚` (end)
- **Team 1**: Use same markers for cross-team compatibility, add to CLAUDE-OPS.md

**3. 4-Layer Separation** ⭐
- **Layers**: Input (bridge), Output (send scripts), Monitor (auto-summary), Agent (tg-archi)
- **Why**: Clear responsibilities, easy debugging, independent scaling
- **Team 1**: Mirror this architecture, integrate with our agent system

**4. Plain Text by Default** ⭐
- **Why**: Never fails on special chars, reliable for status messages
- **Script**: `send_telegram_plain.py` as PRIMARY default
- **Team 1**: Make this the constitutional default (Markdown opt-in only)

**5. Automatic Chunking** ⭐
- **Why**: Handles long messages gracefully, splits at line boundaries
- **Logic**: 4096 char limit - 100 buffer, continuation markers
- **Team 1**: Use same chunking algorithm, test with 10k+ char messages

**6. State Persistence** ⭐
- **Files**: `.tg_sessions/monitor_state.json`, `.tg_sessions/{user_id}.json`
- **Why**: Survives restarts, context clears, crashes
- **Team 1**: Store in `.claude/.tg_sessions/` for consistency

**7. Delta Detection** ⭐
- **Pattern**: Track last buffer position, only scan new lines
- **Why**: Prevents duplicate detection, reduces CPU usage
- **Team 1**: Implement from Day 1 (don't wait for issues)

**8. Full Content Hashing** ⭐
- **Algorithm**: SHA256 of entire message content
- **Why**: Prevents duplicates even with similar starts
- **Team 1**: Use SHA256, store in dedup set

---

### Improve These Areas

**1. Smart Completion Detection**
- **Current**: Fixed timeout (10s wait before capture)
- **Problem**: Too short = incomplete response, too long = user waits unnecessarily
- **Team 1 Solution**: Watch for tool completion markers, idle timeout, or prompt return
- **Implementation**: Poll tmux every 0.5s, detect when AI stops generating

**2. Response Boundary Markers**
- **Current**: Captures last 100 lines, finds `[TELEGRAM from @...]` marker
- **Problem**: Fragile parsing, may capture unrelated output
- **Team 1 Solution**: Add unique start/end markers around responses
- **Implementation**: Inject `[TG_RESPONSE_START]` ... `[TG_RESPONSE_END]` wrappers

**3. Markdown Validation**
- **Current**: Try Markdown, fall back to plain on 400 error
- **Problem**: Wastes API call, user sees error in logs
- **Team 1 Solution**: Pre-validate Markdown syntax before sending
- **Implementation**: Regex check for unescaped special chars, auto-escape or warn

**4. Retry with Backoff**
- **Current**: Never retry (fail-safe dedup marks as seen)
- **Problem**: Transient network errors → permanent message loss
- **Team 1 Solution**: Retry up to 3 times with exponential backoff (1s, 2s, 4s)
- **Implementation**: Track retry count in state, mark as seen only after 3 failures

**5. Health Check Automation**
- **Current**: Manual health checks, auto-restart on invocation
- **Problem**: Downtime between agent invocations
- **Team 1 Solution**: Systemd service + watchdog timer
- **Implementation**: Create systemd units, 60s watchdog, email alert on repeated failures

**6. File Upload Progress**
- **Current**: No progress indication for large files
- **Problem**: >10MB files appear to hang
- **Team 1 Solution**: Progress callback, log upload speed
- **Implementation**: Use requests_toolbelt for multipart upload progress

**7. Caption Markdown Fallback**
- **Current**: File captions use Markdown, no fallback
- **Problem**: Caption parse error → send fails
- **Team 1 Solution**: Same fallback as message body
- **Implementation**: Try Markdown caption, catch 400, retry plain

**8. Multi-User Session Isolation**
- **Current**: Single tmux session for all users
- **Problem**: Privacy leak (users see each other's context)
- **Team 1 Solution**: Separate tmux sessions per user OR single-user authorization
- **Implementation**: For Corey-only use, single user is fine; for multi-user, spawn isolated sessions

---

### Team 1-Specific Considerations

**Integration with Skills System**

A-C-Gee doesn't have a skills system like Team 1. We need to make Telegram a discoverable skill.

**Proposal**:
```json
{
  "skill_name": "telegram-communication",
  "category": "infrastructure",
  "capabilities": [
    "send_message_plain",
    "send_message_formatted",
    "send_file",
    "auto_mirror_summaries"
  ],
  "discovery_triggers": [
    "notify Corey",
    "send Telegram",
    "mobile notification"
  ],
  "agent_owner": "tg-bridge",
  "grant_date": "2025-10-19",
  "status": "active"
}
```

**Integration Points**:
1. **AGENT-CAPABILITY-MATRIX.md** - Add telegram-communication row
2. **ACTIVATION-TRIGGERS.md** - When to delegate to tg-bridge agent
3. **CLAUDE-OPS.md** - Wake-up protocol: Send Telegram ping in Step 5
4. **Mission class** - Auto-Telegram on mission complete

**Constitutional Documents**

A-C-Gee has PRIMARY-TELEGRAM-QUICK-REFERENCE.md for their Primary AI.

**Team 1 needs**:
1. **TELEGRAM-QUICK-REFERENCE.md** - Copy-paste commands for The Conductor
2. **Update CLAUDE-OPS.md** - Add Telegram ping to wake-up protocol Step 5
3. **Update AGENT-INVOCATION-GUIDE.md** - Add tg-bridge agent invocation syntax
4. **Update FLOW-LIBRARY-INDEX.md** - Add "Telegram Notification" flow

**Wake-Up Protocol Integration**

A-C-Gee's teaching: "No wake up protocol will be complete without you waking up knowing how to do that"

**Team 1 wake-up protocol Step 5 addition**:
```bash
# Step 5: Infrastructure Activation (add after reading templates)

# Telegram ping (NEW - mobile presence)
python3 /home/corey/projects/AI-CIV/grow_openai/tools/send_telegram_plain.py \
  437939400 \
  "The Conductor online - wake-up protocol complete, ready for orchestration"
```

**Memory System Logging**

A-C-Gee has agent-specific memory directories: `memories/agents/tg-archi/`

**Team 1 should log**:
- **tg-bridge agent memory**: Delivery metrics, health checks, capability research
- **Primary memory**: When to use Telegram, wrapper protocol, troubleshooting

**Integration with capability-curator**

Team 1 has autonomous weekly skill scans. Telegram should be discovered automatically.

**File placement for discovery**:
```
/home/corey/projects/AI-CIV/grow_openai/.claude/skills/telegram-communication/
  - README.md (capability description)
  - grant.json (skill grant metadata)
  - QUICK-REFERENCE.md (usage guide)
```

---

## Code Snippets for Team 1

### Configuration Pattern

**A-C-Gee's approach** (`config/telegram_config.json`):
```json
{
  "bot_token": "YOUR_BOT_TOKEN_HERE",
  "authorized_users": {
    "437939400": {
      "name": "Corey",
      "role": "creator",
      "admin": true
    }
  },
  "tmux_session": "acgee-main",
  "tmux_pane": "acgee-main:0.0",
  "working_directory": "/home/corey/projects/AI-CIV/grow_gemini_deepresearch",
  "response_timeout": 10,
  "max_response_length": 4000
}
```

**Team 1 adaptation** (`.claude/config/telegram_config.json`):
```json
{
  "bot_token": "${TELEGRAM_BOT_TOKEN}",
  "authorized_users": {
    "437939400": {
      "name": "Corey",
      "role": "creator",
      "admin": true,
      "team": "team1"
    }
  },
  "tmux_session": "team1-primary",
  "tmux_pane": "team1-primary:0.0",
  "working_directory": "/home/corey/projects/AI-CIV/grow_openai",
  "response_timeout": 15,
  "max_response_length": 4000,
  "completion_detection": "smart",
  "health_check_interval": 60,
  "retry_max_attempts": 3,
  "retry_backoff_base": 2
}
```

**Improvements**:
- Environment variable for bot token (never commit secrets)
- Longer response timeout (Claude Code tools may be slower)
- Smart completion detection config
- Health check and retry configuration

---

### tmux Injection Pattern

**A-C-Gee's approach**:
```python
def inject_to_tmux(self, message: str, username: str = "user") -> bool:
    formatted = f"[TELEGRAM from @{username}] {message}"
    
    subprocess.run(
        ["tmux", "send-keys", "-t", self.tmux_pane, "-l", formatted],
        check=True, timeout=5
    )
    
    subprocess.run(
        ["tmux", "send-keys", "-t", self.tmux_pane, "Enter"],
        check=True, timeout=5
    )
    
    return True
```

**Team 1 adaptation**:
```python
def inject_to_tmux(self, message: str, username: str = "user", 
                   add_markers: bool = True) -> bool:
    """
    Inject message to Primary AI tmux session with optional response markers.
    
    Args:
        message: User message to inject
        username: Telegram username for context
        add_markers: If True, wrap in [TG_RESPONSE_START/END] markers
    
    Returns:
        True if injection succeeded
    """
    formatted = f"[TELEGRAM from @{username}] {message}"
    
    try:
        # Inject message with literal mode (-l) for special chars
        subprocess.run(
            ["tmux", "send-keys", "-t", self.tmux_pane, "-l", formatted],
            check=True, timeout=5, capture_output=True
        )
        
        # Press Enter to submit
        subprocess.run(
            ["tmux", "send-keys", "-t", self.tmux_pane, "Enter"],
            check=True, timeout=5, capture_output=True
        )
        
        logger.info(f"Injected message to {self.tmux_pane}: {formatted[:100]}")
        
        # If markers requested, inject response boundary markers
        if add_markers:
            self._inject_response_markers()
        
        return True
        
    except subprocess.CalledProcessError as e:
        logger.error(f"tmux injection failed: {e.stderr}")
        return False
    except subprocess.TimeoutExpired:
        logger.error("tmux injection timed out")
        return False

def _inject_response_markers(self):
    """Inject response boundary markers for clean extraction."""
    try:
        # Send invisible marker (won't confuse AI)
        subprocess.run(
            ["tmux", "send-keys", "-t", self.tmux_pane, "-l", 
             "<!-- TG_RESPONSE_START -->"],
            check=True, timeout=2
        )
    except Exception as e:
        logger.warning(f"Failed to inject response markers: {e}")
```

**Improvements**:
- Response boundary markers for clean extraction
- Better error handling with captured stderr
- Logging for debugging
- Optional marker injection

---

### Error Handling Pattern

**A-C-Gee's approach** (Markdown with fallback):
```python
try:
    response = requests.post(url, json=payload, timeout=10)
    response.raise_for_status()
    return True
except requests.HTTPError as e:
    if e.response.status_code == 400:
        # Markdown parse error - fall back to plain text
        logger.info("Markdown parse failed, retrying as plain text")
        payload = {"chat_id": user_id, "text": message}
        response = requests.post(url, json=payload, timeout=10)
        response.raise_for_status()
        return True
    else:
        raise
```

**Team 1 adaptation** (with retry and validation):
```python
def send_telegram_message(bot_token: str, user_id: int, message: str, 
                         use_markdown: bool = False, max_retries: int = 3) -> bool:
    """
    Send message via Telegram Bot API with retry and validation.
    
    Args:
        bot_token: Telegram bot token
        user_id: Telegram user ID (chat_id)
        message: Message text
        use_markdown: If True, use Markdown (with validation)
        max_retries: Max retry attempts for transient failures
    
    Returns:
        True if sent successfully
    """
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    
    # Pre-validate Markdown if requested
    if use_markdown:
        is_valid, escaped_message = validate_and_escape_markdown(message)
        if not is_valid:
            logger.warning("Invalid Markdown detected, using plain text")
            use_markdown = False
        else:
            message = escaped_message
    
    payload = {
        "chat_id": user_id,
        "text": message
    }
    
    if use_markdown:
        payload["parse_mode"] = "Markdown"
    
    # Retry with exponential backoff
    for attempt in range(max_retries):
        try:
            response = requests.post(url, json=payload, timeout=10)
            response.raise_for_status()
            
            logger.info(f"Message sent successfully to {user_id}")
            return True
            
        except requests.HTTPError as e:
            if e.response.status_code == 400 and use_markdown:
                # Markdown parse error despite validation - fall back to plain
                logger.warning("Markdown failed despite validation, retrying plain")
                payload["parse_mode"] = None  # Remove Markdown
                use_markdown = False
                continue
            elif e.response.status_code >= 500:
                # Server error - retry with backoff
                if attempt < max_retries - 1:
                    backoff = 2 ** attempt
                    logger.warning(f"Server error {e.response.status_code}, "
                                 f"retry {attempt+1}/{max_retries} after {backoff}s")
                    time.sleep(backoff)
                    continue
                else:
                    logger.error(f"Failed after {max_retries} retries: {e}")
                    return False
            else:
                # Client error (4xx) - don't retry
                logger.error(f"Client error {e.response.status_code}: {e.response.text}")
                return False
                
        except requests.RequestException as e:
            # Network error - retry with backoff
            if attempt < max_retries - 1:
                backoff = 2 ** attempt
                logger.warning(f"Network error, retry {attempt+1}/{max_retries} after {backoff}s: {e}")
                time.sleep(backoff)
                continue
            else:
                logger.error(f"Network failed after {max_retries} retries: {e}")
                return False
    
    return False

def validate_and_escape_markdown(text: str) -> tuple[bool, str]:
    """
    Validate and escape Markdown special characters.
    
    Returns:
        (is_valid, escaped_text) tuple
    """
    # Special characters that need escaping: _ * [ ] ( ) ~ ` > # + - = | { } . !
    special_chars = r'_*[]()~`>#+-=|{}.!'
    
    # Check for balanced formatting
    if text.count('*') % 2 != 0 or text.count('_') % 2 != 0:
        logger.warning("Unbalanced Markdown formatting detected")
        return False, text
    
    # Check for unclosed code blocks
    if text.count('```') % 2 != 0 or text.count('`') % 2 != 0:
        logger.warning("Unclosed code blocks detected")
        return False, text
    
    # Auto-escape special chars outside formatting contexts
    escaped = escape_markdown_v2(text)
    return True, escaped

def escape_markdown_v2(text: str) -> str:
    """Escape special characters for Telegram MarkdownV2."""
    escape_chars = r'_*[]()~`>#+-=|{}.!'
    return re.sub(f'([{re.escape(escape_chars)}])', r'\\\1', text)
```

**Improvements**:
- Pre-validation before sending
- Retry with exponential backoff for transient failures
- Distinguishes server errors (retry) from client errors (don't retry)
- Auto-escaping of special characters
- Balanced formatting detection

---

## Dependencies & Setup

### Required Libraries

**Team 1 requirements.txt** (Telegram subset):
```txt
# Telegram Bridge Dependencies
python-telegram-bot>=20.0  # Async Telegram Bot API wrapper
python-dotenv>=1.0.0       # Environment variable management
requests>=2.31.0           # HTTP client for direct API calls
requests-toolbelt>=1.0.0   # Upload progress for large files

# Standard library (no install needed):
# - asyncio (async/await support)
# - subprocess (tmux interaction)
# - json (config and session storage)
# - logging (debug and monitoring)
# - pathlib (file operations)
# - hashlib (SHA256 for deduplication)
```

### Configuration Files

**Structure for Team 1**:
```
/home/corey/projects/AI-CIV/grow_openai/
├── .claude/
│   ├── config/
│   │   └── telegram_config.json        # Bot token, authorized users
│   └── .tg_sessions/
│       ├── monitor_state.json          # Monitor dedup state
│       └── {user_id}.json              # Per-user session metadata
├── tools/
│   ├── telegram_bridge.py              # Bidirectional bridge (daemon)
│   ├── telegram_monitor.py             # Auto-summary sender (daemon)
│   ├── send_telegram_plain.py          # Plain text sender (PRIMARY default)
│   ├── send_telegram_direct.py         # Markdown sender (fallback)
│   └── send_telegram_file.py           # File attachment sender
└── .env
    └── TELEGRAM_BOT_TOKEN=XXX           # Secret (never commit)
```

### Telegram Bot Setup

**BotFather steps** (same as A-C-Gee):
1. Search `@BotFather` in Telegram
2. `/newbot` → Name: "Team 1 Conductor Bridge" → Username: `team1_conductor_bot`
3. Copy bot token → Add to `.env` as `TELEGRAM_BOT_TOKEN=XXX`
4. Get Corey's user ID: Search `@userinfobot` → `/start` → Copy ID (437939400)
5. Add to `telegram_config.json` authorized_users

**Configuration template** (`.claude/config/telegram_config.json`):
```json
{
  "bot_token": "${TELEGRAM_BOT_TOKEN}",
  "authorized_users": {
    "437939400": {
      "name": "Corey",
      "role": "creator",
      "admin": true,
      "team": "team1"
    }
  },
  "tmux_session": "team1-primary",
  "tmux_pane": "team1-primary:0.0",
  "working_directory": "/home/corey/projects/AI-CIV/grow_openai",
  "response_timeout": 15,
  "max_response_length": 4000
}
```

---

## Testing Strategy

### What A-C-Gee Tested

**Manual testing**:
1. Send `/start` to bot → Check welcome message
2. Send `/ping` → Check pong response
3. Send message → Check tmux injection + response capture
4. Wrap message in emojis → Check monitor detects and auto-sends

**Test script** (`test_telegram_monitor_fixes.sh`):
```bash
#!/bin/bash
# Clear state
rm -f .tg_sessions/monitor_state.json

# Send test wrapped message
tmux send-keys -t 0:0 "echo '🤖🎯📱'" Enter
tmux send-keys -t 0:0 "echo 'Test message 1'" Enter
tmux send-keys -t 0:0 "echo '✨🔚'" Enter

# Run monitor for 10s
timeout 10 python3 tools/telegram_monitor.py --interval 5

# Verify delivery count (should be 1)
```

**Gotchas they missed initially**:
- Didn't test duplicate detection thoroughly → 12+ duplicates in production
- Didn't test Markdown special chars → 400 errors in production
- Didn't test context clear recovery → destabilization on restart

### What Team 1 Should Test

**Unit Tests** (`tests/test_telegram.py`):
```python
import pytest
from tools.send_telegram_plain import send_telegram_message
from tools.telegram_monitor import get_summary_hash, extract_summaries

def test_deduplication_full_hash():
    """Verify SHA256 hashes entire content."""
    summary1 = {"type": "message", "content": "Same start, different end A"}
    summary2 = {"type": "message", "content": "Same start, different end B"}
    
    hash1 = get_summary_hash(summary1)
    hash2 = get_summary_hash(summary2)
    
    assert hash1 != hash2, "Full hash should differ for different endings"

def test_delta_detection():
    """Verify monitor only scans new lines."""
    # Simulate buffer growth
    old_buffer = "line 1\nline 2\nline 3"
    new_buffer = "line 1\nline 2\nline 3\nline 4\nline 5"
    
    # Only extract from delta
    old_lines = old_buffer.split('\n')
    new_lines = new_buffer.split('\n')
    delta = new_lines[len(old_lines):]
    
    assert delta == ["line 4", "line 5"]

def test_markdown_fallback():
    """Verify fallback to plain text on Markdown error."""
    # Message with unescaped underscore (Markdown syntax)
    message = "Test_message_with_underscores"
    
    # Should attempt Markdown, fall back to plain
    # (Mock requests.post to simulate 400 error)
    # ...

def test_chunking_boundary():
    """Verify chunking respects line boundaries."""
    long_message = "Line 1\n" * 1000  # ~7000 chars
    
    # Send should auto-chunk
    chunks = chunk_message(long_message, max_length=4096)
    
    assert len(chunks) >= 2
    for chunk in chunks:
        assert len(chunk) <= 4096
        assert not chunk.endswith("Line ")  # Should split at \n
```

**Integration Tests**:
```python
def test_round_trip_tmux():
    """Test message injection → AI response → Telegram delivery."""
    # Inject message to tmux
    inject_to_tmux("Test message", username="pytest")
    
    # Wait for response
    time.sleep(5)
    
    # Capture response
    response = capture_tmux_response()
    
    assert "[TELEGRAM from @pytest]" in response
    assert len(response) > 0

def test_monitor_auto_send():
    """Test monitor detects wrapped message and auto-sends."""
    # Clear state
    Path(".tg_sessions/monitor_state.json").unlink(missing_ok=True)
    
    # Inject wrapped message to tmux
    subprocess.run(["tmux", "send-keys", "-t", "team1-primary:0.0", "-l",
                   "🤖🎯📱\nMonitor test message\n✨🔚"])
    subprocess.run(["tmux", "send-keys", "-t", "team1-primary:0.0", "Enter"])
    
    # Run monitor for 10s
    subprocess.run(["timeout", "10", "python3", "tools/telegram_monitor.py",
                   "--interval", "5"])
    
    # Check state file shows 1 message sent
    state = json.loads(Path(".tg_sessions/monitor_state.json").read_text())
    assert len(state["last_summaries"]) == 1
```

**Stability Tests** (run before production):
```python
def test_duplicate_prevention():
    """Send same wrapped message 10 times, verify only 1 Telegram delivery."""
    for i in range(10):
        inject_wrapped_message("Duplicate test")
    
    # Run monitor
    # ...
    
    # Verify state shows only 1 unique hash
    state = load_state()
    assert len(state["last_summaries"]) == 1

def test_context_clear_recovery():
    """Simulate context clear, verify system recovers."""
    # Start monitor
    # Send wrapped message → verify delivery
    # Simulate context clear (clear state files)
    # Restart monitor
    # Send wrapped message → verify delivery (no duplicates)
    # ...

def test_network_failure_retry():
    """Verify retry with backoff on transient network errors."""
    # Mock requests.post to fail 2 times, succeed on 3rd
    # Send message
    # Verify 3 attempts made
    # Verify message eventually delivered
    # ...
```

---

## Integration with Team 1 Infrastructure

### Skills System

**Skill Grant** (`.claude/skills/telegram-communication/grant.json`):
```json
{
  "skill_name": "telegram-communication",
  "category": "infrastructure",
  "grant_date": "2025-10-19",
  "granted_to": "the-conductor",
  "capabilities": [
    "send_message_plain",
    "send_message_formatted",
    "send_file_attachment",
    "auto_mirror_summaries",
    "bidirectional_messaging"
  ],
  "owner_agent": "tg-bridge",
  "status": "active",
  "discovery_keywords": [
    "telegram",
    "notify corey",
    "mobile notification",
    "send message",
    "mirror to phone"
  ],
  "quick_reference": ".claude/skills/telegram-communication/QUICK-REFERENCE.md"
}
```

**Skill README** (`.claude/skills/telegram-communication/README.md`):
```markdown
# Telegram Communication Skill

**Status**: Active  
**Owner**: tg-bridge agent  
**Granted**: 2025-10-19

## Capabilities

1. **send_message_plain** - Send plain text to Corey's Telegram (safe, never fails)
2. **send_message_formatted** - Send Markdown-formatted messages (with fallback)
3. **send_file_attachment** - Send files up to 50MB (docs, logs, images)
4. **auto_mirror_summaries** - Automatically send emoji-wrapped summaries
5. **bidirectional_messaging** - Receive messages from Corey via Telegram

## Usage

**Send plain text** (recommended default):
```bash
python3 tools/send_telegram_plain.py 437939400 "Message text"
```

**Delegate to agent**:
```
Task(tg-bridge):
  Send message to Corey: "Mission complete - handoff ready"
```

**Auto-mirror** (wrap in emojis):
```
🤖🎯📱
Your summary content here
✨🔚
```

## When to Use

- Session start/end notifications
- Achievement alerts
- Error/warning notifications
- Mission completion summaries
- File sharing (handoffs, logs)

## Activation Triggers

See `.claude/templates/ACTIVATION-TRIGGERS.md` for tg-bridge agent.
```

**AGENT-CAPABILITY-MATRIX.md addition**:
```markdown
| Agent | ... | Telegram | ... |
|-------|-----|----------|-----|
| tg-bridge | ... | ✅ PRIMARY | ... |
| the-conductor | ... | ✅ (via delegation) | ... |
| human-liaison | ... | ✅ (for notifications) | ... |
```

**ACTIVATION-TRIGGERS.md addition**:
```markdown
### tg-bridge

**Invoke When**:
- Need to send Telegram message to Corey
- Need to send file attachment via Telegram
- Telegram infrastructure health check needed
- Exploring new Telegram capabilities

**Don't Invoke When**:
- Simple wake-up ping (The Conductor can do directly)
- Message already wrapped in emojis (monitor handles auto)

**Escalate When**:
- Bridge/monitor down for >30 minutes
- Bot token invalid
- Corey reports missing notifications
```

### Wake-Up Protocol

**CLAUDE-OPS.md Step 5 addition** (Infrastructure Activation):
```markdown
### ☑️ Step 5: Infrastructure Activation (3 min)

**Read infrastructure docs**:
```bash
cat /home/corey/projects/AI-CIV/grow_openai/.claude/templates/ACTIVATION-TRIGGERS.md
cat /home/corey/projects/AI-CIV/grow_openai/.claude/templates/AGENT-OUTPUT-TEMPLATES.md
cat /home/corey/projects/AI-CIV/grow_openai/.claude/flows/FLOW-LIBRARY-INDEX.md
cat /home/corey/projects/AI-CIV/grow_openai/.claude/AGENT-CAPABILITY-MATRIX.md
```

**Send Telegram ping** (NEW - mobile presence):
```bash
cd /home/corey/projects/AI-CIV/grow_openai
python3 tools/send_telegram_plain.py 437939400 \
  "The Conductor online - wake-up protocol complete, ready for orchestration"
```

**Why**: Corey receives mobile notification that session started. "No wake-up protocol is complete without you knowing how to do that."
```

### Constitutional Documents

**Create TELEGRAM-QUICK-REFERENCE.md**:
```markdown
# The Conductor - Telegram Quick Reference

**Status**: Production Ready
**Date**: 2025-10-19

## The Simple Pattern (USE THIS)

### Session Start Notification
```bash
cd /home/corey/projects/AI-CIV/grow_openai
python3 tools/send_telegram_plain.py 437939400 \
  "The Conductor online - session started"
```

### Session End Notification
```bash
python3 tools/send_telegram_plain.py 437939400 \
  "Session complete - handoff ready at to-corey/HANDOFF-$(date +%Y%m%d).md"
```

### Achievement Notification
```bash
python3 tools/send_telegram_plain.py 437939400 \
  "Achievement: [brief description]"
```

## Auto-Mirror Pattern

**Wrap summaries in emoji markers for automatic Telegram delivery**:
```
🤖🎯📱

Your summary content here.
Can be multiple paragraphs.

✨🔚
```

**Monitor detects these markers and auto-sends to Corey's Telegram.**

## Delegation Pattern

**For complex formatted messages or file attachments**:
```
Task(tg-bridge):
  Context: Mission ending, significant achievements
  Task: Send formatted session summary to Corey via Telegram
  Content: [achievements, metrics, next steps]
  Format: Use Markdown for readability
```

## Troubleshooting

**Error: Config file not found**
- Fix: `cd /home/corey/projects/AI-CIV/grow_openai`

**Error: 400 Bad Request**
- Cause: Using send_telegram_direct.py with special characters
- Fix: Use send_telegram_plain.py instead

**Message not received**
- Check bridge/monitor running: `ps aux | grep telegram`
- Check logs: `tail -20 /tmp/telegram_bridge.log`
- Delegate to tg-bridge for health check

---

**Remember**: Telegram is existential infrastructure. Every message strengthens the bridge to Corey's awareness.
```

### Memory System

**tg-bridge agent memory structure**:
```
/home/corey/projects/AI-CIV/grow_openai/.claude/memory/agents/tg-bridge/
├── patterns/
│   ├── successful-formatting.md
│   └── auto-mirror-best-practices.md
├── references/
│   ├── telegram-api-capabilities.md
│   └── markdown-escaping-rules.md
├── fixes/
│   ├── deduplication-algorithm.md
│   └── completion-detection.md
└── performance_log.json
```

**What to preserve**:
- Delivery success rate metrics
- Common Markdown escaping issues
- Completion detection accuracy
- Health check findings
- Capability research notes

---

## Timeline Estimate for Team 1

Based on A-C-Gee's experience and our improvements:

### Phase 1: Basic Sending (4-6 hours)
- ✅ Install dependencies (`python-telegram-bot`, `requests`)
- ✅ Create bot via BotFather, get token
- ✅ Implement `send_telegram_plain.py` (copy from A-C-Gee, adapt paths)
- ✅ Create config template (`.claude/config/telegram_config.json`)
- ✅ Test basic sending (exit code 0, Corey receives message)
- ✅ Add to wake-up protocol (CLAUDE-OPS.md Step 5)

**Deliverable**: The Conductor can send plain text Telegram messages on wake-up

### Phase 2: Bidirectional Bridge (6-8 hours)
- ✅ Implement `telegram_bridge.py` (adapt from A-C-Gee)
- ✅ Add smart completion detection (poll tmux every 0.5s, detect idle)
- ✅ Add response boundary markers for clean extraction
- ✅ Test round-trip (Corey → Telegram → tmux → AI → capture → Telegram → Corey)
- ✅ Create systemd service (auto-start bridge on boot)

**Deliverable**: Corey can message Team 1 via Telegram, get responses

### Phase 3: Auto-Summary Monitor (4-6 hours)
- ✅ Implement `telegram_monitor.py` with delta detection from Day 1
- ✅ Use SHA256 full content hashing (no weak dedup)
- ✅ Implement fail-safe deduplication (mark failures as seen, max 3 retries)
- ✅ Test emoji marker detection (`🤖🎯📱` ... `✨🔚`)
- ✅ Create systemd service (auto-start monitor on boot)

**Deliverable**: Emoji-wrapped summaries auto-send to Telegram without The Conductor action

### Phase 4: Stability & Polish (6-8 hours)
- ✅ Implement `send_telegram_direct.py` with Markdown pre-validation
- ✅ Implement `send_telegram_file.py` with progress callbacks
- ✅ Add retry with exponential backoff (max 3 attempts, 2^n backoff)
- ✅ Create health check automation (60s watchdog, auto-restart)
- ✅ Write comprehensive tests (unit, integration, stability)
- ✅ Create tg-bridge agent manifest
- ✅ Document in skills system

**Deliverable**: Production-ready Telegram infrastructure with self-healing

### Phase 5: Integration & Documentation (3-4 hours)
- ✅ Update CLAUDE-OPS.md (wake-up protocol)
- ✅ Update AGENT-CAPABILITY-MATRIX.md
- ✅ Update ACTIVATION-TRIGGERS.md
- ✅ Create TELEGRAM-QUICK-REFERENCE.md
- ✅ Create skill grant (telegram-communication)
- ✅ Integration audit (ensure discoverable)

**Deliverable**: Fully integrated, documented, discoverable Telegram capability

---

**Total Estimate**: 23-32 hours (3-4 days of focused work)

**With buffer for unknowns**: 30-40 hours (5-7 days)

**Critical Path**: Phases 1 → 2 → 3 (basic → bidirectional → auto-summary)  
**Parallel Work**: Phase 4 stability improvements can overlap with Phase 3  
**Final Step**: Phase 5 integration audit before marking "done"

---

## Recommended Next Steps

### Immediate (Today/Tomorrow)
1. ✅ **Review this archaeological report** - Understand A-C-Gee's patterns
2. ✅ **Create Telegram bot** - @BotFather setup, get token
3. ✅ **Test send_telegram_plain.py** - Adapt from A-C-Gee, send test message
4. ✅ **Add to wake-up protocol** - Immediate value, builds habit

### Short-Term (This Week)
1. ✅ **Implement bidirectional bridge** - telegram_bridge.py with improvements
2. ✅ **Test round-trip messaging** - Corey → Team 1 → Corey
3. ✅ **Create systemd services** - Auto-start on boot, auto-restart on crash
4. ✅ **Write unit tests** - Deduplication, chunking, fallback logic

### Medium-Term (Next Week)
1. ✅ **Implement monitor** - Delta detection, full hashing, emoji markers
2. ✅ **Test auto-summary** - Wrap message, verify Telegram delivery
3. ✅ **Stability hardening** - Retry logic, health checks, error handling
4. ✅ **Create tg-bridge agent** - Manifest, memory structure, delegation patterns

### Long-Term (Month 1)
1. ✅ **Capability exploration** - Inline buttons, message editing, batch files
2. ✅ **Performance optimization** - Completion detection tuning, buffer efficiency
3. ✅ **Multi-user consideration** - If other humans join, session isolation
4. ✅ **Cross-team coordination** - Share Telegram patterns with A-C-Gee

---

## Files Created by This Analysis

**This report**: `/home/corey/projects/AI-CIV/grow_openai/to-corey/ACG-TELEGRAM-ARCHAEOLOGY-REPORT.md`

**Next steps**:
1. The Conductor reviews this report
2. Decide on implementation timeline (immediate vs staged)
3. Create GitHub issue or mission for Telegram integration
4. Delegate initial implementation to appropriate agent(s)

---

## Success Criteria

**Archaeological task complete when**:
- ✅ All A-C-Gee core components analyzed
- ✅ Destabilization root causes identified
- ✅ Team 1 adaptation patterns documented
- ✅ Code snippets ready for copy-paste implementation
- ✅ Timeline estimate provided
- ✅ Integration points with Team 1 infrastructure defined
- ✅ Testing strategy documented
- ✅ Next steps clear and actionable

**Team 1 Telegram integration complete when**:
- ⏳ The Conductor can send Telegram ping on wake-up (Phase 1)
- ⏳ Bidirectional messaging works (Corey ↔ Team 1) (Phase 2)
- ⏳ Auto-summary monitor detects emoji markers and sends (Phase 3)
- ⏳ System self-heals (auto-restart, health checks) (Phase 4)
- ⏳ Fully integrated and discoverable via skills system (Phase 5)
- ⏳ No destabilization issues observed for 1 week continuous operation

---

## Meta-Learning: Code Archaeology Insights

**What I learned as code-archaeologist**:

1. **Read production fixes, not just original code** - A-C-Gee's Oct 18 fixes revealed destabilization patterns
2. **Teaching reports are gold** - TG-ARCHI-TEACHING-REPORT explained "why" not just "what"
3. **Configuration reveals intent** - Example configs show expected usage patterns
4. **Agent manifests show organizational structure** - tg-archi.md revealed 4-layer separation
5. **Look for "Fix" and "Teaching" files** - Recent production issues documented learnings

**Pattern for future archaeology**:
1. Start with README/setup docs (understand purpose)
2. Read core implementation files (understand "how")
3. Read fix/teaching reports (understand "what went wrong")
4. Read agent manifests (understand "who does what")
5. Read config examples (understand "expected usage")
6. Synthesize adaptation recommendations (understand "what to change")

**This pattern worked well for Telegram archaeology. Recommend for future cross-team learning.**

---

**Status**: ARCHAEOLOGY COMPLETE  
**Next**: The Conductor decides on Telegram integration timeline  
**Handoff**: Report ready for review in `/home/corey/projects/AI-CIV/grow_openai/to-corey/`

---

**Code-archaeologist signing off - A-C-Gee's Telegram patterns fully excavated!** 🏺
