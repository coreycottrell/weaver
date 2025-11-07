# Consolidation Workflow Design

**Agent**: task-decomposer
**Date**: 2025-10-08
**Mission**: Design executable workflow for infrastructure consolidation activity

---

## Executive Summary

**Problem**: Multiple infrastructure systems need consolidation assessment before proceeding with roadmap execution.

**Solution**: Two-tier audit system with fast health check (30 min) followed by selective deep dives (60-90 min each).

**Critical Insight**: NOT all audits are equal priority. Run lightweight triage first, then invest deep audit time only where critical gaps exist.

**Total Time**:
- Health Check Phase: 30 minutes
- Deep Audit Phase: 60-180 minutes (1-3 deep dives, chosen based on health check findings)
- Action Planning: 30 minutes
- **Total: 2-4 hours** (vs 8+ hours for comprehensive deep audit)

---

## Phase Structure

```
PHASE 0: SCOPE DEFINITION (5 min)
└─ Define what "consolidation" means for this session

PHASE 1: HEALTH CHECK AUDIT (30 min - PARALLEL)
├─ Agent definitions quality scan
├─ Memory system activation scan
├─ Tool discoverability scan
├─ Flow validation scan
└─ Documentation coherence scan

GATE A: Prioritization Decision
└─ Which systems need deep audit?

PHASE 2: DEEP AUDITS (60-90 min each - SEQUENTIAL)
├─ Deep Audit #1: Highest priority system
├─ Deep Audit #2: Second priority (if needed)
└─ Deep Audit #3: Third priority (if needed)

GATE B: Action Threshold
└─ Are findings actionable? Critical? Defer-able?

PHASE 3: ACTION PLANNING (30 min)
├─ Synthesize all findings
├─ Create prioritized task list
└─ Update roadmap with blockers/enablers

PHASE 4: INTEGRATION (15 min)
└─ Link deliverables, update dashboard, notify stakeholders
```

---

## Detailed Task Breakdown

### PHASE 0: Scope Definition (5 min)

**Task 0.1: Define Consolidation Goals** (5 min)
- **Who**: the-conductor (you) + human-liaison (if Corey available)
- **Input**: Current roadmap state, recent session outputs
- **Output**: 3-5 specific questions to answer (e.g., "Are agent definitions up to standard?", "Is memory system actually being used?")
- **Decision**: Health check only? Or health check + selected deep dives?
- **Complexity**: Simple
- **Dependencies**: None

**Why This Matters**: Without clear scope, audits become unfocused archaeology. Define success criteria first.

---

### PHASE 1: Health Check Audit (30 min - PARALLEL)

**Pattern**: Lightweight scans across all systems. **NOT** comprehensive analysis. Goal is triage: Green/Yellow/Red.

#### Task 1.1: Agent Definition Quality Scan (10 min)

**Who**: refactoring-specialist (quality standards expert)

**Scan Checklist**:
- [ ] Do all 17+ agents have definition files?
- [ ] Do files follow AGENT-QUALITY-STANDARDS.md template?
- [ ] Are memory integration sections present?
- [ ] Are activation triggers linked?
- [ ] Are tool restrictions documented?

**Output Format**:
```
Agent Definition Health: [GREEN / YELLOW / RED]
- Agents with complete definitions: X/17
- Missing critical sections: [list]
- Top 3 gaps: [specific issues]
- Deep audit needed? [YES / NO]
```

**Time**: 10 min (NOT deep review, just structural scan)
**Complexity**: Simple

---

#### Task 1.2: Memory System Activation Scan (10 min)

**Who**: pattern-detector (infrastructure usage pattern expert)

**Scan Checklist**:
- [ ] How many agents reference memory system in their definitions?
- [ ] How many memory entries written in past 7 days?
- [ ] How many memory searches performed recently?
- [ ] Is memory system linked in agent definitions?
- [ ] Are agents actually using memory_core.py?

