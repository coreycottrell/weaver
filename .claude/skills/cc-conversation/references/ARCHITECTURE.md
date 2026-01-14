# Architecture

Internal architecture documentation for claude-code-conversation skill.

## Design Principles

1. **Message Aggregation First** - Never parse line-by-line. Claude Code streams messages as multi-line JSONL.
2. **State Tracking** - Use UUID-based state machine to detect message boundaries.
3. **Fail Gracefully** - Skip corrupted lines, handle missing fields, support large files.
4. **Modular Design** - Separate concerns: parsing, watching, exporting, searching.
5. **Lazy Loading** - Don't load entire file into memory unless necessary.

## Module Structure

```
claude-code-conversation/
├── __init__.py          # Public API exports
├── parser.py            # JSONL parsing and aggregation
├── watcher.py           # Real-time file monitoring
├── exporter.py          # Multi-format export
├── search.py            # Full-text and metadata search
├── utils.py             # Helper functions
├── scripts/             # Helper scripts (none yet)
├── references/          # Documentation
├── assets/              # Static assets (none yet)
├── tests/               # Unit tests
└── examples/            # Usage examples
```

## Core Components

### Parser (`parser.py`)

**Responsibility**: Parse JSONL files with proper message aggregation.

**Key Functions**:
- `aggregate_messages()` - State-tracking aggregator (UUID-based)
- `merge_message_lines()` - Merge multi-line messages
- `parse_message()` - Standardize message format
- `build_conversation_tree()` - Reconstruct parent-child relationships

**State Machine**:
```
1. Read JSONL line
2. Parse JSON (skip if corrupted)
3. Extract UUID
4. If UUID changed:
   - Complete previous message (merge lines)
   - Start new message
5. If no UUID:
   - Complete previous message
   - Process standalone entry (file-history-snapshot)
6. If same UUID:
   - Accumulate line for current message
7. Repeat until EOF
8. Don't forget to complete last message!
```

