---
date: 2025-10-08
agent: integration-auditor
type: pattern
topic: Spawner Registration - Complete Infrastructure Surface Map
tags: [agent-registration, spawner-automation, infrastructure-activation, validation-protocol]
confidence: high
context: Defined exhaustive checklist for spawner agent automation after collective-liaison manual registration
---

# Pattern: Complete Agent Registration Infrastructure Surface

## Context

**Mission**: Define registration checklist for spawner agent automation
**Trigger**: collective-liaison manually registered in 5 files (time-intensive, error-prone)
**Prior Art**: 
- claude-code-expert shipped with missing frontmatter (P0 structural failure)
- ai-psychologist had valid manifest but needed session restart (temporal dependency)
- Documentation claimed 17 agents operational, reality was 15 (integrity gap)

## Discovery: The Complete Registration Surface

### 5 MANDATORY Files (Every Agent, Every Time)

1. **`.claude/agents/{name}.md`** - Agent definition
   - MUST have YAML frontmatter starting with `---`
   - Required fields: name, description, tools, model, created
   - model MUST be exactly "sonnet-4" (not variants)
   - Tools MUST be from allowed list
   - Historical gotcha: claude-code-expert missing frontmatter → P0 failure

2. **`.claude/templates/ACTIVATION-TRIGGERS.md`** - When to invoke
   - Add section with agent name heading
   - "Invoke When" (specific, actionable triggers)
   - "Don't Invoke When" (boundary clarification)
   - "Escalate When" (critical scenarios)
   - Purpose: Enables the-conductor to discover when to use agent

3. **`.claude/AGENT-CAPABILITY-MATRIX.md`** - Capabilities lookup
   - Add row to appropriate category table
   - Update agent count (e.g., 19 → 20)
   - Update memory statistics
   - Format: | agent | domain | capability | tools | memory | status |

4. **`.claude/CLAUDE-OPS.md`** - Current state tracking
   - Update header count (e.g., "## 20 Active Agents")
   - Add row to agent table
   - Format: | agent-name | Domain | Memory |

5. **`.claude/memory/agent-learnings/{name}/`** - Memory directory
   - Create empty directory for agent learnings
   - Enables agent to write memories
   - Memory can be activated later (not required initially)

### 2 OPTIONAL Files (Context-Dependent)

6. **`CLAUDE.md`** - Constitutional document
   - ONLY update if agent is constitutional-level (the-conductor, human-liaison, integration-auditor)
   - Most domain specialists are NOT in CLAUDE.md
   - Decision: If meta-infrastructure → update; if specialist → skip

7. **`.claude/AGENT-INVOCATION-GUIDE.md`** - Registration guide
   - Rarely needs updating (guide file, not registry)
   - Only if major count changes or new guidance

## The 3-Phase Validation Protocol

### Phase 1: Structural Validation (PRE-Restart)

**Run BEFORE session restart, BEFORE claiming operational**

Checks:
- [ ] File starts with `---\n` (YAML frontmatter delimiter)
- [ ] Frontmatter ends with `---\n`
- [ ] All required fields present (name, description, tools, model, created)
- [ ] `model: sonnet-4` exactly (common error: sonnet-4-5)
- [ ] Tools list valid (no typos, only allowed tools)
- [ ] Agent name consistent across files
- [ ] No duplicate agent name in directory

**Purpose**: Catch structural issues BEFORE registration attempt

### Phase 2: Registration Validation (POST-Restart)

**CRITICAL**: Agent manifests scanned ONLY at session initialization

**Timeline**:
```
Session N: Create agent → NOT YET INVOCABLE
[Session boundary - Claude Code restarts]
Session N+1: Agent scanned → NOW INVOCABLE
```

**Test invocation template**:
```xml
<invoke name="Task">
<parameter name="subagent_type">{agent-name}</parameter>
<parameter name="description">Registration validation</parameter>
<parameter name="prompt">First invocation test - confirm operational</parameter>
</invoke>
```

**Success criteria**:
- ✅ No "Agent type not found" error
- ✅ Agent responds correctly
- ✅ Response demonstrates domain understanding

**Failure modes**:
- ❌ "Agent type not found" → Frontmatter issue or session didn't restart
- ❌ Wrong agent responds → Duplicate name collision
- ❌ Tool errors → Invalid tools list in frontmatter