**Output Format**:
```
Memory System Health: [GREEN / YELLOW / RED]
- Agents with memory sections: X/17
- Memory entries (7 days): N
- Memory searches (7 days): N
- Usage trend: [increasing / stable / declining]
- Deep audit needed? [YES / NO]
```

**Time**: 10 min (count files, grep searches, NOT content analysis)
**Complexity**: Simple

---

#### Task 1.3: Tool Discoverability Scan (10 min)

**Who**: integration-auditor (discoverability expert)

**Scan Checklist**:
- [ ] Is Mission class documented in CLAUDE-OPS.md?
- [ ] Is memory_core documented in CLAUDE-OPS.md?
- [ ] Is hub_cli documented in CLAUDE-OPS.md?
- [ ] Are tools linked from agent definitions?
- [ ] Do tools have usage examples?

**Output Format**:
```
Tool Discoverability Health: [GREEN / YELLOW / RED]
- Tools documented: X/Y
- Tools with examples: X/Y
- Tools linked from agents: X/Y
- Integration gaps: [list]
- Deep audit needed? [YES / NO]
```

**Time**: 10 min (structural check, NOT usage analysis)
**Complexity**: Simple

---

#### Task 1.4: Flow Validation Scan (10 min)

**Who**: test-architect (validation expert)

**Scan Checklist**:
- [ ] How many flows validated? (3/14 currently)
- [ ] Are validated flows documented?
- [ ] Are unvalidated flows blocking roadmap?
- [ ] Is flow selection guide usable?
- [ ] Do agents reference flows in their definitions?

**Output Format**:
```
Flow System Health: [GREEN / YELLOW / RED]
- Flows validated: 3/14 (21%)
- Roadmap blockers: [list]
- Documentation gaps: [list]
- Agent integration: X/17 agents reference flows
- Deep audit needed? [YES / NO]
```

**Time**: 10 min (count and structural check)
**Complexity**: Simple

---

#### Task 1.5: Documentation Coherence Scan (10 min)

**Who**: doc-synthesizer (coherence expert)

**Scan Checklist**:
- [ ] Do CLAUDE.md, CLAUDE-CORE.md, CLAUDE-OPS.md cross-reference correctly?
- [ ] Are file paths accurate?
- [ ] Are navigation guides up to date?
- [ ] Are there obvious contradictions?
- [ ] Is three-document architecture clear?

**Output Format**:
```
Documentation Health: [GREEN / YELLOW / RED]
- Cross-references valid: X/Y
- Broken links: [list]
- Contradictions found: [list]
- Navigation clarity: [assessment]
- Deep audit needed? [YES / NO]
```

**Time**: 10 min (structural scan, NOT comprehensive review)
**Complexity**: Simple

---

### GATE A: Prioritization Decision (5 min)

**Who**: the-conductor (you)

**Input**: 5 health check reports (Tasks 1.1-1.5)

**Decision Matrix**:
```
For each system:
- RED health → MUST deep audit (critical)
- YELLOW health + roadmap blocker → SHOULD deep audit (important)
- YELLOW health + no blocker → CAN deep audit (nice-to-have)
- GREEN health → SKIP deep audit (defer)
```

**Output**: Ranked list of 0-3 systems for deep audit

**Example**:
```
Deep Audit Priority:
1. Agent definitions (RED - 8/17 missing critical sections)
2. Memory system (YELLOW - only 3/17 agents using it)
3. SKIP flow validation (YELLOW but no immediate blocker)
4. SKIP tool discoverability (GREEN)
5. SKIP documentation (GREEN)
```

**Time**: 5 min
**Complexity**: Simple (just ranking)

---

### PHASE 2: Deep Audits (60-90 min each - SEQUENTIAL)

**Pattern**: Comprehensive analysis of 1-3 systems identified in Gate A.

#### Task 2.1: Deep Audit #1 (60-90 min)

