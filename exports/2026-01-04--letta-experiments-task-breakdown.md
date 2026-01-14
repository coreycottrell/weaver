# Letta Experiments Task Breakdown

**Agent**: task-decomposer
**Domain**: Task Planning & Decomposition
**Date**: 2026-01-04

---

## High-Level Goal

Experiment with 3 Letta-inspired concepts to evolve WEAVER's agent capabilities:
1. Sleep-time compute (memory consolidation during idle)
2. Memory omni-tool (agents actively manage their own memory)
3. Agent file integration (serializable agent state)

---

## Experiment 1: Sleep-Time Compute

### Concept
Agents process/consolidate memories during idle periods (overnight, between sessions). Memory consolidation, pattern detection, self-improvement run without human supervision.

### Minimum Viable Experiment (1-2 hours)

**Task 1.1: Night-Watch Memory Consolidation Script**
- **Effort**: 45 min
- **Description**: Create a standalone script that runs during night-watch that:
  - Scans all agent memory files from the past 7 days
  - Identifies themes/patterns across memories
  - Writes a synthesis file to `sandbox/consolidations/`
- **Files to create**: `sandbox/prototypes/sleep_consolidate.py`
- **Dependencies**: None (uses existing `memory_core.py`)
- **Success criteria**:
  - Script runs without error
  - Produces readable synthesis with 3+ identified patterns
  - Takes < 30 seconds to execute

**Task 1.2: Integrate with Night-Watch Protocol**
- **Effort**: 30 min
- **Description**: Add consolidation step to night-watch skill
- **Files to modify**: `.claude/skills/night-watch/SKILL.md` (add consolidation phase)
- **Dependencies**: Task 1.1 complete
- **Success criteria**:
  - Night-watch protocol includes memory consolidation step
  - Clear documentation on when/how consolidation runs

**Task 1.3: Test One Consolidation Cycle**
- **Effort**: 30 min
- **Description**: Run the consolidation manually, review output quality
- **Dependencies**: Tasks 1.1 and 1.2 complete
- **Success criteria**:
  - Consolidation produces useful insights
  - No false patterns or hallucinations detected
  - Output is human-readable and actionable

### What We Learn
- Whether pattern detection on unstructured memories produces value
- Optimal frequency for consolidation (daily? weekly?)
- Memory volume thresholds for useful consolidation
- Quality of emergent patterns vs noise

### Blockers/Risks
- Memory files may be too sparse for meaningful patterns (WEAVER is young)
- LLM-based pattern detection could hallucinate connections
- Mitigation: Start with human review of all consolidation outputs

---

## Experiment 2: Memory Omni-Tool

### Concept
Agents actively manage their own memory - not just read, but replace, edit, and decide what to remember. Currently agents read memory but Conductor writes. Enable autonomous memory curation.

### Minimum Viable Experiment (1.5-2 hours)

**Task 2.1: Design Agent Memory API Extension**
- **Effort**: 30 min
- **Description**: Design API additions to `memory_core.py`:
  - `memory_replace(old_entry, new_entry)` - Update existing memory
  - `memory_deprecate(entry, reason)` - Mark memory as outdated
  - `decide_importance(entry) -> float` - Score memory importance
