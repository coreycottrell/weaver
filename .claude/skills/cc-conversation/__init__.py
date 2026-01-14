"""
claude-code-conversation skill

Comprehensive access and monitoring for Claude Code conversation logs.

Main API:
- read_conversation(): Parse JSONL and return messages
- watch_conversation(): Real-time monitoring
- export_conversation(): Multi-format export
- search_history(): Full-text and metadata search
- get_active_session(): Find most recent session
- extract_wrapped_messages(): Get Telegram-wrapped messages
"""

__version__ = "1.0.0"
__author__ = "AI-CIV Team 1"
__license__ = "MIT"

from .parser import (
    read_conversation,
    aggregate_messages,
    parse_message,
    filter_sidechains,
    build_conversation_tree
)

from .watcher import (
    watch_conversation,
    ConversationWatcher
)

from .exporter import (
    export_conversation,
    Exporter,
    MarkdownExporter,
    HTMLExporter,
    JSONExporter,
    TextExporter
)

from .search import (
    search_history,
    search_session,
    search_by_metadata
)

from .utils import (
    get_active_session,
    extract_wrapped_messages,
    get_project_sessions,
    detect_session_switches,
    get_session_info
)

__all__ = [
    # Parser
    'read_conversation',
    'aggregate_messages',
    'parse_message',
    'filter_sidechains',
    'build_conversation_tree',

    # Watcher
    'watch_conversation',
    'ConversationWatcher',

    # Exporter
    'export_conversation',
    'Exporter',
    'MarkdownExporter',
    'HTMLExporter',
    'JSONExporter',
    'TextExporter',

    # Search
    'search_history',
    'search_session',
    'search_by_metadata',

    # Utils
    'get_active_session',
    'extract_wrapped_messages',
    'get_project_sessions',
    'detect_session_switches',
    'get_session_info',
]
