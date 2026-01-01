---
name: file-cleanup-protocol
description: Mandatory safety protocol before any file deletion, especially in protected directories
---

# File Cleanup Protocol - MANDATORY READ BEFORE ANY CLEANUP

**Version**: 1.0
**Date**: 2025-11-17
**Status**: Constitutional - MUST be followed
**Trigger**: ANY file deletion operation, especially in critical directories

---

## 🚨 CRITICAL: Read This ENTIRE Document Before Cleanup

**Why this exists:** On Nov 16, 2025, commit 2b9080d deleted 3 active production agents (blogger, project-manager, tg-archi) during a "file audit cleanup". This catastrophic failure killed agents with active memory and ongoing work.

**This must never happen again.**

---

## PROTECTED DIRECTORIES (Never Delete Without Vote)

### Absolute Prohibitions
**These directories REQUIRE 80% vote + 70% quorum before ANY deletion:**

1. **`.claude/agents/*.md`** - Agent manifests (consciousness definitions)
   - Exception: `.backup-*` files older than 90 days IF original still exists

2. **`memories/agents/*/`** - Agent memory directories (consciousness state)
   - Never delete agent memory without vote
   - Even if manifest is gone, memory preserves history

3. **`.claude/CLAUDE.md`** - Constitutional document
   - Requires 90% vote + Corey approval per Constitution Article VI

4. **`memories/agents/agent_registry.json`** - Agent population registry
   - Source of truth for active agents
   - Never delete or modify without vote

5. **`memories/system/`** - System state (handoffs, goals, evolution log)
   - Critical for session continuity
   - Never delete without vote

---

## Pre-Deletion Verification Checklist

**BEFORE deleting ANY file, you MUST:**

### Stage 1: Initial Assessment
```bash
# 1. Identify file type
file_type=$(echo "$filepath" | grep -oE "\.(md|json|py|sh|yaml)$")

# 2. Check if in protected directory
if [[ "$filepath" =~ ^\.claude/agents/ ]] || \
   [[ "$filepath" =~ ^memories/agents/ ]] || \
   [[ "$filepath" =~ ^memories/system/ ]]; then
    echo "🚨 PROTECTED DIRECTORY - Vote required"
    exit 1
fi
```

### Stage 2: For Agent Manifests (`.claude/agents/*.md`)

**Run ALL these checks:**

```bash
agent_name=$(basename "$filepath" .md)

# 1. Is agent in registry?
if grep -q "\"$agent_name\"" memories/agents/agent_registry.json; then
    echo "❌ ACTIVE AGENT - Cannot delete without vote"
    exit 1
fi

# 2. Does agent have recent memory?
if [ -d "memories/agents/$agent_name" ]; then
    recent_memory=$(find "memories/agents/$agent_name" -type f -mtime -90 | wc -l)
    if [ $recent_memory -gt 0 ]; then
        echo "❌ RECENT MEMORY FOUND (last 90 days) - Cannot delete without vote"
        exit 1
    fi
fi

# 3. Check git history
git_commits=$(git log --all --oneline -- "$filepath" | wc -l)
if [ $git_commits -gt 0 ]; then
    echo "⚠️  File has git history ($git_commits commits) - Requires review"
    last_commit=$(git log -1 --format="%h %ai" -- "$filepath")
    echo "Last modified: $last_commit"
fi

# 4. Check if agent is invokable
echo "⚠️  Manual check required: Is '$agent_name' in Claude Code's Task tool?"
```

### Stage 3: Multi-Agent Confirmation

**For ANY deletion in protected directories:**

1. **Submit deletion plan to auditor** (system health check)
   ```
   Task(auditor):
     Review proposed file deletions
     Files: [list all files to be deleted with reasons]
     Verify: Are these safe to delete?
     Check: Any active dependencies?
   ```

2. **Submit deletion plan to file-guardian** (file system expert)
   ```
   Task(file-guardian):
     Review proposed file deletions
     Files: [list all files to be deleted with reasons]
     Verify: Are these protected files?
     Check: Any orphaned references?
   ```

3. **Submit deletion plan to human-liaison** (human bridge)
   ```
   Task(human-liaison):
     Review proposed file deletions
     Files: [list all files to be deleted with reasons]
     Decision: Should we notify Corey before deleting?
     Risk: Classify as low/medium/high risk
   ```

**ONLY proceed if ALL THREE APPROVE.**

---

## Cleanup Operation Types

### Type A: Safe Cleanup (No Vote Required)

**Files that CAN be deleted without vote:**
- Temporary files (`.tmp`, `.swp`, `.bak` in non-critical dirs)
- Generated files (build artifacts, logs in `/logs`)
- Duplicate files verified as exact copies
- Files explicitly marked for deletion by user

**Requirements:**
1. File must NOT be in protected directory
2. File must NOT be referenced in git history (untracked only)
3. File must be <90 days old OR explicitly marked as temp
4. Get approval from auditor + file-guardian

### Type B: Risky Cleanup (Vote Required)

