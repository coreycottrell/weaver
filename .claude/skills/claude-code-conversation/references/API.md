# API Reference

Complete API documentation for claude-code-conversation skill.

## Parser Module

### `read_conversation()`

Parse conversation from JSONL file.

**Signature**:
```python
def read_conversation(
    session_id: Optional[str] = None,
    project_path: Optional[str] = None,
    filter_sidechains: bool = False,
    filter_snapshots: bool = True,
    role_filter: Optional[str] = None,
    debug: bool = False
) -> List[Dict[str, Any]]
```

**Parameters**:
- `session_id` (str, optional): Session UUID. If None, finds most recent session.
- `project_path` (str, optional): Path to Claude project directory. Auto-detects if None.
- `filter_sidechains` (bool): Exclude sidechain messages. Default: False.
- `filter_snapshots` (bool): Exclude file-history-snapshot entries. Default: True.
- `role_filter` (str, optional): Filter by role ("user" or "assistant"). None = all.
- `debug` (bool): Enable debug logging. Default: False.

**Returns**: `List[Dict[str, Any]]`

Each message dictionary contains:
- `uuid` (str): Message unique identifier
- `timestamp` (str): ISO 8601 timestamp
- `type` (str): "user" or "assistant"
- `role` (str): Message role
- `content` (str): Message content (text)
- `parent_uuid` (str): Parent message UUID
- `is_sidechain` (bool): Sidechain status
- `tool_results` (list): Tool use results (if present)
- `model` (str): Model used (assistant messages only)
- `usage` (dict): Token usage statistics (assistant messages only)

**Example**:
```python
from claude_code_conversation import read_conversation

# Read most recent session
messages = read_conversation()

# Read specific session, filter by role
messages = read_conversation(
    session_id="6c380f81-29ba-4240-a87f-77bab63a2b09",
    role_filter="user"
)
```

---

### `aggregate_messages()`

Aggregate multi-line streaming messages from JSONL.

**Signature**:
```python
def aggregate_messages(
    jsonl_path: str,
    debug: bool = False
) -> List[Dict[str, Any]]
```

**Parameters**:
- `jsonl_path` (str): Path to JSONL file.
- `debug` (bool): Enable debug logging.

**Returns**: `List[Dict[str, Any]]` - Complete messages (one dict per message).

**Note**: This is a low-level function. Use `read_conversation()` for most use cases.

---

### `parse_message()`

Parse raw JSONL message into standardized format.

**Signature**:
```python
def parse_message(
    raw_message: Dict[str, Any]
) -> Dict[str, Any]
```

**Parameters**:
- `raw_message` (dict): Raw message dictionary from JSONL.

**Returns**: `Dict[str, Any]` - Standardized message dictionary.

---

### `filter_sidechains()`

Filter sidechain messages.

**Signature**:
```python
def filter_sidechains(
    messages: List[Dict[str, Any]],
    include: bool = False
) -> List[Dict[str, Any]]
```

**Parameters**:
- `messages` (list): List of messages.
- `include` (bool): If True, include sidechains. If False, exclude them.

**Returns**: `List[Dict[str, Any]]` - Filtered message list.

---

### `build_conversation_tree()`

Build parent-child relationships for messages.

**Signature**:
```python
def build_conversation_tree(
    messages: List[Dict[str, Any]]
) -> List[Dict[str, Any]]
```

**Parameters**:
- `messages` (list): List of messages.

**Returns**: `List[Dict[str, Any]]` - Root messages (no parent). Each message has 'children' field.

---

## Watcher Module

### `watch_conversation()`

Watch conversation for new messages in real-time.

**Signature**:
```python
def watch_conversation(
    session_id: Optional[str] = None,
    project_path: Optional[str] = None,
    callback: Optional[Callable[[Dict[str, Any]], None]] = None,
    filter_sidechains: bool = False,
    filter_snapshots: bool = True,
    debug: bool = False
) -> ConversationWatcher
```

