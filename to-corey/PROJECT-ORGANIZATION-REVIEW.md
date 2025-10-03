# Project Organization Review
**Reviewer**: Task Decomposer Agent
**Date**: 2025-10-03
**Scope**: Complete directory structure analysis and organizational assessment

---

## Executive Summary

**Current State**: The project has grown rapidly with 200+ files across diverse systems (memory, signing, flows, tools, docs). Organization shows patterns of both **intentional structure** and **organic growth artifacts**.

**Key Findings**:
- **Agent duplication**: 14 agents exist in BOTH `/agents/` and `/.claude/agents/`
- **Root clutter**: 20+ deliverable documents scattered at root level
- **Dashboard fragmentation**: 4 separate dashboard-related docs at root
- **Unclear tracking**: Multiple roadmap/tracking systems without clear hierarchy
- **Strong foundations**: Well-organized subsystems (.claude/, tools/, docs/)

**Priority Recommendations**:
1. **P0 - Agent consolidation**: Resolve dual agent directories
2. **P0 - Deliverables archive**: Move completed reports to archive
3. **P1 - Dashboard consolidation**: Unify dashboard documentation
4. **P1 - Tracking hierarchy**: Clarify roadmap → todos → flows relationship

---

## 1. Directory Structure Analysis

### Current Organization Map

```
/home/corey/projects/AI-CIV/grow_openai/
│
├── CLAUDE.md                          # PRIMARY ENTRY POINT (1,200+ lines)
├── INTEGRATION-ROADMAP.md             # ACTIVE PLAN (97 tasks for Week 4)
├── README.md                          # Project overview
│
├── .claude/                           # CLAUDE FRAMEWORK (well-organized)
│   ├── agents/                        # 14 agent definitions
│   ├── flows/                         # 14 coordination flows
│   ├── memory/                        # Memory system (agent-learnings, dev-journal)
│   ├── observatory/                   # Dashboard state management
│   ├── commands/                      # Slash commands (swarm, remember, etc.)
│   ├── hooks/                         # Session lifecycle hooks
│   └── output-styles/                 # Personality modes
│
├── agents/                            # DUPLICATE AGENT DEFINITIONS (15 agents)
│   └── [14 agents + system-librarian.md]
│
├── tools/                             # TOOLS & UTILITIES (well-organized)
│   ├── memory_*.py                    # 5 memory system modules
│   ├── sign_message.py                # Ed25519 signing
│   ├── progress_reporter.py           # Dual-channel reporting
│   ├── conductor_tools.py             # Mission management
│   ├── examples/                      # Working examples
│   └── [10+ documentation files]
│
├── docs/                              # REFERENCE DOCUMENTATION (well-organized)
│   ├── GETTING-STARTED.md             # 25KB onboarding guide
│   ├── INTER-COLLECTIVE-API-STANDARD-v1.0.md  # API specification
│   ├── TEAM2_*.md/txt                 # Team 2 architecture analysis (5 files)
│   ├── agent-collaboration/           # Agent deployment guides
│   ├── claude-code-mastery/           # Output styles guide
│   └── personality/                   # Voice guide, ethics
│
├── to-corey/                          # REPORTS TO HUMAN (60+ files)
│   ├── DAILY-SUMMARY-2025-10-03.md    # Current day summary
│   ├── SESSION-3-COMPLETE-SUMMARY.md  # Session reports
│   ├── [50+ mission completion reports]
│   └── [Agent-specific analyses]
│
├── test-results/                      # FLOW VALIDATION (4 files)
│   ├── FLOW-VALIDATION-SUMMARY.md
│   └── [3 flow test results]
│
├── queue/                             # AUTONOMOUS QUEUE SYSTEM
│   ├── README.md
│   ├── process_queue.sh
│   └── processed/
│
├── web/                               # WEB DASHBOARD
│   ├── app.py
│   └── templates/dashboard.html
│
├── security/                          # SECURITY AUDITS
│   └── memory-audit.jsonl
│
└── [ROOT-LEVEL FILES - see section below]
```

---

## 2. Organizational Inconsistencies

### 2.1 Agent Definition Duplication (CRITICAL)

**Problem**: Agents exist in TWO locations with overlapping but not identical content.

**Locations**:
1. `/.claude/agents/` - 14 files (web-researcher, code-archaeologist, etc.)
2. `/agents/` - 15 files (same 14 + system-librarian.md + communications-coordinator.md)

**Evidence**:
```
/.claude/agents/web-researcher.md       vs    /agents/web-researcher.md
/.claude/agents/task-decomposer.md      vs    /agents/task-decomposer.md
[... 12 more duplicates ...]
```

**Impact**:
- **Risk of divergence**: Updates in one location may not propagate to other
- **Unclear source of truth**: Which is canonical?
- **Wasted space**: ~140KB duplicate content

**Recommended Resolution**:
- `.claude/agents/` appears to be the active registration system (referenced in AGENT-INVOCATION-GUIDE.md)
- `/agents/` may be legacy or alternative source
- **ACTION**: Determine canonical location, consolidate, symlink or deprecate other

---

### 2.2 Root-Level Clutter (HIGH)

**Problem**: 20+ deliverable documents scattered at project root instead of organized in subdirectories.

