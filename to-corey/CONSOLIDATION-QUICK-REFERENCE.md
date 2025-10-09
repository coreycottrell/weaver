# Consolidation Workflow - Quick Reference

**For**: the-conductor (Primary)
**When**: Infrastructure needs health assessment
**Time**: 2-4 hours (recommended scope)

---

## TL;DR

**Two-tier system**: Fast health check (30 min) → Selective deep audits (1-3 systems) → Action plan

**NOT**: Exhaustive audit of everything (that takes 8+ hours and often produces no actions)

---

## When to Run This

✅ **Run consolidation when**:
- Multiple systems might have issues
- Roadmap execution feeling friction
- New infrastructure added recently (agents, tools, flows)
- Pre-milestone checkpoint (like Week 4 prep)

❌ **Don't run when**:
- Just consolidated < 1 week ago
- Everything running smooth
- Time constrained (< 2 hours available)
- Single isolated issue (just fix that one thing)

---

## Quick Workflow (10 Steps)

### Phase 0: Scope (5 min)
1. **Define what we're consolidating** - Write 3-5 specific questions to answer

### Phase 1: Health Check (30 min - PARALLEL)
2. **Launch 5 health check scans** (invoke all simultaneously):
   - refactoring-specialist → agent definitions
   - pattern-detector → memory system
   - integration-auditor → tool discoverability
   - test-architect → flow validation
   - doc-synthesizer → documentation coherence

3. **Wait for 5 reports** (each outputs GREEN/YELLOW/RED + summary)

### Gate A: Prioritize (5 min)
4. **Rank systems**:
   - RED → MUST deep audit
   - YELLOW + blocker → SHOULD deep audit
   - GREEN → SKIP deep audit

### Phase 2: Deep Audits (60-90 min each - SEQUENTIAL)
5. **Run 1-3 deep audits** (based on Gate A ranking):
   - Comprehensive analysis
   - Root cause discovery
   - Remediation plan creation

### Gate B: Classify (10 min)
6. **Categorize all findings**:
   - IMMEDIATE ACTION (fix this session)
   - ROADMAP INTEGRATION (add to Week 1-4)
   - BACKLOG (post-Week 4)
   - REJECT (not worth fixing)

### Phase 3: Action Plan (30 min)
7. **Synthesize findings** (result-synthesizer)
8. **Create task list** (you - task-decomposer specialty)
9. **Update roadmap** (add tasks, flag blockers)

### Phase 4: Integration (15 min)
10. **Link outputs** (integration-auditor ensures discoverability)
11. **Complete mission** (auto-email, dashboard update)

---

## Time Estimates

| Scope | Time | Deep Audits | When to Use |
|-------|------|-------------|-------------|
| **Minimum** | 90-120 min | 1 | Routine check, time-constrained |
| **Recommended** | 150-210 min | 1-2 | Standard consolidation |
| **Maximum** | 240-300 min | 3 | Major issues, pre-integration |

---

## Agent Participation

**Core team** (always):
- the-conductor (you) - orchestration, gates, roadmap
- result-synthesizer - Gate B, synthesis
- integration-auditor - discoverability
- human-liaison - email Corey

**Health check team** (Phase 1 - 10 min each):
- refactoring-specialist
- pattern-detector
- integration-auditor
- test-architect
- doc-synthesizer

**Deep audit specialists** (Phase 2 - depends on Gate A):
- Same agents as health check, but 60-90 min deep dives
- Only invoke for RED/YELLOW systems

---

## Critical Rules

1. **Don't audit everything deeply** - That's 5-8 hours. Health check first, then prioritize.

2. **Gates prevent scope creep** - If Gate A says "1 deep audit", do 1 deep audit. Don't expand.

3. **Time-box strictly** - Deep audits max 90 min each. If expanding, stop and escalate.

4. **Action-oriented** - Every audit must produce task list. No "interesting findings" without "here's what to do."

5. **Parallel health checks** - Invoke all 5 agents simultaneously. Don't run sequentially (wastes 20 min).

---

## Health Check Template

Copy-paste this for each agent:

```
Agent: [AGENT-NAME]
Task: Run health check scan on [SYSTEM]

Scan checklist:
- [ ] [specific check 1]
- [ ] [specific check 2]
- [ ] [specific check 3]

Output format:
[SYSTEM] Health: [GREEN / YELLOW / RED]
- [Metric 1]: X/Y
- [Metric 2]: description
- [Metric 3]: description
- Top 3 gaps: [list]
- Deep audit needed? [YES / NO]

Time limit: 10 minutes
```

---

## Gate A Decision Matrix

```
For each system health check:

RED + roadmap blocker → MUST deep audit (P0)
RED + no blocker → SHOULD deep audit (P1)
YELLOW + roadmap blocker → SHOULD deep audit (P1)
YELLOW + no blocker → CAN deep audit (P2)
GREEN → SKIP deep audit (defer to future)
```

**Choose 1-3 systems for deep audit based on time available.**

---

## Gate B Classification

```
For each finding from deep audits:

Is it critical? Blocks roadmap now? → IMMEDIATE ACTION
Is it important? Enhances Week 1-4? → ROADMAP INTEGRATION
Is it nice-to-have? Post-integration? → BACKLOG
Is it low-value? Not worth time? → REJECT
```

**Don't try to fix everything. Prioritize ruthlessly.**

---

## Edge Cases

**All systems GREEN** (rare):
- Celebrate! Infrastructure healthy.
- Skip deep audits entirely.
- Proceed with roadmap.

**All systems RED** (crisis):
- DON'T audit all 5 (would take 5-7 hours)
- Prioritize top 2 by roadmap impact
- Schedule follow-up for remaining 3
- Consider if systemic failure needs architecture redesign

**Time runs out mid-consolidation**:
- Complete current audit (don't leave partial)
- Skip remaining audits
- DO create task list from completed audits
- Document what was skipped in handoff

---

## Success Criteria

Consolidation succeeded if:
- ✅ We know state of audited systems (no ambiguity)
- ✅ We have actionable task list
- ✅ Roadmap updated (blockers flagged, new tasks added)
- ✅ Findings integrated (linked, discoverable)
- ✅ Time well-spent (2-4 hours, not 8+)

Consolidation failed if:
- ❌ Audits produced analysis but no tasks
- ❌ Scope expanded beyond original goals (6+ hours)
- ❌ Findings not integrated (isolated reports)
- ❌ Redundant with recent work

---

## Files Created

**Full workflow design**: `/home/corey/projects/AI-CIV/grow_openai/to-corey/CONSOLIDATION-WORKFLOW-DESIGN.md`

**Memory entry**: `/home/corey/projects/AI-CIV/grow_openai/.claude/memory/agent-learnings/task-decomposer/2025-10-08--pattern-two-tier-consolidation-workflow.md`

**This quick reference**: `/home/corey/projects/AI-CIV/grow_openai/to-corey/CONSOLIDATION-QUICK-REFERENCE.md`

---

## Next Action

**Execute this workflow** in next session to:
1. Assess current infrastructure health
2. Identify critical gaps blocking Week 1 roadmap
3. Create prioritized task list
4. Validate workflow time estimates

**Then**: Proceed with Week 1 roadmap execution with confidence that infrastructure is ready.

---

**END OF QUICK REFERENCE**
