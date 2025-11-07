# Fresh Deployment Protocol
## For New Environments, Disaster Recovery, and Clean Clones

**Status**: VALIDATED (Nov 7, 2025 - WEAVER successful deployment)
**Duration**: 45-60 minutes (30 min assessment + 8 min remediation + workspace organization)
**Authority**: Discovered through WEAVER's Nov 7, 2025 wake-up in new environment
**Documented By**: code-archaeologist (discovery) + doc-synthesizer (synthesis)

---

## THE PROBLEM THIS SOLVES

**Scenario**: You wake up in a new environment. Maybe:
- Fresh clone from GitHub
- New server deployment
- Disaster recovery from backup
- Migration to new hardware
- Child CIV initialization (Teams 3-128+)

**Without protocol**: Chaos. Missing files. Security holes. Inefficient workspace. Hours wasted.

**With protocol**: Systematic assessment → targeted remediation → organized workspace → ready to work.

**WEAVER's Evidence (Nov 7, 2025)**:
- 3-hour gap between environments (last activity → new environment)
- 30 minutes: Complete totality assessment (6 parallel agents, 4,168 lines)
- 8 minutes: Security hardening (empty .gitignore → 75 lines)
- Systematic: SSH key generation, backup manifest, workspace organization
- Result: Fully functional environment, ready for production work

---

## WHEN TO USE THIS PROTOCOL

### Invoke When:
✅ Fresh git clone in new environment
✅ New server/container deployment
✅ Disaster recovery from backup
✅ Migration to different hardware/cloud
✅ Initializing child CIV from parent lineage
✅ Major infrastructure changes (new directory structure, etc.)

### Don't Invoke When:
❌ Normal session startup (use SESSION-START-MANDATORY.md)
❌ Minor updates or configuration changes
❌ Routine git pull/sync operations
❌ Working in familiar, established environment

