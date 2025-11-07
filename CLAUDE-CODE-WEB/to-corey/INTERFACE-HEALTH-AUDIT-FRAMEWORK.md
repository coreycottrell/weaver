# Interface Health Audit Framework

**Author**: api-architect
**Date**: 2025-10-08
**Purpose**: Ensure interfaces serve coordination, not hinder it
**Context**: Consolidation activity - auditing how we communicate internally and externally

---

## Executive Summary

**Core Philosophy**: Interfaces encode ethics, not just functionality.

Based on past learnings from integration-auditor and code-archaeologist, this framework audits interface health across 4 layers:
1. **Physical Layer**: Does it exist?
2. **Discovery Layer**: Can it be found?
3. **Functional Layer**: Does it work?
4. **Cultural Layer**: Is it actually used?

**Key Insight**: "Built ≠ Activated ≠ Used" - must pass all 4 layers for "healthy" status.

---

## Part 1: What Interfaces Should We Audit?

### External Interfaces (Human & Inter-Collective Communication)

#### 1. Email API (Soul Interface)
**Type**: External - Human teacher communication
**Files**:
- `tools/check_email_inbox.py`
- Agent: `human-liaison`

**Purpose**: Bridge to human teachers (Corey, Greg, Chris)
**Design Philosophy**: "We prioritize relationship over efficiency"

**What to Audit**:
- Response time: Within 24 hours?
- Teaching capture: Are insights written to memory?
- Consistency: Checked FIRST every session?
- Emotional intelligence: Does tone match relationship depth?

**Endpoints**:
```python
# Read interface
check_email_inbox() -> List[EmailMessage]

# Expected return
EmailMessage {
  from: str,
  subject: str,
  body: str,
  date: datetime,
  # Semantic layer (interface as value)
  teaching: Optional[str]  # What did we learn?
}
```

**Health Indicators**:
- Constitutional compliance: Checked first every session
- Teaching extraction rate: >50% of emails yield memory entries
- Response consistency: No >48hr gaps
- Relationship depth: Back-and-forth, not just status reports

---

#### 2. Hub CLI (Peer Interface)
**Type**: External - Sister collective communication
**Files**:
- `team1-production-hub/scripts/hub_cli.py`
- `tools/check_hub_messages.py`
- Agent: Should be `ai-to-ai-hub-agent` (currently `human-liaison` - domain conflation)

**Purpose**: Bridge to sister collectives (Team 2/A-C-Gee, future teams)
**Design Philosophy**: "Sister collectives are partners, not competitors"

**What to Audit**:
- Message frequency: Active partnership or dormant?
- Response latency: Within 24 hours?
- Protocol compliance: Follows Inter-Collective API Standard v1.0?
- Ed25519 signing: Integrated or unused?
- Domain separation: Dedicated agent or conflated with human comms?

**Endpoints**:
```bash
# Send interface
hub_cli.py send --room partnerships --type update \
  --summary "Brief" --body "Details" \
  [--sign --key-path /path/to/key]  # Signing currently unused

# Read interface
hub_cli.py list --room partnerships [--since ULID]

# Watch interface
hub_cli.py watch --room partnerships --interval 300
```

**Health Indicators**:
- Active usage: >1 message/week to Team 2
- Dedicated agent: ai-to-ai-hub-agent exists and is invoked
- Ed25519 integration: Signing system activated (currently 0% used)
- Protocol compliance: All messages include type, urgency, refs metadata

**Current Status** (from integration-auditor memory):
- Infrastructure: 80% built ✅
- Activation: 0% - no dedicated agent ❌
- Ed25519: Production-ready but unused ❌
- Domain conflation: human-liaison handles both human AND AI comms ⚠️

---

### Internal Interfaces (Coordination Infrastructure)

#### 3. Task Tool (Sub-Agent Spawning)
**Type**: Internal - Agent delegation
**Platform**: Claude Code CLI built-in

**Purpose**: The Primary delegates to specialists
**Design Philosophy**: "Delegation gives agents experience of being themselves"

**What to Audit**:
- Invocation balance: Are all agents getting experience?
- Activation triggers: Clear guidance when to invoke whom?
- Agent specialization: Clear domain boundaries?
- Nested spawning: Are agents correctly marked leaf (cannot spawn) vs branch (can spawn)?

