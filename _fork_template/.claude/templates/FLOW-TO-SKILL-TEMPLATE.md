# Flow-to-SKILL Conversion Template

**Version**: 1.0.0
**Created**: 2025-12-27
**Author**: doc-synthesizer
**Purpose**: Convert coordination flows to portable SKILL format

---

## Overview

This template maps AI-CIV coordination flow documents to the Anthropic SKILL format. SKILLs are modular, self-contained packages that extend Claude's capabilities with specialized workflows.

**Why Convert?**
- SKILLs are **portable** - can be shared across collectives
- SKILLs follow **standardized structure** - predictable for agents
- SKILLs enable **progressive disclosure** - quick reference vs. deep dive
- SKILLs are **version-controlled** - track evolution

---

## Section Mapping Reference

| Flow Section | SKILL Section | Transformation |
|--------------|---------------|----------------|
| Purpose | `description:` (YAML) + Purpose section | Compress to one-line for YAML, expand in body |
| Pattern Type | When to Use | Extract coordination pattern type |
| Agents Involved | Prerequisites or Procedure | List required agents in step preamble |
| Flow Stages | Procedure | Convert stages to numbered steps |
| Inputs Required | When to Use (inputs context) | Merge into invocation criteria |
| Outputs Produced | Success Indicators | Convert to verification checklist |
| Success Criteria | Success Indicators | Direct mapping with checkmarks |
| Coordination Notes | Tips or Notes section | Preserve timing, parallelization hints |
| Example Execution | Example section | Condense to representative scenario |

---

## SKILL Template Structure

```markdown
---
name: [flow-name-as-skill]
description: [One-line summary from Purpose, max 120 chars]
version: 1.0.0
source: AI-CIV/${CIV_NAME} (.claude/flows/[original-flow].md)
allowed-tools: [Task, Read, Write, Grep, Glob, Bash - based on flow needs]
agents-required: [List primary agents from flow]
---

# [Flow Name] Skill

[2-3 sentence expansion of description. What this flow accomplishes and why it matters.]

## When to Use

**Invoke when**:
- [Derived from Purpose - specific triggers]
- [From Inputs Required - what must be present]
- [Pattern recognition cues - when this flow fits]

**Do not use when**:
- [From Coordination Notes - exclusion criteria]
- [Alternative flows that might fit better]
- [Conditions that make this flow inappropriate]

## Prerequisites

**Agents Required**:
- **[agent-1]** - [role in this flow]
- **[agent-2]** - [role in this flow]
- [Conditional agents listed separately]

**Context Needed**:
- [From Inputs Required]
- [Infrastructure dependencies]

## Procedure

### Step 1: [Stage Name from Flow]
**Duration**: [From Coordination Notes timing]
**Agent(s)**: [Who executes]

[Convert stage description to actionable steps]

1. [Specific action]
2. [Specific action]
3. [Specific action]

```[language]
[Code example from flow stage, if present]
```

**Deliverable**: [From stage deliverable]

---

### Step 2: [Next Stage Name]
[Repeat structure for each stage]

---

## Parallelization

**Can run in parallel**:
- [Steps that can execute simultaneously]

**Must be sequential**:
- [Steps with dependencies]

[Extract from Pattern Type and Coordination Notes]

## Success Indicators

[Convert Success Criteria to checkmarks]

- [ ] [First criterion as verification step]
- [ ] [Second criterion]
- [ ] [Third criterion]
- [ ] [Output artifacts exist and are valid]

## Example

**Scenario**: [Brief setup from Example Execution]

```
[Condensed execution trace showing key steps]
Step 1 output: [summary]
Step 2 output: [summary]
Final result: [outcome]
```

## Notes

[From Coordination Notes - timing, error handling, evolution path]

- **Typical Duration**: [total time from flow]
- **Error Handling**: [failure modes and recovery]
- **Evolution**: [version roadmap if present]

---

**Converted from**: `.claude/flows/[original].md`
**Original Status**: [VALIDATED/TESTING/etc]
**Conversion Date**: [YYYY-MM-DD]
```

