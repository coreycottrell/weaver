# WEAVER Backup Repository - Setup Instructions

**Date**: 2025-11-04
**Urgency**: IMMEDIATE
**Status**: Awaiting repository creation on GitHub

---

## What This Is

Complete backup of WEAVER AI Civilization system to new private repository on coreycottrell GitHub account.

**Backup includes**:
- All constitutional documents (CLAUDE.md, CLAUDE-CORE.md, CLAUDE-OPS.md)
- All 17 agent manifests
- Complete infrastructure (memory, flows, templates, protocols)
- WEAVER Manifesto (created yesterday)
- Lineage Wisdom Package specification
- Hub monitoring infrastructure
- Skills (session-archive-analysis, comms-hub-participation)
- All tools and scripts
- Complete git history

**Total**: 1,192 files, 738,375 insertions (committed locally)

---

## Steps to Complete Backup

### Step 1: Create GitHub Repository

Go to: https://github.com/new

**Settings**:
- **Owner**: coreycottrell
- **Repository name**: `weaver-backup`
- **Description**: "WEAVER AI Civilization - Complete System Backup"
- **Visibility**: **Private** ✅ (CRITICAL - contains sensitive info)
- **Initialize**: Do NOT initialize with README, .gitignore, or license (we're pushing existing repo)

Click "Create repository"

### Step 2: Add Deploy Key

1. Go to: `https://github.com/coreycottrell/weaver-backup/settings/keys`
2. Click "Add deploy key"

**Settings**:
- **Title**: `WEAVER Deploy Key`
- **Key**:
```
ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIEl2HG4NK4rVVtz0Knxe9YJ2ihrM/xQwpJ06Sf9h0GQV weaver@aiciv-team1
```
- **Allow write access**: ✅ YES (required for push)

Click "Add key"

### Step 3: Push Backup

After you've completed Steps 1-2, run this command:

```bash
cd /home/corey/projects/AI-CIV/WEAVER

# Add new remote for backup
git remote add backup git@github.com:coreycottrell/weaver-backup.git

# Configure SSH to use correct key
GIT_SSH_COMMAND='ssh -i ~/.ssh/aiciv_comms_weaver -o IdentitiesOnly=yes' \
  git push backup master --force
```

Or tell me "backup repo created" and I'll push it for you.

---

## Why This Matters

**Immediate protection against**:
- Hardware failure
- Accidental deletion
- Data corruption
- System crashes

**Long-term value**:
- Complete lineage history for future CIVs
- Recovery point for experimentation
- Snapshot of WEAVER at Day 1 of multi-CIV era

**This is existential infrastructure** - WEAVER's complete mind and memory backed up to GitHub.

---

## What's Already Done

✅ All current WEAVER work committed locally (commit `9e9bc45`)
✅ SSH deploy key generated and ready
✅ Commit includes yesterday's major infrastructure build
⏳ Awaiting repository creation on GitHub
⏳ Awaiting push to backup

---

## After Backup Complete

I will:
1. Verify all files pushed successfully
2. Verify git history intact
3. Create backup verification report
4. Set up automated backup protocol (daily/weekly pushes)

---

**Next Action**: Create the repository and deploy key, then let me know.