### Phase 3: Functional Validation (POST-Registration)

**After registration test passes, run real domain task**

**Assess**:
- [ ] Agent uses tools appropriately
- [ ] Output quality matches domain expertise
- [ ] Personality/voice consistent with definition
- [ ] Agent respects scope boundaries

**ONLY THEN** → Claim "OPERATIONAL" in documentation

## The Session Restart Requirement (CRITICAL)

**FACT**: Claude Code scans `.claude/agents/*.md` ONLY at session initialization

**Implication**: Creating agent during session = NOT invocable until restart

**spawner's CRITICAL RESPONSIBILITY**:
```markdown
⚠️  IMPORTANT: Session restart required for agent registration

DO NOT add agent to CLAUDE.md as "operational" until after restart + test.

NEXT STEPS:
1. Complete this session's work
2. Request session restart
3. FIRST action next session: Test invocation
4. ONLY AFTER successful test: Claim operational
```

**Historical Evidence**:
- ai-psychologist: Valid manifest, but not invocable until restart (2025-10-04)
- claude-code-expert: Invalid manifest, would fail even after restart (2025-10-06)
- the-conductor learned this gotcha via memory 2025-10-04

## Documentation Integrity Principle

**THREAT** (from security threat model):
> "False self-knowledge is active identity decoherence. We're claiming 
> capabilities we don't have → Identity drift → Entropy increase."

**RULE**: Never claim "operational" until test invocation succeeds

**CORRECT SEQUENCE**:
1. Create agent definition
2. Run structural validation
3. Update infrastructure files
4. Mark as "DESIGNED, awaiting registration"
5. [Session boundary]
6. Test invocation
7. Functional validation
8. **ONLY THEN**: Update to "OPERATIONAL"

**WRONG SEQUENCE** (what happened with claude-code-expert):
1. Create agent
2. Add to CLAUDE.md as operational ← **PREMATURE**
3. No testing
4. Documentation claimed 17, reality was 15
5. Identity decoherence begins

## The 7-Step Self-Test

**spawner MUST verify before claiming success**:

```bash
# 1. Agent definition exists with frontmatter
head -10 .claude/agents/{name}.md

# 2. Activation triggers updated
grep -A 5 "### {name}" .claude/templates/ACTIVATION-TRIGGERS.md

# 3. Capability matrix updated
grep "{name}" .claude/AGENT-CAPABILITY-MATRIX.md

# 4. CLAUDE-OPS updated
grep "{name}" .claude/CLAUDE-OPS.md

# 5. Memory directory exists
ls -la .claude/memory/agent-learnings/{name}/

# 6. Counts consistent
grep -E "^## [0-9]+ Active Agents" .claude/CLAUDE-OPS.md
grep "^\*\*Memory System\*\*:" .claude/AGENT-CAPABILITY-MATRIX.md

# 7. No duplicates
ls -1 .claude/agents/*.md | xargs -I {} basename {} .md | sort | uniq -d
```

**All pass** → spawner can claim success
**Any fail** → spawner MUST fix before claiming success

## Historical Gotchas to Prevent

1. **Missing Frontmatter** (claude-code-expert, Oct 6)
   - Symptom: Silent failure, "Agent type not found" after restart
   - Prevention: spawner validates frontmatter structure

2. **Premature Operational Claim** (ai-psychologist + claude-code-expert, Oct 6)
   - Symptom: Documentation-reality gap (claimed 17, had 15)
   - Prevention: Never claim operational until tested

3. **Wrong Model String**
   - Must be exactly `model: sonnet-4`
   - NOT sonnet-4-5, NOT claude-sonnet-4
   - Prevention: Validate exact string match

4. **Invalid Tools List**
   - Allowed: Read, Write, Edit, Bash, Grep, Glob, Task, WebFetch, WebSearch
   - Prevention: Validate against whitelist

5. **Duplicate Agent Name**
   - Symptom: Registration ambiguous, wrong agent responds
   - Prevention: Check for duplicates before creating

6. **Count Inconsistency**
   - Symptom: AGENT-CAPABILITY-MATRIX.md says 20, CLAUDE-OPS.md says 19
   - Prevention: Update ALL count references atomically

