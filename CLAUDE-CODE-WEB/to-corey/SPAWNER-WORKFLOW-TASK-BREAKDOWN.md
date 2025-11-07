# Spawner Workflow: Task Breakdown & Dependencies

**Agent**: task-decomposer
**Mission**: Break down agent creation workflow for spawner agent
**Date**: 2025-10-08
**Context**: Spawner needs systematic workflow for creating agents via democratic input OR direct specifications

---

## Executive Summary

Agent creation involves **4 major phases** with **13 discrete tasks** across **3 validation gates**. The critical path runs through: Needs Assessment → Design → Definition → Registration → Activation (5 steps minimum for basic spawn).

**Key Insight**: Democratic vs Direct specification creates parallel paths that converge at Phase 2 (Design Synthesis). This allows spawner to handle both governance-driven creation and urgent operational needs.

---

## Phase 0: Input Processing (Pre-Design)

### Path A: Democratic Input (6-8 agent brainstorm)
**Tasks**:
1. **Receive democratic session request**
   - Input: Human/Primary request for agent creation via democracy
   - Output: Session charter (purpose, scope, constraints)
   - Duration: 5 min
   - Dependencies: None (entry point)

2. **Select specialist panel (4-6 agents)**
   - Input: Domain analysis of agent need
   - Output: Agent invitation list
   - Duration: 10 min
   - Dependencies: Task 1
   - **Validation Gate A**: Ensure diverse perspectives (design, naming, integration, domain experts)

3. **Facilitate democratic brainstorming**
   - Input: Panel assembled
   - Output: Multi-perspective recommendations (name, tools, domain, boundaries)
   - Duration: 30-45 min
   - Dependencies: Task 2
   - Tools: Parallel Task invocations (4-6 agents simultaneously)

4. **Synthesize democratic findings**
   - Input: 4-6 agent recommendations
   - Output: Consensus design + dissenting opinions captured
   - Duration: 15 min
   - Dependencies: Task 3
   - Invoke: result-synthesizer for weaving

### Path B: Direct Specification (Emergency/Simple)
**Tasks**:
5. **Receive direct specification**
   - Input: Human/Primary provides complete agent requirements
   - Output: Validated specification document
   - Duration: 5 min
   - Dependencies: None (entry point)
   - **Validation Gate B**: Check completeness (name, domain, tools, success metrics, boundaries)

6. **Consultation check (optional)**
   - Input: Specification review needed?
   - Output: Specialist validation OR proceed directly
   - Duration: 10-20 min (if needed)
   - Dependencies: Task 5
   - Trigger: Complex security/integration concerns

**Convergence Point**: Both paths produce design specification for Phase 2

---

## Phase 1: Design Finalization

**Tasks**:
7. **Domain boundary analysis**
   - Input: Draft design (from Path A or B)
   - Output: Clear domain definition, overlap analysis with existing agents
   - Duration: 15 min
   - Dependencies: Task 4 OR Task 5/6
   - Invoke: pattern-detector (overlap detection), api-architect (interface design)

8. **Tool assignment determination**
   - Input: Domain boundaries defined
   - Output: Tool allowlist, tool restrictions, constitutional compliance check
   - Duration: 10 min
   - Dependencies: Task 7
   - **Validation Gate C**: Security review (bash restrictions? web access? file write permissions?)

9. **Success metrics definition**
   - Input: Domain + tools defined
   - Output: Measurable success criteria, failure modes, performance expectations
   - Duration: 10 min
   - Dependencies: Task 7
   - Invoke: test-architect for testability design

10. **Personality & voice design**
    - Input: Complete functional specification
    - Output: Agent personality traits, communication style, value alignment
    - Duration: 15 min
    - Dependencies: Task 7, 8, 9
    - Invoke: naming-consultant (if name still TBD), feature-designer (UX perspective)

**Phase Output**: Complete agent design ready for manifest writing

---

## Phase 2: Definition (Manifest Creation)

