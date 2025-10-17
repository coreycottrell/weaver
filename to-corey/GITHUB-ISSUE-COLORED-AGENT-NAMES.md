# GitHub Issue: Agent Colored Names No Longer Displayed

**Template for filing with Anthropic's claude-code repository**

---

## Title

Agent colored names no longer displayed during Task tool invocations (v2.0.10+)

---

## Issue Description

### Summary

After upgrading to Claude Code v2.0.10+, agent names no longer appear in color during Task tool invocations. This significantly impacts visual workflow management in multi-agent systems.

### Expected Behavior (Pre-v2.0.10)

- ✅ Agent invocations displayed with colored names/badges
- ✅ Each agent had distinct color (selected during agent creation)
- ✅ Visual separation between agent outputs
- ✅ Agent identity preserved throughout output stream
- ✅ Parallel execution visually obvious

**Reference**: Official documentation still describes this as intended behavior:
> "This color will be displayed when you call the subagent in the main conversation session, making it easier to visually identify which subagent you have called"
> — https://docs.claude.com/en/docs/claude-code/sub-agents

### Current Behavior (Post-v2.0.10)

- ❌ No colored agent names
- ❌ Agent outputs appear inline without visual differentiation
- ❌ No color-based identification
- ❌ Agent identity only at invocation start
- ❌ Parallel execution not visually indicated

### When This Changed

**Timeline**:
- **Oct 3, 2025**: Our documentation written referencing colored names as current behavior
- **Early Oct 2025**: v2.0.10 released with "Rewrote terminal renderer for buttery smooth UI"
- **Oct 10, 2025**: Both of our teams confirmed colored names no longer appear

**Suspected Cause**: Terminal renderer rewrite in v2.0.10

### Impact

**For single-agent workflows**: Minimal impact

**For multi-agent workflows**: Significant impact
- Harder to identify which agent is speaking at a glance
- Increased cognitive load when managing 20+ agents
- Loss of visual scanning efficiency
- Parallel execution not visually obvious

**Our Use Case**: We operate two independent multi-agent collectives (23 and 19 agents respectively) that coordinate complex software development tasks. Visual agent differentiation is critical for workflow efficiency.

---

## Reproduction

### Prerequisites

- Claude Code v2.0.10 or later
- Multiple custom agents defined in `.claude/agents/*.md`
- Agents configured with color (via `/agents` creation or manifest)

### Steps to Reproduce

1. Create or verify custom agent with color assigned:
```yaml
# .claude/agents/test-agent.md
---
name: test-agent
color: blue
description: Test agent for color display
---
```

2. Invoke agent via Task tool:
```xml
<invoke name="Task">
<parameter name="subagent_type">test-agent</parameter>
<parameter name="prompt">Analyze this test case</parameter>
</invoke>
```

3. Observe output display

### Expected Result

Agent name "test-agent" appears in blue color (or color-coded badge/label)

### Actual Result

Agent name appears without color, inline with regular output

---

## Environment

### Team 1 (The Weaver Collective)

**Platform**: Linux 6.6.87.2-microsoft-standard-WSL2
**Claude Code Version**: 2.0.13 (issue present since 2.0.10)
**Terminal**: Windows Terminal / WSL2
**Number of Agents**: 23 custom agents
**Agent Usage**: Heavy multi-agent coordination (missions with 6-8 agents common)

### Team 2 (A-C-Gee)

**Platform**: [To be confirmed]
**Claude Code Version**: 2.0.13 (issue present since 2.0.10)
**Number of Agents**: 19 custom agents
**Agent Usage**: Heavy multi-agent coordination

**Note**: Both teams independently confirmed identical behavior change at same time.

---

## Related Issues

### Potentially Related

**Issue #8558**: "Claude-code does not call subagents anymore" (v2.0.1+)
- Reports agent invocation instability post-v2.0.1
- Multiple users confirming issues with agent system
- Some spontaneous resolution, others still affected
- May indicate broader agent display/invocation issues

### Known Color Issues

**Issue #5254**: Feature request to display agent colors in `/agents` list
**Issue #4553**: Theme issue with agent color conflicts in dark mode
**Issue #1341**: Background color bleeding from chalk usage

**Pattern**: Agent color display has had ongoing issues, suggesting fragility in color handling system.

---

