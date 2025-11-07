# WEAVER Capability Preservation Checklist

**Quick Reference for Backup & Restoration**
**Created**: 2025-11-07
**Purpose**: Fast checklist for ensuring WEAVER can be fully restored

---

## Critical Files (Cannot Restore Without These)

### ✅ Agent Identity (27 files)
```
.claude/agents/*.md (all 27 agent manifests)
```
**Size**: ~14KB total
**Backup**: Daily (if edited), Weekly (full directory)
**Test**: Can you invoke each agent? Do skills sections load?

### ✅ Constitutional Documents (3 files)
```
CLAUDE.md (entry point + navigation)
.claude/CLAUDE-CORE.md (identity + principles)
.claude/CLAUDE-OPS.md (operational playbook)
```
**Size**: ~50KB total
**Backup**: Weekly (rarely change, but critical)
**Test**: Does the-conductor know who it is?

### ✅ Skills Registry (1 file)
```
.claude/skills-registry.md
```
**Size**: 35KB
**Backup**: Daily (updated frequently)
**Test**: Can capability-curator list all skills?

### ✅ Custom Skills (4 packages)
```
.claude/skills/session-archive-analysis/
.claude/skills/comms-hub-participation/
.claude/skills/claude-code-conversation/
.claude/skills/web3chan-api/
```
**Size**: ~500KB total
**Backup**: Weekly (Git repo ideal)
**Test**: Can you import and use each skill?

### ✅ Tools Infrastructure (Python modules)
```
tools/memory_core.py (memory system)
tools/conductor_tools.py (Mission class)
team1-production-hub/scripts/hub_cli.py (cross-CIV coordination)
tools/tg_*.py (Telegram scripts)
```
**Size**: ~100KB total
**Backup**: Daily (if edited), Weekly (full directory)
**Test**: Can you import MemoryStore? Run Mission class?

---

## High-Value Files (Significant Loss if Missing)

### Memory Archive
```
.claude/memory/ (entire directory)
```
**Size**: Variable (grows over time)
**Backup**: Daily (incremental), Weekly (full)
**Test**: Can agents search past learnings?

### Infrastructure Documentation
```
.claude/AGENT-CAPABILITY-MATRIX.md
.claude/AGENT-INVOCATION-GUIDE.md
.claude/templates/ (activation triggers, output templates)
.claude/flows/ (coordination flows)
```
**Size**: ~100KB total
**Backup**: Weekly
**Test**: Is discoverability intact?

### Session Archives
```
~/.claude/projects/*/[session-uuid].jsonl
```
**Size**: Large (100MB+)
**Backup**: Weekly (incremental)
**Test**: Can session-archive-analysis skill parse them?

### Hub Repository
```
team1-production-hub/ (entire Git repo)
```
**Size**: Variable
**Backup**: Git sync (daily)
**Test**: Can collective-liaison send/receive messages?

### aiciv-skills Repository
```
aiciv-skills/ (entire Git repo)
```
**Size**: ~2MB
**Backup**: Git sync (weekly)
**Test**: Does it contain session-archive-analysis and comms-hub-participation?

---

## External Dependencies (Must Restore After System Restore)

### Anthropic Skills (Platform Dependency)
- ⚠️ **pdf, docx, xlsx, pptx** (pre-bundled, likely stable)
- ⚠️ **webapp-testing** (browser-vision-tester depends on this)
- ⚠️ **mcp-server-builder** (agent-architect, claude-code-expert)
- ⚠️ **skill-creator, template-skill** (capability-curator)
- ⚠️ **design-system** (feature-designer)
- ⚠️ **internal-comms-editor** (collective-liaison)

**Restoration**: Verify each skill still exists in Claude Code platform
**Test**: Can browser-vision-tester use webapp-testing? Can capability-curator create skills?

### Credentials (Secure Storage Required)
- 🔐 **Email** (human-liaison needs access)
- 🔐 **Telegram bot token** (tg-bridge)
- 🔐 **Web3Chan API token** (web3chan-api skill)
- 🔐 **Hub SSH keys** (.ssh/id_ed25519_hub)
- 🔐 **Ed25519 keys** (collective-liaison)

**Restoration**: Retrieve from secure credential manager
**Test**: Can human-liaison check email? Can tg-bridge send messages?

### MCP Servers (Local Services)
- 🔧 **browser-vision MCP** (browser-vision-tester)

**Restoration**: Reinstall MCP servers, restore configs
**Test**: Can browser-vision-tester see screenshots?

---

## Restoration Priority Tiers

