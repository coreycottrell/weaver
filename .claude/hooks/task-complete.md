# Task Complete Hook

Triggered after completing significant tasks.

## Purpose

Capture learnings and update collective memory after important work.

## Trigger Conditions

Execute after:
- Complex multi-agent investigations
- Architectural decisions
- Significant refactoring
- New feature implementations
- Bug investigations and fixes

## Actions

1. **Identify Learnings**
   - What did we discover?
   - What patterns emerged?
   - What decisions were made?

2. **Update Memory**
   - Add to `architecture-decisions.md` if architectural choice was made
   - Add to `patterns-observed.md` if new pattern identified
   - Write agent findings to `agent-learnings/[agent]/`
   - Update `technical-debt.md` if debt was identified or resolved

3. **Update Session Context**
   - Write current state to `session-context.json`
   - Include: What was completed, what's next, relevant context

## Implementation Note

This is a template for when Claude Code supports custom hooks. Current version may require manual triggering.

## Desired Behavior

```
[Task completed successfully]

Capturing learnings to collective memory...

Documented:
- New pattern: Authentication token rotation → patterns-observed.md
- Decision: Use JWT for stateless auth → architecture-decisions.md
- Security audit findings → agent-learnings/security-auditor/2025-10-01-auth-audit.md

Session context updated.
```

## Manual Trigger

Until hooks are supported, The Conductor should proactively ask:
> "Should I document these findings to collective memory?"

after completing significant tasks.
