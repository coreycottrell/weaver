# Contradiction Quick Fix Guide

**Priority**: P0 - Fix Today
**Time Estimate**: 30-45 minutes
**Impact**: Unblocks Team 2 integration, clarifies system status

---

## 5 Critical Fixes (Do in Order)

### Fix 1: Agent Location (5 min)
**File**: `.claude/AGENT-INVOCATION-GUIDE.md`

**Find and Replace**:
```
OLD: .claude/agents/[agent-name].md
NEW: agents/[agent-name].md
```

**Lines to Update**: 24, 68

**Verification**:
```bash
ls agents/*.md | wc -l  # Should show 14 or 16
ls .claude/agents/*.md 2>/dev/null  # Should be empty or error
```

---

### Fix 2: Agent Count (10 min)
**Task**: Count actual agent files and update all references

**Command**:
```bash
cd /home/corey/projects/AI-CIV/grow_openai
ls -1 agents/*.md | wc -l
ls -1 agents/*.md
```

**Expected Count**:
- Original 14 agents PLUS
- communications-coordinator
- system-librarian
= **16 total agents**

**Files to Update**:
1. `CLAUDE.md` - Change "14 agents" → "16 agents" (or keep 14, clarify 2 are new)
2. `docs/AGENT-OUTPUTS.md` line 340 - Verify "15 agents" claim
3. Search all "14 agents" references, update to accurate count

**Decision Required**: Are the 2 new agents "official" or "experimental"?

---

### Fix 3: Memory System Status (5 min)
**File**: `CLAUDE.md` line 267

**Current**:
```
IMPORTANT: Currently only 6/14 agents have memories. Full enablement pending.
```

**Replace With**:
```
MEMORY SYSTEM STATUS:
- Infrastructure: ✅ Production-ready (tools/memory_*.py complete)
- Agent Capability: ✅ All agents enabled (memory sections in manifests)
- Memory Content: ⏳ Partial (6/16 agents have written memories)
- Agents with memories: web-researcher, pattern-detector, code-archaeologist,
  doc-synthesizer, security-auditor, api-architect

Full memory population is ongoing work, not a blocker.
```

---

### Fix 4: Flow Count (10 min)
**Task**: Count canonical flows and update references

**Count Flows**:
```bash
cd /home/corey/projects/AI-CIV/grow_openai/.claude/flows
ls -1 *.md | grep -v README | grep -v brainstorm
```

**Expected**: 14-15 flow files

**Canonical 14 Flows** (verify this list):
1. morning-consolidation.md
2. contract-first-integration-needs-testing.md
3. cross-pollination-synthesis-needs-testing.md
4. knowledge-archaeology-needs-testing.md
5. dialectic-forge-needs-testing.md
6. recursive-complexity-breakdown-needs-testing.md
7. semantic-harmonization-needs-testing.md
8. performance-cascade-analysis-needs-testing.md
9. user-story-to-implementation-needs-testing.md
10. test-driven-refactoring-gauntlet-needs-testing.md
11. fortress-protocol-needs-testing.md
12. architecture-xray-needs-testing.md
13. competitive-intelligence-deep-dive-needs-testing.md
14. democratic-mission-selection.md

**Validated Count**: 5 (not 3, not 6)
- morning-consolidation
- contract-first-integration
- knowledge-archaeology
- cross-pollination-synthesis
- democratic-mission-selection

**Update**: `.claude/flows/README.md` with accurate count and validation status

---

### Fix 5: ADR004 Status (10 min)
**Files**:
1. `MISSION-COMPLETE-ADR004.md`
2. `to-corey/ADR004-INTEGRATION-COMPLETE.md`
3. `INTEGRATION-ROADMAP.md`

**Clarification**:
```
ADR004 STATUS BREAKDOWN:

✅ COMPLETE:
- Ed25519 signing system (tools/sign_message.py)
- ADR004 wrapper library (tools/examples/adr004_integration_example.py)
- Integration documentation (QUICK-START-ADR004.md)
- Security analysis (SECURITY-THREAT-MODEL.md)

⏳ PENDING:
- A-C-Gee adoption (their action, not ours)
- Integration into our hub_cli.py (our TODO)

STATUS: "Integration-Ready" not "Integration-Complete"
```

**Actions**:
1. Rename `MISSION-COMPLETE-ADR004.md` → `ADR004-INTEGRATION-READY.md`
2. Add status clarification to top of both docs
3. Update INTEGRATION-ROADMAP.md to reflect correct scope

---

## Verification Checklist

After completing all 5 fixes:

```bash
# 1. Agent location correct?
grep -r "\.claude/agents/" *.md .claude/*.md 2>/dev/null
# Should only find this in archived/deprecated docs

# 2. Agent count consistent?
grep -r "14 agents\|15 agents\|16 agents" *.md | wc -l
# Review each mention for accuracy

# 3. Memory status clear?
grep -A5 "MEMORY SYSTEM" CLAUDE.md
# Should show updated status

# 4. Flow count accurate?
ls .claude/flows/*.md | grep -v README | wc -l
# Should match documented count

# 5. ADR004 status clear?
ls *ADR004* to-corey/*ADR004*
# Should show renamed files
```

---

## Impact Assessment

**Before Fixes**:
- Team 2 confused about agent location ❌
- Agent count claims vary (14/15/16?) ❌
- Memory system status unclear ❌
- Flow validation progress ambiguous ❌
- ADR004 appears "done" but isn't integrated ❌

**After Fixes**:
- Agent location canonical (agents/*.md) ✅
- Agent count accurate and explained ✅
- Memory system status transparent ✅
- Flow progress trackable ✅
- ADR004 handoff clear ✅

---

## Files Modified Summary

**Files to Edit** (5-8 total):
1. `.claude/AGENT-INVOCATION-GUIDE.md`
2. `CLAUDE.md`
3. `docs/AGENT-OUTPUTS.md`
4. `.claude/flows/README.md`
5. `MISSION-COMPLETE-ADR004.md` (rename)
6. `to-corey/ADR004-INTEGRATION-COMPLETE.md` (update)
7. `INTEGRATION-ROADMAP.md`
8. Any additional files with "14 agents" claims

**Time**: 30-45 minutes total

**Risk**: Low (documentation fixes, no code changes)

**Testing**: None required (doc-only changes)

---

## After P0 Fixes Complete

**Next Priority**: P1 fixes (11 contradictions)
- Add tool restrictions to agent manifests
- Remove external/ communication references
- Document production-ready levels
- Create style guide

**Estimate**: 2-3 hours for all P1 fixes

---

## Quick Commands

**Search for contradictions**:
```bash
# Find agent count references
grep -rn "14 agents\|15 agents\|16 agents" *.md

# Find .claude/agents references
grep -rn "\.claude/agents" *.md

# Find memory status claims
grep -rn "memory.*complete\|memory.*pending" *.md -i

# Find flow counts
grep -rn "14 flows\|flow.*validated" *.md -i

# Find ADR004 status claims
grep -rn "ADR.*complete\|ADR.*ready" *.md -i
```

---

**Ready to execute? Start with Fix 1 and work through sequentially.**

Each fix builds on previous fixes (e.g., agent count affects flow docs).

**Estimated completion**: 30-45 minutes for all P0 fixes.
