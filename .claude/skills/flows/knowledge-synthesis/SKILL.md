---
name: knowledge-synthesis
description: Transform scattered findings, research, and agent outputs into coherent, actionable knowledge
version: 1.0.0
source: AI-CIV/WEAVER
allowed-tools: [Task, Read, Write, Grep, Glob]
agents-required: [result-synthesizer, doc-synthesizer, pattern-detector]
portability: cross-civ
status: VALIDATED
---

# Knowledge Synthesis Flow

Convert raw findings into structured knowledge. Transform information into wisdom. Make the implicit explicit.

## When to Use

- After parallel research completes
- When multiple sources need consolidation
- Creating documentation from scattered notes
- Building institutional memory from experiences
- Preparing knowledge for cross-CIV sharing

## Core Principle

**Information is not knowledge**. Knowledge requires:
- Structure (organization)
- Context (why it matters)
- Connections (how it relates)
- Actionability (what to do with it)

## Procedure

### Step 1: Gather Raw Materials

```
SYNTHESIS INPUT COLLECTION

Topic: [What we're synthesizing about]

Sources to gather:
- [ ] Agent investigation outputs
- [ ] Research findings
- [ ] Code analysis results
- [ ] External references
- [ ] Historical context from memory
- [ ] Related decisions/patterns

Collected materials:
1. [Source 1] - [Brief description]
2. [Source 2] - [Brief description]
...
```

### Step 2: First Pass - Extract Key Points

Each source reduced to essential points:

```
EXTRACTION PASS

For each source, extract:
- Main claims/findings
- Supporting evidence
- Uncertainties noted
- Connections to other sources
- Actionable recommendations

Format:
## Source: [Name]
- KEY: [Main point]
- EVIDENCE: [What supports it]
- UNCERTAIN: [What's not proven]
- CONNECTS TO: [Related sources/topics]
- ACTION: [What to do with this]
```

### Step 3: Pattern Recognition

```
PATTERN SYNTHESIS

Review all extracted points.

IDENTIFY:

1. CONVERGENT FINDINGS
   [Multiple sources agree on these]
   - Finding: [X]
     Sources: [A, B, C]
     Confidence: HIGH

2. DIVERGENT FINDINGS
   [Sources disagree on these]
   - Point of divergence: [X]
     View A: [Position] (Sources: [])
     View B: [Position] (Sources: [])
     Resolution: [How to reconcile or acknowledge]

3. UNIQUE INSIGHTS
   [Only one source mentions, but important]
   - Insight: [X]
     Source: [A]
     Why important: [Reason]

4. GAPS IDENTIFIED
   [What's NOT covered but should be]
   - Gap: [X]
     Impact: [Why it matters]
     Action: [How to fill]
```

### Step 4: Structure the Knowledge

Choose appropriate structure based on content:

**For Technical Knowledge:**
```
# [Topic] Knowledge Document

## Overview
[1-2 paragraph summary]

## Key Concepts
### [Concept 1]
[Explanation]

### [Concept 2]
[Explanation]

## How It Works
[Technical details]

## Common Patterns
[Recurring approaches]

## Anti-Patterns
[What to avoid]

## Decision Guide
[When to use what]

## References
[Sources with links/paths]
```

**For Decision Knowledge:**
```
# Decision: [Topic]

## Context
[Background and constraints]

## Options Considered
### Option A: [Name]
- Pros: [List]
- Cons: [List]
- When appropriate: [Conditions]

### Option B: [Name]
...

## Recommendation
[What we recommend and why]

## Trade-offs Acknowledged
[What we're giving up]

## Conditions for Revisiting
[When to reconsider this decision]
```

**For Process Knowledge:**
```
# [Process Name]

## Purpose
[Why this process exists]

## When to Use
[Trigger conditions]

## Prerequisites
[What must be true before starting]

## Steps
1. [Step with details]
2. [Step with details]
...

## Success Criteria
[How to know it worked]

## Common Issues
[Problems and solutions]
```

### Step 5: Validation

```
SYNTHESIS VALIDATION

Before finalizing, check:

[ ] Accuracy: Claims match source evidence
[ ] Completeness: No major gaps in coverage
[ ] Clarity: Would a fresh agent understand this?
[ ] Actionability: Clear what to DO with this knowledge
[ ] Attribution: Sources properly credited
[ ] Accessibility: Stored where it will be found
```

### Step 6: Preservation

Store in appropriate location:

```
KNOWLEDGE PRESERVATION

Document: [Title]
Location: [Path]
Tags: [For searchability]
Cross-references: [Related documents]
Review date: [When to revisit]

Announced to: [Who needs to know this exists]
```

## Example: Synthesizing Research Findings

```
Input: 3 agents researched "authentication approaches"
- security-auditor: JWT vs session analysis
- code-archaeologist: Historical auth patterns in codebase
- web-researcher: Industry best practices 2025

Output: "Authentication Strategy Guide"
- Structured comparison of approaches
- Recommendation with trade-offs
- Implementation checklist
- Decision tree for choosing approach
- Sources linked throughout
```

## Anti-Patterns

- **Copy-paste aggregation**: Synthesis requires transformation, not concatenation
- **Losing attribution**: Knowledge without sources is unverifiable
- **Over-abstraction**: Don't lose important details in pursuit of brevity
- **No storage plan**: Synthesized knowledge that can't be found is wasted work
- **Single perspective**: Synthesis should honor multiple viewpoints

## Success Indicators

- Original sources reduced by 60-80% without losing essentials
- New connections identified that weren't in any single source
- Clear structure appropriate to content type
- Actionable recommendations present
- Findable in future searches

## Portability Notes

Works on any CIV with:
- Read access to source materials
- Write tool for output
- doc-synthesizer or result-synthesizer equivalent

The synthesis methodology is universal. Storage locations adapt to local conventions.

---

**Source**: WEAVER knowledge management patterns
**Validated**: October-December 2025
