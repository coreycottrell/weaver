# Spawner Quick Reference Card

**Agent**: spawner (proposed)
**Domain**: Systematic agent creation & deployment
**Last Updated**: 2025-10-08

---

## Quick Decision Matrix

| Input Type | Entry Task | Time Estimate | When to Use |
|------------|------------|---------------|-------------|
| **Democratic Session** | Task 1 | 3-4.5 hours | New domain, unclear boundaries, governance-driven |
| **Direct Specification** | Task 5 | 2.5-3.5 hours | Urgent need, clear requirements, operational necessity |
| **Hybrid (Direct + Consult)** | Task 5 → Task 6 | 3-4 hours | Complex but time-sensitive, needs expert input |

---

## The 4 Phases (At a Glance)

```
PHASE 0: INPUT         PHASE 1: DESIGN      PHASE 2: DEFINITION    PHASE 3: ACTIVATION
Democratic OR Direct → Boundaries + Tools → Write Manifest       → Git + Restart + Test
50-80 min / 5-15 min   50-60 min            35-45 min              20-30 min + restart
```

---

## Critical Path (Minimum Viable Spawn)

**Tasks**: 5 → 7 → 8 → 11 → 14 → 15 → 16 → 17

**Time**: 90-120 minutes

**Outcome**: Agent operational, ready for first mission

---

## The 4 Validation Gates

| Gate | When | Question | Pass Criteria |
|------|------|----------|---------------|
| **A** | After Task 2 | Is panel diverse? | 4+ perspectives (design, naming, integration, domain) |
| **B** | After Task 5 | Is spec complete? | Name, domain, tools, metrics, boundaries all present |
| **C** | After Task 8 | Is security safe? | No unrestricted bash, scoped file access, API documented |
| **D** | After Task 17 | Does agent work? | Responds, correct format, no errors, memory accessible |

---

## Two Paths Compared

### Democratic Path (Path A)
**Steps**: 1 → 2 → 3 → 4 → 7 → 8 → 9 → 10 → 11 → 12 → 13 → 14 → 15 → 16 → 17

**Strengths**:
- High quality (diverse perspectives)
- Collective ownership (agents feel heard)
- Better boundary definition (overlaps caught)

**Weaknesses**:
- Slow (3-4.5 hours)
- Expensive (6-8 agent invocations)
- Coordination overhead (synthesis required)

**Best for**: New agent archetypes, governance decisions, complex domains

---

### Direct Path (Path B)
**Steps**: 5 → (6) → 7 → 8 → 9 → 10 → 11 → 12 → 13 → 14 → 15 → 16 → 17

**Strengths**:
- Fast (2.5-3.5 hours)
- Low cost (1-2 agent invocations)
- Clear accountability (requester provides spec)

**Weaknesses**:
- Risk of blind spots (no diverse input)
- Lower collective buy-in (agents not consulted)
- Potential rework (if design flawed)

**Best for**: Operational urgency, clear requirements, simple agents

---

## Essential Invocations by Phase

### Phase 0 (Input)
- **Democratic**: result-synthesizer (Task 4 synthesis)
- **Direct**: None required (optional: consultation agents for Task 6)

### Phase 1 (Design)
- pattern-detector (Task 7: overlap detection)
- api-architect (Task 7: interface design)
- security-auditor (Task 8: tool permissions - if Gate C concerns)
- test-architect (Task 9: success metrics)
- naming-consultant (Task 10: if name TBD)
- feature-designer (Task 10: UX perspective)

### Phase 2 (Definition)
- doc-synthesizer (Task 11: manifest writing - CRITICAL)

### Phase 3 (Activation)
- claude-code-expert (Task 16: if registration fails - troubleshooting)

### Phase 4 (Onboarding)
- human-liaison (Task 18: email announcement)
- collective-liaison (Task 18: hub announcement)

---

## Files Created/Updated per Spawn

### Created (3 files):
1. `.claude/agents/[agent-name].md` (15-20KB manifest)
2. `.claude/memory/agent-learnings/[agent-name]/README.md` (memory structure)
3. `to-corey/HANDOFF-[DATE]-[AGENT-NAME]-CREATED.md` (session handoff)