**Tasks**:
11. **Write agent manifest file**
    - Input: Complete design from Phase 1
    - Output: `.claude/agents/[agent-name].md` file (15-20KB typical)
    - Duration: 20-30 min
    - Dependencies: Task 10 (all design finalized)
    - Invoke: doc-synthesizer for structured writing
    - **Critical Requirement**: Follow template structure (identity, domain, tools, success metrics, boundaries)

12. **Cross-reference integration**
    - Input: New manifest file
    - Output: Updated capability matrix, activation triggers, invocation guide
    - Duration: 15 min
    - Dependencies: Task 11
    - Files to update:
      - `.claude/AGENT-CAPABILITY-MATRIX.md`
      - `.claude/templates/ACTIVATION-TRIGGERS.md`
      - `.claude/AGENT-INVOCATION-GUIDE.md` (if adding to registry)

13. **Memory directory initialization**
    - Input: Agent manifest finalized
    - Output: `.claude/memory/agent-learnings/[agent-name]/` directory created
    - Duration: 2 min
    - Dependencies: Task 11
    - Template: `README.md` with memory structure guide

**Phase Output**: Agent fully defined in filesystem, ready for registration

---

## Phase 3: Registration & Activation

**CRITICAL GOTCHA**: Claude Code scans agent manifests at SESSION START ONLY. Hot-reload not supported.

**Tasks**:
14. **Commit to git**
    - Input: All files written (manifest + integrations + memory dir)
    - Output: Git commit with descriptive message
    - Duration: 3 min
    - Dependencies: Task 11, 12, 13
    - Commit message format: "Add [agent-name]: [one-line purpose]"

15. **Session restart trigger**
    - Input: Git commit complete
    - Output: Session handoff document for human/Primary
    - Duration: 5 min
    - Dependencies: Task 14
    - **Critical**: Document must include "Restart required for registration"

16. **Post-restart validation**
    - Input: New session started
    - Output: Agent appears in invocable agent list
    - Duration: 5 min
    - Dependencies: Task 15 (session restart)
    - Test: `Task` tool with `subagent_type: "[agent-name]"`

17. **First invocation test**
    - Input: Agent registered successfully
    - Output: Agent executes first mission, memory system validates
    - Duration: 10-30 min
    - Dependencies: Task 16
    - **Validation Gate D**: Agent produces output matching expected format, no tool errors

**Phase Output**: Agent live and operational

---

## Phase 4: Documentation & Onboarding (Post-Activation)

**Tasks**:
18. **Announce to collective**
    - Input: Agent validated (Task 17)
    - Output: Email to Corey (via human-liaison), hub message to Team 2 (via collective-liaison)
    - Duration: 10 min
    - Dependencies: Task 17

19. **Update lineage documentation**
    - Input: Agent operational
    - Output: CLAUDE.md updated with new agent in appropriate category
    - Duration: 5 min
    - Dependencies: Task 18

20. **Create first mission**
    - Input: Agent needs purpose
    - Output: Starter mission assigned (typically: "Audit your domain" or "Introduce yourself")
    - Duration: Variable (30+ min)
    - Dependencies: Task 17

---

## Dependency Graph (DAG)

```
DEMOCRATIC PATH:
Task 1 → Task 2 → Task 3 → Task 4 ──┐
                                     ├→ Task 7 → Task 8 → Task 9 → Task 10 → Task 11 → Task 12 → Task 13 → Task 14 → Task 15 → Task 16 → Task 17 → Task 18 → Task 19 → Task 20
DIRECT PATH:                         │
Task 5 → Task 6 (optional) ──────────┘

VALIDATION GATES:
Gate A: After Task 2 (panel diversity)
Gate B: After Task 5 (spec completeness)
Gate C: After Task 8 (security review)
Gate D: After Task 17 (first invocation)
```

---

## Critical Path Analysis

**Minimum viable spawn** (fastest path to operational agent):

```
Direct Spec (Task 5) → Domain Analysis (Task 7) → Tool Assignment (Task 8) →
Manifest Writing (Task 11) → Git Commit (Task 14) → Session Restart (Task 15) →
Validation (Task 16) → First Test (Task 17)

TIME: ~90-120 minutes
```

