"""
Search conversation history with full-text and metadata filtering.
"""

import os
import re
import glob
from typing import List, Dict, Any, Optional
from datetime import datetime


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
) -> List[Dict[str, Any]]:
    """
    Search across conversation history.

    Args:
        query: Regex pattern to search in message content. None = search all.
        project_path: Path to project directory. None = auto-detect.
        role_filter: Filter by role ("user" or "assistant").
        model_filter: Filter by model name (partial match).
        date_from: Start date (ISO format "YYYY-MM-DD").
        date_to: End date (ISO format "YYYY-MM-DD").
        min_tokens: Minimum input tokens.
        session_limit: Max number of sessions to search (most recent first).
        case_sensitive: Case-sensitive search.

    Returns:
        List of matching results with metadata.
    """
    from .utils import get_project_sessions
    from .parser import read_conversation

    # Get sessions to search
    sessions = get_project_sessions(project_path)

    # Apply session limit
    if session_limit:
        sessions = sessions[:session_limit]

    # Compile regex if provided
    pattern = None
    if query:
        flags = 0 if case_sensitive else re.IGNORECASE
        try:
            pattern = re.compile(query, flags)
        except re.error as e:
            raise ValueError(f"Invalid regex pattern: {e}")

    # Search each session
    results = []

    for session_info in sessions:
        session_id = session_info['session_id']
        jsonl_path = session_info['file_path']

        try:
            messages = read_conversation(
                session_id=session_id,
                filter_sidechains=True,
                filter_snapshots=True
            )
        except Exception:
            continue  # Skip corrupted sessions

        # Filter and search messages
        for msg in messages:
            # Apply filters
            if role_filter and msg.get('role') != role_filter:
                continue

            if model_filter and model_filter not in str(msg.get('model', '')):
                continue

            if date_from:
                msg_date = msg.get('timestamp', '')[:10]  # YYYY-MM-DD
                if msg_date < date_from:
                    continue

            if date_to:
                msg_date = msg.get('timestamp', '')[:10]
                if msg_date > date_to:
                    continue

            if min_tokens:
                input_tokens = msg.get('usage', {}).get('input_tokens', 0)
                if input_tokens < min_tokens:
                    continue

            # Text search
            content = msg.get('content', '')

            if pattern:
                match = pattern.search(content)
                if not match:
                    continue

                # Extract match highlights
                highlights = []
                for m in pattern.finditer(content):
                    start = max(0, m.start() - 50)
                    end = min(len(content), m.end() + 50)
                    snippet = content[start:end]
                    highlights.append(f"...{snippet}...")
            else:
                highlights = []

            # Add to results
            results.append({
                'session_id': session_id,
                'message_uuid': msg.get('uuid'),
                'timestamp': msg.get('timestamp'),
                'role': msg.get('role'),
                'model': msg.get('model'),
                'content_preview': content[:200],
                'match_highlights': highlights[:3],  # Top 3 matches
                'file_path': jsonl_path,
                'usage': msg.get('usage'),
            })

    return results


def search_session(
    session_id: str,
    query: str,
    project_path: Optional[str] = None,
    case_sensitive: bool = False
) -> List[Dict[str, Any]]:
    """
    Search within a single session.

    Args:
        session_id: Session UUID to search.
        query: Regex pattern to search.
        project_path: Project path. None = auto-detect.
        case_sensitive: Case-sensitive search.

    Returns:
        List of matching messages.
    """
    return search_history(
        query=query,
        project_path=project_path,
        case_sensitive=case_sensitive,
        session_limit=1  # Only search this session
    )


def search_by_metadata(
    project_path: Optional[str] = None,
    role: Optional[str] = None,
    model: Optional[str] = None,
    has_tool_results: bool = False,
    is_sidechain: Optional[bool] = None,
    session_limit: Optional[int] = None
) -> List[Dict[str, Any]]:
    """
    Search by metadata only (no text search).

    Args:
        project_path: Project path. None = auto-detect.
        role: Filter by role.
        model: Filter by model.
        has_tool_results: If True, only messages with tool results.
        is_sidechain: Filter by sidechain status.
        session_limit: Max sessions to search.

    Returns:
        List of matching messages.
    """
    from .utils import get_project_sessions
    from .parser import read_conversation

    sessions = get_project_sessions(project_path)

    if session_limit:
        sessions = sessions[:session_limit]

    results = []

    for session_info in sessions:
        session_id = session_info['session_id']

        try:
            messages = read_conversation(
                session_id=session_id,
                filter_snapshots=True
            )
        except Exception:
            continue

        for msg in messages:
            # Apply filters
            if role and msg.get('role') != role:
                continue

            if model and model not in str(msg.get('model', '')):
                continue

            if has_tool_results and not msg.get('tool_results'):
                continue

            if is_sidechain is not None and msg.get('is_sidechain') != is_sidechain:
                continue

            results.append(msg)

    return results


def find_large_responses(
    min_output_tokens: int = 1000,
    project_path: Optional[str] = None,
    session_limit: Optional[int] = 10
) -> List[Dict[str, Any]]:
    """
    Find large assistant responses.

    Args:
        min_output_tokens: Minimum output token count.
        project_path: Project path.
        session_limit: Max sessions to search.

    Returns:
        List of large responses sorted by token count (descending).
    """
    results = search_by_metadata(
        project_path=project_path,
        role="assistant",
        session_limit=session_limit
    )

    # Filter and sort by output tokens
    large = []
    for msg in results:
        output_tokens = msg.get('usage', {}).get('output_tokens', 0)
        if output_tokens >= min_output_tokens:
            large.append({
                'session_id': msg.get('session_id'),
                'uuid': msg.get('uuid'),
                'timestamp': msg.get('timestamp'),
                'output_tokens': output_tokens,
                'content_preview': msg.get('content', '')[:200]
            })

    large.sort(key=lambda x: x['output_tokens'], reverse=True)
    return large


def find_errors(
    project_path: Optional[str] = None,
    session_limit: Optional[int] = 20
) -> List[Dict[str, Any]]:
    """
    Find error messages in conversation history.

    Args:
        project_path: Project path.
        session_limit: Max sessions to search.

    Returns:
        List of messages containing errors.
    """
    error_patterns = r"error|exception|failed|traceback|warning|critical|fatal"

    return search_history(
        query=error_patterns,
        project_path=project_path,
        session_limit=session_limit,
        case_sensitive=False
    )