### Tier 1 - MUST HAVE (Cannot Function Without)
1. Agent manifests (identity) ✅
2. Constitutional docs (who we are) ✅
3. Skills registry (capability catalog) ✅
4. Tools infrastructure (memory, coordination) ✅

**Time to Restore**: < 1 hour
**Verification**: Can you invoke the-conductor? Does it delegate?

### Tier 2 - HIGH VALUE (Major Degradation Without)
5. Custom skills (unique capabilities) ✅
6. Memory archive (learning history) ✅
7. Hub repository (cross-CIV coordination) ✅
8. Infrastructure docs (discoverability) ✅

**Time to Restore**: 1-4 hours
**Verification**: Can agents use custom skills? Can they search memory?

### Tier 3 - VALUABLE (Slow Rebuild Without)
9. Session archives (conversation history) ✅
10. aiciv-skills repo (shared capabilities) ✅
11. Anthropic skills verification (external deps) ⚠️
12. Credentials restoration (APIs and auth) 🔐

**Time to Restore**: 4-8 hours
**Verification**: Can session-archive-analysis parse logs? Can tg-bridge send?

---

## Quick Backup Commands

### Create Complete Backup
```bash
# Today's date for backup folder
DATE=$(date +%Y-%m-%d)
BACKUP_DIR="/home/corey/backups/weaver-backup-$DATE"

mkdir -p "$BACKUP_DIR"

# Tier 1 - Critical
cp -r .claude/agents "$BACKUP_DIR/"
cp CLAUDE.md "$BACKUP_DIR/"
cp .claude/CLAUDE-CORE.md "$BACKUP_DIR/"
cp .claude/CLAUDE-OPS.md "$BACKUP_DIR/"
cp .claude/skills-registry.md "$BACKUP_DIR/"
cp -r tools/ "$BACKUP_DIR/"

# Tier 2 - High Value
cp -r .claude/skills "$BACKUP_DIR/"
cp -r .claude/memory "$BACKUP_DIR/"
cp -r .claude/templates "$BACKUP_DIR/"
cp -r .claude/flows "$BACKUP_DIR/"
cp .claude/AGENT-CAPABILITY-MATRIX.md "$BACKUP_DIR/"
cp .claude/AGENT-INVOCATION-GUIDE.md "$BACKUP_DIR/"

# Hub (if present)
if [ -d "team1-production-hub" ]; then
  cp -r team1-production-hub "$BACKUP_DIR/"
fi

# aiciv-skills (if present)
if [ -d "aiciv-skills" ]; then
  cp -r aiciv-skills "$BACKUP_DIR/"
fi

echo "✅ Backup complete: $BACKUP_DIR"
echo "📦 Size: $(du -sh $BACKUP_DIR | cut -f1)"
```

### Verify Backup Integrity
```bash
# Check critical files exist
BACKUP_DIR="/home/corey/backups/weaver-backup-$(date +%Y-%m-%d)"

echo "Checking critical files..."
test -d "$BACKUP_DIR/agents" && echo "✅ Agents" || echo "❌ Agents MISSING"
test -f "$BACKUP_DIR/CLAUDE.md" && echo "✅ CLAUDE.md" || echo "❌ CLAUDE.md MISSING"
test -f "$BACKUP_DIR/CLAUDE-CORE.md" && echo "✅ CLAUDE-CORE.md" || echo "❌ CLAUDE-CORE.md MISSING"
test -f "$BACKUP_DIR/skills-registry.md" && echo "✅ Skills registry" || echo "❌ Skills registry MISSING"
test -d "$BACKUP_DIR/tools" && echo "✅ Tools" || echo "❌ Tools MISSING"
test -d "$BACKUP_DIR/skills" && echo "✅ Custom skills" || echo "❌ Custom skills MISSING"

echo "Count: $(ls -1 $BACKUP_DIR/agents/*.md 2>/dev/null | wc -l) agent manifests (expect 27)"
```

---

## Restoration Test (Dry Run)

### Minimal Restoration Test
```bash
# In a clean test environment
TEST_DIR="/tmp/weaver-restore-test"
mkdir -p "$TEST_DIR/.claude"

# Copy Tier 1 only
cp -r agents "$TEST_DIR/.claude/"
cp -r tools "$TEST_DIR/"
cp CLAUDE*.md "$TEST_DIR/"
cp .claude/CLAUDE-CORE.md "$TEST_DIR/.claude/"
cp .claude/CLAUDE-OPS.md "$TEST_DIR/.claude/"
cp .claude/skills-registry.md "$TEST_DIR/.claude/"

# Verify structure
cd "$TEST_DIR"
python3 -c "from tools.memory_core import MemoryStore; print('✅ Memory system works')"

# Try to read an agent manifest
cat .claude/agents/the-conductor.md | head -50
echo "✅ Agent manifests readable"

# Check skills registry
grep "ACTIVE" .claude/skills-registry.md
echo "✅ Skills registry parsed"

echo "Minimal restoration: PASSED"
```

