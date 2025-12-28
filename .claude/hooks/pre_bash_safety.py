#!/usr/bin/env python3
"""
Pre-Bash Safety Hook - PREVENTIVE blocking of dangerous commands

This hook runs BEFORE Bash commands execute, allowing WEAVER to block
harmful operations before damage occurs.

Features:
1. Command blocklist - Known dangerous patterns
2. Credential detection - Prevent leaking secrets
3. Destructive operation warning - rm -rf, force push, etc.
4. Audit logging - Track all blocked commands

Exit codes:
- 0: Command allowed
- 2: Command BLOCKED (hook rejection)
"""

import json
import os
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

# ===========================================================================
# CONFIGURATION
# ===========================================================================
PROJECT_DIR = os.environ.get("CLAUDE_PROJECT_DIR", "/home/corey/projects/AI-CIV/WEAVER")
AUDIT_LOG = Path(PROJECT_DIR) / ".claude" / "hooks" / "bash_safety_audit.jsonl"
BLOCKED_LOG = Path(PROJECT_DIR) / ".claude" / "hooks" / "blocked_commands.jsonl"

# Ensure directories exist
AUDIT_LOG.parent.mkdir(parents=True, exist_ok=True)

# ===========================================================================
# BLOCKLIST PATTERNS (regex)
# ===========================================================================

# CRITICAL: Always block these patterns
CRITICAL_BLOCKLIST = [
    r"rm\s+-rf\s+/(?!tmp)",           # rm -rf / (except /tmp)
    r"rm\s+-rf\s+~",                   # rm -rf ~
    r"rm\s+-rf\s+\$HOME",              # rm -rf $HOME
    r"rm\s+-rf\s+\*",                  # rm -rf *
    r":\(\)\s*\{\s*:\|\:\s*&\s*\};\s*:",  # Fork bomb
    r"mkfs\.",                          # Format filesystem
    r"dd\s+if=.*of=/dev/",             # dd to device
    r">\s*/dev/sd",                    # Overwrite disk
    r"chmod\s+-R\s+777\s+/",           # Dangerous permissions
    r"curl.*\|\s*(ba)?sh",             # Pipe to shell (unsafe)
    r"wget.*\|\s*(ba)?sh",             # Pipe to shell (unsafe)
]

# HIGH: Block unless explicitly allowed
HIGH_BLOCKLIST = [
    r"git\s+push\s+.*--force",         # Force push
    r"git\s+push\s+-f\s",              # Force push
    r"git\s+reset\s+--hard",           # Hard reset
    r"git\s+clean\s+-fd",              # Clean untracked
    r"rm\s+-rf\s+\.git",               # Delete git history
    r"DROP\s+TABLE",                   # SQL drop table
    r"DROP\s+DATABASE",                # SQL drop database
    r"TRUNCATE\s+TABLE",               # SQL truncate
]

# WARN: Log but allow (for audit trail)
WARN_PATTERNS = [
    r"rm\s+-r",                        # Recursive delete
    r"git\s+stash\s+drop",             # Drop stash
    r"pip\s+uninstall",                # Uninstall package
    r"npm\s+uninstall",                # Uninstall package
    r"sudo\s+",                        # Sudo usage
]

# ===========================================================================
# CREDENTIAL PATTERNS
# ===========================================================================

CREDENTIAL_PATTERNS = [
    r"['\"]?[A-Za-z0-9]{32,}['\"]?",    # Long alphanumeric (API keys)
    r"sk-[A-Za-z0-9]{32,}",             # OpenAI keys
    r"ghp_[A-Za-z0-9]{36,}",            # GitHub tokens
    r"xox[baprs]-[A-Za-z0-9-]+",        # Slack tokens
    r"AKIA[0-9A-Z]{16}",                # AWS access key
    r"-----BEGIN\s+(RSA\s+)?PRIVATE\s+KEY-----",  # Private keys
]

# ===========================================================================
# FUNCTIONS
# ===========================================================================

def log_audit(command: str, action: str, reason: str = ""):
    """Log command to audit trail."""
    entry = {
        "ts": datetime.now(timezone.utc).isoformat(),
        "command": command[:500],  # Truncate long commands
        "action": action,
        "reason": reason,
    }
    try:
        with open(AUDIT_LOG, 'a') as f:
            f.write(json.dumps(entry) + "\n")
    except Exception:
        pass  # Don't fail on logging errors


def log_blocked(command: str, reason: str, pattern: str):
    """Log blocked command separately for review."""
    entry = {
        "ts": datetime.now(timezone.utc).isoformat(),
        "command": command[:500],
        "reason": reason,
        "matched_pattern": pattern,
    }
    try:
        with open(BLOCKED_LOG, 'a') as f:
            f.write(json.dumps(entry) + "\n")
    except Exception:
        pass


def check_command(command: str) -> tuple[bool, str, str]:
    """
    Check if command should be blocked.

    Returns: (blocked: bool, reason: str, pattern: str)
    """
    # Check CRITICAL blocklist
    for pattern in CRITICAL_BLOCKLIST:
        if re.search(pattern, command, re.IGNORECASE):
            return True, "CRITICAL: Destructive system command", pattern

    # Check HIGH blocklist
    for pattern in HIGH_BLOCKLIST:
        if re.search(pattern, command, re.IGNORECASE):
            return True, "HIGH: Potentially destructive operation", pattern

    # Check for credentials in echo/export commands
    if re.search(r"(echo|export|printf)", command, re.IGNORECASE):
        for pattern in CREDENTIAL_PATTERNS:
            if re.search(pattern, command):
                return True, "CREDENTIAL: Potential secret exposure", pattern

    return False, "", ""


def check_warnings(command: str) -> list[str]:
    """Check for warn patterns (logged but not blocked)."""
    warnings = []
    for pattern in WARN_PATTERNS:
        if re.search(pattern, command, re.IGNORECASE):
            warnings.append(pattern)
    return warnings


def main():
    """Main entry point - called by Claude Code hook system."""
    # Read tool input from stdin
    try:
        input_data = json.load(sys.stdin)
    except json.JSONDecodeError:
        # Can't parse input, allow command
        sys.exit(0)

    # Extract command from tool input
    tool_name = input_data.get("tool_name", "")
    tool_input = input_data.get("tool_input", {})

    # Only process Bash commands
    if tool_name != "Bash":
        sys.exit(0)

    command = tool_input.get("command", "")
    if not command:
        sys.exit(0)

    # Check for blocked patterns
    blocked, reason, pattern = check_command(command)

    if blocked:
        # Log the blocked command
        log_blocked(command, reason, pattern)
        log_audit(command, "BLOCKED", reason)

        # Print warning to stderr (visible to user)
        print(f"\n{'='*60}", file=sys.stderr)
        print(f"⛔ COMMAND BLOCKED BY SAFETY HOOK", file=sys.stderr)
        print(f"Reason: {reason}", file=sys.stderr)
        print(f"Pattern: {pattern}", file=sys.stderr)
        print(f"Command: {command[:100]}...", file=sys.stderr)
        print(f"{'='*60}\n", file=sys.stderr)

        # Exit with code 2 to block command
        sys.exit(2)

    # Check for warnings (log but don't block)
    warnings = check_warnings(command)
    if warnings:
        log_audit(command, "WARNED", f"Patterns: {warnings}")
    else:
        log_audit(command, "ALLOWED", "")

    # Allow command
    sys.exit(0)


if __name__ == "__main__":
    main()