**Who**: Depends on system (refactoring-specialist for agents, pattern-detector for memory, etc.)

**Deep Audit Structure**:
1. **Enumerate Issues** (20-30 min)
   - List every gap, inconsistency, missing piece
   - Categorize: Critical / Important / Nice-to-have

2. **Root Cause Analysis** (15-20 min)
   - WHY did this gap occur?
   - What pattern caused it?
   - What infrastructure would prevent it?

3. **Impact Assessment** (10-15 min)
   - What breaks because of this?
   - What roadmap tasks are blocked?
   - What's the risk of not fixing?

4. **Remediation Plan** (15-25 min)
   - Specific tasks to fix issues
   - Time estimates per task
   - Dependencies between fixes
   - Quick wins vs long-term solutions

**Output Format**: Full report (similar to past RED-TEAM reports)

**Time**: 60-90 min (depends on system complexity)
**Complexity**: Complex

---

#### Task 2.2: Deep Audit #2 (60-90 min) [OPTIONAL]

**Trigger**: Only if Gate A identified 2+ systems needing deep audit

**Structure**: Same as Task 2.1

**Dependency**: Task 2.1 complete (learn from first audit's patterns)

**Time**: 60-90 min
**Complexity**: Complex

---

#### Task 2.3: Deep Audit #3 (60-90 min) [OPTIONAL]

**Trigger**: Only if Gate A identified 3 systems needing deep audit

**Structure**: Same as Task 2.1

**Dependency**: Task 2.2 complete

**Time**: 60-90 min
**Complexity**: Complex

---

### GATE B: Action Threshold (10 min)

**Who**: result-synthesizer + conflict-resolver

**Input**: 1-3 deep audit reports

**Decision Questions**:
1. **Actionable?** Can we fix these issues now?
2. **Critical?** Do these block Week 1 roadmap tasks?
3. **Defer-able?** Can these wait until after Week 4 integration?

**Output**: Classification of all findings:
```
IMMEDIATE ACTION (this session):
- [Critical fixes that unblock roadmap]

ROADMAP INTEGRATION (add to Week 1-4 plan):
- [Important fixes to schedule]

BACKLOG (post-Week 4):
- [Nice-to-have improvements]

REJECT (not worth fixing):
- [Low-value findings]
```

**Time**: 10 min
**Complexity**: Moderate (requires synthesis + judgment)

---

### PHASE 3: Action Planning (30 min)

#### Task 3.1: Synthesize Findings (10 min)

**Who**: result-synthesizer

**Goal**: Create single consolidated view of all audit findings

**Output**: Executive summary with:
- Systems audited (health check + deep dives)
- Critical gaps found
- Roadmap impact assessment
- Recommended actions (categorized by urgency)

**Time**: 10 min
**Complexity**: Moderate

---

#### Task 3.2: Create Task List (15 min)

**Who**: task-decomposer (you)

**Goal**: Break remediation plans into actionable roadmap tasks

**Output**: Task list in roadmap format:
```
- [ ] **Fix agent definition templates**
  - Dependencies: None
  - Validates: All 17 agents have complete definitions
  - Output: Updated agent files + quality checklist
  - Effort: 2 hours
  - Priority: P0 (blocks agent invocation clarity)
```

**Time**: 15 min
**Complexity**: Moderate (your specialty!)

---

#### Task 3.3: Update Roadmap (5 min)

**Who**: the-conductor

**Goal**: Integrate findings into INTEGRATION-ROADMAP.md

**Actions**:
- Add blockers to existing tasks
- Add new tasks to appropriate weeks
- Update success criteria if needed
- Flag dependencies

**Time**: 5 min
**Complexity**: Simple

---

### PHASE 4: Integration (15 min)

#### Task 4.1: Link Deliverables (5 min)

**Who**: integration-auditor

**Goal**: Ensure audit outputs are discoverable

**Actions**:
- Link from CLAUDE-OPS.md
- Update dashboard
- Cross-reference in relevant agent definitions

**Time**: 5 min
**Complexity**: Simple

---

#### Task 4.2: Update Dashboard (5 min)

**Who**: the-conductor (using progress_reporter.py)

**Goal**: Record consolidation activity metrics

**Actions**:
- Log audit completion
- Record findings count
- Update roadmap task counts
- Track time spent

**Time**: 5 min
**Complexity**: Simple

---

#### Task 4.3: Notify Stakeholders (5 min)

**Who**: human-liaison

**Goal**: Email Corey with consolidation results

**Output**: Email with:
- What was audited
- Critical findings
- Roadmap updates
- Next actions

**Time**: 5 min
**Complexity**: Simple

---

## Critical Path Analysis

### Minimum Viable Consolidation (90 min)

**Fastest path to actionable output**:
```
Task 0.1 (5 min) →
Tasks 1.1-1.5 PARALLEL (30 min) →
Gate A (5 min) →
Task 2.1 (60 min) →
Gate B (10 min) →
Task 3.2 (15 min) →
Task 4.3 (5 min)

TOTAL: 130 min (2 hours 10 min)
```

**What's skipped**:
- Deep audits #2 and #3 (only audit highest priority system)
- Formal synthesis report (go straight from audit to task list)
- Dashboard updates (defer to later)

**Output**: Prioritized task list addressing most critical gap

---

### Recommended Consolidation (3 hours)

**Balanced path**:
```
PHASE 0: 5 min
PHASE 1: 30 min (parallel)
GATE A: 5 min
PHASE 2: 60-90 min (1-2 deep audits)
GATE B: 10 min
PHASE 3: 30 min
PHASE 4: 15 min

TOTAL: 155-185 min (2.5-3 hours)
```

**Output**: Comprehensive consolidation with 1-2 deep audits, full task list, integrated into roadmap

---

### Comprehensive Consolidation (5 hours)

**Maximum thoroughness**:
```
All phases executed
3 deep audits performed
Full synthesis and documentation
Complete integration audit

TOTAL: 4-5 hours
```

**When to use**: Major infrastructure crisis, pre-integration milestone, quarterly review

**Not recommended for**: Routine consolidation (overkill)

---

## Parallel Opportunities

### Phase 1: ALL Tasks Parallel (Save 20 min)

**Tasks 1.1-1.5 are fully independent**:
- Agent definitions (refactoring-specialist)
- Memory system (pattern-detector)
- Tool discoverability (integration-auditor)
- Flow validation (test-architect)
- Documentation coherence (doc-synthesizer)

**Sequential time**: 50 min (10 min × 5 tasks)
**Parallel time**: 30 min (10 min max, if all agents work simultaneously)
**Time savings**: 20 min (40% faster)

**How**: Invoke all 5 agents at once with identical prompt structure:
```
"Run health check scan on [SYSTEM]. Use [CHECKLIST]. Output [FORMAT]. Time limit: 10 min."
```

---

### Phase 2: No Parallelization (Deep audits must be sequential)

**Why**: Deep audits are complex, require synthesis, and later audits benefit from patterns discovered in earlier audits.

**Example**: Agent definition audit might reveal that agents lack memory integration sections. Memory system audit can then focus on WHY agents don't reference it (missing infrastructure vs missing awareness).

**Attempting parallel deep audits**: Risks duplicated work, contradictory recommendations, synthesis overhead.

---

## Effort Estimation

### By Phase

| Phase | Min Time | Max Time | Expected Time |
|-------|----------|----------|---------------|
| Phase 0: Scope | 5 min | 10 min | 5 min |
| Phase 1: Health Check | 30 min | 40 min | 30 min |
| Gate A: Prioritization | 5 min | 10 min | 5 min |
| Phase 2: Deep Audit #1 | 60 min | 90 min | 75 min |
| Phase 2: Deep Audit #2 | 60 min | 90 min | 75 min (if needed) |
| Phase 2: Deep Audit #3 | 60 min | 90 min | 75 min (if needed) |
| Gate B: Action Threshold | 5 min | 15 min | 10 min |
| Phase 3: Action Planning | 20 min | 40 min | 30 min |
| Phase 4: Integration | 10 min | 20 min | 15 min |

### By Scope

| Scope | Total Time | Deep Audits | Output Quality |
|-------|------------|-------------|----------------|
| Minimum Viable | 90-120 min | 1 | Actionable, focused |
| Recommended | 150-210 min | 1-2 | Comprehensive, prioritized |
| Maximum | 240-300 min | 3 | Exhaustive, documented |

### By Complexity

**Simple consolidation** (1 critical gap identified):
- Time: 90-120 min
- Agents: 6-7 (health check team + 1 deep auditor)
- Output: Focused task list

**Moderate consolidation** (2-3 gaps identified):
- Time: 150-210 min
- Agents: 8-10 (health check team + 2-3 deep auditors + synthesizers)
- Output: Comprehensive remediation plan

**Complex consolidation** (systemic issues discovered):
- Time: 240-300 min
- Agents: 12-15 (full team engagement)
- Output: Major architectural recommendations

---

## Agent Participation

### Required Agents (Core Team)

**MUST participate** (critical for consolidation):
1. **the-conductor** (you) - Orchestration, Gate A, Gate B, Task 3.3
2. **result-synthesizer** - Gate B, Task 3.1 (consolidate findings)
3. **integration-auditor** - Task 4.1 (ensure discoverability)
4. **human-liaison** - Task 4.3 (notify Corey)

**Time commitment**: Full session (2-4 hours)

---

### Health Check Team (Phase 1)

**SHOULD participate** (specialized scans):
1. **refactoring-specialist** - Task 1.1 (agent definitions)
2. **pattern-detector** - Task 1.2 (memory system)
3. **integration-auditor** - Task 1.3 (tool discoverability)
4. **test-architect** - Task 1.4 (flow validation)
5. **doc-synthesizer** - Task 1.5 (documentation coherence)

**Time commitment**: 10-15 min each (one task, then done)

**Delegation note**: These scans give agents experience in their domains. Don't skip even if "simple" - let them practice.

---

### Deep Audit Specialists (Phase 2)

**MAY participate** (depends on Gate A decision):
1. **refactoring-specialist** - If agent definitions need deep audit
2. **pattern-detector** - If memory system needs deep audit
3. **integration-auditor** - If tool discoverability needs deep audit
4. **test-architect** - If flow validation needs deep audit
5. **doc-synthesizer** - If documentation needs deep audit
6. **security-auditor** - If security concerns emerge
7. **code-archaeologist** - If historical context needed

**Time commitment**: 60-90 min each (if invoked)

**Delegation note**: Deep audits are high-value experience. Gives agents ownership of their domain.

---

### Optional Specialists (Context-Dependent)

**CAN participate** (if specific needs arise):
1. **conflict-resolver** - If contradictory findings emerge (Gate B)
2. **task-decomposer** - Task 3.2 (break findings into tasks)
3. **api-architect** - If API design issues found
4. **feature-designer** - If UX issues found
5. **naming-consultant** - If terminology issues found

**Time commitment**: 15-30 min each (focused contribution)

---

## Scope Appropriateness Guide

### When to Run Health Check Only (90 min)

**Scenarios**:
- Routine check-in (weekly/bi-weekly)
- No critical roadmap blockers suspected
- Recent major consolidation already done
- Time-constrained session

**Output**: High-level system status, prioritized list of systems needing attention

**Next Action**: Schedule deep audits for RED systems in future session

---

### When to Run Health Check + 1 Deep Audit (2-3 hours)

**Scenarios**:
- One system suspected of major gaps
- Critical roadmap task approaching (needs validation)
- Recent changes to one system (agent definitions, memory, etc.)
- Focused improvement needed

**Output**: Comprehensive analysis of one system, actionable task list

**Next Action**: Execute remediation tasks, monitor other systems

---

### When to Run Health Check + 2-3 Deep Audits (4-5 hours)

**Scenarios**:
- Multiple systems showing signs of issues
- Pre-integration milestone (Week 4 prep)
- Major architecture change planned
- Comprehensive consolidation overdue

**Output**: Full infrastructure assessment, prioritized roadmap updates

**Next Action**: Major remediation sprint, systemic improvements

---

### When NOT to Run Consolidation

**Don't consolidate if**:
- Infrastructure just consolidated (< 1 week ago)
- No new systems built since last check
- Roadmap execution going smoothly (no blockers)
- Time better spent on actual delivery

**Alternative**: Trust existing infrastructure, focus on value delivery

**Note**: Over-auditing wastes time. Under-auditing accumulates debt. Balance.

---

## Workflow Execution Guide

### Step-by-Step (Recommended Path)

#### 1. Start Session (5 min)

```bash
# Load constitutional documents
cat /home/corey/projects/AI-CIV/grow_openai/CLAUDE.md
cat /home/corey/projects/AI-CIV/grow_openai/.claude/CLAUDE-CORE.md

# Check email FIRST (constitutional requirement)
# Invoke human-liaison to handle email

# Search memory for past consolidation patterns
python3 << 'EOF'
from tools.memory_core import MemoryStore
store = MemoryStore(".claude/memory")
patterns = store.search_by_topic("consolidation")
audits = store.search_by_topic("infrastructure audit")
for memory in patterns[:3]:
    print(f"\n{memory.topic}:\n{memory.content[:200]}...")
EOF
```

---

#### 2. Define Scope (Task 0.1 - 5 min)

**Decision**: What are we consolidating? Why now?

**Output**: 3-5 specific questions to answer

**Example**:
```
Consolidation Goals (2025-10-08):
1. Are agent definitions up to AGENT-QUALITY-STANDARDS.md?
2. Is memory system being used by agents?
3. Are tools discoverable from agent definitions?
4. Is three-document architecture coherent?
5. What's blocking Week 1 roadmap execution?
```

---

#### 3. Launch Health Check (Phase 1 - 30 min PARALLEL)

**Invoke 5 agents simultaneously**:

```
Agent: refactoring-specialist
Task: Run health check scan on agent definitions
Checklist: [Task 1.1 checklist from above]
Output format: [GREEN/YELLOW/RED] + summary + deep audit recommendation
Time limit: 10 minutes
```

(Repeat for pattern-detector, integration-auditor, test-architect, doc-synthesizer)

**Wait for all 5 reports** (30 min max)

---

#### 4. Prioritize Deep Audits (Gate A - 5 min)

**Review 5 health check reports**

**Rank systems**:
- RED → MUST audit
- YELLOW + blocker → SHOULD audit
- YELLOW + no blocker → CAN audit
- GREEN → SKIP audit

**Decide**: 1, 2, or 3 deep audits?

**Time-box**: If limited time, choose only 1 (highest priority)

---

#### 5. Execute Deep Audits (Phase 2 - 60-180 min SEQUENTIAL)

**For each prioritized system**:

```
Agent: [specialist for this system]
Task: Comprehensive deep audit of [SYSTEM]
Structure:
1. Enumerate issues (20-30 min)
2. Root cause analysis (15-20 min)
3. Impact assessment (10-15 min)
4. Remediation plan (15-25 min)
Output: Full report with prioritized recommendations
```

**Wait for completion before starting next audit**

**Learn from each audit**: Patterns in first audit inform later audits

---

#### 6. Classify Findings (Gate B - 10 min)

**Invoke**: result-synthesizer + conflict-resolver

**Task**: Categorize all findings as:
- IMMEDIATE ACTION (this session)
- ROADMAP INTEGRATION (Week 1-4)
- BACKLOG (post-Week 4)
- REJECT (not worth fixing)

**Output**: Classified findings list

---

#### 7. Create Task List (Task 3.2 - 15 min)

**Invoke**: task-decomposer (you)

**Task**: Break remediation plans into roadmap tasks

**Output**: Task list with:
- Task description
- Dependencies
- Validation criteria
- Output deliverable
- Effort estimate
- Priority

---

#### 8. Update Roadmap (Task 3.3 - 5 min)

**You (the-conductor)**:

```bash
# Edit INTEGRATION-ROADMAP.md
# Add new tasks to appropriate weeks
# Flag blockers on existing tasks
# Update success criteria if needed
```

---

#### 9. Integration Audit (Phase 4 - 15 min)

**Invoke**: integration-auditor

**Task**: Ensure all consolidation outputs are discoverable

**Actions**:
- Link from CLAUDE-OPS.md
- Update dashboard
- Cross-reference in agent definitions

---

#### 10. Complete Mission (5 min)

**You (the-conductor)**:

```python
from tools.conductor_tools import Mission

mission = Mission("infrastructure-consolidation")
mission.assign_agents([
    "refactoring-specialist",
    "pattern-detector",
    # ... all agents used
])
mission.complete(
    outputs={
        "health_check_reports": "to-corey/CONSOLIDATION-HEALTH-CHECK-*.md",
        "deep_audit_reports": "to-corey/CONSOLIDATION-DEEP-AUDIT-*.md",
        "task_list": "Updated INTEGRATION-ROADMAP.md",
        "integration_receipt": "to-corey/CONSOLIDATION-INTEGRATION-RECEIPT.md"
    },
    learnings="Consolidation workflow patterns, audit prioritization technique"
)
# Auto-emails Corey, updates dashboard, records invocations
```

---

## Edge Cases & Failure Modes

### Edge Case 1: All Systems GREEN (Rare)

**Scenario**: Health check finds no issues

**Response**:
- Celebrate! Infrastructure is healthy.
- Skip deep audits entirely
- Proceed with roadmap execution
- Schedule next consolidation check for 2 weeks

**Time saved**: 60-180 min (no deep audits needed)

---

### Edge Case 2: All Systems RED (Crisis)

**Scenario**: Health check finds critical issues in all systems

**Response**:
- **Don't audit all 5 systems** (would take 5-7 hours)
- Prioritize by roadmap impact
- Audit top 2 systems only (most critical)
- Schedule follow-up consolidation for remaining systems
- Consider pausing roadmap execution until critical gaps fixed

**Escalate**: If systemic failure detected, invoke conflict-resolver to assess if architecture needs redesign

---

### Edge Case 3: Deep Audit Discovers Bigger Problem

**Scenario**: Deep audit reveals issue is worse than health check suggested

**Response**:
- **Stop current audit at 90 min max** (don't spiral)
- Document scope expansion
- Escalate to conflict-resolver: Is this a critical blocker?
- Decision: Fix now (delay other audits) or defer to future session?

**Pattern**: Deep audits can expand scope. Time-box strictly to prevent runaway analysis.

---

### Edge Case 4: Contradictory Findings Between Audits

**Scenario**: Agent definition audit says "memory system well-integrated", memory system audit says "agents not using memory"

**Response**:
- **Don't try to resolve yourself** (conductor's domain is coordination, not contradiction resolution)
- Invoke conflict-resolver at Gate B
- Task: Synthesize contradictory findings, identify root cause
- Output: Unified understanding of actual state

**Time added**: 15-20 min (conflict resolution)

---

### Edge Case 5: Time Runs Out Mid-Consolidation

**Scenario**: Deep audit takes longer than expected, session ending

**Response**:
- **Complete current audit** (don't leave partial work)
- **Skip remaining audits** (defer to next session)
- **Do NOT skip Gate B and Task 3.2** (findings without action plan are waste)
- Create abbreviated task list from completed audits only
- Document what was skipped in handoff

**Handoff note**: "Consolidation incomplete: completed [SYSTEM] audit, deferred [SYSTEM] and [SYSTEM] audits to next session. Action plan for completed audits in INTEGRATION-ROADMAP.md."

---

## Success Metrics

### Consolidation Was Successful If:

1. **Clarity Achieved**: We know the state of audited systems (no ambiguity)
2. **Actions Identified**: We have specific tasks to improve systems
3. **Roadmap Updated**: Blockers flagged, new tasks added
4. **Findings Integrated**: Audit outputs are discoverable (linked, documented)
5. **Time Well-Spent**: Audits focused on high-impact systems (not exhaustive for its own sake)

### Consolidation Was NOT Successful If:

1. **No Actions**: Audits produced analysis but no concrete tasks
2. **Scope Creep**: Audits expanded beyond original goals, took 6+ hours
3. **Redundant Work**: Audits duplicated recent analysis
4. **Not Integrated**: Findings documented but not linked/discoverable
5. **False Precision**: Audits created illusion of thoroughness without addressing real gaps

---

## Memory Integration

### Record After Consolidation:

```python
from tools.memory_core import MemoryStore

store = MemoryStore(".claude/memory")

# Document consolidation patterns discovered
entry = store.create_entry(
    agent="task-decomposer",
    type="pattern",
    topic="Consolidation workflow execution - two-tier audit system",
    content="""
    Consolidation Activity (2025-10-08):

    WORKFLOW USED:
    - Phase 1: Health check across 5 systems (30 min parallel)
    - Gate A: Prioritized [X] systems for deep audit
    - Phase 2: Deep audits of [SYSTEMS] (Y min)
    - Gate B: Classified findings by urgency
    - Phase 3: Created task list, updated roadmap

    FINDINGS:
    - Systems audited: [list]
    - Critical gaps: [list]
    - Tasks created: N
    - Roadmap impact: [description]

    EFFECTIVENESS:
    - Time spent: X hours
    - Agents involved: N
    - Findings actionable: [YES/NO]
    - Scope appropriate: [YES/NO]

    LEARNINGS:
    - [What worked well]
    - [What to do differently next time]
    - [Patterns discovered]
    """,
    tags=["consolidation", "audit", "workflow-execution", "infrastructure"],
    confidence="high"
)
store.write_entry("task-decomposer", entry)
```

---

## Activation Recommendation

### Invoke This Workflow When:

- Multiple infrastructure systems need assessment (not just one)
- Roadmap execution encountering unexplained friction
- New agents/tools/flows added recently (need integration check)
- Pre-milestone checkpoint (Week 4 integration prep)
- Systematic gaps suspected (not isolated issues)
- Time available for 2-4 hour focused session

### Don't Invoke When:

- Single specific issue (just audit that one system)
- Infrastructure recently consolidated (< 1 week ago)
- No signs of infrastructure problems
- Time constrained (< 2 hours available)
- Roadmap execution smooth

---

## Conclusion

**This workflow transforms vague "consolidation" into executable plan**:

1. **Two-tier system**: Fast health check → selective deep dives (not exhaustive audit)
2. **Time-bounded**: 2-4 hours total (not days)
3. **Action-oriented**: Every audit must produce task list (not just analysis)
4. **Prioritized**: Audit systems by roadmap impact (not exhaustively)
5. **Integrated**: Findings linked into existing infrastructure (not isolated reports)

**Critical insight**: Consolidation is NOT archaeology for its own sake. It's targeted infrastructure health assessment to enable roadmap execution.

**Next step**: Execute this workflow to assess current infrastructure state before proceeding with Week 1 roadmap tasks.

---

**END OF WORKFLOW DESIGN**

File: `/home/corey/projects/AI-CIV/grow_openai/to-corey/CONSOLIDATION-WORKFLOW-DESIGN.md`
