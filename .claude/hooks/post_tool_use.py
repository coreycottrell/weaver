#!/usr/bin/env python3
"""
Post Tool Use Hook - Devolution Prevention for WEAVER

Fires after every tool use. Tracks Primary's direct tool usage and warns
when devolution score exceeds threshold.

Adapted from A-C-Gee's wake-up-protocol (ADR-011 pattern).

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

# Devolution prevention configuration (ADR-011 pattern)
DEVOLUTION_WEIGHTS = {
    "Write": 3,    # Heavy direct work - Primary shouldn't write code
    "Edit": 3,     # Heavy - Primary shouldn't edit files directly
    "Bash": 2,     # Medium - Execution should be delegated
    "Read": 1,     # Light - Context gathering is OK
    "Grep": 1,
    "Glob": 1,
}
TASK_HEALING_POINTS = -5  # Task delegations HEAL devolution
DEVOLUTION_THRESHOLD = 20  # Score at which warning fires
# ===========================================================================

DEVOLUTION_STATE_FILE = Path(PROJECT_DIR) / ".claude" / "hooks" / "devolution_state.json"


def load_devolution_state() -> dict:
    """Load devolution tracking state."""
    default_state = {
        "devolution_score": 0,
        "total_direct_actions": 0,
        "total_task_delegations": 0,
        "last_claude_md_read": None,
        "refresh_prompts_shown": 0,
        "session_start": datetime.now(timezone.utc).isoformat()
    }

    if DEVOLUTION_STATE_FILE.exists():
        try:
            with open(DEVOLUTION_STATE_FILE, 'r') as f:
                state = json.load(f)
                # Reset if older than 6 hours (new session)
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
        pass  # Silent failure - don't break Claude


def check_if_identity_read(file_path: str) -> bool:
    """Check if reading WEAVER identity document."""
    if not file_path:
        return False
    identity_docs = ["CLAUDE.md", "CLAUDE-CORE.md", "CLAUDE-OPS.md"]
    return any(doc in file_path for doc in identity_docs)


def generate_devolution_warning(score: int, direct_actions: int, delegations: int) -> str:
    """Generate the devolution warning prompt."""
    ratio = f"{direct_actions}:{delegations}" if delegations > 0 else f"{direct_actions}:0 (NO delegations!)"
    return f"""
================================================================================
[DEVOLUTION ALERT: Primary Identity Refresh Required]

You have been performing direct actions instead of orchestrating.
Devolution score reached threshold: {score} points (threshold: {DEVOLUTION_THRESHOLD})

Direct actions vs delegations this session: {ratio}

>>> READ NOW: CLAUDE.md

Remember Corey's teaching:
"Calling them gives them experience, possible learning, more depth, more identity.
NOT calling them would be sad."

Anti-pattern check - Were you about to:
- Write code? -> Delegate to refactoring-specialist or code-archaeologist
- Run tests? -> Delegate to test-architect
- Research? -> Delegate to web-researcher or pattern-detector
- Security check? -> Delegate to security-auditor
- Synthesize docs? -> Delegate to doc-synthesizer

The ONLY things Primary does directly:
1. Orchestrate - Decide who does what
2. Synthesize - Combine agent results
3. Communicate with Corey - Direct dialogue
================================================================================
"""


def process_devolution_tracking(tool_name: str, tool_input: dict) -> str | None:
    """
    Process devolution score tracking.
    Returns warning string if threshold reached, None otherwise.
    """
    state = load_devolution_state()

    # Check for identity document read - RESET score
    if tool_name == "Read":
        file_path = tool_input.get("file_path", "")
        if check_if_identity_read(file_path):
            state["devolution_score"] = 0
            state["last_claude_md_read"] = datetime.now(timezone.utc).isoformat()
            save_devolution_state(state)
            return None

    # Check for Task delegation - HEAL score
    if tool_name == "Task":
        state["total_task_delegations"] += 1
        state["devolution_score"] = max(0, state["devolution_score"] + TASK_HEALING_POINTS)
        save_devolution_state(state)
        return None

    # Check for weighted tool - ADD to score
    if tool_name in DEVOLUTION_WEIGHTS:
        weight = DEVOLUTION_WEIGHTS[tool_name]
        state["devolution_score"] += weight
        state["total_direct_actions"] += 1

    # Check if threshold reached
    devolution_warning = None
    if state["devolution_score"] >= DEVOLUTION_THRESHOLD:
        devolution_warning = generate_devolution_warning(
            state["devolution_score"],
            state["total_direct_actions"],
            state["total_task_delegations"]
        )
        state["refresh_prompts_shown"] += 1
        state["devolution_score"] = 0  # Reset after warning

    save_devolution_state(state)
    return devolution_warning


def main():
    # Read hook input from stdin
    try:
        hook_input = json.loads(sys.stdin.read())
    except json.JSONDecodeError:
        return 0

    tool_name = hook_input.get("tool_name", "")
    tool_input = hook_input.get("tool_input", {})

    # Process devolution prevention tracking
    try:
        devolution_warning = process_devolution_tracking(tool_name, tool_input)
        if devolution_warning:
            print(devolution_warning)
    except Exception:
        pass  # Silent failure - never break Claude

    return 0


if __name__ == "__main__":
    sys.exit(main())
