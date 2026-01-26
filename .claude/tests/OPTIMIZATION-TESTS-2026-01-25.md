# Optimization Evaluation Tests

**Created**: 2026-01-25
**Backup point**: `c7f3f51` (tag: backup-pre-optimization-2026-01-25)
**Purpose**: Validate the 5 optimization actions

---

## Test 1: WAKE-UP-ESSENTIAL Token Savings

### Hypothesis
Essential wake-up uses ~16K tokens vs ~77K for full wake-up (79% reduction)

### Test Procedure

1. **Baseline (Full Wake-Up)**:
   ```bash
   # In new session, run full wake-up per CLAUDE-OPS.md
   # Record: total tokens used before first user task
   ```

2. **Treatment (Essential Wake-Up)**:
   ```bash
   # In new session, run essential wake-up per WAKE-UP-ESSENTIAL.md
   # Record: total tokens used before first user task
   ```

3. **Measurement**:
   - Count files read during each protocol
   - Estimate tokens: (total bytes read) / 4

### Success Criteria
- Essential wake-up < 25K tokens
- Full wake-up > 60K tokens
- Savings > 50%

### Risks
- Essential may miss critical context
- Lazy loading may cause mid-task delays

---

## Test 2: BASE-AGENT-PROTOCOLS Adoption

### Hypothesis
Agent manifests referencing shared protocols are smaller without losing functionality

### Test Procedure

1. **Baseline**: Measure current agent manifest sizes
   ```bash
   wc -c .claude/agents/*.md | sort -n
   ```

2. **Treatment**: Refactor 3 agent manifests to use BASE-AGENT-PROTOCOLS.md
   - security-auditor.md (high usage)
   - web-researcher.md (high usage)
   - pattern-detector.md (high usage)

3. **Measure**:
   - Size before/after for each agent
   - Functionality test: invoke each agent, verify normal operation

### Success Criteria
- Each manifest reduced by >50%
- No functionality regression
- Agents still follow memory-first protocol

---

## Test 3: 71% Claim Validation Study

### Hypothesis
Memory search provides time savings, but actual rate unknown

### Test Procedure

1. **Design experiment**:
   - Task type: "Find and fix security vulnerability"
   - Condition A: No memory search
   - Condition B: Memory search before work
   - Sample size: 5 tasks each condition

2. **Measure**:
   - Time to completion
   - Quality of output
   - Steps taken

3. **Analyze**:
   - Calculate actual savings percentage
   - Compare to 71% claim

### Success Criteria
- Proper statistical methodology
- Documented baseline and treatment
- Confidence interval on savings estimate

---

## Test 4: Bluesky Skills Consolidation

### Hypothesis
bsky-core + bsky-engagement provide same capability as 7 original skills

### Test Procedure

1. **Functionality Matrix**:

   | Capability | Old Skill | New Skill | Works? |
   |------------|-----------|-----------|--------|
   | Single post | bluesky-mastery | bsky-core | ? |
   | Thread | bluesky-blog-thread | bsky-core | ? |
   | Facets | bluesky-social-mastery | bsky-core | ? |
   | Notifications | bsky-boop-manager | bsky-engagement | ? |
   | Reply | bsky-engage | bsky-engagement | ? |
   | BOOP cycle | boop-bluesky-post | bsky-engagement | ? |

2. **Test each capability**:
   - Invoke bsky-manager agent with consolidated skills
   - Attempt each operation
   - Record success/failure

3. **Token measurement**:
   ```bash
   # Before: sum of 7 skill sizes
   # After: sum of 3 skill sizes
   ```

### Success Criteria
- All 6 capabilities work with new skills
- Token reduction > 50%
- No new errors in Bluesky operations

---

## Test 5: data-analyst Agent Proposal

### Hypothesis
data-analyst agent can validate claims that currently go untested

### Test Procedure

1. **If approved, create agent and run first mission**:
   - Mission: "Validate memory system time savings"
   - Provide access to session logs
   - Request proper statistical analysis

2. **Evaluate output**:
   - Does it include methodology?
   - Does it include sample size?
   - Does it include confidence interval?
   - Is the conclusion evidence-based?

### Success Criteria
- Agent produces quantified findings
- Methodology is reproducible
- Findings differ from "71% proven" assertion (demonstrating rigor)

---

## How to Run Tests

### Quick Smoke Test (5 min)

```bash
# Verify new files exist
ls -la .claude/WAKE-UP-ESSENTIAL.md
ls -la .claude/templates/BASE-AGENT-PROTOCOLS.md
ls -la .claude/skills/bsky-core/SKILL.md
ls -la .claude/skills/bsky-engagement/SKILL.md
ls -la .claude/agents/proposals/data-analyst-proposal.md
ls -la .claude/memory/validations/71-percent-savings-claim-status.md

# Verify consolidation doc
cat .claude/skills/BSKY-CONSOLIDATION-2026-01-25.md
```

### Token Measurement Test (15 min)

```bash
# Measure essential wake-up files
wc -c CLAUDE.md .claude/WAKE-UP-ESSENTIAL.md

# Measure infrastructure files (now deferred)
wc -c .claude/templates/ACTIVATION-TRIGGERS.md \
     .claude/templates/AGENT-OUTPUT-TEMPLATES.md \
     .claude/flows/FLOW-LIBRARY-INDEX.md \
     .claude/AGENT-CAPABILITY-MATRIX.md \
     .claude/skills-registry.md

# Calculate savings potential
```

### Functional Test (30 min)

1. Start fresh session
2. Use WAKE-UP-ESSENTIAL.md
3. Invoke bsky-manager with consolidated skills
4. Attempt: post, thread, notification check
5. Record any failures

---

## Rollback Procedure

If tests fail:

```bash
git checkout backup-pre-optimization-2026-01-25
# Or:
git checkout c7f3f51
```

---

## Test Results Log

| Test | Date | Result | Notes |
|------|------|--------|-------|
| 1. Essential wake-up | | | |
| 2. Agent protocols | | | |
| 3. 71% validation | | | |
| 4. Bsky consolidation | | | |
| 5. data-analyst | | | |

---

**Next step**: Run quick smoke test to verify files created correctly.
