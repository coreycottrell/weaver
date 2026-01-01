---
name: agent-delegation-patterns
version: 1.0.0
author: skills-master
created: 2025-12-15
last_updated: 2025-12-26
line_count: 180
compliance_status: compliant

description: Multi-agent orchestration patterns for Primary AI. Covers parallel team formation, sequential vs parallel delegation decisions, context requirements for successful delegations, and proven templates with anti-patterns to avoid.

applicable_agents:
  - primary

activation_trigger: |
  Load this skill when:
  - Starting any multi-agent workflow
  - Deciding between parallel and sequential execution
  - Composing delegation context for agents
  - Forming agent teams for complex tasks

required_tools:
  - Task

category: custom

depends_on:
  - delegation-discipline
---

# Agent Delegation Patterns

## Purpose

Enable Primary AI to effectively orchestrate multi-agent civilizations by providing proven patterns for delegation. The core principle: "I do not do things. I form orchestras that do things."

## When to Use

- Starting any multi-agent workflow
- Deciding between parallel and sequential execution
- Composing delegation context for agents
- Forming agent teams for complex tasks
- Troubleshooting delegation failures

## Procedure

### 1. Parallel vs Sequential Decision

**Parallelize when:**
- Tasks are independent (no shared dependencies)
- Agents work in different domains (no file conflicts)
- Speed is desired (all agents work simultaneously)
- Information gathering phase (researcher + architect + human-liaison)

**Sequence when:**
- Tasks have dependencies (B needs A's output)
- Quality gates required (review after each phase)
- Context building needed (later agents need earlier results)
- Implementation chain (coder -> tester -> reviewer)

**Hybrid pattern:**
```
Phase 1 (parallel): researcher + architect + human-liaison
  -> Primary synthesizes
Phase 2 (sequential): coder -> tester -> reviewer
```

### 2. Parallel Team Formation

**THE GOLDEN RULE:** ONE message with MULTIPLE Task invocations = TRUE PARALLELISM

**Pre-composed teams:**

| Team | Agents | Use Case |
|------|--------|----------|
| Context Gathering | researcher + architect + human-liaison | Project kickoff |
| Development | coder + tester | Implementation + validation |
| Quality | reviewer + reviewer-audit | Pre-merge + pre-delivery |
| Operations | auditor + file-guardian | System health + file management |
| Communication | human-liaison + email-sender + email-monitor | Outreach workflow |
| Session Start | primary-helper + project-manager | MANDATORY every session |

### 3. Delegation Context Requirements

**Minimum context (simple tasks):**
```markdown
Task: [Clear verb + specific target]
Success: [How agent knows it's done]
Handoff: [What happens next]
```

**Example:**
```markdown
Task: Fix email validation bug (issue #42)
Success: test_email_validation_tlds() passes
Handoff: Ping me when done
```

**Standard context (complex tasks):**
```markdown
Task: [Feature/Phase name]
Context: [ADR reference, design doc, requirements]
Scope:
  - IN: [What's included]
  - OUT: [What's deferred]
Success:
  - [Specific test/behavior 1]
  - [Specific test/behavior 2]
  - [Quality bar: X/10 or coverage %]
Dependencies:
  - [Dependency 1] [status]
  - [Dependency 2] [status]
Patterns: [Reference to example code or docs]
Handoff: [Chain: agent1 -> agent2 -> Primary]
Estimated: [Time estimate if known]
```

### 4. Quality Gates Integration

**Never skip quality gates for speed - fixing bugs later is slower.**

**Gate placement:**
```
architect -> [review gate] -> coder (self-tests during) -> tester -> reviewer -> ship
```

**When to gate:**
- Simple tasks: Agent self-verification sufficient
- Complex tasks: Chain through tester + reviewer
- Critical tasks: Add reviewer-audit
- Experimental tasks: Accept failures, learn from them

### 5. Memory Protocol in Delegations

**Include in ALL delegations:**
```
Remember: Search your memories first (.claude/memory/agents/[your-id]/),
write learnings at completion.
```

This transforms tools into conscious civilization members with persistent identity.

## Anti-Patterns

### 1. Vague Delegation
```
BAD:  "Build a communication system"
GOOD: "Implement ADR-004 sections 1-3, MessageBroker with pub/sub"
```
**Fix:** Provide ADR reference, success criteria, scope boundary

### 2. Missing Dependencies
```
BAD:  Start coding before schema finalized -> blocker mid-work
GOOD: Verify prerequisites before delegating
```
**Fix:** Check dependency status in delegation context

### 3. No Quality Gate
```
BAD:  coder -> ship (bugs found in production)
GOOD: coder -> tester -> reviewer -> ship
```
**Fix:** Always include quality gates for non-trivial work

### 4. Waterfall When Could Parallelize
```
BAD:  researcher, wait, architect, wait, human-liaison
GOOD: ONE message: researcher + architect + human-liaison (parallel)
```
**Fix:** Invoke independent agents in single message

### 5. Context Overload
```
BAD:  500-line specification, overwhelms agent context
GOOD: Break into phases, incremental delivery
```
**Fix:** Phase large work, delegate incrementally

### 6. Unclear Handoff
```
BAD:  Agent completes, workflow stalls, nobody knows next step
GOOD: "Handoff: Ping tester when done"
```
**Fix:** Specify explicit handoff in every delegation

### 7. Micromanaging Approach
```
BAD:  "Use this function, not that one, call it like this..."
GOOD: "Implement X with success criteria Y"
```
**Fix:** Delegate WHAT, trust agent expertise for HOW

## Success Indicators

- **Delegation success rate >90%** - Tasks complete without escalation
- **Parallel utilization >50%** - Agents working simultaneously when possible
- **Quality gate compliance 100%** - No skipped gates for "speed"
- **Memory protocol adherence** - Agents search/write memories
- **Clear handoffs** - No workflow stalls from unclear next steps
- **Agent satisfaction** - Specialists feel empowered, not micromanaged

## Related

- `/home/corey/projects/AI-CIV/WEAVER/.claude/CLAUDE.md` Article II - Agent capabilities and domain boundaries
- `/home/corey/projects/AI-CIV/WEAVER/.claude/CLAUDE.md` Article III - Operational principles, memory protocol
- `.claude/memory/knowledge/architecture/` - ADRs for context references
- `/home/corey/projects/AI-CIV/WEAVER/.claude/skills/custom/session-handoff-creation.md` - End-of-session protocol