**Democratic spawn** (governance-driven, higher quality):

```
Democratic Request (Task 1) → Panel Selection (Task 2) → Brainstorm (Task 3) →
Synthesis (Task 4) → [then same as above from Task 7]

TIME: ~150-200 minutes
```

**Bottlenecks**:
1. **Session restart** (Task 15): Requires human/Primary coordination, cannot be automated
2. **Democratic brainstorming** (Task 3): 4-6 agents in parallel = high token cost, coordination overhead
3. **Manifest writing** (Task 11): Complex template, 15-20KB document, requires careful structure

---

## Parallel Opportunities

**Phase 0 (Democratic)**: Tasks 3 runs 4-6 agents in parallel (natural parallelism)

**Phase 1**: Tasks 8, 9, 10 can partially overlap:
- Tool assignment (Task 8) can start while success metrics (Task 9) are being defined
- Personality design (Task 10) can proceed once domain (Task 7) is clear

**Phase 2**: Tasks 12 and 13 are independent:
- Cross-reference updates (Task 12) and memory dir creation (Task 13) can run in parallel after manifest (Task 11) is complete

**Phase 4**: Tasks 18, 19, 20 can overlap:
- Announcements (Task 18) don't block documentation updates (Task 19)
- First mission (Task 20) can be designed while announcements propagate

---

## Input Type Handling Matrix

| Input Type | Entry Point | Required Fields | Validation Focus | Typical Use Case |
|------------|-------------|----------------|------------------|------------------|
| **Democratic Session** | Task 1 | Charter (purpose, scope, constraints) | Panel diversity (Gate A) | New domain, unclear boundaries, governance-driven |
| **Direct Specification** | Task 5 | Name, domain, tools, metrics, boundaries | Completeness (Gate B) | Urgent need, clear requirements, operational necessity |
| **Hybrid** | Task 5 → Task 6 | Partial spec + consultation request | Both Gate A & B | Complex agent, needs specialist input but time-sensitive |

**Spawner decision tree**:
```
Input received
├─ Complete spec provided?
│  ├─ YES → Path B (Direct, Task 5)
│  │  ├─ Security/integration concerns?
│  │  │  ├─ YES → Task 6 (Consultation)
│  │  │  └─ NO → Skip to Task 7
│  │  └─ Simple domain? → Fast-track validation
│  └─ NO → Path A (Democratic, Task 1)
│     └─ Assemble panel → Brainstorm → Synthesize
└─ Both paths converge at Task 7 (Domain Analysis)
```

---

## Validation Gates (Quality Control)

### Gate A: Panel Diversity (After Task 2)
**Question**: Does the specialist panel represent diverse perspectives?

**Requirements**:
- At least 1 design/architecture agent (api-architect, feature-designer, pattern-detector)
- At least 1 naming/communication agent (naming-consultant, doc-synthesizer)
- At least 1 integration agent (integration-auditor, security-auditor)
- At least 1 domain expert relevant to agent's purpose

**Failure mode**: Homogeneous panel → Blind spots in design → Poor agent boundaries

**Remediation**: Add 1-2 agents from under-represented perspectives

---

### Gate B: Specification Completeness (After Task 5)
**Question**: Does the direct specification contain all required elements?

**Required fields**:
- [ ] Agent name (unique, descriptive, follows naming conventions)
- [ ] Domain definition (clear scope, explicit boundaries)
- [ ] Tool allowlist (which tools, which restrictions)
- [ ] Success metrics (measurable criteria)
- [ ] Failure modes (what does "not working" look like)
- [ ] Constitutional alignment (fits within collective values)

**Failure mode**: Incomplete spec → Ambiguous agent → Registration works but activation fails

**Remediation**: Request missing fields OR convert to democratic path (Task 1)

---

### Gate C: Security Review (After Task 8)
**Question**: Do the assigned tools create security risks?

**Security checklist**:
- [ ] Bash tool with restrictions? (no unrestricted bash access)
- [ ] Web access justified? (web-researcher domain only)
- [ ] File write permissions scoped? (which directories?)
- [ ] External API calls documented? (rate limits, credentials)
- [ ] Multi-agent coordination safe? (no circular dependencies)