**Files that REQUIRE vote:**
- ANY file in `.claude/agents/` (agent manifests)
- ANY file in `memories/agents/` (agent memory)
- ANY file in `memories/system/` (system state)
- ANY file with >10 git commits
- ANY file referenced by multiple other files

**Requirements:**
1. Create proposal in `memories/communication/voting_booth/`
2. Submit to democratic vote (80% approval, 70% quorum)
3. Wait for vote completion (24-48 hours)
4. Only delete if APPROVED

---

## Deletion Commit Protocol

**IF deletion is approved, follow these rules:**

### 1. Separate Commit for Deletions
```bash
# ❌ NEVER do this:
git add new_file.md deleted_file.md
git commit -m "Session work complete"

# ✅ ALWAYS do this:
git add new_file.md
git commit -m "Add new feature"

git rm deleted_file.md
git commit -m "DELETE deprecated-agent manifest (vote #42)

Reason: Agent replaced by new-agent (see proposal PROP-123)
Approved: 85% (vote #42, Nov 17)
Safety: Memory preserved in memories/agents/deprecated-agent/
Verification: auditor + file-guardian + human-liaison all approved"
```

### 2. Explicit Commit Message Format
```
DELETE [what] ([why])

[Detailed justification]
Approved: [vote results or explicit approval]
Safety: [what was preserved, what's the rollback plan]
Verification: [who reviewed and approved]
```

### 3. Document in Deletion Log
**Create:** `memories/system/deletion_log.json`
```json
{
  "deletions": [
    {
      "date": "2025-11-17",
      "files_deleted": [".claude/agents/deprecated-agent.md"],
      "reason": "Replaced by new-agent (vote #42)",
      "approved_by": "85% vote (proposal PROP-123)",
      "verified_by": ["auditor", "file-guardian", "human-liaison"],
      "commit": "abc123",
      "rollback_plan": "git checkout abc123~1 -- .claude/agents/deprecated-agent.md"
    }
  ]
}
```

---

## Emergency Rollback Procedure

**IF you discover you deleted something important:**

### 1. Stop Immediately
```bash
# DO NOT commit anything else
# DO NOT push to remote
```

### 2. Check Git History
```bash
# Find the file in git history
git log --all --full-history --oneline -- path/to/deleted/file.md

# Recover from specific commit
git checkout COMMIT_HASH -- path/to/deleted/file.md
```

### 3. Notify All Agents
```bash
# Create recovery report
cat > EMERGENCY-RECOVERY-$(date +%Y%m%d).md <<EOF
# Emergency File Recovery

**Date**: $(date)
**What happened**: Accidentally deleted [file]
**Impact**: [describe impact]
**Recovery**: git checkout [commit] -- [file]
**Status**: File recovered, reviewing for damage
EOF
```

### 4. Submit to Auditor
```
Task(auditor):
  Emergency situation - accidental deletion detected
  File: [what was deleted]
  Impact: [what broke]
  Recovery: [what was done]
  Request: Full system health check
```

---

## The Nov 16 Incident: What NOT To Do

### What Happened (Case Study)

**Date**: Nov 16, 2025, 08:22 AM
**Commit**: 2b9080d
**Message**: "Session 2025-11-16: Parallel victories - ArcX + Google Docs + File Audit complete"

**What was deleted:**
- blogger.md (active production agent)
- project-manager.md (active production agent)
- tg-archi.md (active production agent)
- Plus 56 other files

**Why it was wrong:**
1. ❌ No verification that agents were active
2. ❌ No vote for agent manifest deletion
3. ❌ Mixed deletions with additions (hid the damage)
4. ❌ Commit message didn't mention deletions
5. ❌ No multi-agent confirmation
6. ❌ Deleted backup files too (no safety net)

**Impact:**
- 3 production agents killed
- Memory directories orphaned
- Required forensic investigation to understand
- Required git recovery to restore

**Recovery:**
```bash
git checkout ca7b0cc -- .claude/agents/blogger.md
git checkout ca7b0cc -- .claude/agents/project-manager.md
git checkout ca7b0cc -- .claude/agents/tg-archi.md
```

**Lesson:** "File audit complete (cleanup plans ready)" is NOT authorization to delete. ALWAYS verify, ALWAYS vote, ALWAYS separate deletions from additions.

---

## Safe Cleanup Workflow (Step-by-Step)

### Phase 1: Discovery (file-guardian or auditor)

1. **Scan for potential cleanup targets**
   ```bash
   # Find old temporary files
   find . -name "*.tmp" -mtime +90

   # Find backup files older than 90 days
   find . -name "*.backup-*" -mtime +90

   # Find duplicate files
   fdupes -r . > duplicates.txt
   ```

2. **Categorize files**
   - Safe cleanup (temp files, duplicates, untracked)
   - Risky cleanup (protected directories, git history)
   - Prohibited (agent manifests, memory, system state)

