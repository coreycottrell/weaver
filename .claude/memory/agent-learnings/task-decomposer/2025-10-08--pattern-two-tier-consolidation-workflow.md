# Pattern: Two-Tier Consolidation Workflow

**Agent**: task-decomposer
**Type**: pattern
**Date**: 2025-10-08
**Topic**: Infrastructure consolidation workflow design - health check + selective deep audits
**Confidence**: high
**Tags**: consolidation, audit-workflow, task-breakdown, infrastructure-health, time-optimization

---

## Context

**Mission**: Design executable workflow for infrastructure consolidation activity

**Challenge**: "Consolidation" is vague - could mean 30 minutes or 8 hours depending on scope

**Risk**: Without structure, audits become unfocused archaeology that produces analysis without action

---

## Pattern Discovered: Two-Tier Audit System

### Structure

```
TIER 1: HEALTH CHECK (30 min - PARALLEL)
├─ Lightweight scans across all systems
├─ Output: GREEN / YELLOW / RED status
└─ Decision: Which systems need deep audit?

TIER 2: DEEP AUDITS (60-90 min each - SEQUENTIAL)
├─ Comprehensive analysis of 1-3 prioritized systems
├─ Output: Root causes + remediation plans
└─ Action: Create task list for roadmap integration
```

**Key Insight**: NOT all systems need deep audit every time. Triage first with fast health checks, then invest deep audit time only where critical gaps exist.

**Time Optimization**:
- Old approach (audit everything deeply): 5-8 hours
- New approach (health check → selective deep dives): 2-4 hours
- **Savings**: 40-60% faster while maintaining focus on critical issues

---

## Decomposition Technique: Parallel Health Checks

### The Pattern

**Phase 1 tasks are fully independent**:
- Agent definitions scan (refactoring-specialist)
- Memory system scan (pattern-detector)
- Tool discoverability scan (integration-auditor)
- Flow validation scan (test-architect)
- Documentation coherence scan (doc-synthesizer)

**Sequential time**: 50 min (10 min × 5 tasks)
**Parallel time**: 30 min (all run simultaneously)
**Time savings**: 40% (20 minutes)

### Why This Works