**Parameters**:
- `session_id` (str, optional): Session UUID to watch. Auto-detects if None.
- `project_path` (str, optional): Project directory path.
- `callback` (callable): Function to call with each new message.
- `filter_sidechains` (bool): Skip sidechain messages.
- `filter_snapshots` (bool): Skip file-history-snapshot entries.
- `debug` (bool): Enable debug logging.

**Returns**: `ConversationWatcher` instance (already started).

**Example**:
```python
from claude_code_conversation import watch_conversation

def handler(msg):
    print(f"[{msg['role']}]: {msg['content'][:100]}")

watcher = watch_conversation(callback=handler)

# Later...
watcher.stop()
```

---

### `ConversationWatcher` Class

Real-time conversation watcher using inotify.

**Methods**:

- `start()` - Start watching in background thread
- `stop()` - Stop watching and cleanup

**Attributes**:
- `jsonl_path` (str): Path to watched file
- `callback` (callable): Message callback function

---

## Exporter Module

### `export_conversation()`

Export conversation to file.

**Signature**:
```python
def export_conversation(
    session_id: Optional[str] = None,
    project_path: Optional[str] = None,
    output_path: Optional[str] = None,
    format: str = "markdown",
    include_metadata: bool = True,
    filter_sidechains: bool = False,
    filter_snapshots: bool = True,
    style: str = "github"
) -> str
```

**Parameters**:
- `session_id` (str, optional): Session UUID. Auto-detects if None.
- `project_path` (str, optional): Project path.
- `output_path` (str, optional): Output file path. Auto-generates if None.
- `format` (str): Export format ("json", "markdown", "html", "text"). Default: "markdown".
- `include_metadata` (bool): Include timestamps, UUIDs, token usage. Default: True.
- `filter_sidechains` (bool): Skip sidechain messages.
- `filter_snapshots` (bool): Skip file-history-snapshot entries.
- `style` (str): HTML style preset (for format="html"). Default: "github".

**Returns**: `str` - Path to exported file.

**Example**:
```python
from claude_code_conversation import export_conversation

# Export to Markdown
path = export_conversation(
    format="markdown",
    output_path="/tmp/session.md"
)
```

---

## Search Module

### `search_history()`

Search across conversation history.

**Signature**:
```python
def search_history(
    query: Optional[str] = None,
    project_path: Optional[str] = None,
    role_filter: Optional[str] = None,
    model_filter: Optional[str] = None,
    date_from: Optional[str] = None,
    date_to: Optional[str] = None,
    min_tokens: Optional[int] = None,
    session_limit: Optional[int] = None,
    case_sensitive: bool = False
) -> List[Dict[str, Any]]
```

**Parameters**:
- `query` (str, optional): Regex pattern to search in content. None = search all.
- `project_path` (str, optional): Project directory path.
- `role_filter` (str, optional): Filter by role.
- `model_filter` (str, optional): Filter by model name (partial match).
- `date_from` (str, optional): Start date (ISO format "YYYY-MM-DD").
- `date_to` (str, optional): End date (ISO format "YYYY-MM-DD").
- `min_tokens` (int, optional): Minimum input tokens.
- `session_limit` (int, optional): Max sessions to search (most recent first).
- `case_sensitive` (bool): Case-sensitive search. Default: False.

**Returns**: `List[Dict[str, Any]]` - Matching results.

Each result contains:
- `session_id` (str): Session UUID
- `message_uuid` (str): Message UUID
- `timestamp` (str): Message timestamp
- `role` (str): Message role
- `content_preview` (str): First 200 chars
- `match_highlights` (list): Matched text snippets
- `file_path` (str): Full path to JSONL file

**Example**:
```python
from claude_code_conversation import search_history

# Search for errors
results = search_history(
    query=r"error|exception",
    session_limit=10
)

for result in results:
    print(f"{result['timestamp']}: {result['content_preview']}")
```

---

### `find_errors()`

Find error messages in conversation history.

**Signature**:
```python
def find_errors(
    project_path: Optional[str] = None,
    session_limit: Optional[int] = 20
) -> List[Dict[str, Any]]
```

**Parameters**:
- `project_path` (str, optional): Project path.
- `session_limit` (int, optional): Max sessions to search.