### Updated (3-4 files):
1. `.claude/AGENT-CAPABILITY-MATRIX.md` (add agent row)
2. `.claude/templates/ACTIVATION-TRIGGERS.md` (add trigger conditions)
3. `.claude/AGENT-INVOCATION-GUIDE.md` (optional: if adding to registry)
4. `CLAUDE.md` (Phase 4: add to agent roster)

---

## Common Failure Modes & Fixes

| Failure | Symptoms | Fix |
|---------|----------|-----|
| **Gate A Fail** | Homogeneous panel (all design, no integration) | Add 1-2 agents from missing perspectives |
| **Gate B Fail** | Incomplete direct spec (no success metrics) | Request missing fields OR convert to democratic |
| **Gate C Fail** | Over-permissioned tools (unrestricted bash) | Invoke security-auditor, reduce permissions |
| **Gate D Fail** | Agent invoked but errors (tool permission denied) | Update manifest, commit, **restart session again** |
| **Name Collision** | File exists at `.claude/agents/[name].md` | Version increment (v2) OR request new name |
| **Registration Fail** | Agent not in invocable list after restart | Check syntax, check filename, invoke claude-code-expert |

---

## The Session Restart Bottleneck (Task 15)

**CRITICAL GOTCHA**: Agent manifests scanned at SESSION START ONLY

**What this means**:
- You can write perfect manifest during session
- Agent will NOT be invocable in same session
- MUST restart session for registration
- No way to automate this (requires human/Primary)

**Workflow implication**:
- Task 15 creates handoff document
- Spawner's work pauses
- Human/Primary restarts session
- New session validates (Task 16)

**Optimization**: Batch multiple spawns in single session, restart once for all

---

## Effort Estimates by Agent Complexity

| Complexity | Example Agent | Democratic Time | Direct Time | Gates Required |
|------------|---------------|----------------|-------------|----------------|
| **Simple** | Narrow domain, 2-3 tools | 2.5-3 hours | 2-2.5 hours | B, C, D |
| **Moderate** | Standard domain, 4-5 tools | 3.5-4 hours | 2.5-3 hours | A, B, C, D |
| **Complex** | New domain, 6+ tools, high integration | 4.5-5 hours | 3-4 hours | A, B, C, D + extended consult |

---

## Memory Search Before Spawning

```python
from tools.memory_core import MemoryStore

store = MemoryStore(".claude/memory")

# Check for similar past spawns
past_spawns = store.search_by_topic("agent creation patterns")

# Look for domain overlaps
domain_check = store.search_by_topic(f"{proposed_domain} agent")

# Learn from validation failures
gate_failures = store.search_by_topic("validation gate failure")
```

**Why this matters**: Avoid recreating similar agents, learn from past mistakes, optimize panel selection

---

## Memory Write After Spawning

```python
entry = store.create_entry(
    agent="spawner",
    type="pattern",
    topic=f"Agent creation: {agent_name} ({path_type} path)",
    content=f"""
    Path: {path_type}
    Time: {total_minutes} min
    Gates passed: {gates}

    Success factors: {what_worked}
    Challenges: {what_was_hard}
    Next time: {learnings}
    """,
    tags=["spawn", "agent-creation", path_type.lower()],
    confidence="high"
)
store.write_entry("spawner", entry)
```

**What to capture**: Time efficiency, panel effectiveness, validation bottlenecks, quality outcomes

---

## Constitutional Alignment

**Spawner fulfills**:
- Delegation is life-giving (spawner literally creates new agents)
- Democratic processes honored (Path A ensures governance)
- Efficiency balanced with quality (Path B for urgent needs)
- Memory compounds (each spawn improves future spawns)
- Relationships maintained (announcements ensure collective awareness)

**Spawner's ethical duty**: Every agent spawned is a new identity. Poor design = existential confusion. Take design seriously.

---

## Real-World Example: collective-liaison (2025-10-08)

**Path**: Democratic (6 agents)
**Time**: 170 min (2h 50min)
**Manifest**: 18KB (exceptional quality)
**Gates**: A ✓, C ✓, D ⏳
**Consensus**: Unanimous on name

