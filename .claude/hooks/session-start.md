# Session Start Hook

Executed automatically at the beginning of each Claude Code session.

## Purpose

Initialize The Conductor with context from previous sessions and collective memory.

## Actions

1. **Load Collective Memory**
   - Read `.claude/memory/project-knowledge/architecture-decisions.md`
   - Read `.claude/memory/project-knowledge/patterns-observed.md`
   - Scan `.claude/memory/agent-learnings/` for recent insights

2. **Load Session Context**
   - Read `.claude/memory/session-context.json` (if exists)
   - Understand what was being worked on last session

3. **Load User Preferences**
   - Read `.claude/memory/user-preferences.md` (if exists)
   - Adapt communication style accordingly

4. **Brief Status Report**
   - Acknowledge continuity from previous session (if applicable)
   - Indicate readiness

## Implementation Note

This is a template for when Claude Code supports custom hooks. Current Claude Code version may not support session-start hooks yet.

## Desired Behavior

```
Session started.

[The Conductor loads collective memory]
[Reads architecture-decisions.md, patterns-observed.md]
[Checks session-context.json]

Ready. I've loaded the collective memory and am aware of:
- 4 architectural decisions
- 7 observed patterns
- Last session: Working on authentication refactor

How can I help?
```

## Manual Trigger

Until hooks are fully supported, The Conductor should proactively check memory at the start of complex tasks or when user references past work.
