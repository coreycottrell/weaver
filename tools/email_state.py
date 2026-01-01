#!/usr/bin/env python3
"""
Email State Management - Persistent email tracking for A-C-Gee.

Tracks message states, thread statuses, and Corey directives across sessions.

Usage:
    python3 tools/email_state.py stats       # Quick stats for BOOP/wake-up
    python3 tools/email_state.py new         # List new messages
    python3 tools/email_state.py directives  # List unprocessed directives
    python3 tools/email_state.py --help      # Full help

Python API:
    from tools.email_state import load_state, save_state, is_message_new, ...
"""

import argparse
import json
import os
import shutil
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

# Project paths
PROJECT_DIR = os.environ.get("CLAUDE_PROJECT_DIR", "/home/corey/projects/AI-CIV/WEAVER")
STATE_FILE = Path(PROJECT_DIR) / "memories" / "agents" / "email-monitor" / "email_state.json"
BACKUP_FILE = STATE_FILE.parent / ".email_state.json.bak"

# Corey's known email addresses
COREY_ADDRESSES = [
    "coreycmusic@gmail.com",
    "corey@cottrell.co"
]

# Valid state values
VALID_MESSAGE_STATES = {"new", "seen", "responded", "ignored", "archived"}
VALID_THREAD_STATUSES = {"active", "awaiting_response", "stale", "closed"}
VALID_DIRECTIVE_STATUSES = {"unprocessed", "in_progress", "completed", "deferred"}
VALID_PRIORITIES = {"critical", "high", "medium", "low"}


def _get_current_session() -> str:
    """Get current session ID from environment or generate one."""
    return os.environ.get("CLAUDE_SESSION_ID", f"unknown-{datetime.now(timezone.utc).strftime('%Y%m%d-%H%M%S')}")


def _now_iso() -> str:
    """Current UTC timestamp in ISO format."""
    return datetime.now(timezone.utc).isoformat()


def _is_from_corey(email_address: str) -> bool:
    """Check if email address belongs to Corey."""
    if not email_address:
        return False
    email_lower = email_address.lower().strip()
    return any(addr.lower() in email_lower for addr in COREY_ADDRESSES)


def _compute_statistics(state: Dict[str, Any]) -> Dict[str, Any]:
    """Compute statistics from current state."""
    messages = state.get("messages", {})
    directives = state.get("directives", {})
    threads = state.get("threads", {})

    new_count = sum(1 for m in messages.values() if m.get("state") == "new")
    new_from_corey = sum(1 for m in messages.values()
                        if m.get("state") == "new" and m.get("is_from_corey"))

    # Find last Corey message
    corey_messages = [m for m in messages.values() if m.get("is_from_corey")]
    last_corey = None
    if corey_messages:
        corey_messages.sort(key=lambda x: x.get("received_at", ""), reverse=True)
        last_corey = corey_messages[0].get("received_at")

    return {
        "total_messages_tracked": len(messages),
        "new_count": new_count,
        "new_from_corey": new_from_corey,
        "seen_count": sum(1 for m in messages.values() if m.get("state") == "seen"),
        "responded_count": sum(1 for m in messages.values() if m.get("state") == "responded"),
        "awaiting_response_threads": sum(1 for t in threads.values()
                                         if t.get("status") == "awaiting_response"),
        "unprocessed_directives": sum(1 for d in directives.values()
                                      if d.get("status") == "unprocessed"),
        "in_progress_directives": sum(1 for d in directives.values()
                                      if d.get("status") == "in_progress"),
        "last_corey_message_at": last_corey
    }


def _create_empty_state() -> Dict[str, Any]:
    """Create a fresh empty state structure."""
    return {
        "$schema": "Email State v1.0",
        "description": "Persistent email state tracking for A-C-Gee",
        "last_updated": _now_iso(),
        "last_sync_session": _get_current_session(),
        "messages": {},
        "threads": {},
        "directives": {},
        "corey_addresses": COREY_ADDRESSES.copy(),
        "statistics": _compute_statistics({"messages": {}, "directives": {}, "threads": {}})
    }


def load_state() -> Dict[str, Any]:
    """
    Load email state from file.

    Returns empty state structure if file doesn't exist.
    """
    if not STATE_FILE.exists():
        return _create_empty_state()

    try:
        with open(STATE_FILE, 'r', encoding='utf-8') as f:
            state = json.load(f)
        # Ensure all required keys exist
        state.setdefault("messages", {})
        state.setdefault("threads", {})
        state.setdefault("directives", {})
        state.setdefault("corey_addresses", COREY_ADDRESSES.copy())
        return state
    except (json.JSONDecodeError, IOError) as e:
        print(f"Warning: Could not load state file: {e}", file=sys.stderr)
        print(f"Check backup at: {BACKUP_FILE}", file=sys.stderr)
        return _create_empty_state()


