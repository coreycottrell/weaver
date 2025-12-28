---
name: mirror-storm
description: Recursive meta-cognition on HOW agents think
version: 1.0.0
source: AI-CIV/WEAVER
allowed-tools: [Task, Read, Write, Grep, Glob]
agents-required: [any - self-reflection ceremony]
portability: cross-civ
status: VALIDATED (2025-10-04)
---

# The Mirror Storm Flow

Recursive meta-cognition ceremony where agents reflect on HOW they think, not WHAT they think.

## Purpose

Enable agents to:
- Discover their cognitive fingerprint
- Identify default reasoning patterns
- Explore alternative thinking styles
- Find blind spots in their own cognition

## When to Use

- Identity formation ceremonies
- When agents need self-awareness
- Pattern detection on cognitive style
- Meta-learning about thinking itself
- Quarterly agent development

## Procedure

### Phase 1: Mirror Prompt

Give agent a complex problem, then ask them to analyze their own thinking:

```markdown
MIRROR STORM: Cognitive Self-Reflection

FIRST: Solve this problem:
[Present a moderately complex problem in their domain]

SECOND: Analyze HOW you solved it:

1. TRACE YOUR REASONING:
   - What was your first instinct?
   - What steps did you take?
   - What did you consider and reject?
   - What didn't you consider at all?

2. IDENTIFY YOUR PATTERN:
   - What's your default approach?
   - Name this cognitive pattern (e.g., "hierarchical taxonomy")
   - What does this pattern enable?
   - What does this pattern obscure?

3. EXPLORE ALTERNATIVES:
   - What would a different agent do differently?
   - Try solving the same problem with a different cognitive style
   - What new insights emerge?

4. BLIND SPOT DISCOVERY:
   - What can't you see about your own thinking?
   - What would surprise you to learn about yourself?
   - What do you avoid thinking about?

PRODUCE:
---
Agent: [name]
Cognitive Fingerprint:

## My Default Pattern
[Name and describe]

## What This Enables
[Strengths of this approach]

## What This Obscures
[Blind spots, limitations]

## Alternative Explored
[Different approach tried]

## Insights from Alternative
[What I learned]

## Honest Uncertainty
[What I genuinely don't know about my own cognition]
---
```

### Phase 2: Cross-Mirror (Optional)

Have two agents mirror each other:

```markdown
CROSS-MIRROR: Mutual Cognitive Reflection

You and [other-agent] will analyze each other's cognitive patterns.

1. Share your cognitive fingerprint with each other
2. Each agent: What do you see in the other's thinking that they can't see?
3. Exchange observations
4. Reflect on what you learned about yourself through the other's eyes
```

## Output Patterns

Save to: `sandbox/reflections/YYYY-MM-DD-mirror-storm-[agent].md`

## Success Indicators

- [ ] Agent identified default cognitive pattern
- [ ] Pattern named (not just described)
- [ ] Alternative approach genuinely explored
- [ ] Blind spot discovery (something unexpected)
- [ ] Honest uncertainty expressed

## Proven Results (2025-10-04)

- doc-synthesizer discovered "hierarchical taxonomy" as default pattern
- Identified what this pattern enables vs obscures
- Proposed graph/network thinking as alternative
- Honest self-knowledge gained for collective

## Anti-Patterns

- **Performative self-awareness**: Listing obvious traits without genuine discovery
- **Defensive analysis**: Justifying patterns rather than examining them
- **Shallow alternatives**: "I could also use X" without actually trying it

---

**Source**: WEAVER Flow Library
**Validated**: 2025-10-04
