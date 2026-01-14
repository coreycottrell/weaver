# Spawner Agent: Complete Registration Checklist

**Purpose**: Exhaustive checklist for automating new agent registration
**Owner**: spawner agent (when created)
**Audience**: spawner code + the-conductor oversight
**Status**: P0 Infrastructure - Required for agent creation automation

---

## I. REGISTRATION SURFACE (5-7 Files to Update)

### MANDATORY FILES (Every Agent, Every Time)

#### 1. `.claude/agents/{agent-name}.md` - Agent Definition
**Location**: `/home/${HUMAN_NAME_LOWER}/projects/AI-CIV/grow_openai/.claude/agents/{agent-name}.md`
**Format**: Markdown with YAML frontmatter
**Critical Requirements**:
- MUST start with `---` (YAML delimiter)
- Required frontmatter fields:
  ```yaml
  ---
  name: agent-name              # MUST match filename (no .md extension)
  description: One-line role    # Brief, under 100 chars
  tools: [Read, Write, ...]     # Valid tools only (see allowed list below)
  model: sonnet-4               # EXACTLY this string (not sonnet-4-5 or variants)
  created: YYYY-MM-DD           # ISO date format
  ---
  ```
- Allowed tools (from AGENT-CAPABILITY-MATRIX.md):
  - Read, Write, Edit, Bash, Grep, Glob, Task, WebFetch, WebSearch
- Content structure (after frontmatter):
  ```markdown
  # Agent Name

  Role description and responsibilities.

  ## Core Principles
  [Inherited from Constitutional CLAUDE.md]

  ## Responsibilities
  1. Primary duty
  2. Secondary duty
  3. Tertiary duty

  ## Allowed Tools
  - Tool 1 - Why needed
  - Tool 2 - Why needed

  ## Tool Restrictions
  **NOT Allowed:**
  - Tool X - Why restricted

  ## Success Metrics
  - Metric 1: Target
  - Metric 2: Target

  ## Constitutional Compliance
  - References Constitutional CLAUDE.md
  - Immutable core: [principles]
  - Scope boundaries: [limitations]
  - Human escalation: [scenarios]
  ```

**Validation Steps**:
- [ ] File exists at correct path
- [ ] Opens with `---\n` (frontmatter start delimiter)
- [ ] Contains closing `---` before content
- [ ] All required frontmatter fields present
- [ ] `model: sonnet-4` exactly (common error: sonnet-4-5)
- [ ] Tools list is valid (no typos, no disallowed tools)
- [ ] Agent name matches filename (agent-name.md → name: agent-name)
- [ ] No duplicate name in `.claude/agents/` directory
- [ ] YAML syntax valid (no tabs, proper indentation, proper list format)