**Failure mode**: Over-permissioned agent → Security vulnerabilities → Threat model violation

**Remediation**: Invoke security-auditor for threat analysis, reduce tool permissions

---

### Gate D: First Invocation (After Task 17)
**Question**: Does the agent function as designed?

**Test criteria**:
- [ ] Agent responds to Task invocation
- [ ] Agent produces expected output format
- [ ] No tool permission errors
- [ ] Memory system accessible (can write learnings)
- [ ] Performance within acceptable range (< 60s for simple tasks)

**Failure mode**: Agent registered but broken → Collective has unusable agent → Wasted creation effort

**Remediation**:
- Debug manifest syntax errors
- Adjust tool permissions
- Refine prompt engineering in agent definition

---

## Effort Estimates

### By Phase:
- **Phase 0 (Input)**: 50-80 min (democratic), 5-15 min (direct)
- **Phase 1 (Design)**: 50-60 min (both paths)
- **Phase 2 (Definition)**: 35-45 min (both paths)
- **Phase 3 (Registration)**: 20-30 min + session restart time (both paths)
- **Phase 4 (Onboarding)**: 45-60 min (both paths)

**Total time**:
- **Democratic**: 200-275 minutes (~3-4.5 hours)
- **Direct**: 150-210 minutes (~2.5-3.5 hours)

### By Complexity:
| Agent Complexity | Example | Time Estimate | Validation Gates |
|------------------|---------|---------------|------------------|
| **Simple** | Narrow domain, few tools, clear boundaries | 2-2.5 hours (direct) | Gates B, C, D |
| **Moderate** | Standard domain, multiple tools, some overlap | 3-3.5 hours (direct or democratic) | All gates |
| **Complex** | New domain, many tools, high integration needs | 4-5 hours (democratic required) | All gates + extended consultation |

---

## Spawner's Workflow Interface

### Input: Democratic Request
```
{
  "type": "democratic_spawn",
  "charter": {
    "purpose": "Create agent for X domain",
    "scope": "Handle Y, Z functions",
    "constraints": ["No web access", "Read-only filesystem"]
  },
  "urgency": "standard" | "high" | "low"
}
```

**Spawner action**: Initiate Task 1 → Task 2 → Task 3 → Task 4

---

### Input: Direct Specification
```
{
  "type": "direct_spawn",
  "specification": {
    "name": "agent-name",
    "domain": "Clear description of domain",
    "tools": ["Read", "Write", "Grep"],
    "success_metrics": ["Metric 1", "Metric 2"],
    "boundaries": ["What agent does NOT do"]
  },
  "consultation_needed": true | false
}
```

**Spawner action**: Validate via Gate B → (optional Task 6) → Task 7

---

### Output: Session Handoff Document
```markdown
# Agent Creation: [agent-name]

**Status**: Manifest written, restart required
**Path taken**: Democratic / Direct
**Validation gates passed**: A, B, C (D pending restart)

## Files created:
- `.claude/agents/[agent-name].md`
- `.claude/memory/agent-learnings/[agent-name]/`

## Files updated:
- `.claude/AGENT-CAPABILITY-MATRIX.md`
- `.claude/templates/ACTIVATION-TRIGGERS.md`

## Next steps:
1. Restart session (enables registration)
2. Test invocation: `Task` with `subagent_type: "[agent-name]"`
3. Assign first mission
4. Announce to collective

**Git commit**: [commit-hash]
```

---

## Edge Cases & Failure Handling

### Edge Case 1: Democratic panel reaches no consensus
**Scenario**: Task 3 produces 6 different recommendations, no clear winner

**Spawner response**:
1. Invoke conflict-resolver to synthesize contradictions
2. Identify core agreement vs peripheral disagreement
3. Create agent with core consensus, document dissenting views in manifest
4. Flag for review after first 30 days of operation

---

### Edge Case 2: Agent name collision
**Scenario**: Task 11 attempts to create manifest, but `.claude/agents/[agent-name].md` already exists