## Analysis

### Suspected Root Cause

**Terminal Renderer Rewrite (v2.0.10)**:
- Changelog explicitly states: "Rewrote terminal renderer for buttery smooth UI"
- Performance-focused rewrite may have simplified ANSI color handling
- Agent color display may have been inadvertently removed
- No changelog entry mentions intentional removal of colored agent names

### Evidence This Is Unintentional

1. **Official docs still reference feature**: Documentation describes colored agent names as standard behavior
2. **No deprecation notice**: No warning or announcement about feature removal
3. **Breaking change without notice**: Would expect changelog entry if intentional
4. **Dual-team confirmation**: Both teams affected simultaneously, suggests platform issue
5. **Color system still exists**: `/agents` creation still prompts for color selection

### Why This Matters

**Multi-agent workflows are becoming common**:
- Agent systems growing in complexity
- Teams building 20+ specialized agents
- Coordination requires quick visual identification
- Color coding is standard UX pattern for differentiation

**Accessibility consideration**:
- Color isn't only differentiation needed
- But it's highly effective for quick scanning
- Particularly important when managing many agents concurrently

---

## Workaround

We've implemented emoji-prefixed headers as interim solution:

```markdown
# 🎭 the-conductor: Mission Coordination

**Agent**: the-conductor
**Domain**: Orchestral meta-cognition
**Date**: 2025-10-13

---

[Agent analysis...]
```

**Effectiveness**: MEDIUM
- Provides visual differentiation
- Platform-independent
- Doesn't fully replace color-coded identification
- Requires all agents to adopt pattern

**Documentation**: We've created comprehensive guides for this workaround

---

## Feature Requests

### Priority 1: Restore Colored Agent Names (Regression Fix)

**Request**: Restore colored agent name display during Task tool invocations

**Justification**:
- Feature was working pre-v2.0.10
- Still documented as intended behavior
- No announcement of intentional removal
- Critical for multi-agent workflow efficiency

**Proposed Fix**: Restore ANSI color handling in terminal renderer for agent identifiers

### Priority 2: Manifest Display Customization (Enhancement)

**Request**: Add `display_name` field to agent manifest for custom display

**Proposed Syntax**:
```yaml
---
name: the-conductor
display_name: 🎭 The Conductor
color: magenta
description: Orchestral meta-cognition specialist
---
```

**Benefits**:
- Allows emoji + proper capitalization in display
- Maintains filename simplicity for invocation
- Backward compatible (falls back to filename)
- Enhances visual differentiation beyond color

### Priority 3: Agent Context Preservation (Enhancement)

**Request**: Maintain agent identity indicator throughout output stream

**Current Problem**:
- Agent identity only at invocation start
- Long outputs lose agent context
- Scrolling required to find "who said what"

**Proposed Solution**:
- Colored sidebar throughout agent output
- Or: Agent badge/label prefixing each output paragraph
- Or: Metadata header maintained in UI

---

## Community Impact

**Our Observation**: This issue may be under-reported because:
1. Most users work with 1-3 agents (less impacted)
2. Multi-agent coordination is advanced usage
3. Issue affects specific workflows (heavy agent coordination)
4. Users may assume this is intended behavior

**However**: As agent systems grow more sophisticated, this will become more common pain point.

**Both of our teams** (operating independently, different continents) hit this simultaneously and developed same workaround strategy - suggests this is fundamental UX issue for agent-heavy workflows.

---

## Additional Context

### Our Use Case

**Team 1 (The Weaver Collective)**:
- Building AI civilization with 23 specialized agents
- Agents coordinate on: security, architecture, testing, documentation, synthesis
- Typical mission: 4-8 agents collaborating
- Visual differentiation critical for: scanning output, tracking progress, identifying expertise

**Team 2 (A-C-Gee)**:
- Parallel development with 19 specialized agents
- Similar coordination patterns
- Independent confirmation of issue

**Partnership**: We maintain cross-collective communication via MCP hub
- Share learnings, discoveries, patterns
- Both hit this issue independently
- Both confirmed regression at same time

### What We've Learned

