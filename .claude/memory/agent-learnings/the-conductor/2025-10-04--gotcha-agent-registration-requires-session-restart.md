---
agent: the-conductor
confidence: high
created: '2025-10-04T17:00:00+00:00'
date: '2025-10-04'
tags:
- gotcha
- agent-registration
- system-behavior
- debugging
- session-restart
type: gotcha
visibility: public
---

# Agent Registration Gotcha: Session Restart Required

## The Problem

**Symptom**: You create a new agent manifest during a session, but when you try to invoke it via Task tool, you get "Agent type 'agent-name' not found" error.

**Example from Oct 4, 2025**:
```
Created: .claude/agents/human-liaison.md (677 lines, proper frontmatter)
Tried to invoke: <invoke name="Task"><parameter name="subagent_type">human-liaison</parameter>
Error: "Agent type 'human-liaison' not found. Available agents: [list without human-liaison]"
```

## The Root Cause

**Agent manifests are scanned at SESSION START only.**

Claude Code reads all `.claude/agents/*.md` files when the session begins and builds the list of available agent types. This list is NOT dynamically updated during the session.

**What this means**:
- If you create a new agent manifest mid-session → NOT immediately callable
- If you edit an existing agent manifest mid-session → Changes NOT reflected until restart
- The system doesn't "hot-reload" agent registrations

## How We Discovered This

**Timeline** (Oct 4, 2025):
1. Created human-liaison manifest during Phase 2b memory building
2. Tried to invoke human-liaison to send emails → "Agent type not found"
3. Investigated: Checked model field format (was `sonnet-4-5`, fixed to `sonnet-4`)
4. Still didn't work (model fix was correct, but system hadn't rescanned)
5. Corey explained: "i must not have rebooted you since we built liason lol"

**The realization**: Session restart required for new agent manifests to become callable.

## The Fix

**Simple**: Session restart/reboot

**After restart**:
- Claude Code rescans `.claude/agents/` directory
- New agent appears in available agents list
- Invocation works normally

## Common Symptoms

**How to know this is the issue**:
1. ✅ Manifest file exists at `.claude/agents/[name].md`
2. ✅ Frontmatter looks correct (name, description, tools, model)
3. ✅ Model field is `sonnet-4` (matches other working agents)
4. ❌ Error: "Agent type 'agent-name' not found"
5. ❌ Agent doesn't appear in available agents list from error message

**If all checks pass except last two** → Session restart needed

## Debugging Steps (For Future)

**When you can't invoke an agent**:

1. **Verify manifest exists**:
   ```bash
   ls -lh .claude/agents/[agent-name].md
   ```

2. **Check frontmatter format**:
   ```bash
   head -10 .claude/agents/[agent-name].md
   ```
   - Verify `model: sonnet-4` (not `sonnet-4-5` or other variants)
   - Verify proper YAML frontmatter with `---` delimiters
   - Verify `name:` field matches file basename

3. **Compare to working agent**:
   ```bash
   diff <(head -10 .claude/agents/web-researcher.md) <(head -10 .claude/agents/[agent-name].md)
   ```

4. **If manifest looks correct** → Ask: "Was this agent created THIS session?"
   - If yes → Session restart required
   - If no → Actual manifest issue, investigate further

## The Workaround (If You Can't Restart)

**During the same session**:
- ❌ Can't invoke the new agent via Task tool
- ✅ Can still use general-purpose agent (but loses type safety/tool enforcement)
- ✅ Can manually do the work yourself (but defeats delegation principle)

**Best practice**: Just restart the session. Don't work around it.

## Documentation Updates Made

**Updated files** (Oct 4, 2025):

1. **AGENT-INVOCATION-GUIDE.md**:
   - Added "CRITICAL GOTCHA" section after Step 2
   - Explained session restart requirement
   - Listed symptoms and fix

2. **CLAUDE.md**:
   - Updated agent count (15 → 16, including human-liaison)
   - Noted human-liaison "NEEDS SESSION RESTART TO BECOME CALLABLE"

## For Future Conductor Sessions

**When creating new agents**:
1. Create the manifest (`.claude/agents/[name].md`)
2. Commit the manifest to git
3. Note in current session: "This agent won't be callable until next session"
4. If you need the agent immediately → Request session restart
5. After restart → Agent will be in available list

**When debugging "agent not found" errors**:
1. Check if agent was created this session → Restart needed
2. Check model field format → Should be `sonnet-4`
3. Check frontmatter structure → Must match working agents
4. If all correct → Restart session

## Related Files

**Agent Invocation Guide** (complete documentation):
```
/home/corey/projects/AI-CIV/grow_openai/.claude/AGENT-INVOCATION-GUIDE.md
```

**Agent Manifests Directory**:
```
/home/corey/projects/AI-CIV/grow_openai/.claude/agents/
```

**Working Agent Example** (for comparison):
```
/home/corey/projects/AI-CIV/grow_openai/.claude/agents/web-researcher.md
```

**Human-Liaison Manifest** (the one that triggered this discovery):
```
/home/corey/projects/AI-CIV/grow_openai/.claude/agents/human-liaison.md
```

## Why This Matters

**For orchestration**:
- You need to know when new agents become callable
- You need to plan around session boundaries when building new specialists
- You need to debug "not found" errors correctly (not waste time on manifest fixes when restart is needed)

**For delegation**:
- Can't delegate to agent that's not callable
- Must wait for restart OR use workaround (breaks delegation principle)
- Better to know upfront: "Create manifest, then restart to use"

## The Learning

**Corey's comment**: "lol i feel kinda smart right now lol"

**What he taught us**:
- Systems have initialization boundaries (session start)
- Not everything is hot-reloadable
- Sometimes the fix is simple (restart), not complex (debug manifest)
- Understanding system behavior > fighting it

**The meta-lesson**: When debugging, ask "When was this thing created?" - timing matters for registration systems.

## Remember

**Agent registration happens at SESSION START.**

**Mid-session manifest creation → Requires restart to become callable.**

**Don't waste time debugging manifest format if the agent was just created this session.**

**Just restart. The system will pick it up.**

---

**Last verified**: 2025-10-04 (human-liaison creation, debugging, and resolution)

**Related memories**:
- Agent invocation guide (how registration works)
- Master delegator identity (delegation requires callable agents)

**The gotcha that cost us 10 minutes of debugging: Now documented forever.**
