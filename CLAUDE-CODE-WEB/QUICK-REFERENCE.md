# CLAUDE-CODE-WEB Quick Reference Guide

**Last Updated**: 2025-11-07
**Total Files**: 408 (34 root + 374 in to-corey/)
**Purpose**: Consolidated work product archive from WEAVER collective

---

## 🎯 What Is CLAUDE-CODE-WEB?

**CLAUDE-CODE-WEB** is the organized archive of all WEAVER work product, consolidating scattered documentation from the project root into a single discoverable location.

**What's Here**:
- Session summaries and daily reports
- Agent design specifications
- Infrastructure audits and health checks
- Skills ecosystem reports
- Telegram/communication system documentation
- Strategic roadmaps and manifestos
- Handoffs between sessions
- Experimental workflows and validations

**What's NOT Here**:
- Core constitutional documents (stay in `.claude/`)
- Active codebase (stays in project structure)
- Operational infrastructure (tools, agents, flows)

**Think of it as**: The collective's "published papers" - completed work, findings, reports, and analyses.

---

## 📁 Structure Overview

```
CLAUDE-CODE-WEB/
├── [34 root files]          # High-level strategic documents
└── to-corey/                # Detailed session reports & analyses
    └── [374 files]          # Chronological work product
```

**Root Level** = Strategic/High-Importance
- Roadmaps, manifestos, major checklists
- Documents Corey needs quick access to
- Synthesis documents spanning multiple sessions

