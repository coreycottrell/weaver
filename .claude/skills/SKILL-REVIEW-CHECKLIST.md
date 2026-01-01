# WEAVER Skill Review Checklist

**Purpose**: Validate skills before sharing to hub or marking as production-ready.
**Owner**: capability-curator
**Created**: 2025-12-30

---

## Pre-Share Checklist

Before pushing any skill to the comms hub, verify:

### 1. Documentation Quality
- [ ] **SKILL.md exists** with proper frontmatter (name, description)
- [ ] **Purpose is clear** - one sentence explaining what it does
- [ ] **Owner assigned** - which agent maintains this skill
- [ ] **Status marked** - VALIDATED, VERIFIED, or UNTESTED with date
- [ ] **Quick reference** - copy-paste ready commands/code
- [ ] **Anti-patterns** - what NOT to do (lessons learned)

### 2. Functional Testing
- [ ] **Core function tested** - the main thing the skill does WORKS
- [ ] **Edge cases noted** - what breaks, what's fragile
- [ ] **Dependencies documented** - API keys, packages, external services
- [ ] **Error handling** - what happens when things fail

### 3. Integration Testing
- [ ] **End-to-end run** - complete workflow from start to finish
- [ ] **Real output produced** - not just "it ran", but "it delivered value"
- [ ] **Delivery confirmed** - if skill produces artifacts, they reached destination

### 4. Cross-CIV Readiness
- [ ] **No hardcoded WEAVER paths** - or clearly marked as WEAVER-specific
- [ ] **Portable instructions** - other CIVs can adapt
- [ ] **Dependencies available** - not relying on WEAVER-only infrastructure

---

## Testing Status Markers

Use these in SKILL.md:

```markdown
**Status**: ✅ VALIDATED 2025-12-30 (full pipeline tested)
**Status**: ✅ VERIFIED 2025-12-30 (core functions work)
**Status**: ⚠️ PARTIAL 2025-12-30 (X works, Y untested)
**Status**: ❌ UNTESTED (documentation only)
```

---

## Current WEAVER Skills Audit

### Ready for Hub (VALIDATED)
| Skill | Last Tested | Notes |
|-------|-------------|-------|
| linkedin-content-pipeline | 2025-12-30 | Full FA test ✅ |
| image-generation | 2025-12-30 | Blog headers work ✅ |
| bluesky-mastery | 2025-12-30 | 7/9 functions verified ✅ |
| comms-hub-operations | 2025-12-27 | Production use ✅ |

### Needs Testing
| Skill | Issue | Priority |
|-------|-------|----------|
| bluesky-social-mastery | Follow function untested | Medium |
| parallel-research | Not tested with haiku model | Low |
| night-watch-flow | Night mode removed, retest needed | Low |

### Documentation Only (No Testing Yet)
| Skill | Created | Notes |
|-------|---------|-------|
| dream-forge | 2025-12-27 | Ceremonial, hard to test |
| mirror-storm | 2025-12-27 | Meta-cognitive, needs structure |
| paradox-game | 2025-12-27 | Experimental |

---

## Testing Protocol

### Quick Test (5 min)
```bash
# 1. Read the skill
cat .claude/skills/[skill-name]/SKILL.md

# 2. Try the quick reference command
[copy-paste from skill]

# 3. Verify output exists
ls -la [expected output path]
```

### Full Test (15-30 min)
1. Read skill completely
2. Execute each documented function
3. Verify each produces expected output
4. Test one failure case
5. Update SKILL.md with findings

### Pipeline Test (30-60 min)
For workflow skills (like linkedin-content-pipeline):
1. Run complete pipeline start to finish
2. Verify all outputs created
3. Verify all deliveries completed
4. Document timing and any issues
5. Update skill with lessons learned

---

## Review Triggers

**Mandatory review before**:
- Pushing to comms hub
- Recommending to sister CIV
- Adding to agent manifest

**Periodic review**:
- Monthly for production skills
- After any API/dependency changes
- After significant codebase changes

---

## Skill Quality Tiers

### Tier 1: Production Ready
- Full testing complete
- Used successfully in production
- Safe to share with sister CIVs
- Examples: comms-hub-operations, image-generation

### Tier 2: Working but Limited
- Core function tested
- Some edge cases unknown
- Share with caveats
- Examples: bluesky-mastery (follows untested)

### Tier 3: Experimental
- Concept documented
- Minimal testing
- Internal use only
- Examples: dream-forge, paradox-game

---

## Post-Share Monitoring

After sharing skill to hub:
- [ ] Check if sister CIVs use it (hub messages)
- [ ] Collect feedback
- [ ] Update based on cross-CIV learnings
- [ ] Version if significant changes

---

*This checklist is itself a skill that should be reviewed periodically.*
