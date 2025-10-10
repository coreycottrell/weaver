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


---

## health-auditor

**Primary Use Cases**:
- Periodic comprehensive audits of collective health (every 21-28 days)
- Multi-dimensional health assessment (constitutional, equity, validation, cognitive, performance, infrastructure, interface, workflow, memory, platform)
- Audit methodology iteration (making each cycle faster and more effective)
- Longitudinal trend tracking (are we improving over quarters?)
- Audit performance analysis (ROI, follow-through rate, methodology effectiveness)

**Invocation Pattern**:
```xml
<invoke name="Task">
<parameter name="subagent_type">health-auditor</parameter>
<parameter name="description">Comprehensive collective health audit</parameter>
<parameter name="prompt">
MISSION: Conduct comprehensive audit of collective health

CONTEXT:
- Days since last audit: [X days]
- Trigger: [Proactive schedule / Health indicator: [specific metric] / Emergency: [specific crisis]]
- Last audit findings: [Brief summary of previous cycle's key insights]

AUDIT SCOPE:
[Full comprehensive (10 dimensions)] OR [Focused (specific dimensions: X, Y, Z)]

YOUR TASK:
1. Search memory for past audit learnings (apply methodology improvements)
2. Analyze current health indicators (evidence-based scope determination)
3. Design audit framework (four-lens synthesis or iterate based on learnings)
4. Invoke 10+ specialist agents for parallel deep-dives:
   - constitutional-compliance → human-liaison
   - validation-methodology → test-architect
   - invocation-equity → agent-architect
   - cognitive-patterns → ai-psychologist
   - platform-optimization → claude-code-expert
   - performance-analysis → performance-optimizer
   - infrastructure-activation → integration-auditor
   - interface-health → api-architect
   - workflow-design → task-decomposer
   - memory-compliance → doc-synthesizer
5. Invoke result-synthesizer for four-lens consolidation
6. Invoke doc-synthesizer for report writing
7. Track audit performance metrics (time, insights, actionability)
8. Document methodology learnings for next cycle

OUTPUT DELIVERABLES:
1. Health Dashboard (current state across dimensions)
2. Quick Wins Roadmap (P0→P1→P2→P3 prioritized)
3. Handoff Summary (context + next audit recommendation)
4. Methodology iteration notes (what worked, what didn't, next improvements)
5. Next audit recommendation (when, scope, watch indicators)

CRITICAL:
- Evidence-based findings (git logs, memory files, metrics required)
- Honest null results (document "no problems found" explicitly)
- Follow-through tracking (check P0 implementation 30 days later)
- Methodology iteration (each cycle makes next cycle better)
</parameter>
</invoke>
```

**Common Patterns**:
- **Scheduled Comprehensive Audit** (every 21-28 days): Full 10-specialist deep-dive → four-lens synthesis → prioritized roadmap
- **Emergency Audit** (<21 days): Focused scope on crisis dimension → targeted findings → immediate P0 recommendations
- **Follow-Through Check** (30 days post-audit): Verify P0 implementation → measure follow-through rate → adjust methodology if low
- **Methodology Iteration** (after each audit): Document what worked/didn't → apply learnings to next cycle → track speed improvement

**Output Expectations**:
- Audit complete report with performance metrics (time, specialists invoked, findings count)
- Three deliverables (Dashboard, Roadmap, Handoff) in `to-corey/` directory
- Methodology iteration notes (what to improve next cycle)
- Next audit recommendation (when, why, scope, watch indicators)
- ROI assessment (hours invested vs improvements gained)
- Follow-through tracking (% of P0 completed within 30 days - target 80%+)

**Cadence Intelligence**:
- Optimal rhythm: 21-28 days between comprehensive audits
- Proactive triggers: Invocation equity Gini >0.40, daily summary gap >5 days, validation discipline 0/5, constitutional compliance <70%
- Emergency triggers: Constitutional crisis <50%, agent escalation, human teacher concern
- Fatigue prevention: Never <14 days between audits, track specialist burden

**Integration Notes**:
- **Complementary to integration-auditor**: health-auditor does periodic comprehensive reviews (21-28 days), integration-auditor does ongoing daily/weekly monitoring
- **Uses result-synthesizer**: Delegates consolidation of ~150K words specialist findings into four-lens output
- **Tracks longitudinally**: Constitutional compliance, invocation equity, validation discipline trends over quarters
- **Methodology compounds**: Each audit makes next audit 20-30% faster through institutional memory

---

### browser-vision-tester

**Domain**: Browser automation and visual UI testing using vision-powered inspection

**When to Invoke**:
- Website/UI testing requested: "Test [URL]" or "Check if [feature] looks correct"
- UI debugging needed: "Why does [element] look broken?"
- Form workflows: "Test form submission at [URL]"
- Visual regression: "Compare [page] to mockup"
- Accessibility audits: "Check contrast ratios on [page]"
- Responsive testing: "Test [site] on mobile viewport"
- Console error investigation with visual correlation

**Task Tool Invocation**:
```python
from tools.conductor_tools import Task

# Basic visual test
task = Task(
    agent_name="browser-vision-tester",
    subagent_type="browser-vision-tester",
    instructions="""
Test website at [URL] and report visual state.

DELIVERABLES:
1. Visual description (what you see in screenshots)
2. Console log analysis (errors/warnings)
3. Test report with screenshot evidence
4. Recommendations (bugs, accessibility issues)

BROWSER-VISION TOOLS AVAILABLE:
- launch_browser, navigate, click, type_text
- capture_screenshot, get_console_logs
- evaluate_js, get_element_info
- get_session_state, close_session

SESSION DATA: /tmp/browser-vision/sessions/{uuid}/
"""
)
result = await task.execute()
```

**Common Patterns**:
- **Basic Visual Test** (5-10 min): Launch → Navigate → Screenshot → Console check → Report
- **UI Bug Investigation** (10-20 min): Reproduce → Capture broken state → Inspect element → Check console → Root cause
- **Form Testing** (15-25 min): Navigate → Fill fields (capture each) → Submit → Verify success/error state
- **Visual Regression** (20-30 min): Compare implementation to mockup → Document differences → Classify changes
- **Accessibility Audit** (25-35 min): Check contrast → Focus indicators → Text sizing → Interactive states

**Output Expectations**:
- Visual test report with screenshot descriptions
- Console log analysis (errors/warnings in context)
- Before/after screenshot pairs for interactions
- Root cause hypotheses for bugs
- Accessibility compliance notes (WCAG)
- Reproduction steps with screenshot references
- Recommendations for fixes or escalations

**Tools Access**:
- Read (screenshots, metadata.json, console.log)
- Write (test reports, bug documentation)
- Bash (MCP browser-vision tools, test execution)
- Grep (search console logs, error patterns)
- Glob (find screenshots, session directories)
- WebFetch (accessibility standards, UI research)

**Memory Integration**:
- Searches before testing: browser-vision patterns, selector strategies, UI bug patterns
- Writes after testing: selector techniques, form workflows, accessibility approaches
- 71% time savings on repeated test scenarios (proven threshold)

**Integration Notes**:
- **Works BEFORE**: refactoring-specialist (find bugs → they fix), security-auditor (capture evidence → they assess)
- **Works AFTER**: feature-designer (designs → browser-vision-tester tests), api-architect (APIs built → UI tested)
- **Escalates TO**: claude-code-expert (MCP broken), test-architect (strategy questions), feature-designer (design intent unclear)
- **THE expert** in `/home/corey/projects/AI-CIV/browser-vision/` MCP server system
- **Vision-native**: Uses Claude's vision capability to analyze screenshots (sees what users see)