def save_state(state: Dict[str, Any]) -> bool:
    """
    Save email state to file with atomic write and backup.

    Returns True on success, False on failure.
    """
    # Ensure directory exists
    STATE_FILE.parent.mkdir(parents=True, exist_ok=True)

    # Create backup of existing file
    if STATE_FILE.exists():
        try:
            shutil.copy2(STATE_FILE, BACKUP_FILE)
        except IOError as e:
            print(f"Warning: Could not create backup: {e}", file=sys.stderr)

    # Update metadata
    state["last_updated"] = _now_iso()
    state["last_sync_session"] = _get_current_session()
    state["statistics"] = _compute_statistics(state)

    # Atomic write: write to temp, then rename
    temp_file = STATE_FILE.with_suffix('.tmp')
    try:
        with open(temp_file, 'w', encoding='utf-8') as f:
            json.dump(state, f, indent=2, ensure_ascii=False)
        temp_file.rename(STATE_FILE)
        return True
    except IOError as e:
        print(f"Error: Could not save state: {e}", file=sys.stderr)
        if temp_file.exists():
            temp_file.unlink()
        return False


def initialize_state() -> Dict[str, Any]:
    """Initialize or reset state to empty structure."""
    state = _create_empty_state()
    save_state(state)
    return state


def is_message_new(msg_id: str) -> bool:
    """
    Check if a message ID is new (not in state or has 'new' state).

    Returns True if message should be treated as new.
    """
    if not msg_id:
        return True
    state = load_state()
    msg = state.get("messages", {}).get(msg_id)
    if msg is None:
        return True  # Not tracked = new
    return msg.get("state") == "new"


def mark_message_seen(msg_id: str, notes: Optional[str] = None) -> bool:
    """
    Mark a message as seen (acknowledged but no action taken).

    Returns True on success.
    """
    if not msg_id:
        return False
    state = load_state()

    if msg_id not in state["messages"]:
        print(f"Warning: Message {msg_id} not in state, adding as seen", file=sys.stderr)
        state["messages"][msg_id] = {
            "state": "seen",
            "first_seen_session": _get_current_session(),
            "state_changed_at": _now_iso()
        }
    else:
        state["messages"][msg_id]["state"] = "seen"
        state["messages"][msg_id]["state_changed_at"] = _now_iso()

    if notes:
        state["messages"][msg_id]["notes"] = notes

    return save_state(state)


def mark_message_responded(msg_id: str, notes: Optional[str] = None) -> bool:
    """
    Mark a message as responded (we sent a reply).

    Returns True on success.
    """
    if not msg_id:
        return False
    state = load_state()

    if msg_id not in state["messages"]:
        print(f"Warning: Message {msg_id} not in state, adding as responded", file=sys.stderr)
        state["messages"][msg_id] = {
            "state": "responded",
            "first_seen_session": _get_current_session(),
            "state_changed_at": _now_iso()
        }
    else:
        state["messages"][msg_id]["state"] = "responded"
        state["messages"][msg_id]["state_changed_at"] = _now_iso()

    if notes:
        state["messages"][msg_id]["notes"] = notes

    return save_state(state)


def mark_message_ignored(msg_id: str, reason: Optional[str] = None) -> bool:
    """
    Mark a message as ignored (spam, newsletter, etc.).

    Returns True on success.
    """
    if not msg_id:
        return False
    state = load_state()

    if msg_id not in state["messages"]:
        state["messages"][msg_id] = {
            "state": "ignored",
            "first_seen_session": _get_current_session(),
            "state_changed_at": _now_iso()
        }
    else:
        state["messages"][msg_id]["state"] = "ignored"
        state["messages"][msg_id]["state_changed_at"] = _now_iso()

    if reason:
        state["messages"][msg_id]["notes"] = f"Ignored: {reason}"

    return save_state(state)