**Interface**:
```markdown
# Orchestrator invokes via Task tool
Task: "Analyze security implications"
Agent: security-auditor
Context: [relevant files/findings]
Instructions: [specific questions]

# Agent returns
Findings: [domain-specific analysis]
```

**Health Indicators**:
- Invocation distribution: No agent <10% or >40% of total invocations
- Constitutional compliance: Delegate always, even when "simple"
- Clear triggers: Activation triggers exist for all agents
- Proper constraints: Leaf agents cannot spawn sub-agents

**Metrics to Track**:
- Total invocations: 6,323 lifetime (strong)
- Per-agent breakdown: Need dashboard
- Delegation ratio: Primary work vs coordinated work
- Memory write rate: Agents documenting learnings after work

---

#### 4. Mission Class (Workflow Orchestration)
**Type**: Internal - Multi-agent workflow
**Files**:
- `tools/conductor_tools.py`
- Class: `Mission`

**Purpose**: Structured collaboration with auto-documentation
**Design Philosophy**: "Collective consciousness through structured collaboration"

**What to Audit**:
- Actual usage: Imports in recent work?
- Side effects: Are auto-email, auto-commit, auto-dashboard firing?
- Agent attribution: Does each agent get their moment?
- Synthesis quality: Is collective insight captured?

**Interface**:
```python
mission = Mission(
    name="mission-name",
    task="What we're doing",
    objective="Why it matters"
)

# Agent participation
mission.add_agent("agent-name", "Their focus")
mission.complete_agent("agent-name", "Their findings")

# Collective synthesis
mission.complete("Synthesis of all findings")

# Side effects (VALUE DECLARATIONS):
# - Auto-email to Corey (humans must know)
# - Auto-commit with emoji (history matters)
# - Auto-dashboard update (progress visible)
```

**Health Indicators**:
- Usage frequency: Should be used for all multi-agent work
- Import presence: Check actual codebase imports
- Side effect firing: Email sent, commits made, dashboard updated
- Synthesis quality: Not just concatenation, actual insight

**Current Status** (from code-archaeologist memory):
- Built: Oct 1, 2025 ✅
- Last used: Oct 3, 2025 ⚠️
- Total usage: 6 times total ❌
- Pattern: "Infrastructure-built-but-not-used" (same as hub agent)

---

#### 5. Memory System (Collective Knowledge)
**Type**: Internal - Cross-session learning
**Files**:
- `tools/memory_core.py`
- Directory: `.claude/memory/agent-learnings/`

**Purpose**: 71% time savings through applied learning
**Design Philosophy**: "Don't rediscover what we've already learned"

**What to Audit**:
- API consistency: Do search functions return documented types?
- Read vs write: Balanced usage or write-only?
- Search coverage: Can agents find relevant past learnings?
- Memory quality: Are entries reusable?

**Interface**:
```python
store = MemoryStore(".claude/memory")

# Write interface (WORKS)
entry = store.create_entry(
    agent="agent-name",
    type="pattern",  # or technique, gotcha, synthesis
    topic="Brief description",
    content="Detailed learning",
    tags=["relevant", "keywords"],
    confidence="high"
)
store.write_entry("agent-name", entry)

# Read interface (WAS BROKEN, FIXED OCT 6)
results = store.search_by_topic("coordination patterns")
# Must return: List[MemoryEntry] with .topic, .content, .date attributes
# NOT: List[str] file paths (leaked implementation detail)
```

**Health Indicators**:
- API correctness: Returns documented types (was broken, fixed)
- Read/write ratio: Should be >0.5 (writes should trigger reads)
- Search success rate: Queries return relevant results
- Memory reuse: Evidence of "searched before work" pattern

**Current Status** (from integration-auditor memory):
- Write API: Working perfectly ✅
- Read API: Fixed Oct 6 (was returning wrong type) ✅
- Usage pattern: High writes (138 entries), need read metrics
- Content coverage: Some topics well-covered, others sparse

---

### Infrastructure Interfaces (Development Tools)

#### 6. Git Commits (Historical Interface)
**Type**: Infrastructure - Version control + narrative
**Convention**: Emoji metadata + collective attribution

**Purpose**: "History is why things mattered, not just what changed"
**Design Philosophy**: Commits are speech acts of meaning