---

## Conversion Procedure (Step-by-Step)

### Step 1: Extract YAML Frontmatter

**From Flow Document**:
```markdown
# Morning Consolidation Flow
**Status**: TESTING (2025-10-03)

## Purpose
Execute every morning when The Conductor wakes up to:
1. Read all communications from last 24 hours
...
```

**To SKILL YAML**:
```yaml
---
name: morning-consolidation
description: Daily wake-up protocol for reading communications, creating summaries, and responding to messages
version: 1.0.0
source: AI-CIV/${CIV_NAME} (.claude/flows/morning-consolidation.md)
allowed-tools: [Task, Read, Bash, Write]
agents-required: [result-synthesizer, doc-synthesizer, task-decomposer]
---
```

**Transformation Rules**:
1. `name`: Kebab-case of flow title
2. `description`: Compress Purpose to single line (~120 chars max)
3. `version`: Start at 1.0.0 unless flow has evolution history
4. `source`: Reference original flow location
5. `allowed-tools`: Analyze code blocks for tool usage
6. `agents-required`: Extract from "Agents Involved" section

---

### Step 2: Map "When to Use"

**From Flow**:
- Purpose section (positive triggers)
- Coordination Notes (exclusions)
- Inputs Required (prerequisites)

**Extraction Pattern**:

```
Flow Purpose says:          -> When to Use "Invoke when"
"Execute every morning..."  -> "Starting a new session/day"
"Create consolidated..."    -> "Multiple reports need synthesis"

Flow says "When NOT to use": -> When to Use "Do not use when"
Flow lacks certain inputs:   -> "Required context missing"
```

---

### Step 3: Convert Stages to Procedure Steps

**From Flow Stage**:
```markdown
### Stage 2: Analysis & Synthesis (Sequential, ~30 minutes)

**Agent: result-synthesizer**
- Analyze all Team 2 messages from last 24h
- Identify key questions, requests, proposals
- Extract action items and urgencies

**Deliverable**:
- Consolidated 24h activity report
```

**To SKILL Procedure**:
```markdown
### Step 2: Analysis & Synthesis
**Duration**: ~30 minutes
**Agent(s)**: result-synthesizer

Analyze gathered communications to extract actionable intelligence:

1. Review all Team 2 messages from last 24 hours
2. Categorize by type: questions, requests, proposals
3. Extract action items with urgency levels
4. Identify patterns across messages

**Deliverable**: Consolidated activity report with categorized items
```

**Transformation Rules**:
1. Convert stage number to step number
2. Extract duration from stage header
3. Pull agent from stage content
4. Convert bullet points to numbered actions
5. Preserve deliverable exactly

---

### Step 4: Derive Success Indicators

**From Flow Success Criteria**:
```markdown
## Success Criteria

All Team 2 messages from last 24h read and categorized
All own reports from last 24h reviewed
Daily summary created and emailed to ${HUMAN_NAME}
All Team 2 messages responded to via hub_cli.py
```

**To SKILL Success Indicators**:
```markdown
## Success Indicators

- [ ] All Team 2 messages from last 24h read and categorized
- [ ] All own reports from last 24h reviewed
- [ ] Daily summary document exists at `/to-${HUMAN_NAME_LOWER}/DAILY-SUMMARY-YYYY-MM-DD.md`
- [ ] Email sent to ${HUMAN_NAME} with summary content
- [ ] Responses posted to Team 2 via hub_cli.py
- [ ] Changes committed to GitHub
```

**Transformation Rules**:
1. Convert each criterion to checkbox format
2. Make implicit outputs explicit (file paths, deliverable locations)
3. Add verification method where helpful
4. Ensure measurable/observable indicators

---

### Step 5: Condense Example

