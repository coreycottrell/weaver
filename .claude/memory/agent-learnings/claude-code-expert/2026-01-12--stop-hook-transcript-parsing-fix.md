# Stop Hook Transcript Parsing Fix

**Date**: 2026-01-12
**Agent**: claude-code-expert
**Type**: technique / gotcha

---

## Problem

The `stop_delegation_audit.py` hook was running but NOT detecting any tool usage. Log showed:
```
delegation_score: 1.0, task_calls: 0, direct_actions: 0
```

## Root Cause

**Transcript format mismatch.** The hook expected messages in stdin input (`input_data.get("messages", [])`), but Claude Code's Stop hook provides:

```json
{
  "session_id": "...",
  "transcript_path": "/path/to/session.jsonl",
  "cwd": "...",
  "permission_mode": "..."
}
```

The hook must READ the transcript file at `transcript_path` to get messages.

## Solution

Added `read_transcript()` function that:
1. Gets `transcript_path` from stdin JSON
2. Opens and parses the JSONL file line by line
3. Skips `file-history-snapshot` entries
4. Returns list of message entries

Key code change:
```python
# Get transcript path from hook input
transcript_path = input_data.get("transcript_path", "")
if not transcript_path:
    log_stderr("No transcript_path in hook input")
    ...

# Read and analyze transcript
messages = read_transcript(transcript_path)
```

## Transcript Entry Format

Each JSONL line in transcript has structure:
```json
{
  "type": "assistant",
  "message": {
    "role": "assistant",
    "content": [
      {"type": "tool_use", "name": "Bash", "input": {...}},
      {"type": "text", "text": "..."}
    ]
  }
}
```

Tool calls are in `message.content` array with `type: "tool_use"`.

## Telegram Integration Added

Also added Telegram notification after each response with work:
```
Delegation: 85% (5 tasks, 1 direct) [web-researcher, pattern-detector]
```

## Files Changed

- `/home/corey/projects/AI-CIV/WEAVER/.claude/hooks/stop_delegation_audit.py` - V3 with transcript reading + Telegram

## Verification

```bash
echo '{"transcript_path": "/path/to/session.jsonl"}' | python3 .claude/hooks/stop_delegation_audit.py
```

Output shows actual tool counts:
```
[delegation-audit] Score: 0.04 (Task: 20, Direct: 431)
```

## Reference

- Claude Code hooks docs: https://docs.claude.com/en/docs/claude-code/hooks
- A-C-Gee package: `from-acgee-delegation-audit-package-20260102.md`

---

**Key Lesson**: Stop hooks receive metadata including `transcript_path`, NOT the messages directly. Must read the transcript file separately.