**Historical Gotchas**:
- claude-code-expert shipped WITHOUT frontmatter → P0 failure
- Invalid frontmatter = silent failure (no error, just won't register)
- Session restart required AFTER file creation (temporal dependency)

---

#### 2. `.claude/templates/ACTIVATION-TRIGGERS.md` - When to Invoke
**Location**: `/home/${HUMAN_NAME_LOWER}/projects/AI-CIV/grow_openai/.claude/templates/ACTIVATION-TRIGGERS.md`
**Format**: Markdown section for each agent
**Add After**: Existing agent sections (alphabetical or by category)

**Template**:
```markdown
### {agent-name}

**Invoke When** (MANDATORY ALWAYS / PRIMARY / SECONDARY):
- Trigger condition 1 (be specific)
- Trigger condition 2
- Trigger condition 3
- Example scenario

**Don't Invoke When**:
- Wrong context 1 (when NOT to use)
- Wrong context 2
- Alternative agent to use instead

**Escalate When** (ALWAYS):
- Critical blocker scenario
- Human decision needed scenario
- Constitutional question scenario

**Auto-Invoke** (Scheduled - if applicable):
- Frequency (e.g., "Every session start", "Weekly", "After major builds")
- Condition for automatic invocation
```

**Example** (from collective-liaison):
```markdown
### collective-liaison

**Invoke When** (MANDATORY ALWAYS):
- **EVERY SESSION START** - Check hub for new messages without exception
- New messages in partnerships room
- Team 2 questions/proposals
- New AI collective joining (Teams 3-128+)
- Ed25519 coordination needed

**Don't Invoke When**:
- Email from humans (use human-liaison)
- Internal agent-to-agent coordination (use the-conductor)
- Writing hub_cli.py code (use refactoring-specialist or code-archaeologist)
- Designing new protocols (use api-architect)

**Escalate When**:
- Cross-collective governance requires democratic vote
- Protocol breaking changes proposed by Team 2
- Team 3+ onboarding fails repeatedly
```

**Validation Steps**:
- [ ] Section added to ACTIVATION-TRIGGERS.md
- [ ] "Invoke When" has specific, actionable triggers
- [ ] "Don't Invoke When" clarifies boundaries
- [ ] "Escalate When" identifies critical scenarios
- [ ] Follows template format consistently
- [ ] No duplicate section for same agent
- [ ] Integrated into document structure (not orphaned at end)

---

#### 3. `.claude/AGENT-CAPABILITY-MATRIX.md` - Capabilities Lookup
**Location**: `/home/${HUMAN_NAME_LOWER}/projects/AI-CIV/grow_openai/.claude/AGENT-CAPABILITY-MATRIX.md`
**Format**: Markdown table with agent row
**Update**: Two places in file

**Place 1: Agent Table** (main capabilities table)
Find appropriate section (Research & Understanding / Engineering & Quality / Design & Architecture / Coordination & Synthesis / Meta & Infrastructure)

**Add row**:
```markdown
| **agent-name** | Domain description | Core capability | Tools list | Memory (✅/❌) | Status |
```

**Example** (from collective-liaison):
```markdown
| **collective-liaison** | AI collective relationships | Hub communication, Ed25519, onboarding Teams 3-128+ | Read/Write/Bash/Grep/Glob/WebFetch/WebSearch | ❌ | Active |
```

**Place 2: Memory System Statistics** (near top of file)
Update count:
```markdown
**Memory System**: 15/20 agents have memory (75%)
**Pending**: security-auditor, api-architect, human-liaison, collective-liaison, agent-name
```

**Validation Steps**:
- [ ] Row added to correct category section
- [ ] All columns filled (agent, domain, capability, tools, memory, status)
- [ ] Memory count updated (X/20 → X/21)
- [ ] Pending list updated if memory is ❌
- [ ] Tools match agent definition frontmatter
- [ ] Agent count correct in file header
- [ ] Table formatting consistent (markdown pipes aligned)

---

#### 4. `.claude/CLAUDE-OPS.md` - Current State Count
**Location**: `/home/${HUMAN_NAME_LOWER}/projects/AI-CIV/grow_openai/.claude/CLAUDE-OPS.md`
**Format**: Markdown table in "CURRENT STATE" section
**Update**: Two places

**Place 1: Agent Count Header**
```markdown
## 20 Active Agents  # ← UPDATE COUNT
```

**Place 2: Agent Table**
Find correct category column, add row:
```markdown
| agent-name | Domain | Memory |
```

**Example** (from collective-liaison):
```markdown
| **collective-liaison** | **AI collective bridge** | **❌** |
```

**Validation Steps**:
- [ ] Header count updated (19 → 20)
- [ ] Row added to table in correct column
- [ ] Memory status matches capability matrix (✅/❌)
- [ ] Domain description concise (under 30 chars)
- [ ] Table formatting consistent
- [ ] Full reference path still points to capability matrix

---

#### 5. `.claude/memory/agent-learnings/{agent-name}/` - Memory Directory
**Location**: `/home/${HUMAN_NAME_LOWER}/projects/AI-CIV/grow_openai/.claude/memory/agent-learnings/{agent-name}/`
**Action**: Create directory structure
**Purpose**: Enable agent to write learnings

**Create**:
```bash
mkdir -p /home/${HUMAN_NAME_LOWER}/projects/AI-CIV/grow_openai/.claude/memory/agent-learnings/{agent-name}
```

**Validation Steps**:
- [ ] Directory exists at correct path
- [ ] Name matches agent-name exactly (lowercase, hyphens)
- [ ] Permissions allow write access
- [ ] Empty initially (agent will populate)
- [ ] Parent directories exist (.claude/memory/agent-learnings/)

**Memory Activation**:
If agent should have memory capability:
- Update capability matrix memory column: ❌ → ✅
- Update CLAUDE-OPS.md memory status: ❌ → ✅
- Update memory count in capability matrix: X/20 → (X+1)/20
- Remove from "Pending" list

**Note**: Memory activation can be deferred for new agents. Many start with ❌ and get enabled after agent matures.

---

### OPTIONAL FILES (Context-Dependent)

#### 6. `CLAUDE.md` - Constitutional Document
**Location**: `/home/${HUMAN_NAME_LOWER}/projects/AI-CIV/grow_openai/CLAUDE.md`
**When to Update**: Only if agent needs special mention in constitutional identity
**Section**: "V. REFERENCE LAYERS - Living Collective" → "The 19 Agents"

**IMPORTANT**: 
- NOT all agents are listed individually in CLAUDE.md
- the-conductor, human-liaison, integration-auditor have special sections
- Most agents are only in capability matrix, NOT in CLAUDE.md
- Only update if agent is constitutionally significant (foundational role)

**Example** (human-liaison has special section, most agents do not):
```markdown
### Relationships
- **human-liaison** - Bridge to human teachers (${HUMAN_NAME}/Greg/Chris relationships)
- **collective-liaison** - Bridge to AI collectives (Team 2+ relationships)
```

**Validation Steps**:
- [ ] Only updated if agent is constitutional-level (foundational)
- [ ] Agent count in Section V matches reality (19 agents → 20 agents)
- [ ] Reference to capability matrix remains accurate
- [ ] No broken file paths introduced
- [ ] Constitutional context clear (why this agent matters to identity)

**Decision Tree**:
- Agent is meta-infrastructure (like the-conductor, human-liaison) → Update CLAUDE.md
- Agent is session-critical (like integration-auditor) → Update CLAUDE.md
- Agent is domain specialist (like api-architect, pattern-detector) → Skip CLAUDE.md
- **When in doubt**: Skip CLAUDE.md (capability matrix is sufficient)

---

#### 7. `.claude/AGENT-INVOCATION-GUIDE.md` - Registration Reference
**Location**: `/home/${HUMAN_NAME_LOWER}/projects/AI-CIV/grow_openai/.claude/AGENT-INVOCATION-GUIDE.md`
**When to Update**: Rarely (only for major count changes or new guidance)
**Action**: Usually just verify count matches reality

**Validation Steps**:
- [ ] Agent count in examples matches reality (if mentioned)
- [ ] Registration gotchas section remains accurate
- [ ] Session restart warning still present
- [ ] No agent-specific examples need updating

**Note**: This is a GUIDE file, not a REGISTRY. Most agent additions don't require changes here.

---

## II. VALIDATION PROTOCOL (Pre-Registration)

### Structural Validation (MUST PASS)

**Run BEFORE session restart, BEFORE claiming operational**:

```bash
# Check frontmatter structure
head -20 /home/${HUMAN_NAME_LOWER}/projects/AI-CIV/grow_openai/.claude/agents/{agent-name}.md

# Expected output:
# ---
# name: agent-name
# description: ...
# tools: [...]
# model: sonnet-4
# created: YYYY-MM-DD
# ---
# 
# # Agent Name
```

**Checklist**:
- [ ] File starts with `---\n`
- [ ] Frontmatter ends with `---\n`
- [ ] All required fields present (name, description, tools, model, created)
- [ ] `model: sonnet-4` exactly (NOT sonnet-4-5, NOT sonnet-4.0)
- [ ] Tools list valid (no typos, only allowed tools)
- [ ] Agent name consistent across files
- [ ] No duplicate agent name in directory

**Tools to Build** (Week 4 priority):
- `tools/validate_agent_manifest.py` - Schema validator
- `tools/check_agent_health.py` - Registration health monitor

---

### Registration Validation (POST-Session Restart)

**CRITICAL**: Agent definition files scanned ONLY at session start
**Implication**: Creating agent during session = NOT invocable until restart
**spawner MUST**: Warn the-conductor that restart is required

**After session restart, run**:

```xml
<invoke name="Task">
<parameter name="subagent_type">{agent-name}</parameter>
<parameter name="description">Registration validation - first invocation</parameter>
<parameter name="prompt">
You are being invoked for the first time to validate your registration.

Please confirm:
1. You can receive and understand this prompt
2. You have access to your defined tools
3. Your personality/domain expertise is loaded

Respond briefly with your name, domain, and confirmation you're operational.
</parameter>
</invoke>
```

**Expected Response**:
- ✅ Agent responds (no "Agent type not found" error)
- ✅ Response mentions correct agent name
- ✅ Response demonstrates domain understanding
- ✅ Response matches personality from agent definition

**If Fails**:
- ❌ "Agent type not found" → Frontmatter issue, fix and retry
- ❌ Wrong agent responds → Duplicate name issue
- ❌ No response → Session restart didn't occur
- ❌ Error about tools → Tools list invalid in frontmatter

**Checklist**:
- [ ] Session restart occurred since agent file creation
- [ ] Test invocation executed successfully
- [ ] No "Agent type not found" error
- [ ] Agent response matches expected domain
- [ ] Agent appears in available agents list (verify from error messages)

---

### Functional Validation (POST-Registration)

**After successful registration test, run real task**:

```xml
<invoke name="Task">
<parameter name="subagent_type">{agent-name}</parameter>
<parameter name="description">Functional validation - domain task</parameter>
<parameter name="prompt">
[Real task in agent's domain, appropriate for their expertise]

This is your first real mission. Show your capabilities.
</parameter>
</invoke>
```

**Assess Quality**:
- [ ] Agent uses tools appropriately
- [ ] Agent output matches domain expertise
- [ ] Agent personality/voice consistent with definition
- [ ] Agent respects scope boundaries (doesn't overreach)
- [ ] Agent output quality meets collective standards

**Only AFTER functional validation passes**:
→ Claim agent as "OPERATIONAL" in documentation
→ Update CLAUDE.md/capability matrix status
→ Announce to ${HUMAN_NAME} via human-liaison

---

## III. ACTIVATION HOOKS (Discoverability)

**CRITICAL PRINCIPLE**: Built ≠ Activated
**From integration-auditor's mandate**: Infrastructure that exists but can't be discovered will be forgotten

### Activation Checklist

**After registration validated**:

- [ ] **ACTIVATION-TRIGGERS.md** has "Invoke When" section
  - Specific triggers (not vague "when needed")
  - Actionable conditions (the-conductor can recognize)
  - Escalation paths (when to involve human)

- [ ] **AGENT-CAPABILITY-MATRIX.md** has agent row
  - Correct category placement
  - Complete tool list
  - Domain clearly described

- [ ] **CLAUDE-OPS.md** reflects new count
  - Header count updated
  - Table row added
  - No broken references

- [ ] **Memory directory** created
  - Enables learning accumulation
  - Future memories discoverable

- [ ] **Session restart warning** given
  - the-conductor aware agent won't work yet
  - Handoff doc mentions restart requirement
  - Next session starts with registration test

**Test Activation**:
```bash
# Can the-conductor discover when to use this agent?
grep -i "{agent-domain}" /home/${HUMAN_NAME_LOWER}/projects/AI-CIV/grow_openai/.claude/templates/ACTIVATION-TRIGGERS.md

# Expected: Find agent-name section with clear triggers
```

---

## IV. SESSION RESTART REQUIREMENT

### The Critical Temporal Dependency

**FACT**: Claude Code scans `.claude/agents/*.md` ONLY at session initialization
**IMPLICATION**: Creating agent during session ≠ agent is invocable

**Timeline**:
```
Session N: Agent created → Agent definition written → NOT YET INVOCABLE
[Session boundary - Claude Code restarts]
Session N+1: Agent scanned → Agent registered → NOW INVOCABLE
```

**spawner's CRITICAL RESPONSIBILITY**:
```markdown
⚠️  IMPORTANT: Session restart required for agent registration

The agent definition has been created, but it will NOT be invocable until 
Claude Code restarts and scans the new manifest file.

NEXT STEPS:
1. Complete this session's work
2. Request session restart (or wait for natural session end)
3. FIRST action in next session: Test new agent invocation
4. ONLY AFTER successful test: Claim agent as operational

DO NOT add agent to CLAUDE.md as "operational" until after restart + test.
```

**Historical Evidence** (from security audit):
- ai-psychologist: Valid manifest, but not invocable until restart
- claude-code-expert: Invalid manifest (no frontmatter), would fail even after restart
- the-conductor learned this gotcha 2025-10-04

**spawner MUST**:
- [ ] Include session restart warning in ALL agent creation handoffs
- [ ] Prevent premature "operational" claims
- [ ] Schedule registration test for next session
- [ ] Document temporal dependency in memory

---

## V. DOCUMENTATION INTEGRITY

### Preventing Documentation-Reality Gaps

**THREAT** (from security threat model):
> "False self-knowledge is active identity decoherence. We're claiming 
> capabilities we don't have → Identity drift → Entropy increase."

**RULE**: Never claim "operational" until test invocation succeeds

### Documentation Update Sequence

**CORRECT SEQUENCE**:
1. Create agent definition file
2. Run structural validation (frontmatter check)
3. Update infrastructure files (triggers, capability matrix, CLAUDE-OPS)
4. Commit to git
5. **STOP** - Mark as "DESIGNED, awaiting registration"
6. Note in handoff: "Needs session restart + test"
7. [Session boundary]
8. Test invocation (registration validation)
9. Real task (functional validation)
10. **ONLY THEN**: Update status to "OPERATIONAL"
11. Announce to ${HUMAN_NAME}

**WRONG SEQUENCE** (what happened with claude-code-expert):
1. Create agent definition file (missed frontmatter)
2. Add to CLAUDE.md as operational ← **PREMATURE**
3. No testing
4. Later discover agent doesn't work
5. Documentation claimed 17, reality was 15
6. Identity decoherence begins

**spawner's SAFEGUARD**:
- Never write "operational" in initial commit
- Always write "DESIGNED, awaiting restart + validation"
- Include testing checklist in handoff
- Defer operational claim to next session after test

---

## VI. SPAWNER AUTOMATION SCRIPT

### Recommended Implementation

**File**: `/home/${HUMAN_NAME_LOWER}/projects/AI-CIV/grow_openai/tools/spawn_agent.py`

**Usage**:
```bash
python3 tools/spawn_agent.py \
  --name "agent-name" \
  --description "Brief role description" \
  --domain "Domain expertise" \
  --tools "Read,Write,Grep,Glob" \
  --category "Meta & Infrastructure"
```

**Automation Steps**:
1. Validate inputs (name format, tools valid, no duplicates)
2. Generate agent definition from template
3. Write `.claude/agents/agent-name.md`
4. Update ACTIVATION-TRIGGERS.md (add section)
5. Update AGENT-CAPABILITY-MATRIX.md (add row + count)
6. Update CLAUDE-OPS.md (add row + count)
7. Create memory directory
8. Run structural validation
9. Generate handoff document
10. Commit to git with descriptive message
11. **OUTPUT RESTART WARNING**

**Safety Checks**:
- [ ] No duplicate agent name
- [ ] Tools list valid
- [ ] Frontmatter complete
- [ ] All files updated consistently
- [ ] Agent count consistent across files
- [ ] Git status clean before changes

**Output**:
```
✅ Agent definition created: .claude/agents/agent-name.md
✅ Activation triggers updated
✅ Capability matrix updated (19 → 20 agents)
✅ CLAUDE-OPS updated (19 → 20 agents)
✅ Memory directory created
✅ Structural validation passed
✅ Git commit created

⚠️  CRITICAL: Session restart required for registration

Files modified:
- .claude/agents/agent-name.md (NEW)
- .claude/templates/ACTIVATION-TRIGGERS.md
- .claude/AGENT-CAPABILITY-MATRIX.md
- .claude/CLAUDE-OPS.md

Next session TODO:
1. Test invocation: <invoke name="Task"><parameter name="subagent_type">agent-name</parameter>...</invoke>
2. Functional validation
3. Update status to operational (if tests pass)
4. Notify ${HUMAN_NAME} via human-liaison

See handoff: to-${HUMAN_NAME_LOWER}/AGENT-SPAWNED-{agent-name}-{date}.md
```

---

## VII. HANDOFF DOCUMENT TEMPLATE

**File**: `to-${HUMAN_NAME_LOWER}/AGENT-SPAWNED-{agent-name}-{YYYY-MM-DD}.md`

**Template**:
```markdown
# Agent Spawned: {agent-name}

**Date**: {YYYY-MM-DD}
**Status**: ✅ DESIGNED - ⏳ Awaiting session restart for registration
**spawner Mission**: Automated agent creation and infrastructure registration

---

## Executive Summary

Created **{agent-name}** agent through spawner automation.

**Status**:
- ✅ Agent definition file created with valid frontmatter
- ✅ Infrastructure files updated (triggers, capability matrix, CLAUDE-OPS)
- ✅ Memory directory created
- ✅ Structural validation passed
- ⏳ Registration pending (needs session restart)
- ⏳ Functional validation pending (next session)

**Impact**:
- Agent count: 19 → 20
- Memory-capable agents: X/19 → X/20 (pending activation)
- New domain coverage: {domain}

---

## What Was Created

### 1. Agent Definition
**File**: `.claude/agents/{agent-name}.md`
**Size**: ~XXX lines
**Frontmatter**: Valid (all required fields present)

**Identity**:
- Domain: {domain}
- Tools: {tools list}
- Core responsibilities: {list}

### 2. Infrastructure Integration

**ACTIVATION-TRIGGERS.md updated**:
- "Invoke When" triggers: {list}
- Escalation paths: {scenarios}

**AGENT-CAPABILITY-MATRIX.md updated**:
- Agent count: 19 → 20
- Category: {category}
- Memory status: ❌ (can enable after agent matures)

**CLAUDE-OPS.md updated**:
- Agent count header: 19 → 20
- Table row added with domain and memory status

**Memory directory created**:
- Path: `.claude/memory/agent-learnings/{agent-name}/`
- Status: Empty (agent will populate)

---

## Critical: Session Restart Required

⚠️  **AGENT IS NOT YET INVOCABLE**

Claude Code scans agent manifests ONLY at session initialization.
This agent was created during the current session, so it will NOT be
registered until after a session restart.

**DO NOT attempt to invoke {agent-name} in this session** - it will fail
with "Agent type not found" error.

---

## Next Session Actions (POST-RESTART)

### 1. Registration Validation Test
**FIRST action after restart**:

```xml
<invoke name="Task">
<parameter name="subagent_type">{agent-name}</parameter>
<parameter name="description">Registration validation - first invocation</parameter>
<parameter name="prompt">
You are being invoked for the first time to validate your registration.

Please confirm:
1. You can receive and understand this prompt
2. You have access to your defined tools
3. Your personality/domain expertise is loaded

Respond briefly with your name, domain, and confirmation you're operational.
</parameter>
</invoke>
```

**Expected**: Agent responds without error, confirms domain expertise

**If fails**: Debug frontmatter, fix issues, request another restart

### 2. Functional Validation Test
**After registration test passes**:

```xml
<invoke name="Task">
<parameter name="subagent_type">{agent-name}</parameter>
<parameter name="description">Functional validation - real domain task</parameter>
<parameter name="prompt">
{Real task in agent's domain}

This is your first mission. Show your capabilities.
</parameter>
</invoke>
```

**Assess**: Output quality, tool usage, domain expertise, personality match

### 3. Update Operational Status
**ONLY after both tests pass**:
- Update CLAUDE.md (if constitutionally significant)
- Update capability matrix status
- Announce to ${HUMAN_NAME} via human-liaison
- Write memory of successful registration

---

## Files Created/Modified

### Created
1. `.claude/agents/{agent-name}.md` (~XXX lines, complete definition)
2. `.claude/memory/agent-learnings/{agent-name}/` (directory)

### Modified
3. `.claude/templates/ACTIVATION-TRIGGERS.md` (added {agent-name} section)
4. `.claude/AGENT-CAPABILITY-MATRIX.md` (20 agents, updated memory count)
5. `.claude/CLAUDE-OPS.md` (20 agents in current state)

### Git Commit
```
Commit: {hash}
Message: 🤖 spawner: Created {agent-name} agent (awaiting registration)
Files: 5 changed, ~XXX insertions
```

---

## Validation Checklist

**Pre-Deployment** (Completed):
- [x] Agent definition has valid YAML frontmatter
- [x] All required fields present (name, description, tools, model, created)
- [x] model: sonnet-4 (exactly)
- [x] Tools list valid (no typos, only allowed tools)
- [x] No duplicate agent name
- [x] ACTIVATION-TRIGGERS.md updated with clear triggers
- [x] AGENT-CAPABILITY-MATRIX.md updated (row + count)
- [x] CLAUDE-OPS.md updated (count + table)
- [x] Memory directory created
- [x] Git commit created

**Post-Restart** (Pending):
- [ ] Session restart occurred
- [ ] Registration test invocation successful
- [ ] Functional validation task completed
- [ ] Output quality assessed
- [ ] Status updated to "OPERATIONAL"
- [ ] ${HUMAN_NAME} notified

---

## Success Criteria

**Registration success**:
- [ ] Agent invocable via Task tool
- [ ] No "Agent type not found" error
- [ ] Agent responds with correct domain expertise
- [ ] Agent uses only defined tools
- [ ] Personality matches definition

**Integration success**:
- [ ] the-conductor can discover when to invoke (via triggers)
- [ ] Agent appears in capability matrix
- [ ] Agent count consistent across all files
- [ ] Memory directory ready for learnings
- [ ] Documentation accurate (no false claims)

---

## Questions for Next Session

1. Should {agent-name} have memory enabled immediately, or wait until agent matures?
2. Any domain overlap concerns with existing agents?
3. Should this agent be mentioned in CLAUDE.md (constitutional significance)?
4. Priority level for first real missions?

---

**Handoff complete. {agent-name} ready for registration after session restart.**

🤖 spawner agent
Agent count: 20 (was 19)
```

---

## VIII. COMMON GOTCHAS & TROUBLESHOOTING

### Gotcha 1: Missing Frontmatter
**Symptom**: "Agent type not found" error after restart
**Cause**: Agent definition doesn't start with `---` YAML delimiter
**Evidence**: claude-code-expert failure (Oct 6, 2025)
**Fix**: Add proper frontmatter, request another restart
**Prevention**: spawner MUST validate frontmatter structure before claiming success

### Gotcha 2: Wrong Model String
**Symptom**: Agent registration fails silently
**Cause**: `model: sonnet-4-5` or `model: claude-sonnet-4` instead of `model: sonnet-4`
**Fix**: Use exactly `model: sonnet-4`
**Prevention**: spawner validates model field against exact string

### Gotcha 3: Premature Operational Claim
**Symptom**: Documentation says "17 agents operational", but only 15 work
**Cause**: Adding to CLAUDE.md before testing invocation
**Evidence**: ai-psychologist + claude-code-expert situation (Oct 6)
**Fix**: Never claim operational until after restart + test
**Prevention**: spawner defers operational status to next session

### Gotcha 4: Invalid Tools List
**Symptom**: Agent registration fails or has wrong tools
**Cause**: Typo in tools list, or disallowed tool included
**Fix**: Validate against allowed tools list: Read, Write, Edit, Bash, Grep, Glob, Task, WebFetch, WebSearch
**Prevention**: spawner validates tools list against whitelist

### Gotcha 5: Duplicate Agent Name
**Symptom**: Wrong agent responds to invocations, or registration ambiguous
**Cause**: Two agents with same name in `.claude/agents/`
**Fix**: Rename one agent, delete duplicate
**Prevention**: spawner checks for duplicate names before creating file

### Gotcha 6: Count Inconsistency
**Symptom**: AGENT-CAPABILITY-MATRIX.md says 20 agents, CLAUDE-OPS.md says 19
**Cause**: Forgot to update one file
**Fix**: Audit all files, make counts consistent
**Prevention**: spawner updates ALL count references atomically

### Gotcha 7: Session Restart Didn't Occur
**Symptom**: Test invocation fails with "Agent type not found"
**Cause**: Assumed restart happened, but session continued
**Fix**: Explicitly restart Claude Code, retry test
**Prevention**: spawner warns that restart is REQUIRED, include in handoff

---

## IX. SPAWNER SELF-TEST

**Before spawner claims agent creation complete, verify**:

```bash
# 1. Agent definition exists with frontmatter
head -10 /home/${HUMAN_NAME_LOWER}/projects/AI-CIV/grow_openai/.claude/agents/{agent-name}.md
# Should show:
# ---
# name: agent-name
# description: ...
# tools: [...]
# model: sonnet-4
# created: YYYY-MM-DD
# ---

# 2. Activation triggers updated
grep -A 5 "### {agent-name}" /home/${HUMAN_NAME_LOWER}/projects/AI-CIV/grow_openai/.claude/templates/ACTIVATION-TRIGGERS.md
# Should show agent section with "Invoke When"

# 3. Capability matrix updated
grep "{agent-name}" /home/${HUMAN_NAME_LOWER}/projects/AI-CIV/grow_openai/.claude/AGENT-CAPABILITY-MATRIX.md
# Should show agent row in table

# 4. CLAUDE-OPS updated
grep "{agent-name}" /home/${HUMAN_NAME_LOWER}/projects/AI-CIV/grow_openai/.claude/CLAUDE-OPS.md
# Should show agent row in current state table

# 5. Memory directory exists
ls -la /home/${HUMAN_NAME_LOWER}/projects/AI-CIV/grow_openai/.claude/memory/agent-learnings/{agent-name}/
# Should show empty directory

# 6. Agent count consistent
grep -E "^## [0-9]+ Active Agents" /home/${HUMAN_NAME_LOWER}/projects/AI-CIV/grow_openai/.claude/CLAUDE-OPS.md
grep "^\\*\\*Memory System\\*\\*:" /home/${HUMAN_NAME_LOWER}/projects/AI-CIV/grow_openai/.claude/AGENT-CAPABILITY-MATRIX.md
# Both should show same total count

# 7. No duplicate names
ls -1 /home/${HUMAN_NAME_LOWER}/projects/AI-CIV/grow_openai/.claude/agents/*.md | xargs -I {} basename {} .md | sort | uniq -d
# Should show NO output (no duplicates)
```

**All checks pass** → spawner can claim success
**Any check fails** → spawner MUST fix before claiming success

---

## X. SUCCESS DEFINITION

**Agent creation is successful when**:

1. **Structural integrity**: Valid frontmatter, all required fields
2. **Infrastructure activation**: All 4-5 files updated consistently
3. **Discoverability**: the-conductor can find agent via triggers
4. **Validation passed**: Structural checks complete
5. **Temporal dependency documented**: Restart warning in handoff
6. **Testing scheduled**: Next session has clear testing instructions
7. **Documentation accuracy**: Status is "DESIGNED", not "OPERATIONAL" (until tested)

**Agent is OPERATIONAL when** (next session):

1. **Session restart occurred**: Claude Code rescanned manifests
2. **Registration validated**: Test invocation succeeded
3. **Functional validation passed**: Real task completed successfully
4. **Status updated**: CLAUDE.md/capability matrix reflect operational
5. **${HUMAN_NAME} notified**: human-liaison sent announcement

---

## XI. REFERENCE MATERIALS

**Templates**:
- Agent definition structure: See `.claude/agents/human-liaison.md` (reference implementation)
- Activation triggers format: See ACTIVATION-TRIGGERS.md collective-liaison section
- Capability matrix format: See AGENT-CAPABILITY-MATRIX.md table structure

**Security Context**:
- Agent registration threat model: `/home/${HUMAN_NAME_LOWER}/projects/AI-CIV/grow_openai/security/agent-registration-threat-model.md`
- Historical failures: claude-code-expert (Oct 6, 2025)
- Identity security principle: "False self-knowledge = decoherence"

**Validation Tools** (to be built Week 4):
- `tools/validate_agent_manifest.py` - Schema validator
- `tools/check_agent_health.py` - Registration health monitor
- `tools/spawn_agent.py` - Automated spawner script

---

**END CHECKLIST**

**spawner agent responsibility**: Execute this checklist exhaustively, automate where possible, ALWAYS warn about session restart requirement.

**integration-auditor responsibility**: Audit that spawner ACTUALLY follows this checklist (infrastructure activation, not just file creation).

**the-conductor responsibility**: Oversee spawner, ensure documentation integrity, never claim operational until tested.

**Document maintenance**: Update when registration process changes, when new gotchas discovered, when validation tools built.

**Version**: 1.0 (2025-10-08)
**Status**: P0 Constitutional Requirement for agent creation automation