**to-corey/** = Detailed Session Work
- Daily session summaries
- Agent design specs
- Specific audits and analyses
- Handoff documents
- Experiment reports

---

## 🔍 How to Find What You Need

### By Document Type

**Strategic Planning**:
- `/home/user/weaver/CLAUDE-CODE-WEB/INTEGRATION-ROADMAP.md` - Current plan & priorities
- `/home/user/weaver/CLAUDE-CODE-WEB/PRODUCTION-READY-CHECKLIST.md` - Production readiness
- `/home/user/weaver/CLAUDE-CODE-WEB/LINEAGE-WISDOM-PACKAGE-SPEC.md` - Knowledge transfer plan

**Identity & Philosophy**:
- `/home/user/weaver/CLAUDE-CODE-WEB/WEAVER-MANIFESTO.md` - Who we are
- `/home/user/weaver/CLAUDE-CODE-WEB/WEAVER-MANIFESTO-SUMMARY.md` - Quick version
- `/home/user/weaver/CLAUDE-CODE-WEB/HUMAN-WISDOM-SYNTHESIS.md` - Teacher learnings

**Infrastructure Guides**:
- `/home/user/weaver/CLAUDE-CODE-WEB/MEMORY-SYSTEM-README.md` - Memory system usage
- `/home/user/weaver/CLAUDE-CODE-WEB/INTEGRATION-GUIDE.md` - Integration patterns
- `/home/user/weaver/CLAUDE-CODE-WEB/DASHBOARD-README.md` - Dashboard overview

**Session Summaries**:
```bash
# Find by date
ls /home/user/weaver/CLAUDE-CODE-WEB/to-corey/ | grep "DAILY-SUMMARY-2025-10"
ls /home/user/weaver/CLAUDE-CODE-WEB/to-corey/ | grep "SESSION-"

# Latest session
/home/user/weaver/CLAUDE-CODE-WEB/to-corey/session-summary-latest.md
```

**Agent Designs**:
```bash
# All agent design reports
ls /home/user/weaver/CLAUDE-CODE-WEB/to-corey/ | grep "AGENT-ARCHITECT-REPORT"
ls /home/user/weaver/CLAUDE-CODE-WEB/to-corey/ | grep "AGENT-.*-DESIGN"

# Cross-civ integrator (example)
/home/user/weaver/CLAUDE-CODE-WEB/to-corey/agent-design-cross-civ-integrator/
```

**Skills Infrastructure**:
```bash
# Skills ecosystem reports
ls /home/user/weaver/CLAUDE-CODE-WEB/to-corey/ | grep "SKILLS-"

# Key documents
/home/user/weaver/CLAUDE-CODE-WEB/to-corey/SKILLS-INFRASTRUCTURE-TRANSFORMATION-COMPLETE.md
/home/user/weaver/CLAUDE-CODE-WEB/to-corey/SKILLS-PHASE1-ACTIVATION-REPORT.md
```

**Telegram/Communications**:
```bash
# Telegram debugging & fixes
ls /home/user/weaver/CLAUDE-CODE-WEB/to-corey/ | grep "TG-"
ls /home/user/weaver/CLAUDE-CODE-WEB/to-corey/ | grep "TELEGRAM-"

# Quick start
/home/user/weaver/CLAUDE-CODE-WEB/to-corey/TELEGRAM-QUICKSTART.md
```

**Audits & Health Checks**:
```bash
# All audits
ls /home/user/weaver/CLAUDE-CODE-WEB/to-corey/ | grep "AUDIT"
ls /home/user/weaver/CLAUDE-CODE-WEB/to-corey/ | grep "HEALTH"

# Examples
/home/user/weaver/CLAUDE-CODE-WEB/to-corey/CONSTITUTIONAL-COMPLIANCE-AUDIT-OCT-9.md
/home/user/weaver/CLAUDE-CODE-WEB/to-corey/COGNITIVE-HEALTH-AUDIT-OCT-9.md
```

---

## 📋 Key Documents by Use Case

### "I'm waking up cold - what happened recently?"

1. **Latest session summary**:
   `/home/user/weaver/CLAUDE-CODE-WEB/to-corey/session-summary-latest.md`

2. **Recent daily summaries**:
   ```bash
   ls -lt /home/user/weaver/CLAUDE-CODE-WEB/to-corey/DAILY-SUMMARY-* | head -5
   ```

3. **Current plan**:
   `/home/user/weaver/CLAUDE-CODE-WEB/INTEGRATION-ROADMAP.md`

### "What is WEAVER's identity/purpose?"

1. **Manifesto** (full):
   `/home/user/weaver/CLAUDE-CODE-WEB/WEAVER-MANIFESTO.md`

2. **Manifesto** (summary):
   `/home/user/weaver/CLAUDE-CODE-WEB/WEAVER-MANIFESTO-SUMMARY.md`

3. **Self-portrait** (collective perspective):
   `/home/user/weaver/CLAUDE-CODE-WEB/to-corey/COLLECTIVE-SELF-PORTRAIT.md`

### "How do I use [specific infrastructure]?"

**Memory System**:
- `/home/user/weaver/CLAUDE-CODE-WEB/MEMORY-SYSTEM-README.md`
- `/home/user/weaver/CLAUDE-CODE-WEB/MEMORY-SYSTEM-IMPLEMENTATION-REPORT.md`

**Dashboard**:
- `/home/user/weaver/CLAUDE-CODE-WEB/DASHBOARD-README.md`
- `/home/user/weaver/CLAUDE-CODE-WEB/DASHBOARD-SUMMARY.md`

**Telegram Bridge**:
- `/home/user/weaver/CLAUDE-CODE-WEB/to-corey/TELEGRAM-QUICKSTART.md`
- `/home/user/weaver/CLAUDE-CODE-WEB/to-corey/TELEGRAM-QUICK-REFERENCE.md`

**Skills System**:
- `/home/user/weaver/CLAUDE-CODE-WEB/to-corey/SKILLS-TRANSFORMATION-QUICK-REFERENCE.md`
- `/home/user/weaver/CLAUDE-CODE-WEB/to-corey/SKILLS-INFRASTRUCTURE-TRANSFORMATION-COMPLETE.md`

### "What experiments have we run?"

```bash
# Experiment reports
ls /home/user/weaver/CLAUDE-CODE-WEB/to-corey/ | grep "experiment-"

# Examples:
/home/user/weaver/CLAUDE-CODE-WEB/to-corey/experiment-1-parallel-research.md
/home/user/weaver/CLAUDE-CODE-WEB/to-corey/experiment-2-specialist-consultation.md
/home/user/weaver/CLAUDE-CODE-WEB/to-corey/experiment-3-democratic-debate.md
```

### "What's the status of [agent design]?"

```bash
# All agent architect reports
ls /home/user/weaver/CLAUDE-CODE-WEB/to-corey/ | grep "AGENT-ARCHITECT-REPORT"

# Specific examples:
# - health-auditor
# - cross-civ-integrator
# - tg-bridge
```

### "What consolidation/cleanup work was done?"

```bash
# Consolidation reports
ls /home/user/weaver/CLAUDE-CODE-WEB/to-corey/ | grep "CONSOLIDATION"

# Key documents:
/home/user/weaver/CLAUDE-CODE-WEB/to-corey/CONSOLIDATION-MISSION-COMPLETE.md
/home/user/weaver/CLAUDE-CODE-WEB/to-corey/CONSOLIDATION-QUICK-REFERENCE.md
```

### "How do I communicate with Team 2 (A-C-Gee)?"

```bash
# Team 2 communications
ls /home/user/weaver/CLAUDE-CODE-WEB/to-corey/ | grep "TEAM2"
ls /home/user/weaver/CLAUDE-CODE-WEB/to-corey/ | grep "ACG"

# Examples:
/home/user/weaver/CLAUDE-CODE-WEB/to-corey/ACG-MESSAGE-PARTNERSHIP-CHECKIN-DRAFT.md
/home/user/weaver/CLAUDE-CODE-WEB/to-corey/TEAM2-MESSAGE-SENT.md
```

---

## 🔎 Search Patterns

### By Date

**Find October 2025 work**:
```bash
ls /home/user/weaver/CLAUDE-CODE-WEB/to-corey/ | grep "2025-10"
```

**Find November 2025 work**:
```bash
ls /home/user/weaver/CLAUDE-CODE-WEB/to-corey/ | grep "2025-11"
```

**Find specific date** (e.g., Oct 9):
```bash
ls /home/user/weaver/CLAUDE-CODE-WEB/to-corey/ | grep "OCT-9"
ls /home/user/weaver/CLAUDE-CODE-WEB/to-corey/ | grep "2025-10-09"
```

### By Topic

**Skills**:
```bash
find /home/user/weaver/CLAUDE-CODE-WEB -name "*SKILLS*" -o -name "*skills*"
```

**Telegram**:
```bash
find /home/user/weaver/CLAUDE-CODE-WEB -name "*TG-*" -o -name "*TELEGRAM*"
```

**Audits**:
```bash
find /home/user/weaver/CLAUDE-CODE-WEB -name "*AUDIT*"
```

**Agent designs**:
```bash
find /home/user/weaver/CLAUDE-CODE-WEB -name "*AGENT-ARCHITECT*"
```

**Handoffs**:
```bash
find /home/user/weaver/CLAUDE-CODE-WEB -name "*HANDOFF*"
```

### By Agent/Role

**Conductor/Primary work**:
```bash
ls /home/user/weaver/CLAUDE-CODE-WEB/to-corey/ | grep "CONDUCTOR"
```

**AI Psychologist work**:
```bash
ls /home/user/weaver/CLAUDE-CODE-WEB/to-corey/ | grep "AI-PSYCHOLOGIST"
```

**Integration auditor work**:
```bash
ls /home/user/weaver/CLAUDE-CODE-WEB/to-corey/ | grep "INTEGRATION"
```

---

## 📊 Most Important Documents (Top 20)

### Strategic (Must Read for Context)

1. **INTEGRATION-ROADMAP.md** - Current plan & priorities
2. **WEAVER-MANIFESTO.md** - Identity & purpose
3. **PRODUCTION-READY-CHECKLIST.md** - Deployment readiness
4. **HUMAN-WISDOM-SYNTHESIS.md** - Teacher insights

### Infrastructure Guides

5. **MEMORY-SYSTEM-README.md** - How to use memory system
6. **DASHBOARD-README.md** - Dashboard overview
7. **INTEGRATION-GUIDE.md** - Integration patterns

### Recent Major Work

8. **to-corey/WEAVER-CAPABILITIES-ASSESSMENT-2025-11-07.md** - Latest capability scan
9. **to-corey/WEAVER-MEMORY-INVENTORY-2025-11-07.md** - Memory system state
10. **to-corey/WEAVER-TRANSFORMATION-COMPLETE-2025-11-02.md** - Transformation milestone

### Skills Infrastructure

11. **to-corey/SKILLS-INFRASTRUCTURE-TRANSFORMATION-COMPLETE.md** - Skills system complete
12. **to-corey/SKILLS-PHASE1-ACTIVATION-REPORT.md** - Phase 1 results
13. **to-corey/SKILLS-TRANSFORMATION-QUICK-REFERENCE.md** - Skills quick guide

### Communication Systems

14. **to-corey/TELEGRAM-QUICKSTART.md** - Telegram setup
15. **to-corey/COMMS-HUB-BOOTSTRAP-COMPLETE-2025-11-04.md** - Hub status

### Agent Designs

16. **to-corey/AGENT-ARCHITECT-REPORT-HEALTH-AUDITOR.md** - Health auditor design
17. **to-corey/AGENT-ARCHITECT-REPORT-cross-civ-integrator-2025-11-02.md** - Cross-civ design

### Health & Audits

18. **to-corey/CONSTITUTIONAL-COMPLIANCE-AUDIT-OCT-9.md** - Constitutional check
19. **to-corey/COGNITIVE-HEALTH-AUDIT-OCT-9.md** - Cognitive health assessment

### Session Tracking

20. **to-corey/session-summary-latest.md** - Most recent session

---

## 🗂️ Content Categories (Detailed)

### 1. Session Management (50+ files)

**Daily summaries**: DAILY-SUMMARY-2025-[DATE].md
**Session handoffs**: SESSION-HANDOFF-*, SESSION-COMPLETE-*
**Session summaries**: SESSION-SUMMARY-*

**Common patterns**:
- End-of-session reports
- Cold start handoffs (session → session)
- Completion reports with achievements

### 2. Agent Designs (15+ files)

**AGENT-ARCHITECT-REPORT-[name].md** - Detailed design specs
**agent-design-[name]/** - Multi-file designs (design-brief, quality-score, etc.)

**Agents documented**:
- health-auditor
- cross-civ-integrator
- tg-bridge
- claude-code-expert

### 3. Skills Infrastructure (25+ files)

**SKILLS-*** - Skills ecosystem work
**SKILL-CREATED-*** - Custom skill reports

**Key categories**:
- Ecosystem scans
- Grant reports
- Phase activation reports
- Transformation documentation

### 4. Telegram/Communications (30+ files)

**TG-*** - Telegram bridge debugging
**TELEGRAM-*** - Telegram system documentation
**COMMS-HUB-*** - Communication hub work

**Covers**:
- Bridge fixes & debugging
- Duplicate message diagnosis
- Monitoring setup
- Quick references

### 5. Audits & Health (40+ files)

**[TOPIC]-AUDIT-*** - Formal audits
**[TOPIC]-HEALTH-*** - Health checks

**Audit types**:
- Constitutional compliance
- Cognitive health
- Integration readiness
- Test coverage
- UX health
- Workflow health

### 6. Consolidation Work (20+ files)

**CONSOLIDATION-*** - Documentation organization
**CONTRADICTION-*** - Conflict resolution

**Topics**:
- Interface audits
- Quick wins
- Synthesis methodologies
- Validation frameworks

### 7. Experiments (3 files)

**experiment-[N]-[name].md** - Validated workflows

**Experiments**:
1. Parallel research
2. Specialist consultation
3. Democratic debate

### 8. Team 2 Communications (10+ files)

**ACG-*** - A-C-Gee related
**TEAM2-*** - Sister collective coordination

**Content**:
- Partnership check-ins
- Capability scans
- Message drafts
- Python SDK recommendations

### 9. Strategic Documents (10+ files)

**High-level roadmaps, checklists, manifestos**

**Examples**:
- INTEGRATION-ROADMAP.md
- PRODUCTION-READY-CHECKLIST.md
- LINEAGE-WISDOM-PACKAGE-SPEC.md

### 10. Handoffs & Transitions (15+ files)

**HANDOFF-*** - Session transitions
**COLD-START-*** - Cold boot procedures

**Covers**:
- Human handoffs
- Session-to-session handoffs
- Deterministic check procedures

---

## 🚀 Quick Start Scenarios

### Scenario 1: New Session, Cold Boot

```bash
# 1. Check latest session
cat /home/user/weaver/CLAUDE-CODE-WEB/to-corey/session-summary-latest.md

# 2. Check current plan
cat /home/user/weaver/CLAUDE-CODE-WEB/INTEGRATION-ROADMAP.md

# 3. Check recent work (last 5 days)
ls -lt /home/user/weaver/CLAUDE-CODE-WEB/to-corey/DAILY-SUMMARY-* | head -5
```

### Scenario 2: Understanding a Specific System

**Example: Memory System**
```bash
# Read main guide
cat /home/user/weaver/CLAUDE-CODE-WEB/MEMORY-SYSTEM-README.md

# Check implementation report
cat /home/user/weaver/CLAUDE-CODE-WEB/MEMORY-SYSTEM-IMPLEMENTATION-REPORT.md

# Check latest inventory
cat /home/user/weaver/CLAUDE-CODE-WEB/to-corey/WEAVER-MEMORY-INVENTORY-2025-11-07.md
```

### Scenario 3: Researching Past Work

**Example: Find all October 9 work**
```bash
# List all Oct 9 documents
ls /home/user/weaver/CLAUDE-CODE-WEB/to-corey/ | grep "OCT-9"

# Or by full date
ls /home/user/weaver/CLAUDE-CODE-WEB/to-corey/ | grep "2025-10-09"
```

### Scenario 4: Agent Design Research

**Example: Check health-auditor design**
```bash
# Find the report
ls /home/user/weaver/CLAUDE-CODE-WEB/to-corey/ | grep "HEALTH-AUDITOR"

# Read it
cat /home/user/weaver/CLAUDE-CODE-WEB/to-corey/AGENT-ARCHITECT-REPORT-HEALTH-AUDITOR.md
```

---

## 📝 Naming Conventions

### File Naming Patterns

**ALL-CAPS-WITH-DASHES.md** = Formal reports, summaries, guides
**lowercase-with-dashes.md** = Informal notes, drafts, brainstorms
**TOPIC-SUBTOPIC-DATE.md** = Time-stamped reports

### Date Formats

**YYYY-MM-DD** = ISO format (2025-10-19)
**MMM-D** = Abbreviated (OCT-9)
**YYYYMMDD** = Compressed (20251019)

### Common Prefixes

**AGENT-*** = Agent-related work
**SKILLS-*** = Skills infrastructure
**TG-*** or **TELEGRAM-*** = Telegram system
**SESSION-*** = Session management
**DAILY-*** = Daily summaries
**AUDIT-*** = Formal audits
**CONSOLIDATION-*** = Organization work
**HANDOFF-*** = Transition documents

---

## 🎯 Tips for Effective Navigation

### 1. Use Tab Completion

Most shell environments support tab completion:
```bash
cat /home/user/weaver/CLAUDE-CODE-WEB/to-corey/SKI<TAB>
# Expands to show all SKILLS-* files
```

### 2. Grep for Content

If you know a phrase but not the file:
```bash
grep -r "parallel research" /home/user/weaver/CLAUDE-CODE-WEB/
```

### 3. Sort by Modification Time

Find most recently updated files:
```bash
ls -lt /home/user/weaver/CLAUDE-CODE-WEB/to-corey/ | head -20
```

### 4. Count Files by Pattern

See how many of each type:
```bash
ls /home/user/weaver/CLAUDE-CODE-WEB/to-corey/ | grep "SKILLS" | wc -l
ls /home/user/weaver/CLAUDE-CODE-WEB/to-corey/ | grep "AGENT" | wc -l
```

### 5. Create Custom Searches

Save common searches:
```bash
# Add to your shell profile
alias weaver-skills="ls /home/user/weaver/CLAUDE-CODE-WEB/to-corey/ | grep SKILLS"
alias weaver-recent="ls -lt /home/user/weaver/CLAUDE-CODE-WEB/to-corey/ | head -10"
```

---

## 🔗 Related Documentation

**Core Constitutional Documents** (NOT in CLAUDE-CODE-WEB):
- `/home/corey/projects/AI-CIV/WEAVER/CLAUDE.md` - Entry point
- `/home/corey/projects/AI-CIV/WEAVER/.claude/CLAUDE-CORE.md` - Constitutional foundation
- `/home/corey/projects/AI-CIV/WEAVER/.claude/CLAUDE-OPS.md` - Operational playbook

**Active Infrastructure** (NOT in CLAUDE-CODE-WEB):
- `/home/corey/projects/AI-CIV/WEAVER/.claude/agents/` - Agent manifests
- `/home/corey/projects/AI-CIV/WEAVER/.claude/flows/` - Workflow definitions
- `/home/corey/projects/AI-CIV/WEAVER/.claude/templates/` - Templates
- `/home/corey/projects/AI-CIV/WEAVER/.claude/skills-registry.md` - Skills catalog

**Live Tools** (NOT in CLAUDE-CODE-WEB):
- `tools/` - Python utilities (Mission, Memory, Progress)
- `team1-production-hub/` - Hub coordination

---

## 📊 Quick Stats

**Total Files**: 408
- Root level: 34
- to-corey/: 374

**Estimated Coverage**:
- Session summaries: 50+
- Agent designs: 15+
- Skills reports: 25+
- Telegram/comms: 30+
- Audits: 40+
- Consolidation: 20+
- Experiments: 3
- Team 2 comms: 10+
- Strategic docs: 10+
- Handoffs: 15+

**Date Range**: Primarily October 2025 - November 2025

**Size**: ~2-3 MB of documentation (estimated)

---

## 🛠️ Maintenance Notes

**This folder is append-only** - old documents remain for historical record.

**Not for active editing** - work products are snapshots at completion time.

**For current work**, reference:
- `.claude/` infrastructure
- Active project files
- Real-time tools

**For historical research**, reference:
- CLAUDE-CODE-WEB/ (this folder)

---

**END OF QUICK REFERENCE**

*This guide will grow as CLAUDE-CODE-WEB accumulates more work product. Update periodically as new categories emerge.*
