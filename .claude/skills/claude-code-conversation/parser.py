"""
JSONL parsing with proper message aggregation.

Critical: Claude Code logs streaming messages as multi-line JSONL.
A single message may span 5-20+ lines. Use state-tracking aggregation,
NOT line-by-line parsing.
"""

import json
import os
from typing import List, Dict, Optional, Any
from datetime import datetime


def read_conversation(
    session_id: Optional[str] = None,
    project_path: Optional[str] = None,
    filter_sidechains: bool = False,
    filter_snapshots: bool = True,
    role_filter: Optional[str] = None,
    debug: bool = False
) -> List[Dict[str, Any]]:
    """
    Read and parse conversation from JSONL file.

    Args:
        session_id: Session UUID. If None, finds most recent session.
        project_path: Path to Claude project directory. If None, auto-detects from cwd.
        filter_sidechains: If True, exclude sidechain messages.
        filter_snapshots: If True, exclude file-history-snapshot entries (default True).
        role_filter: Filter by role ("user" or "assistant"). None = all messages.
        debug: Enable debug logging.

    Returns:
        List of parsed messages with standardized fields.
    """
    from .utils import get_active_session, get_session_path

    # Find session file
    if session_id:
        jsonl_path = get_session_path(session_id, project_path)
    else:
        session_info = get_active_session(project_path)
        jsonl_path = session_info['file_path']
        session_id = session_info['session_id']

    if not os.path.exists(jsonl_path):
        raise FileNotFoundError(f"Session file not found: {jsonl_path}")

    if debug:
        print(f"Reading session: {session_id}")
        print(f"File: {jsonl_path}")

    # Aggregate multi-line messages
    raw_messages = aggregate_messages(jsonl_path, debug=debug)

    # Parse and filter
    messages = []
    for raw_msg in raw_messages:
        try:
            parsed = parse_message(raw_msg)

            # Apply filters
            if filter_snapshots and parsed.get('type') == 'file-history-snapshot':
                continue

            if filter_sidechains and parsed.get('is_sidechain', False):
                continue

            if role_filter and parsed.get('role') != role_filter:
                continue

            messages.append(parsed)
        except Exception as e:
            if debug:
                print(f"Warning: Failed to parse message {raw_msg.get('uuid')}: {e}")
            continue

    if debug:
        print(f"Parsed {len(messages)} messages (from {len(raw_messages)} raw)")

    return messages


def aggregate_messages(jsonl_path: str, debug: bool = False) -> List[Dict[str, Any]]:
    """
    Aggregate multi-line streaming messages from JSONL.

    Claude Code writes messages as streaming JSONL - a single message
    may span multiple lines with the same UUID. This function aggregates
    them using state tracking.

    Args:
        jsonl_path: Path to JSONL file.
        debug: Enable debug logging.

    Returns:
        List of complete messages (one dict per message).
    """
    messages = []
    current_message_lines = []
    current_uuid = None
    corrupted_count = 0

    with open(jsonl_path, 'r', encoding='utf-8', errors='ignore') as f:
        for line_num, line in enumerate(f, 1):
            line = line.strip()
            if not line:
                continue

            try:
                entry = json.loads(line)
            except json.JSONDecodeError as e:
                corrupted_count += 1
                if debug:
                    print(f"Line {line_num}: Corrupted JSON - {e}")
                continue

            entry_uuid = entry.get('uuid')

            # Message completion conditions:
            # 1. UUID changed (new message started)
            # 2. No UUID in current entry (metadata/snapshot)
            if entry_uuid and entry_uuid != current_uuid:
                # Complete previous message
                if current_message_lines:
                    messages.append(merge_message_lines(current_message_lines))

                # Start new message
                current_message_lines = [entry]
                current_uuid = entry_uuid

            elif not entry_uuid:
                # No UUID = standalone entry (file-history-snapshot, etc.)
                if current_message_lines:
                    messages.append(merge_message_lines(current_message_lines))
                    current_message_lines = []
                    current_uuid = None

                # Add standalone entry
                messages.append(entry)

            else:
                # Same UUID = continuation of current message
                current_message_lines.append(entry)

        # Don't forget last message
        if current_message_lines:
            messages.append(merge_message_lines(current_message_lines))

    if debug and corrupted_count > 0:
        print(f"Warning: Skipped {corrupted_count} corrupted lines")

    return messages


