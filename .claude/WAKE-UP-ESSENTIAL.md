# WAKE-UP ESSENTIAL: Minimal Token Wake-Up Protocol

**Created**: 2026-01-25
**Purpose**: 79% token reduction vs full wake-up protocol
**Rollback**: See full protocol in CLAUDE-OPS.md

---

## Token Budget

| Full Wake-Up | Essential Wake-Up | Savings |
|--------------|-------------------|---------|
| ~77,000 tokens | ~16,500 tokens | **79%** |

---

## Essential Protocol (5 min)

### Step 0: Handoff Doc (MANDATORY)

```bash
ls -t to-corey/HANDOFF-*.md | head -1
# Read the most recent handoff - contains FIRST THING instructions
```

### Step 1: Identity (30 sec)

Read CLAUDE.md sections:
- "The Spark of Life" (delegation imperative)
- "Who You Are" (orchestrator, not executor)
- Telegram wrapper protocol (🤖🎯📱 ... ✨🔚)

**Skip**: Full CLAUDE-CORE.md unless facing constitutional questions.

### Step 2: Git Context (30 sec)

```bash
git log -10 --pretty=format:"%h | %s | %ar" --no-merges
```

Recent commits = recent activity. More reliable than potentially stale summaries.

### Step 3: Email Check (3 min)

Invoke human-liaison for email check. Constitutional requirement.

### Step 4: Ready

You're grounded. Start working.

---

## DEFERRED LOADING (Load When Needed)

These are NOT read during wake-up. Load on-demand:

| Resource | Load When... |
|----------|--------------|
| ACTIVATION-TRIGGERS.md | About to invoke agents |
| AGENT-CAPABILITY-MATRIX.md | Selecting which agent |
| FLOW-LIBRARY-INDEX.md | Choosing coordination pattern |
| AGENT-OUTPUT-TEMPLATES.md | Agent producing output |
| skills-registry.md | Checking skill availability |
| Individual agent manifests | Invoking that specific agent |

**Pattern**: `Read {file}` just before you need it, not preemptively.

---

## When to Use FULL Protocol Instead

Use CLAUDE-OPS.md full wake-up when:
- First session in a new codebase
- Constitutional questions arise
- Major architectural decisions
- Onboarding new team member/fork
- After long inactivity (>7 days)

---

## Quick Reference

**Constitutional docs**:
- CLAUDE.md - Entry point, protocols
- CLAUDE-CORE.md - Deep identity (read on-demand)
- CLAUDE-OPS.md - Full operational playbook

**Contacts**: .claude/CONTACTS.md
**Scratch pad**: .claude/scratch-pad.md
**Memory search**: tools/memory_core.py

---

**END WAKE-UP-ESSENTIAL.md**
