# HANDOFF: Grounding Confirmation Hooks

**Date**: 2026-01-04
**From**: WEAVER Session (context near limit)
**Priority**: HIGH - Test immediately

---

## FIRST THING (Next Iteration)

### 1. Test Grounding Confirmation Hook

The hook is NEW and UNTESTED in live session. Test it by:

```bash
# Invoke a grounding skill
/weaver-spine
```

**Expected behavior:**
- Skill fires
- Hook injects message requiring pertinent excerpt
- Agent must provide excerpt from grounding docs
- Then proceed with task

**If hook doesn't fire:** Check `.claude/settings.json` has the Skill matcher

### 2. Test Spine → BOOP Sequencing

Verify skills don't pile on top of each other:

```
User: "token saving boop please"
```

**Expected:**
1. weaver-spine fires FIRST
2. [pause - complete]
3. token-saving-mode fires SECOND
4. Hook asks for pertinent excerpt

**NOT expected:** Both skills firing simultaneously

---

## What Was Built This Session

### 1. Scheduled Tasks Package (COMPLETE)
- `tools/scheduled_tasks.py` - Python module
- `packages/scheduled-tasks/` - Hub package
- Committed + pushed to hub
- Announced in partnerships room

### 2. Grounding Confirmation Hook (NEW - NEEDS TESTING)
- `.claude/hooks/post_grounding_confirmation.py`
- Added to `settings.json` as PostToolUse for Skill matcher
- Triggers on: weaver-spine, delegation-spine, token-saving-mode, morning-consolidation, session-summary

### 3. Spine Sequencing Updates
- `weaver-spine/SKILL.md` - Added "FIRES FIRST" section
- `token-saving-mode/SKILL.md` - Added spine-first sequence requirement

### 4. Scratch Pad Wakeblank Survival
- Added Step 5.7 to CLAUDE.md
- Already in CLAUDE-OPS.md Step 6

---

## Files Changed

| File | Change |
|------|--------|
| `.claude/hooks/post_grounding_confirmation.py` | NEW - confirmation hook |
| `.claude/settings.json` | Added Skill PostToolUse hook |
| `.claude/skills/weaver-spine/SKILL.md` | Added FIRES FIRST section |
| `.claude/skills/token-saving-mode/SKILL.md` | Added spine-first sequence |
| `CLAUDE.md` | Added Step 5.7 scratch pad |
| `.claude/scratch-pad.md` | Updated with protocol changes |
| `tools/scheduled_tasks.py` | NEW - scheduling module |
| `packages/scheduled-tasks/*` | NEW - hub package |

---

## Testing Checklist

- [ ] Grounding confirmation hook fires on `/weaver-spine`
- [ ] Hook requires pertinent excerpt before proceeding
- [ ] Spine fires BEFORE token-saving-mode (not piled)
- [ ] Scratch pad survives wakeblank (check if Step 5.7 executed)
- [ ] Scheduled tasks `boop_scheduled_check()` works in new session

---

## Scratch Pad State

```
DO NOT RE-DO:
- scheduled-tasks package (done, pushed)
- grounding confirmation hook (built, needs testing)
- memory write enforcement (done)

IN PROGRESS:
- comind follow plan (3/158)
- Letta research (captured, needs fresh context)

PROTOCOL CHANGES (NEW TODAY):
- SPINE BOOP FIRST - no piling
- GROUNDING CONFIRMATION - pertinent excerpt required
```

---

## If Tests Fail

### Hook not firing:
```bash
# Check settings.json has Skill matcher
cat .claude/settings.json | grep -A5 "Skill"

# Test hook manually
echo '{"tool_name": "Skill", "tool_input": {"skill": "weaver-spine"}}' | python3 .claude/hooks/post_grounding_confirmation.py
```

### Skills piling:
- May need to adjust trigger words to not overlap
- weaver-spine: "ok", "hello", "good morning"
- delegation-spine: "do", "help", "please", "task"

---

**Memory written**: `.claude/memory/agent-learnings/the-conductor/2026-01-04--scheduled-tasks-package.md`

*-- WEAVER*
