"""
Utility functions for conversation management.
"""

import os
import glob
from typing import List, Dict, Any, Optional
from pathlib import Path


def get_active_session(project_path: Optional[str] = None) -> Dict[str, Any]:
    """
    Get the most recently modified session file.

    Args:
        project_path: Path to project directory. If None, auto-detects from cwd.

    Returns:
        Dictionary with session info:
        - session_id: Session UUID
        - file_path: Full path to JSONL file
        - last_modified: Timestamp of last modification
        - file_size: File size in bytes
        - message_count: Approximate message count
    """
    sessions = get_project_sessions(project_path)

    if not sessions:
        raise FileNotFoundError(f"No session files found in {project_path or 'auto-detected project'}")

    return sessions[0]  # Already sorted by modification time


def get_project_sessions(project_path: Optional[str] = None) -> List[Dict[str, Any]]:
    """
    Get all session files for a project, sorted by modification time (newest first).

    Args:
        project_path: Path to project directory. If None, auto-detects.

    Returns:
        List of session info dictionaries.
    """
    if not project_path:
        project_path = auto_detect_project()

    # Find all JSONL files
    pattern = os.path.join(project_path, "*.jsonl")
    jsonl_files = glob.glob(pattern)

    # Get info for each file
    sessions = []
    for jsonl_path in jsonl_files:
        stat = os.stat(jsonl_path)
        session_id = os.path.basename(jsonl_path).replace('.jsonl', '')

        # Estimate message count (very rough)
        message_count = estimate_message_count(jsonl_path)

        sessions.append({
            'session_id': session_id,
            'file_path': jsonl_path,
            'last_modified': stat.st_mtime,
            'file_size': stat.st_size,
            'message_count': message_count
        })

    # Sort by modification time (newest first)
    sessions.sort(key=lambda s: s['last_modified'], reverse=True)

    return sessions


def auto_detect_project() -> str:
    """
    Auto-detect project directory from current working directory.

    Returns:
        Path to Claude projects directory for current project.
    """
    cwd = os.getcwd()

    # Convert path to Claude projects format
    # /home/corey/projects/AI-CIV/grow_openai -> -home-corey-projects-AI-CIV-grow-openai
    project_name = cwd.replace('/', '-')

    claude_dir = os.path.expanduser("~/.claude/projects")
    project_dir = os.path.join(claude_dir, project_name)

    if os.path.exists(project_dir):
        return project_dir

    # Fallback: find most recently used project
    all_projects = glob.glob(os.path.join(claude_dir, "*"))
    if all_projects:
        # Sort by modification time
        all_projects.sort(key=lambda p: os.path.getmtime(p), reverse=True)
        return all_projects[0]

    raise FileNotFoundError(f"Could not find Claude project directory for {cwd}")


def get_session_path(session_id: str, project_path: Optional[str] = None) -> str:
    """
    Get full path to session JSONL file.

    Args:
        session_id: Session UUID.
        project_path: Project directory. If None, auto-detects.

    Returns:
        Full path to JSONL file.
    """
    if not project_path:
        project_path = auto_detect_project()

    return os.path.join(project_path, f"{session_id}.jsonl")


def extract_wrapped_messages(
    session_id: Optional[str] = None,
    project_path: Optional[str] = None
) -> List[Dict[str, Any]]:
    """
    Extract messages wrapped in Telegram markers (🤖🎯📱 ... ✨🔚).

    Args:
        session_id: Session UUID. If None, uses most recent.
        project_path: Project path. If None, auto-detects.

    Returns:
        List of wrapped messages with:
        - uuid: Message UUID
        - timestamp: When message was sent
        - wrapped_content: Content between markers
        - full_content: Complete message content
    """
    from .parser import read_conversation

    messages = read_conversation(
        session_id=session_id,
        project_path=project_path,
        role_filter="assistant"  # Only assistant messages have wrappers
    )

    wrapped = []

    for msg in messages:
        content = msg.get('content', '')

        if '🤖🎯📱' in content and '✨🔚' in content:
            # Extract wrapped content
            start_marker = '🤖🎯📱'
            end_marker = '✨🔚'

            start_idx = content.find(start_marker)
            end_idx = content.find(end_marker)

            if start_idx != -1 and end_idx != -1 and end_idx > start_idx:
                wrapped_content = content[start_idx + len(start_marker):end_idx].strip()

                wrapped.append({
                    'uuid': msg.get('uuid'),
                    'timestamp': msg.get('timestamp'),
                    'wrapped_content': wrapped_content,
                    'full_content': content
                })

    return wrapped


