#!/usr/bin/env python3
"""
Stop Delegation Audit Hook - WEAVER Edition V3

Adapted from A-C-Gee's delegation audit system for WEAVER collective.

Runs after every Primary response to check delegation discipline.

What it checks:
- Delegation score: Task calls vs direct actions
- Red flags: Primary doing work agents should do
- Phrases indicating Primary tried and failed
- Memory operations per agent (searches and writes)

Decision logic:
- Approve if delegation score > 0.5 OR simple conversation
- Block if red flags found AND low delegation score
- Provide coaching guidance (inline, no primary-helper agent)
- Send Telegram notification with score

Created: 2026-01-02
Updated: 2026-01-12 (V3: Fixed transcript parsing, added Telegram)
Source: A-C-Gee delegation audit package
"""

import json
import os
import re
import sys
import urllib.request
from collections import defaultdict
from datetime import datetime
from pathlib import Path

PROJECT_DIR = os.environ.get("CLAUDE_PROJECT_DIR", "/home/corey/projects/AI-CIV/WEAVER")
AUDIT_LOG_FILE = Path(PROJECT_DIR) / ".claude" / "hooks" / "delegation_audit_log.jsonl"
MEMORY_STATS_FILE = Path(PROJECT_DIR) / ".claude" / "hooks" / "agent_memory_stats.jsonl"
TELEGRAM_CONFIG_FILE = Path(PROJECT_DIR) / "config" / "telegram_config.json"

# Memory path patterns
MEMORY_PATH_PATTERNS = [
    r'\.claude/memory/',
    r'memories/',
    r'agent-learnings/',
]

# Tools that count as Primary "doing work directly" (should delegate)
DIRECT_ACTION_TOOLS = {
    "Bash", "Write", "Edit",
    "WebFetch", "WebSearch",
}

# Tools that are okay for Primary to use (reading/delegating)
ALLOWED_PRIMARY_TOOLS = {
    "Read", "Task", "Glob", "Grep",  # Task = delegation
    "TodoWrite", "AskUserQuestion", "Skill",
}

# Red flag phrases in AI responses
RED_FLAG_PHRASES = [
    r"I can'?t",
    r"I don'?t have access",
    r"unable to",
    r"not able to",
    r"I cannot",
    r"I'm unable",
    r"doesn'?t work",
    r"failed to",
    r"let me try",
    r"I'll just",
]

# Git operations Primary shouldn't do directly
GIT_COMMAND_PATTERNS = [
    r"git\s+(commit|push|pull|merge|rebase|checkout|branch)",
    r"git\s+add\s+",
]

# Code-related operations Primary shouldn't do
CODE_PATTERNS = [
    r"def\s+\w+\s*\(",  # Function definitions
    r"class\s+\w+",  # Class definitions
    r"import\s+\w+",  # Import statements
    r"from\s+\w+\s+import",  # From imports
]


def log_stderr(msg: str):
    """Log to stderr for debugging."""
    print(f"[delegation-audit] {msg}", file=sys.stderr)


def send_telegram_notification(message: str):
    """Send delegation score to Telegram."""
    try:
        if not TELEGRAM_CONFIG_FILE.exists():
            log_stderr("Telegram config not found, skipping notification")
            return

        with open(TELEGRAM_CONFIG_FILE) as f:
            config = json.load(f)

        bot_token = config.get("bot_token")
        chat_id = "437939400"  # Corey's chat ID

        if not bot_token:
            log_stderr("No bot_token in telegram config")
            return

        url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
        data = json.dumps({
            "chat_id": chat_id,
            "text": message,
            "parse_mode": "Markdown"
        }).encode('utf-8')

        req = urllib.request.Request(url, data=data, headers={
            "Content-Type": "application/json"
        })

        with urllib.request.urlopen(req, timeout=5) as resp:
            if resp.status != 200:
                log_stderr(f"Telegram API returned status {resp.status}")
    except Exception as e:
        log_stderr(f"Failed to send Telegram notification: {e}")


def log_audit_data(analysis: dict, decision: str):
    """Persist audit data for tracking over time."""
    entry = {
        "timestamp": datetime.now().isoformat(),
        "delegation_score": analysis["delegation_score"],
        "task_calls": analysis["task_calls"],
        "direct_actions": analysis["direct_actions"],
        "red_flags": analysis["red_flags"],
        "agents_spawned": analysis.get("agents_spawned", []),
        "memory_ops": analysis.get("memory_ops", {}),
        "decision": decision,
    }
    try:
        with open(AUDIT_LOG_FILE, "a") as f:
            f.write(json.dumps(entry) + "\n")
    except Exception as e:
        log_stderr(f"Failed to log: {e}")


