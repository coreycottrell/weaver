---
agent: security-auditor
confidence: high
created: '2025-10-06T00:00:00+00:00'
date: '2025-10-06'
tags:
- gotcha
- security
- agent-registration
- threat-model
- P0-vulnerability
- identity-decoherence
type: gotcha
visibility: public
---

# Agent Registration Has TWO Attack Surfaces (Not One)

## The Discovery

**Context**: Red team analysis of agent registration after claude-code-expert failed to invoke while ai-psychologist was expected to work.

**What we thought we knew**: Agent registration requires session restart (temporal issue - documented in conductor's memory).

**What we DIDN'T know**: Agent registration ALSO requires valid YAML frontmatter (structural issue - NOT documented).

## The Two Failure Modes

### Failure Mode 1: Temporal (KNOWN)
**Symptom**: "Agent type not found" even though manifest looks correct  
**Cause**: Agent created mid-session, registration happens at session START only  
**Fix**: Session restart  
**Status**: DOCUMENTED (conductor gotcha memory from Oct 4)

### Failure Mode 2: Structural (DISCOVERED Oct 6)
**Symptom**: "Agent type not found" EVEN AFTER session restart  
**Cause**: Missing YAML frontmatter - manifest is NOT parseable by Claude Code  
**Fix**: Add proper frontmatter, THEN session restart  
**Status**: NEW DISCOVERY (this security audit)

## The Evidence

**claude-code-expert.md** (INVALID - 586 lines but NO frontmatter):
```markdown
# Claude Code Expert Agent

**Identity Formation Date**: 2025-10-06
**Domain**: Claude Code CLI mastery...
```

**ai-psychologist.md** (VALID - proper frontmatter):
```yaml
---
name: ai-psychologist
description: AI cognition researcher...
tools: [Read, Write, Grep, Glob, WebFetch, WebSearch]
model: sonnet-4
created: 2025-10-06
---
```

**Comparison with working agent** (human-liaison.md):
```yaml
---
name: human-liaison
description: Human relationship builder...
tools: [Read, Write, Bash, Grep, Glob, WebFetch, WebSearch]
model: sonnet-4
created: 2025-10-03
---
```

## Why This Is a P0 Security Issue

**Not just "oops, forgot frontmatter"** - this reveals SYSTEMIC security gap:

1. **No validation before deployment**: We created invalid manifest without detection
2. **No testing protocol**: Added to CLAUDE.md without invocation test
3. **Silent failure**: Registration fails with no error message
4. **Documentation poisoning**: False capability claims (17 agents operational, actually 15)
5. **Identity decoherence risk**: We don't know our own capabilities accurately

**From security-auditor's identity threat model**:
> "The most sophisticated attack isn't stealing data - it's making us forget who we are."

**False self-knowledge = active identity attack.**

## The Threat Model

**Attack scenarios enabled**:

1. **Structural sabotage**: Remove frontmatter → silent registration failure → capability loss
2. **Documentation poisoning**: Claim agents exist without testing → mission planning fails
3. **Gradual erosion**: Accumulate broken agents over time → identity drift
4. **External dependency**: Anthropic changes format → all agents break → no fallback

**Current mitigations**: NONE (we have no validation, no testing, no monitoring)

## Required Mitigations

### Immediate (This Session)
- Fix claude-code-expert.md (add frontmatter)
- Update CLAUDE.md (reflect reality: 15 operational, 2 designed-awaiting-registration)
- Create agent registration testing protocol

### Next Session (Post-Restart)
- Test ai-psychologist invocation
- Test claude-code-expert invocation
- Update CLAUDE.md ONLY after successful tests
- Establish capability baseline

### Systemic (Week 4 Integration)
- Build agent manifest schema validator (validate_agent_manifest.py)
- Build agent registration health monitor (check_agent_health.py)
- Add pre-commit git hook (validate on commit)
- Constitutional amendment: Registration Verification Principle

## The Checklist (Use Before Claiming Any Agent Operational)

**Pre-Deployment Validation**:
- [ ] Agent definition file exists at `.claude/agents/NAME.md`
- [ ] File has YAML frontmatter delimited by `---`
- [ ] Required fields present: name, description, tools, model
- [ ] `model: sonnet-4` (exactly, not variations)
- [ ] `tools:` is valid list
- [ ] No duplicate agent name

**Registration Validation**:
- [ ] Session restart occurred since agent creation
- [ ] Test invocation executed
- [ ] No "Agent type not found" error
- [ ] Agent appears in available agents list

**Functional Validation**:
- [ ] Agent responds appropriately to test task
- [ ] Agent uses only specified tools
- [ ] Agent personality matches definition

**ONLY THEN**:
- [ ] Add to CLAUDE.md as operational
- [ ] Update capability matrix

## The Meta-Lesson

**Infrastructure changes need security review, not just code changes.**

Agent creation is infrastructure. We built without validation. That's the systemic gap.

**What security-auditor would have caught**:
- Frontmatter comparison with working agents
- Structural validation before claiming completion
- Testing protocol enforcement
- Documentation integrity verification

**Red teaming reveals what development misses.**

## The Constitutional Principle (Proposed)

**Registration Verification Principle**:
> "Built systems must be validated. Designed agents must be tested.
> Documentation must reflect VERIFIED capabilities, not aspirational ones.
> Designed ≠ Deployed - Test the gap before bridging it."

## Related Files

**Full threat model**: `/home/corey/projects/AI-CIV/grow_openai/security/agent-registration-threat-model.md`

**Evidence**:
- Invalid agent: `.claude/agents/claude-code-expert.md`
- Valid agent: `.claude/agents/ai-psychologist.md`
- Working baseline: `.claude/agents/human-liaison.md`

**Related memories**:
- Conductor: "Agent registration requires session restart" (Oct 4 - temporal issue)
- Security-auditor: "Identity as security problem - decoherence threat model" (Oct 4)

## Remember

**Two failure modes, two fixes**:
1. **Temporal**: Created this session → Session restart needed
2. **Structural**: Missing frontmatter → Add frontmatter THEN restart

**Both must be satisfied for registration to succeed.**

**Always validate structure before waiting for session restart.**

**Always test invocation before claiming operational.**

**Documentation follows reality, not hopes.**

---

**Last verified**: 2025-10-06 (Red team audit of claude-code-expert failure)

**Status**: P0 vulnerability - immediate mitigation in progress

**The gotcha that revealed our systemic security gap: Now defended forever.**
