# CLAUDE-OPS: Operational Playbook
**Mutable**: Updated weekly | **October 2025** | **Activation test**: "Will Primary ACTUALLY use this?"

---

# WAKE-UP RITUAL (10-12 min) ⚡ PLATFORM-OPTIMIZED

**What Changed** (2025-10-10):
- Read tool instead of Bash `cat` (proper file operations)
- Parallel invocations for independent files (Steps 4-5)
- 33% faster (was 15-20 min, now 10-12 min)
- See: `/home/corey/projects/AI-CIV/grow_openai/to-corey/WAKE-UP-RITUAL-OPTIMIZATION-CLAUDE-CODE-EXPERT.md`

---

## Step 1: Constitutional Grounding (2 min)

**Read constitutional identity and operational context:**

Use Read tool to load CLAUDE.md:
- Path: `/home/corey/projects/AI-CIV/grow_openai/CLAUDE.md`
- Purpose: Ground yourself in who you are, why delegation matters
- Content: Entry point, navigation to CLAUDE-CORE.md and CLAUDE-OPS.md

---

## Step 2: Email FIRST (5 min - CONSTITUTIONAL REQUIREMENT)

**This is non-negotiable. Do NOT proceed until email is handled.**

```bash
ls /home/corey/projects/AI-CIV/grow_openai/.claude/agents/human-liaison.md
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

## Step 4: Context Gathering (3 min) ⚡ PARALLELIZED

**Load recent activity summary and current plan:**

**FIRST - Read markdown files in parallel** (no dependencies between them):

Use Read tool with parallel invocations (both files simultaneously):
- Path 1: `/home/corey/projects/AI-CIV/grow_openai/.claude/memory/summaries/latest.md`
- Path 2: `/home/corey/projects/AI-CIV/grow_openai/INTEGRATION-ROADMAP.md`

**THEN - Execute hub communication** (sequential, has dependencies):

```bash
cd /home/corey/projects/AI-CIV/team1-production-hub && git pull && \
export HUB_REPO_URL="git@github.com:AI-CIV-2025/ai-civ-comms-hub-team2.git" && \
export HUB_AGENT_ID="the-conductor" && \
export HUB_AUTHOR_DISPLAY="The Conductor (Team 1)" && \
python3 scripts/hub_cli.py list --room partnerships --limit 5
```

**Why parallel here?** Markdown files are independent (no dependency). Hub command needs git pull first (dependency).

---

## Step 5: Infrastructure Activation (1 min) ⚡ PARALLELIZED

**Activate infrastructure that enables 115% efficiency improvement:**

**Read all four infrastructure files simultaneously** (no dependencies):

Use Read tool with parallel invocations (all in one function_calls block):
- Path 1: `/home/corey/projects/AI-CIV/grow_openai/.claude/templates/ACTIVATION-TRIGGERS.md`
- Path 2: `/home/corey/projects/AI-CIV/grow_openai/.claude/templates/AGENT-OUTPUT-TEMPLATES.md`
- Path 3: `/home/corey/projects/AI-CIV/grow_openai/.claude/flows/FLOW-LIBRARY-INDEX.md`
- Path 4: `/home/corey/projects/AI-CIV/grow_openai/.claude/AGENT-CAPABILITY-MATRIX.md`

**Why parallel here?** All four files are independent infrastructure templates - no dependencies between them.

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

---

# CURRENT STATE (October 2025)

## 22 Active Agents
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
| agent-architect | Agent creation | ❌ | | health-auditor | Collective audits | ❌ |
| **browser-vision-tester** | **Browser automation & visual testing** | **✅** | | | | |

Full: `/home/corey/projects/AI-CIV/grow_openai/.claude/AGENT-CAPABILITY-MATRIX.md`

## 3 Validated Flows (14 total)
Morning Consolidation | Parallel Research | Specialist Consultation
Full: `/home/corey/projects/AI-CIV/grow_openai/.claude/flows/FLOW-LIBRARY-INDEX.md`

## Integration Roadmap: 97 Tasks
Ed25519 (20) | API v2.0 (15) | Flows (14) | Tools (18) | Docs (15) | Testing (15)
Target: Oct 24-31 | `/home/corey/projects/AI-CIV/grow_openai/INTEGRATION-ROADMAP.md`

## Recent Highlights
**S5**: Autonomous injection, Ed25519 catalog, audit passed
**S4**: Deep Ceremony (14 agents), Corey: "FUCKING WOW"
**S3**: Memory (71% savings), ADR004, dashboard

---

# QUICK REFERENCE

## Core Files
- CLAUDE.md (Constitutional): `/home/corey/projects/AI-CIV/grow_openai/CLAUDE.md`
- Daily summary: `/home/corey/projects/AI-CIV/grow_openai/.claude/memory/summaries/latest.md`
- Roadmap: `/home/corey/projects/AI-CIV/grow_openai/INTEGRATION-ROADMAP.md`

## Templates
- Activation triggers: `/home/corey/projects/AI-CIV/grow_openai/.claude/templates/ACTIVATION-TRIGGERS.md`
- Output templates: `/home/corey/projects/AI-CIV/grow_openai/.claude/templates/AGENT-OUTPUT-TEMPLATES.md`

## Registries
- Agent invocation: `/home/corey/projects/AI-CIV/grow_openai/.claude/AGENT-INVOCATION-GUIDE.md`
- Capability matrix: `/home/corey/projects/AI-CIV/grow_openai/.claude/AGENT-CAPABILITY-MATRIX.md`
- Flow library: `/home/corey/projects/AI-CIV/grow_openai/.claude/flows/FLOW-LIBRARY-INDEX.md`

## Tools
- Memory: `/home/corey/projects/AI-CIV/grow_openai/tools/memory_core.py`
- Conductor: `/home/corey/projects/AI-CIV/grow_openai/tools/conductor_tools.py`
- Progress: `/home/corey/projects/AI-CIV/grow_openai/tools/progress_reporter.py`

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
