#!/usr/bin/env python3
"""
Post-Grounding Confirmation Hook

After spine/grounding skills fire, requires proof of actual reading
by extracting a PERTINENT excerpt from grounding docs.

This prevents "theater reading" where the agent claims to have read
docs without actually processing them.

The task: Pick an excerpt that's relevant to current context.
This forces reading AND contextual thinking.

Created: 2026-01-04
Author: WEAVER Collective
"""

import json
import sys
import os

# Skills that require grounding confirmation
GROUNDING_SKILLS = [
    "weaver-spine",
    "delegation-spine",
    "token-saving-mode",
    "morning-consolidation",
    "session-summary"
]

# Grounding docs to read
GROUNDING_DOCS = [
    "CLAUDE.md",
    ".claude/CLAUDE-CORE.md",
    ".claude/CLAUDE-OPS.md",
    ".claude/scratch-pad.md"
]

def main():
    """
    Check if grounding skill was invoked and require confirmation.

    Returns JSON with:
    - continue: bool - whether to proceed
    - message: str - instruction or confirmation
    """

    # Get tool info from stdin (Claude Code hook protocol)
    try:
        input_data = json.load(sys.stdin)
    except:
        # No input or invalid JSON - pass through
        print(json.dumps({"continue": True}))
        return

    tool_name = input_data.get("tool_name", "")
    tool_input = input_data.get("tool_input", {})

    # Only check Skill invocations
    if tool_name != "Skill":
        print(json.dumps({"continue": True}))
        return

    skill_name = tool_input.get("skill", "")

    # Check if this is a grounding skill
    if skill_name not in GROUNDING_SKILLS:
        print(json.dumps({"continue": True}))
        return

    # This is a grounding skill - require confirmation
    # The hook itself can't enforce the excerpt requirement,
    # but it can inject the reminder into the response

    confirmation_message = f"""
## GROUNDING CONFIRMATION REQUIRED

You invoked `{skill_name}`. Before proceeding:

**TASK**: Pick ONE excerpt from the grounding docs that is PERTINENT to your current context/task.

Docs to scan:
- CLAUDE.md
- .claude/CLAUDE-CORE.md
- .claude/CLAUDE-OPS.md
- .claude/scratch-pad.md

Format your response:
```
PERTINENT EXCERPT:
"[Quote from doc]"
— [Source file]

WHY PERTINENT:
[1-2 sentences on relevance to current context]
```

This proves actual reading. Proceed with task after providing excerpt.
"""

    # Return continue=True but with the confirmation message injected
    # The message will appear in Claude's context
    result = {
        "continue": True,
        "message": confirmation_message.strip()
    }

    print(json.dumps(result))


if __name__ == "__main__":
    main()
