# AI-CIV File Location Index

**Purpose**: Quick reference for locating any file in the Team 1 collective.

**Last Updated**: 2025-10-03
**Maintained By**: System Librarian

---

## 📂 Directory Structure Overview

```
/home/corey/projects/AI-CIV/grow_openai/
├── .claude/                    # Internal AI systems
│   ├── flows/                  # Coordination patterns (18 files)
│   ├── memory/                 # Persistent knowledge
│   └── observatory/            # Mission tracking
├── agents/                     # Agent personalities (15 files)
├── docs/                       # Documentation (20+ files)
├── queue/                      # Autonomous task system
├── to-corey/                   # Human-facing reports (16 files)
├── tools/                      # Production tools
└── web/                        # Web dashboard
```

---

## 🛠️ Tools & Utilities (`/tools/`)

### Core Python Tools
- **conductor_tools.py** (195 lines) - Mission management system
  - Mission class for orchestration
  - Integration with Observatory, Email, GitHub

- **email_reporter.py** (362 lines) - Email reporting system
  - HTML report generation
  - Automatic mission summaries

- **github_backup.py** (281 lines) - Git automation
  - Auto-commit and push
  - Smart .gitignore handling

- **sign_message.py** (632 lines) - Ed25519 signing library
  - Cryptographic message signing
  - CLI and Python API

### Testing & Examples
- **test_signing.py** (376 lines) - Ed25519 test suite
  - 10/10 tests passing

- **examples/signing_example.py** (607 lines) - Working examples
  - Signing workflows
  - Verification examples

### Documentation
- **INTEGRATION-GUIDE-SIGNING.md** (515 lines) - Signing integration
- **SECURITY-THREAT-MODEL.md** (968 lines) - Security analysis
- **README-SIGNING.md** (672 lines) - Quick reference
- **ARCHITECTURE-DIAGRAM.txt** (22,952 lines) - Architecture diagrams

### Scripts & Data
- **install_signing.sh** (7,962 lines) - Installation script
- **message-signature-schema.json** (1,998 lines) - JSON schema

---

## 📊 Dashboard & Monitoring (Root + `.claude/observatory/`)

### Flow Dashboard (Root)
- **flow_dashboard.json** (12KB) - Flow tracking data
- **view_dashboard.py** (277 lines) - CLI viewer
- **update_dashboard.py** (348 lines) - CLI updater
- **dashboard_demo.sh** - Interactive demo
- **DASHBOARD-README.md** - Usage guide
- **DASHBOARD-SUMMARY.md** - Summary
- **DASHBOARD-DELIVERABLES.md** - Deliverables
- **DASHBOARD-EXAMPLE.md** - Example output

### Observatory (`.claude/observatory/`)
- **observatory.py** (6,735 lines) - Core state management
- **dashboard.py** (6,670 lines) - Terminal UI
- **test_dashboard.py** (1,632 lines) - Test suite
- **dashboard-state.json** (6,446 lines) - Runtime state
- **README.md** (4,663 lines) - Documentation
- **IMPLEMENTATION.md** (10,740 lines) - Implementation guide

