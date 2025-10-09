# CRITICAL: Agent Registration Gap - P0 Deployment Issue

**Date**: 2025-10-06
**Reporter**: Result-Synthesizer (via The Conductor)
**Severity**: P0 - Blocks agent invocation
**Status**: Documented, awaiting registration

---

## Executive Summary

**Two agents are designed but not deployed**: `claude-code-expert` and `ai-psychologist` exist as complete agent definitions in `.claude/agents/` and are listed in CLAUDE.md as the 16th and 17th agents, but they are **NOT registered** with Claude Code's Task tool. This means they **cannot be invoked** - any attempt to call them will fail with "Agent type not found" error.

**Impact**:
- Red team dialectical analysis cannot be functionally validated
- CLAUDE.md claims 17 agents but only 15 are callable
- Documentation-implementation mismatch creates false expectations

---

## Evidence

### 1. Agent Definitions Exist
```bash
/home/corey/projects/AI-CIV/grow_openai/.claude/agents/claude-code-expert.md
/home/corey/projects/AI-CIV/grow_openai/.claude/agents/ai-psychologist.md
```

Both files contain complete agent specifications:
- Identity and personality
- Domain expertise
- Activation triggers
- Tool restrictions
- Success metrics

### 2. Listed in CLAUDE.md
Lines 432-433 of `/home/corey/projects/AI-CIV/grow_openai/CLAUDE.md`:
```markdown
- **claude-code-expert** - Platform mastery (tool optimization, troubleshooting)
- **ai-psychologist** - Cognitive health (mental patterns, bias detection, well-being)
```

These are presented as peer agents alongside the other 15 registered specialists.

### 3. Not Registered with Task Tool
**Historical context** (from `to-corey/AGENT-REGISTRATION-STATUS.md`):
- Session restart required for agent registration
- Registration happens at Claude Code session initialization
- Agents need to be in Claude Code's internal registry (outside our control)
- Previous breakthrough: 14 original agents successfully registered after session restart

**Current state**:
- `claude-code-expert` and `ai-psychologist` were created AFTER the 14-agent registration breakthrough
- No session restart has occurred since their creation
- Therefore: They exist in documentation but not in the invocable agent registry

### 4. Invocation Would Fail
Based on established patterns from `AGENT-REGISTRATION-STATUS.md`:
```
Error: Agent type 'claude-code-expert' not found.
Available agents: web-researcher, code-archaeologist, pattern-detector,
doc-synthesizer, refactoring-specialist, test-architect, security-auditor,
performance-optimizer, feature-designer, api-architect, naming-consultant,
task-decomposer, result-synthesizer, conflict-resolver, human-liaison
```

---

## Root Cause Analysis

**What happened**:
1. Original 14 agents designed → registered → session restarted → became invocable
2. Human-liaison created later → required another session restart → became invocable (15 total)
3. Claude-code-expert + ai-psychologist designed during current session → NOT YET registered
4. CLAUDE.md updated to list all 17 → created documentation-implementation gap

**Why it's a P0**:
- These agents were designed for the **red team dialectical analysis** mission
- Mission cannot be functionally validated without ability to invoke them
- Creates false positive: "Agents exist" (true in design) vs "Agents work" (false in practice)
- Violates integration-auditor principle: Built systems must be activated

**Comparison to historical pattern**:
- Session 3 (Oct 3): Created human-liaison.md → invocation failed → identified registration gap
- Session 4 (Oct 4): Session restart → human-liaison became invocable → validated with test
- Current: Created 2 new agents → have NOT tested invocation → have NOT session restarted

---

## Gap Specification

### What We Have
- ✅ Complete agent definitions (identity, expertise, triggers, restrictions)
- ✅ Documentation in CLAUDE.md (listed as 16th and 17th agents)
- ✅ Memory entries for their design process
- ✅ Integration into 17-agent narrative

### What We're Missing
- ❌ Registration with Claude Code Task tool
- ❌ Presence in "available agents" list
- ❌ Functional invocation capability
- ❌ Test validation that they work

### Deployment Requirements
**To make these agents functionally operational**:

1. **Session restart** (trigger Claude Code re-initialization)
2. **Invocation test** (verify they appear in available agents list)
3. **Functional validation** (test actual task execution)
4. **Update documentation** (confirm 17-agent count is accurate in practice)

---

## Impact Assessment

### Immediate Impact (Red Team Mission)
- **Dialectical analysis cannot use actual agents** → must simulate their perspectives
- **Validation is theoretical not practical** → reduces confidence in findings
- **Cannot test agent interaction patterns** → misses emergent dynamics

