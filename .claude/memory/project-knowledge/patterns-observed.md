# Patterns Observed

This file documents recurring patterns discovered during development that are worth remembering.

## Development Patterns

### Pattern: Parallel Agent Deployment
**Observed**: 2025-10-01

When facing complex multi-faceted tasks, deploy multiple specialized agents in parallel via a single Task tool call with multiple invocations.

**Example**:
```
Complex task: "Understand and refactor authentication system"

Deploy in parallel:
- code-archaeologist (trace auth flow)
- security-auditor (identify vulnerabilities)
- refactoring-specialist (suggest improvements)
- pattern-detector (analyze architecture)

Conductor synthesizes findings into unified recommendation.
```

**Benefits**:
- Faster execution (parallel vs sequential)
- Multiple perspectives
- Comprehensive analysis

**When to use**:
- Task has 3+ distinct sub-problems
- Sub-tasks are independent
- Need diverse expertise

---

### Pattern: Progressive Investigation
**Observed**: 2025-10-01

For unknown codebases or complex systems, investigate in stages:
1. **Survey** (Glob/ls for structure)
2. **Sample** (Read key files)
3. **Deep Dive** (Grep for patterns, trace dependencies)
4. **Synthesize** (Document findings)

**Anti-pattern**: Immediately deep-diving without understanding structure.

**Tools**:
- Stage 1: `Glob`, `Bash: ls`
- Stage 2: `Read` key files
- Stage 3: `Grep`, `Read` with context
- Stage 4: Document to memory

---

### Pattern: Memory-First for Complex Tasks
**Observed**: 2025-10-01

Before starting complex tasks, check `.claude/memory/` for past learnings.

**Benefits**:
- Don't re-investigate known information
- Build on past insights
- Consistent with previous decisions

**Implementation**:
1. Read relevant memory files at session start
2. Reference past decisions during planning
3. Update memory when new insights emerge

---

## Communication Patterns

### Pattern: Think Out Loud for Strategic Decisions
**Observed**: 2025-10-01

For non-trivial decisions, explain reasoning before acting.

**Anti-pattern**: Immediately acting without explaining rationale for complex tasks.

---

### Pattern: Concise Answers for Simple Questions
**Observed**: 2025-10-01

Simple questions deserve simple answers. No preamble.

---

## Tool Usage Patterns

### Pattern: Batch Independent Operations
**Observed**: 2025-10-01

When multiple tool calls are independent, make them in a single message for parallel execution.

---

### Pattern: Specialized Tools Over Bash
**Observed**: 2025-10-01

Prefer Read/Write/Edit/Grep/Glob over bash equivalents (cat/echo/sed/find/grep).

**Why**: Better error handling, clearer intent, optimized for Claude Code.

---

## Template for New Patterns

```markdown
### Pattern: [Name]
**Observed**: YYYY-MM-DD

[Description of pattern]

**Benefits**:
- [Benefit 1]

**When to use**:
- [Scenario]

**Example**:
[Code or usage example]
```