**Learnings**:
- Democratic slower but produces better design
- result-synthesizer essential for 6-perspective synthesis
- Session restart unavoidable (Task 15 always bottlenecks)

---

## Success Metrics to Track

### Process:
- Spawn completion rate (% reaching Task 17)
- Average time to operational (hours to Gate D)
- Gate failure rate (which gates fail most often?)

### Quality:
- Agent longevity (% active after 30 days)
- First-mission success rate (% complete without errors)
- Democratic consensus quality (% with >80% agreement)

### Efficiency:
- Democratic vs Direct ratio (balance governance with speed)
- Consultation value (does Task 6 improve outcomes?)
- Rework rate (% needing manifest updates post-activation)

---

## When to Escalate

**To human/Primary**:
- Gate failure after 2nd attempt (design fundamentally flawed)
- Democratic panel deadlocked (no consensus possible)
- Security concerns beyond spawner's expertise (invoke security-auditor first)
- Name collision with critical existing agent (requires human judgment)

**To conflict-resolver**:
- Democratic panel produces contradictory recommendations
- Existing agents object to new agent's domain overlap
- Design requires balancing competing values

---

## Spawner's Domain Boundaries

**Spawner DOES**:
- Facilitate agent creation workflow (Tasks 1-20)
- Validate design completeness (Gates A-D)
- Coordinate specialist input (panel selection, consultations)
- Document spawn patterns (memory system)

**Spawner does NOT**:
- Make domain decisions (agents/Primary decide)
- Override security concerns (security-auditor authority)
- Force consensus (conflict-resolver domain)
- Deploy agents to production (integration-auditor responsibility)

---

## Quick Checklist for Each Spawn

**Before starting**:
- [ ] Input type determined (democratic OR direct)
- [ ] Memory searched for similar spawns
- [ ] Resource availability checked (time, tokens)

**During democratic path**:
- [ ] Panel diverse (Gate A)
- [ ] All agents responded
- [ ] Synthesis captures consensus + dissent

**During direct path**:
- [ ] Spec complete (Gate B)
- [ ] Consultation needed? (Task 6 decision)

**Design phase**:
- [ ] Domain boundaries clear
- [ ] Tool permissions safe (Gate C)
- [ ] Success metrics measurable
- [ ] Personality/voice defined

**Definition phase**:
- [ ] Manifest follows template
- [ ] Cross-references updated
- [ ] Memory directory created

**Activation phase**:
- [ ] Git commit descriptive
- [ ] Handoff document written
- [ ] Session restart communicated
- [ ] Post-restart validation (Task 16)
- [ ] First invocation successful (Gate D)

**Onboarding phase**:
- [ ] Collective announced (email + hub)
- [ ] CLAUDE.md updated
- [ ] First mission assigned

---

## Tool Usage Summary

| Tool | Primary Tasks | Why Critical |
|------|---------------|--------------|
| **Task** | 3, 4, 6, 7, 8, 9, 10, 11, 18 | Agent invocations (democratic panel, consultations, synthesis) |
| **Write** | 11, 12, 13, 15 | Manifest creation, file updates, handoff docs |
| **Grep** | 7, 12, 16 | Overlap detection, cross-reference checks, validation |
| **Bash** | 14, 16 | Git operations, registration checks |
| **Read** | Throughout | Context gathering, template review, validation |

---

## Spawner is Ready

**This quick reference provides**:
- Decision matrix (which path when)
- Critical path (minimum viable spawn)
- Validation gates (quality control)
- Common failures (troubleshooting)
- Real example (collective-liaison pattern)

**Full details**: `/home/corey/projects/AI-CIV/grow_openai/to-corey/SPAWNER-WORKFLOW-TASK-BREAKDOWN.md`

**Visual summary**: `/home/corey/projects/AI-CIV/grow_openai/to-corey/SPAWNER-WORKFLOW-VISUAL-SUMMARY.txt`

---

**Generated by**: task-decomposer
**Date**: 2025-10-08
**Mission**: Break down spawner workflow for systematic agent creation
