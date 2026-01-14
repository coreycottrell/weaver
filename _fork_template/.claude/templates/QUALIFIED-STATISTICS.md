# Qualified Statistics Template

## The "71% Time Savings" Claim

### What We Actually Measured (N=1)

**Single experiment** (Oct 3, 2025):
- **Round 1**: 6 agents research memory systems → 145 minutes
- **Round 2**: Same 6 agents design memory system using Round 1 memories → 42 minutes
- **Savings**: 103 minutes (71% reduction)

**Conditions**:
- Same agents both rounds
- Highly related tasks (design what you just researched)
- Optimal memory relevance (perfect topic match)
- Sequential work (immediate application)

### What This Means

**High confidence for similar scenarios**:
- ✅ Related sequential work by same agents
- ✅ High topic overlap between past and current work
- ✅ Well-tagged, searchable memories

**Unknown confidence for**:
- ❓ Unrelated tasks (cold topics)
- ❓ Different agent combinations
- ❓ Novel problems (no prior memory)
- ❓ Long-term memory (30+ days old)

### Correct Usage

**Instead of**: "Memory system delivers 71% time savings"
**Say**: "In one validation scenario (N=1), memory search reduced time 71% for related sequential work"

**Instead of**: "71% time savings proven"
**Say**: "71% time savings measured in optimal conditions; broader validation ongoing"

### Realistic Expectations

Based on single data point, reasonable estimates:
- **Same task, same agents, sequential**: 50-70% savings (likely)
- **Related task, different agents**: 20-40% savings (moderate)
- **Unrelated task, cold start**: 0-10% savings (minimal)
- **Novel problems**: May hurt (searching wastes time if no relevant memories)

### What We Need

**To generalize the 71% claim**, we need:
1. ✅ N=1 measured (Oct 3)
2. ❌ N=10+ across diverse scenarios
3. ❌ Different agent combinations tested
4. ❌ Unrelated task performance measured
5. ❌ Long-term memory value tracked
6. ❌ Failure cases documented (when memory hurts)

**Current status**: PARTIALLY VALIDATED (1 scenario only)

---

## Template for All Future Claims

### Statistical Claim Format

```markdown
**Claim**: [Metric] of [Value]

**Evidence**:
- N=[sample size]
- Conditions: [specific scenario]
- Date: [when measured]
- Reference: [file with data]

**Generalizability**:
- High confidence: [what this applies to]
- Unknown: [what we haven't tested]
- Unlikely: [where this probably doesn't apply]

**Status**: VALIDATED | PARTIALLY VALIDATED | HYPOTHESIS
```

### Example: 71% Claim (Corrected)

```markdown
**Claim**: Memory system time savings of 71%

**Evidence**:
- N=1 (single experiment)
- Conditions: Same 6 agents, related sequential task, optimal topic match
- Date: 2025-10-03
- Reference: `/to-${HUMAN_NAME_LOWER}/MEMORY-SYSTEM-COMPARISON.md`

**Generalizability**:
- High confidence: Related work by same agents
- Unknown: Unrelated tasks, different agents, novel problems
- Unlikely: Cold starts with no relevant memory

**Status**: PARTIALLY VALIDATED (need N=10+ diverse scenarios)
```

---

## Red Team Feedback Integration

**From pattern-detector anti-pattern analysis**:
> "71% appears 108 times across codebase. It has become liturgy, not hypothesis."

**From test-architect validation gaps**:
> "MISLEADINGLY PRESENTED: Single data point (n=1) generalized as if proven system-wide"

**Action taken**: Created this template to qualify all statistical claims going forward

---

**This template is NOW THE STANDARD for all metrics we report.**
