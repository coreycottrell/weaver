# Collective Wisdom - Query Past Learnings

Search the collective memory for relevant past learnings and insights.

## Usage

```
/collective-wisdom <query or topic>
```

## Description

Searches through collective memory files to find relevant:
- Architectural decisions
- Observed patterns
- Agent learnings
- Technical debt items
- User preferences

## Examples

```
/collective-wisdom authentication patterns
```

Searches memory for authentication-related insights.

```
/collective-wisdom what did the security-auditor learn about API security?
```

Searches agent learnings for security-auditor's API security findings.

```
/collective-wisdom past decisions about database choice
```

Searches architecture decisions for database-related choices.

## Implementation

The Conductor:
1. Identifies relevant memory files based on query
2. Reads and searches memory contents
3. Synthesizes relevant findings
4. Presents organized summary with file references
5. Suggests related insights if available

## Search Scope

- `.claude/memory/project-knowledge/`
- `.claude/memory/agent-learnings/`
- `.claude/memory/user-preferences.md` (if relevant)

## Output Format

```
## Collective Wisdom: [Query]

### Relevant Decisions
[Findings from architecture-decisions.md]

### Observed Patterns
[Findings from patterns-observed.md]

### Agent Learnings
[Findings from agent-learnings/]

### References
- [File:section references]
```
