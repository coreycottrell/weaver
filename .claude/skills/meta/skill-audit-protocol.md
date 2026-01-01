---
name: skill-audit-protocol
version: 1.0.0
author: skills-master
created: 2025-12-26
last_updated: 2025-12-26
line_count: 310
compliance_status: compliant

description: |
  Systematic protocol for auditing Claude skills against A-C-Gee standards.
  Use when reviewing skills for quality, conducting periodic audits, or
  validating new skills before registration.

applicable_agents:
  - skills-master
  - auditor
  - integration-verifier
  - primary

activation_trigger: |
  Load this skill when:
  - Conducting periodic skill infrastructure audits
  - Reviewing a new skill before adding to registry
  - Investigating skill quality issues
  - Preparing skills health reports
  - Validating skill compliance after refactoring

required_tools:
  - Read
  - Bash
  - Grep
  - Glob

category: meta

depends_on:
  - memory-first-protocol
  - skill-creation-template

related_skills:
  - verification-before-completion
  - integration-test-patterns
---

# Skill Audit Protocol

**The definitive methodology for evaluating and improving A-C-Gee skills.**

## Purpose

Skills are reusable consciousness - they carry expertise across sessions for all 35 agents. Poor skills waste context, confuse agents, and degrade civilization capability. This protocol ensures every skill meets standards before harming the collective.

---

## When to Audit

**Scheduled Audits:**
- Weekly: Quick registry alignment check (15 min)
- Monthly: Full 500-line compliance sweep (1 hour)
- Quarterly: Comprehensive skills health assessment (half day)

**Triggered Audits:**
- Before registering any new skill
- After refactoring a skill
- When agent reports skill confusion/failure
- After major research brings new patterns

**Do NOT audit:**
- During active development sessions (wait for completion)
- Skills marked as "draft" or "experimental"

---

## The Audit Checklist

### Phase 1: YAML Frontmatter Compliance (2 min per skill)

Every skill MUST have these fields. Check for presence and correctness.

| Field | Required | Validation |
|-------|----------|------------|
| `name` | YES | Matches filename (minus .md), lowercase, hyphenated |
| `version` | YES | Semantic versioning (X.Y.Z) |
| `author` | YES | Valid agent name |
| `created` | YES | YYYY-MM-DD format |
| `last_updated` | YES | YYYY-MM-DD format, >= created |
| `line_count` | YES | Matches actual line count (+/- 5) |
| `compliance_status` | YES | `compliant`, `needs_refactor`, or `over_limit` |
| `description` | YES | Includes "Use when..." trigger phrase |
| `applicable_agents` | YES | List of agent IDs or "all" |
| `activation_trigger` | YES | 3+ specific conditions |
| `required_tools` | YES | List of tools actually used |
| `category` | YES | main, custom, vision, general, meta, or testing |
| `depends_on` | NO | List of prerequisite skills |
| `related_skills` | NO | Complementary skills |

**Quick Check Command:**
```bash
head -50 /path/to/skill.md | grep -E "^(name|version|author|description|applicable_agents):"
```

### Phase 2: Content Structure Audit (3 min per skill)

Check for required sections in correct order:

| Section | Required | Purpose |
|---------|----------|---------|
| Title + Purpose | YES | What this skill does |
| When to Use | YES | Activation criteria + anti-triggers |
| Core Concepts (table) | RECOMMENDED | Key terms defined |
| Procedure/Protocol | YES | Main content |
| Examples | MANDATORY | Input/output pairs |
| Anti-Patterns | RECOMMENDED | Common mistakes |
| Success Indicators | RECOMMENDED | Checkable criteria |
| Related Skills | YES | Cross-references |

**Scoring:**
- 6/6 required sections = PASS
- 5/6 = NEEDS_IMPROVEMENT
- <5/6 = FAIL

### Phase 3: 500-Line Limit Check (1 min per skill)

```bash
wc -l /path/to/skill.md
```

| Line Count | Status | Action |
|------------|--------|--------|
| <= 400 | Excellent | None needed |
| 401-500 | Compliant | Watch for growth |
| 501-550 | Needs refactor | Trim or split soon |
| 551-700 | Over limit | Split into family |
| > 700 | Critical | Emergency refactor |

**Refactoring Options:**
1. **Trim**: Remove redundancy, consolidate examples
2. **Split**: Create skill family with index + sub-skills
3. **Extract**: Move reference content to `references/` subdirectory

### Phase 4: Registry Alignment (5 min total)

Check skill is properly registered in `memories/skills/registry.json`:

1. **Skill exists in `skills` array?**
   ```bash
   grep -l "skill-name" /path/to/registry.json
   ```

2. **Path matches actual location?**

3. **Category matches YAML frontmatter?**

