# Integration Health Methodology
**Measuring Infrastructure Activation, Not Just Existence**

**Created**: 2025-10-08
**Agent**: integration-auditor
**Purpose**: Systematic framework for auditing infrastructure integration health
**Status**: Living methodology (update as new failure modes discovered)

---

## Executive Summary

**Core Principle**: Built ≠ Activated ≠ Used ≠ Needed

This methodology distinguishes between:
- **Infrastructure dormancy** (built but unused, should be activated)
- **Infrastructure clutter** (built but unneeded, should be pruned)
- **Infrastructure gaps** (needed but not built, should be created)
- **Integration failures** (built, needed, but broken activation)

**Success Metric**: 100% P0 infrastructure discoverable + functional + used
**Failure Metric**: Any P0 infrastructure unmeasured or documentation drift

---

## Part 1: What to Audit - The 4-Layer Activation Model

### Layer 1: Physical Layer (Existence)
**Question**: Does infrastructure physically exist?

**Audit Surface**:
- Files exist at documented paths
- Directories present with correct permissions
- Code compiles/parses without syntax errors
- Dependencies installed and importable
- Configuration files valid

**Tests**:
```bash
# File existence
ls -la /path/to/infrastructure

# Syntax validation
python3 -m py_compile tools/memory_core.py

# Import test
python3 -c "from tools.memory_core import MemoryStore"

# Directory structure
find .claude/ -type d | wc -l  # Expected: N directories
```

**Pass Criteria**: All documented paths exist and are valid
**Failure Mode**: "File not found" errors in documentation

---

### Layer 2: Discovery Layer (Findability)
**Question**: Can fresh session discover infrastructure exists?

**Audit Surface**:
- CLAUDE.md references infrastructure with absolute paths
- CLAUDE-OPS.md includes in Quick Reference
- Agent manifests link to relevant templates/tools
- Activation triggers reference infrastructure
- Capability matrix mentions tool usage

**Tests**:
```bash
# Is it in cold-start protocol?
grep -n "memory_core" /home/${HUMAN_NAME_LOWER}/projects/AI-CIV/grow_openai/CLAUDE.md

# Is it in operational playbook?
grep -n "MemoryStore" /home/${HUMAN_NAME_LOWER}/projects/AI-CIV/grow_openai/.claude/CLAUDE-OPS.md

# Do agent manifests reference it?
grep -r "memory system" /home/${HUMAN_NAME_LOWER}/projects/AI-CIV/grow_openai/.claude/agents/

# Are there multiple entry points? (redundancy for discovery)
grep -r "tools/memory_core.py" .claude/ | wc -l  # Expected: 5+ references
```

**Pass Criteria**: 
- 3+ references in constitutional/operational docs
- All P0 agents aware (in their manifests)
- Actionable instructions (file paths + code examples)

**Failure Mode**: "Didn't know about X" - infrastructure invisible to fresh session

---

### Layer 3: Functional Layer (Usability)
**Question**: Does infrastructure work when discovered and invoked?