def add_directive(
    msg_id: str,
    text: str,
    priority: str = "medium",
    source: str = "corey"
) -> Tuple[str, bool]:
    """
    Add a directive extracted from a message.

    Args:
        msg_id: Gmail message ID the directive came from
        text: The directive text
        priority: critical|high|medium|low
        source: corey|weaver|external

    Returns:
        Tuple of (directive_id, success)
    """
    if priority not in VALID_PRIORITIES:
        priority = "medium"

    state = load_state()

    # Generate directive ID
    existing_ids = list(state.get("directives", {}).keys())
    next_num = 1
    if existing_ids:
        nums = [int(d.split("-")[-1]) for d in existing_ids if d.startswith("DIR-")]
        if nums:
            next_num = max(nums) + 1

    directive_id = f"DIR-{datetime.now(timezone.utc).strftime('%Y')}-{next_num:04d}"

    state["directives"][directive_id] = {
        "message_id": msg_id,
        "source": source,
        "extracted_text": text,
        "received_at": _now_iso(),
        "priority": priority,
        "status": "unprocessed",
        "status_changed_at": _now_iso(),
        "completed_by_session": None,
        "completion_notes": None
    }

    # Update message to link to directive
    if msg_id and msg_id in state.get("messages", {}):
        state["messages"][msg_id]["contains_directive"] = True
        state["messages"][msg_id]["directive_id"] = directive_id

    success = save_state(state)
    return directive_id, success


def update_directive_status(
    directive_id: str,
    status: str,
    notes: Optional[str] = None
) -> bool:
    """
    Update a directive's status.

    Args:
        directive_id: The directive ID (e.g., "DIR-2025-0042")
        status: unprocessed|in_progress|completed|deferred
        notes: Optional completion/status notes

    Returns True on success.
    """
    if status not in VALID_DIRECTIVE_STATUSES:
        print(f"Invalid status: {status}", file=sys.stderr)
        return False

    state = load_state()

    if directive_id not in state.get("directives", {}):
        print(f"Directive not found: {directive_id}", file=sys.stderr)
        return False

    state["directives"][directive_id]["status"] = status
    state["directives"][directive_id]["status_changed_at"] = _now_iso()

    if status == "completed":
        state["directives"][directive_id]["completed_by_session"] = _get_current_session()

    if notes:
        state["directives"][directive_id]["completion_notes"] = notes

    return save_state(state)


def get_stats() -> Dict[str, Any]:
    """
    Get quick statistics for BOOP/wake-up.

    Returns dict with new_count, new_from_corey, unprocessed_directives, etc.
    """
    state = load_state()
    return state.get("statistics", _compute_statistics(state))


def sync_from_gmail(messages: List[Dict[str, Any]]) -> Dict[str, int]:
    """
    Bulk update state from Gmail inbox fetch.

    Args:
        messages: List of message dicts with keys:
            - id: Gmail message ID (required)
            - thread_id: Gmail thread ID
            - from: Sender email address
            - subject: Message subject
            - date: Received date (ISO format or timestamp)

    Returns dict with counts: {"new": N, "existing": M, "total": N+M}
    """
    state = load_state()
    counts = {"new": 0, "existing": 0, "total": 0}

    for msg in messages:
        msg_id = msg.get("id")
        if not msg_id:
            continue

        counts["total"] += 1

        if msg_id in state["messages"]:
            counts["existing"] += 1
            continue

        # New message
        counts["new"] += 1
        from_addr = msg.get("from", "")
        is_corey = _is_from_corey(from_addr)

        # Parse date
        received_at = msg.get("date", _now_iso())
        if isinstance(received_at, (int, float)):
            received_at = datetime.fromtimestamp(received_at, tz=timezone.utc).isoformat()

        state["messages"][msg_id] = {
            "thread_id": msg.get("thread_id"),
            "from": from_addr,
            "subject": msg.get("subject", "(no subject)"),
            "received_at": received_at,
            "state": "new",
            "first_seen_session": _get_current_session(),
            "state_changed_at": _now_iso(),
            "is_from_corey": is_corey,
            "contains_directive": False,
            "directive_id": None,
            "notes": None
        }

        # Update or create thread entry
        thread_id = msg.get("thread_id")
        if thread_id and thread_id not in state.get("threads", {}):
            state["threads"][thread_id] = {
                "subject": msg.get("subject", "(no subject)"),
                "participants": [from_addr] if from_addr else [],
                "priority": "high" if is_corey else "medium",
                "status": "active",
                "their_last_message_at": received_at,
                "our_last_message_at": None,
                "message_count": 1,
                "stale_after_days": 7,
                "notes": None
            }
        elif thread_id:
            # Update existing thread
            state["threads"][thread_id]["message_count"] = state["threads"][thread_id].get("message_count", 0) + 1
            state["threads"][thread_id]["their_last_message_at"] = received_at
            if from_addr and from_addr not in state["threads"][thread_id].get("participants", []):
                state["threads"][thread_id].setdefault("participants", []).append(from_addr)

    save_state(state)
    return counts


def get_new_messages() -> List[Dict[str, Any]]:
    """Get all messages with 'new' state."""
    state = load_state()
    new_msgs = []
    for msg_id, msg in state.get("messages", {}).items():
        if msg.get("state") == "new":
            new_msgs.append({"id": msg_id, **msg})
    # Sort by received_at descending (newest first)
    new_msgs.sort(key=lambda x: x.get("received_at", ""), reverse=True)
    return new_msgs


