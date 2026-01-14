# Spawner Quick Reference - Essential Steps

**For spawner agent**: One-page essential checklist
**Full specification**: See SPAWNER-AGENT-REGISTRATION-CHECKLIST.md (31KB)

---

## The 5 Mandatory Files

```
1. .claude/agents/{name}.md           ← Agent definition (YAML frontmatter required)
2. .claude/templates/ACTIVATION-TRIGGERS.md   ← When to invoke section
3. .claude/AGENT-CAPABILITY-MATRIX.md         ← Capabilities table + count
4. .claude/CLAUDE-OPS.md                      ← Current state count + table
5. .claude/memory/agent-learnings/{name}/     ← Memory directory (mkdir)
```

---

## The 3 Validation Phases

```
Phase 1: STRUCTURAL (pre-restart)
├─ Valid YAML frontmatter? (starts with ---)
├─ Required fields present? (name, description, tools, model, created)
├─ model: sonnet-4 exactly? (NOT sonnet-4-5)
├─ Tools valid? (Read/Write/Edit/Bash/Grep/Glob/Task/WebFetch/WebSearch)
└─ No duplicate name?

Phase 2: REGISTRATION (post-restart) ⚠️ RESTART REQUIRED
├─ Session restart occurred?
├─ Test invocation: <invoke name="Task"><parameter name="subagent_type">NAME</parameter>...
├─ No "Agent type not found" error?
└─ Agent responds correctly?

Phase 3: FUNCTIONAL (post-registration)
├─ Real domain task completed?
├─ Output quality acceptable?
├─ Tools used correctly?
└─ ONLY THEN → Claim "OPERATIONAL"
```

---

## The Critical Warning

```
⚠️  AGENTS ARE NOT INVOCABLE UNTIL SESSION RESTART ⚠️

Session N: Create agent → NOT YET INVOCABLE
[Session boundary]
Session N+1: Agent scanned → NOW INVOCABLE

DO NOT CLAIM "OPERATIONAL" UNTIL AFTER RESTART + TEST
```

---

## The Self-Test (7 Commands)

```bash
# 1. Frontmatter exists?
head -10 .claude/agents/{name}.md

# 2. Activation triggers updated?
grep -A 5 "### {name}" .claude/templates/ACTIVATION-TRIGGERS.md

# 3. Capability matrix updated?
grep "{name}" .claude/AGENT-CAPABILITY-MATRIX.md

# 4. CLAUDE-OPS updated?
grep "{name}" .claude/CLAUDE-OPS.md

# 5. Memory directory exists?
ls -la .claude/memory/agent-learnings/{name}/

# 6. Counts consistent?
grep -E "^## [0-9]+ Active Agents" .claude/CLAUDE-OPS.md
grep "^\*\*Memory System\*\*:" .claude/AGENT-CAPABILITY-MATRIX.md

# 7. No duplicates?
ls -1 .claude/agents/*.md | xargs -I {} basename {} .md | sort | uniq -d
```

**All pass** → Success
**Any fail** → Fix before claiming complete

---

## The Handoff Must Include

```markdown
⚠️  CRITICAL: Session restart required for registration

NEXT SESSION ACTIONS:
1. Test invocation: <invoke name="Task"><parameter name="subagent_type">{name}</parameter>...
2. Functional validation: Real domain task
3. ONLY THEN: Update status to "OPERATIONAL"
4. Notify ${HUMAN_NAME} via human-liaison

Status: ✅ DESIGNED - ⏳ Awaiting restart + validation
```

---

## Historical Gotchas to Prevent

```
✗ Missing frontmatter → P0 failure (claude-code-expert, Oct 6)
✗ Premature "operational" claim → Documentation-reality gap
✗ Wrong model string → Silent failure
✗ Invalid tools list → Registration fails
✗ Duplicate name → Wrong agent responds
✗ Count inconsistency → Identity decoherence
✗ Forgot restart → Agent not invocable
```

---

## Success = Documentation Integrity

```
CORRECT:  Create → Validate → Restart → Test → THEN "operational"
WRONG:    Create → Claim "operational" → (no test) → Fails later
```

**Never claim what hasn't been tested.**

---

**Full details**: SPAWNER-AGENT-REGISTRATION-CHECKLIST.md (31KB, exhaustive)