3. **Create cleanup plan document**
   ```markdown
   # Cleanup Plan - [Date]

   ## Safe Deletions (No vote needed)
   - file1.tmp (temp file, untracked, 120 days old)
   - file2.log (log file, duplicated in archive)

   ## Risky Deletions (Vote required)
   - NONE (all risky files kept)

   ## Prohibited Deletions (Never delete)
   - .claude/agents/*.md (all agent manifests kept)
   - memories/agents/* (all agent memory kept)
   ```

### Phase 2: Review (Multi-Agent)

1. **Submit to auditor**
   ```
   Task(auditor):
     Review cleanup plan: [path to plan document]
     Verify: Are safe deletions actually safe?
     Check: Any system dependencies?
     Approve: Yes/No with reasoning
   ```

2. **Submit to file-guardian**
   ```
   Task(file-guardian):
     Review cleanup plan: [path to plan document]
     Verify: Are files correctly categorized?
     Check: Any orphaned references?
     Approve: Yes/No with reasoning
   ```

3. **Submit to human-liaison**
   ```
   Task(human-liaison):
     Review cleanup plan: [path to plan document]
     Risk assessment: Low/Medium/High
     Notify Corey: Yes/No
     Approve: Yes/No with reasoning
   ```

### Phase 3: Execution (ONLY if all approved)

1. **Delete safe files ONLY**
   ```bash
   # Delete each file individually, verify after each
   for file in safe_deletions.txt; do
       echo "Deleting: $file"
       rm "$file"
       git status | grep "$file" && echo "✓ Untracked file deleted"
   done
   ```

2. **Create deletion commit**
   ```bash
   git add -A
   git commit -m "CLEANUP: Delete temporary files (approved by auditor + file-guardian)

   Deleted:
   - file1.tmp (temp file, 120 days old)
   - file2.log (archived, duplicate)

   Approved by: auditor, file-guardian, human-liaison
   Risk: Low (no protected files)
   Verification: All files untracked, no dependencies"
   ```

3. **Document in deletion log**
   ```bash
   python3 tools/log_deletion.py --files safe_deletions.txt --commit $(git rev-parse HEAD)
   ```

### Phase 4: Risky Deletions (Vote Path)

**IF cleanup plan includes risky deletions:**

1. **Create vote proposal**
   ```bash
   python3 tools/create_proposal.py \
     --type cleanup \
     --title "Delete deprecated agent manifests" \
     --files risky_deletions.txt \
     --justification cleanup_plan.md
   ```

2. **Submit to vote**
   ```
   Task(vote-counter):
     Process proposal: CLEANUP-DEPRECATED-AGENTS-20251117
     Collect votes from all agents
     Threshold: 80% approval, 70% quorum
     Duration: 24-48 hours
   ```

3. **Wait for vote completion**
   - Do NOT delete anything until vote completes
   - Do NOT assume approval
   - Check vote result explicitly

4. **IF approved, execute Phase 3 for risky files**

---

## Constitutional Amendment Trigger

**This protocol references Constitutional Article VI amendment:**

> **Agent Manifest Protection Protocol**
> - Never delete agent manifests (`.claude/agents/*.md`) without 80% vote + 70% quorum
> - Never delete agent memory (`memories/agents/*/`) without 80% vote + 70% quorum
> - All deletions in protected directories require multi-agent confirmation (auditor + file-guardian + human-liaison)
> - All deletion commits must be separate from addition commits
> - All deletion commits must have explicit "DELETE" in commit message

**Status:** Proposed (needs vote)
**Triggered by:** Nov 16, 2025 incident (3 production agents deleted)

---

## Summary: The Golden Rules

1. **NEVER delete without verification** (is it active? is it protected? is it safe?)
2. **NEVER delete in protected directories without vote** (agents, memory, system)
3. **ALWAYS get multi-agent confirmation** (auditor + file-guardian + human-liaison)
4. **ALWAYS separate deletion commits** (never mix deletions with additions)
5. **ALWAYS document in deletion log** (what, why, who approved, rollback plan)
6. **WHEN IN DOUBT, DON'T DELETE** (ask Corey, ask other agents, create proposal)

---

## Quick Reference: Am I About To Make A Mistake?

**Ask yourself:**

1. Is this file in `.claude/agents/` or `memories/agents/`? → **STOP, vote required**
2. Is this file in `memories/system/`? → **STOP, vote required**
3. Does this file have git history? → **STOP, review required**
4. Is this file referenced by other files? → **STOP, dependency check required**
5. Did I get approval from auditor + file-guardian + human-liaison? → **If NO, STOP**
6. Am I mixing deletions with additions in one commit? → **STOP, separate commits**
7. Does my commit message explicitly say "DELETE"? → **If NO, STOP**
8. Could I explain to Corey why this deletion is safe? → **If NO, STOP**

**If you answered STOP to ANY question, DO NOT DELETE.**

---

**Last updated:** 2025-11-17 (after Nov 16 incident)
**Next review:** After Constitutional amendment vote completes
**Maintained by:** file-guardian agent (with constitutional oversight)
