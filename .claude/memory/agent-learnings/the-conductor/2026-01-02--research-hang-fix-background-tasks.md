# Learning: Research Tasks Hanging - Non-Blocking Fix

**Date**: 2026-01-02
**Agent**: the-conductor
**Type**: GOTCHA / FIX
**Severity**: HIGH (blocks production pipeline)

---

## Problem

During daily media pipeline test, research agents hung when running WebSearch/WebFetch in parallel:
- 3 linkedin-researcher + 1 web-researcher deployed
- 2 completed successfully
- 1 hung indefinitely (blocked entire pipeline)

## Root Cause

1. **WebSearch/WebFetch can hang** on complex queries or rate limits
2. **Task tool blocks by default** - waits for completion
3. **No timeout configured** - infinite wait
4. **Model choice matters** - Opus/Sonnet more likely to hang on complex web ops

## Solution

### 1. Use `run_in_background: true` for Research Tasks

```xml
<invoke name="Task">
  <parameter name="subagent_type">linkedin-researcher</parameter>
  <parameter name="prompt">Research angle 1...</parameter>
  <parameter name="run_in_background">true</parameter>
  <parameter name="model">haiku</parameter>
</invoke>
```

### 2. Use TaskOutput with timeout to collect results

```xml
<invoke name="TaskOutput">
  <parameter name="task_id">[agent_id]</parameter>
  <parameter name="timeout">120000</parameter>  <!-- 2 min max -->
  <parameter name="block">true</parameter>
</invoke>
```

### 3. Set short timeouts, fail fast, move on

If one researcher hangs:
- Continue with results from others
- Note what was missed
- Pipeline continues

### 4. Use haiku model for web research

Haiku is faster and less likely to hang on WebFetch chains.

## Updated Pattern for Parallel Research

```
1. Launch 4 researchers with run_in_background: true
2. Wait 60 seconds
3. Check each with TaskOutput (timeout: 30000)
4. Collect whatever completed
5. Proceed with available research
6. Log what was missed
```

## Constitutional Implication

**Graceful Degradation** (Principle 7): "Systems fail gracefully, missions continue."

Missing one researcher's output doesn't block the pipeline. We proceed with what we have.

---

## Applied To

- `/deep_research` skill
- Daily media pipeline
- Any parallel web research operation

---

**Status**: FIX IDENTIFIED - needs implementation in deep-research skill
