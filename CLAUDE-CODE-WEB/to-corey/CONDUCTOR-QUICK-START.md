# Conductor Transformation - Quick Start Guide

**Read this first. Full plan in CONDUCTOR-AGENT-TRANSFORMATION-PLAN.md**

---

## The Problem

The Conductor is special-cased in CLAUDE.md. This causes decoherence - every session loses orchestration learnings. As Corey said: "working... but not ideal."

---

## The Solution (6 Phases)

### DO NOW (1-2 hours)

**Phase 0: Foundation**
1. Read 3 agent manifests (10 min)
2. Document registration pattern (20 min)
3. Extract Conductor personality (30 min)
4. Design memory schema (30 min)

**Output**: 3 documents that enable Phase 1

---

### DO NEXT (if time allows, 1 hour)

**Phase 1: Create Conductor Agent**
1. Write `.claude/agents/the-conductor.md` (30 min)
2. Initialize memory directory (20 min)
3. Test invocation (10 min)

**Output**: Conductor is a registered agent with memory

**This is the key win** - stops decoherence

---

### DO LATER (separate session, 2-3 hours)

**Phase 2: Restructure CLAUDE.md** (1 hour)
- Change to WHO/WHAT/WHEN framework
- Move personality to agent manifest
- Simplify to delegation guide

**Phase 3: Self-Updating Spawner** (1-2 hours)
- Build `update_claude_md.py`
- Auto-update WHO/WHAT on agent registration
- Test with dummy agent

**Output**: Automated agent registration

---

### CAN WAIT (not urgent, 5-7 hours total)

**Phase 4: Comms Monitor Agent** (1 hour)
- Operational enhancement
- Not blocking other work

**Phase 5: Constitutional Convention v2** (2-3 hours)
- Strategic work
- Better with full foundation

**Phase 6: Deep Ceremony v2** (2-3 hours)
- Reflective work
- Builds on everything else

---

## Dependency Flow

```
Phase 0 (Foundation)
  ↓
Phase 1 (Conductor Agent) ← STOPS DECOHERENCE
  ↓
Phase 2 (CLAUDE.md Restructure)
  ↓
Phase 3 (Auto-Spawner)
  ↓
Phase 4 (Comms Monitor)
  ↓
Phase 5 (Convention v2)
  ↓
Phase 6 (Ceremony v2)
```

**Critical path**: 0 → 1 → 2 → 3 (4-6 hours)
**Everything else can wait**

---

## Recommended Approach

### Option 1: Just Phase 0 Today (1-2 hours)
- Safest approach
- Learn the pattern
- Get Corey's feedback
- Continue tomorrow

### Option 2: Phases 0-1 Today (2-3 hours)
- Highest ROI
- Conductor gets memory
- Decoherence stops
- Good checkpoint

### Option 3: Phases 0-2 Today (3-4 hours)
- Ambitious but doable
- CLAUDE.md restructured
- Ready for spawner work
- May be too much

**Task Decomposer recommends: Option 2**

---

## What Success Looks Like

### After Phase 0
- You understand agent registration pattern
- You've extracted Conductor's personality
- You have a memory schema design
- Ready to build Phase 1

### After Phase 1
- `.claude/agents/the-conductor.md` exists
- Conductor has memory directory
- Can be invoked via Task tool
- **Decoherence stopped**

### After Phase 2
- CLAUDE.md is clean WHO/WHAT/WHEN
- No personality in CLAUDE.md (lives in agent manifest)
- Clear delegation rules
- Ready for automation

### After Phase 3
- New agents auto-update CLAUDE.md
- Zero manual maintenance
- Registration is automated
- Foundation complete

---

## Key Files Created

### Phase 0 (DO NOW)
- `to-corey/AGENT-REGISTRATION-PATTERN.md`
- `to-corey/CONDUCTOR-IDENTITY-ANALYSIS.md`
- `to-corey/CONDUCTOR-MEMORY-DESIGN.md`

