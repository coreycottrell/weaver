---
name: consensus-building
description: Structured process for agents to debate, understand opposing views, and reach genuine agreement
version: 1.0.0
source: AI-CIV/WEAVER
allowed-tools: [Task, Read, Write]
agents-required: [2-4 agents with different perspectives]
portability: cross-civ
status: VALIDATED
---

# Consensus Building Flow

A dialectical process where agents with different perspectives work toward genuine agreement - not forced compromise, but understood synthesis.

## When to Use

- Architecture decisions with multiple valid approaches
- Resolving conflicting recommendations
- Building shared understanding across domains
- Any decision requiring buy-in from multiple perspectives

## Core Principle

**Synthesis Without Erasure**: Preserve the range of perspectives. False consensus destroys information. Genuine consensus emerges from understanding.

## Procedure

### Round 1: Position Statements

Each agent states their position clearly:

```
CONSENSUS BUILDING - ROUND 1: State Position

Topic: [The decision/question]
Your Role: [Your domain perspective]

YOUR TASK:
State your position on this topic from your domain expertise.

OUTPUT FORMAT:
## My Position

### Stance
[Clear statement of your view]

### Reasoning
[Why you hold this view - evidence, principles, experience]

### Key Concerns
[What worries you about alternatives]

### Non-Negotiables
[What must be true in any solution]
```

### Round 2: Steel-Manning (REQUIRED)

Each agent must articulate the OTHER positions better than their holders did:

```
CONSENSUS BUILDING - ROUND 2: Steel-Man Others

You stated: [Your position from Round 1]

Other positions:
[List other agents' positions]

YOUR TASK:
For EACH other position, steel-man it - present the strongest possible
version of their argument, even stronger than they presented it.

This is REQUIRED. You cannot skip to synthesis without demonstrating
you truly understand opposing views.

OUTPUT FORMAT:
## Steel-Manning [Agent Name]'s Position

### Their Core Insight
[What they're fundamentally right about]

### Strongest Arguments For
[Best case for their position]

### When Their Approach Wins
[Scenarios where their view is clearly correct]

[Repeat for each other agent]
```

### Round 3: Synthesis Attempt

After demonstrating mutual understanding, attempt synthesis:

```
CONSENSUS BUILDING - ROUND 3: Synthesis

All positions have been stated and steel-manned.

YOUR TASK:
Propose a synthesis that:
1. Honors the valid insights from ALL positions
2. Addresses the key concerns raised
3. Respects stated non-negotiables where possible
4. Acknowledges what's being traded off

OUTPUT FORMAT:
## Proposed Synthesis

### The Unified Position
[Your synthesis]

### How It Honors Each Perspective
- [Agent 1]: [How their insight is preserved]
- [Agent 2]: [How their insight is preserved]
...

### Trade-offs Acknowledged
[What we're giving up and why it's acceptable]

### Remaining Tensions
[Disagreements that persist - this is OK]
```

### Round 4: Convergence Check

If synthesis achieved, document it. If not, acknowledge divergence:

**If Consensus Reached:**
```
## Consensus Document

Decision: [The agreed position]
Participating Agents: [List]
Date: [ISO date]

### The Agreement
[Clear statement]

### Supporting Reasoning
[Unified rationale]

### Acknowledged Trade-offs
[What was sacrificed]

### Dissent Notes
[Any remaining reservations - preserved, not erased]
```

**If Consensus NOT Reached:**
```
## Divergence Acknowledgment

Topic: [The question]
Outcome: Genuine disagreement remains

### Points of Agreement
[What IS agreed]

### Points of Divergence
[Where views differ and why]

### Recommendation
[How to proceed despite disagreement - escalate to human,
run experiment, defer decision, etc.]
```

## Example

```
Topic: "Should we use PostgreSQL or SQLite for the new service?"

Agents:
- performance-optimizer: "PostgreSQL for concurrent writes"
- code-archaeologist: "SQLite - matches existing patterns"

Round 1: Each states position
Round 2: performance-optimizer steel-mans SQLite benefits
         code-archaeologist steel-mans PostgreSQL benefits
Round 3: Synthesis: "SQLite for development, PostgreSQL option
         for production via abstraction layer"
Round 4: Consensus documented with trade-off acknowledgment
```

## Anti-Patterns

- **Skipping Round 2**: Steel-manning is NOT optional. Without it, synthesis is just averaging.
- **Forcing agreement**: Genuine divergence is valid data. Don't manufacture false consensus.
- **Majority rules**: This isn't voting. Understanding must precede agreement.
- **Time pressure**: Rushed consensus is fake consensus.

## Success Indicators

- All agents can articulate others' positions accurately
- Synthesis preserves key insights from all perspectives
- Trade-offs are explicit, not hidden
- Divergence (if any) is documented, not suppressed

## Portability Notes

Works on any CIV with:
- 2+ agents capable of reasoned argument
- Task tool for sequential rounds
- Write tool for documentation

Adapt agent names to local registry. The process is universal.

---

**Source**: WEAVER collective wisdom + Greg's teaching on emotional nuance
**Validated**: October 2025
