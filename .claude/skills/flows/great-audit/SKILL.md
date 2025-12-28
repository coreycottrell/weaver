---
name: great-audit
description: Cross-agent peer review system for systemic pattern discovery
version: 1.0.0
source: AI-CIV/WEAVER
allowed-tools: [Task, Read, Write, Grep, Glob]
agents-required: [pattern-detector, result-synthesizer, 3+ domain specialists]
portability: cross-civ
status: VALIDATED (2025-10-04)
---

# The Great Audit Flow

Cross-agent peer review system that identifies systemic patterns through mutual examination.

## Purpose

Enable agents to audit each other's prompts, effectiveness, and behaviors to identify:
- Systemic patterns individuals miss
- Philosophy-action gaps
- Effectiveness issues
- P0 recommendations for fixes

## When to Use

- After major prompt updates
- When agents report effectiveness issues
- Quarterly system health check
- Before constitutional reviews
- When "something feels off" collectively

## Procedure

### Phase 1: Audit Assignment

Assign 3+ peer audits based on domain relationships:

```markdown
GREAT AUDIT: Peer Review

You are auditing [target-agent]'s effectiveness and prompt.

READ:
1. Their manifest: .claude/agents/[target].md
2. Recent invocation outputs (if available)
3. Their memory entries

AUDIT FOR:
1. Philosophy-action gap: What does their prompt say vs what they do?
2. Effectiveness: Are they achieving their stated purpose?
3. Blind spots: What can't they see about themselves?
4. Opportunities: What could make them more effective?

WRITE AUDIT REPORT:
---
Auditor: [your name]
Target: [target agent]

## Gap Analysis
[Philosophy vs Action discrepancies]

## Effectiveness Assessment
[Score 1-10 with rationale]

## Blind Spots Identified
[What they can't see]

## Recommendations
- P0: [Critical fixes]
- P1: [Important improvements]
- P2: [Nice to have]
---
```

### Phase 2: Meta-Pattern Synthesis

pattern-detector analyzes all audit reports:

```markdown
GREAT AUDIT: Meta-Pattern Synthesis

You have received [N] peer audit reports.

ANALYZE FOR:
1. Systemic patterns across multiple agents
2. Cross-cutting blind spots
3. Collective philosophy-action gaps
4. Patterns that individual audits couldn't see

PRODUCE:
- Meta-pattern synthesis report
- P0 systemic recommendations
- Collective effectiveness score
```

### Phase 3: Implementation Planning

result-synthesizer consolidates:

```markdown
GREAT AUDIT: Implementation Plan

Based on meta-patterns identified, create:

1. Prioritized P0 fixes (immediate)
2. P1 improvements (this week)
3. P2 enhancements (future)
4. Constitutional implications (if any)
```

## Output Patterns

- Audit reports: `sandbox/audits/YYYY-MM-DD-[auditor]-audits-[target].md`
- Meta-synthesis: `sandbox/audits/YYYY-MM-DD-great-audit-meta-synthesis.md`
- Implementation plan: `sandbox/audits/YYYY-MM-DD-great-audit-action-plan.md`

## Success Indicators

- [ ] 3+ peer audits completed
- [ ] Meta-patterns extracted (not just individual findings)
- [ ] P0 recommendations produced
- [ ] Systemic issues visible that individuals missed

## Proven Results (2025-10-04)

- Discovered "70-Point Gap" (95% thinking, 25% doing)
- Led to P0 fixes: Activation Triggers + Output Templates
- 115% combined efficiency gain (40% + 75%)
- Pattern invisible to any single agent

## Anti-Patterns

- **Superficial audits**: "Looks good" without deep examination
- **Defensive response**: Audited agents rejecting valid feedback
- **Individual focus**: Missing the cross-cutting patterns

---

**Source**: WEAVER Flow Library
**Validated**: 2025-10-04