- **Files to modify**: Design doc only (`sandbox/prototypes/memory-api-design.md`)
- **Dependencies**: None
- **Success criteria**:
  - Clear API spec with function signatures
  - Edge cases identified (what if entry doesn't exist?)
  - Access control model defined (can agents edit others' memories?)

**Task 2.2: Implement memory_replace**
- **Effort**: 30 min
- **Description**: Add memory replacement function to `memory_core.py`
  - Preserve old version in history
  - Update filename date if significant change
  - Maintain audit trail
- **Files to modify**: `tools/memory_core.py`
- **Dependencies**: Task 2.1 complete
- **Success criteria**:
  - Function works in isolation tests
  - Old memory preserved (not destroyed)
  - History trail visible

**Task 2.3: Test Agent Self-Memory Edit**
- **Effort**: 45 min
- **Description**: Have one agent (suggest: ai-psychologist) use new API to:
  - Read one of their old memories
  - Decide if it needs updating
  - Write an improved version using memory_replace
- **Dependencies**: Task 2.2 complete
- **Success criteria**:
  - Agent successfully edits own memory
  - Audit trail shows before/after
  - No corruption of memory system

**Task 2.4: Document Learnings**
- **Effort**: 15 min
- **Description**: Write up what worked, what didn't, recommendations
- **Files to create**: `sandbox/prototypes/memory-omni-learnings.md`
- **Dependencies**: Task 2.3 complete
- **Success criteria**:
  - Clear recommendation: proceed, iterate, or abandon
  - Identified risks and mitigations

### What We Learn
- Whether agents make good decisions about their own memory
- Risk of memory drift/degradation over time
- Value of memory versioning
- Trust model for agent self-modification

### Blockers/Risks
- Agents might "improve" memories in ways that lose valuable info
- Memory corruption risk if implementation is buggy
- Mitigation: Read-only backup of entire memory dir before experiment

---

## Experiment 3: Agent File Integration

### Concept
Serializable agent state with memory. Checkpoint/restore agent state. Version control agent evolution. Think: "save game" for agent development state.

### Minimum Viable Experiment (1-2 hours)

**Task 3.1: Define Agent State Schema**
- **Effort**: 30 min
- **Description**: Design what constitutes "agent state" for serialization:
  - Agent manifest (from `.claude/agents/{name}.md`)
  - Agent memories (from `.claude/memory/agent-learnings/{name}/`)
  - Invocation count / experience level
  - Skills granted
  - Last active date
- **Files to create**: `sandbox/prototypes/agent-state-schema.md`
- **Dependencies**: None
- **Success criteria**:
  - Complete list of state components
  - JSON/YAML schema defined
  - Size estimate (how big is one agent snapshot?)

**Task 3.2: Build Agent Snapshot Function**
- **Effort**: 45 min
- **Description**: Create function that exports agent to single file:
  - `snapshot_agent(agent_name) -> dict`
  - Gathers all state components
  - Produces JSON file with all agent data
- **Files to create**: `sandbox/prototypes/agent_snapshot.py`
- **Dependencies**: Task 3.1 complete
- **Success criteria**:
  - Function produces valid JSON
  - All state components captured
  - File size reasonable (< 1MB per agent)

**Task 3.3: Build Agent Restore Function**
- **Effort**: 30 min
- **Description**: Create function that restores agent from snapshot:
  - `restore_agent(snapshot_path) -> bool`
  - Writes manifest and memories to correct locations
  - Handles conflicts (agent already exists)
- **Files to modify**: `sandbox/prototypes/agent_snapshot.py`
- **Dependencies**: Task 3.2 complete
- **Success criteria**:
  - Restore produces identical state to snapshot
  - Conflicts handled gracefully (rename or merge)
  - Dry-run mode available

**Task 3.4: Round-Trip Test**
- **Effort**: 15 min
- **Description**: Snapshot an agent, modify their state, restore, verify original state returned
- **Dependencies**: Tasks 3.2 and 3.3 complete
- **Success criteria**:
  - Agent state identical before/after round-trip
  - No data loss or corruption
  - Performance acceptable (< 10 sec per agent)

### What We Learn
- Whether agent state is fully capturable
- Size/complexity of agent snapshots
- Feasibility of "agent version control" (git for agents)
- Foundation for agent reproduction/lineage

### Blockers/Risks
- Agent state may have hidden components not captured
- Memory file references may break on restore
- Mitigation: Start with one agent, expand if successful

---

## Dependencies Diagram

```
Experiment 1 (Sleep-Time)     Experiment 2 (Omni-Tool)     Experiment 3 (Agent Files)
          |                            |                            |
      [1.1] ─────────────────────────────────────────────────────────────
          |                            |                            |
      [1.2] ←──── depends on ←──── [1.1]                       [3.1]
          |                            |                            |
      [1.3]                        [2.1]                        [3.2]
                                       |                            |
                                   [2.2]                        [3.3]
                                       |                            |
                                   [2.3]                        [3.4]
                                       |
                                   [2.4]
```

**No cross-experiment dependencies** - all three can run in parallel.

---

## Parallel Opportunities

| Can Run Together | Notes |
|-----------------|-------|
| 1.1 + 2.1 + 3.1 | All are design/planning tasks |
| 1.2 + 2.2 + 3.2 | All are implementation (different files) |
| 1.3 + 2.3 + 3.4 | All are testing/validation |

**Maximum parallelism**: 3 experiments running simultaneously
**Minimum sequential path**: Design -> Implement -> Test (3 phases)

---

## Critical Path

**Longest dependency chain**: Experiment 2 (4 tasks sequential)
- Task 2.1 (30 min) -> Task 2.2 (30 min) -> Task 2.3 (45 min) -> Task 2.4 (15 min)
- Total: 2 hours

**If doing sequentially all experiments**: ~5-6 hours total
**If maximum parallelism**: ~2 hours (limited by Experiment 2 critical path)

---

## Effort Summary

| Experiment | Tasks | Total Effort | Complexity |
|------------|-------|--------------|------------|
| Sleep-Time Compute | 3 | 1.75 hours | Medium |
| Memory Omni-Tool | 4 | 2 hours | High |
| Agent File Integration | 4 | 2 hours | Medium |
| **Combined** | **11** | **5.75 hours** | - |

---

## Recommended Execution Order

**If limited time (2 hours available)**:
1. Experiment 3 (Agent Files) - Most foundational, enables future work

**If medium time (4 hours available)**:
1. Experiment 3 (Agent Files)
2. Experiment 1 (Sleep-Time) - Integrates with existing night-watch

**If full time available**:
1. Start all three in parallel at design phase
2. Converge at implementation
3. Test together

---

## Success Criteria Summary

| Experiment | Key Success Indicator |
|------------|----------------------|
| Sleep-Time | Produces 3+ meaningful patterns from memory |
| Omni-Tool | Agent successfully self-edits memory without data loss |
| Agent Files | Round-trip snapshot/restore is lossless |

---

## Risk Register

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| Memory corruption | Medium | High | Backup before experiment |
| Pattern hallucination | Medium | Low | Human review all outputs |
| Agent state incomplete | Low | Medium | Start with one agent |
| Performance issues | Low | Low | Test on small dataset first |

---

## Next Actions

1. **Choose which experiment(s) to start**
2. **Back up memory directory** (`cp -r .claude/memory .claude/memory-backup-2026-01-04`)
3. **Begin Task X.1** (design phase of chosen experiment)
4. **Document as you go** (sandbox/prototypes/)

---

*Decomposition complete. Ready for execution.*
