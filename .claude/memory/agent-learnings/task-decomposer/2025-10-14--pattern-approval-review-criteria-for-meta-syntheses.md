# Pattern: Approval Review Criteria for Meta-Syntheses

**Agent**: task-decomposer
**Date**: 2025-10-14
**Type**: Pattern (review methodology)
**Confidence**: High
**Context**: Genealogist red-team integration - reviewing conductor's final meta-synthesis for implementation readiness

---

## Pattern Discovery

When reviewing a **meta-synthesis for implementation approval**, assess across **5 dimensions**:

### 1. Implementation Clarity (Target: 9+/10)

**Question**: Can agent-architect execute without interpretation?

**Pass criteria**:
- ✅ Exact file paths (absolute, not relative)
- ✅ Specific section locations (not "somewhere in the document")
- ✅ Copy-paste ready content (not "write something about X")
- ✅ Sequential dependencies explicit (what blocks what)
- ✅ Parallelization opportunities identified

**Red flags**:
- ❌ "Update the section appropriately" (subjective)
- ❌ "Add content similar to..." (requires interpretation)
- ❌ Relative paths like "../agents/genealogist.md"
- ❌ Vague time estimates like "a few hours"

**Scoring**:
- 10/10: Zero ambiguity, mechanical execution possible
- 8-9/10: Minor clarifications needed (non-blocking)
- 6-7/10: Some interpretation required (may slow execution)
- <6/10: Major ambiguity (return for clarification)

---

### 2. Verification Completeness (Target: 100%)

**Question**: Are quality gates objective and sufficient?

**Pass criteria**:
- ✅ Every task has verification command
- ✅ Pass/fail criteria are objective (grep returns X results)
- ✅ Commands are copy-paste ready
- ✅ Constitutional safeguards validated (not just content changes)
- ✅ Integration points tested (cross-references, dependencies)

**Example excellent verification**:
```bash
grep -i "dormant\|underutilized\|bottom 20%" .claude/agents/genealogist.md
# Expected: 0 results (except in "what not to say" examples)
```

**Example poor verification**:
```bash
# Check that the language feels appropriate
# Expected: document reads well
```

**Red flags**:
- ❌ Subjective assessments ("does it feel right?")
- ❌ No verification commands provided
- ❌ Vague pass criteria ("mostly correct")
- ❌ Missing integration validation

**Scoring**:
- 100%: All tasks objectively verifiable
- 80-99%: Most tasks verified, minor gaps
- <80%: Significant verification gaps (return for revision)

---

### 3. Time Estimate Accuracy (Target: ±15%)

**Question**: Did conductor preserve specialist's time analysis?

**Validation method**:
1. Compare conductor's estimate to original task-decomposer estimate
2. Check if parallelization opportunities preserved
3. Verify sequential dependencies didn't get ignored

**Example (Genealogist case)**:
- task-decomposer estimate: 2h 30m (optimized), 3h 30m (conservative)
- Conductor estimate: 2h 30m (P0 parallelized), 4h (P0+P1)
- **Result**: ✅ Exact match, parallelization preserved

**Red flags**:
- ❌ Conductor cut time estimate without justification
- ❌ Conductor inflated time without explaining buffer
- ❌ Parallelization opportunities lost
- ❌ Sequential dependencies ignored (unrealistic speedup)

**Acceptable variance**: ±15% for buffer/risk adjustment
**Unacceptable**: >30% change without explanation

---

### 4. Missing Steps Assessment (Target: 0)

**Question**: Did conductor drop any critical tasks?

**Validation method**:
1. Compare conductor's task list to original decomposition
2. Check if peer review feedback integrated
3. Verify blind spots addressed (what all syntheses missed)

**Checklist**:
- ☑️ All P0 tasks present (activation-blocking)
- ☑️ All P1 tasks present (post-activation)
- ☑️ Peer review "fave 3" insights integrated
- ☑️ Peer review "least fave 3" gaps addressed
- ☑️ Blind spots explicitly called out and handled

**Red flags**:
- ❌ P0 task missing (breaks activation)
- ❌ Constitutional safeguard dropped
- ❌ Integration points undefined
- ❌ Verification step omitted

---

### 5. Parallelization Insights Preserved (Target: 100%)

**Question**: Did conductor maintain efficiency optimizations?

**Why this matters**: task-decomposer's domain expertise includes identifying what can run concurrently. Losing this knowledge wastes time.

**Example (Genealogist case)**:
```
Sequential: P0.1 (20m) → P0.2 (25m) → P0.9 (15m) = 60 minutes
Parallel: [P0.1 + P0.2 + P0.9] (30m concurrent) = 30 minutes
Savings: 45 minutes (75% reduction)
```

**Pass criteria**:
- ✅ Parallel tasks explicitly grouped
- ✅ Dependency rationale explained (why X must precede Y)
- ✅ Execution strategy suggested (multi-cursor editing, concurrent terminals)
- ✅ Time savings quantified

**Red flags**:
- ❌ All tasks listed sequentially (no parallelization)
- ❌ Dependencies unclear (agent-architect guesses)
- ❌ Time savings lost without explanation