def merge_message_lines(lines: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Merge multiple JSONL lines into a single complete message.

    For streaming messages, later lines may have additional fields
    or updated content. We merge them intelligently.

    Args:
        lines: List of JSONL entries with same UUID.

    Returns:
        Merged message dictionary.
    """
    if len(lines) == 1:
        return lines[0]

    # Start with first line
    merged = lines[0].copy()

    # Merge subsequent lines
    for line in lines[1:]:
        for key, value in line.items():
            if key not in merged:
                # New field - add it
                merged[key] = value
            elif isinstance(value, dict) and isinstance(merged[key], dict):
                # Nested dict - deep merge
                merged[key] = {**merged[key], **value}
            elif isinstance(value, list) and isinstance(merged[key], list):
                # List - extend
                merged[key].extend(value)
            else:
                # Primitive - use latest value
                merged[key] = value

    return merged


def parse_message(raw_message: Dict[str, Any]) -> Dict[str, Any]:
    """
    Parse raw JSONL message into standardized format.

    Args:
        raw_message: Raw message dictionary from JSONL.

    Returns:
        Standardized message dictionary.
    """
    msg_type = raw_message.get('type', 'unknown')

    # Handle file-history-snapshot
    if msg_type == 'file-history-snapshot':
        return {
            'uuid': raw_message.get('messageId'),
            'type': 'file-history-snapshot',
            'timestamp': raw_message.get('snapshot', {}).get('timestamp'),
            'snapshot': raw_message.get('snapshot', {})
        }

    # Parse message field
    message_data = raw_message.get('message', {})

    # Extract content
    content = message_data.get('content', '')
    if isinstance(content, list):
        # Assistant messages have content as array of text blocks
        content_parts = []
        tool_results = []

        for item in content:
            if isinstance(item, dict):
                if item.get('type') == 'text':
                    content_parts.append(item.get('text', ''))
                elif item.get('type') == 'tool_result':
                    tool_results.append(item)

        content = '\n'.join(content_parts)
    else:
        tool_results = []

    # Detect tool results in user messages
    if msg_type == 'user' and isinstance(message_data.get('content'), list):
        for item in message_data['content']:
            if isinstance(item, dict) and item.get('type') == 'tool_result':
                tool_results.append(item)

    return {
        'uuid': raw_message.get('uuid'),
        'timestamp': raw_message.get('timestamp'),
        'type': msg_type,
        'role': message_data.get('role'),
        'content': content,
        'parent_uuid': raw_message.get('parentUuid'),
        'is_sidechain': raw_message.get('isSidechain', False),
        'session_id': raw_message.get('sessionId'),
        'cwd': raw_message.get('cwd'),
        'git_branch': raw_message.get('gitBranch'),
        'tool_results': tool_results if tool_results else None,
        'model': message_data.get('model'),
        'usage': message_data.get('usage'),
        'request_id': raw_message.get('requestId'),
        'user_type': raw_message.get('userType'),
    }


def filter_sidechains(messages: List[Dict[str, Any]], include: bool = False) -> List[Dict[str, Any]]:
    """
    Filter sidechain messages.

    Args:
        messages: List of messages.
        include: If True, include sidechains. If False, exclude them.

    Returns:
        Filtered message list.
    """
    if include:
        return messages
    return [m for m in messages if not m.get('is_sidechain', False)]


def build_conversation_tree(messages: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Build parent-child relationships for messages.

    Args:
        messages: List of messages.

    Returns:
        List of root messages (no parent). Each message has 'children' field.
    """
    # Create UUID -> message map
    message_map = {m['uuid']: m for m in messages if m.get('uuid')}

    # Build parent-child links
    for message in messages:
        parent_uuid = message.get('parent_uuid')
        if parent_uuid and parent_uuid in message_map:
            parent = message_map[parent_uuid]
            parent.setdefault('children', []).append(message)

    # Find roots (no parent)
    roots = [m for m in messages if not m.get('parent_uuid') or m['parent_uuid'] not in message_map]

    return roots


def get_message_by_uuid(messages: List[Dict[str, Any]], uuid: str) -> Optional[Dict[str, Any]]:
    """
    Find message by UUID.

    Args:
        messages: List of messages.
        uuid: Message UUID to find.

    Returns:
        Message dictionary or None if not found.
    """
    for msg in messages:
        if msg.get('uuid') == uuid:
            return msg
    return None


def get_conversation_thread(messages: List[Dict[str, Any]], start_uuid: str) -> List[Dict[str, Any]]:
    """
    Get conversation thread starting from a specific message.

    Walks up to root, then down through all children.

    Args:
        messages: List of messages.
        start_uuid: UUID to start from.

    Returns:
        List of messages in thread (chronologically ordered).
    """
    message_map = {m['uuid']: m for m in messages if m.get('uuid')}
    start_msg = message_map.get(start_uuid)

    if not start_msg:
        return []

    # Walk up to root
    current = start_msg
    while current.get('parent_uuid') and current['parent_uuid'] in message_map:
        current = message_map[current['parent_uuid']]

    root = current

    # Walk down collecting all descendants
    thread = []

    def collect_descendants(msg):
        thread.append(msg)
        for child in msg.get('children', []):
            collect_descendants(child)

    # Build tree first
    build_conversation_tree(messages)
    collect_descendants(root)

    # Sort by timestamp
    thread.sort(key=lambda m: m.get('timestamp', ''))

    return thread