def detect_session_switches(
    session_id: Optional[str] = None,
    project_path: Optional[str] = None
) -> List[Dict[str, Any]]:
    """
    Detect when user switched between sessions.

    Args:
        session_id: Session UUID to analyze. If None, uses most recent.
        project_path: Project path.

    Returns:
        List of session switches with:
        - from_session: Previous session ID
        - to_session: New session ID
        - timestamp: When switch occurred
    """
    from .parser import read_conversation

    messages = read_conversation(
        session_id=session_id,
        project_path=project_path
    )

    switches = []
    prev_session = None

    for msg in messages:
        current_session = msg.get('session_id')

        if prev_session and current_session != prev_session:
            switches.append({
                'from_session': prev_session,
                'to_session': current_session,
                'timestamp': msg.get('timestamp')
            })

        prev_session = current_session

    return switches


def get_session_info(
    session_id: str,
    project_path: Optional[str] = None
) -> Dict[str, Any]:
    """
    Get detailed info about a session.

    Args:
        session_id: Session UUID.
        project_path: Project path.

    Returns:
        Dictionary with:
        - session_id: UUID
        - file_path: Full path
        - file_size: Bytes
        - message_count: Total messages
        - user_messages: Count of user messages
        - assistant_messages: Count of assistant messages
        - first_message: Timestamp of first message
        - last_message: Timestamp of last message
        - total_tokens: Input + output tokens
        - models_used: List of models used
    """
    from .parser import read_conversation

    jsonl_path = get_session_path(session_id, project_path)
    stat = os.stat(jsonl_path)

    messages = read_conversation(
        session_id=session_id,
        project_path=project_path
    )

    user_count = sum(1 for m in messages if m.get('role') == 'user')
    assistant_count = sum(1 for m in messages if m.get('role') == 'assistant')

    total_input = sum(m.get('usage', {}).get('input_tokens', 0) for m in messages if m.get('usage'))
    total_output = sum(m.get('usage', {}).get('output_tokens', 0) for m in messages if m.get('usage'))

    models = set(m.get('model') for m in messages if m.get('model'))

    return {
        'session_id': session_id,
        'file_path': jsonl_path,
        'file_size': stat.st_size,
        'message_count': len(messages),
        'user_messages': user_count,
        'assistant_messages': assistant_count,
        'first_message': messages[0].get('timestamp') if messages else None,
        'last_message': messages[-1].get('timestamp') if messages else None,
        'total_input_tokens': total_input,
        'total_output_tokens': total_output,
        'models_used': list(models)
    }


def estimate_message_count(jsonl_path: str) -> int:
    """
    Estimate message count from JSONL file (fast, approximate).

    Counts lines and divides by average lines per message (~8).

    Args:
        jsonl_path: Path to JSONL file.

    Returns:
        Estimated message count.
    """
    try:
        with open(jsonl_path, 'r') as f:
            line_count = sum(1 for _ in f)
        return max(1, line_count // 8)  # ~8 lines per message on average
    except:
        return 0


def cleanup_old_sessions(
    project_path: Optional[str] = None,
    keep_count: int = 20,
    dry_run: bool = True
) -> List[str]:
    """
    Clean up old session files, keeping only the N most recent.

    Args:
        project_path: Project path.
        keep_count: Number of sessions to keep.
        dry_run: If True, don't actually delete (just return what would be deleted).

    Returns:
        List of file paths that were (or would be) deleted.
    """
    sessions = get_project_sessions(project_path)

    # Skip if we have fewer than keep_count
    if len(sessions) <= keep_count:
        return []

    # Sessions to delete (oldest ones)
    to_delete = sessions[keep_count:]

    deleted = []

    for session in to_delete:
        if not dry_run:
            try:
                os.remove(session['file_path'])
                deleted.append(session['file_path'])
            except Exception:
                pass  # Skip errors
        else:
            deleted.append(session['file_path'])

    return deleted
