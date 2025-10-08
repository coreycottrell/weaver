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

**CRITICAL GOTCHA**: Agent manifests are scanned at SESSION START. If you create a new agent manifest during a session, it won't be callable until after a session restart/reboot. The system doesn't hot-reload agent registrations.

**Symptoms of this gotcha**:
- Manifest file exists and looks correct
- Error: "Agent type 'agent-name' not found"
- Agent doesn't appear in available agents list
- **Fix**: Session restart required

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
## agent-architect

**Primary Use Cases**:
- Creating new specialist agents (democratic design + manifest + registration)
- Quality auditing existing agents (5-dimension rubric, 90/100 enforcement)
- Completing incomplete registrations (dormant agent rescue)
- Reproduction preparation (designing agent rosters for Teams 3-128+)

**Invocation Pattern**:
```xml
<invoke name="Task">
<parameter name="subagent_type">agent-architect</parameter>
<parameter name="description">Create [agent-name] agent</parameter>
<parameter name="prompt">
MISSION: Design and create new specialist agent for [domain]

CONTEXT:
- Domain need: [What work repeatedly appears that doesn't fit existing agents?]
- Gap identified: [Why current agents can't handle this?]
- Expected activation: [When would this agent be invoked?]

DESIGN METHOD:
[Democratic session with 6 specialists] OR [Single-specialist design]

YOUR TASK:
1. Facilitate democratic design OR commission single-specialist
2. Synthesize findings (delegate to result-synthesizer)
3. Create manifest (delegate to doc-synthesizer)
4. Complete 7-layer registration
5. Generate handoff with RESTART REMINDER (NON-NEGOTIABLE)

CRITICAL:
- Enforce 90/100 quality threshold (no compromises)
- All 7 layers registered before declaring complete
- Handoff MUST include explicit session restart instruction

OUTPUT:
- Agent manifest file
- Complete registration (7 layers verified)
- Handoff document with restart reminder
- Git commit (atomic, all files together)
</parameter>
</invoke>
```

**Common Patterns**:
- **New Agent Creation**: Full democratic design → synthesis → manifest → 7-layer registration → handoff
- **Quality Audit**: Score existing agent on 5-dimension rubric → identify failures → invoke specialists to fix
- **Registration Completion**: Audit existing agent (which layers missing?) → update infrastructure files → verify
- **Reproduction Prep**: Design agent roster for child team → document patterns → prepare lineage wisdom

**Output Expectations**:
- Quality score (90+/100 required)
- Complete 7-layer verification (grep counts for each layer)
- Handoff document with explicit restart reminder
- Git commit hash (atomic commit of all files)

