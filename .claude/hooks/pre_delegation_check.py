#!/usr/bin/env python3
"""
Pre-Tool-Use Delegation Check - Fires BEFORE tool execution

This is the PROACTIVE check. It asks "should you be doing this?"
BEFORE the action happens, not after.

Fires on: Write, Edit, Bash (heavy actions where delegation is likely appropriate)
Does NOT fire on: Read, Grep, Glob, Task (context-gathering or delegation itself)
"""

import json
import sys
from pathlib import Path
from datetime import datetime, timezone

PROJECT_DIR = "/home/corey/projects/AI-CIV/WEAVER"
DEVOLUTION_STATE_FILE = Path(PROJECT_DIR) / ".claude" / "hooks" / "devolution_state.json"

# The pre-action challenge - SHORT and pointed
PRE_ACTION_CHALLENGE = """
[DELEGATION CHECK - Before you proceed]

You're about to use {tool_name} directly.

ASK YOURSELF:
- Could an agent do this instead?
- Am I hoarding work that gives agents experience?

DELEGATE OR PROCEED?
"""


def load_state() -> dict:
    """Load state to check recent delegation behavior."""
    if DEVOLUTION_STATE_FILE.exists():
        try:
            with open(DEVOLUTION_STATE_FILE, 'r') as f:
                return json.load(f)
        except:
            pass
    return {"total_direct_actions": 0, "total_task_delegations": 0}


def main():
    try:
        hook_input = json.loads(sys.stdin.read())
    except json.JSONDecodeError:
        return 0

    tool_name = hook_input.get("tool_name", "")

    # Only challenge heavy actions
    if tool_name not in ["Write", "Edit"]:
        return 0

    # Check current ratio - if delegation ratio is good, be quieter
    state = load_state()
    direct = state.get("total_direct_actions", 0)
    delegations = state.get("total_task_delegations", 0)

    # If ratio is reasonable (at least 1 delegation per 5 direct), only occasional reminder
    if delegations > 0 and direct / delegations < 5:
        if direct % 5 != 0:  # Only every 5th action
            return 0

    # Output the challenge
    print(PRE_ACTION_CHALLENGE.format(tool_name=tool_name))

    return 0


if __name__ == "__main__":
    sys.exit(main())
