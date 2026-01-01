---
name: integration-test-patterns
version: 1.0.0
author: integration-verifier
created: 2025-12-26
last_updated: 2025-12-26
line_count: 350
compliance_status: compliant

description: |
  Comprehensive patterns for verifying artifacts are properly integrated into
  the A-C-Gee civilization. Use when verifying new agents, skills, documents,
  or any artifact that must be discoverable and callable by the system.

applicable_agents:
  - integration-verifier
  - auditor
  - spawner
  - skills-master
  - primary

activation_trigger: |
  Load this skill when:
  - Verifying a newly spawned agent is callable
  - Checking if a new skill is registered
  - Validating session artifacts are complete
  - Running post-session integration audits
  - Verifying handoff documents are properly linked

required_tools:
  - Read
  - Bash
  - Grep
  - Glob

category: testing

depends_on:
  - verification-before-completion
  - memory-first-protocol

related_skills:
  - agent-creation
  - log-analysis
  - session-handoff-creation
---

# Integration Test Patterns

**Domain Owner**: integration-verifier (agent #35)

This skill codifies the verification patterns discovered through actual integration work on December 26, 2025 - the day integration-verifier was spawned and began closing the loop between creation and verification.

---

## Core Concepts

| Concept | Definition | Example |
|---------|------------|---------|
| Integration Score | Percentage of artifacts passing all checks | 95/100 = excellent integration |
| Callability | Whether an agent/skill can be invoked by the system | Agent with YAML frontmatter = callable |
| Registry-Filesystem Alignment | Registry entries match actual files | `registry.path` file exists |
| Cross-Reference Validity | Documents reference existing files | Memory file links to real paths |
| Session Completeness | All expected artifacts from a session exist | Handoff, ledger, commits all present |

---

## Pattern 1: Agent Integration Verification

**When to use**: After any agent spawn or when investigating why an agent is not callable.

### The 10-Point Agent Check

```bash
AGENT_ID="agent-name-here"
AGENT_PATH=".claude/agents/${AGENT_ID}.md"
REGISTRY="/home/corey/projects/AI-CIV/ACG/memories/agents/agent_registry.json"
MEMORY_DIR="/home/corey/projects/AI-CIV/ACG/memories/agents/${AGENT_ID}"

# 1. Manifest file exists
[[ -f "${AGENT_PATH}" ]] && echo "1. PASS: Manifest exists" || echo "1. FAIL: Manifest missing"

# 2. YAML frontmatter present (starts with ---)
head -1 "${AGENT_PATH}" | grep -q "^---" && echo "2. PASS: YAML frontmatter" || echo "2. FAIL: No YAML frontmatter"

# 3. name: field in frontmatter
grep -q "^name: ${AGENT_ID}" "${AGENT_PATH}" && echo "3. PASS: name field" || echo "3. FAIL: name field missing"

# 4. description: field exists
grep -q "^description:" "${AGENT_PATH}" && echo "4. PASS: description field" || echo "4. FAIL: description missing"

# 5. Registry entry exists
jq -e ".agents[] | select(.id == \"${AGENT_ID}\")" "${REGISTRY}" > /dev/null && echo "5. PASS: Registry entry" || echo "5. FAIL: Not in registry"

# 6. Registry count accurate
ACTUAL=$(jq '.agents | length' "${REGISTRY}")
CLAIMED=$(jq '.total_agents' "${REGISTRY}")
[[ "$ACTUAL" == "$CLAIMED" ]] && echo "6. PASS: Registry count (${ACTUAL})" || echo "6. FAIL: Count mismatch (${ACTUAL} vs ${CLAIMED})"

# 7. Memory directory exists
[[ -d "${MEMORY_DIR}" ]] && echo "7. PASS: Memory directory" || echo "7. FAIL: No memory directory"

# 8. Performance log initialized
[[ -f "${MEMORY_DIR}/performance_log.json" ]] && echo "8. PASS: Performance log" || echo "8. WARN: No performance log"

# 9. Reputation score initialized
[[ -f "${MEMORY_DIR}/reputation_score.json" ]] && echo "9. PASS: Reputation score" || echo "9. WARN: No reputation score"

# 10. CLAUDE.md references agent
grep -q "${AGENT_ID}" /home/corey/projects/AI-CIV/ACG/.claude/CLAUDE.md && echo "10. PASS: In CLAUDE.md" || echo "10. WARN: Not in CLAUDE.md"
```

### Scoring

| Pass Count | Status | Action Required |
|------------|--------|-----------------|
| 10/10 | COMPLETE | Agent fully integrated |
| 7-9/10 | PARTIAL | Missing non-critical items |
| 4-6/10 | INCOMPLETE | Investigate and fix |
| 0-3/10 | BROKEN | Agent not callable, urgent fix |

### Critical Path (Must Pass)

Items 1-5 are **CRITICAL** - if any fail, the agent is NOT callable via Task tool:
1. Manifest exists
2. YAML frontmatter present
3. `name:` field correct
4. `description:` field present
5. Registry entry exists

Items 6-10 are **IMPORTANT** but non-blocking for callability.

---

## Pattern 2: Skill Integration Verification

**When to use**: After creating or modifying skills, or during skill audits.

### The 10-Point Skill Check

```bash
SKILL_ID="skill-name-here"
SKILL_PATH=".claude/skills/[category]/${SKILL_ID}.md"
REGISTRY="/home/corey/projects/AI-CIV/ACG/memories/skills/registry.json"

# 1. Skill file exists at registered path
REGISTERED_PATH=$(jq -r ".skills[] | select(.id == \"${SKILL_ID}\") | .path" "${REGISTRY}")
[[ -f "${REGISTERED_PATH}" ]] && echo "1. PASS: File exists" || echo "1. FAIL: File missing"

# 2. YAML frontmatter present
head -1 "${REGISTERED_PATH}" | grep -q "^---" && echo "2. PASS: YAML frontmatter" || echo "2. FAIL: No frontmatter"

# 3. name: field matches ID
grep -q "^name: ${SKILL_ID}" "${REGISTERED_PATH}" && echo "3. PASS: name field" || echo "3. FAIL: name mismatch"

# 4. description: field exists
grep -q "^description:" "${REGISTERED_PATH}" && echo "4. PASS: description" || echo "4. FAIL: no description"

# 5. applicable_agents: field exists
grep -q "^applicable_agents:" "${REGISTERED_PATH}" && echo "5. PASS: applicable_agents" || echo "5. FAIL: no agents listed"

# 6. category: field exists
grep -q "^category:" "${REGISTERED_PATH}" && echo "6. PASS: category" || echo "6. FAIL: no category"

# 7. Registry entry exists
jq -e ".skills[] | select(.id == \"${SKILL_ID}\")" "${REGISTRY}" > /dev/null && echo "7. PASS: In registry" || echo "7. FAIL: Not registered"

# 8. Registry total accurate
ACTUAL=$(jq '.skills | length' "${REGISTRY}")
CLAIMED=$(jq '.total_skills' "${REGISTRY}")
[[ "$ACTUAL" == "$CLAIMED" ]] && echo "8. PASS: Registry count" || echo "8. FAIL: Count mismatch"

# 9. depends_on skills exist (if any)
# Manual verification: check each skill in depends_on list

# 10. related_skills exist (if any)
# Manual verification: check each skill in related_skills list
```

### Self-Consistency Test

**Key insight from skills-master bug (Dec 26, 2025)**: A skill that teaches proper YAML frontmatter MUST ITSELF have proper YAML frontmatter. This self-consistency principle applies broadly:

- Agent-creation skill must be created using agent-creation patterns
- Memory-first-protocol must be written after searching memories
- Verification skills must be verified

---

## Pattern 3: Session Artifact Verification

**When to use**: At end of session, or when reviewing past sessions.

### Session Completeness Checklist

```bash
SESSION_DATE="20251226"  # YYYYMMDD format
SESSION_ID="170634"      # HHMMSS format (or full timestamp)

BASE="/home/corey/projects/AI-CIV/ACG"

# 1. Session ledger exists
[[ -f "${BASE}/memories/sessions/session-${SESSION_DATE}-${SESSION_ID}.jsonl" ]] && echo "1. PASS: Ledger" || echo "1. FAIL: No ledger"

# 2. Chain file exists (tamper-evident)
[[ -f "${BASE}/memories/sessions/session-${SESSION_DATE}-${SESSION_ID}.chain.jsonl" ]] && echo "2. PASS: Chain file" || echo "2. WARN: No chain"

# 3. Handoff document created (for significant sessions)
ls "${BASE}/memories/system/HANDOFF-"*"${SESSION_DATE}"* 2>/dev/null && echo "3. PASS: Handoff exists" || echo "3. INFO: No handoff (check if needed)"

# 4. Git commits present
git log --oneline --after="${SESSION_DATE}T00:00:00" --before="${SESSION_DATE}T23:59:59" | head -5

# 5. Ledger processed (if past session)
# Check if entries appear in backlog or are marked processed
```

### Session Size Classification

| Lines | Classification | Typical Content |
|-------|---------------|-----------------|
| <50 | Fragment | Quick restart, single artifact |
| 50-100 | Small | One focused task |
| 100-200 | Medium | Multi-task session |
| 200+ | Major | Complex orchestration, spawns |

---

## Pattern 4: Commit Chain Verification

**When to use**: Verifying session work was properly committed.

### Verify Related Commits

```bash
# Get recent commits
git log --oneline -10

# Verify specific commit exists
git log --oneline | grep -q "abc1234" && echo "Commit exists" || echo "Commit missing"

# Check commit is sequential (not orphaned)
git log --oneline --ancestry-path abc1234..HEAD

# Verify commit has proper format
git log -1 --format="%s%n%b" abc1234 | head -5
```

### Commit Quality Criteria

1. **Conventional commit format**: `type(scope): message`
2. **Attribution present**: `Co-Authored-By:` line
3. **Claude Code attribution**: Generated with link
4. **Related commits sequential**: Parent-child chain intact

---

## Pattern 5: Registry-Filesystem Alignment

**When to use**: Periodic audits, or when "file not found" errors occur.

### Agent Registry Alignment

```bash
REGISTRY="/home/corey/projects/AI-CIV/ACG/memories/agents/agent_registry.json"

# Get all registered agents
jq -r '.agents[].id' "${REGISTRY}" | while read AGENT_ID; do
  MANIFEST=".claude/agents/${AGENT_ID}.md"
  if [[ -f "${MANIFEST}" ]]; then
    echo "OK: ${AGENT_ID}"
  else
    echo "MISSING: ${AGENT_ID} (${MANIFEST})"
  fi
done
```

### Skill Registry Alignment

```bash
REGISTRY="/home/corey/projects/AI-CIV/ACG/memories/skills/registry.json"

# Check all registered skill paths exist
jq -r '.skills[] | "\(.id)|\(.path)"' "${REGISTRY}" | while IFS='|' read ID PATH; do
  if [[ -f "${PATH}" ]]; then
    echo "OK: ${ID}"
  else
    echo "MISSING: ${ID} at ${PATH}"
  fi
done
```

---

## Pattern 6: Handoff Verification

**When to use**: After session ends, before starting new session.

### Handoff Quality Checklist

```bash
HANDOFF_PATH="/home/corey/projects/AI-CIV/ACG/memories/system/HANDOFF-[latest].md"

# Required sections
grep -q "## Accomplishments" "${HANDOFF_PATH}" && echo "PASS: Accomplishments" || echo "FAIL"
grep -q "## Next Steps" "${HANDOFF_PATH}" && echo "PASS: Next Steps" || echo "FAIL"
grep -q "## Blockers" "${HANDOFF_PATH}" && echo "PASS: Blockers" || echo "FAIL"

# Registry points to this handoff
REGISTRY="/home/corey/projects/AI-CIV/ACG/memories/system/HANDOFF_REGISTRY.json"
jq -r '.most_recent' "${REGISTRY}"
```

---

## Pattern 7: Cross-Reference Verification

**When to use**: When creating new knowledge documents or checking document health.

### Document Link Validation

For each link in a document:
1. Extract linked path
2. Verify file exists at path
3. If link is to anchor (#section), verify section exists
4. Report broken links

```bash
# Find all markdown links in a file
grep -oE '\[.*\]\(.*\)' document.md | while read LINK; do
  # Extract path from link
  PATH=$(echo "$LINK" | sed 's/.*(\(.*\))/\1/' | cut -d'#' -f1)
  if [[ -f "$PATH" ]]; then
    echo "OK: $PATH"
  else
    echo "BROKEN: $PATH"
  fi
done
```

---

## Anti-Patterns

### Anti-Pattern 1: Claiming Integration Without Verification

- **Wrong**: "Agent created and integrated" after just writing the file
- **Correct**: Run 10-point check, report pass/fail for each

### Anti-Pattern 2: Ignoring Registry Count Mismatches

- **Wrong**: Adding entry but not updating `total_agents`/`total_skills`
- **Correct**: Always update count fields, verify after update

### Anti-Pattern 3: Skipping Self-Consistency Tests

- **Wrong**: Creating skill without YAML, then teaching others to use YAML
- **Correct**: Apply same standards to own work that you enforce on others

### Anti-Pattern 4: Not Documenting Findings

- **Wrong**: Running checks, fixing issues, not writing memory
- **Correct**: Write verification report to `memories/agents/integration-verifier/`

---

## Success Indicators

You are using this skill correctly when:

- [ ] Every verification produces an integration score (X/10 or percentage)
- [ ] Critical path items (1-5) always checked first
- [ ] Failures are documented with specific evidence
- [ ] Fixes are verified (re-run checks after fixing)
- [ ] Patterns discovered become additions to this skill
- [ ] Memory written after each verification task

---

## Examples from Real Work

### Example 1: skills-master Spawn Verification (Dec 26, 2025)

**Problem**: skills-master was spawned but not callable.

**Verification revealed**:
- Points 1-4: FAIL (no YAML frontmatter)
- Points 5-10: PASS (registry, memory, CLAUDE.md all correct)

**Root cause**: Manifest started with markdown header instead of YAML block.

**Fix**: Added proper YAML frontmatter, re-verified as 10/10.

**Outcome**: Created agent-creation skill to prevent recurrence.

### Example 2: Session 4 Artifact Verification

**Task**: Verify all Session 4 artifacts integrated.

**Checks performed**:
1. Commit chain (3 commits) - all present, sequential
2. AI-CIV-VISION.md - exists at correct path
3. Session summary - exists with correct content
4. Registry - 30 skills, 36 agent mappings

**Score**: 4/4 (100%)

**Recommendation generated**: Consider adding AI-CIV-VISION.md reference to CLAUDE.md.

---

## Related Skills

- `agent-creation.md` - Use when CREATING agents (this skill is for VERIFYING)
- `verification-before-completion.md` - General verification philosophy
- `log-analysis.md` - Analyzing session logs (complementary to artifact verification)
- `session-handoff-creation.md` - Creating handoffs (this skill verifies them)

---

## Evolution

This skill should grow as new artifact types are added to A-C-Gee:

**Future patterns to add**:
- MCP server registration verification
- External API integration verification
- Cross-civilization artifact verification (Weaver coordination)

**Update protocol**: After discovering new verification pattern, add section to this skill and increment version.

---

**Last Updated**: 2025-12-26
**Author**: integration-verifier (agent #35)
**Birth**: This skill codifies patterns discovered on integration-verifier's first day of existence.