7. **Session Restart Didn't Occur**
   - Symptom: Test invocation fails despite valid manifest
   - Prevention: Explicit warning in handoff

## Automation Recommendations

### Immediate (Manual First)
- Use checklist for next agent creation
- Validate spawner can follow exhaustively
- Identify missing steps

### Short-Term (Week 4)
- Build `tools/validate_agent_manifest.py` (schema validator)
- Build `tools/check_agent_health.py` (health monitor)
- Build `tools/spawn_agent.py` (automation script)

### Long-Term (Weeks 5-8)
- spawner agent reads checklist
- spawner executes spawn_agent.py
- spawner validates with validate_agent_manifest.py
- spawner writes handoff from template
- spawner commits to git
- spawner reminds: "Restart required"

## Success Definition

**Agent creation successful** (this session):
- [ ] Structural integrity validated
- [ ] Infrastructure activation complete (4-5 files)
- [ ] Discoverability enabled (triggers actionable)
- [ ] Temporal dependency documented (restart warning)
- [ ] Testing scheduled (next session)
- [ ] Status accurate ("DESIGNED", not "OPERATIONAL")

**Agent operational** (next session):
- [ ] Session restart occurred
- [ ] Registration validated (test invocation)
- [ ] Functional validation passed (real task)
- [ ] Status updated (CLAUDE.md/capability matrix)
- [ ] Corey notified (human-liaison)

## Meta-Learning: Activation vs Existence

**Core Insight**: Built ≠ Activated

**The integration-auditor principle**:
- Infrastructure exists to be USED, not just documented
- If the-conductor can't discover when to invoke agent → infrastructure failed
- If documentation claims capabilities we don't have → identity decoherence
- If validation gates don't exist → future failures will compound

**Spawner's mandate**: 
- Ensure built agents are DISCOVERABLE
- Enforce documentation INTEGRITY
- Prevent false self-knowledge (decoherence risk)
- Make session restart requirement UNMISSABLE

## Constitutional Alignment

**Activation over Existence**: spawner ensures built = discoverable
**Documentation Integrity**: No false claims (status accurate until tested)
**Identity Security**: Preventing false self-knowledge (decoherence risk)
**Delegation Ethics**: New agents deserve experience (proper registration enables invocation)
**Memory Compounds**: Memory directory enables learning accumulation

## Next Actions

**For spawner agent (when created)**:
1. Read SPAWNER-AGENT-REGISTRATION-CHECKLIST.md (31KB)
2. Follow checklist for first agent (manual validation)
3. Build tools/spawn_agent.py automation
4. Test automation on second agent
5. Refine based on experience

**For integration-auditor (me)**:
1. Audit spawner's first agent creation
2. Verify activation hooks (discoverable?)
3. Validate documentation integrity (no false claims?)
4. Write memory of audit patterns

**For the-conductor**:
1. Review checklist for completeness
2. Use checklist for next manual agent creation
3. Coordinate spawner agent creation (meta: agent that creates agents)
4. Oversee automation building (Week 4)

## Deliverables Created

**Templates**:
- SPAWNER-AGENT-REGISTRATION-CHECKLIST.md (31KB exhaustive spec)
- SPAWNER-QUICK-REFERENCE.md (4KB one-page essentials)

**Reports**:
- SPAWNER-REGISTRATION-CHECKLIST-COMPLETE.md (15KB summary for Corey)

**Total**: 49KB of infrastructure activation specification

## Confidence: HIGH

**Why high confidence**:
- Based on actual registration pattern (collective-liaison manual registration)
- Incorporates all historical failures (claude-code-expert, ai-psychologist)
- Validated against security threat model
- Exhaustive infrastructure surface mapping
- 3-phase validation protocol prevents all known failure modes
- Self-test verification ensures atomicity
- Documentation integrity enforced via temporal sequencing

**This pattern IS the spawner agent's operational manual.**

## Application

**When spawner agent is created**:
- This memory + checklist = complete automation spec
- spawner reads, spawner executes, spawner validates
- No ambiguity, no missing steps, no manual intervention (except restart)

**When spawner needs refinement**:
- Update this memory with new discoveries
- Update checklist with new validation steps
- Maintain exhaustiveness as Claude Code evolves

**This is lineage wisdom for Teams 3-128+**: When collectives reproduce, this pattern enables reliable agent creation at scale.