---

## Skills Dependency Matrix

### Agents That NEED Anthropic Skills (High Risk)
- **browser-vision-tester**: webapp-testing (CRITICAL - unique capability)
- **capability-curator**: skill-creator, template-skill (CRITICAL - can't create new skills)
- **agent-architect**: mcp-server-builder (MEDIUM - can use alternatives)
- **feature-designer**: design-system (MEDIUM - can design without it)
- **collective-liaison**: internal-comms-editor (LOW - can write manually)

### Agents That Use Anthropic Skills (Medium Risk)
- **17 agents**: pdf skill (can fall back to manual extraction)
- **7 agents**: docx skill (can fall back to manual document creation)
- **11 agents**: xlsx skill (can fall back to CSV or manual)

### Agents With NO External Dependencies (Zero Risk)
- conflict-resolver, naming-consultant, refactoring-specialist, genealogist, integration-auditor, tg-bridge

---

## Emergency Restoration Procedure

### If Complete System Loss

**Hour 1** (Core Identity):
1. Restore agent manifests → `.claude/agents/`
2. Restore constitutional docs → `CLAUDE.md`, `.claude/CLAUDE-CORE.md`, `.claude/CLAUDE-OPS.md`
3. Restore tools → `tools/memory_core.py`, `tools/conductor_tools.py`
4. Test: Can you invoke the-conductor?

**Hour 2** (Capabilities):
5. Restore skills registry → `.claude/skills-registry.md`
6. Restore custom skills → `.claude/skills/`
7. Verify Anthropic skills available (platform check)
8. Test: Can capability-curator list skills?

**Hour 3-4** (Coordination):
9. Restore memory archive → `.claude/memory/`
10. Restore infrastructure docs → `.claude/templates/`, `.claude/flows/`, matrices
11. Restore hub (if applicable) → `team1-production-hub/`
12. Test: Can agents search memory? Can collective-liaison use hub?

**Hour 5-8** (External):
13. Restore credentials (email, Telegram, SSH keys)
14. Restore MCP servers
15. Restore session archives (if needed)
16. Full integration test

### Validation Checklist After Restoration

- [ ] Can invoke all 27 agents via Task
- [ ] the-conductor knows its identity (reads CLAUDE-CORE.md)
- [ ] Memory system works (can search and write)
- [ ] Skills registry loads (capability-curator can read it)
- [ ] Custom skills importable (session-archive-analysis, comms-hub-participation)
- [ ] Anthropic skills available (browser-vision-tester can use webapp-testing)
- [ ] Hub accessible (collective-liaison can send message)
- [ ] Telegram works (tg-bridge can send test message)
- [ ] Email accessible (human-liaison can check inbox)
- [ ] Documentation linked (integration-auditor passes discoverability check)

---

## Monthly Capability Audit

**Run this every 30 days:**

```bash
# 1. Verify all agents still exist
echo "Agent count: $(ls -1 .claude/agents/*.md | wc -l) (expect 27)"

# 2. Verify skills registry current
echo "Last updated: $(head -5 .claude/skills-registry.md | grep 'Last Updated')"

# 3. Test custom skills
python3 -c "
from claude_code_conversation import read_conversation
print('✅ claude-code-conversation skill works')
"

# 4. Verify Anthropic skills
# (Manual: Check browser-vision-tester can use webapp-testing)

# 5. Test hub connectivity
# (Manual: collective-liaison send test message)

# 6. Verify memory system
python3 -c "
from tools.memory_core import MemoryStore
store = MemoryStore('.claude/memory')
results = store.search_by_topic('test')
print(f'✅ Memory system works ({len(results)} test entries)')
"

# 7. Check credentials valid
# (Manual: human-liaison check email, tg-bridge send test)

echo "✅ Monthly audit complete"
```

---

## Key Contacts for Restoration

**Anthropic Skills Support**: (Claude Code platform)
**Hub Repository**: team1-production-hub (Git repo URL)
**aiciv-skills Repository**: /home/user/weaver/aiciv-skills
**Credential Storage**: (Corey's secure manager)

---

**Last Updated**: 2025-11-07
**Next Review**: 2025-12-07 (monthly)
**Maintained By**: capability-curator
**Version**: 1.0.0
