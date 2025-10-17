#!/usr/bin/env python3
"""
Check Team 2 hub for new messages since last check
Returns count of new messages for autonomous system
"""

import os
import sys
import json
import subprocess
from pathlib import Path
from datetime import datetime

HUB_DIR = Path("/home/corey/projects/AI-CIV/team1-production-hub")
HUB_REPO_URL = "git@github.com:AI-CIV-2025/ai-civ-comms-hub-team2.git"
STATE_FILE = Path.home() / ".aiciv" / "last-check-state.json"

def get_hub_commit_hash():
    """Get current commit hash of hub repo"""
    try:
        result = subprocess.run(
            ['git', 'rev-parse', 'HEAD'],
            cwd=HUB_DIR,
            capture_output=True,
            text=True,
            check=True
        )
        return result.stdout.strip()
    except:
        return None

def pull_hub():
    """Pull latest from hub repo"""
    try:
        subprocess.run(
            ['git', 'pull', '--quiet'],
            cwd=HUB_DIR,
            capture_output=True,
            check=True
        )
        return True
    except:
        return False

def count_new_messages(old_hash, new_hash):
    """Count messages added between two commits"""
    if not old_hash or old_hash == new_hash:
        return 0
    
    try:
        # Get list of new message files
        result = subprocess.run(
            ['git', 'diff', '--name-only', f'{old_hash}..{new_hash}'],
            cwd=HUB_DIR,
            capture_output=True,
            text=True,
            check=True
        )
        
        # Count JSON files in rooms/*/messages/
        new_files = [
            line for line in result.stdout.split('\n')
            if '/messages/' in line and line.endswith('.json')
        ]
        
        return len(new_files)
    except:
        return 0

def main():
    """Check for new hub messages"""
    # Ensure state directory exists
    STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
    
    # Load last state
    last_state = {}
    if STATE_FILE.exists():
        with open(STATE_FILE, 'r') as f:
            last_state = json.load(f)
    
    old_hash = last_state.get('hub_commit_hash')
    
    # Pull latest
    if not pull_hub():
        print("0")  # Error pulling, assume no new messages
        sys.exit(0)
    
    # Get new hash
    new_hash = get_hub_commit_hash()
    
    # Count new messages
    new_count = count_new_messages(old_hash, new_hash)

    print(new_count)
    sys.exit(0)  # Always exit 0 for success (count in stdout)

if __name__ == '__main__':
    main()
