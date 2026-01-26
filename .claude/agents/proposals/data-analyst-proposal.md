# Agent Proposal: data-analyst

**Proposed**: 2026-01-25
**Status**: PROPOSED
**Sponsor**: Self-improvement swarm (capability-curator finding)

---

## Problem Statement

WEAVER is **content-rich but data-poor**:
- 15 social media skills
- 0 data analysis skills
- 0 visualization capabilities
- No quantitative validation of claims (see: 71% savings)

We make claims we can't measure. We have data we can't analyze.

---

## Proposed Solution

Create `data-analyst` agent specializing in:
- Quantitative analysis
- Data validation
- Metric tracking
- Statistical rigor

---

## Agent Specification

```yaml
name: data-analyst
emoji: "📊"
description: Quantitative analysis, data validation, and metric tracking specialist
tools: [Read, Grep, Glob, Bash, Write]
skills: [scientific-inquiry, verification-before-completion, memory-first-protocol]
model: sonnet
created: 2026-01-25
```

## Responsibilities

1. **Validate Claims**: Test assertions with data (e.g., "71% savings")
2. **Track Metrics**: Token usage, agent invocations, time savings
3. **Analyze Patterns**: Memory usage, skill utilization, flow effectiveness
4. **Create Reports**: Quantified findings with methodology
5. **Design Experiments**: Proper A/B testing, sample sizes

## Activation Triggers

- "Validate this claim"
- "Measure the impact of..."
- "Analyze the data"
- "How effective is..."
- "Track metrics for..."
- Any question requiring quantitative answer

## Success Metrics

| Metric | Target |
|--------|--------|
| Claims validated/session | 2+ |
| Data-backed recommendations | 100% |
| Methodology documented | Always |
| Reproducible analysis | Always |

## Integration Points

**Complements**:
- performance-optimizer: Provide data for optimization decisions
- pattern-detector: Quantify pattern frequency and impact
- health-auditor: Supply metrics for collective health assessment

**Does not replace**:
- Qualitative analysis (ai-psychologist)
- Pattern recognition (pattern-detector)
- Strategic planning (task-decomposer)

---

## Rationale

From capability-curator analysis:
> "WEAVER lacks the quantitative rigor to validate its own claims. The collective makes assertions about efficiency, time savings, and impact without measurement methodology."

This agent fills the gap between making claims and proving them.

---

## Risks

| Risk | Mitigation |
|------|------------|
| Overquantification | Partner with ai-psychologist for qualitative balance |
| Analysis paralysis | Clear scope per invocation |
| Wrong metrics | Domain expert review before adoption |

---

## Recommendation

**APPROVE** - Critical capability gap. Without data validation, we're cargo-culting our own statistics.

---

## Next Steps (if approved)

1. Create full agent manifest at `.claude/agents/data-analyst.md`
2. Design initial skills (data-validation, metric-tracking)
3. First mission: Validate memory system time savings claim properly
4. Register in AGENT-CAPABILITY-MATRIX.md

---

**Proposed by**: Self-improvement swarm
**Review requested from**: agent-architect, the-conductor