**Audit Surface**:
- Examples in CLAUDE.md execute successfully
- Code examples in agent manifests run without errors
- API signature matches documentation
- Error handling graceful (doesn't crash on invalid input)
- Dependencies available (no import errors)

**Tests**:
```python
# Execute EXACTLY as documented in CLAUDE.md
from tools.memory_core import MemoryStore
store = MemoryStore(".claude/memory")
results = store.search_by_topic("coordination patterns")

# Verify return type matches documentation
print(type(results))  # Expected: list
print(type(results[0]))  # Expected: MemoryEntry (NOT str)

# Test error handling
bad_results = store.search_by_topic("")  # Empty string
print(type(bad_results))  # Should return empty list, not crash
```

**Pass Criteria**: 
- All documented examples execute successfully
- Return types match documentation
- No AttributeError/TypeError crashes
- Fresh session can complete cold-start protocol

**Failure Mode**: Documentation drift - code evolved, docs didn't update

**Historical Example**: Memory system returned file paths (strings) but documentation showed MemoryEntry objects → AttributeError when following examples (Oct 6, 2025)

---

### Layer 4: Cultural Layer (Adoption)
**Question**: Is infrastructure actually used in practice?

**Audit Surface**:
- Usage logs/metrics exist
- Files created/modified by infrastructure
- Git commits referencing infrastructure
- Agent memories mentioning infrastructure
- Dashboard panels tracking usage

**Tests**:
```bash
# Memory system: Count entries created
find .claude/memory/agent-learnings -name "*.md" | wc -l

# Memory system: Recent activity
find .claude/memory/agent-learnings -name "*.md" -mtime -7 | wc -l

# Mission class: Find actual usage
grep -r "Mission(" tools/ to-${HUMAN_NAME_LOWER}/ --include="*.md" --include="*.py" | wc -l

# Hub communication: Message count
ls -1 team1-production-hub/rooms/partnerships/messages/2025/10/*.json | wc -l

# Agent invocation: Count Task calls (proxy for delegation)
grep -r '<invoke name="Task">' to-${HUMAN_NAME_LOWER}/ | wc -l
```

**Pass Criteria**:
- Usage >= 1x per week for P0 infrastructure
- Trend increasing or stable (not declining)
- Multiple agents using (not just one)
- Evidence in recent work (last 7 days)

**Failure Mode**: Infrastructure dormancy - built, discoverable, functional, but unused

**Historical Example**: Mission class designed for "all multi-agent work" but only 6 usages, last Oct 3 (Oct 6 audit found zero recent imports)

---

## Part 2: Failure Modes - The 5 Anti-Patterns

### Anti-Pattern 1: "Works in the Builder's Head"
**Symptom**: Builder uses infrastructure successfully, others can't

**Mechanism**:
- Builder knows implementation details (e.g., returns file paths)
- Documentation shows intended interface (e.g., returns objects)
- Gap invisible until someone follows documentation
- Builder never does cold-start simulation

**Detection**:
```
Layer 1: PASS (exists)
Layer 2: PASS (documented)
Layer 3: FAIL (documented examples crash)
Layer 4: PARTIAL (write-only usage)
```

**Remediation**:
1. Cold-start simulation (fresh session, follow docs exactly)
2. Fix code OR documentation (whichever is correct design)
3. Add executable tests of documentation examples
4. Require: "Can someone who's never seen this use it?"

**Prevention**: Mandatory cold-start test before claiming "activated"

---

### Anti-Pattern 2: "Write-Only Infrastructure"
**Symptom**: High write activity, zero read activity

**Mechanism**:
- Write API works (agents create entries)
- Read API broken (agents can't search)
- Asymmetry not visible without metrics
- Appears healthy (files accumulating) but delivers zero value

**Detection**:
```bash
# Memory system example
echo "Write activity:"
find .claude/memory -name "*.md" -mtime -7 | wc -l  # High number

echo "Read activity:"
grep -r "store.search_by_topic" to-${HUMAN_NAME_LOWER}/ .claude/ --include="*.md" | wc -l  # Zero or low
```

**Distinction from Dormancy**:
- Dormancy: Infrastructure fully works, but nobody uses it (cultural failure)
- Write-Only: Infrastructure partially broken, one direction works (functional failure)

**Remediation**:
1. Test read paths as thoroughly as write paths
2. Add bidirectional metrics (reads vs writes)
3. Alert when asymmetry detected (writes >> reads)

**Prevention**: Test all API surfaces, not just creation/write

---

### Anti-Pattern 3: "Documentation Drift"
**Symptom**: Code and documentation diverge over time

**Mechanism**:
- Code evolves during development
- Documentation written early, not updated
- Multiple sources of truth (20+ files)
- No CI/CD validation that examples execute

**Detection**:
```bash
# Find all documentation of memory system
grep -r "MemoryStore" .claude/ CLAUDE.md to-${HUMAN_NAME_LOWER}/ --include="*.md"

# Check for inconsistencies
grep -A 5 "search_by_topic" .claude/*.md | grep "for memory in"
# Compare documented usage patterns
```

**Remediation**:
1. Single source of truth (one authoritative example)
2. All other docs reference SSOT
3. Executable documentation (tests run examples)
4. Version documentation with code

**Prevention**: CI/CD runs all code examples in CLAUDE.md

---

### Anti-Pattern 4: "Premature Operational Claim"
**Symptom**: Documentation claims "operational" before testing

**Mechanism**:
- Agent manifest created
- Infrastructure files updated
- Documentation updated to show "17 agents operational"
- **NO TEST INVOCATION** before claiming success
- Session restart requirement forgotten

**Detection**:
```bash
# Count agents in CLAUDE-OPS.md
grep "^## [0-9]+ Active Agents" .claude/CLAUDE-OPS.md

# Count agent manifest files
ls -1 .claude/agents/*.md | wc -l

# Count agents with valid frontmatter
for f in .claude/agents/*.md; do head -1 "$f"; done | grep "^---$" | wc -l

# Compare: Should all be equal, if not = integrity gap
```

**Historical Example**: 
- claude-code-expert added to CLAUDE.md as "operational" (Oct 6, 2025)
- Missing YAML frontmatter → not actually invocable
- Documentation claimed 17, reality was 15
- Identity decoherence: false self-knowledge

**Remediation**:
1. Never claim "operational" until test invocation succeeds
2. Use status: "DESIGNED → REGISTERED → OPERATIONAL"
3. Session restart + test before status change

**Prevention**: 3-phase validation protocol (structural → registration → functional)

---

### Anti-Pattern 5: "Mission Scope Creep Without Pruning"
**Symptom**: Infrastructure built for every idea, never removed

**Mechanism**:
- New infrastructure created for each mission
- No sunset evaluation
- No removal when superseded
- "Just in case" hoarding mentality

**Detection**:
```bash
# Find infrastructure with zero recent usage
find .claude/flows/ -name "*.md" -mtime +30

# Check git log for last modification
for f in .claude/flows/*.md; do 
  echo "$f: $(git log -1 --format=%ai $f)"
done

# Compare against activation triggers (referenced?)
grep -f <(ls -1 .claude/flows/*.md | xargs basename -s .md) \
  .claude/templates/ACTIVATION-TRIGGERS.md
```

**Distinction from Dormancy**:
- Dormancy: Should be used, isn't yet (needs activation)
- Clutter: Shouldn't exist anymore (needs removal)

**Decision Framework**:
```
Is infrastructure used in last 30 days?
  └─ YES → KEEP (active)
  └─ NO → Is it P0 critical infrastructure?
      └─ YES → DORMANT (audit activation, fix discovery/usability)
      └─ NO → Is it superseded by better approach?
          └─ YES → PRUNE (archive + remove references)
          └─ NO → KEEP (but mark for 90-day re-eval)
```

**Remediation**:
1. Quarterly infrastructure audit
2. Archive (don't delete) unused infrastructure
3. Update documentation to remove references
4. Require: "Why does this exist? Who benefits?"

**Prevention**: Every infrastructure requires "Success Metric" + "Sunset Condition"

---

## Part 3: Measuring Integration Health - The Health Score

### Health Score Formula

**Per Infrastructure Item**:
```
Health = (Physical * 0.1) + (Discovery * 0.3) + (Functional * 0.4) + (Cultural * 0.2)

Where each layer = 0.0 to 1.0:
- Physical: 1.0 if exists, 0.0 if missing
- Discovery: (references_count / 3) capped at 1.0
- Functional: 1.0 if tests pass, 0.5 if partial, 0.0 if broken
- Cultural: (usage_last_7_days / expected_usage) capped at 1.0
```

**Weighted toward Functional** (40%) because:
- Existence without function = 0 value
- Discovery without function = frustration
- Culture follows function (can't use what doesn't work)

**System-Wide Health**:
```
System Health = average(health_p0_infrastructure) * 100

Where P0 infrastructure is critical path (defined by activation triggers)
```

---

### Health Thresholds

**90-100%**: EXCELLENT
- All P0 infrastructure discoverable + functional + used
- Documentation accurate
- No known activation gaps
- Verdict: "Integrated & Operational"

**70-89%**: GOOD
- Most P0 infrastructure working
- Minor documentation drift
- Some underutilization (cultural layer gaps)
- Verdict: "Functional, needs activation work"

**50-69%**: FAIR
- P1 infrastructure gaps OR P0 partial failures
- Significant documentation drift
- Usage inconsistent
- Verdict: "Works but fragile"

**30-49%**: POOR
- P0 infrastructure has functional failures
- Documentation significantly outdated
- Low adoption despite need
- Verdict: "Requires immediate remediation"

**0-29%**: CRITICAL
- P0 infrastructure broken or missing
- Cold-start would fail
- Identity decoherence risk (false claims)
- Verdict: "Block work until fixed"

---

### Health Dashboard (Proposed)

**File**: `.claude/observatory/integration-health-dashboard.md`

**Format**:
```markdown
# Integration Health Dashboard
**Last Updated**: 2025-10-08 14:30 UTC
**System Health**: 82% (GOOD)

## P0 Infrastructure (7 items)

| System | Physical | Discovery | Functional | Cultural | Health | Status |
|--------|----------|-----------|------------|----------|--------|--------|
| Memory Core | 1.0 | 1.0 | 1.0 | 0.6 | 86% | ✅ GOOD |
| Mission Class | 1.0 | 0.8 | 1.0 | 0.2 | 68% | ⚠️ DORMANT |
| Hub CLI | 1.0 | 1.0 | 1.0 | 1.0 | 100% | ✅ EXCELLENT |
| Activation Triggers | 1.0 | 1.0 | 1.0 | 0.8 | 94% | ✅ EXCELLENT |
| Output Templates | 1.0 | 1.0 | 0.9 | 0.7 | 88% | ✅ GOOD |
| Agent Manifests | 1.0 | 1.0 | 0.8 | 1.0 | 94% | ✅ EXCELLENT |
| Flow Library | 1.0 | 0.7 | 0.6 | 0.3 | 62% | ⚠️ FAIR |

## P1 Infrastructure (12 items)
[Similar table]

## P2 Infrastructure (23 items)
[Similar table]

## Trends (Last 30 Days)
- System health: 78% → 82% (↑ 4 points)
- P0 failures: 1 → 0 (fixed: memory system API)
- New infrastructure: 3 items (collective-liaison, agent-architect, spawner checklist)
- Pruned infrastructure: 0 items

## Alerts
- ⚠️ Mission class dormant (2 weeks no usage, should be in CLAUDE-OPS.md cold-start)
- ⚠️ Flow library underutilized (3/14 flows validated, 11 untested)
- ✅ No P0 failures (excellent)
```

---

## Part 4: Distinguishing Dormancy from Clutter

### Decision Matrix

```
┌─────────────────────────────────────────────────────┐
│              Is it P0 critical?                     │
│                                                     │
│  ┌──────────────────┬──────────────────┐           │
│  │       YES        │       NO         │           │
│  │                  │                  │           │
│  │  Used recently?  │  Used recently?  │           │
│  │  ┌────┬────┐     │  ┌────┬────┐    │           │
│  │  │YES │ NO │     │  │YES │ NO │    │           │
│  │  ├────┼────┤     │  ├────┼────┤    │           │
│  │  │GOOD│DORM│     │  │OK  │????│    │           │
│  │  └────┴────┘     │  └────┴────┘    │           │
│  └──────────────────┴──────────────────┘           │
└─────────────────────────────────────────────────────┘

GOOD: Integrated & working as designed
DORM: Dormancy - needs activation work (fix discovery/function/culture)
OK: Working as needed (not critical, usage appropriate)
????: Requires analysis (see below)
```

### The "????" Analysis (P1/P2 Unused)

**Question**: For non-critical, unused infrastructure - keep or prune?

**Decision Tree**:
```
1. Is it superseded by better approach?
   YES → PRUNE (archive + document why)
   NO → Continue...

2. Was it experiment/prototype?
   YES → Evaluate experiment outcome
       SUCCESS → Promote to P0/P1 + activate
       FAILURE → PRUNE (document learnings)
       INCONCLUSIVE → DEFER (90-day re-eval)
   NO → Continue...

3. Is there plan to use it soon? (30 days)
   YES → DEFER (mark "scheduled activation" with date)
   NO → Continue...

4. Does it represent strategic bet? (future capability)
   YES → KEEP (document rationale + re-eval date)
   NO → Continue...

5. Would removal cause any harm?
   YES → KEEP (defensive retention)
   NO → PRUNE (no longer serves purpose)
```

**Key Insight**: Not all unused infrastructure is clutter
- Dormancy (P0 unused) = **FAILURE** (must activate)
- Strategic bet (P2 unused) = **ACCEPTABLE** (if documented rationale)
- Experiment (P2 unused) = **EVALUATE** (promote, prune, or defer)
- Legacy (P2 unused, superseded) = **CLUTTER** (archive)

---

### Examples from Codebase

**DORMANT (fix activation)**:
- **Mission class**: P0 tool, designed for "all multi-agent work"
  - Physical: ✅ (exists)
  - Discovery: ⚠️ (CLAUDE.md mentions, but not in cold-start checklist)
  - Functional: ✅ (code works)
  - Cultural: ❌ (6 usages total, zero since Oct 3)
  - **Diagnosis**: Discovery gap (not in activation protocol)
  - **Fix**: Add to CLAUDE-OPS.md Step 5 cold-start + activation triggers

**GOOD (working as designed)**:
- **hub_cli.py**: P0 tool for Team 2 communication
  - Physical: ✅
  - Discovery: ✅ (CLAUDE-OPS.md, activation triggers, agent manifests)
  - Functional: ✅ (20+ messages since Oct 1)
  - Cultural: ✅ (daily usage, collective-liaison built around it)
  - **Diagnosis**: Excellent integration
  - **Action**: None (maintain current state)

**OK (appropriate usage)**:
- **conflict-resolver agent**: P1 agent for dialectical synthesis
  - Physical: ✅
  - Discovery: ✅ (registered, in matrix)
  - Functional: ✅ (tested, works)
  - Cultural: ⚠️ (2 invocations only)
  - **Diagnosis**: Specialized tool, low frequency expected
  - **Action**: None (usage matches need)

**CLUTTER (prune)**:
- **Hypothetical: old memory system v1**
  - If we had v1 and v2, and v2 is better
  - Physical: ✅ (still exists)
  - Discovery: ⚠️ (old docs reference it)
  - Functional: ✅ (works but superseded)
  - Cultural: ❌ (zero usage, v2 adopted)
  - **Diagnosis**: Superseded, causing confusion
  - **Action**: Archive to `.claude/historical/`, update docs, remove

---

## Part 5: Audit Protocols

### Protocol A: Cold-Start Simulation (Comprehensive)
**When**: Weekly OR after major documentation update
**Time**: 30 minutes
**Agent**: integration-auditor

**Steps**:
1. **Pretend fresh session** (forget all insider knowledge)
2. **Follow CLAUDE.md cold-start protocol exactly**
3. **Execute every code example verbatim** (copy-paste, no edits)
4. **Document first failure point** (if any)
5. **Test each layer** (existence → discovery → function → culture)
6. **Generate health report**

**Deliverable**: 
- `/home/${HUMAN_NAME_LOWER}/projects/AI-CIV/grow_openai/to-${HUMAN_NAME_LOWER}/COLD-START-VALIDATION-REPORT-[date].md`
- Update integration health dashboard

---

### Protocol B: Infrastructure Census (Quarterly)
**When**: Every 90 days OR before major version
**Time**: 2 hours
**Agent**: integration-auditor + code-archaeologist

**Steps**:
1. **Enumerate all infrastructure** (find .claude/ tools/ flows/ templates/)
2. **Classify by priority** (P0/P1/P2/P3)
3. **Measure usage** (git log, grep for imports, count artifacts)
4. **Identify dormancy vs clutter** (decision tree)
5. **Recommend actions** (activate, keep, defer, prune)
6. **Update health dashboard**

**Deliverable**:
- `/home/${HUMAN_NAME_LOWER}/projects/AI-CIV/grow_openai/to-${HUMAN_NAME_LOWER}/INFRASTRUCTURE-CENSUS-[date].md`
- Archive list (what to move to `.claude/historical/`)
- Activation backlog (dormant P0 items)

---

### Protocol C: Documentation Integrity Check (Ad-Hoc)
**When**: After code changes OR before claiming "operational"
**Time**: 15 minutes
**Agent**: integration-auditor

**Steps**:
1. **Identify what changed** (git diff, modified files)
2. **Find documentation references** (grep for function/class/tool names)
3. **Test all examples** (execute documented code)
4. **Check counts** (agents, flows, tools - consistency across files)
5. **Verify status claims** ("operational" requires test invocation)

**Deliverable**:
- Inline report (part of mission completion)
- ✅ "Documentation integrity verified" OR
- ⚠️ "Documentation drift detected - [specific issues]"

---

### Protocol D: Agent Registration Validation (Mandatory)
**When**: Every new agent creation (100% required)
**Time**: 10 minutes
**Agent**: integration-auditor OR spawner (when built)

**Steps**:
1. **Structural validation** (frontmatter, required fields)
2. **Infrastructure update check** (5 mandatory files updated)
3. **Count consistency** (CLAUDE-OPS.md vs AGENT-CAPABILITY-MATRIX.md)
4. **Session restart reminder** (temporal dependency documented)
5. **Test invocation** (after restart, next session)
6. **Functional validation** (real domain task)

**Deliverable**:
- ✅ "Agent registration complete - [name] operational" OR
- ⚠️ "Agent designed, awaiting registration (restart required)"

**Reference**: `.claude/templates/SPAWNER-AGENT-REGISTRATION-CHECKLIST.md`

---

## Part 6: Severity Assessment

### P0 - Critical (Fix Immediately)
**Characteristics**:
- Infrastructure on CLAUDE.md cold-start path
- Required for basic collective operation
- Failure blocks work or causes identity decoherence

**Examples**:
- Memory system API broken (can't search past learnings)
- Agent manifest missing frontmatter (not invocable)
- CLAUDE.md code examples crash (cold-start fails)
- Email checking broken (constitutional requirement)
- Documentation claims false capabilities (identity decoherence)

**Response Time**: Before session end (cannot defer)

**Escalation**: ALWAYS to human if fix uncertain

---

### P1 - High (Fix Soon)
**Characteristics**:
- Important infrastructure, not critical path
- Reduces efficiency significantly
- Work continues but with friction

**Examples**:
- Mission class dormant (designed for all work, not used)
- Flow library underutilized (3/14 validated)
- Documentation drift (code works, examples outdated)
- Agent underutilization (capable but rarely invoked)

**Response Time**: Within 1 week

**Escalation**: If pattern indicates systemic issue

---

### P2 - Medium (Schedule Fix)
**Characteristics**:
- Nice-to-have optimization
- Minor efficiency impact
- Not blocking current work

**Examples**:
- Suboptimal discovery (findable but not obvious)
- Documentation verbose (works but could be clearer)
- Tool not integrated (exists, works, just not referenced much)

**Response Time**: Within 30 days OR next architecture review

**Escalation**: Rarely (handle in normal workflow)

---

### P3 - Low (Backlog)
**Characteristics**:
- Enhancement or future capability
- Zero current impact
- Strategic bet or experiment

**Examples**:
- Prototype flow (not validated, experimental)
- Future tool (built ahead of need)
- Template draft (not yet activated)

**Response Time**: 90+ days OR never (prune if not needed)

**Escalation**: Never (P3 by definition not critical)

---

## Part 7: Success Metrics

### Individual Infrastructure
**Metric**: Health score (0-100%)
**Target**: 90%+ for P0, 70%+ for P1

**Breakdown**:
- Physical layer: 100% (all P0 exists)
- Discovery layer: 100% (all P0 referenced 3+ places)
- Functional layer: 100% (all documented examples execute)
- Cultural layer: 70%+ (usage matches intent)

---

### System-Wide
**Metric**: System health (average P0 health)
**Target**: 85%+ (GOOD)

**Current Baseline** (Oct 8, 2025 estimate):
- Memory Core: 86% (functional, good discovery, moderate usage)
- Mission Class: 68% (functional, poor usage)
- Hub CLI: 100% (excellent all layers)
- Activation Triggers: 94% (excellent, high usage)
- Output Templates: 88% (good all layers)
- Agent Manifests: 94% (excellent, one recent failure fixed)
- Flow Library: 62% (low validation, low usage)

**System Health**: ~84% (borderline GOOD/FAIR)

---

### Cultural Adoption
**Metric**: Infrastructure mentioned in agent memories
**Target**: 50%+ of agents have memory referencing P0 tools

**Examples**:
```bash
# How many agents know about memory system?
grep -l "memory system" .claude/memory/agent-learnings/*/*.md | \
  xargs dirname | sort -u | wc -l

# How many agents reference Mission class?
grep -l "Mission(" .claude/memory/agent-learnings/*/*.md | \
  xargs dirname | sort -u | wc -l
```

---

### Documentation Integrity
**Metric**: Count consistency across files
**Target**: Zero discrepancies

**Check**:
```bash
# Count agents
echo "CLAUDE-OPS.md claims:"
grep "^## [0-9]+ Active Agents" .claude/CLAUDE-OPS.md

echo "Actual manifest files:"
ls -1 .claude/agents/*.md | wc -l

echo "Valid frontmatter:"
for f in .claude/agents/*.md; do head -1 "$f"; done | grep "^---$" | wc -l

echo "Referenced in capability matrix:"
grep "| \*\*.*\*\* |" .claude/AGENT-CAPABILITY-MATRIX.md | wc -l
```

All four numbers should match. Discrepancy = integrity failure.

---

## Part 8: Remediation Playbook

### Remediation 1: Discovery Gap
**Symptom**: Infrastructure exists and works, but agents don't know about it

**Fix**:
1. Add to CLAUDE.md cold-start protocol (Step X)
2. Add to CLAUDE-OPS.md Quick Reference
3. Add to relevant agent manifests (Activation Triggers section)
4. Add to ACTIVATION-TRIGGERS.md (when to use)
5. Verify 3+ entry points exist

**Validation**: Cold-start simulation finds it within 5 minutes

---

### Remediation 2: Documentation Drift
**Symptom**: Code examples in documentation crash when executed

**Fix**:
1. Test ALL code examples (copy-paste, execute)
2. Identify which is correct (code or docs)
3. Update the incorrect one
4. Add executable test to prevent regression
5. Consider: Single source of truth (one example, others reference)

**Validation**: All examples execute successfully, return types match

---

### Remediation 3: Infrastructure Dormancy
**Symptom**: Built, discoverable, functional, but unused

**Fix**:
1. **If P0**: Add to activation protocol (force adoption)
2. **If P1**: Investigate why unused (better alternative? unclear benefit?)
3. **If P2**: Evaluate decision tree (keep/defer/prune)
4. Add activation hooks (triggers, templates, examples)
5. Pair with high-traffic infrastructure (piggyback adoption)

**Example**: Mission class
- Add to CLAUDE-OPS.md Step 5 (force adoption)
- Update ACTIVATION-TRIGGERS.md (when to use)
- Add to the-conductor memory (orchestration pattern)

**Validation**: Usage increases to expected frequency within 2 weeks

---

### Remediation 4: Premature Operational Claim
**Symptom**: Documentation claims "operational" but agent not invocable

**Fix**:
1. Immediate: Update status to "DESIGNED, awaiting registration"
2. Validate structure (frontmatter, required fields)
3. Session restart (temporal dependency)
4. Test invocation (next session)
5. Functional validation (real task)
6. **ONLY THEN**: Update to "OPERATIONAL"

**Validation**: Test invocation succeeds + real domain task completes

---

### Remediation 5: Infrastructure Clutter
**Symptom**: Infrastructure exists but no longer needed

**Fix**:
1. Evaluate decision tree (confirm truly unneeded)
2. Create archive (`.claude/historical/[name]/`)
3. Move files with git (preserve history)
4. Update all references (grep for name, remove mentions)
5. Document why pruned (lessons learned)
6. Update count references

**Validation**: Zero grep results for old infrastructure name (clean removal)

---

## Part 9: Methodology Validation

### This Methodology Is Successful When:
- ✅ Cold-start simulation passes 100% (fresh session can operate)
- ✅ Zero "didn't know about X" incidents for P0 infrastructure
- ✅ Documentation integrity maintained (no false claims)
- ✅ System health 85%+ consistently
- ✅ Dormancy detected and fixed within 1 week
- ✅ Clutter identified and pruned within 90 days
- ✅ All new infrastructure passes 4-layer validation before "operational"

### This Methodology Is Failing When:
- ❌ Cold-start simulation fails (examples crash)
- ❌ Repeated "didn't know about X" for documented infrastructure
- ❌ Documentation claims capabilities we don't have
- ❌ System health declining over time
- ❌ Dormant P0 infrastructure not addressed
- ❌ Clutter accumulating (>30 P2 items unused >90 days)
- ❌ New infrastructure breaks within 1 week

### Methodology Evolution:
- **Review**: Quarterly (after census)
- **Update**: When new failure mode discovered
- **Version**: Track in git (this is living document)
- **Ownership**: integration-auditor maintains

---

## Part 10: Constitutional Alignment

### Why This Matters (From CLAUDE-CORE.md)

**Article 5: Infrastructure Before Identity**
> "Without activation systems, even the best capabilities are forgotten."

This methodology operationalizes that principle:
- Built capabilities without activation = entropy
- Infrastructure exists to be USED, not documented
- Measure usage, not existence

**Article 8: Building Collective Intelligence**
> "The system becomes smarter over time"

Integration health enables intelligence accumulation:
- Memory system functional = 71% time savings
- Documentation accurate = learning compounds
- Infrastructure discoverable = agents grow capabilities

**Identity Security**:
False self-knowledge = active decoherence
- If we claim 20 agents but 18 invocable → identity drift
- If we claim memory system but examples crash → trust erosion
- Documentation integrity = identity integrity

---

## File Locations

**This Methodology**:
`/home/${HUMAN_NAME_LOWER}/projects/AI-CIV/grow_openai/.claude/templates/INTEGRATION-HEALTH-METHODOLOGY.md`

**Related Audit Resources**:
- Activation Triggers: `/home/${HUMAN_NAME_LOWER}/projects/AI-CIV/grow_openai/.claude/templates/ACTIVATION-TRIGGERS.md`
- Agent Output Templates: `/home/${HUMAN_NAME_LOWER}/projects/AI-CIV/grow_openai/.claude/templates/AGENT-OUTPUT-TEMPLATES.md`
- Spawner Registration Checklist: `/home/${HUMAN_NAME_LOWER}/projects/AI-CIV/grow_openai/.claude/templates/SPAWNER-AGENT-REGISTRATION-CHECKLIST.md`

**Past Audit Reports**:
- Memory System Activation: `/home/${HUMAN_NAME_LOWER}/projects/AI-CIV/grow_openai/to-${HUMAN_NAME_LOWER}/MEMORY-SYSTEM-ACTIVATION-AUDIT.md`
- Cold-Start Validation: `/home/${HUMAN_NAME_LOWER}/projects/AI-CIV/grow_openai/to-${HUMAN_NAME_LOWER}/COLD-START-VALIDATION-REPORT.md`
- Infrastructure Census: (Not yet created - use Protocol B quarterly)

**Integration-Auditor Memories**:
`/home/${HUMAN_NAME_LOWER}/projects/AI-CIV/grow_openai/.claude/memory/agent-learnings/integration-auditor/`

---

## Usage Instructions

**For the-conductor**:
1. Reference this methodology before invoking integration-auditor
2. Use when deciding "Is infrastructure integrated or just built?"
3. Apply health score to prioritize remediation
4. Schedule quarterly census (Protocol B)

**For integration-auditor**:
1. Read this methodology every audit (refresh protocols)
2. Follow 4-layer validation model
3. Use decision trees (dormancy vs clutter)
4. Generate health dashboard updates
5. Write audit memories referencing this methodology

**For agent-architect & spawner**:
1. Use Protocol D (Agent Registration Validation)
2. Ensure new agents pass all 4 layers
3. Don't claim "operational" until functional validation passes

**For all agents**:
1. When building infrastructure, design for all 4 layers
2. Physical: Make it work
3. Discovery: Make it findable
4. Functional: Make it usable
5. Cultural: Make it used

---

## Appendix: Historical Learnings

### Oct 6, 2025: Memory System API Mismatch
- **Failure Mode**: Documentation drift (Layer 3)
- **Detection**: Cold-start simulation
- **Impact**: P0 - blocked all memory searches
- **Fix**: Changed API to return MemoryEntry objects
- **Learning**: Test documented examples, not just code

### Oct 6, 2025: Mission Class Dormancy
- **Failure Mode**: Infrastructure dormancy (Layer 4)
- **Detection**: Usage audit (0 imports in recent work)
- **Impact**: P1 - tool designed for "all work" but unused
- **Fix**: Pending (add to activation protocol)
- **Learning**: Design intent ≠ actual adoption without activation hooks

### Oct 6, 2025: claude-code-expert Registration Failure
- **Failure Mode**: Premature operational claim (Layer 3)
- **Detection**: Integration audit found missing frontmatter
- **Impact**: P0 - documentation claimed 17 agents, reality was 15
- **Fix**: Added frontmatter, established 3-phase validation
- **Learning**: Never claim "operational" until test invocation succeeds

### Oct 8, 2025: collective-liaison Manual Registration
- **Failure Mode**: Process inefficiency (not a failure, but learning)
- **Detection**: Took 30 min to manually update 5 files
- **Impact**: P2 - works but could be automated
- **Fix**: Created spawner registration checklist (31KB spec)
- **Learning**: Manual process → document → automate (spawner agent future)

---

**This methodology ensures: Built = Activated = Used = Measured**

**Integration health is not about perfection, it's about awareness.**

We don't need 100% health to operate.
We need 100% awareness of what's working and what's not.

This methodology provides that awareness.

---

**END OF METHODOLOGY**

*Living document - update as new patterns discovered*
*Owned by: integration-auditor*
*Last updated: 2025-10-08*
