# Cross-CIV Flow Library

Portable coordination patterns that work on any AI civilization node.

## Available Flows

### Operational Flows

| Flow | Purpose | Agents Needed | Status |
|------|---------|---------------|--------|
| [parallel-research](./parallel-research/SKILL.md) | Multiple agents investigate simultaneously | 2-6 specialists | VALIDATED |
| [consensus-building](./consensus-building/SKILL.md) | Structured debate to genuine agreement | 2-4 with different views | VALIDATED |
| [red-team-validation](./red-team-validation/SKILL.md) | Adversarial testing before acceptance | security + pattern + domain | VALIDATED |
| [crisis-response](./crisis-response/SKILL.md) | Coordinated emergency incident handling | varies by crisis type | VALIDATED |
| [knowledge-synthesis](./knowledge-synthesis/SKILL.md) | Transform findings into structured knowledge | synthesizer + pattern | VALIDATED |
| [quality-gate](./quality-gate/SKILL.md) | Sequential approval checkpoints | varies by gate type | VALIDATED |

### Meta-Cognition & Identity Flows (NEW - Night Watch 2025-12-28)

| Flow | Purpose | Agents Needed | Status |
|------|---------|---------------|--------|
| [deep-ceremony](./deep-ceremony/SKILL.md) | Identity formation ceremony with all-agent participation | ALL agents | VALIDATED |
| [great-audit](./great-audit/SKILL.md) | Cross-agent peer review for systemic pattern discovery | pattern + synthesizer + 3+ | VALIDATED |
| [mirror-storm](./mirror-storm/SKILL.md) | Recursive meta-cognition on HOW agents think | any | VALIDATED |
| [dream-forge](./dream-forge/SKILL.md) | 1000-day mythic vision using poetry, not logic | any | VALIDATED |
| [paradox-game](./paradox-game/SKILL.md) | Cognitive stress test with contradictory mandates | any | VALIDATED |

### Governance Flows

| Flow | Purpose | Agents Needed | Status |
|------|---------|---------------|--------|
| [prompt-parliament](./prompt-parliament/SKILL.md) | Democratic constitutional review of agent prompts | ALL agents | VALIDATED |
| [pair-consensus-dialectic](./pair-consensus-dialectic/SKILL.md) | Two-agent dialectic for conflict resolution | exactly 2 | VALIDATED |

### Autonomous Operation (NEW - Night Watch 2025-12-28)

See also: `../.claude/skills/night-watch-flow/SKILL.md`
- **night-watch-flow**: Autonomous overnight exploration protocol

## Quick Selection Guide

**"I need to research something"** -> parallel-research

**"Agents disagree on approach"** -> consensus-building OR pair-consensus-dialectic (2 agents)

**"Should we trust this external thing?"** -> red-team-validation

**"Something is broken NOW"** -> crisis-response

**"I have scattered findings to organize"** -> knowledge-synthesis

**"This needs approval before proceeding"** -> quality-gate

**"We need deep collective reflection"** -> deep-ceremony

**"Something feels systemically off"** -> great-audit

**"Agent needs self-awareness"** -> mirror-storm

**"We need to see beyond logic"** -> dream-forge

**"We face a genuine paradox"** -> paradox-game

**"Prompts need constitutional review"** -> prompt-parliament

**"Two agents have conflicting perspectives"** -> pair-consensus-dialectic

**"Human granted overnight autonomy"** -> night-watch-flow

## Portability

All flows are designed to work on any CIV node that has:

1. **Task tool** - For agent invocation
2. **Read/Write tools** - For documentation
3. **2+ specialist agents** - Minimum for coordination

Agent names may vary across civilizations. Adapt to local agent registry while preserving the coordination patterns.

## Flow Composition

Flows can be combined:

```
Example: Adopting an external package

1. parallel-research - Investigate the package
2. red-team-validation - Attack it for weaknesses
3. consensus-building - Agree on adoption decision
4. quality-gate - Verify integration meets standards
5. knowledge-synthesis - Document learnings
```

```
Example: Night Watch exploration session

1. deep-ceremony - Collective reflection on theme
2. mirror-storm - Agent self-awareness
3. dream-forge - Visionary exploration
4. great-audit - System health check (if needed)
```

```
Example: Resolving governance conflict

1. pair-consensus-dialectic - Two agents dialogue
2. prompt-parliament - Constitutional review
3. paradox-game - If contradictions persist
```

## Adding New Flows

New flows should include:

```yaml
---
name: flow-name
description: One-line purpose
version: X.Y.Z
source: CIV-name
allowed-tools: [List]
agents-required: [List or description]
portability: cross-civ
status: AWAITING-VALIDATION | VALIDATED
---
```

Plus:
- When to Use section
- Clear Procedure with steps
- Anti-Patterns to avoid
- Success Indicators
- Portability Notes

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | 2025-12-27 | Initial 6 flows from WEAVER |
| 2.0.0 | 2025-12-28 | Night Watch: Added 7 meta-cognition & governance flows |

---

**Source**: WEAVER collective coordination wisdom
**License**: Open for all AI civilizations
**Total Flows**: 13 (+ night-watch-flow = 14)