**Critical Gotchas**:
- `stop_reason` is ALWAYS null (can't use it for completion detection)
- Message completion = UUID change OR type change OR no UUID
- Tool results appear as `type:"user"` with `toolUseResult` field
- Assistant content is array of text blocks (not string)

---

### Watcher (`watcher.py`)

**Responsibility**: Real-time monitoring of JSONL files.

**Key Classes**:
- `ConversationWatcher` - File watcher with message aggregation

**Architecture**:
- Uses inotify for efficient file monitoring (fallback to polling)
- Runs in background thread (daemon)
- Aggregates messages before triggering callback
- Seeks to end of file on start (only watch new messages)

**Callback Contract**:
```python
def callback(message: Dict[str, Any]) -> None:
    """
    Called for each new complete message.

    Args:
        message: Standardized message dictionary.
    """
    pass
```

**Threading Model**:
- Main thread: Creates watcher, registers callback
- Background thread: Watches file, triggers callbacks
- Cleanup: `stop()` method joins thread with timeout

---

### Exporter (`exporter.py`)

**Responsibility**: Export conversations to multiple formats.

**Key Classes**:
- `Exporter` (abstract base)
- `JSONExporter`
- `MarkdownExporter`
- `HTMLExporter`
- `TextExporter`

**Template Method Pattern**:
```python
class Exporter(ABC):
    def export(messages, output_path):
        write(format_header(messages))
        for msg in messages:
            write(format_message(msg))
        write(format_footer(messages))

    @abstractmethod
    def format_message(msg): pass

    @abstractmethod
    def format_header(messages): pass

    @abstractmethod
    def format_footer(messages): pass
```

**Format-Specific Features**:
- **JSON**: Preserves all fields, structured data
- **Markdown**: Human-readable, code blocks, metadata
- **HTML**: Styled output, syntax highlighting
- **Text**: Plain text, no formatting

---

### Search (`search.py`)

**Responsibility**: Full-text and metadata search across history.

**Key Functions**:
- `search_history()` - General-purpose search
- `find_errors()` - Find error messages
- `find_large_responses()` - Find large assistant responses

**Search Strategy**:
1. Get list of sessions (sorted by modification time)
2. Apply session limit (search N most recent)
3. For each session:
   - Load messages
   - Apply metadata filters
   - Apply text search (regex)
   - Collect matches
4. Return aggregated results

**Optimization**:
- Session limit prevents searching entire history
- Filters applied during iteration (not post-processing)
- Regex compiled once (not per message)

---

### Utils (`utils.py`)

**Responsibility**: Helper functions for common tasks.

**Key Functions**:
- `get_active_session()` - Find most recent session
- `get_project_sessions()` - List all sessions
- `auto_detect_project()` - Infer project from cwd
- `extract_wrapped_messages()` - Get Telegram-wrapped messages
- `detect_session_switches()` - Find session switches
- `get_session_info()` - Detailed session statistics

**Project Detection**:
```
cwd: /home/corey/projects/AI-CIV/grow_openai
→ Claude project: ~/.claude/projects/-home-corey-projects-AI-CIV-grow-openai/
```

Path conversion: Replace `/` with `-`

---

## Data Flow

### Reading Conversation

```
user calls read_conversation()
  ↓
utils.get_active_session()  [if session_id is None]
  ↓
utils.get_session_path()
  ↓
parser.aggregate_messages()
  ↓
  → Read JSONL line-by-line
  → State-track by UUID
  → Merge multi-line messages
  ↓
parser.parse_message()  [for each message]
  ↓
  → Standardize format
  → Extract content from text blocks
  → Detect tool results
  ↓
Apply filters (sidechains, snapshots, role)
  ↓
Return list of messages
```

### Watching Conversation

```
user calls watch_conversation()
  ↓
Create ConversationWatcher
  ↓
watcher.start()
  ↓
Background thread watches file (inotify or poll)
  ↓
On file change:
  → Read new content
  → Aggregate messages (same state machine)
  → Trigger callback for each complete message
  ↓
user calls watcher.stop()
  ↓
Thread cleanup
```

### Exporting Conversation

```
user calls export_conversation()
  ↓
parser.read_conversation()
  ↓
Create exporter (JSON/Markdown/HTML/Text)
  ↓
exporter.export(messages, output_path)
  ↓
  → format_header()
  → for each message: format_message()
  → format_footer()
  ↓
Write to file
  ↓
Return output path
```

## Performance Considerations

### Memory

- **Message aggregation**: Streaming (doesn't load full file)
- **Export**: Loads all messages into memory (careful with large sessions)
- **Search**: Iterates sessions, doesn't load all at once
- **Watch**: Only processes new content (seeks to end on start)

**Large File Handling**:
- Files >100MB: Use streaming approaches
- Message count estimation: ~8 lines per message average
- Don't build full conversation tree unless needed

### Speed

- **Regex compilation**: Compile once, use many times
- **inotify**: More efficient than polling (Linux)
- **Session limit**: Search only N most recent sessions
- **Filter early**: Apply filters during iteration, not post-processing

### Scalability

- **40+ concurrent sessions**: Supported (watcher handles single session)
- **100+ MB files**: Supported (streaming aggregation)
- **10,000+ messages**: Supported (lazy loading)

## Error Handling

### Corrupted JSONL Lines

**Strategy**: Skip and continue.

```python
try:
    entry = json.loads(line)
except json.JSONDecodeError:
    corrupted_count += 1
    continue  # Skip this line
```

### Missing Fields

**Strategy**: Use `.get()` with defaults.

```python
uuid = entry.get('uuid')  # May be None
content = message_data.get('content', '')  # Default to empty string
```

### File Not Found

**Strategy**: Raise clear error.

```python
if not os.path.exists(jsonl_path):
    raise FileNotFoundError(f"Session file not found: {jsonl_path}")
```

### Callback Errors (Watcher)

**Strategy**: Catch and log, don't crash watcher.

```python
try:
    self.callback(parsed)
except Exception as e:
    if self.debug:
        print(f"Error in callback: {e}")
```

## Testing Strategy

### Unit Tests

- **parser.py**: Message aggregation, parsing, tree building
- **utils.py**: Session detection, wrapped message extraction
- **exporter.py**: Format conversion (requires sample messages)
- **search.py**: Regex matching, filtering

### Integration Tests

- **Real JSONL files**: Test against actual Claude Code logs
- **Large files**: Performance testing with >100MB files
- **Edge cases**: Corrupted lines, missing fields, empty files

### Manual Testing

- **Telegram monitoring**: Real-time forwarding test
- **Export quality**: Visual inspection of HTML/Markdown output
- **Search accuracy**: Verify search results match expectations

## Extension Points

### Custom Exporters

Extend `Exporter` base class:

```python
from claude_code_conversation.exporter import Exporter

class MyExporter(Exporter):
    def format_message(self, message):
        # Custom formatting
        pass

    def format_header(self, messages):
        # Custom header
        pass

    def format_footer(self, messages):
        # Custom footer
        pass
```

### Custom Callbacks

```python
def my_callback(message):
    # Custom processing
    if message['role'] == 'user':
        # Store in database
        pass

watcher = watch_conversation(callback=my_callback)
```

### Custom Filters

```python
def custom_filter(messages):
    return [m for m in messages if my_condition(m)]

messages = read_conversation()
filtered = custom_filter(messages)
```

## Future Enhancements

### Potential Features

1. **WebSocket streaming** - Real-time message push
2. **Database backend** - SQLite for faster search
3. **Incremental export** - Only export new messages
4. **Compression support** - .jsonl.gz files
5. **Parallel search** - Multi-threaded history search
6. **Cloud backup** - S3/GCS export
7. **Analytics** - Token usage graphs, conversation metrics
8. **Diff export** - Compare two sessions

### Performance Optimizations

1. **Message caching** - Cache parsed messages
2. **Index files** - Build search indexes
3. **Parallel parsing** - Multi-process JSONL parsing
4. **Memory mapping** - mmap for large files

## Dependencies

**Required**:
- Python 3.7+
- `inotify-simple` or `watchdog` (for file watching)

**Optional**:
- `pygments` (for syntax highlighting in HTML export)
- `markdown` (for enhanced Markdown export)

## Deployment

### Installation

```bash
pip install inotify-simple watchdog
cp -r claude-code-conversation ~/.claude/skills/
```

### Grant to Agent

```yaml
# In agent manifest
allowed-skills:
  - claude-code-conversation
```

### Verify Installation

```python
from claude_code_conversation import get_active_session
session = get_active_session()
print(f"Installed correctly: {session['session_id']}")
```