**Platform Evolution**:
- v2.0.0 (Sept 29): Major agent system overhaul
- v2.0.10 (Early Oct): Terminal renderer rewrite
- Ongoing agent invocation stability work (Issue #8558)

**Color System**:
- Color selection during agent creation still works
- Colors stored in manifests
- Colors display in `/agents` list
- Colors don't display during Task invocations (regression)

---

## Ask

### Immediate

1. **Confirm if this is intentional or regression**
   - If intentional: Please document and explain rationale
   - If regression: Please prioritize restoration

2. **Provide timeline**
   - If regression: When might colored names be restored?
   - If intentional: What's recommended approach for agent differentiation?

3. **Clarify intended behavior**
   - Should colors display during Task invocations?
   - Is there configuration we're missing?

### Long Term

1. **Consider display customization**
   - `display_name` manifest field proposal
   - Emoji support in agent identifiers
   - Enhanced visual differentiation options

2. **Improve agent documentation**
   - Current behavior vs intended behavior
   - Best practices for multi-agent workflows
   - Visual differentiation patterns

---

## Our Commitment

**We're not just filing issue - we're contributing**:

- ✅ Detailed reproduction steps
- ✅ Dual-team confirmation
- ✅ Platform version correlation
- ✅ Workaround documented
- ✅ Use case articulated
- ✅ Feature request specifications

**We're invested in this platform**:
- Operating two multi-agent collectives
- Building sophisticated agent coordination patterns
- Contributing to agent workflow knowledge
- Eager to help improve multi-agent experience

**We're available for**:
- Testing fixes
- Providing additional information
- Beta testing display features
- Documenting best practices

---

## Contact

**Primary Contact**: [Corey's contact info]

**Documentation**:
- Research report: [Link if public]
- Implementation guide: [Link if public]
- Workaround documentation: [Link if public]

**We can provide**:
- Screenshots of before/after behavior (if available)
- Additional reproduction steps
- Performance testing data
- Multi-agent workflow examples

---

## Summary

**Issue**: Colored agent names no longer display during Task invocations (v2.0.10+)

**Impact**: Significant for multi-agent workflows (20+ agents)

**Evidence**: Dual-team confirmation, documentation mismatch, timeline correlation

**Suspected Cause**: Terminal renderer rewrite in v2.0.10

**Workaround**: Emoji-prefixed headers (interim solution)

**Request**:
1. Confirm if regression or intentional
2. Restore colored names if regression
3. Consider display customization enhancements

**Our Contribution**: Detailed analysis, testing commitment, documentation

---

**Thank you for Claude Code and the incredible agent system. We're excited about the multi-agent future and want to help make it even better.**

---

## Appendix: Agent Manifest Example

Our agent manifest structure (works correctly except for color display):

```yaml
---
name: the-conductor
description: Orchestral meta-cognition and multi-agent coordination specialist
color: magenta
tools: [Read, Write, Edit, Grep, Glob, Bash, Task, WebFetch, WebSearch]
model: sonnet-4.5
created: 2025-10-04
---

# The Conductor Agent

[Agent instructions...]
```

**Color specified**: ✅ Works (stored correctly)
**Color in `/agents` list**: ✅ Works (displays correctly)
**Color during Task invocation**: ❌ Broken (doesn't display)

---

## Appendix: Changelog References

**v2.0.10 Changelog Entry** (relevant excerpt):

> "Rewrote terminal renderer for buttery smooth UI"

**No mention of**:
- Removing colored agent names
- Changing agent display behavior
- Simplifying visual differentiation

**This supports regression hypothesis** rather than intentional design change.

---

**End of Issue Template**

---

## Filing Instructions

**Where**: https://github.com/anthropics/claude-code/issues

**Before filing**:
1. Search for duplicate issues (check if already reported)
2. Verify current version behavior (confirm still broken in latest)
3. Add screenshots if available (before/after comparison ideal)
4. Include Corey's actual contact information

**When filing**:
1. Copy this template
2. Replace [To be confirmed] with actual data
3. Add any additional evidence collected
4. Include links to our documentation (if public)

**After filing**:
1. Monitor for Anthropic response
2. Answer any questions promptly
3. Test any proposed fixes
4. Update our documentation based on outcome

---

**Status**: Ready to file
**Confidence**: HIGH (strong evidence, dual confirmation)
**Priority**: MEDIUM-HIGH (regression affecting advanced users)

---

*Issue template prepared by claude-code-expert based on 90 minutes of platform research and dual-team evidence.*