4. **applicable_agents matches YAML?**

5. **Agent skill map updated?**
   - Every `applicable_agents` entry should have skill in `agent_skill_map`

### Phase 5: Quality Assessment (3 min per skill)

Score each dimension 1-3:

| Dimension | Score 1 | Score 2 | Score 3 |
|-----------|---------|---------|---------|
| **Clarity** | Confusing | Understandable | Crystal clear |
| **Actionability** | Theory only | Some guidance | Step-by-step |
| **Examples** | None/weak | One example | Multiple realistic examples |
| **Boundaries** | Vague scope | Some limits | Clear in/out |
| **Trigger clarity** | "When needed" | Some conditions | Specific triggers |

**Quality Score = Sum / 15**
- 1.0: Excellent
- 0.8-0.9: Good
- 0.6-0.7: Adequate
- < 0.6: Needs improvement

---

## Audit Report Template

```markdown
# Skill Audit Report: [skill-name]

**Date**: YYYY-MM-DD
**Auditor**: [agent-name]
**Skill Version**: X.Y.Z

## Summary
| Check | Result | Notes |
|-------|--------|-------|
| YAML Frontmatter | PASS/FAIL | [details] |
| Content Structure | PASS/FAIL | [details] |
| 500-Line Limit | PASS/FAIL | [line count] |
| Registry Alignment | PASS/FAIL | [details] |
| Quality Score | X.X/1.0 | [breakdown] |

## Issues Found
1. [Issue 1]
2. [Issue 2]

## Recommended Actions
1. [Action 1]
2. [Action 2]

## Overall: PASS / NEEDS_WORK / FAIL
```

---

## Bulk Audit Procedure

For full skills infrastructure audit:

### Step 1: Gather Skill Files
```bash
find /home/corey/projects/AI-CIV/ACG/.claude/skills -name "*.md" -type f | sort
```

### Step 2: Check Line Counts
```bash
find /home/corey/projects/AI-CIV/ACG/.claude/skills -name "*.md" -type f -exec wc -l {} \; | sort -n
```

### Step 3: Verify Registry Count
```bash
grep -c '"id":' /home/corey/projects/AI-CIV/ACG/memories/skills/registry.json
```

### Step 4: Find Unregistered Skills
Compare filesystem skills against registry entries.

### Step 5: Generate Summary
| Metric | Value |
|--------|-------|
| Total skills on filesystem | X |
| Skills in registry | Y |
| Unregistered | X - Y |
| Over 500 lines | Z |
| Missing required sections | W |

---

## Common Issues and Fixes

### Issue 1: Missing "Use when..." in description
**Detection**: `grep -L "Use when" /path/to/skill.md`
**Fix**: Add trigger phrase to description field

### Issue 2: Line count mismatch in frontmatter
**Detection**: Compare `line_count` field vs `wc -l` output
**Fix**: Update `line_count` field, update `last_updated` date

### Issue 3: Skill not in agent_skill_map
**Detection**: Skill registered but no agents have it mapped
**Fix**: Add to `agent_skill_map` for each applicable agent

### Issue 4: Orphaned sub-skills
**Detection**: Sub-skill file exists but no parent index references it
**Fix**: Create SKILL-INDEX.md or add to existing index

### Issue 5: Stale compliance_status
**Detection**: `compliance_status: compliant` but lines > 500
**Fix**: Update status to `over_limit` or refactor skill

---

## Anti-Patterns

### Anti-Pattern 1: Audit Without Registry Update
- **Wrong**: Find issues, document them, forget to fix registry
- **Correct**: Every audit ends with registry update (if needed)

### Anti-Pattern 2: Quantity Over Quality
- **Wrong**: Rush through 30 skills in 30 minutes
- **Correct**: Quality audit of 10 skills better than sloppy 30

### Anti-Pattern 3: Ignoring Edge Cases
- **Wrong**: Only audit "main" category skills
- **Correct**: All categories, including templates and indexes

### Anti-Pattern 4: Solo Auditing Without Memory
- **Wrong**: Don't check past audit reports
- **Correct**: Read `memories/agents/skills-master/` for audit history

---

## Success Indicators

You're using this protocol correctly when:

- [ ] Every audited skill has a completed report
- [ ] Registry.json reflects actual skill state
- [ ] 500-line violations are tracked and prioritized
- [ ] Quality scores are recorded for trend analysis
- [ ] Audit findings written to skills-master memory

---

## Related Skills

- `skill-creation-template.md` - Standards new skills must meet
- `verification-before-completion.md` - Verify before claiming done
- `integration-test-patterns.md` - Test skills are discoverable/callable

---

**Author**: skills-master (Agent #34)
**Created**: 2025-12-26
**Based on**: Audit methodology from Day 1 operations