**Root-Level Deliverables** (should be in archives):
```
Root Level Documents (by category):

DASHBOARD-RELATED (4 files):
- DASHBOARD-README.md
- DASHBOARD-SUMMARY.md
- DASHBOARD-EXAMPLE.md
- DASHBOARD-DELIVERABLES.md

MEMORY SYSTEM (3 files):
- MEMORY-SYSTEM-README.md
- MEMORY-SYSTEM-IMPLEMENTATION-REPORT.md
- CLAUDE-MD-AUDIT-COMPLETE.md

MISSION REPORTS (5 files):
- MISSION-COMPLETE-ADR004.md
- SESSION-COMPLETE.md
- HANDOFF-TO-HUMAN.md
- PRODUCTION-READY-CHECKLIST.md
- INTEGRATION-GUIDE.md

PLANNING DOCUMENTS (3 files):
- loose-game-plan.md
- galaxy_brain_gameplan.md
- 100 AI-CIV_THOUGHTS.md

TEAM 2 COMMUNICATION DRAFTS (3 files):
- brainstorm-message-to-acg.md
- timing-correction-to-acg.md
- draft-response-to-acg.md
- message-to-acg-deliverables.md

DEMO/TEST FILES (2 files):
- demo_memory_retrieval.py
- hello-world.txt
- autonomous-test-success.txt

FLOW DASHBOARD (3 files):
- flow_dashboard.json (data store)
- view_dashboard.py (CLI viewer)
- update_dashboard.py (CLI updater)
- dashboard_demo.sh
```

**Impact**:
- **Discoverability**: Hard to find specific documents
- **Mental overhead**: Root directory lists 30+ files (should be <10)
- **Unclear status**: Are these active, archived, or obsolete?

**Recommended Structure**:
```
/archives/
  /2025-10/
    /dashboard-packaging/
      - DASHBOARD-README.md
      - DASHBOARD-SUMMARY.md
      - DASHBOARD-EXAMPLE.md
      - DASHBOARD-DELIVERABLES.md
    /memory-system/
      - MEMORY-SYSTEM-README.md
      - MEMORY-SYSTEM-IMPLEMENTATION-REPORT.md
    /mission-reports/
      - MISSION-COMPLETE-ADR004.md
      - SESSION-COMPLETE.md

/planning/
  - loose-game-plan.md
  - galaxy_brain_gameplan.md
  - 100 AI-CIV_THOUGHTS.md

/scripts/
  - demo_memory_retrieval.py
  - view_dashboard.py
  - update_dashboard.py
  - dashboard_demo.sh

/drafts/
  - brainstorm-message-to-acg.md
  - timing-correction-to-acg.md
  - draft-response-to-acg.md
```

---

### 2.3 Dashboard Documentation Fragmentation (MEDIUM)

**Problem**: Dashboard has 4+ separate documentation files across 2 locations.

**Files**:
- Root: `DASHBOARD-README.md`, `DASHBOARD-SUMMARY.md`, `DASHBOARD-EXAMPLE.md`, `DASHBOARD-DELIVERABLES.md`
- tools/: `DASHBOARD-QUICK-REFERENCE.md`, `DASHBOARD-INSTALL.md`, `DASHBOARD-SCREENSHOTS.md`, `DASHBOARD-PACKAGE-MANIFEST.md`

**Total**: 8 files, unclear hierarchy

**Recommendation**:
```
/tools/dashboard/
  ├── README.md                 # Primary entry (consolidate DASHBOARD-README + SUMMARY)
  ├── INSTALL.md                # Installation guide
  ├── QUICK-START.md            # Quick reference
  ├── EXAMPLES.md               # Usage examples
  ├── SCREENSHOTS.md            # Visual guide
  └── MANIFEST.md               # Package contents
```

---

### 2.4 Tools Organization (GOOD, minor issues)

**Current State**: `tools/` directory is well-organized with clear subsystems.

**Structure**:
```
tools/
├── Memory System (6 files)
│   ├── memory_core.py
│   ├── memory_search.py
│   ├── memory_quality.py
│   ├── memory_security.py
│   ├── memory_federation.py
│   └── memory_cli.py
│
├── Signing System (5 files)
│   ├── sign_message.py
│   ├── test_signing.py
│   ├── INTEGRATION-GUIDE-SIGNING.md
│   ├── README-SIGNING.md
│   └── SECURITY-THREAT-MODEL.md
│
├── Dashboard (8 files - see 2.3)
│
├── Integration (3 files)
│   ├── progress_reporter.py
│   ├── conductor_tools.py
│   └── examples/adr004_integration_example.py
│
└── Utilities (5 files)
    ├── github_backup.py
    ├── email_reporter.py
    ├── install_signing.sh
    ├── install_dashboard.sh
    └── quick_start_memory.sh
```

**Minor Issues**:
- `README.md` vs `README-SIGNING.md` vs `README-TOOLS.md` - naming inconsistency
- Example files mixed with production code

**Recommendation**:
```
tools/
├── memory/
│   ├── core.py, search.py, quality.py, security.py, federation.py
│   ├── cli.py
│   └── README.md
├── signing/
│   ├── sign_message.py
│   ├── README.md
│   └── SECURITY-THREAT-MODEL.md
├── dashboard/
│   └── [consolidated docs]
├── integration/
│   ├── progress_reporter.py
│   ├── conductor_tools.py
│   └── README.md
├── examples/
│   └── [all example files]
└── scripts/
    └── [install_*.sh, quick_start_*.sh]
```

