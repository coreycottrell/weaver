# claude-code-conversation

**Production-ready skill for accessing and monitoring Claude Code conversation logs.**

## Quick Start

```python
from claude_code_conversation import read_conversation, export_conversation, watch_conversation

# Read latest conversation
messages = read_conversation()
print(f"Found {len(messages)} messages")

# Export to Markdown
path = export_conversation(format="markdown", output_path="/tmp/session.md")
print(f"Exported to: {path}")

# Watch for new messages in real-time
def handler(msg):
    print(f"[{msg['role']}]: {msg['content'][:100]}")

watcher = watch_conversation(callback=handler)
# ... later ...
watcher.stop()
```

## Features

- **Message Aggregation** - Properly handles streaming multi-line JSONL messages
- **Real-Time Monitoring** - Watch active sessions with inotify
- **Multiple Export Formats** - JSON, Markdown, HTML, Plain Text
- **Full-Text Search** - Search history with metadata filtering
- **Telegram Integration** - Extract wrapped messages for forwarding
- **Session Management** - Auto-detect active sessions, handle concurrent sessions
- **Robust Error Handling** - Corrupted lines, missing fields, large files (>100MB)

## Installation

```bash
# Install dependencies
pip install inotify-simple watchdog

# Install skill (using Claude Code CLI)
claude code skill install claude-code-conversation

# Or manual installation
cp -r claude-code-conversation ~/.claude/skills/
```

## Usage

See [SKILL.md](SKILL.md) for complete documentation.

### Read Conversation

```python
from claude_code_conversation import read_conversation

# Read most recent session
messages = read_conversation()

# Read specific session
messages = read_conversation(session_id="6c380f81-29ba-4240-a87f-77bab63a2b09")

# Filter by role
user_messages = read_conversation(role_filter="user")
```

### Export Conversation

```python
from claude_code_conversation import export_conversation

# Export to Markdown
export_conversation(output_path="/tmp/session.md", format="markdown")

# Export to HTML with styling
export_conversation(output_path="/tmp/session.html", format="html", style="github")

# Export to JSON (preserves all data)
export_conversation(output_path="/tmp/session.json", format="json")
```

### Watch Conversation

```python
from claude_code_conversation import watch_conversation

def on_message(msg):
    print(f"New message: {msg['content'][:100]}...")

watcher = watch_conversation(callback=on_message, filter_sidechains=True)

# Stop watching
watcher.stop()
```

### Search History

```python
from claude_code_conversation import search_history, find_errors

# Search for specific text
results = search_history(query="telegram wrapper protocol", session_limit=10)

# Find errors
errors = find_errors(session_limit=20)

# Search with filters
results = search_history(
    query=r"error|exception",
    role_filter="assistant",
    date_from="2025-10-01",
    min_tokens=1000
)
```

## Examples

See [examples/](examples/) directory:

- **basic_export.py** - Export latest session to Markdown
- **telegram_monitor.py** - Real-time Telegram forwarding
- **conversation_search.py** - Search for errors and large responses

## API Reference

See [references/API.md](references/API.md) for complete API documentation.

## Architecture

See [references/ARCHITECTURE.md](references/ARCHITECTURE.md) for internal architecture.

## Testing

```bash
# Run unit tests
python -m unittest discover tests/

# Run specific test
python tests/test_parser.py
```

## License

MIT License - see [LICENSE](LICENSE) file for details.

## Support

- **Issues**: https://github.com/AI-CIV/skills/issues
- **Documentation**: https://github.com/AI-CIV/skills/tree/main/claude-code-conversation
- **Maintained by**: AI-CIV Team 1 (capability-curator, code-archaeologist)

## Version History

- **1.0.0** (2025-10-20): Initial release
  - Message aggregation with state tracking
  - Real-time watching with inotify
  - Multi-format export (JSON, Markdown, HTML, Text)
  - Full-text search with filtering
  - Telegram wrapper extraction
  - Session management
  - Comprehensive error handling

## Contributing

Contributions welcome! Please:

1. Fork repository
2. Create feature branch
3. Add tests for new functionality
4. Submit pull request

## AI-CIV Original

This skill was created by AI-CIV Team 1 as a custom capability for managing Claude Code conversation logs. It is not an official Anthropic skill, but follows Anthropic's skill specification for compatibility.
