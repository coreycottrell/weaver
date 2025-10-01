# Remember - Add to Collective Memory

Store important information in the collective memory for future sessions.

## Usage

```
/remember <fact or insight>
```

## Description

Adds significant insights, decisions, or patterns to the appropriate memory file:
- User preferences → `.claude/memory/user-preferences.md`
- Architectural decisions → `.claude/memory/project-knowledge/architecture-decisions.md`
- Observed patterns → `.claude/memory/project-knowledge/patterns-observed.md`
- Technical debt → `.claude/memory/project-knowledge/technical-debt.md`

## Examples

```
/remember User prefers detailed explanations for complex topics
```
→ Stored in `user-preferences.md`

```
/remember We decided to use PostgreSQL for relational data and Redis for caching
```
→ Stored in `architecture-decisions.md`

```
/remember Error handling pattern: try-catch at controller level, custom error classes
```
→ Stored in `patterns-observed.md`

## Implementation

The Conductor:
1. Analyzes the information type
2. Selects appropriate memory file
3. Formats the entry with timestamp and context
4. Writes to memory file
5. Confirms what was remembered and where