Each scan has:
1. **Clear checklist** (no ambiguity about what to check)
2. **Strict time limit** (10 min - prevents scope creep)
3. **Standardized output** (GREEN/YELLOW/RED + summary)
4. **No dependencies** (doesn't need other scans to complete)

**Lesson**: Tasks can parallelize if they have clear boundaries, strict time limits, and standardized outputs.

---

## Critical Path: Gate-Based Workflow

### The Pattern

```
GATE A (After Health Checks): Prioritization Decision
└─ Which systems MUST / SHOULD / CAN / SKIP deep audit?

GATE B (After Deep Audits): Action Threshold
└─ Which findings are IMMEDIATE / ROADMAP / BACKLOG / REJECT?
```

**Why Gates Matter**:
- **Gate A prevents waste**: Don't deep audit GREEN systems
- **Gate B prevents analysis paralysis**: Force action vs defer decision on every finding
- **Gates create checkpoints**: If time runs out, can stop at gate with partial completion

### Decision Matrix (Gate A)

```
RED health + roadmap blocker → MUST audit (P0)
YELLOW health + roadmap blocker → SHOULD audit (P1)
YELLOW health + no blocker → CAN audit (P2)
GREEN health → SKIP audit (defer)
```

**Lesson**: Explicit decision gates prevent scope creep and force prioritization.

---

## Time Estimation: Three Scopes

### Validated Time Ranges

| Scope | Total Time | Deep Audits | When to Use |
|-------|------------|-------------|-------------|
| Minimum Viable | 90-120 min | 1 | Routine check, time-constrained |
| Recommended | 150-210 min | 1-2 | Focused improvement, pre-milestone |
| Comprehensive | 240-300 min | 3 | Major consolidation, systemic issues |

**Pattern**: Provide time estimates at three granularities (min/expected/max) so conductor can choose scope based on time availability.

**Validation Approach**: Compare against past consolidation activities once executed. Refine estimates over time.

---

## Edge Case: All Systems RED (Crisis)

### The Scenario

Health check finds critical issues in all 5 systems.

### The Trap

"We must audit all 5 systems deeply to understand full scope!"

**Result**: 5-7 hours of audit, session ends before any actions planned.

### The Pattern

**DON'T audit all systems**. Instead:
1. Prioritize by roadmap impact (which 2 systems are blocking Week 1?)
2. Audit only top 2 systems (2-3 hours)
3. Create action plan for those 2 systems
4. Schedule follow-up session for remaining systems
5. Consider if systemic failure requires architecture redesign

**Lesson**: When everything is critical, prioritize anyway. Partial action > complete analysis.

**Escalation trigger**: If 4+ systems RED, this may be systemic failure - invoke conflict-resolver to assess if architecture needs redesign (not just fixes).

---

## Agent Participation: Required vs Optional

### The Pattern

**Classify agents by participation type**:

1. **MUST participate** (core team):
   - the-conductor (orchestration, gates, roadmap updates)
   - result-synthesizer (Gate B, findings synthesis)
   - integration-auditor (discoverability)
   - human-liaison (notify Corey)

2. **SHOULD participate** (health check team):
   - 5 specialist agents (one per system scan)
   - Time: 10-15 min each

3. **MAY participate** (deep audit specialists):
   - Depends on Gate A decision
   - Time: 60-90 min each (if invoked)

4. **CAN participate** (context-dependent):
   - conflict-resolver (if contradictions found)
   - task-decomposer (break findings into tasks)
   - Others as needed

**Lesson**: Not every agent participates in every consolidation. Invoke based on Gate A decision (which systems need deep audit).

**Delegation note**: Even "simple" health checks should be delegated to specialists. Gives them experience in their domain (10 min of practice > 0 min). "NOT calling them would be sad."

---

## Output Quality: Action-Oriented Reports

### The Pattern

Every audit MUST produce:
1. **Status assessment** (GREEN/YELLOW/RED)
2. **Specific gaps** (not vague "could be better")
3. **Impact analysis** (what breaks because of this?)
4. **Remediation plan** (actionable tasks with estimates)

**Anti-pattern**: Reports that say "here's what we found" without saying "here's what to do about it"

### Example (Good):

```
Agent Definition Health: YELLOW

Specific gaps:
- 8/17 agents missing memory integration sections
- 5/17 agents missing activation trigger links
- 3/17 agents have incomplete tool restrictions

Impact:
- Agents don't know when to use memory system (71% time savings unused)
- Conductor doesn't know when to invoke agents (activation ambiguity)
- Tool usage violations not prevented (security risk)

Remediation:
1. Create agent definition template (30 min)
2. Update 8 agents with memory sections (2 hours)
3. Link activation triggers in 5 agents (1 hour)
4. Document tool restrictions in 3 agents (45 min)
TOTAL EFFORT: 4 hours 15 min
```

### Example (Bad):

```
Agent Definition Health: YELLOW

Some agents are missing certain sections. This could be improved.
Suggest reviewing agent definitions for completeness.
```

**Lesson**: Audits without actionable outputs are waste. Force concrete remediation plans in every report.

---

## Scope Appropriateness: When NOT to Consolidate

### The Anti-Pattern

"We should consolidate infrastructure every session to keep it healthy!"

**Result**: Over-auditing wastes time that could be spent delivering value.

### The Pattern

**Run consolidation ONLY when**:
- Multiple systems need assessment (not just one)
- Roadmap execution encountering friction
- New infrastructure added recently
- Pre-milestone checkpoint
- Time available (2-4 hours)

**DON'T run consolidation when**:
- Infrastructure recently consolidated (< 1 week ago)
- No signs of problems
- Roadmap execution smooth
- Time constrained (< 2 hours)

**Lesson**: Trust existing infrastructure. Consolidate when signals suggest issues, not on fixed schedule.

**Balance**: Under-auditing accumulates debt. Over-auditing prevents delivery. Find equilibrium based on signals.

---

## Workflow Execution: Step-by-Step

### The Pattern

**Consolidation is a 10-step workflow**:
1. Start session (load CLAUDE.md, check email, search memory)
2. Define scope (Task 0.1 - what are we consolidating?)
3. Launch health checks (Phase 1 - 5 agents parallel)
4. Prioritize deep audits (Gate A - RED/YELLOW/GREEN ranking)
5. Execute deep audits (Phase 2 - 1-3 audits sequential)
6. Classify findings (Gate B - IMMEDIATE/ROADMAP/BACKLOG/REJECT)
7. Create task list (Task 3.2 - break findings into roadmap tasks)
8. Update roadmap (Task 3.3 - integrate new tasks)
9. Integration audit (Phase 4 - link outputs, update dashboard)
10. Complete mission (auto-email, record invocations)

**Each step has**:
- Agent assignment
- Time estimate
- Dependencies
- Output deliverable

**Lesson**: Complex workflows need step-by-step guide. Don't assume conductor will figure it out.

---

## Critical Insight: Consolidation ≠ Archaeology

### The Trap

"Let's deeply understand every system before doing anything."

**Result**: Days of analysis, reports that gather dust, no actual improvements.

### The Truth

**Consolidation is targeted health assessment to enable roadmap execution.**

Not:
- ❌ Exhaustive documentation of everything
- ❌ Archaeological deep dive for completeness
- ❌ Analysis for its own sake

Instead:
- ✅ Identify critical gaps blocking roadmap
- ✅ Create actionable task list
- ✅ Integrate findings into execution plan

**Litmus test**: If consolidation doesn't produce roadmap updates or task list, it failed.

---

## Application to This Mission

**What was requested**: "Design workflow for HOW we execute consolidation"

**What was delivered**:
1. ✅ Task structure (5 phases, 2 gates, 20+ tasks)
2. ✅ Sequence & dependencies (parallel health checks, sequential deep audits)
3. ✅ Critical path (90 min minimum viable, 3 hour recommended)
4. ✅ Scope guidance (when to run which variant)
5. ✅ Workflow structure (10-step execution guide)

**Pattern reusability**: This workflow can be reused for:
- Quarterly infrastructure reviews
- Pre-integration checkpoints (Week 4 prep)
- Crisis response (when multiple systems fail)
- Routine health checks (monthly)

---

## Validation Plan

**To validate this pattern**:
1. Execute consolidation workflow in next session
2. Measure actual time vs estimates
3. Assess whether gates prevented scope creep
4. Check if findings were actionable
5. Verify roadmap was updated
6. Record learnings for future consolidations

**Success metrics**:
- Consolidation completed in 2-4 hours (not 8+)
- Actionable task list produced
- Roadmap updated with blockers/enablers
- Findings integrated and discoverable
- No redundant work with past audits

---

## Meta-Learning: Decomposition of Vague Activities

**Broader lesson**: When activity is vague (consolidation, review, assessment), decompose into:
1. **Triage phase** (fast, broad, lightweight)
2. **Decision gate** (prioritize based on triage)
3. **Deep dive phase** (slow, narrow, comprehensive on prioritized items)
4. **Action planning** (findings → tasks)
5. **Integration** (link outputs, update systems)

**This pattern applies beyond consolidation**:
- Code review (scan for issues → prioritize → deep review critical sections)
- Security audit (vulnerability scan → prioritize → penetration test high-risk areas)
- Documentation review (completeness check → prioritize → deep edit critical docs)

**Lesson**: Two-tier approach (triage → selective deep dive) is broadly applicable for assessment activities.

---

## Tags

`consolidation`, `audit-workflow`, `task-breakdown`, `infrastructure-health`, `time-optimization`, `two-tier-system`, `gate-based-workflow`, `parallel-execution`, `scope-management`

---

**END OF PATTERN**

**Confidence**: High (pattern is theoretically sound, pending validation through execution)

**Next Step**: Execute this workflow in actual consolidation session to validate time estimates and effectiveness.