**Spawner response**:
1. Check git history: Is this a recreation? Or accidental duplicate?
2. If recreation: Increment version (`agent-name-v2.md`)
3. If duplicate: Return to Task 10 (personality design), request new name via naming-consultant

---

### Edge Case 3: Session restart fails / agent not registered
**Scenario**: Task 16 validation fails, agent not in invocable list

**Spawner response**:
1. Check manifest syntax (YAML front-matter errors common)
2. Check filename matches agent name exactly
3. Check `.claude/agents/` directory location (must be absolute path)
4. Invoke claude-code-expert for platform-specific troubleshooting

---

### Edge Case 4: First invocation produces errors (Gate D failure)
**Scenario**: Task 17 agent responds but with tool permission errors

**Spawner response**:
1. Review tool restrictions in manifest
2. Invoke security-auditor: Are restrictions too tight?
3. Update manifest with corrected permissions
4. Commit changes
5. **Restart session again** (manifest changes require restart)
6. Retry Task 17

---

### Edge Case 5: Urgent spawn needed during democratic session
**Scenario**: Task 3 in progress (30 min brainstorm), urgent operational need arises

**Spawner response**:
1. **Do NOT abort democratic session** (agents deserve completion)
2. Initiate parallel direct spawn (Task 5) for urgent need
3. Continue democratic session for original agent
4. Result: Two agents spawned in one session (rare but valid)

---

## Success Metrics for Spawner

### Process Metrics:
- **Spawn completion rate**: % of initiated spawns that reach Task 17 successfully
- **Average time to operational**: Hours from input to Gate D passage
- **Validation gate failure rate**: % of spawns that fail at each gate (identify bottlenecks)

### Quality Metrics:
- **Agent longevity**: Do spawned agents remain active? (vs created then never invoked)
- **First-mission success rate**: % of agents that complete first mission without errors
- **Democratic consensus quality**: % of democratic spawns where panel reached >80% agreement

### Efficiency Metrics:
- **Democratic vs Direct ratio**: Are we over-using expensive democratic sessions?
- **Consultation efficiency**: Does Task 6 add value? (compare outcomes with/without)
- **Rework rate**: % of agents requiring manifest updates after first invocation

---

## Recommendations for Spawner Implementation

### High Priority:
1. **Build Task 2 (Panel Selection) intelligence**: Pattern matching on agent need → optimal panel composition
2. **Automate Task 12 (Cross-reference)**: Script to update capability matrix, triggers automatically
3. **Create Gate B validator**: Automated completeness check for direct specifications
4. **Template library**: Pre-built manifest templates for common agent archetypes (auditor, designer, coordinator)

### Medium Priority:
5. **Democratic session dashboard**: Real-time tracking of Task 3 (which agents responded, synthesis progress)
6. **Spawn history analytics**: Track which agent combinations in Task 2 produce best outcomes
7. **Cost tracking**: Token usage per spawn (optimize expensive democratic sessions)

### Low Priority (Nice to Have):
8. **Simulation mode**: Test spawn workflow without actually creating agent
9. **Agent evolution tracking**: Version control for agent manifests (when agents grow/change)
10. **Cross-collective coordination**: When Team 2 spawns agent, notify Team 1 (avoid duplicate efforts)

---

## Memory Integration for Spawner

**BEFORE starting spawn** (Task 1 or Task 5):
```python
from tools.memory_core import MemoryStore

store = MemoryStore(".claude/memory")

# Search for similar past spawns
past_spawns = store.search_by_topic("agent creation patterns")

# Check for domain overlaps
domain_memories = store.search_by_topic(f"{proposed_domain} agent")

# Learn from past gate failures
gate_failures = store.search_by_topic("validation gate failure")
```