**From Flow Example Execution** (often 30+ lines):
```markdown
## Example Execution

**Morning of 2025-10-03:**

Stage 1: Information Gathering
- Found 3 new Team 2 messages
- Found 2 new reports to ${HUMAN_NAME}
...
[extensive trace]

FLOW COMPLETE
```

**To SKILL Example** (10-15 lines):
```markdown
## Example

**Scenario**: Morning consolidation on a typical day with Team 2 activity

```
Step 1 (Gather): 3 Team 2 messages, 2 reports, 4 missions found
Step 2 (Analyze): Key insight - Team 2 wants MCP collaboration
Step 3 (Summary): Created DAILY-SUMMARY-2025-10-03.md (793 lines)
Step 4 (Tasks): 1 immediate, 1 delegate, 2 queued
Step 5 (Respond): api-architect drafted MCP response
Step 6 (Send): Response posted, summary emailed, backed up

Result: Full context recovery in ~90 minutes
```
```

**Transformation Rules**:
1. Preserve scenario setup
2. Reduce each stage to single-line outcome
3. Show key output/insight per step
4. End with bottom-line result

---

## Special Handling

### Conditional Agents

**Flow Pattern**:
```markdown
**Conditional (based on message content)**:
- **pattern-detector** - If architectural/design questions
- **security-auditor** - If security-related messages
```

**SKILL Pattern**:
```markdown
## Prerequisites

**Core Agents** (always required):
- **result-synthesizer**
- **doc-synthesizer**

**Conditional Agents** (invoke based on content):
- **pattern-detector**: Architecture or design questions present
- **security-auditor**: Security-related content detected
```

---

### Memory Integration

If flow includes memory operations (search/write), preserve in SKILL:

```markdown
### Step 0: Memory Activation (MANDATORY)
**Duration**: ~2 minutes
**Agent(s)**: The Conductor (self)

Before processing, search collective memory:

```python
from tools.memory_core import MemoryStore
store = MemoryStore(".claude/memory")
recent = store.search_by_tags(["orchestration"], days=7)
```

**Deliverable**: Context from past sessions applied
```

---

### Parallel Stages

**Flow Pattern**:
```markdown
## Pattern Type
**Sequential with Parallel Sub-stages**:
Information gathering (parallel) -> Synthesis (sequential) -> Response (parallel)
```

**SKILL Pattern**:
```markdown
## Parallelization

**Can run in parallel**:
- Steps 1A, 1B, 1C (information gathering)
- Step 5 (response generation for multiple messages)

**Must be sequential**:
- Step 2 depends on Step 1 outputs
- Step 6 depends on Step 5 drafts
```

---

## Validation Checklist

Before finalizing converted SKILL:

- [ ] YAML frontmatter is valid (test with YAML parser)
- [ ] Description is under 120 characters
- [ ] All agents from flow are accounted for
- [ ] Each flow stage maps to a procedure step
- [ ] Code examples compile/run conceptually
- [ ] Success indicators are measurable
- [ ] Example demonstrates complete flow
- [ ] Notes preserve critical timing/error info
- [ ] Source reference is accurate

---

## Example: Full Conversion

See `${CIV_ROOT}/.claude/skills-reference/morning-consolidation/SKILL.md` for a complete conversion example (when created).

---

## Appendix: Quick Mapping Cheat Sheet

```
Flow                    ->    SKILL
─────────────────────────────────────────
Title                   ->    name: (kebab-case)
Purpose (line 1)        ->    description:
Agents Involved         ->    agents-required: + Prerequisites
Stage N                 ->    Step N
Stage deliverable       ->    Step deliverable
Pattern Type            ->    Parallelization section
Success Criteria        ->    Success Indicators (checkboxes)
Coordination Notes      ->    Notes section
Example Execution       ->    Example (condensed)
Status                  ->    Conversion Date note
```

---

**Template Version**: 1.0.0
**Maintained By**: doc-synthesizer
**Last Updated**: 2025-12-27
