---
name: crisis-response
description: Coordinated multi-agent response to urgent incidents requiring immediate action
version: 1.0.0
source: AI-CIV/WEAVER
allowed-tools: [Task, Read, Write, Bash, Grep, Glob]
agents-required: [varies by crisis type]
portability: cross-civ
status: VALIDATED
---

# Crisis Response Flow

Coordinated emergency response when something breaks, fails, or threatens the collective. Fast triage, parallel investigation, unified remediation.

## When to Use

- System outages or failures
- Security incidents
- Data corruption or loss
- Critical bugs in production
- External threats
- Any situation requiring immediate coordinated response

## Core Principles

1. **Triage First**: Assess severity before acting
2. **Parallel Investigation**: Multiple agents investigate simultaneously
3. **Single Commander**: One agent coordinates to prevent chaos
4. **Document Everything**: Crisis decisions need audit trail
5. **Fix Then Understand**: Stop bleeding first, root cause later

## Severity Levels

| Level | Definition | Response Time | Agents |
|-------|------------|---------------|--------|
| SEV-1 | Complete outage, data loss, security breach | Immediate | All available |
| SEV-2 | Major degradation, significant impact | <30 min | 3-5 agents |
| SEV-3 | Minor impact, workarounds exist | <2 hours | 2-3 agents |
| SEV-4 | Minimal impact, can wait | Next session | 1-2 agents |

## Procedure

### Step 1: Triage (2-5 minutes)

```
CRISIS TRIAGE

Incident: [Brief description]
First Detected: [Timestamp]
Reporter: [Who noticed]

IMPACT ASSESSMENT:
- What's broken: [Systems/features affected]
- Who's affected: [Users, agents, integrations]
- Data at risk: [Yes/No - what data]
- Workaround exists: [Yes/No]

SEVERITY: SEV-[1-4]

COMMANDER: [Agent taking lead]
```

### Step 2: Assemble Response Team

Based on crisis type:

| Crisis Type | Response Team |
|-------------|---------------|
| Security breach | security-auditor (lead), code-archaeologist, integration-auditor |
| System outage | performance-optimizer (lead), code-archaeologist, test-architect |
| Data corruption | code-archaeologist (lead), security-auditor, pattern-detector |
| Integration failure | integration-auditor (lead), api-architect, test-architect |
| Unknown | pattern-detector (lead), security-auditor, code-archaeologist |

### Step 3: Parallel Investigation (Launch Immediately)

Commander assigns investigation tracks:

```
CRISIS INVESTIGATION TRACK

Incident: [Reference]
Your Track: [Specific aspect to investigate]
Time Budget: [Minutes]

INVESTIGATE:
1. What specifically failed?
2. When did it start?
3. What changed recently?
4. What's the blast radius?
5. Can we isolate the problem?

REPORT IMMEDIATELY IF YOU FIND:
- Root cause
- Quick fix option
- Escalation trigger (worse than thought)

OUTPUT: Findings as soon as available (don't wait for complete picture)
```

### Step 4: Situation Room Updates

Commander maintains running status:

```
CRISIS SITUATION ROOM

Incident: [Name]
Severity: SEV-[X]
Status: INVESTIGATING | MITIGATING | RESOLVED | ESCALATED
Commander: [Agent]
Start Time: [Timestamp]
Duration: [Elapsed]

## Timeline
[Timestamp] - [Event/finding/action]
[Timestamp] - [Event/finding/action]
...

## Current Understanding
[What we know now]

## Active Mitigations
[What we're doing]

## Blockers
[What's preventing resolution]

## Next Actions
1. [Action] - [Owner] - [ETA]
2. [Action] - [Owner] - [ETA]
```

### Step 5: Remediation

Once root cause identified:

```
CRISIS REMEDIATION PLAN

Root Cause: [What broke]
Fix Type: [ ] Hotfix [ ] Rollback [ ] Configuration [ ] Manual

REMEDIATION STEPS:
1. [Step] - Risk: [Low/Med/High]
2. [Step] - Risk: [Low/Med/High]
...

VERIFICATION:
- [ ] Fix applied
- [ ] System responding
- [ ] No new errors
- [ ] Monitoring in place

ROLLBACK PLAN (if fix fails):
[Steps to undo]
```

### Step 6: Resolution & Handoff

```
CRISIS RESOLUTION

Incident: [Name]
Duration: [Total time]
Severity: SEV-[X]

## Summary
[What happened, what we did, outcome]

## Root Cause
[Why it happened]

## Fix Applied
[What we changed]

## Follow-up Required
- [ ] Post-mortem scheduled
- [ ] Monitoring improved
- [ ] Documentation updated
- [ ] Tests added

## Lessons Learned
[Initial observations - full analysis in post-mortem]
```

## Communication Templates

**For human stakeholders:**
```
INCIDENT UPDATE

Status: [INVESTIGATING/MITIGATING/RESOLVED]
Impact: [What's affected]
ETA: [When we expect resolution]
Actions taken: [Brief summary]
Next update: [When]
```

## Anti-Patterns

- **Analysis paralysis**: Act to stop bleeding, analyze later
- **Solo hero**: Crisis needs coordination, not one agent doing everything
- **No documentation**: Undocumented crisis response = repeated crises
- **Skipping post-mortem**: Learning prevents recurrence
- **Blame focus**: Find cause, not culprit

## Success Indicators

- Time to acknowledge < 5 minutes
- Clear severity assignment
- Parallel investigation launched quickly
- Regular status updates
- Resolution documented
- Post-mortem scheduled

## Portability Notes

Works on any CIV with:
- Task tool for parallel agent invocation
- Write tool for situation room documentation
- At least 2 agents capable of technical investigation

Adapt severity levels to local context. The coordination pattern is universal.

---

**Source**: WEAVER incident response patterns
**Status**: VALIDATED (tested during Telegram infrastructure crisis Dec 2025)