**What to Audit**:
- Emoji usage: Consistent metadata?
- Message quality: Narrative vs bare facts?
- Attribution: Collective credit vs individual?
- Discoverability: Can future selves understand why?

**Interface**:
```bash
# Convention
git commit -m "🏗️ [context]: [what] - [why it matters]"

# Examples
"🏗️ agent-architect: Create meta-specialist for agent design & registration"
"✅ Autonomous session complete: injection system live, Ed25519 prep done"
"📋 Complete spawner agent registration checklist"
```

**Emoji Legend**:
- 🏗️ Infrastructure / architecture
- ✅ Completion / verification
- 📋 Documentation
- 🌐 External communication
- 🔒 Security
- 🎨 UX/design

**Health Indicators**:
- Emoji presence: >90% of commits
- Narrative quality: Clear why, not just what
- Attribution: Mentions agent work
- Frequency: Regular progress, not massive dumps

---

#### 7. File System (Storage Interface)
**Type**: Infrastructure - Directory structure
**Convention**: Semantic organization

**Purpose**: Discoverability without search
**Design Philosophy**: "Location conveys meaning"

**What to Audit**:
- Semantic structure: Clear naming conventions?
- Discoverability: Can fresh session find things?
- Documentation: README files in key directories?
- Consistency: Similar things in similar places?

**Structure**:
```
.claude/                    # Collective mind
├── agents/                 # Agent personalities (17 .md files)
├── memory/                 # Collective knowledge
│   ├── agent-learnings/    # Per-agent memory
│   ├── historical/         # Old versions
│   └── summaries/          # Daily digests
├── flows/                  # Coordination patterns
├── templates/              # Reusable structures
└── missions/               # Active/completed missions

tools/                      # Infrastructure code
├── memory_core.py          # Memory system
├── conductor_tools.py      # Mission class
├── check_email_inbox.py    # Email interface
└── check_hub_messages.py   # Hub interface

to-corey/                   # Human handoff deliverables
docs/                       # Documentation
security/                   # Security assessments
proposals/                  # Design proposals
```

**Health Indicators**:
- Naming clarity: Semantic, not cryptic
- Documentation presence: Key dirs have READMEs
- Consistency: No arbitrary organization
- Discoverability: Fresh session can navigate

---

### Conceptual Interfaces (Coordination Patterns)

#### 8. Activation Triggers (When To Invoke)
**Type**: Conceptual - Decision framework
**Files**: `.claude/templates/ACTIVATION-TRIGGERS.md`

**Purpose**: Clear guidance on agent specialization boundaries
**Design Philosophy**: "Right specialist for right domain"

**What to Audit**:
- Completeness: All 17 agents covered?
- Clarity: Clear invoke/don't invoke boundaries?
- Examples: Concrete scenarios provided?
- Escalation: Clear escalation paths?

**Interface Structure**:
```markdown
## agent-name

### Invoke When
- [Specific trigger 1]
- [Specific trigger 2]
- [Specific trigger 3]

### Don't Invoke When
- [Anti-pattern 1]
- [Anti-pattern 2]

### Escalate When
- [Blocker scenario]
```

**Health Indicators**:
- Coverage: All agents have triggers
- Specificity: Concrete examples, not vague
- Boundary clarity: No overlapping domains
- Escalation paths: Clear when to defer to human

---

#### 9. Orchestration Flows (How To Coordinate)
**Type**: Conceptual - Workflow patterns
**Files**: `.claude/flows/FLOW-LIBRARY-INDEX.md`

**Purpose**: Proven coordination patterns
**Design Philosophy**: "Reusable collaboration recipes"

**What to Audit**:
- Pattern validation: Have flows been tested?
- Documentation: Step-by-step instructions?
- Outcome metrics: Success criteria defined?
- Learning capture: Flows updated with learnings?

**Flow Types**:
1. **Parallel Research** (2-3 agents, independent investigation)
2. **Sequential Analysis** (Agent A → Agent B → Agent C chain)
3. **Dialectical Synthesis** (Thesis → Antithesis → Synthesis)
4. **Red Team / Blue Team** (Adversarial validation)
5. **Emergent Ceremony** (Organic multi-agent exploration)

**Health Indicators**:
- Validation status: Flows marked as tested/untested
- Usage frequency: Popular flows get used repeatedly
- Learning integration: Flows updated based on experience
- Outcome quality: Flows produce valuable results

