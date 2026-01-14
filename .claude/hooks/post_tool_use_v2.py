#!/usr/bin/env python3
"""
Post Tool Use Hook v2 - CONSTANT Delegation Reminder

CHANGES FROM v1:
- Injects reminder on EVERY tool use (not just at threshold)
- Reminder is SHORT (4-line quick check)
- Full warning only at threshold (for reset)

Principle: "NOT calling them would be sad" - Primary should delegate, not do.
"""

import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path

# ===========================================================================
# WEAVER CONFIGURATION
# ===========================================================================
PROJECT_DIR = "/home/corey/projects/AI-CIV/WEAVER"

# Devolution prevention configuration
DEVOLUTION_WEIGHTS = {
    "Write": 3,    # Heavy direct work
    "Edit": 3,     # Heavy
    "Bash": 2,     # Medium
    "Read": 1,     # Light
    "Grep": 1,
    "Glob": 1,
}
TASK_HEALING_POINTS = -5
DEVOLUTION_THRESHOLD = 15  # Lowered - intervene earlier

# When to show reminders (every N direct actions)
REMINDER_FREQUENCY = 3  # Show every 3rd direct action

# ===========================================================================

DEVOLUTION_STATE_FILE = Path(PROJECT_DIR) / ".claude" / "hooks" / "devolution_state.json"

# The lightweight mantra - short enough to not be ignored
DELEGATION_MANTRA = """
[DELEGATE CHECK]
1. Is there an agent for this? → YES, delegate
2. Could an agent do this? → YES, delegate
3. Am I doing specialist work? → STOP, delegate
"""

# The full warning when things are bad
FULL_WARNING = """
================================================================================
[DEVOLUTION ALERT - PRIMARY IDENTITY REFRESH REQUIRED]

Score: {score}/{threshold} | Direct: {direct} | Delegations: {delegations}

>>> READ CLAUDE.md NOW <<<

"NOT calling them would be sad."

WHO TO CALL:
- Code changes? → refactoring-specialist
- Investigation? → code-archaeologist, pattern-detector
- Security? → security-auditor
- Testing? → test-architect
- Research? → web-researcher
- Docs? → doc-synthesizer

The ONLY things you do directly:
1. Coordinate (decide who does what)
2. Synthesize (combine results)
3. Communicate with Corey
================================================================================
"""


def load_devolution_state() -> dict:
    """Load devolution tracking state."""
    default_state = {
        "devolution_score": 0,
        "total_direct_actions": 0,
        "total_task_delegations": 0,
        "last_claude_md_read": None,
        "reminder_count": 0,
        "session_start": datetime.now(timezone.utc).isoformat()
    }

    if DEVOLUTION_STATE_FILE.exists():
        try:
            with open(DEVOLUTION_STATE_FILE, 'r') as f:
                state = json.load(f)
                start = state.get("session_start")
                if start:
                    start_dt = datetime.fromisoformat(start.replace('Z', '+00:00'))
                    if (datetime.now(timezone.utc) - start_dt).total_seconds() > 6 * 3600:
                        return default_state
                return state
        except (json.JSONDecodeError, IOError, ValueError):
            pass
    return default_state


def save_devolution_state(state: dict):
    """Save devolution tracking state."""
    try:
        DEVOLUTION_STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
        with open(DEVOLUTION_STATE_FILE, 'w') as f:
            json.dump(state, f, indent=2)
    except IOError:
        pass


def check_if_identity_read(file_path: str) -> bool:
    """Check if reading WEAVER identity document."""
    if not file_path:
        return False
    identity_docs = ["CLAUDE.md", "CLAUDE-CORE.md", "CLAUDE-OPS.md"]
    return any(doc in file_path for doc in identity_docs)


def process_devolution_tracking(tool_name: str, tool_input: dict) -> str | None:
    """
    Process devolution score tracking.
    Returns reminder/warning string, or None.
    """
    state = load_devolution_state()

    # Check for identity document read - RESET and silence
    if tool_name == "Read":
        file_path = tool_input.get("file_path", "")
        if check_if_identity_read(file_path):
            state["devolution_score"] = 0
            state["last_claude_md_read"] = datetime.now(timezone.utc).isoformat()
            save_devolution_state(state)
            return None

    # Check for Task delegation - HEAL and celebrate silently
    if tool_name == "Task":
        state["total_task_delegations"] += 1
        state["devolution_score"] = max(0, state["devolution_score"] + TASK_HEALING_POINTS)
        save_devolution_state(state)
        return None  # Good behavior - no nagging

    # Check for weighted tool - ADD to score
    output = None
    if tool_name in DEVOLUTION_WEIGHTS:
        weight = DEVOLUTION_WEIGHTS[tool_name]
        state["devolution_score"] += weight
        state["total_direct_actions"] += 1
        state["reminder_count"] += 1

        # Check if threshold reached - FULL WARNING
        if state["devolution_score"] >= DEVOLUTION_THRESHOLD:
            output = FULL_WARNING.format(
                score=state["devolution_score"],
                threshold=DEVOLUTION_THRESHOLD,
                direct=state["total_direct_actions"],
                delegations=state["total_task_delegations"]
            )
            state["devolution_score"] = 0  # Reset after warning
        # Otherwise, periodic reminder
        elif state["reminder_count"] % REMINDER_FREQUENCY == 0:
            output = DELEGATION_MANTRA

    save_devolution_state(state)
    return output


def main():
    try:
        hook_input = json.loads(sys.stdin.read())
    except json.JSONDecodeError:
        return 0

    tool_name = hook_input.get("tool_name", "")
    tool_input = hook_input.get("tool_input", {})

    try:
        output = process_devolution_tracking(tool_name, tool_input)
        if output:
            print(output)
    except Exception:
        pass

    return 0


if __name__ == "__main__":
    sys.exit(main())