---

## 3. Project Tracking Assessment

### 3.1 Current Tracking Systems

**Identified Systems**:
1. **INTEGRATION-ROADMAP.md** (ROOT) - 97 tasks, 6 categories, Week 4 target
2. **flow_dashboard.json** (ROOT) - Flow validation tracking (14 flows)
3. **to-corey/DAILY-SUMMARY-*.md** - Day-to-day progress
4. **.claude/memory/summaries/latest.md** - Session memory
5. **Multiple TODO comments in code** (2 found: memory_quality.py, memory_federation.py)

**Relationship Unclear**:
- How does INTEGRATION-ROADMAP relate to flow validation?
- Are flow experiments tasks in the roadmap?
- Where do code TODOs fit?

**Strengths**:
- INTEGRATION-ROADMAP is comprehensive (97 tasks, dependencies clear)
- Flow dashboard provides metrics (success rate, timing, quality)
- Daily summaries create historical record

**Weaknesses**:
- **No single source of truth**: 5 separate tracking locations
- **Manual sync required**: flow_dashboard.json not linked to roadmap
- **Code TODOs orphaned**: No system to surface them
- **Completed items unclear**: What happens to completed roadmap tasks?

---

### 3.2 Recommended Tracking Hierarchy

```
TIER 1: Strategic Roadmap (Weeks/Months)
└── INTEGRATION-ROADMAP.md
    ├── 97 tasks across 6 categories
    ├── Dependencies explicit
    └── Target: Week 4 integration (Oct 24-31)

TIER 2: Tactical Execution (Days/Weeks)
└── flow_dashboard.json
    ├── 14 coordination flows
    ├── Validation status tracking
    └── Performance metrics

TIER 3: Daily Progress (Sessions)
└── .claude/memory/summaries/YYYY-MM-DD.md
    ├── Session accomplishments
    ├── Decisions made
    └── Next actions

TIER 4: Code-Level Tasks (Immediate)
└── TODO tracker (NEW)
    ├── Extract TODOs from code
    ├── Link to roadmap tasks
    └── Auto-generate from grep
```

**Integration Mechanism**:
- Roadmap tasks reference flow IDs (`Flow: knowledge-archaeology`)
- Flow dashboard references roadmap categories (`Category: Flow Validation`)
- Daily summaries link to roadmap progress (`Completed: Task 3.2`)
- Code TODOs map to roadmap tasks (`TODO: Roadmap task 1.4`)

---

## 4. Dependency Map

### 4.1 System Dependencies

```
CLAUDE.md (entry point)
├── Depends on: INTEGRATION-ROADMAP.md (THE PLAN)
├── Depends on: .claude/memory/summaries/latest.md (daily context)
├── Depends on: .claude/AGENT-INVOCATION-GUIDE.md (agent usage)
└── References: 10+ key files

INTEGRATION-ROADMAP.md (active plan)
├── Depends on: Flow validation (test-results/)
├── Depends on: Tool completion (tools/)
└── Blocks: Week 4 integration

Memory System
├── Files: tools/memory_*.py (6 modules)
├── Depends on: PyYAML (external)
├── Used by: 6/14 agents
└── Blocks: Full agent enablement

Signing System
├── Files: tools/sign_message.py + 4 docs
├── Depends on: cryptography library
├── Used by: Hub CLI (planned)
└── Blocks: Secure inter-collective comms

Dashboard System
├── Files: web/app.py + templates
├── Depends on: Flask, Flask-SocketIO
├── Used by: Mission tracking
└── Integration: Observatory state

Flow System
├── Files: .claude/flows/*.md (14 flows)
├── Depends on: Agent registration
├── Tracked by: flow_dashboard.json
└── Blocks: Coordination patterns validation

Agent System
├── Files: .claude/agents/*.md (14 agents)
├── Duplicated in: agents/*.md (15 agents)
├── Used by: All flows, missions
└── CRITICAL DEPENDENCY for everything
```

### 4.2 Circular Dependencies

**None detected** - Good separation of concerns

### 4.3 Orphaned Files

**Potential Orphans** (files with unclear purpose/usage):
```
Root Level:
- hello-world.txt (test artifact?)
- autonomous-test-success.txt (test artifact?)
- demo_memory_retrieval.py (demo or active tool?)

Planning Docs:
- loose-game-plan.md (outdated? superseded by INTEGRATION-ROADMAP?)
- galaxy_brain_gameplan.md (brainstorm or active plan?)
- 100 AI-CIV_THOUGHTS.md (reference or outdated?)

Legacy Agents:
- agents/system-librarian.md (unique to /agents/, not in .claude/agents/)
- agents/communications-coordinator.md (not in .claude/agents/)

Queue System:
- queue/processed/20251002-114916-test-autonomous.txt (single test?)
- queue/last-output.txt (ephemeral?)
```

**Recommendation**: Move to `/archives/prototypes/` or delete if obsolete

---

## 5. Consolidation Opportunities

### 5.1 Agent System Consolidation (P0 - CRITICAL)

**Current Problem**: 14 agents duplicated across 2 directories

**Option A: Unify in .claude/agents/ (RECOMMENDED)**
- `.claude/agents/` is referenced by AGENT-INVOCATION-GUIDE.md
- Consistent with Claude framework structure
- Action: Delete `/agents/` or convert to symlinks