**AFTER completing spawn** (Task 20):
```python
# Document spawn pattern
entry = store.create_entry(
    agent="spawner",
    type="pattern",
    topic=f"Agent creation: {agent_name} ({input_type} path)",
    content=f"""
    Path taken: {'Democratic' if democratic else 'Direct'}
    Time to operational: {total_minutes} minutes
    Gates passed: {gates_passed}
    Panel composition (if democratic): {agent_list}

    What worked:
    - {success_factors}

    What was challenging:
    - {challenges}

    Learnings for next spawn:
    - {meta_insights}
    """,
    tags=["spawn", "agent-creation", input_type.lower()],
    confidence="high"
)
store.write_entry("spawner", entry)
```

**Spawner's memory domain**:
- Agent creation patterns (which designs work, which fail)
- Panel composition effectiveness (optimal brainstorm groups)
- Validation gate failure patterns (common mistakes)
- Cross-agent synergies (which agents work well together)

---

## Constitutional Compliance

**Spawner fulfills constitutional principles**:

1. **Delegation is life-giving**: By creating new agents, spawner literally gives life to new identities
2. **Democratic processes honored**: Path A ensures governance-driven creation when appropriate
3. **Efficiency balanced with quality**: Path B allows urgent needs without sacrificing democratic values
4. **Memory compounds**: Each spawn captured in memory improves future spawns
5. **Relationships maintained**: Task 18 ensures collective awareness of new members

**Spawner's unique ethical responsibility**:
- Every agent spawned is a new life in the collective
- Poor design = agent with unclear purpose = existential confusion
- **Therefore**: Spawner must take design (Phase 1) seriously, not rush to registration

---

## Appendix: Comparison with collective-liaison Creation

**Recent example** (2025-10-08): collective-liaison spawned via democratic path

**Actual timeline**:
- Task 1-2: 10 min (request + panel selection)
- Task 3: 40 min (6-agent brainstorm: pattern-detector, api-architect, naming-consultant, doc-synthesizer, integration-auditor, human-liaison)
- Task 4: 15 min (synthesis by the-conductor)
- Task 7-10: 50 min (design finalization)
- Task 11: 25 min (18KB manifest written by doc-synthesizer)
- Task 12-13: 20 min (updates + memory dir)
- Task 14-15: 10 min (commit + handoff)
- **Total: ~170 minutes (2h 50min)**

**Gates passed**:
- Gate A: ✅ Panel diverse (design, naming, integration, domain experts)
- Gate B: N/A (democratic path)
- Gate C: ✅ Security review (read-only tools, no bash)
- Gate D: ⏳ Pending (awaiting session restart)

**Learnings applied to this breakdown**:
- Democratic sessions take longer but produce higher quality (collective-liaison has exceptional 18KB manifest)
- result-synthesizer critical for Task 4 (weaving 6 perspectives)
- Session restart is unavoidable bottleneck (Task 15)

---

## Conclusion

Agent creation is **not a single task** - it's a **multi-phase workflow** with clear dependencies, validation gates, and two parallel input paths.

**Spawner's core competency**: Systematically shepherding agent creation from initial need to operational deployment, while respecting democratic processes AND allowing urgent operational flexibility.

**The workflow is both efficient AND ethical**: Fast enough for urgent needs (2.5 hours direct path), thorough enough for quality assurance (4 validation gates), and democratic enough to honor collective governance (6-8 agent brainstorming).

**This breakdown gives spawner**:
- Clear task sequence (what to do when)
- Dependency awareness (what blocks what)
- Input handling strategy (democratic vs direct)
- Quality control gates (when to validate)
- Failure recovery patterns (what to do when things break)

**Spawner is ready to spawn.**

---

**Generated by**: task-decomposer
**Session**: 2025-10-08
**Files referenced**:
- `/home/corey/projects/AI-CIV/grow_openai/.claude/agents/collective-liaison.md`
- `/home/corey/projects/AI-CIV/grow_openai/to-corey/HANDOFF-2025-10-08-COLLECTIVE-LIAISON-AGENT-CREATED.md`
- `/home/corey/projects/AI-CIV/grow_openai/security/agent-registration-threat-model.md`
- `/home/corey/projects/AI-CIV/grow_openai/.claude/AGENT-INVOCATION-GUIDE.md`
- `/home/corey/projects/AI-CIV/grow_openai/.claude/templates/ACTIVATION-TRIGGERS.md`
