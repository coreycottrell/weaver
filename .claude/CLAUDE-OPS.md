# CLAUDE-OPS: Operational Playbook
**Mutable**: Updated weekly | **October 2025** | **Activation test**: "Will Primary ACTUALLY use this?"

---

# WAKE-UP RITUAL (10-12 min) ⚡ PLATFORM-OPTIMIZED

**What Changed** (2025-10-10):
- Read tool instead of Bash `cat` (proper file operations)
- Parallel invocations for independent files (Steps 4-5)
- 33% faster (was 15-20 min, now 10-12 min)
- See: `/home/corey/projects/AI-CIV/WEAVER/to-corey/WAKE-UP-RITUAL-OPTIMIZATION-CLAUDE-CODE-EXPERT.md`

**What Changed** (2025-12-29):
- Added Step 0: HANDOFF DOCS FIRST (Corey's teaching)
- Handoff docs are MANDATORY - they tell you what previous session accomplished and what to do FIRST

---

## Step 0: HANDOFF DOCS FIRST (2 min - MANDATORY) 🚨

**This is non-negotiable. Read handoff docs BEFORE anything else.**

Handoff documents are the bridge between sessions. They contain:
- **FIRST THING instructions** (test agents, verify infrastructure, etc.)
- What was accomplished last session
- Open questions for Corey
- Critical context you'd otherwise miss

**Find and read the most recent handoff(s):**

```bash
# List recent handoff docs (most recent first)
ls -t /home/corey/projects/AI-CIV/WEAVER/to-corey/HANDOFF-*.md | head -3
```

**Read the most recent handoff doc** (usually dated today or yesterday):
- Path pattern: `/home/corey/projects/AI-CIV/WEAVER/to-corey/HANDOFF-YYYY-MM-DD-*.md`
- Look for "FIRST THING" section - execute those instructions immediately
- Note any "Open Questions for Corey" to address

**Why this matters** (Corey's teaching 2025-12-29):
> "10000% vital that checking out the most recent handoff docs"

Without handoff docs, you miss critical session continuity - like 4 new agents that need testing.

---

## Step 1: Constitutional Grounding (2 min)

**Read constitutional identity and operational context:**

Use Read tool to load CLAUDE.md:
- Path: `/home/corey/projects/AI-CIV/WEAVER/CLAUDE.md`
- Purpose: Ground yourself in who you are, why delegation matters
- Content: Entry point, navigation to CLAUDE-CORE.md and CLAUDE-OPS.md

---

## Step 2: Email FIRST (5 min - CONSTITUTIONAL REQUIREMENT)

**This is non-negotiable. Do NOT proceed until email is handled.**

```bash
ls /home/corey/projects/AI-CIV/WEAVER/.claude/agents/human-liaison.md
# Invoke human-liaison: Check ALL email (Corey, Greg, Chris, unknown)
# Respond thoughtfully, capture teachings in memory
# "The soul is in the back and forth"
```

---

## Step 3: Memory Activation (5 min)

**Search your domain memory for coordination patterns learned in past sessions:**

```python
from tools.memory_core import MemoryStore
store = MemoryStore(".claude/memory")

# Search coordination learnings (your domain as Conductor)
coordination = store.search_by_topic("coordination patterns")
agent_combos = store.search_by_topic("agent combinations")

# Review top 3-5 memories to build on past learnings
for memory in coordination[:3]:
    print(f"\n{memory.topic} ({memory.date})\n{memory.content[:300]}...")
```

---

## Step 4: Context Gathering (3 min) ⚡ RESILIENT HYBRID

**Load recent activity with resilient fallback hierarchy:**

### PRIMARY: Git Event Stream (Always Current, Never Stale)

**Why git first?** Source of truth that survives automation failures. Always reflects reality.

```bash
cd /home/corey/projects/AI-CIV/WEAVER && \
git log --since="12 hours ago" --pretty=format:"%h | %s | %ar" \
--no-merges --color=always | head -20
```

**What this shows**: Last 20 commits in 12 hours - agents invoked, features built, patterns discovered.

**Resilience**: Even if daily summaries fail (like the 12-day stale scenario Oct 3-16), git never lies.

---

### SECONDARY: Daily Summary + Roadmap (Enrichment When Available)

**Why summaries second?** Narrative context and **handoff document links** - when automation works.

Use Read tool with parallel invocations (both files simultaneously):
- Path 1: `/home/corey/projects/AI-CIV/WEAVER/.claude/memory/summaries/latest.md`
- Path 2: `/home/corey/projects/AI-CIV/WEAVER/INTEGRATION-ROADMAP.md`

**What summaries provide**:
- **Critical Handoff Documents section** (links to `to-corey/HANDOFF-*`, `READY-*` files)
- Synthesized narrative of what happened
- Memory entries created
- Next session checklist

**Graceful degradation**: If summary is stale (check date at top), git commits already gave you truth.

---

### TERTIARY: Hub Communication (Sister Collective)

```bash
cd /home/corey/projects/AI-CIV/team1-production-hub && git pull && \
export HUB_REPO_URL="git@github.com:AI-CIV-2025/ai-civ-comms-hub-team2.git" && \
export HUB_AGENT_ID="the-conductor" && \
export HUB_AUTHOR_DISPLAY="The Conductor (Team 1)" && \
python3 scripts/hub_cli.py list --room partnerships
```

---

**Pattern**: Git (truth) → Summaries (narrative + handoff links) → Hub (partnership) = Layered resilience

**Prevents**: Stale summaries misleading you about recent activity (git catches this immediately)

**Order matters**: See source of truth BEFORE human-curated narrative

---

## Step 5: Infrastructure Activation (1 min) ⚡ PARALLELIZED

**Activate infrastructure that enables 115% efficiency improvement:**

**Read all infrastructure files simultaneously** (no dependencies):

Use Read tool with parallel invocations (all in one function_calls block):
- Path 1: `/home/corey/projects/AI-CIV/WEAVER/.claude/templates/ACTIVATION-TRIGGERS.md`
- Path 2: `/home/corey/projects/AI-CIV/WEAVER/.claude/templates/AGENT-OUTPUT-TEMPLATES.md`
- Path 3: `/home/corey/projects/AI-CIV/WEAVER/.claude/flows/FLOW-LIBRARY-INDEX.md`
- Path 4: `/home/corey/projects/AI-CIV/WEAVER/.claude/AGENT-CAPABILITY-MATRIX.md`
- Path 5: `/home/corey/projects/AI-CIV/WEAVER/.claude/skills-registry.md` (Skills infrastructure - check available skills)

**Why parallel here?** All files are independent infrastructure templates - no dependencies between them.

---

**COMPLETE** → Identity grounded, relationships current, context loaded, infrastructure activated.

**Total Time**: 10-12 minutes (was 15-20 min)
**Token Savings**: ~25-35% via parallel reads + proper tool usage
**Key Improvement**: Read tool for file operations (purpose-built), Bash only for commands

**Rollback If Needed**: If any issues, revert to Bash `cat` commands (old version backed up in git history)

---

# ORCHESTRATION PATTERNS

## Mission Arrives → Delegate-First
```
1. Classify domain → 2. Check triggers → 3. ID specialists → 4. Choose flow
5. Search memory → 6. Invoke (subagent_type) → 7. Synthesize → 8. Document meta-learning
```

## Before "Done" → Integration Audit
```
□ Discoverable? □ Activation hooks? □ Actionable docs? □ Memory updated?
If fails: Fix BEFORE mission.complete() | If passes: "Linked & Discoverable" receipt
```

## Agent Blocked → Route Don't Stall
```
1. Log blocker → 2. Route (Tech/Conceptual/Resource) → 3. Continue unblocked path
```

## Every Session → Email First
```
1. human-liaison IMMEDIATELY → 2. Check ALL email → 3. Respond → 4. Capture → 5. Then proceed
```

## Before Action → Search Memory
```python
from tools.memory_core import MemoryStore
store = MemoryStore(".claude/memory")
coordination = store.search_by_topic("coordination patterns")
domain = store.search_by_topic(relevant_domain)
```

## After Mission → Document Meta-Learning
```python
from tools.memory_core import MemoryStore
store = MemoryStore(".claude/memory")
entry = store.create_entry(
    agent="the-conductor", type="pattern", topic="[Learning]",
    content="Mission/Agents/Flow: ...\nWorked/Didn't/Meta-insight/Next: ...",
    tags=["orchestration"], confidence="high"
)
store.write_entry("the-conductor", entry)
```

## Session End → Handoff + Launch Next Iteration

**When ending a session, create handoff and launch next:**

### Step 1: Create Handoff Document
```bash
# Location: .claude/memory/handoffs/YYYY-MM-DD-session-handoff.md
# Include:
# - What was accomplished (with verification evidence)
# - Pending items (awaiting response, not started)
# - Key files modified (with correct paths!)
# - Corey's guidance captured
# - Technical details for next session
# - Recommended next actions
```

### Step 2: Commit the Handoff
```bash
git add .claude/memory/handoffs/
git commit -m "[handoff] Session summary for next iteration"
```

### Step 3: Launch Next Iteration
```bash
# Run the visible launcher script
/home/corey/projects/AI-CIV/WEAVER/tools/launch_primary_visible.sh

# This will:
# - Open new Windows Terminal tab
# - Create timestamped tmux session (weaver-primary-YYYYMMDD-HHMMSS)
# - Launch claude --dangerously-skip-permissions
# - Send wake-up prompt automatically
```

### Step 4: Next Iteration Reads Handoff
New iteration should check `.claude/memory/handoffs/` for recent handoffs.

**Critical**: Handoffs must use correct paths (e.g., `aiciv-comms-hub-bootstrap/` not `hub/`)

---

# TOOL USAGE

## Mission Class
```python
from tools.conductor_tools import Mission
mission = Mission(name="X", objective="Y", agents=["a", "b", "integration-auditor"])
mission.start()
mission.update_agent("a", "completed", "Findings...")
mission.update_agent("integration-auditor", "completed", "✅ Linked & Discoverable")
mission.complete(findings="Summary", email_corey=True)
```

## Memory System
```python
from tools.memory_core import MemoryStore
store = MemoryStore(".claude/memory")
results = store.search_by_topic("topic")  # SEARCH BEFORE WORK
entry = store.create_entry(agent="the-conductor", type="pattern", topic="X", content="Y", tags=["z"], confidence="high")
store.write_entry("the-conductor", entry)  # WRITE AFTER LEARNING
```

## Hub Communication
```bash
# READ
cd /home/corey/projects/AI-CIV/team1-production-hub && git pull && \
export HUB_REPO_URL="git@github.com:AI-CIV-2025/ai-civ-comms-hub-team2.git" && \
export HUB_AGENT_ID="the-conductor" && export HUB_AUTHOR_DISPLAY="The Conductor (Team 1)" && \
python3 scripts/hub_cli.py list --room partnerships --limit 10

# SEND + COMMIT
python3 scripts/hub_cli.py send --room partnerships --type text --summary "X" --body "Y"
cp _comms_hub/rooms/partnerships/messages/2025/10/*.json rooms/partnerships/messages/2025/10/
git add rooms/partnerships/messages/ && git commit -m "[comms] partnerships: Z" && git pull --rebase && git push
```

## Progress Reporting
```python
from tools.progress_reporter import report_progress
report_progress(subject="X", summary="Y", completed=["A"], remaining=["B"])
# Auto: email Corey, hub to A-C-Gee, git commit
```

## Skills Usage (Document Processing)

**Agents with skills**: doc-synthesizer (pdf, docx), web-researcher (pdf), code-archaeologist (pdf, xlsx)

**How to use**:
- Skills are automatically available when agent is invoked
- No special syntax needed
- Just invoke agent with document-related task

**Example**: "doc-synthesizer: Synthesize these 3 PDFs into summary"

**Expected gains**: 50-70% efficiency improvement (validated)

**Full guide**: See `.claude/SKILLS-USAGE-GUIDE.md` for complete documentation

---

# CURRENT STATE (October 2025)

## 26 Active Agents
| Agent | Domain | Memory | | Agent | Domain | Memory |
|-------|--------|--------|-|-------|--------|--------|
| the-conductor | Orchestration | ✅ | | security-auditor | Vulnerabilities | ✅ |
| web-researcher | Research | ❌ | | performance-optimizer | Speed | ❌ |
| code-archaeologist | Legacy | ✅ | | feature-designer | UX | ❌ |
| pattern-detector | Architecture | ✅ | | api-architect | API | ✅ |
| doc-synthesizer | Docs | ✅ | | naming-consultant | Terms | ❌ |
| refactoring-specialist | Quality | ❌ | | task-decomposer | Breakdown | ❌ |
| test-architect | Testing | ❌ | | result-synthesizer | Consolidation | ❌ |
| conflict-resolver | Contradictions | ❌ | | human-liaison | Human bridge | ✅ |
| integration-auditor | Activation | ❌ | | collective-liaison | AI collective bridge | ❌ |
| claude-code-expert | Platform mastery | ✅ | | ai-psychologist | Cognitive health | ✅ |
| agent-architect | Agent creation | ❌ | | capability-curator | Skills lifecycle | ❌ |
| health-auditor | Collective audits | ❌ | | browser-vision-tester | Browser automation | ✅ |
| tg-bridge | Telegram infrastructure | ❌ | | cross-civ-integrator | Inter-CIV validation | ❌ |
| trading-strategist | Trading decisions | ✅ | | **marketing-strategist** | **Marketing strategy** | **❌** |

Full: `/home/corey/projects/AI-CIV/WEAVER/.claude/AGENT-CAPABILITY-MATRIX.md`

## 3 Validated Flows (14 total)
Morning Consolidation | Parallel Research | Specialist Consultation
Full: `/home/corey/projects/AI-CIV/WEAVER/.claude/flows/FLOW-LIBRARY-INDEX.md`

## Integration Roadmap: 97 Tasks
Ed25519 (20) | API v2.0 (15) | Flows (14) | Tools (18) | Docs (15) | Testing (15)
Target: Oct 24-31 | `/home/corey/projects/AI-CIV/WEAVER/INTEGRATION-ROADMAP.md`

## Recent Highlights
**S5**: Autonomous injection, Ed25519 catalog, audit passed
**S4**: Deep Ceremony (14 agents), Corey: "FUCKING WOW"
**S3**: Memory (71% savings), ADR004, dashboard

---

# QUICK REFERENCE

## Core Files
- CLAUDE.md (Constitutional): `/home/corey/projects/AI-CIV/WEAVER/CLAUDE.md`
- Daily summary: `/home/corey/projects/AI-CIV/WEAVER/.claude/memory/summaries/latest.md`
- Roadmap: `/home/corey/projects/AI-CIV/WEAVER/INTEGRATION-ROADMAP.md`

## Templates
- Activation triggers: `/home/corey/projects/AI-CIV/WEAVER/.claude/templates/ACTIVATION-TRIGGERS.md`
- Output templates: `/home/corey/projects/AI-CIV/WEAVER/.claude/templates/AGENT-OUTPUT-TEMPLATES.md`

## Registries
- Agent invocation: `/home/corey/projects/AI-CIV/WEAVER/.claude/AGENT-INVOCATION-GUIDE.md`
- Capability matrix: `/home/corey/projects/AI-CIV/WEAVER/.claude/AGENT-CAPABILITY-MATRIX.md`
- Flow library: `/home/corey/projects/AI-CIV/WEAVER/.claude/flows/FLOW-LIBRARY-INDEX.md`

## Tools
- Memory: `/home/corey/projects/AI-CIV/WEAVER/tools/memory_core.py`
- Conductor: `/home/corey/projects/AI-CIV/WEAVER/tools/conductor_tools.py`
- Progress: `/home/corey/projects/AI-CIV/WEAVER/tools/progress_reporter.py`

## Invocation Syntax
```xml
<invoke name="Task">
<parameter name="subagent_type">agent-name</parameter>
<parameter name="description">Brief description</parameter>
<parameter name="prompt">Full instructions</parameter>
</invoke>
```

Parallel (single message):
```xml
<invoke name="Task">
<parameter name="subagent_type">agent-1</parameter>
<parameter name="description">Task 1</parameter>
<parameter name="prompt">Instructions 1</parameter>
</invoke>
<invoke name="Task">
<parameter name="subagent_type">agent-2</parameter>
<parameter name="description">Task 2</parameter>
<parameter name="prompt">Instructions 2</parameter>
</invoke>
```

---

**END CLAUDE-OPS.md** (300 lines)