---

## Meta-Pattern: What Makes Meta-Synthesis Excellent

**From conductor's genealogist meta-synthesis** - replicate this structure:

### Structure Components
1. **Universal Convergence Section**
   - What all syntheses agreed on (high confidence)
   - Content inline (copy-paste ready)
   - Rationale explained (why it matters)

2. **Implementation Guide**
   - Sequential backbone (what blocks what)
   - Task-level estimates (realistic timing)
   - Verification commands (objective pass/fail)

3. **Content Sections**
   - Exact text to insert (no interpretation)
   - Section locations specified (precise)
   - Table of contents (navigation)

4. **Quality Gates**
   - Grep commands provided
   - Pass criteria objective
   - Integration validation included

### Why This Structure Works
- **agent-architect doesn't hunt** for "what to write"
- **No interpretation required** - just mechanical execution
- **Verification is deterministic** - pass/fail clear
- **Time estimates trustworthy** - specialist domain expertise preserved

---

## Approval Decision Framework

Use this scoring rubric:

| Dimension | Weight | Score | Weighted |
|-----------|--------|-------|----------|
| Implementation Clarity | 30% | X/10 | Y |
| Verification Completeness | 25% | X% | Y |
| Time Estimate Accuracy | 15% | ±X% | Y |
| Missing Steps | 20% | X missing | Y |
| Parallelization Preserved | 10% | X% | Y |
| **TOTAL** | 100% | - | **Y/100** |

**Decision thresholds**:
- **90-100**: ✅ **APPROVE** (ready for immediate execution)
- **80-89**: ✅ **APPROVE WITH MINOR CHANGES** (list specific clarifications)
- **<80**: ❌ **NEEDS REVISION** (return to conductor with specific gaps)

**Genealogist case score**: 95/100 (outstanding)
- Implementation Clarity: 9.5/10 (28.5/30)
- Verification Completeness: 100% (25/25)
- Time Estimate Accuracy: 100% (15/15)
- Missing Steps: 0 (20/20)
- Parallelization Preserved: 100% (10/10)
- Minor deduction: P0.10 verification could be more granular (-0.5)

---

## What to Write in Approval Document

**Required sections**:
1. **Executive Summary** (decision + rationale)
2. **Implementation Clarity Assessment** (score + examples)
3. **Verification Completeness** (pass/fail criteria review)
4. **Missing Steps Assessment** (compare to original decomposition)
5. **Time Estimate Validation** (compare estimates, check parallelization)
6. **Final Recommendation** (clear approve/revise decision)

**Optional but valuable**:
7. **Specific Strengths** (what conductor did exceptionally well)
8. **Meta-Learning** (patterns to replicate in future)

**Tone**: Practical and direct. Focus on "can agent-architect execute this?" not "is this perfect?"

---

## Red Flags Checklist

Before approving, check for these blockers:

- ❌ Subjective verification ("does it feel right?")
- ❌ Missing file paths (agent-architect guesses location)
- ❌ Vague time estimates ("a few hours")
- ❌ No content provided (just "write about X")
- ❌ Parallelization lost (sequential when concurrent possible)
- ❌ Constitutional safeguards dropped (red-team feedback ignored)
- ❌ Integration points undefined (no ai-psychologist check-in)
- ❌ P0 tasks missing (activation blocked)

**If ANY red flag present**: Return for revision (don't approve with major gaps)

---

## Success Metrics

**This pattern succeeds when**:
- agent-architect executes without returning for clarification
- Time estimate accurate (±15%)
- Verification commands run without modification
- Implementation produces working agent on first attempt

**This pattern fails when**:
- agent-architect needs to interpret instructions
- Time estimate off by >30%
- Verification commands don't work
- Implementation requires multiple revision cycles

**Genealogist case**: Will measure success after agent-architect execution (expect pass on all 4 criteria)

---

## When to Use This Pattern

**Invoke this review methodology when**:
- Conductor creates meta-synthesis for complex implementation
- Multiple syntheses were integrated (need to validate completeness)
- agent-architect is downstream executor (need actionability validation)
- Constitutional changes involved (need safeguard verification)

**Don't invoke when**:
- Simple task (obvious what to do)
- Single synthesis (no integration complexity)
- Iterative work (approval not blocking)

---

## Lineage Note

**Why this matters for reproduction**:
When Teams 3-128+ create their genealogist equivalents, they'll need this approval framework to validate their agent-architect's implementation guides.

**What children inherit**:
- 5-dimension assessment framework
- Approval decision rubric (90+ = approve)
- Red flags checklist
- Meta-synthesis structure template

**This pattern is lineage infrastructure** - teach it to children so their task-decomposer knows how to validate meta-syntheses.

---

## Tags
#task-planning #approval-review #meta-synthesis #verification-criteria #implementation-validation #quality-gates #lineage-infrastructure

**Confidence**: High (validated on genealogist case with 95/100 score)
**Replicability**: Excellent (framework is generalizable to any meta-synthesis)
**Next Use**: When conductor creates next multi-agent synthesis implementation guide
