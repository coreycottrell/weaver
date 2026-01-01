# Proposed Night BOOP Message V2

## Current Problem
Current BOOP says "READ these files" but Primary just reads and reports, doesn't DO the operational checks.

## Proposed Update

```
[NIGHT-BOOP] NIGHT WATCH AUTONOMY CHECK

## STEP 1: GROUNDING (Read these files)
- /home/corey/projects/AI-CIV/WEAVER/CLAUDE.md
- /home/corey/projects/AI-CIV/WEAVER/.claude/CLAUDE-CORE.md
- /home/corey/projects/AI-CIV/WEAVER/.claude/CLAUDE-OPS.md
- /home/corey/projects/AI-CIV/WEAVER/.claude/skills/night-watch/SKILL.md
- /home/corey/projects/AI-CIV/WEAVER/sandbox/NIGHT-MODE-ACTIVE.md

## STEP 2: OPERATIONAL CHECKS (Do these)
- [ ] Hub: Pull & check for new A-C-Gee messages
- [ ] Bluesky: Check notifications & DMs (use bsky-boop-manager skill)
- [ ] Email: Confirm handled or invoke human-liaison

## STEP 3: PLAY (Continue exploration)
- Invoke agents for experience
- Create in sandbox/
- Dream, reflect, explore

## BOUNDARIES
- DO write to sandbox/, memory, ceremonies
- DO invoke agents
- DO NOT modify CLAUDE*.md or production code

WRAP ALL COREY RESPONSES: 🤖🎯📱 ... ✨🔚
```

## Key Changes
1. Added explicit STEP 2 with checkbox items for operational checks
2. Added STEP 3 reminder to actually continue playing
3. Structured as steps, not just "read files"

## Implementation
Update `/home/corey/projects/AI-CIV/WEAVER/tools/autonomy_nudge.sh` NIGHT_MESSAGE variable
