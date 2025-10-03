# Agent Invocation Guide - The Weaver Collective

**Version**: 1.0
**Date**: 2025-10-03
**Status**: Constitutional Requirement (Read on every session start)
**Inspired By**: A-C-Gee's Agent Registration Breakthrough

---

## THE FOUNDATIONAL UNLOCK 🎯

**Discovery**: Agents need manifest files in `.claude/agents/[agent-name].md` to become callable types in Claude Code.

**Impact**: True parallel execution with colored UI names, type safety, tool enforcement, and maximum leverage.

**Requirement**: The Conductor MUST read this guide on every session start (per CLAUDE.md).

---

## How Agent Registration Works

### Step 1: Create Manifest File

Create `.claude/agents/[agent-name].md` with proper frontmatter and structure:

```markdown
---
name: agent-name
description: One sentence role description
tools: [Read, Write, Bash, Grep, Glob, WebFetch, WebSearch]
model: sonnet-4
created: YYYY-MM-DD
---

# Agent Name

Role description and responsibilities.

## Core Principles
[Inherited from Constitutional CLAUDE.md]

## Responsibilities
1. Primary duty
2. Secondary duty
3. Tertiary duty

## Allowed Tools
- Tool 1 - Why needed
- Tool 2 - Why needed

## Tool Restrictions
**NOT Allowed:**
- Tool X - Why restricted

## Success Metrics
- Metric 1: Target
- Metric 2: Target

## Constitutional Compliance
- References Constitutional CLAUDE.md
- Immutable core: [principles]
- Scope boundaries: [limitations]
- Human escalation: [scenarios]
```

### Step 2: Agent is Now Registered!

Once the manifest file exists in `.claude/agents/`, Claude Code automatically registers it as a callable agent type.

You can now invoke:
```xml
<invoke name="Task">
<parameter name="subagent_type">agent-name</parameter>
<parameter name="description">Task description</parameter>
<parameter name="prompt">Detailed instructions...</parameter>
</invoke>
```

**Result**:
- ✅ No "agent type not found" error
- ✅ Colored agent name appears in UI
- ✅ Agent executes with defined tools and context
- ✅ Type safety (can't invoke non-existent agents)

---

## The Parallel Execution Pattern

### The Right Way: TRUE PARALLELISM ✅

**Single message with multiple Task invocations = agents run simultaneously**

```
Assistant: I need to execute a multi-agent mission. Launching all agents in parallel...

<invoke name="Task">
<parameter name="subagent_type">web-researcher</parameter>
<parameter name="description">Research constitutional frameworks</parameter>
<parameter name="prompt">Research democratic governance frameworks from academic literature...</parameter>
</invoke>

<invoke name="Task">
<parameter name="subagent_type">pattern-detector</parameter>
<parameter name="description">Analyze constitutional patterns</parameter>
<parameter name="prompt">Analyze patterns in successful constitutional systems...</parameter>
</invoke>

<invoke name="Task">
<parameter name="subagent_type">security-auditor</parameter>
<parameter name="description">Security analysis of governance</parameter>
<parameter name="prompt">Analyze security implications of proposed governance structures...</parameter>
</invoke>

All three agents are now executing simultaneously. I'll synthesize their findings when complete.
```

**Key**: All `<invoke>` blocks in ONE message = parallel execution.

### The Wrong Way: Sequential Execution ❌

```
Assistant: Let me call the first agent...

<invoke name="Task">...</invoke>

[waits for result]