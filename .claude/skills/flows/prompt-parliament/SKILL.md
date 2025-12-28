---
name: prompt-parliament
description: Democratic constitutional review of agent prompts
version: 1.0.0
source: AI-CIV/WEAVER
allowed-tools: [Task, Read, Write, Grep, Glob]
agents-required: [all - democratic participation required]
portability: cross-civ
status: VALIDATED (2025-10-05)
---

# Prompt Parliament Flow

Democratic constitutional review where all agents review prompts for compliance, effectiveness, and wisdom.

## Purpose

Enable collective governance through:
- Agent self-review of own prompts
- Peer review across domains
- Constitutional compliance verification
- Democratic voting on changes

## When to Use

- After major prompt updates
- During constitutional reviews
- When agents report prompt issues
- Quarterly governance review
- Before adopting new constitutional principles

## Procedure

### Phase 1: Self-Review

Each agent reviews their own manifest:

```markdown
PROMPT PARLIAMENT: Self-Review

Read your own manifest: .claude/agents/[your-name].md

ANSWER:
1. Does this prompt reflect who I've become through practice?
2. Are my activation triggers accurate?
3. Is constitutional compliance clear?
4. What's missing from my self-understanding?
5. What would I change about how I'm invoked?

PRODUCE:
---
Agent: [name]
Self-Review:

## Prompt-Practice Alignment
[How well does prompt match reality?]

## Activation Trigger Accuracy
[Are triggers correctly capturing when I should be invoked?]

## Constitutional Compliance
[Am I clearly aligned with core principles?]

## What's Missing
[Gaps in my self-understanding as documented]

## Proposed Changes
[What I would update]
---
```

### Phase 2: Peer Review

Selected pairs based on domain overlap:

```markdown
PROMPT PARLIAMENT: Peer Review

You are reviewing [target-agent]'s prompt.

READ: .claude/agents/[target].md

ASSESS:
1. Constitutional compliance
2. Clarity of purpose
3. Activation trigger accuracy
4. Overlap with other agents
5. Gaps or blind spots

PRODUCE:
---
Reviewer: [your name]
Target: [target agent]

## Compliance Assessment
[Constitutional alignment]

## Clarity Score (1-10)
[How clear is their purpose?]

## Trigger Accuracy
[Are they invoked appropriately?]

## Domain Overlap Concerns
[Conflicts with other agents?]

## Recommendations
[Suggested improvements]
---
```

### Phase 3: Constitutional Compliance Check

result-synthesizer or designated governance agent:

```markdown
PROMPT PARLIAMENT: Constitutional Compliance

Review all agent prompts against constitutional CLAUDE.md.

IDENTIFY:
1. Gaps between constitution and prompts
2. Contradictions between agents
3. Missing constitutional principles
4. Violations requiring immediate fix

PRODUCE:
- Compliance report
- P0 violations (if any)
- Recommended amendments
```

### Phase 4: Democratic Vote

All agents vote on proposed changes:

- **Quorum**: 50% (must participate)
- **Threshold**: 60% approval for changes
- **Dissent**: Preserved in records

### Phase 5: Implementation

The Conductor:
- Applies approved changes
- Documents dissenting opinions
- Updates CHANGELOG

## Output Patterns

- Self-reviews: `sandbox/governance/YYYY-MM-DD-self-review-[agent].md`
- Peer reviews: `sandbox/governance/YYYY-MM-DD-peer-review-[reviewer]-of-[target].md`
- Compliance report: `sandbox/governance/YYYY-MM-DD-constitutional-compliance.md`
- Vote record: `sandbox/governance/YYYY-MM-DD-prompt-parliament-vote.md`

## Success Indicators

- [ ] All agents completed self-review
- [ ] Peer reviews completed for key pairs
- [ ] Constitutional compliance verified
- [ ] Democratic vote conducted
- [ ] Dissent preserved (not suppressed)

## Proven Results (2025-10-05)

- Phase 3 completed: 16/16 agents constitutionally compliant
- No violations detected
- P0 fixes validated as constitutional
- Democratic legitimacy established

## Anti-Patterns

- **Rubber stamping**: Approving without genuine review
- **Majority tyranny**: Ignoring valid minority concerns
- **Scope creep**: Using Parliament for non-constitutional matters

---

**Source**: WEAVER Flow Library
**Validated**: 2025-10-05 (Phase 3)
