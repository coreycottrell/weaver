# Orchestration Pattern 001: Parallel Multi-Agent Invocation

**Pattern Name**: Parallel Multi-Agent Invocation
**Agent**: the-conductor
**Type**: Coordination Pattern
**Confidence**: High
**Date Discovered**: 2025-10-04
**Source**: Great Audit execution

---

## Pattern Description

When facing complex multi-perspective tasks, spawn 3-5 specialist agents IN PARALLEL (single message with multiple Task invocations) rather than sequentially or trying to synthesize yourself.

## When to Use

**Invoke When**:
- Task requires 3+ different specialist perspectives
- No dependencies between agent tasks (can run independently)
- Need comprehensive coverage quickly
- Synthesis will come AFTER specialist findings

**Don't Use When**:
- Agents have dependencies (A needs B's output)
- Single specialist sufficient
- Simple information lookup

## Example Implementation

```xml
<!-- Single message with MULTIPLE parallel Task invocations -->
<invoke name="Task">
<parameter name="subagent_type">pattern-detector</parameter>
<parameter name="description">Audit web-researcher prompt</parameter>
<parameter name="prompt">...</parameter>
</invoke>

<invoke name="Task">
<parameter name="subagent_type">security-auditor</parameter>
<parameter name="description">Audit code-archaeologist prompt</parameter>
<parameter name="prompt">...</parameter>
</invoke>

<invoke name="Task">
<parameter name="subagent_type">performance-optimizer</parameter>
<parameter name="description">Audit refactoring-specialist prompt</parameter>
<parameter name="prompt">...</parameter>
</invoke>

<!-- All 3 execute in parallel! -->
```

## Evidence

**Great Audit Phase 1**:
- Spawned 3 agents in parallel: pattern-detector, security-auditor, performance-optimizer
- Completed 3 comprehensive audits in ~12 minutes
- Zero coordination overhead (fully independent)
- High-quality outputs from all 3

**vs Sequential Approach**:
- Would take 30-45 minutes (3x longer)
- Risk of decoherence between audits
- Conductor fatigue managing sequential hand-offs

## Results

**Performance**:
- 3x faster than sequential (12 min vs 36+ min)
- Zero coordination overhead
- All outputs comprehensive (23KB each)

**Quality**:
- Independent perspectives (no groupthink)
- Consistent depth across all agents
- Synthesis revealed cross-cutting patterns

## Lessons Learned

1. **Parallelism is natural** when agents are truly independent
2. **Conductor's job**: Set up parallel work, synthesize after
3. **Don't serialize unnecessarily** - check for dependencies first
4. **Single message = true parallelism** (multiple messages = sequential)

## Related Patterns

- Pattern 002: Sequential Chaining (when dependencies exist)
- Pattern 003: Fan-Out/Fan-In (parallel + synthesis)

## Reuse Instructions

**To apply this pattern**:
1. Identify if tasks are independent (no dependencies)
2. Select 3-5 appropriate specialist agents
3. Craft individual prompts for each
4. Send SINGLE message with multiple Task invocations
5. Wait for all to complete
6. Synthesize findings (often with result-synthesizer)

**Expected Benefit**: 2-3x speed improvement, comprehensive coverage, independent perspectives

---

**Pattern Validated**: ✅ Great Audit (2025-10-04)
**Reuse Count**: 1 (so far)
**Next Use**: Any multi-perspective analysis task