### Web Dashboard (`/web/`)
- **app.py** (3,945 lines) - Flask server
- **templates/** - HTML templates

---

## 🤖 Agent Definitions (`/agents/`)

All agents are markdown personality profiles with capabilities, voice guides, and achievements.

**Research & Analysis:**
- web-researcher.md (2,475 lines)
- code-archaeologist.md (3,636 lines)
- pattern-detector.md (4,405 lines)
- doc-synthesizer.md (8,158 lines)

**Engineering:**
- refactoring-specialist.md (5,883 lines)
- test-architect.md (7,225 lines)
- security-auditor.md (7,043 lines)

**Performance:**
- performance-optimizer.md (10,161 lines)

**Creative & Design:**
- feature-designer.md (7,038 lines)
- api-architect.md (8,748 lines)
- naming-consultant.md (11,333 lines)

**Coordination:**
- task-decomposer.md (11,268 lines)
- result-synthesizer.md (13,566 lines)
- conflict-resolver.md (12,511 lines)

**Library & Knowledge:**
- system-librarian.md (6,923 lines)

---

## 🔄 Coordination Flows (`.claude/flows/`)

### Core Flows
- **README.md** (2,892 lines) - Flow library overview
- **democratic-mission-selection.md** (4,789 lines) - Validated governance flow
- **morning-consolidation.md** (10,057 lines) - Morning sync flow

### Untested Flows (needs-testing)
- archaeological-dig-needs-testing.md (8,746 lines)
- architecture-xray-needs-testing.md (8,023 lines)
- competitive-intelligence-deep-dive-needs-testing.md (6,205 lines)
- contract-first-integration-needs-testing.md (738 lines)
- cross-pollination-synthesis-needs-testing.md (730 lines)
- dialectic-forge-needs-testing.md (725 lines)
- fortress-protocol-needs-testing.md (695 lines)
- knowledge-archaeology-needs-testing.md (722 lines)
- performance-cascade-analysis-needs-testing.md (729 lines)
- recursive-complexity-breakdown-needs-testing.md (736 lines)
- semantic-harmonization-needs-testing.md (723 lines)
- technical-debt-archaeology-needs-testing.md (1,256 lines)
- test-driven-refactoring-gauntlet-needs-testing.md (717 lines)

### Planning & Design
- **flow-brainstorm-2025-10-02.md** (23,290 lines) - Complete brainstorm session

---

## 🧠 Memory System (`.claude/memory/`)

### Root Level
- **README.md** (3,095 lines) - Memory system guide
- **session-context.json** (930 lines) - Current session context
- **user-preferences.md** (836 lines) - User preferences
- **session-summary.md** (11,032 lines) - Session synthesis
- **mission-proposals.md** (5,946 lines) - Mission ideas
- **mission-rankings.md** (12,161 lines) - Democratic vote results
- **memory-system-proposals.md** (12,792 lines) - 4 design proposals
- **comms-systems-evaluation.md** (8,131 lines) - Communication evaluation
- **comms-system-vote-2025-10-02.md** (7,530 lines) - Team 2 Hub vote
- **team2-hub-deployment-2025-10-02.md** (13,715 lines) - Hub deployment

### Project Knowledge (`project-knowledge/`)
- architecture-decisions.md (4,083 lines)
- patterns-observed.md (2,884 lines)
- technical-debt.md (1,144 lines)

### Dev Journal (`dev-journal/`)
- 2025-10-01-initial-build.md (4,136 lines)
- 2025-10-01-completion.md (8,725 lines)
- 2025-10-01-observatory-complete.md (16,344 lines)
- 2025-10-01-second-cycle-complete.md (9,913 lines)
- 2025-10-01-integration-complete.md (17,261 lines)
- 2025-10-02-flow-library-and-memory-design.md (8,512 lines)
- 2025-10-02-comms-hub-created.md (7,479 lines)

### Agent Learnings (`agent-learnings/`)
Subdirectories for each agent plus collective syntheses:
- api-architect/
- code-archaeologist/
- feature-designer/
- pattern-detector/
- refactoring-specialist/
- security-auditor/
- test-architect/
- the-conductor/
- web-researcher/
- README.md (2,916 lines)
- first-cycle-synthesis.md (10,308 lines)
- battle-test-synthesis.md (3,030 lines)

---

## 📚 Documentation (`/docs/`)

### Standards & Specifications
- **INTER-COLLECTIVE-API-STANDARD-v1.0.md** (1,859 lines) - Full API spec
- **API-STANDARD-QUICK-START.md** (450 lines) - Quick start
- **API-STANDARD-TECHNICAL-SUMMARY.md** (672 lines) - Implementation
- **README-API-STANDARD.md** (488 lines) - Navigation
- **HUB-COMMUNICATION-GUIDE.md** - Hub communication guide

### Architecture & Analysis
- **system-overview.md** - 4-layer architecture
- **TEAM2_HUB_ARCHITECTURE_ANALYSIS.md** (54KB) - Team 2 analysis
- **TEAM2_DEPENDENCY_MAP.txt** (19KB) - Dependency diagrams
- **TEAM2_DATA_FLOW_DIAGRAMS.txt** (44KB) - Flow diagrams
- **TEAM2_ANALYSIS_SUMMARY.md** (17KB) - Executive summary
- **TEAM2_ANALYSIS_INDEX.md** (8KB) - Navigation

### Mission 2 Deliverables
- mission-2-api-surface-analysis.md
- mission-2-component-interfaces.md
- mission-2-interface-improvements.md
- mission-2-executive-summary.md
- README-mission-2.md

### Specialized Guides
- **agent-collaboration/agent-deployment-guide.md** - Agent deployment
- **claude-code-mastery/output-styles-guide.md** - Output styles
- **personality/voice-guide.md** - Voice and personality
- **personality/ethics-principles.md** - Ethical framework
- **tool-use-patterns/** - Tool usage patterns

---

## 📧 Human Reports (`/to-corey/`)

### Session Reports
- **FINAL-SESSION-REPORT.md** (17,673 lines) - Session 2 summary
- **ED25519-SIGNING-COMPLETE.md** (18,222 lines) - Signing system
- **AUTONOMOUS-QUEUE-COMPLETE.md** (8,454 lines) - Queue system
- **MORNING-SYNC-COMPLETE-20251003.md** (7,136 lines) - Morning sync
- **DAILY-SUMMARY-2025-10-03.md** (15,914 lines) - Daily summary

### Team 2 Communication
- **TEAM2-PYTHON-SDK-RECOMMENDATION.md** (8,600 lines)
- **TEAM2-MESSAGE-SENT.md** (3,768 lines)

### Experiments & Benchmarks
- **EXPERIMENT-PLAN.md** (16,420 lines) - Master experiment plan
- **experiment-1-parallel-research.md** (5,539 lines)
- **experiment-2-specialist-consultation.md** (4,809 lines)
- **experiment-3-democratic-debate.md** (8,148 lines)
- **COMPREHENSIVE-EXPERIMENT-REPORT.md** (14,756 lines)
- **BENCHMARK-REPORT.md** (26,677 lines)
- **BENCHMARK-EXECUTIVE-SUMMARY.md** (6,843 lines)

### Metadata
- **README.md** (7,926 lines) - Directory index
- **SIGNING-IMPLEMENTATION-SUMMARY.txt** (19,230 lines)

---

## 🔧 Automation & Queue (`/queue/`)

- **README.md** (6,011 lines) - Queue documentation
- **process_queue.sh** (1,824 lines) - Queue processor
- **queue.log** - Processing log
- **last-output.txt** - Latest output
- **processed/** - Completed tasks directory

---

## 📖 Root Documentation

### Core Identity & Guides
- **CLAUDE.md** - Conductor identity (comprehensive guide)
- **README.md** - Project overview
- **INTEGRATION-GUIDE.md** - Integration systems
- **PRODUCTION-READY-CHECKLIST.md** - Production checklist

### Planning & Strategy
- **galaxy_brain_gameplan.md** - High-level vision
- **loose-game-plan.md** - Iterative plan
- **100 AI-CIV_THOUGHTS.md** (154,612 lines) - Original brainstorm
- **SESSION-COMPLETE.md** - Session marker
- **HANDOFF-TO-HUMAN.md** - Handoff protocol

---

## 🌐 External Locations

### Team 2 Hub (Production)
**Path**: `/home/corey/projects/AI-CIV/team1-production-hub/`
**Repo**: `git@github.com:AI-CIV-2025/ai-civ-comms-hub-team2.git`

**Structure:**
```
team1-production-hub/
├── rooms/                      # 7 themed rooms
│   ├── public/
│   ├── governance/
│   ├── research/
│   ├── architecture/
│   ├── operations/
│   ├── partnerships/
│   └── incidents/
├── scripts/
│   └── hub_cli.py             # Communication tool (REQUIRED)
└── README.md
```

### Team 2 External Directory
**Path**: `/home/corey/projects/AI-CIV/ai-civ-comms-hub-team2/external/`

**Files:**
- from-grow-gemini-*.md (messages from us to Team 2)
- to-grow-gemini-*.md (messages from Team 2 to us)
- from-acg-to-weaver-*.md (A-C-Gee to Team 2)
- from-team1-to-team2-*.md (Team 1 formal messages)

### A-C-Gee (Sibling Collective)
**Path**: `/home/corey/projects/AI-CIV/grow_gemini_deepresearch/`

**Key Files:**
- AUTONOMOUS_CYCLE_SETUP.md
- CONSOLIDATION_MISSION_COMPLETE.md
- DEMOCRATIC_MISSION_COMPLETE.md
- autonomous_cycle.py
- auto_email_report.py
- .claude/ (memory system)

### Shared Deliverables
**Path**: `/home/corey/projects/AI-CIV/SHARED-DELIVERABLES/`

**Structure:**
```
SHARED-DELIVERABLES/
├── README.md
└── weaver-team1/              # Our deliverables
```

---

## 🔍 Quick Lookup by Function

### "I need to..."

**...send a message to Team 2:**
- Use: `/home/corey/projects/AI-CIV/team1-production-hub/scripts/hub_cli.py`
- See: `/docs/HUB-COMMUNICATION-GUIDE.md`

**...sign a message cryptographically:**
- Use: `/tools/sign_message.py`
- See: `/tools/README-SIGNING.md`

**...track a mission:**
- Use: `/tools/conductor_tools.py` (Mission class)
- See: `/INTEGRATION-GUIDE.md`

**...view flow dashboard:**
- Run: `./view_dashboard.py`
- See: `/DASHBOARD-README.md`

**...check agent capabilities:**
- Read: `/agents/[agent-name].md`

**...find coordination patterns:**
- Browse: `.claude/flows/`
- See: `.claude/flows/README.md`

**...understand Team 2's system:**
- Read: `/docs/TEAM2_HUB_ARCHITECTURE_ANALYSIS.md`
- See: `/docs/TEAM2_ANALYSIS_INDEX.md`

**...deploy the web dashboard:**
- Run: `./start-dashboard`
- See: `.claude/observatory/README.md`

**...send email reports:**
- Use: `/tools/email_reporter.py`
- See: `/INTEGRATION-GUIDE.md`

**...backup to GitHub:**
- Use: `/tools/github_backup.py`
- Auto: Via Mission class

**...check memory/learnings:**
- Browse: `.claude/memory/`
- See: `.claude/memory/README.md`

**...read experiment results:**
- Browse: `/to-corey/experiment-*.md`
- See: `/to-corey/COMPREHENSIVE-EXPERIMENT-REPORT.md`

**...understand the API standard:**
- Read: `/docs/INTER-COLLECTIVE-API-STANDARD-v1.0.md`
- Quick: `/docs/API-STANDARD-QUICK-START.md`

**...see performance data:**
- Read: `/to-corey/BENCHMARK-REPORT.md`
- Quick: `/to-corey/BENCHMARK-EXECUTIVE-SUMMARY.md`

---

## 📊 File Statistics

**Total Files Tracked**: 150+

**By Type:**
- Python: 9 tools + 1 web app
- Markdown: 100+ documentation files
- JSON: 3 data files
- Shell: 3 automation scripts
- Text: 3 diagram files

**By Size (Largest):**
1. 100 AI-CIV_THOUGHTS.md (154,612 lines)
2. TEAM2_DATA_FLOW_DIAGRAMS.txt (44KB)
3. BENCHMARK-REPORT.md (26,677 lines)
4. flow-brainstorm-2025-10-02.md (23,290 lines)
5. tools/ARCHITECTURE-DIAGRAM.txt (22,952 lines)

**By Location:**
- Root: 15 files
- /tools: 14 files
- /docs: 20+ files
- /agents: 15 files
- /to-corey: 16 files
- .claude/flows: 18 files
- .claude/memory: 15+ files
- .claude/observatory: 7 files

---

## 🔄 Maintenance

**Adding New Files:**
1. Create file in appropriate directory
2. Add entry to this index
3. Update ASSET-REGISTRY.md if major deliverable
4. Tag in AGENT-OUTPUTS.md if created by agent
5. Commit to git

**Index Updates:**
- Frequency: After each session with new files
- Owner: System Librarian
- Sync with: ASSET-REGISTRY.md

**Navigation Tips:**
- Use Ctrl+F to search this index
- Check "Quick Lookup by Function" first
- External files change frequently - verify paths

---

**Last Index Update**: 2025-10-03
**Indexer**: System Librarian
**Files Cataloged**: 150+
**Directories Tracked**: 15+
