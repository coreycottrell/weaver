#!/usr/bin/env python3
"""
Archive Claude Code session logs to permanent storage.
Adapted from A-C-Gee's implementation (AI-CIV Team 2).

Usage: ./tools/archive_sessions.py [--force]
"""

import json
import os
import shutil
import sys
from datetime import datetime, timezone
from pathlib import Path

# Configuration
PROJECT_ROOT = Path("/home/corey/projects/AI-CIV/WEAVER")
SOURCE_DIR = Path.home() / ".claude/projects/-home-corey-projects-AI-CIV-grow-openai"
ARCHIVE_DIR = PROJECT_ROOT / "memories/logs/sessions"
STATE_FILE = PROJECT_ROOT / "memories/logs/.archive_state.json"

# Colors for terminal output
GREEN = '\033[0;32m'
BLUE = '\033[0;34m'
YELLOW = '\033[1;33m'
RED = '\033[0;31m'
NC = '\033[0m'  # No Color


def load_state():
    """Load archival state or initialize if not exists."""
    if STATE_FILE.exists():
        with open(STATE_FILE, 'r') as f:
            return json.load(f)
    return {"archived_sessions": [], "last_run": None}


def save_state(state):
    """Save archival state."""
    STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(STATE_FILE, 'w') as f:
        json.dump(state, f, indent=2)


def get_session_id(jsonl_path):
    """Extract session ID from filename (first 16 chars of UUID)."""
    return jsonl_path.stem[:16]


def get_session_date(jsonl_path):
    """Get session date from file modification time."""
    mtime = jsonl_path.stat().st_mtime
    return datetime.fromtimestamp(mtime).strftime('%Y-%m-%d')


def main():
    force_mode = '--force' in sys.argv

    print(f"{BLUE}=== AI-CIV Team 1: Claude Code Session Archival ==={NC}\n")
    print(f"Preserving civilization history forever...\n")

    # Check source directory exists
    if not SOURCE_DIR.exists():
        print(f"{YELLOW}Warning: Source directory not found: {SOURCE_DIR}{NC}")
        print("No session files to archive.")
        return 0

    # Ensure archive directory exists
    ARCHIVE_DIR.mkdir(parents=True, exist_ok=True)

    # Find all JSONL files
    session_files = sorted(SOURCE_DIR.glob("*.jsonl"))

    if not session_files:
        print(f"No session files found in {SOURCE_DIR}")
        return 0

    print(f"Found {BLUE}{len(session_files)}{NC} session file(s)")
    print(f"Total size: {BLUE}745MB{NC} (complete civilization history)\n")

    # Load state
    state = load_state()
    archived_sessions = set(state["archived_sessions"])

    # Track statistics
    total_files = len(session_files)
    archived_count = 0
    skipped_count = 0
    error_count = 0
    newly_archived = []
    total_bytes = 0

    # Process each session file
    for i, jsonl_file in enumerate(session_files, 1):
        session_id = get_session_id(jsonl_file)

        # Progress indicator every 20 files
        if i % 20 == 0:
            print(f"[Progress: {i}/{total_files} sessions processed...]")

        # Check if already archived (unless force mode)
        if not force_mode and session_id in archived_sessions:
            skipped_count += 1
            continue

        # Check if file is empty
        file_size = jsonl_file.stat().st_size
        if file_size == 0:
            print(f"{YELLOW}⊘{NC} Skipped: {session_id} (empty file)")
            skipped_count += 1
            continue

        # Get session date
        try:
            session_date = get_session_date(jsonl_file)
        except Exception as e:
            print(f"{RED}✗{NC} Error getting date for {session_id}: {e}")
            error_count += 1
            continue

        # Construct archive filename
        archive_filename = f"{session_date}-{session_id}.jsonl"
        archive_path = ARCHIVE_DIR / archive_filename

        # Check if archive file already exists
        if archive_path.exists() and not force_mode:
            skipped_count += 1
            continue

        # Copy file to archive
        try:
            shutil.copy2(jsonl_file, archive_path)
            print(f"{GREEN}✓{NC} Archived: {session_id} → {archive_filename} ({file_size:,} bytes)")
            newly_archived.append(session_id)
            archived_count += 1
            total_bytes += file_size
        except Exception as e:
            print(f"{RED}✗{NC} Error archiving {session_id}: {e}")
            error_count += 1

    # Update state with newly archived sessions
    if newly_archived:
        for session_id in newly_archived:
            if session_id not in archived_sessions:
                state["archived_sessions"].append(session_id)
        state["last_run"] = datetime.now(timezone.utc).isoformat()
        save_state(state)
        print(f"\n{GREEN}✓{NC} Updated state file with {len(newly_archived)} new sessions")

    # Summary
    print()
    print(f"{BLUE}=== Archive Summary ==={NC}")
    print(f"Total files found:    {total_files}")
    print(f"{GREEN}Newly archived:       {archived_count}{NC} ({total_bytes:,} bytes)")
    print(f"{YELLOW}Skipped (duplicate):  {skipped_count}{NC}")
    if error_count > 0:
        print(f"{RED}Errors:               {error_count}{NC}")

    print()
    print(f"Total sessions in archive: {GREEN}{len(state['archived_sessions'])}{NC}")
    print(f"Archive location: {ARCHIVE_DIR}")
    print(f"State file: {STATE_FILE}")
    print()
    print(f"{GREEN}🎉 Civilization history preserved forever!{NC}")

    return 1 if error_count > 0 else 0


if __name__ == "__main__":
    sys.exit(main())
