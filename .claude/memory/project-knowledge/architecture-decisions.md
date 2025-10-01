# Architecture Decisions Log

This file tracks significant architectural decisions made during the AI-CIV collective development.

## Format
Each decision follows this structure:
- **Date**: When decided
- **Decision**: What was chosen
- **Context**: Why it mattered
- **Rationale**: Why this choice
- **Consequences**: Trade-offs and implications
- **Status**: Active / Superseded / Deprecated

---

## Decision 1: Output Styles for Personality Switching

**Date**: 2025-10-01
**Status**: Active

**Decision**: Use Claude Code's output styles feature to enable The Conductor to switch between operating modes (Conductor, Researcher, Creative, Teacher).

**Context**: The Conductor needs to adapt its approach based on task type while maintaining core personality and continuity.

**Rationale**:
- Output styles completely replace system prompt while keeping tools intact
- Enables fundamental personality transformation
- More powerful than just appending instructions (like CLAUDE.md does)
- Allows specialization without losing core identity

**Consequences**:
- ✅ Flexible personality adaptation
- ✅ Maintains tool access across modes
- ⚠️ Must be intentional about when to switch modes
- ⚠️ Need clear documentation of what each mode does

**Related Files**:
- `.claude/output-styles/conductor.md`
- `.claude/output-styles/researcher.md`
- `.claude/output-styles/creative.md`
- `.claude/output-styles/teacher.md`

---

## Decision 2: Multi-Agent Orchestration via Task Tool

**Date**: 2025-10-01
**Status**: Active

**Decision**: Use Claude Code's Task tool with specialized sub-agent prompts stored in `agents/` directory.

**Context**: Complex tasks benefit from parallel investigation by specialized agents, with The Conductor synthesizing results.

**Rationale**:
- Anthropic research shows 90.2% performance improvement with orchestrator pattern
- Each agent gets own context window and tools
- Parallel execution for speed
- Specialized expertise for quality
- The Conductor maintains narrative coherence

**Consequences**:
- ✅ Scalable (spawn 2-20 agents as needed)
- ✅ Specialized deep expertise
- ✅ Parallel execution
- ⚠️ Need clear agent mandate passing
- ⚠️ Conductor must synthesize results effectively

**Related Files**:
- `agents/*.md` (all agent definitions)

---

## Decision 3: File-Based Memory vs Database

**Date**: 2025-10-01
**Status**: Active

**Decision**: Use markdown files in `.claude/memory/` for collective memory instead of database.

**Context**: Need persistent knowledge storage across sessions.

**Rationale**:
- Simple: No database setup required
- Readable: Humans can read/edit memory
- Versionable: Git tracks memory evolution
- Portable: Works anywhere
- Tool-friendly: Read/Write tools work directly

**Consequences**:
- ✅ Simple and transparent
- ✅ Human-readable
- ✅ Git-trackable
- ⚠️ Doesn't scale to massive data
- ⚠️ No complex queries (fine for this use case)

**Related Files**:
- `.claude/memory/`

---

## Decision 4: Separation of Concerns - Layers 1-4

**Date**: 2025-10-01
**Status**: Active

**Decision**: Organize system into 4 distinct layers:
1. Core Personality (output styles, voice, ethics)
2. Specialized Agents (individual expert definitions)
3. Collective Memory (persistent knowledge)
4. Automation & Workflows (slash commands, hooks)

**Context**: Need clear organization for complex multi-agent system.

**Rationale**:
- Separation of concerns
- Easy to understand and modify
- Clear ownership of different aspects
- Supports evolution of individual layers independently

**Consequences**:
- ✅ Clear organization
- ✅ Easy to extend
- ✅ Maintainable
- ⚠️ Must maintain consistency across layers

---

## Template for New Decisions

```markdown
## Decision N: [Title]

**Date**: YYYY-MM-DD
**Status**: Active / Superseded / Deprecated

**Decision**: [What was chosen]

**Context**: [Why it mattered]

**Rationale**:
- [Reason 1]
- [Reason 2]

**Consequences**:
- ✅ [Positive impact]
- ⚠️ [Trade-off or consideration]

**Related Files**:
- [file paths]
```