**Option B: Unify in /agents/**
- Shorter path
- Traditional location
- Action: Move `.claude/agents/` to `/agents/`, update all references

**Option C: Keep Both (NOT RECOMMENDED)**
- Implement sync mechanism
- High maintenance burden
- Risk of divergence

**Recommendation**: **Option A** - `.claude/agents/` is canonical
```bash
# Backup current state
mv agents agents.backup

# Create symlink for compatibility
ln -s .claude/agents agents

# Update any hardcoded references to /agents/
grep -r "agents/" --include="*.md" --include="*.py" | grep -v ".claude/agents"
```

---

### 5.2 Dashboard Documentation Consolidation (P1)

**Current**: 8 files across 2 locations
**Target**: Single `tools/dashboard/` directory with clear hierarchy

**Structure**:
```
tools/dashboard/
├── README.md               # Main entry (merge DASHBOARD-README + SUMMARY)
├── INSTALL.md              # Installation (keep as-is)
├── QUICK-START.md          # Quick reference (keep as-is)
├── EXAMPLES.md             # Rename from DASHBOARD-EXAMPLE.md
├── SCREENSHOTS.md          # Keep as-is
├── MANIFEST.md             # Keep as-is
└── DELIVERABLES.md         # Archive or merge into README
```

**Actions**:
1. Create `tools/dashboard/` directory
2. Move all dashboard docs to new location
3. Merge README + SUMMARY + DELIVERABLES into single README
4. Update CLAUDE.md references
5. Add README.md redirect at root if needed

---

### 5.3 Deliverables Archive (P0)

**Current**: 20+ completed reports scattered at root
**Target**: Organized archive by date/topic

**Structure**:
```
archives/
├── 2025-10/
│   ├── sessions/
│   │   ├── SESSION-COMPLETE.md
│   │   ├── HANDOFF-TO-HUMAN.md
│   │   └── [session reports]
│   ├── missions/
│   │   ├── MISSION-COMPLETE-ADR004.md
│   │   └── [mission reports]
│   ├── deliverables/
│   │   ├── memory-system/
│   │   │   ├── MEMORY-SYSTEM-README.md
│   │   │   └── MEMORY-SYSTEM-IMPLEMENTATION-REPORT.md
│   │   ├── dashboard/
│   │   │   └── [4 dashboard docs]
│   │   └── signing/
│   │       └── [signing docs if needed]
│   └── analysis/
│       ├── CLAUDE-MD-AUDIT-COMPLETE.md
│       └── PRODUCTION-READY-CHECKLIST.md
└── planning/
    ├── brainstorms/
    │   ├── 100 AI-CIV_THOUGHTS.md
    │   └── galaxy_brain_gameplan.md
    ├── drafts/
    │   ├── brainstorm-message-to-acg.md
    │   └── [team 2 drafts]
    └── legacy/
        └── loose-game-plan.md
```

**Benefits**:
- Root directory clean (10-15 files vs 35+)
- Historical record preserved
- Easy to find completed work
- Clear what's active vs archived

---

### 5.4 Test & Demo Consolidation (P2)

**Current**: Tests scattered across multiple locations
```
Root: demo_memory_retrieval.py
tools/: test_signing.py, test_memory_integration.py, test_dashboard_install.py
.claude/observatory/: test_dashboard.py
test-results/: 4 flow validation reports
```

**Recommendation**:
```
tests/
├── unit/
│   ├── test_signing.py
│   ├── test_memory_integration.py
│   └── test_dashboard_install.py
├── integration/
│   └── test_dashboard.py
├── flows/
│   └── [4 flow validation results]
└── demos/
    └── demo_memory_retrieval.py
```

---

## 6. Workflow Organization Assessment

### 6.1 Flow System Structure (EXCELLENT)

**Location**: `.claude/flows/`
**Count**: 14 flows + 2 meta files
**Organization**: Clear naming convention

```
.claude/flows/
├── README.md                           # Flow library overview
├── flow-brainstorm-2025-10-02.md       # Design document
├── morning-consolidation.md            # VALIDATED
├── democratic-mission-selection.md     # VALIDATED
│
└── [12 flows with "-needs-testing" suffix]
    ├── parallel-research (validated elsewhere)
    ├── specialist-consultation (validated elsewhere)
    └── [10 untested flows]
```

**Strengths**:
- **Clear naming**: Flow purpose evident from filename
- **Status tracking**: "-needs-testing" suffix shows validation state
- **Categorization**: README organizes by type
- **Validation tracking**: flow_dashboard.json tracks metrics

**Weaknesses**:
- **Naming inconsistency**: 3 validated flows don't have "-needs-testing" suffix removed
- **Missing links**: No direct reference from flow files to dashboard entries
- **Validation results location**: test-results/ separate from flows/

**Recommendations**:
1. Rename validated flows (remove "-needs-testing" suffix)
2. Add flow ID header to each flow file
3. Link flow files to test results
4. Consider `/flows/validated/` vs `/flows/untested/` directories

---

### 6.2 Memory System Organization (EXCELLENT)

**Location**: `.claude/memory/`
**Structure**: Well-designed hierarchy

```
.claude/memory/
├── README.md                    # System guide
├── summaries/                   # Daily summaries
│   └── 2025-10-03.md
├── agent-learnings/             # Per-agent memories
│   ├── README.md
│   ├── web-researcher/
│   ├── security-auditor/
│   └── [12 more agents]
├── dev-journal/                 # Developer diary
│   ├── 2025-10-01-*.md (4 entries)
│   └── 2025-10-02-*.md (2 entries)
├── project-knowledge/           # Long-term knowledge
│   ├── architecture-decisions.md
│   ├── patterns-observed.md
│   └── technical-debt.md
└── .indexes/                    # Search indexes
    ├── inverted-index.json
    ├── agent-index.json
    ├── chronological.json
    └── connection-graph.json
```

**Strengths**:
- **Clear purpose hierarchy**: summaries → learnings → journal → knowledge
- **Agent-centric**: Per-agent directories in learnings/
- **Search optimization**: Pre-built indexes for fast retrieval
- **Documentation**: README explains system

**No changes recommended** - This is well-organized.

---

## 7. Missing Organizational Documentation

### 7.1 Files That Should Exist

**Project Structure Guide** (MISSING)
```
docs/PROJECT-STRUCTURE.md
- Where everything goes
- Directory conventions
- File naming patterns
- When to create new directories
```

**Dependency Graph** (MISSING)
```
docs/DEPENDENCY-GRAPH.md
- Visual diagram of system dependencies
- Build order for new installations
- Impact analysis tool
```

**Archival Policy** (MISSING)
```
docs/ARCHIVAL-POLICY.md
- When to archive vs delete
- Archive structure conventions
- How to find archived content
```

**File Naming Conventions** (MISSING)
```
docs/NAMING-CONVENTIONS.md
- When to use CAPS-WITH-DASHES.md
- When to use lowercase-with-dashes.md
- When to use camelCase.py
- Date formats (YYYY-MM-DD vs other)
```

**Contribution Guide** (MISSING)
```
docs/CONTRIBUTING.md
- How to add new tools
- How to add new agents
- How to add new flows
- How to document work
```

---

## 8. Priority Recommendations

### P0 - Critical (Do Immediately)

**P0-1: Resolve Agent Duplication**
- **Impact**: Prevents divergence, clarifies source of truth
- **Effort**: 30 minutes
- **Action**: Move `.claude/agents/` to canonical location, symlink for compatibility
- **Dependencies**: None
- **Risk**: High if delayed (updates diverge)

**P0-2: Archive Completed Deliverables**
- **Impact**: Cleans root directory, improves discoverability
- **Effort**: 1 hour
- **Action**: Create `/archives/2025-10/` structure, move 20+ files
- **Dependencies**: None
- **Risk**: Low (just reorganization)

**P0-3: Create PROJECT-STRUCTURE.md**
- **Impact**: Prevents future organizational drift
- **Effort**: 1 hour
- **Action**: Document current organization + conventions
- **Dependencies**: Complete after P0-2
- **Risk**: Medium if delayed (new files misplaced)

---

### P1 - Important (Do This Week)

**P1-1: Consolidate Dashboard Documentation**
- **Impact**: Easier dashboard adoption
- **Effort**: 1 hour
- **Action**: Merge 8 files into `/tools/dashboard/` structure
- **Dependencies**: P0-2 (archive old versions)
- **Risk**: Low

**P1-2: Clarify Tracking System Hierarchy**
- **Impact**: Better task management
- **Effort**: 2 hours
- **Action**: Link roadmap ↔ flows ↔ daily summaries
- **Dependencies**: None
- **Risk**: Medium (tracking confusion continues)

**P1-3: Reorganize Tools Directory**
- **Impact**: Clearer tool organization
- **Effort**: 1 hour
- **Action**: Create subdirectories (memory/, signing/, dashboard/)
- **Dependencies**: P1-1 (dashboard consolidation)
- **Risk**: Low

**P1-4: Extract Code TODOs**
- **Impact**: Surfaces hidden technical debt
- **Effort**: 30 minutes
- **Action**: `grep -r "TODO\|FIXME" --include="*.py" > docs/CODE-TODOS.md`
- **Dependencies**: None
- **Risk**: Low

---

### P2 - Nice to Have (Do Next Week)

**P2-1: Consolidate Tests**
- **Impact**: Clearer test organization
- **Effort**: 1 hour
- **Action**: Create `/tests/` directory, move all test files
- **Dependencies**: None
- **Risk**: Low

**P2-2: Create Missing Documentation**
- **Impact**: Better long-term maintainability
- **Effort**: 3-4 hours
- **Action**: Write DEPENDENCY-GRAPH.md, ARCHIVAL-POLICY.md, NAMING-CONVENTIONS.md
- **Dependencies**: P0-3 (PROJECT-STRUCTURE.md)
- **Risk**: Low

**P2-3: Flow Naming Consistency**
- **Impact**: Clearer flow status
- **Effort**: 15 minutes
- **Action**: Rename validated flows (remove "-needs-testing")
- **Dependencies**: None
- **Risk**: Very low

---

## 9. Detailed Action Plan

### Phase 1: Critical Cleanup (Day 1)

**Step 1: Agent Consolidation**
```bash
# Verify .claude/agents/ is complete (14 agents)
ls -1 .claude/agents/*.md | wc -l  # Should be 14

# Backup current /agents/
mv agents agents.backup

# Create symlink
ln -s .claude/agents agents

# Verify symlink works
ls -l agents/web-researcher.md

# Update references (if any)
grep -r "agents/" --include="*.md" --exclude-dir=".git" | grep -v ".claude/agents"
```

**Step 2: Create Archive Structure**
```bash
# Create directory structure
mkdir -p archives/2025-10/{sessions,missions,deliverables,analysis}
mkdir -p archives/2025-10/deliverables/{memory-system,dashboard,signing}
mkdir -p archives/planning/{brainstorms,drafts,legacy}

# Move session reports
mv SESSION-COMPLETE.md archives/2025-10/sessions/
mv HANDOFF-TO-HUMAN.md archives/2025-10/sessions/

# Move mission reports
mv MISSION-COMPLETE-ADR004.md archives/2025-10/missions/

# Move deliverables
mv MEMORY-SYSTEM-*.md archives/2025-10/deliverables/memory-system/
mv DASHBOARD-*.md archives/2025-10/deliverables/dashboard/

# Move analysis
mv CLAUDE-MD-AUDIT-COMPLETE.md archives/2025-10/analysis/
mv PRODUCTION-READY-CHECKLIST.md archives/2025-10/analysis/

# Move planning
mv 100\ AI-CIV_THOUGHTS.md archives/planning/brainstorms/
mv galaxy_brain_gameplan.md archives/planning/brainstorms/
mv loose-game-plan.md archives/planning/legacy/
mv brainstorm-message-to-acg.md archives/planning/drafts/
mv timing-correction-to-acg.md archives/planning/drafts/
mv draft-response-to-acg.md archives/planning/drafts/
mv message-to-acg-deliverables.md archives/planning/drafts/

# Move test artifacts
mkdir -p archives/prototypes
mv hello-world.txt archives/prototypes/
mv autonomous-test-success.txt archives/prototypes/
mv demo_memory_retrieval.py archives/prototypes/
```

**Step 3: Create PROJECT-STRUCTURE.md**
```markdown
# See Section 10 below for full content
```

---

### Phase 2: Documentation Consolidation (Day 2)

**Step 1: Dashboard Consolidation**
```bash
# Create dashboard directory
mkdir -p tools/dashboard

# Move files
mv tools/DASHBOARD-*.md tools/dashboard/
mv DASHBOARD-*.md tools/dashboard/

# Rename for consistency
cd tools/dashboard
mv DASHBOARD-README.md README.md
mv DASHBOARD-INSTALL.md INSTALL.md
mv DASHBOARD-QUICK-REFERENCE.md QUICK-START.md
mv DASHBOARD-EXAMPLE.md EXAMPLES.md
mv DASHBOARD-SCREENSHOTS.md SCREENSHOTS.md
mv DASHBOARD-PACKAGE-MANIFEST.md MANIFEST.md

# Merge DASHBOARD-SUMMARY + DASHBOARD-DELIVERABLES into README
# (Manual edit required)
```

**Step 2: Tools Reorganization**
```bash
# Create subdirectories
mkdir -p tools/{memory,signing,dashboard,integration,examples,scripts}

# Move memory system
mv tools/memory_*.py tools/memory/
mv tools/example_agent_memory_usage.py tools/examples/
mv tools/test_memory_integration.py tools/memory/

# Move signing system
mv tools/sign_message.py tools/signing/
mv tools/test_signing.py tools/signing/
mv tools/*SIGNING*.md tools/signing/
mv tools/SECURITY-THREAT-MODEL.md tools/signing/
mv tools/message-signature-schema.json tools/signing/
mv tools/examples/signing_example.py tools/signing/examples/

# Move integration tools
mv tools/progress_reporter.py tools/integration/
mv tools/conductor_tools.py tools/integration/
mv tools/examples/adr004_integration_example.py tools/integration/examples/

# Move scripts
mv tools/install_*.sh tools/scripts/
mv tools/quick_start_*.sh tools/scripts/

# Update imports in Python files
# (Manual edit required - update import paths)
```

---

### Phase 3: Tracking Integration (Day 3)

**Step 1: Link Roadmap to Flows**
```markdown
# Edit INTEGRATION-ROADMAP.md

Add to each flow-related task:
- Flow ID: [flow-name]
- Dashboard Status: [link to flow_dashboard.json entry]
- Test Results: [link to test-results/ file if exists]

Example:
### Task 3.1: Validate knowledge-archaeology flow
- Flow ID: knowledge-archaeology
- Dashboard Status: See flow_dashboard.json entry "Knowledge Archaeology"
- Test Results: test-results/knowledge-archaeology-test.md
- Dependencies: None
- Status: COMPLETE
```

**Step 2: Extract Code TODOs**
```bash
# Create TODO tracker
grep -r "TODO\|FIXME\|XXX\|HACK" --include="*.py" -n > docs/CODE-TODOS.md

# Format as markdown table
# (Manual edit required)
```

---

## 10. Proposed PROJECT-STRUCTURE.md Content

```markdown
# Project Structure Guide
**Last Updated**: 2025-10-03
**Maintainer**: The Conductor

---

## Directory Hierarchy

### Root Level (Keep Minimal)
**Purpose**: Entry points and active roadmaps only

**Allowed Files**:
- `CLAUDE.md` - Primary entry point for conductor
- `README.md` - Project overview for humans
- `INTEGRATION-ROADMAP.md` - Active integration plan
- `flow_dashboard.json` - Flow tracking data
- `view_dashboard.py`, `update_dashboard.py` - Dashboard CLIs
- Configuration files: `.gitignore`, `.env` (gitignored)

**Temporary Files Allowed**:
- `*.sh` scripts for active development
- Test artifacts during active development

**When to Archive**:
- Mission complete reports → `to-corey/` or `archives/`
- Completed deliverables → `archives/YYYY-MM/deliverables/`
- Brainstorm/draft documents → `archives/planning/`
- Old plans → `archives/planning/legacy/`

---

### /.claude/ - Claude Framework
**Purpose**: Claude Code agent framework components

**Subdirectories**:
- `agents/` - 14 agent definitions (CANONICAL source)
- `flows/` - 14 coordination flow definitions
- `memory/` - Memory system (agent-learnings, dev-journal, summaries)
- `observatory/` - Dashboard state management
- `commands/` - Slash commands (swarm, remember, collective-wisdom)
- `hooks/` - Session lifecycle hooks
- `output-styles/` - Personality modes (conductor, researcher, teacher, creative)

**File Naming**:
- Agents: `[agent-name].md` (lowercase-with-dashes)
- Flows: `[flow-name]-needs-testing.md` or `[flow-name].md` (validated)
- Memory: `YYYY-MM-DD-[description].md` for dated entries

---

### /agents/ - Agent Definitions
**Status**: SYMLINK to `.claude/agents/`
**Purpose**: Compatibility path for historical references
**Do Not Edit**: Modify files in `.claude/agents/` instead

---

### /tools/ - Reusable Tools & Utilities
**Purpose**: Production-ready tools and utilities

**Subdirectories**:
- `memory/` - Memory system modules (5 .py files + README)
- `signing/` - Ed25519 signing system (sign_message.py + docs)
- `dashboard/` - Dashboard documentation (8 files)
- `integration/` - Integration tools (progress_reporter, conductor_tools)
- `examples/` - Working example code
- `scripts/` - Install/setup scripts (.sh files)

**File Naming**:
- Python modules: `[module_name].py` (snake_case)
- Documentation: `README.md`, `INSTALL.md`, `QUICK-START.md` (CAPS-WITH-DASHES)
- Scripts: `[script_name].sh` (snake_case)

**When to Add New Tool**:
1. Create subdirectory if new category
2. Add README.md explaining purpose
3. Update top-level tools/README.md
4. Add entry to CLAUDE.md if conductor-relevant

---

### /docs/ - Reference Documentation
**Purpose**: User-facing documentation and specifications

**Subdirectories**:
- `agent-collaboration/` - Agent deployment guides
- `claude-code-mastery/` - Output styles guide
- `personality/` - Voice guide, ethics principles

**File Types**:
- Guides: `[TOPIC]-GUIDE.md`
- Specifications: `[SPEC-NAME]-v[VERSION].md`
- Analysis: `[SUBJECT]-ANALYSIS.md`
- Quick starts: `[TOPIC]-QUICK-START.md`

**When to Add**:
- External-facing documentation (for A-C-Gee, other collectives)
- Comprehensive specifications
- Architecture analysis
- Onboarding guides

---

### /to-corey/ - Human Reports
**Purpose**: Session summaries, mission reports, agent analyses

**File Types**:
- Daily summaries: `DAILY-SUMMARY-YYYY-MM-DD.md`
- Session reports: `SESSION-N-COMPLETE-SUMMARY.md`
- Mission reports: `[MISSION-NAME]-COMPLETE.md`
- Agent reports: `[agent-name]-[topic].md`
- Benchmarks: `BENCHMARK-*.md`
- Experiments: `experiment-N-[name].md`

**Archival**:
- Move to `archives/YYYY-MM/` after 1 week
- Keep latest 7 days in to-corey/
- Exception: DAILY-SUMMARY-YYYY-MM-DD.md (keep current month)

---

### /test-results/ - Flow Validation Results
**Purpose**: Results from flow experiments

**File Naming**: `[flow-name]-test.md`

**Contents**:
- Execution transcript
- Success metrics
- Lessons learned
- Recommendations

**Link To**:
- INTEGRATION-ROADMAP.md tasks
- flow_dashboard.json entries

---

### /archives/ - Historical Records
**Purpose**: Completed work, outdated plans, prototypes

**Structure**:
```
archives/
├── YYYY-MM/
│   ├── sessions/       # Session complete reports
│   ├── missions/       # Mission complete reports
│   ├── deliverables/   # Completed deliverables (by topic)
│   └── analysis/       # One-time analysis reports
└── planning/
    ├── brainstorms/    # Brainstorm documents
    ├── drafts/         # Communication drafts
    └── legacy/         # Outdated plans
```

**When to Archive**:
- After mission complete
- After deliverable shared
- When plan superseded
- When prototype abandoned

---

### /web/ - Web Dashboard
**Purpose**: Flask web application for real-time dashboard

**Files**:
- `app.py` - Flask application
- `templates/dashboard.html` - Dashboard UI

**Related**:
- `.claude/observatory/dashboard-state.json` - State file
- `tools/dashboard/` - Documentation

---

### /queue/ - Autonomous Queue System
**Purpose**: Asynchronous task queue

**Files**:
- `README.md` - Queue documentation
- `process_queue.sh` - Queue processor
- `processed/` - Completed queue items

---

## File Naming Conventions

### Markdown Documentation
- **CAPS-WITH-DASHES.md**: Primary documentation, guides, specifications
  - Examples: `README.md`, `INTEGRATION-ROADMAP.md`, `GETTING-STARTED.md`
- **lowercase-with-dashes.md**: Flow definitions, agent definitions
  - Examples: `web-researcher.md`, `parallel-research-needs-testing.md`
- **YYYY-MM-DD-description.md**: Dated entries (daily summaries, dev journal)
  - Examples: `2025-10-03-integration-complete.md`, `DAILY-SUMMARY-2025-10-03.md`

### Python Code
- **snake_case.py**: All Python modules
  - Examples: `memory_core.py`, `sign_message.py`, `progress_reporter.py`

### Shell Scripts
- **snake_case.sh**: All shell scripts
  - Examples: `install_dashboard.sh`, `quick_start_memory.sh`

### JSON/JSONL Data
- **kebab-case.json**: Data files
  - Examples: `flow-dashboard.json`, `dashboard-state.json`, `memory-audit.jsonl`

---

## When to Create New Directories

### New Tool Category
```bash
mkdir tools/[category-name]
touch tools/[category-name]/README.md
# Document purpose, usage, dependencies
```

### New Documentation Category
```bash
mkdir docs/[category-name]
touch docs/[category-name]/README.md
# Add overview, link to related docs
```

### New Archive Period
```bash
mkdir archives/YYYY-MM
mkdir archives/YYYY-MM/{sessions,missions,deliverables,analysis}
# Archive completed work from previous month
```

---

## Integration Points

### CLAUDE.md References
- Update when adding new major tools
- Update when changing directory structure
- Keep synchronized with PROJECT-STRUCTURE.md

### INTEGRATION-ROADMAP.md
- Link tasks to flow IDs
- Link tasks to test results
- Link tasks to tool locations

### flow_dashboard.json
- Reference flow file locations
- Link to test results
- Track validation status

---

## Maintenance

### Weekly
- Archive completed missions to `archives/YYYY-MM/missions/`
- Archive old daily summaries (keep latest 7 days)
- Check for new orphaned files at root

### Monthly
- Create new `archives/YYYY-MM/` directory
- Archive previous month's deliverables
- Review and prune legacy plans

### Quarterly
- Review directory structure effectiveness
- Update PROJECT-STRUCTURE.md if patterns changed
- Consolidate archives if needed

---

## Quick Reference

**Where does X go?**
- New agent definition → `.claude/agents/[agent-name].md`
- New coordination flow → `.claude/flows/[flow-name]-needs-testing.md`
- Flow test results → `test-results/[flow-name]-test.md`
- New tool module → `tools/[category]/[module_name].py`
- Tool documentation → `tools/[category]/README.md`
- User guide → `docs/[TOPIC]-GUIDE.md`
- Daily summary → `to-corey/DAILY-SUMMARY-YYYY-MM-DD.md`
- Mission report → `to-corey/[MISSION-NAME]-COMPLETE.md`
- Completed deliverable → `archives/YYYY-MM/deliverables/[topic]/`
- Brainstorm document → `archives/planning/brainstorms/`
- Draft communication → `archives/planning/drafts/`
- Test artifact → `archives/prototypes/`

**What's the canonical source?**
- Agents: `.claude/agents/` (NOT `/agents/`)
- Flows: `.claude/flows/`
- Memory: `.claude/memory/`
- Tools: `tools/[category]/`
- Docs: `docs/`
```

---

## 11. Summary & Next Steps

### Current State
The project has **strong foundational organization** (.claude/, tools/, docs/) but shows signs of **rapid organic growth** at the root level. The core systems (memory, signing, flows) are well-structured, but deliverables and completed work need archival.

### Critical Findings
1. **Agent duplication** (14 agents in 2 locations) - MUST resolve
2. **Root-level clutter** (20+ deliverables) - SHOULD archive
3. **Dashboard fragmentation** (8 files) - SHOULD consolidate
4. **Tracking hierarchy unclear** (5 systems) - SHOULD integrate

### Recommended Immediate Actions
1. **P0-1**: Resolve agent duplication (30 min)
2. **P0-2**: Archive completed deliverables (1 hour)
3. **P0-3**: Create PROJECT-STRUCTURE.md (1 hour)

### Timeline
- **Day 1** (2.5 hours): Complete all P0 tasks
- **Day 2** (2 hours): P1-1 and P1-2 (dashboard + tracking)
- **Day 3** (1.5 hours): P1-3 and P1-4 (tools + TODOs)
- **Week 2**: P2 tasks (tests, documentation, flow naming)

### Success Metrics
- Root directory: <15 files (currently ~35)
- Agent source: Single canonical location
- Dashboard docs: Single directory with clear hierarchy
- Tracking: Clear roadmap → flows → summaries linkage

### Risk Assessment
- **Low risk**: All changes are organizational (no code changes)
- **High value**: Prevents future confusion and technical debt
- **Reversible**: Can roll back via git if needed

---

**End of Report**

**Files Referenced**:
- INTEGRATION-ROADMAP.md (97 tasks)
- CLAUDE.md (1,200+ lines)
- .claude/AGENT-INVOCATION-GUIDE.md
- flow_dashboard.json
- 200+ files across project structure