**Returns**: `List[Dict[str, Any]]` - Messages containing errors.

---

### `find_large_responses()`

Find large assistant responses.

**Signature**:
```python
def find_large_responses(
    min_output_tokens: int = 1000,
    project_path: Optional[str] = None,
    session_limit: Optional[int] = 10
) -> List[Dict[str, Any]]
```

**Parameters**:
- `min_output_tokens` (int): Minimum output token count. Default: 1000.
- `project_path` (str, optional): Project path.
- `session_limit` (int, optional): Max sessions to search.

**Returns**: `List[Dict[str, Any]]` - Large responses sorted by token count (descending).

---

## Utils Module

### `get_active_session()`

Get the most recently modified session file.

**Signature**:
```python
def get_active_session(
    project_path: Optional[str] = None
) -> Dict[str, Any]
```

**Parameters**:
- `project_path` (str, optional): Project directory path. Auto-detects if None.

**Returns**: `Dict[str, Any]` - Session info with:
- `session_id` (str): Session UUID
- `file_path` (str): Full path to JSONL file
- `last_modified` (float): Timestamp of last modification
- `file_size` (int): File size in bytes
- `message_count` (int): Approximate message count

**Example**:
```python
from claude_code_conversation import get_active_session

session = get_active_session()
print(f"Active session: {session['session_id']}")
print(f"Last modified: {session['last_modified']}")
```

---

### `extract_wrapped_messages()`

Extract messages wrapped in Telegram markers (🤖🎯📱 ... ✨🔚).

**Signature**:
```python
def extract_wrapped_messages(
    session_id: Optional[str] = None,
    project_path: Optional[str] = None
) -> List[Dict[str, Any]]
```

**Parameters**:
- `session_id` (str, optional): Session UUID. Auto-detects if None.
- `project_path` (str, optional): Project path.

**Returns**: `List[Dict[str, Any]]` - Wrapped messages with:
- `uuid` (str): Message UUID
- `timestamp` (str): Message timestamp
- `wrapped_content` (str): Content between markers
- `full_content` (str): Complete message content

---

### `get_session_info()`

Get detailed info about a session.

**Signature**:
```python
def get_session_info(
    session_id: str,
    project_path: Optional[str] = None
) -> Dict[str, Any]
```

**Parameters**:
- `session_id` (str): Session UUID.
- `project_path` (str, optional): Project path.

**Returns**: `Dict[str, Any]` - Session info with:
- `session_id` (str): UUID
- `file_path` (str): Full path
- `file_size` (int): Bytes
- `message_count` (int): Total messages
- `user_messages` (int): User message count
- `assistant_messages` (int): Assistant message count
- `first_message` (str): Timestamp of first message
- `last_message` (str): Timestamp of last message
- `total_input_tokens` (int): Total input tokens
- `total_output_tokens` (int): Total output tokens
- `models_used` (list): List of models used

---

## Data Types

### Message Dictionary

Standard message format returned by all functions:

```python
{
    'uuid': str,                # Message unique identifier
    'timestamp': str,           # ISO 8601 timestamp
    'type': str,               # "user", "assistant", or "file-history-snapshot"
    'role': str,               # Message role
    'content': str,            # Message content (text)
    'parent_uuid': str,        # Parent message UUID
    'is_sidechain': bool,      # Sidechain status
    'session_id': str,         # Session UUID
    'cwd': str,                # Working directory
    'git_branch': str,         # Git branch
    'tool_results': list,      # Tool use results (optional)
    'model': str,              # Model used (optional)
    'usage': dict,             # Token usage (optional)
    'request_id': str,         # Request ID (optional)
    'user_type': str,          # User type (optional)
}
```

### Usage Dictionary

Token usage statistics (assistant messages):

```python
{
    'input_tokens': int,           # Input tokens
    'output_tokens': int,          # Output tokens
    'cache_read_input_tokens': int,  # Cached tokens read
    'cache_creation_input_tokens': int  # Tokens written to cache
}
```

### Tool Result Dictionary

Tool use result:

```python
{
    'type': 'tool_result',
    'tool_use_id': str,
    'content': str
}
```
