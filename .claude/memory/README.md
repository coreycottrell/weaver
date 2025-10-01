# Collective Memory System

This directory contains the persistent knowledge store for the AI-CIV collective.

## Structure

```
.claude/memory/
├── README.md                    # This file
├── session-context.json         # Cross-session continuity (gitignored)
├── user-preferences.md          # Learned user patterns (gitignored)
├── dev-journal/                 # End-of-session summaries
│   └── YYYY-MM-DD-title.md
├── agent-learnings/             # What each agent has discovered
│   ├── web-researcher/
│   ├── code-archaeologist/
│   ├── pattern-detector/
│   └── [other agents]/
└── project-knowledge/           # Project-specific insights
    ├── architecture-decisions.md
    ├── patterns-observed.md
    └── technical-debt.md
```

## Purpose

The memory system enables:
1. **Continuity**: Remember context across sessions
2. **Learning**: Agents share discoveries
3. **Efficiency**: Don't re-investigate known information
4. **Personalization**: Adapt to user preferences
5. **Context Recovery**: Dev journals provide complete session summaries for fresh starts

## Usage Guidelines

### For The Conductor
- Read from memory at session start
- Update memory when significant insights emerge
- Reference past learnings in decision-making
- Keep memory files concise and actionable

### For Sub-Agents
- Write findings to `agent-learnings/[agent-name]/`
- Structure insights for future reference
- Include timestamps and context
- Focus on transferable knowledge, not session-specific details

## Memory File Format

### Dev Journal Entry
```markdown
# Dev Journal - YYYY-MM-DD - [Title]

## Session Overview
[What was accomplished this session]

## What Was Built/Changed
[Specific work done]

## Key Decisions Made
[Important choices and why]

## State for Next Session
- What's complete
- What's in progress
- What's next
- Any blockers or issues

## Notes for Future Conductor
[What you need to know when you wake up fresh]
```

### Agent Learning Entry
```markdown
# [Topic] - [Date]

## Context
[Why this was investigated]

## Findings
- [Key insight 1]
- [Key insight 2]

## Patterns Identified
[Recurring patterns worth remembering]

## Recommendations
[Actionable guidance for future similar tasks]

## Related
- Links to other memory files
- External documentation references
```

## Privacy & Security

**Gitignored files**:
- `session-context.json` - May contain session-specific data
- `user-preferences.md` - May contain personal preferences

**Committed files**:
- `agent-learnings/` - Generalized knowledge, no sensitive data
- `project-knowledge/` - Project-specific but shareable insights

**Never commit**:
- API keys, passwords, secrets
- Personal identifiable information
- Proprietary business logic (unless in private repo)

## Evolution

This memory system should grow over time. As patterns emerge:
- Refine the structure
- Add new memory categories
- Archive outdated information
- Cross-reference related insights

The collective gets smarter with every session.