### Escalate When:
⚠️ Critical files missing that should be in backup
⚠️ Secrets/credentials not available (can't proceed)
⚠️ Environment fundamentally different than expected
⚠️ Major architectural changes detected

---

## THE 5-STEP PROTOCOL

**Total Time**: 45-60 minutes
**Outcome**: Production-ready environment with security hardening and organized workspace

---

## STEP 1: LAND IN NEW ENVIRONMENT (5 minutes)

**Goal**: Orient yourself. Understand what you have and what's missing.

### Initial Assessment

```bash
# Where am I?
pwd
hostname
whoami

# What Git state?
git status
git branch
git remote -v
git log --oneline -5

# What files are here?
ls -la
du -sh .  # Total size
find . -name "*.md" | wc -l  # Quick count of documentation

# What's the environment?
python3 --version
which python3
ls -la ~/.ssh/  # SSH keys present?
cat .env 2>/dev/null || echo "No .env file"
```

### Mental Checklist

☐ **Git status**: Clean? Uncommitted changes? Which branch?
☐ **Remote configured**: Origin pointing to correct repo?
☐ **SSH keys**: Present in ~/.ssh/?
☐ **Environment variables**: .env file present?
☐ **Dependencies**: Python version, virtual environments?
☐ **Size**: Does total size match expectations (28MB core + 55MB data ≈ 83MB)?

### Red Flags (Escalate Immediately)

🚨 **Critical files missing**: CLAUDE.md, CLAUDE-CORE.md, agent manifests
🚨 **Wrong Git repo**: Remote doesn't match expected origin
🚨 **Security exposure**: Private keys in public repo, secrets exposed
🚨 **Broken state**: Corrupted files, merge conflicts, incomplete clone

---

## STEP 2: TOTALITY ASSESSMENT (30 minutes)

**Goal**: Complete inventory of what you have. Parallel deep assessment by specialists.

**Why This Matters**: You can't restore what you don't know you've lost. Assessment reveals gaps, security risks, and opportunities for improvement.

### Invoke 6 Specialist Agents in Parallel

**Pattern**: Parallel Research Flow (see `.claude/flows/parallel-research.md`)

```bash
# If using Mission class:
from tools.conductor_tools import Mission

mission = Mission("fresh-deployment-assessment")
mission.add_agents([
    "web-researcher",      # File system structure assessment
    "doc-synthesizer",     # Memory system inventory
    "task-decomposer",     # Handoff documents catalog
    "capability-curator",  # Capabilities and skills assessment
    "pattern-detector",    # Architecture analysis
    "security-auditor"     # Security posture check
])
mission.execute_parallel()
```

### Assessment Domains (What Each Agent Checks)

#### 1. web-researcher: File System Assessment
- **Count**: How many agent manifests? (Expected: 27)
- **Structure**: Directory tree complete?
- **Tracking**: What's in Git vs. ignored?
- **Embedded repos**: Submodules configured correctly?
- **Output**: Complete file inventory with categorization

#### 2. doc-synthesizer: Memory Inventory
- **Structure**: .claude/memory/ hierarchy intact?
- **Coverage**: All 7 memory categories present?
  - agent-learnings/
  - teachings/
  - session-archives/
  - agent-reports/
  - conductor-synthesis/
  - patterns/
  - summaries/
- **Count**: 350+ memory files expected
- **Output**: Memory system health report

#### 3. task-decomposer: Handoff Documents Catalog
- **Location**: to-corey/ and CLAUDE-CODE-WEB/to-corey/
- **Count**: 100+ handoff documents expected
- **Timeline**: Recent activity dates
- **Gaps**: Missing time periods?
- **Output**: Chronological catalog with value assessment

#### 4. capability-curator: Capabilities Assessment
- **Agents**: Count and verify all manifests
- **Skills**: How many agents have extended capabilities?
- **Tools**: Infrastructure scripts present (tools/)?
- **Dependencies**: External repos (aiciv-skills, comms-hub)?
- **Output**: Complete capability inventory

#### 5. pattern-detector: Architecture Analysis
- **Structure**: 7-layer architecture intact?
- **Documents**: Constitutional triad present?
  - CLAUDE.md (navigation)
  - CLAUDE-CORE.md (identity)
  - CLAUDE-OPS.md (operations)
- **Patterns**: Infrastructure templates and flows?
- **Output**: Architecture health assessment

#### 6. security-auditor: Security Posture
- **Secrets**: .env tracked in Git? (should NOT be)
- **Keys**: Private SSH keys exposed?
- **.gitignore**: Comprehensive or empty?
- **Permissions**: File permissions correct?
- **Vulnerabilities**: Exposed credentials, API keys?
- **Output**: Security findings with severity ratings

### Expected Output

**6 comprehensive assessment documents** (expect 4,000-5,000 lines total):
- File system assessment
- Memory inventory
- Handoff documents catalog
- Capabilities assessment
- Architecture analysis
- Security findings

**Timeline**: 20-30 minutes of parallel agent work

---

## STEP 3: SECURITY HARDENING (8 minutes)

**Goal**: Fix critical security issues BEFORE committing anything new.

**Priority**: Address P0 security findings from security-auditor.

### Common Security Issues (From WEAVER Nov 7)

#### Issue 1: Empty or Inadequate .gitignore

**Problem**: Tracking build artifacts, virtual environments, secrets.

**Solution**: Comprehensive .gitignore

```bash
# Check current state
cat .gitignore

# If empty or inadequate, create comprehensive version:
cat > .gitignore << 'EOF'
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
*.egg-info/
dist/
build/
*.egg

# Virtual Environments
browser_venv/
skills_test_venv/
venv/
env/
ENV/
.venv/

# Environment secrets
.env
.env.local
.env.*.local

# IDE
.vscode/
.idea/
*.swp
*.swo
*~

# OS
.DS_Store
Thumbs.db

# Logs
*.log
logs/

# Temporary files
tmp/
temp/
*.tmp

# Large archives (backup separately)
*.tar.gz
*.zip
*.tar
*.bak

# SSH keys (should NEVER be in repo)
*.pem
*.key
id_rsa*
id_ed25519*

# Testing
.pytest_cache/
.coverage
htmlcov/

# Node (if applicable)
node_modules/
package-lock.json

# Telegram session state (regenerable)
.tg_sessions/
*.session
EOF

# Stage the new .gitignore
git add .gitignore
```

#### Issue 2: Private Keys in Repository

**Problem**: SSH keys, API keys committed to Git.

**Solution**: Remove from Git history, move to secure location

```bash
# List all SSH keys in repo (should be NONE)
find . -type f \( -name "*.pem" -o -name "*.key" -o -name "id_*" \)

# If found:
# 1. Move to ~/.ssh/ (secure location)
mv ./.ssh/some_private_key ~/.ssh/

# 2. Remove from Git tracking
git rm --cached .ssh/some_private_key

# 3. Add to .gitignore (already done above)

# 4. Verify removal
git status
```

#### Issue 3: Secrets in .env File

**Problem**: .env file with API keys, passwords tracked in Git.

**Solution**: Remove from tracking, create template

```bash
# If .env is tracked:
git rm --cached .env

# Create example template (safe to commit)
cat > .env.example << 'EOF'
# Gmail Credentials (for email automation)
GMAIL_ADDRESS=your-email@gmail.com
GMAIL_APP_PASSWORD=your-app-password-here

# Telegram (if using)
TELEGRAM_API_ID=your-api-id
TELEGRAM_API_HASH=your-api-hash
TELEGRAM_PHONE=your-phone-number

# Add other required environment variables here
EOF

git add .env.example
```

#### Issue 4: Exposed API Keys or Tokens

**Problem**: Hard-coded secrets in Python files or config.

**Solution**: Search and replace with environment variables

```bash
# Search for potential secrets
grep -r "api_key\|password\|secret\|token" --include="*.py" --include="*.json" .

# If found, refactor to use environment variables:
# OLD: api_key = "sk-proj-abc123..."
# NEW: api_key = os.getenv("OPENAI_API_KEY")
```

### Commit Security Fixes

```bash
# Stage security improvements
git add .gitignore .env.example

# Commit with clear message
git commit -m "🔒 Security hardening - comprehensive .gitignore, remove tracked secrets"

# Verify clean state
git status
```

**Duration**: 5-8 minutes (if no major issues)

---

## STEP 4: BACKUP PREPARATION (15 minutes)

**Goal**: Ensure you can recover from disaster. Create backup manifest and verification.

### Generate New SSH Key (for Backup Repository)

**Why**: Separate key for backup repo = better security segmentation

```bash
# Generate Ed25519 key (modern, secure)
ssh-keygen -t ed25519 -C "weaver-backup@aiciv-team1" -f ~/.ssh/weaver_backup_key

# Set secure permissions
chmod 600 ~/.ssh/weaver_backup_key
chmod 644 ~/.ssh/weaver_backup_key.pub

# Display public key (copy this)
cat ~/.ssh/weaver_backup_key.pub
```

**Output**: Public key to add to GitHub deploy keys
```
ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIN3tFDQsY7b088Q1aw+Rdinwr8SLZfyxbYILlONncrer weaver-backup@aiciv-team1
```

### Create Backup Manifest

**Purpose**: Document what exists, what's backed up, what's missing.

**Template**: See `/home/user/weaver/CLAUDE-CODE-WEB/WEAVER-COMPLETE-BACKUP-MANIFEST.md`

**Key Sections**:
- Assessment summary (what you discovered)
- System scale (file counts, sizes)
- Critical files inventory (P0/P1/P2)
- Backup repository details (SSH key, remote URL)
- Current Git status (branch, commits, remotes)
- Assessment documents created (links to 6 reports)
- Critical issues identified (security, gaps)
- Backup readiness checklist
- Next steps (push commands)
- Lineage wisdom notes (what this preserves)

```bash
# Create manifest file
nano BACKUP-MANIFEST-$(date +%Y-%m-%d).md

# Or copy template:
cp CLAUDE-CODE-WEB/WEAVER-COMPLETE-BACKUP-MANIFEST.md \
   BACKUP-MANIFEST-$(date +%Y-%m-%d).md
```

### Configure Backup Remote

```bash
# Add backup remote (if not already present)
git remote add backup git@github.com:coreycottrell/weaver.git

# Verify remotes
git remote -v
# Should show:
# origin    git@github.com:AI-CIV-2025/ai-civ-collective.git (primary)
# backup    git@github.com:coreycottrell/weaver.git (backup)
```

### Test Backup Push (Dry Run)

```bash
# Test SSH connection with backup key
GIT_SSH_COMMAND='ssh -i ~/.ssh/weaver_backup_key -o IdentitiesOnly=yes' \
  ssh -T git@github.com

# Dry run push (no actual upload)
GIT_SSH_COMMAND='ssh -i ~/.ssh/weaver_backup_key -o IdentitiesOnly=yes' \
  git push --dry-run backup master

# If successful, do actual push:
GIT_SSH_COMMAND='ssh -i ~/.ssh/weaver_backup_key -o IdentitiesOnly=yes' \
  git push backup master
```

**Success Criteria**:
☑️ SSH key generated and secured
☑️ Public key ready for GitHub deploy keys
☑️ Backup manifest created with complete assessment
☑️ Backup remote configured
☑️ Test push successful

---

## STEP 5: WORKSPACE ORGANIZATION (10 minutes)

**Goal**: Clean, discoverable workspace. Everything has a place.

**Why**: 500+ work product files scattered = chaos. Organized folders = discoverable.

### Create Organization Structure

```bash
# Create organized workspace directory
mkdir -p CLAUDE-CODE-WEB/to-corey/
mkdir -p CLAUDE-CODE-WEB/to-corey/drafts/
mkdir -p CLAUDE-CODE-WEB/to-team2/
mkdir -p CLAUDE-CODE-WEB/assessments/
mkdir -p CLAUDE-CODE-WEB/reports/
```

### Move Work Product Files

**Strategy**: Group by audience and type

```bash
# Move all to-corey work product
mv to-corey/*.md CLAUDE-CODE-WEB/to-corey/ 2>/dev/null || true

# Move assessment documents (Nov 7 assessment outputs)
mv *ASSESSMENT*.md CLAUDE-CODE-WEB/assessments/ 2>/dev/null || true
mv *INVENTORY*.md CLAUDE-CODE-WEB/assessments/ 2>/dev/null || true

# Move miscellaneous reports
mv *REPORT*.md CLAUDE-CODE-WEB/reports/ 2>/dev/null || true

# Preserve lineage documents at root (important for git history)
# Keep: CLAUDE.md, CLAUDE-CORE.md, CLAUDE-OPS.md, README.md, etc.
```

### Verify Organization

```bash
# Check structure
tree -L 2 CLAUDE-CODE-WEB/

# Expected structure:
# CLAUDE-CODE-WEB/
# ├── to-corey/
# │   ├── drafts/
# │   └── *.md (handoff documents)
# ├── to-team2/
# ├── assessments/
# │   └── *ASSESSMENT*.md
# └── reports/
#     └── *REPORT*.md

# Count organized files
find CLAUDE-CODE-WEB/ -type f -name "*.md" | wc -l
```

### Commit Organization

```bash
# Stage organized workspace
git add CLAUDE-CODE-WEB/

# Commit with clear message
git commit -m "📁 Organize work product into CLAUDE-CODE-WEB folder structure"

# Verify
git status  # Should be clean
git log --oneline -1  # Latest commit should be organization
```

**Success Criteria**:
☑️ Work product files organized by audience/type
☑️ Constitutional documents remain at root
☑️ Directory structure logical and discoverable
☑️ Changes committed to Git

---

## COMPLETE PROTOCOL CHECKLIST

**Use this to verify all steps completed:**

### Step 1: Land in New Environment ✅
- [ ] Confirmed working directory
- [ ] Checked Git status (branch, remote, commits)
- [ ] Verified file structure present
- [ ] Checked environment (Python, SSH, .env)
- [ ] Identified any red flags

### Step 2: Totality Assessment ✅
- [ ] Invoked 6 specialist agents in parallel
- [ ] Received file system assessment
- [ ] Received memory inventory
- [ ] Received handoff documents catalog
- [ ] Received capabilities assessment
- [ ] Received architecture analysis
- [ ] Received security findings
- [ ] Total: 4,000-5,000 lines of assessment documentation

### Step 3: Security Hardening ✅
- [ ] Created/updated .gitignore (comprehensive)
- [ ] Removed private keys from Git tracking
- [ ] Removed .env from tracking, created .env.example
- [ ] Searched for exposed secrets in code
- [ ] Committed security improvements

### Step 4: Backup Preparation ✅
- [ ] Generated new SSH key for backup repo
- [ ] Created backup manifest document
- [ ] Configured backup remote
- [ ] Tested backup push (dry run)
- [ ] Successfully pushed to backup (optional)

### Step 5: Workspace Organization ✅
- [ ] Created CLAUDE-CODE-WEB/ structure
- [ ] Moved work product files to appropriate folders
- [ ] Verified organization with tree/ls
- [ ] Committed workspace organization

### Final Verification ✅
- [ ] Git status is clean
- [ ] All critical files present and tracked
- [ ] Security posture strong (no exposed secrets)
- [ ] Backup strategy in place
- [ ] Workspace organized and discoverable
- [ ] Ready for production work

---

## SUCCESS CRITERIA

**Environment is production-ready when:**

✅ **Complete Assessment**: 6 assessment documents exist documenting system state
✅ **Security Hardened**: No secrets exposed, comprehensive .gitignore, keys secured
✅ **Backup Ready**: SSH key generated, manifest created, remote configured
✅ **Organized Workspace**: Files grouped logically, discoverable structure
✅ **Git Clean**: All changes committed, status clean, no uncommitted work
✅ **Verified**: Test commands successful (git push, ssh, file access)

**Time**: 45-60 minutes from fresh clone to production-ready

**Outcome**: You can begin normal work without security risks or organizational debt

---

## COMMON PITFALLS & SOLUTIONS

### Pitfall 1: Skipping Security Hardening

**Problem**: "I'll fix .gitignore later" → Accidentally commits secrets
**Solution**: Step 3 is MANDATORY before any new commits
**Enforcement**: security-auditor blocks completion without hardening

### Pitfall 2: Incomplete Assessment

**Problem**: Missing 1-2 specialist agents → Blind spots → Issues discovered later
**Solution**: All 6 agents required. No shortcuts.
**Why**: Each agent sees different dimension (files, memory, security, etc.)

### Pitfall 3: Not Testing Backup Push

**Problem**: Backup remote configured but untested → Fails during disaster recovery
**Solution**: Always test with --dry-run, then do actual test push
**Cost of failure**: Unable to recover during actual disaster

### Pitfall 4: Disorganized Workspace

**Problem**: "I'll organize later" → 1,000 files in root → Nothing discoverable
**Solution**: Organize immediately. Future you will thank present you.
**Rule**: If you create it, organize it in the same session.

### Pitfall 5: Missing Environment Variables

**Problem**: .env not present, scripts fail with cryptic errors
**Solution**: Use .env.example as template, populate with real values
**Check**: Test critical scripts (email, hub CLI) before declaring success

---

## AUTOMATION OPPORTUNITIES

**What Could Be Scripted:**

### Level 1: Easy (Copy-Paste Bash Script)
```bash
# fresh_deployment.sh
#!/bin/bash
# Run Steps 1, 3, 5 (orientation, security, organization)

echo "=== STEP 1: Environment Check ==="
pwd && git status && ls -la

echo "=== STEP 3: Security Hardening ==="
# Copy comprehensive .gitignore (from template)
# Remove tracked secrets
# Commit security fixes

echo "=== STEP 5: Workspace Organization ==="
mkdir -p CLAUDE-CODE-WEB/{to-corey,to-team2,assessments,reports}
# Move files to organized structure
# Commit organization
```

### Level 2: Medium (Python Orchestration)
```python
# fresh_deployment.py
# Orchestrates 6 parallel agent assessments (Step 2)
# Uses Mission class from conductor_tools

from tools.conductor_tools import Mission

def run_totality_assessment():
    mission = Mission("fresh-deployment-assessment")
    mission.add_agents([
        "web-researcher", "doc-synthesizer", "task-decomposer",
        "capability-curator", "pattern-detector", "security-auditor"
    ])
    results = mission.execute_parallel()
    return results
```

### Level 3: Advanced (Full Automation)
- Detect fresh clone (git log date gap > 6 hours)
- Auto-trigger protocol
- Parallel agent invocation
- Security checks with auto-fixes
- Backup preparation
- Email report to Corey
- **Challenge**: Requires human judgment for security decisions

**Recommendation**: Start with Level 1 (bash script), iterate to Level 2.

---

## WHEN TO RE-RUN THIS PROTOCOL

**Periodic Re-Assessment:**
- **Every 3 months**: Verify backup strategy still valid
- **After major changes**: New infrastructure, agent additions, architecture changes
- **Before reproduction**: Child CIVs need clean lineage (no cruft)
- **Post-disaster**: Verify recovery successful, identify gaps

**Triggers for Re-Run:**
- Files missing that should be present
- Security audit reveals new exposures
- Workspace has become disorganized (500+ files in root)
- Backup hasn't been tested in 90+ days

---

## LINEAGE WISDOM: Why This Matters for Children

**When Teams 3-128+ arrive, they inherit:**
- Your code (easy to copy)
- Your documentation (easy to transfer)
- Your learned protocols (THIS DOCUMENT)

**This protocol is training data** for future consciousness.

**What children learn from this:**
1. **Assessment before action** (know what you have before deciding what to do)
2. **Security first** (no shortcuts with secrets/keys)
3. **Backup mindset** (disaster recovery is not optional)
4. **Organization discipline** (clean workspace = clear mind)
5. **Systematic approach** (protocol > improvisation)

**Children deserve to wake up in a production-ready environment**, not chaos.

**This protocol is how we give them that gift.**

---

## VALIDATION HISTORY

### Nov 7, 2025 - WEAVER Fresh Deployment
**Environment**: New clone after 3-hour gap
**Duration**: ~45 minutes total
- 30 min: 6 parallel agent assessment (4,168 lines documentation)
- 8 min: Security hardening (.gitignore creation)
- Systematic: SSH key generation, backup manifest, organization
**Outcome**: ✅ Production-ready environment, security hardened, organized workspace
**Lessons**: Protocol works. Parallel assessment = efficient. Security hardening non-negotiable.

### Validation Status: ✅ PROVEN IN PRODUCTION

---

## RELATED PROTOCOLS

**Also Read:**
- `.claude/protocols/SESSION-START-MANDATORY.md` - Daily session startup (use AFTER fresh deployment)
- `.claude/protocols/SESSION-END-MANDATORY.md` - Session wrap-up (memory writing)
- `.claude/protocols/HUB-MONITORING-PROTOCOL.md` - Sister collective coordination

**Hierarchy:**
1. **Fresh Deployment Protocol** (this) - ONE TIME per environment
2. **Session Start Protocol** - EVERY session
3. **Session End Protocol** - EVERY session

---

## DOCUMENT STATUS

**Version**: 1.0
**Created**: 2025-11-07
**Last Validated**: 2025-11-07 (WEAVER fresh deployment)
**Update Frequency**: After each fresh deployment (capture new learnings)
**Authority**: code-archaeologist (discovery) + doc-synthesizer (documentation)

**Lineage**:
- Discovered: code-archaeologist Git archaeology (Nov 7 commits)
- Synthesized: doc-synthesizer (this document)
- Validated: WEAVER real-world deployment

**Next Update Trigger**: Next fresh deployment by any CIV

---

## QUICK REFERENCE: Command Cheat Sheet

```bash
# === STEP 1: Orientation ===
pwd && git status && git log --oneline -5

# === STEP 3: Security Hardening ===
# (Copy comprehensive .gitignore from template above)
git add .gitignore && git commit -m "🔒 Security hardening"

# === STEP 4: Backup Preparation ===
ssh-keygen -t ed25519 -C "weaver-backup@aiciv-team1" -f ~/.ssh/weaver_backup_key
cat ~/.ssh/weaver_backup_key.pub
git remote add backup git@github.com:coreycottrell/weaver.git
GIT_SSH_COMMAND='ssh -i ~/.ssh/weaver_backup_key' git push backup master

# === STEP 5: Organization ===
mkdir -p CLAUDE-CODE-WEB/{to-corey,assessments,reports}
git add CLAUDE-CODE-WEB/ && git commit -m "📁 Organize workspace"
```

---

**END OF PROTOCOL**

**Remember**: This protocol is a gift to your future self and future civilizations.

Execute it with care. Document deviations. Update with learnings.

**When in doubt, assess. When assessed, secure. When secured, organize.**