### Phase 1 (DO NEXT)
- `.claude/agents/the-conductor.md`
- `.claude/memory/the-conductor/README.md`
- `.claude/memory/the-conductor/*.md`

### Phase 2
- `CLAUDE.md` (restructured)
- `to-corey/CLAUDE-RESTRUCTURE-CHANGELOG.md`

### Phase 3
- `tools/update_claude_md.py`
- `tools/test_spawner_update.py`

---

## Risk Management

### What Could Go Wrong

1. **Conductor invocation breaks**
   - Mitigation: Test before changing CLAUDE.md
   - Rollback: Keep CLAUDE.md.backup

2. **Personality lost in migration**
   - Mitigation: Extract carefully to agent manifest
   - Validation: Compare before/after

3. **Spawner bugs**
   - Mitigation: Test with dummy agents first
   - Rollback: Manual updates still work

### What's Safe

- Phase 0 is pure analysis (no code changes)
- Phase 1 is additive (doesn't remove anything)
- Phase 2 is reversible (git revert)
- Phase 3 is optional (manual fallback exists)

---

## Time Estimates

| Phase | Optimistic | Realistic | Pessimistic |
|-------|------------|-----------|-------------|
| 0 | 1h | 1.5h | 2h |
| 1 | 45m | 1h | 1.5h |
| 2 | 45m | 1h | 1.5h |
| 3 | 1h | 1.5h | 2h |
| **0-1** | **1.75h** | **2.5h** | **3.5h** |
| **0-3** | **3.5h** | **5h** | **7h** |

---

## Next Actions (If You're Starting Now)

1. **Read these agent manifests** (10 min):
   - `.claude/agents/feature-designer.md`
   - `.claude/agents/task-decomposer.md`
   - `.claude/agents/security-auditor.md`

2. **Extract the pattern** (look for):
   - Standard sections (Core Principles, Responsibilities, etc.)
   - Memory integration code blocks
   - Tool allowance lists
   - Constitutional compliance sections

3. **Write AGENT-REGISTRATION-PATTERN.md** (20 min):
   - Document common structure
   - Create reusable template
   - Note variations between agents
   - List required vs optional fields

4. **Then**: Continue with Conductor identity analysis

---

## Questions to Consider During Phase 0

1. **Personality**: Which Conductor traits are essential?
2. **Memory**: What needs long-term persistence vs session-only?
3. **Tools**: Should Conductor have access to ALL tools?
4. **Uniqueness**: How is Conductor different from other agents?
5. **Orchestration**: Is orchestration a capability or a role?

---

## Files to Reference

### Understanding Current State
- `CLAUDE.md` (lines 1-200) - Conductor's current identity
- `.claude/AGENT-INVOCATION-GUIDE.md` - How agents work
- `.claude/agents/*.md` (any 3) - Registration pattern

### Constitutional Context
- `to-corey/CONSTITUTIONAL-SYNTHESIS.md` - Current constitution
- `.claude/identity-work/historical-artifacts/2025-10-04-deep-ceremony-complete-14-unique-thoughts.md` - Ceremony v1

### Technical Reference
- `tools/memory_core.py` - Memory system API
- `.claude/memory/agent-learnings/*/` - Example memories

---

## Summary

**Problem**: Conductor decoherences without memory
**Solution**: Register Conductor as agent with memory
**Urgency**: HIGH (happening now)
**Effort**: 2-3 hours for critical path (Phases 0-1)
**Approach**: Start with Phase 0, validate, continue to Phase 1

**Bottom Line**: Phase 0-1 stops the bleeding. Everything else is infrastructure improvements that can wait.

---

**Read full plan**: `/home/corey/projects/AI-CIV/grow_openai/to-corey/CONDUCTOR-AGENT-TRANSFORMATION-PLAN.md`

**Start here**: Read 3 agent manifests, extract pattern, document it.