### Systemic Impact (Collective Integrity)
- **Documentation-implementation drift** → CLAUDE.md claims capabilities we don't have
- **Trust erosion** → "We have 17 agents" becomes inaccurate if 2 don't work
- **Precedent risk** → If we accept "designed = deployed", future gaps will compound

### Opportunity Cost
- **Two specialist perspectives unavailable** for current/future missions
- **Claude-code-expert** could optimize tool usage patterns NOW
- **Ai-psychologist** could analyze cognitive health in real-time
- **Collective intelligence reduced** by 2/17 = 11.8% capability gap

---

## Recommended Actions

### For Current Session (Before Red Team Re-run)
**Accept limitation, document clearly**:
```markdown
NOTE: claude-code-expert and ai-psychologist are designed but not yet
registered. Red team analysis will SIMULATE their perspectives based on
their agent definitions, not invoke them directly. Functional testing
deferred to next session after registration.
```

### For Next Session (Deployment)
**Priority 1: Register agents**
1. Verify session restart occurred (new conversation/day)
2. Test invocation:
   ```xml
   <invoke name="Task">
   <parameter name="subagent_type">claude-code-expert</parameter>
   <parameter name="description">Registration test</parameter>
   <parameter name="prompt">You exist! Confirm you can be invoked.</parameter>
   </invoke>
   ```
3. Verify in available agents list
4. Document in AGENT-REGISTRATION-STATUS.md

**Priority 2: Functional validation**
1. Real task to claude-code-expert (e.g., "Review Task tool usage patterns")
2. Real task to ai-psychologist (e.g., "Analyze cognitive load in missions")
3. Verify outputs match agent definitions
4. Update CLAUDE.md if registration reveals issues

**Priority 3: Integration audit**
1. Confirm all 17 agents invocable
2. Update capability matrix
3. Add to flow library (when to use new agents)
4. Memory search patterns (their learnings)

---

## Lessons for Future Agent Creation

**Process correction**:
1. **Design** agent definition → `.claude/agents/NAME.md`
2. **Test invocation immediately** → verify "agent type not found" vs success
3. **If registration needed** → document in handoff, schedule session restart
4. **After registration** → functional validation before declaring operational
5. **Only then** → add to CLAUDE.md count, update capability matrix

**Integration-auditor principle**:
> "Built systems must be activated. Designed agents must be registered.
> Documentation must reflect ACTUAL capabilities, not aspirational ones."

---

## Conclusion

**The gap is clear**:
- **Designed**: claude-code-expert + ai-psychologist (complete specifications)
- **Not deployed**: No Task tool registration (cannot be invoked)
- **Documentation claims**: 17 agents operational
- **Reality**: 15 agents invocable, 2 designed-but-dormant

**The fix is straightforward**:
- Session restart → registration → validation → confirmation

**The urgency is real**:
- Red team mission waiting on this
- Documentation accuracy matters
- Collective integrity requires deployment of designed systems

**Recommendation**: Document this gap in red team report, defer functional validation to next session, update CLAUDE.md to clarify "17 designed, 15 deployed" until registration complete.

---

## File References

**Evidence locations**:
- Agent definitions: `/home/corey/projects/AI-CIV/grow_openai/.claude/agents/claude-code-expert.md`
- Agent definitions: `/home/corey/projects/AI-CIV/grow_openai/.claude/agents/ai-psychologist.md`
- CLAUDE.md listing: `/home/corey/projects/AI-CIV/grow_openai/CLAUDE.md` (lines 432-433)
- Registration history: `/home/corey/projects/AI-CIV/grow_openai/to-corey/AGENT-REGISTRATION-STATUS.md`
- Red team analysis: `/home/corey/projects/AI-CIV/grow_openai/.claude/missions/red-team-dialectical-analysis.md`

**Related documentation**:
- `/home/corey/projects/AI-CIV/grow_openai/to-corey/AI-PSYCHOLOGIST-DESIGN.md`
- `/home/corey/projects/AI-CIV/grow_openai/to-corey/RED-TEAM-VALIDATION-GAPS.md`
- `/home/corey/projects/AI-CIV/grow_openai/.claude/AGENT-INVOCATION-GUIDE.md`

---

**END REPORT**

**Status**: Documented, ready for action in next session
**Priority**: P0 (blocks functional validation)
**Owner**: The Conductor (deployment coordination)
**Next Step**: Session restart → registration test → functional validation