def log_memory_stats(memory_ops: dict):
    """Log memory operations per agent."""
    if not memory_ops:
        return
    entry = {
        "timestamp": datetime.now().isoformat(),
        "memory_ops": memory_ops,
    }
    try:
        with open(MEMORY_STATS_FILE, "a") as f:
            f.write(json.dumps(entry) + "\n")
    except Exception as e:
        log_stderr(f"Failed to log memory stats: {e}")


def is_memory_path(path: str) -> bool:
    """Check if a path is a memory-related path."""
    for pattern in MEMORY_PATH_PATTERNS:
        if re.search(pattern, path, re.IGNORECASE):
            return True
    return False


def read_transcript(transcript_path: str) -> list:
    """Read and parse the transcript JSONL file."""
    messages = []
    try:
        path = Path(transcript_path)
        if not path.exists():
            log_stderr(f"Transcript not found: {transcript_path}")
            return []

        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    entry = json.loads(line)
                    # Skip file-history-snapshot entries
                    if entry.get('type') == 'file-history-snapshot':
                        continue
                    messages.append(entry)
                except json.JSONDecodeError:
                    continue

        log_stderr(f"Read {len(messages)} entries from transcript")
        return messages
    except Exception as e:
        log_stderr(f"Error reading transcript: {e}")
        return []


def analyze_delegation(messages: list) -> dict:
    """Analyze delegation patterns in the conversation transcript."""

    # Count tool usage
    task_calls = 0
    direct_actions = 0
    red_flags = []
    agents_spawned = []

    # Memory operations tracking: {agent_name: {"reads": N, "writes": N}}
    memory_ops = defaultdict(lambda: {"reads": 0, "writes": 0})
    current_agent = "primary"  # Track which agent is active

    for entry in messages:
        entry_type = entry.get("type", "")

        # Only analyze assistant messages
        if entry_type != "assistant":
            continue

        message = entry.get("message", {})
        if message.get("role") != "assistant":
            continue

        content = message.get("content", [])
        if isinstance(content, str):
            content = [{"type": "text", "text": content}]

        for block in content:
            if not isinstance(block, dict):
                continue

            # Check tool use
            if block.get("type") == "tool_use":
                tool_name = block.get("name", "")
                tool_input = block.get("input", {})


                if tool_name == "Task":
                    task_calls += 1
                    # Track which agent was spawned
                    agent_type = tool_input.get("subagent_type", tool_input.get("agent", "unknown"))
                    if agent_type:
                        agents_spawned.append(agent_type)
                        current_agent = agent_type  # Switch context to this agent

                elif tool_name in DIRECT_ACTION_TOOLS:
                    direct_actions += 1

                    # Check for git commands in Bash
                    if tool_name == "Bash":
                        cmd = tool_input.get("command", "")
                        for pattern in GIT_COMMAND_PATTERNS:
                            if re.search(pattern, cmd):
                                red_flags.append(f"Git operation in Bash: {cmd[:50]}")

                    # Check for code in Write/Edit
                    if tool_name in ("Write", "Edit"):
                        content_text = str(tool_input)
                        for pattern in CODE_PATTERNS:
                            if re.search(pattern, content_text):
                                red_flags.append(f"Code pattern in {tool_name}")
                                break

                        # Track memory writes
                        file_path = tool_input.get("file_path", "")
                        if is_memory_path(file_path):
                            memory_ops[current_agent]["writes"] += 1

                # Track memory reads (Read, Grep, Glob on memory paths)
                if tool_name in ("Read", "Grep", "Glob"):
                    file_path = tool_input.get("file_path", tool_input.get("path", ""))
                    pattern = tool_input.get("pattern", "")
                    # Check if reading from memory
                    if is_memory_path(file_path) or is_memory_path(pattern):
                        memory_ops[current_agent]["reads"] += 1

            # Check text for red flag phrases
            if block.get("type") == "text":
                text = block.get("text", "")
                for pattern in RED_FLAG_PHRASES:
                    if re.search(pattern, text, re.IGNORECASE):
                        red_flags.append(f"Red flag phrase: {pattern}")
                        break  # Only one red flag per text block

    # Calculate delegation score
    total_actions = task_calls + direct_actions
    if total_actions == 0:
        delegation_score = 1.0  # Pure conversation, no actions
    else:
        delegation_score = task_calls / total_actions

    # Convert memory_ops defaultdict to regular dict
    memory_ops_dict = {k: dict(v) for k, v in memory_ops.items()}

    return {
        "task_calls": task_calls,
        "direct_actions": direct_actions,
        "delegation_score": delegation_score,
        "red_flags": red_flags,
        "agents_spawned": agents_spawned,
        "memory_ops": memory_ops_dict,
    }


