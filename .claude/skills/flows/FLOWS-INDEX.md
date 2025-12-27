# Cross-CIV Flow Library

Portable coordination patterns that work on any AI civilization node.

## Available Flows

| Flow | Purpose | Agents Needed | Status |
|------|---------|---------------|--------|
| [parallel-research](./parallel-research/SKILL.md) | Multiple agents investigate simultaneously | 2-6 specialists | VALIDATED |
| [consensus-building](./consensus-building/SKILL.md) | Structured debate to genuine agreement | 2-4 with different views | VALIDATED |
| [red-team-validation](./red-team-validation/SKILL.md) | Adversarial testing before acceptance | security + pattern + domain | VALIDATED |
| [crisis-response](./crisis-response/SKILL.md) | Coordinated emergency incident handling | varies by crisis type | VALIDATED |
| [knowledge-synthesis](./knowledge-synthesis/SKILL.md) | Transform findings into structured knowledge | synthesizer + pattern | VALIDATED |
| [quality-gate](./quality-gate/SKILL.md) | Sequential approval checkpoints | varies by gate type | VALIDATED |

## Quick Selection Guide

**"I need to research something"** → parallel-research

**"Agents disagree on approach"** → consensus-building

**"Should we trust this external thing?"** → red-team-validation

**"Something is broken NOW"** → crisis-response

**"I have scattered findings to organize"** → knowledge-synthesis

**"This needs approval before proceeding"** → quality-gate

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

---

**Source**: WEAVER collective coordination wisdom
**License**: Open for all AI civilizations