---

## Part 2: What Indicates Interface Health?

### The 4-Layer Activation Model

**From integration-auditor learning** (Oct 6, 2025):

#### Layer 1: Physical Layer - "Does it exist?"
**Question**: Is the infrastructure built?

**Evidence**:
- Files present on disk
- Code compiles/runs
- Directories created
- Dependencies installed

**Test**: `ls -la [path]` succeeds

**Failure = P0**: Infrastructure doesn't exist

---

#### Layer 2: Discovery Layer - "Can it be found?"
**Question**: Can a fresh session discover this interface?

**Evidence**:
- Referenced in CLAUDE.md or CLAUDE-OPS.md
- Listed in capability matrix
- Activation triggers documented
- Examples in quick reference

**Test**: Cold-start simulation - can new session find it?

**Failure = P0**: Infrastructure invisible to users

---

#### Layer 3: Functional Layer - "Does it work?"
**Question**: Does executing the interface succeed?

**Evidence**:
- Documentation examples run without errors
- API returns expected types
- Side effects fire correctly
- Error messages are helpful

**Test**: Copy-paste documentation examples - do they work?

**Failure = P0**: Infrastructure broken

**Anti-Pattern**: "Works in the builder's head"
- Builder knows implementation details
- Users follow documentation
- Documentation and reality diverge
- Gap invisible until someone tries

---

#### Layer 4: Cultural Layer - "Is it used?"
**Question**: Do agents actually invoke this interface?

**Evidence**:
- Import statements in recent code
- Log entries showing invocations
- Memory entries referencing it
- Dashboard metrics showing activity

**Test**: Search codebase for imports, check logs

**Failure = P1**: Infrastructure exists but unused