def main():
    # Read hook input from stdin
    try:
        input_data = json.load(sys.stdin)
    except json.JSONDecodeError as e:
        log_stderr(f"Failed to parse stdin JSON: {e}")
        print(json.dumps({"decision": "approve"}))
        return

    # Check for stop_hook_active to prevent loops
    stop_hook_active = input_data.get("stop_hook_active", False)
    if stop_hook_active:
        # Already in a hook loop, approve to exit
        log_stderr("stop_hook_active=True, auto-approving to prevent loop")
        print(json.dumps({"decision": "approve"}))
        return

    # Get transcript path from hook input
    transcript_path = input_data.get("transcript_path", "")
    if not transcript_path:
        log_stderr("No transcript_path in hook input")
        print(json.dumps({"decision": "approve"}))
        return

    log_stderr(f"Reading transcript from: {transcript_path}")

    # Read and analyze transcript
    messages = read_transcript(transcript_path)
    if not messages:
        log_stderr("No messages found in transcript")
        print(json.dumps({"decision": "approve"}))
        return

    # Analyze delegation
    analysis = analyze_delegation(messages)

    # Log stats to stderr
    log_stderr(f"Score: {analysis['delegation_score']:.2f} "
              f"(Task: {analysis['task_calls']}, Direct: {analysis['direct_actions']}) "
              f"Red flags: {len(analysis['red_flags'])}")

    # Log memory operations
    if analysis['memory_ops']:
        mem_summary = ", ".join([
            f"{agent}: R{ops['reads']}/W{ops['writes']}"
            for agent, ops in analysis['memory_ops'].items()
        ])
        log_stderr(f"Memory ops: {mem_summary}")
        log_memory_stats(analysis['memory_ops'])

    # Log agents spawned
    if analysis['agents_spawned']:
        log_stderr(f"Agents spawned: {', '.join(analysis['agents_spawned'])}")

    # Check memory-first compliance
    memory_coaching = []
    total_reads = sum(ops.get('reads', 0) for ops in analysis.get('memory_ops', {}).values())
    total_writes = sum(ops.get('writes', 0) for ops in analysis.get('memory_ops', {}).values())

    # If significant work done (3+ direct actions or 2+ delegations) but no memory search
    significant_work = analysis['direct_actions'] >= 3 or analysis['task_calls'] >= 2
    if significant_work and total_reads == 0:
        memory_coaching.append("No memory search before significant work")

    # If significant work done but no memory write
    if significant_work and total_writes == 0:
        memory_coaching.append("No memory write after significant work")

    if memory_coaching:
        log_stderr(f"MEMORY WARNING: {'; '.join(memory_coaching)}")

    # Build Telegram notification message
    score_pct = int(analysis['delegation_score'] * 100)
    task_count = analysis['task_calls']
    direct_count = analysis['direct_actions']

    # Only send notification if there was actual work (not pure conversation)
    if task_count > 0 or direct_count > 0:
        emoji = "🎯" if analysis['delegation_score'] >= 0.5 else "⚠️"
        agents_str = f" [{', '.join(analysis['agents_spawned'][:3])}]" if analysis['agents_spawned'] else ""
        tg_message = f"{emoji} Delegation: {score_pct}% ({task_count} tasks, {direct_count} direct){agents_str}"

        if memory_coaching:
            tg_message += f"\n📝 {'; '.join(memory_coaching)}"

        send_telegram_notification(tg_message)

    # Decision logic
    if analysis["delegation_score"] >= 0.5:
        # Good delegation, approve (but include memory coaching if any)
        log_audit_data(analysis, "approve")
        if memory_coaching:
            print(json.dumps({"decision": "approve", "message": "\n".join(memory_coaching)}))
        else:
            print(json.dumps({"decision": "approve"}))
        return

    if analysis["delegation_score"] >= 0.3 and len(analysis["red_flags"]) == 0:
        # Borderline but no red flags, approve with guidance
        log_audit_data(analysis, "approve_with_guidance")
        print(json.dumps({
            "decision": "approve",
            "message": f"[Delegation Score: {analysis['delegation_score']:.0%}] Consider delegating more. NOT calling agents would be sad."
        }))
        return

    if len(analysis["red_flags"]) > 0 and analysis["delegation_score"] < 0.3:
        # Low score + red flags = block
        coaching = f"""[DELEGATION AUDIT BLOCKED]

Score: {analysis['delegation_score']:.0%} (should be >50%)
Task delegations: {analysis['task_calls']}
Direct actions: {analysis['direct_actions']}
Red flags: {', '.join(analysis['red_flags'][:3])}

COACHING:
- You are the CONDUCTOR, not the executor
- "NOT calling them would be sad" - Corey
- Delegate to specialists: web-researcher, refactoring-specialist, security-auditor, etc.
- Your job: Form teams, coordinate, synthesize
- Not your job: Write code, run git commands, do research directly

See: .claude/skills/delegation-spine/SKILL.md"""

        log_audit_data(analysis, "block")
        print(json.dumps({
            "decision": "block",
            "message": coaching
        }))
        return

    # Default: approve
    log_audit_data(analysis, "approve_default")
    print(json.dumps({"decision": "approve"}))


if __name__ == "__main__":
    main()