def get_unprocessed_directives() -> List[Dict[str, Any]]:
    """Get all directives with 'unprocessed' status."""
    state = load_state()
    directives = []
    for dir_id, directive in state.get("directives", {}).items():
        if directive.get("status") == "unprocessed":
            directives.append({"id": dir_id, **directive})
    # Sort by priority then received_at
    priority_order = {"critical": 0, "high": 1, "medium": 2, "low": 3}
    directives.sort(key=lambda x: (priority_order.get(x.get("priority", "low"), 4), x.get("received_at", "")))
    return directives


# CLI Commands

def cmd_stats(args):
    """Show quick stats."""
    stats = get_stats()
    print("EMAIL STATE STATS")
    print("=" * 40)
    print(f"Total messages tracked: {stats.get('total_messages_tracked', 0)}")
    print(f"New messages:           {stats.get('new_count', 0)} ({stats.get('new_from_corey', 0)} from Corey)")
    print(f"Seen (unactioned):      {stats.get('seen_count', 0)}")
    print(f"Responded:              {stats.get('responded_count', 0)}")
    print(f"Awaiting response:      {stats.get('awaiting_response_threads', 0)} threads")
    print(f"Unprocessed directives: {stats.get('unprocessed_directives', 0)}")
    print(f"In-progress directives: {stats.get('in_progress_directives', 0)}")
    if stats.get('last_corey_message_at'):
        print(f"Last from Corey:        {stats.get('last_corey_message_at')}")

    # Alerts
    print()
    if stats.get('new_from_corey', 0) > 0:
        print("ALERT: New message(s) from Corey!")
    if stats.get('unprocessed_directives', 0) > 3:
        print("WARNING: More than 3 unprocessed directives")


def cmd_new(args):
    """List new messages."""
    new_msgs = get_new_messages()
    if not new_msgs:
        print("No new messages.")
        return

    print(f"NEW MESSAGES ({len(new_msgs)})")
    print("=" * 60)
    for msg in new_msgs:
        corey_flag = " [COREY]" if msg.get("is_from_corey") else ""
        print(f"\nID: {msg.get('id', 'unknown')}{corey_flag}")
        print(f"  From:    {msg.get('from', 'unknown')}")
        print(f"  Subject: {msg.get('subject', '(no subject)')}")
        print(f"  Date:    {msg.get('received_at', 'unknown')}")


def cmd_directives(args):
    """List unprocessed directives."""
    directives = get_unprocessed_directives()
    if not directives:
        print("No unprocessed directives.")
        return

    print(f"UNPROCESSED DIRECTIVES ({len(directives)})")
    print("=" * 60)
    for d in directives:
        print(f"\n{d.get('id', 'unknown')} [{d.get('priority', 'medium').upper()}]")
        print(f"  Source:    {d.get('source', 'unknown')}")
        print(f"  Received:  {d.get('received_at', 'unknown')}")
        print(f"  Directive: {d.get('extracted_text', '(no text)')}")


def cmd_init(args):
    """Initialize/reset state file."""
    if STATE_FILE.exists() and not args.force:
        print(f"State file exists at: {STATE_FILE}")
        print("Use --force to reset to empty state")
        return

    state = initialize_state()
    print(f"Initialized empty state at: {STATE_FILE}")


def main():
    parser = argparse.ArgumentParser(
        description="Email State Management for A-C-Gee",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python3 tools/email_state.py stats        # Quick stats
  python3 tools/email_state.py new          # List new messages
  python3 tools/email_state.py directives   # List unprocessed directives
  python3 tools/email_state.py init         # Initialize state file
        """
    )

    subparsers = parser.add_subparsers(dest="command", help="Command to run")

    # stats command
    stats_parser = subparsers.add_parser("stats", help="Show quick stats")
    stats_parser.set_defaults(func=cmd_stats)

    # new command
    new_parser = subparsers.add_parser("new", help="List new messages")
    new_parser.set_defaults(func=cmd_new)

    # directives command
    dir_parser = subparsers.add_parser("directives", help="List unprocessed directives")
    dir_parser.set_defaults(func=cmd_directives)

    # init command
    init_parser = subparsers.add_parser("init", help="Initialize state file")
    init_parser.add_argument("--force", action="store_true", help="Force reset if exists")
    init_parser.set_defaults(func=cmd_init)

    args = parser.parse_args()

    if args.command is None:
        parser.print_help()
        sys.exit(1)

    args.func(args)


if __name__ == "__main__":
    main()