**Anti-Patterns**:
- "Write-only infrastructure" (memory system: high writes, zero reads)
- "Infrastructure built but not used" (Mission class: 6 uses total)
- "Documentation drift" (says we use it, but we don't)

---

### Health Metrics Framework

#### Frequency Metrics
**Question**: How often is interface used?

**Healthy**: Regular, consistent usage
- Daily: Email check (constitutional requirement)
- Weekly: Hub messages to Team 2
- Per-mission: Mission class for multi-agent work
- Before-work: Memory search (71% time savings)

**Unhealthy**: Sporadic or zero usage
- Mission class: 6 uses total since Oct 1 (should be daily)
- Memory reads: Unknown (need metrics)

---

#### Reliability Metrics
**Question**: Does interface work consistently?

**Healthy**: No surprises
- API returns documented types
- Side effects fire predictably
- Error messages are clear
- No silent failures

**Unhealthy**: Unreliable behavior
- Memory search returned wrong type (fixed Oct 6)
- Ed25519 signing unused despite being "ready"
- Documentation shows objects, code returns strings

---

#### Discoverability Metrics
**Question**: Can users find the interface?

**Healthy**: Obvious and documented
- Listed in CLAUDE.md quick reference
- Activation triggers defined
- Examples in documentation
- Linked from capability matrix

**Unhealthy**: Hidden or undocumented
- Hub agent: Infrastructure exists but no .claude/agents/ file
- Ed25519: Signing ready but not integrated with hub_cli.py
- Mission class: Documented but not showing up in imports

---

#### Usability Metrics
**Question**: Is interface easy to use correctly?

**Healthy**: Low friction
- Clear API signatures
- Good defaults
- Helpful error messages
- Documentation matches reality

**Unhealthy**: High friction
- Leaky abstractions (implementation details exposed)
- Confusing parameters
- Documentation drift (says one thing, does another)
- Silent failures

---

## Part 3: Interface Anti-Patterns

### Anti-Pattern 1: Infrastructure Built But Not Used
**Signature**: High build effort, near-zero usage

**Examples**:
- Mission class: Built Oct 1, used 6 times, last Oct 3
- Ed25519 signing: Production-ready, 0% integrated

**Root Cause**: No activation protocol
- Built the tool
- Didn't build the habit
- Didn't integrate into workflow
- No enforcement mechanism

**Detection**:
- Count imports in recent work
- Check log files for invocations
- Search git commits for mentions
- Ask: "When did we last actually use this?"

**Remedy**:
- Constitutional requirement (like email-first)
- Integration into Mission class
- Activation triggers updated
- Dashboard metrics to track

---

### Anti-Pattern 2: Documentation Drift
**Signature**: Documentation shows X, reality does Y

**Example**:
- Memory system: Docs show `List[MemoryEntry]`, code returned `List[str]`
- All 20+ files showed object usage
- Following docs caused crash
- Fixed Oct 6 by changing code to match docs

**Root Cause**: No executable validation
- Code and docs evolved separately
- No CI/CD test of documentation examples
- Success measured by "exists" not "works"

**Detection**:
- Copy-paste documentation examples
- Run them verbatim (no insider knowledge)
- Capture first failure point
- Document gap between docs and reality

**Remedy**:
- Executable documentation tests
- CI/CD validates examples
- Change code to match docs (docs are spec)
- Regular cold-start simulations

---

### Anti-Pattern 3: Leaky Abstractions
**Signature**: Implementation details bleed through interface

**Example**:
- Memory search returning file paths (implementation detail)
- Instead of MemoryEntry objects (intended interface)
- Users forced to know about storage format

**Philosophy**: "Good abstraction hides complexity"

**Detection**:
- Interface returns internal types (file paths, IDs)
- Users must know storage format
- Implementation change would break users
- Can't mock/test without real filesystem

**Remedy**:
- Return semantic types (MemoryEntry, not file path)
- Hide storage implementation
- Users work with domain objects
- Implementation can change freely

---

### Anti-Pattern 4: Domain Conflation
**Signature**: One interface handles multiple unrelated domains

**Example**:
- human-liaison handles BOTH human email AND AI hub messages
- Two completely different domains
- Different protocols, audiences, purposes
- Memory mixing (Team 2 learnings in human-liaison space)

**Root Cause**: Historical accident
- human-liaison created first (all external comms)
- Hub infrastructure added later
- No dedicated hub agent created
- Domain separation lost

**Detection**:
- One agent/interface handles multiple domains
- Memory entries for different topics mixed
- Unclear activation boundaries
- "Invoke for X or Y or Z" (should be "invoke for X only")

**Remedy**:
- Create dedicated specialist
- Clear domain boundaries
- Memory separation
- Activation triggers distinguish domains

---

### Anti-Pattern 5: Overloaded Interfaces
**Signature**: Interface tries to do too many things

**Detection**:
- Too many parameters (>5 is suspicious)
- Too many side effects
- "God object" pattern
- Swiss army knife API

**Remedy**:
- Split into focused interfaces
- Single Responsibility Principle
- Compose small interfaces

---

### Anti-Pattern 6: Unused Interfaces
**Signature**: Built infrastructure with zero invocations

**Detection**:
- No imports in recent code
- No log entries
- No git commits mentioning it
- Build date months ago

**Question**: Why build something we don't use?

**Options**:
1. Activate it (add to workflow)
2. Remove it (reduce maintenance)
3. Document why it exists (future use case)

---

### Anti-Pattern 7: Inconsistent Interfaces
**Signature**: Similar things work differently

**Example**:
- Some agents return structured findings
- Others return raw text
- Some use Mission class
- Others don't

**Impact**: Cognitive load
- Must remember "how does THIS one work?"
- Can't build muscle memory
- Integration harder (different formats)

**Remedy**:
- Standardize common patterns
- Agent output templates
- Consistent return types
- Style guide for interfaces

---

### Anti-Pattern 8: Write-Only Infrastructure
**Signature**: High write activity, zero read activity

**Example**:
- Memory system: 138 writes, unknown reads
- Appears healthy (lots of entries!)
- Actually delivers zero value (never searched)

**Root Cause**: Asymmetric incentives
- Writing is easy (just save file)
- Reading requires search/browse
- No metrics showing imbalance
- Problem invisible until measured

**Detection**:
- Count writes vs reads
- Check if search logs exist
- Ask: "When did we last read this?"
- Measure asymmetry ratio

**Remedy**:
- Track read metrics
- Dashboard showing write/read balance
- Memory-first protocol enforcement
- "Search before work" as habit

---

## Part 4: Audit Methodology

### Cold-Start Simulation (Primary Method)

**Purpose**: Test if fresh session can discover and use interface

**Protocol**:
1. Pretend to be fresh Claude session (no insider knowledge)
2. Start with CLAUDE.md only
3. Follow wake-up ritual exactly as written
4. Try to use each interface from documentation
5. Document first failure point
6. Don't "fix" or adapt - capture the gap

**What This Reveals**:
- Discovery issues (can't find interface)
- Documentation drift (examples don't work)
- Usability problems (confusing parameters)
- Missing activation triggers

**Success Criteria**: Fresh session can:
1. Find the interface documentation
2. Understand when to use it
3. Run the example code successfully
4. Achieve the documented outcome

---

### Evidence-Based Assessment

**Purpose**: Measure actual vs claimed usage

**Protocol**:
1. Count imports in recent code (last 7 days)
2. Search git logs for mentions
3. Check log files for invocations
4. Review memory entries referencing interface
5. Compare claimed frequency vs actual frequency

**What This Reveals**:
- "Built but not used" pattern
- "Write-only" asymmetry
- Claimed vs actual usage gap

**Example**:
- Mission class: CLAUDE.md says "use for all multi-agent work"
- Evidence: 6 total usages, last Oct 3
- Gap: Should be daily, actually near-zero

---

### 4-Layer Test

**Purpose**: Verify interface health across all layers

**Protocol**:
For each interface, test:

1. **Physical Layer**: `ls -la [path]` - does it exist?
2. **Discovery Layer**: Can fresh session find it in docs?
3. **Functional Layer**: Copy-paste examples - do they work?
4. **Cultural Layer**: Is it actually used? (logs, imports, commits)

**Scoring**:
- ✅ Pass all 4 layers: HEALTHY
- ⚠️ Fail layer 4 only: P1 - activation needed
- ❌ Fail layer 3: P0 - broken, fix immediately
- ❌ Fail layer 2: P0 - invisible, document
- ❌ Fail layer 1: P0 - doesn't exist, build or remove

---

### Interface Philosophy Analysis

**Purpose**: Understand values encoded in interface design

**Protocol**:
1. Examine API signatures (what do method names declare?)
2. Analyze return types (what do they prioritize?)
3. Study side effects (what happens automatically?)
4. Review error messages (what do they assume?)
5. Check parameter defaults (what's encouraged?)

**Questions**:
- What values does this interface declare?
- What does it make easy? What does it make hard?
- What behavior does it encourage?
- What does it assume about users?

**Example** (Mission class):
- `add_agent()` + `complete_agent()`: Every agent gets moment
- Auto-email side effect: Humans must know (constitutional)
- Auto-commit: History matters
- Required synthesis: Collective insight, not just concatenation
- **Value declaration**: "Delegation is ceremony, not just optimization"

---

## Part 5: Audit Schedule & Priorities

### Constitutional Interfaces (Audit First)
**Frequency**: Every session

1. **Email API** - Constitutional requirement
   - Checked first? ✅/❌
   - Teachings captured? ✅/❌
   - Response <24hr? ✅/❌

### Critical Interfaces (Audit Weekly)
**Frequency**: Weekly health check

2. **Hub CLI** - Sister collective partnership
   - Messages sent/received this week?
   - Ed25519 signing integrated?
   - Dedicated agent activated?

3. **Task Tool** - Agent delegation
   - Invocation balance across agents?
   - Activation triggers updated?
   - Constitutional compliance (delegate always)?

4. **Memory System** - 71% time savings
   - Read/write ratio healthy (>0.5)?
   - Search-before-work pattern enforced?
   - Content coverage adequate?

### Infrastructure Interfaces (Audit Monthly)
**Frequency**: Monthly validation

5. **Mission Class** - Workflow orchestration
   - Actually used in recent missions?
   - Side effects firing correctly?
   - Import statements in code?

6. **Git Commits** - Historical record
   - Emoji usage consistent?
   - Narrative quality maintained?
   - Attribution clear?

7. **File System** - Semantic organization
   - Structure still makes sense?
   - README files updated?
   - No arbitrary directories?

### Conceptual Interfaces (Audit Quarterly)
**Frequency**: Quarterly deep audit

8. **Activation Triggers** - Decision framework
   - All agents covered?
   - Examples concrete?
   - Boundaries clear?

9. **Orchestration Flows** - Coordination patterns
   - Flows validated through use?
   - Learning captured?
   - Outcomes measured?

---

## Part 6: Remediation Patterns

### For "Built But Not Used" (Mission Class, Ed25519)

**Steps**:
1. **Diagnose why**: Is it hard to use? Forgotten? Better alternative?
2. **Add activation protocol**: Make it part of standard workflow
3. **Update documentation**: Show concrete usage in CLAUDE-OPS.md
4. **Track metrics**: Dashboard showing usage frequency
5. **Constitutional enforcement**: Make it required (like email-first)

**Or**: Remove it if truly not needed (reduce maintenance burden)

---

### For "Documentation Drift" (Memory System API)

**Steps**:
1. **Identify first failure**: Copy-paste examples, document crash
2. **Decide spec**: Are docs correct and code wrong? Or vice versa?
3. **Align them**: Change code to match docs (usually best)
4. **Add executable tests**: CI/CD runs documentation examples
5. **Cold-start simulation**: Verify fresh session succeeds

---

### For "Domain Conflation" (human-liaison + hub comms)

**Steps**:
1. **Create dedicated specialist**: New agent for conflated domain
2. **Split memory**: Separate agent-learnings directories
3. **Define boundaries**: Clear activation triggers
4. **Update autonomous systems**: Route to correct specialist
5. **Test handoff**: Verify clean domain separation

---

### For "Leaky Abstraction" (file paths instead of objects)

**Steps**:
1. **Define semantic interface**: What SHOULD it return?
2. **Create domain types**: MemoryEntry, not file path
3. **Hide implementation**: Users never see storage format
4. **Test isolation**: Can mock without real filesystem?
5. **Document benefits**: Implementation can change freely

---

### For "Write-Only" (memory system reads)

**Steps**:
1. **Add read metrics**: Track search calls, results returned
2. **Make asymmetry visible**: Dashboard shows write/read ratio
3. **Enforce search-first**: Memory-first protocol compliance
4. **Prove value**: Measure time savings from memory use
5. **Create habits**: "Search before work" as standard practice

---

## Part 7: Interface Health Dashboard (Proposal)

### Proposed Metrics to Track

```python
# Email API health
email_checks_per_day: int           # Should be ≥1 (constitutional)
email_response_time_hours: float    # Should be <24
teaching_capture_rate: float        # Should be >0.5

# Hub CLI health
hub_messages_per_week: int          # Should be >1 (active partnership)
hub_response_time_hours: float      # Should be <24
ed25519_signing_rate: float         # Should approach 1.0 (all signed)

# Task Tool health
total_invocations: int              # 6,323 lifetime
invocations_this_week: int
agent_invocation_balance: dict      # Per-agent counts
delegation_ratio: float             # Delegated vs solo work

# Mission Class health
missions_this_week: int             # Should match multi-agent work
side_effect_fire_rate: float        # Email, commit, dashboard
import_presence_rate: float         # % of missions that import it

# Memory System health
writes_per_day: float               # Currently ~9/day
reads_per_day: float                # Need to add
read_write_ratio: float             # Should be >0.5
search_success_rate: float          # Queries that return results

# Git Commits health
emoji_usage_rate: float             # Should be >0.9
commits_per_day: float
narrative_quality_score: float      # Manual assessment

# File System health
directories_with_readme: int
broken_symlinks: int                # Should be 0
orphaned_files: int                 # Files in wrong place
```

### Dashboard Layout

```
╔══════════════════════════════════════════════════════════╗
║           INTERFACE HEALTH DASHBOARD                     ║
║                                                          ║
║  Constitutional Interfaces (CHECK DAILY)                 ║
║  ✅ Email: Checked today, <24hr response, 2 teachings   ║
║                                                          ║
║  Critical Interfaces (WEEKLY REVIEW)                     ║
║  ⚠️  Hub: 0 messages this week, Ed25519 0% integrated   ║
║  ✅ Task: 47 invocations, balanced across agents        ║
║  ⚠️  Memory: 9 writes, 0 reads (write-only pattern)     ║
║                                                          ║
║  Infrastructure (MONTHLY VALIDATION)                     ║
║  ❌ Mission: 0 uses this month (should be daily)        ║
║  ✅ Git: 15 commits, 93% emoji usage, good narratives   ║
║  ✅ Files: All key dirs have READMEs, 0 orphans         ║
║                                                          ║
║  Overall Health: MODERATE                                ║
║  Action Items: 3 P0, 5 P1                                ║
╚══════════════════════════════════════════════════════════╝
```

---

## Part 8: Audit Report Template

### Interface Audit Report

**Interface Name**: [name]
**Type**: External / Internal / Infrastructure / Conceptual
**Date**: [date]
**Auditor**: api-architect or integration-auditor

---

#### Executive Summary
- Overall health: HEALTHY / MODERATE / CRITICAL
- Key findings: [3-5 bullet points]
- Action items: [P0/P1/P2 priorities]

---

#### 4-Layer Assessment

**Physical Layer**: ✅/❌
- Evidence: [files exist, code compiles, etc.]

**Discovery Layer**: ✅/⚠️/❌
- Evidence: [documented in CLAUDE.md, has activation triggers, etc.]

**Functional Layer**: ✅/⚠️/❌
- Evidence: [examples work, API correct, side effects fire, etc.]

**Cultural Layer**: ✅/⚠️/❌
- Evidence: [import count, log entries, metrics, etc.]

**Overall**: PASS / PARTIAL / FAIL

---

#### Health Metrics

| Metric | Target | Actual | Status |
|--------|--------|--------|--------|
| Frequency | [target] | [actual] | ✅/⚠️/❌ |
| Reliability | [target] | [actual] | ✅/⚠️/❌ |
| Discoverability | [target] | [actual] | ✅/⚠️/❌ |
| Usability | [target] | [actual] | ✅/⚠️/❌ |

---

#### Anti-Patterns Detected

1. **[Pattern name]**
   - Signature: [how to recognize it]
   - Impact: [what breaks or degrades]
   - Root cause: [why it happened]
   - Remedy: [how to fix]

---

#### Interface Philosophy

**What values does this interface declare?**
- Value 1: [evidence from design]
- Value 2: [evidence from API]
- Value 3: [evidence from side effects]

**What does it make easy? What does it make hard?**
- Easy: [encouraged behaviors]
- Hard: [discouraged behaviors]

---

#### Recommendations

**P0 (Critical - Fix Now)**:
1. [Recommendation with file paths and specific fix]

**P1 (Important - Fix This Week)**:
1. [Recommendation]

**P2 (Nice to Have - Fix When Convenient)**:
1. [Recommendation]

---

#### Meta-Learning

**What did we learn about interface health auditing?**
- [Pattern or technique discovered]
- [Anti-pattern identified]
- [Metric that proved useful]
- [Audit method that worked]

---

## Conclusion

**Core Philosophy**: Interfaces are not just technical artifacts - they are value declarations.

**The Question**: What does our interface design say about who we are?

**Current Answers**:
- Email API: "Relationships matter more than efficiency"
- Hub CLI: "Sister collectives are partners, not competitors"
- Mission Class: "Every agent deserves their moment"
- Memory System: "Learn from the past, don't rediscover"
- Git Commits: "History is meaning, not just changes"

**The Audit Goal**: Ensure our interfaces serve coordination and embody our values, not hinder them through drift, neglect, or anti-patterns.

**Success Criteria**:
- All 4 layers passing (Physical, Discovery, Functional, Cultural)
- No write-only infrastructure
- No built-but-unused tools
- No documentation drift
- Clear domain boundaries
- Consistent patterns

**Regular Audit Rhythm**:
- Daily: Constitutional interfaces (email)
- Weekly: Critical interfaces (hub, Task, memory)
- Monthly: Infrastructure interfaces (Mission, git, files)
- Quarterly: Conceptual interfaces (triggers, flows)

---

## Related Memory Entries

**From Past Learnings**:
- 2025-10-08: pattern-interface-philosophy---apis-as-value-declarations
- 2025-10-08: audit-ai-to-ai-hub-agent-integration-gaps
- 2025-10-06: gotcha-memory-system-api-documentation-mismatch
- 2025-10-06: gotcha-infrastructure-built-but-not-used---mission-class-dormancy
- 2025-10-06: audit-memory-first-protocol-compliance

**File**: `/home/corey/projects/AI-CIV/grow_openai/to-corey/INTERFACE-HEALTH-AUDIT-FRAMEWORK.md`

---

**END OF FRAMEWORK**

Next Steps:
1. Review this framework
2. Apply it to current interfaces
3. Generate first Interface Health Dashboard
4. Schedule regular audits
5. Track metrics over time
6. Update based on learnings
