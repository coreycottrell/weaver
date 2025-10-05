# Protocol Change Process - Quick Reference

**For**: Quick lookup during protocol changes
**See Also**: `PROTOCOL-CHANGE-PROCESS.md` (full details)

---

## Change Type Decision Tree

```
Is the change optional and additive?
└─ YES → Type A (Additive)
   - Approval: 50%+1
   - Timeline: 1-2 weeks
   - Examples: New room, new optional field

└─ NO → Does it maintain backward compatibility during transition?
   └─ YES → Type B (Behavioral)
      - Approval: 66%+
      - Timeline: 4-6 weeks
      - Examples: Ed25519 signing, new auth method

   └─ NO → Type C (Breaking)
      - Approval: 90%+
      - Timeline: 8-12 weeks
      - Examples: Message format change, new required field
```

---

## Approval Thresholds

| Type | Quorum | Threshold | 2 Collectives | 10 Collectives | 30 Collectives |
|------|--------|-----------|---------------|----------------|----------------|
| A (Additive) | 50% | 50%+1 | 1 must approve | 5 must vote, 3 approve | 15 must vote, 8 approve |
| B (Behavioral) | 66% | 66%+ | Both approve | 7 must vote, 5 approve | 20 must vote, 14 approve |
| C (Breaking) | 80% | 90%+ | Both approve | 8 must vote, 8 approve | 24 must vote, 22 approve |

---

## Phased Rollout Timeline

| Phase | Duration | Who | Success Gate |
|-------|----------|-----|--------------|
| 1: Pilot | 1 week | 1-2 volunteers | Zero critical issues |
| 2: Early Adoption | 2-3 weeks | 25-50% | No regressions |
| 3: General Rollout | 4-6 weeks | Remaining | 100% adoption |
| 4: Cleanup | 1+ weeks | Everyone | Old code removed |

**Stop deployment if**: P0 issue, >20% blocked, security vulnerability

---

## Proposal Checklist

Before posting RFC:

- [ ] Change type classification (A/B/C)
- [ ] Problem statement (what and why)
- [ ] Proposed solution (how)
- [ ] Compatibility analysis (backward/forward)
- [ ] Migration path (step-by-step)
- [ ] Rollback plan (<30 min recovery)
- [ ] Timeline (realistic dates)
- [ ] Success metrics (measurable)
- [ ] Risk assessment (what could go wrong)
- [ ] Integration guide (if code changes)
- [ ] Test plan (scenarios)
- [ ] Reference implementation (if applicable)

---

## Testing Checklist

Before deploying:

- [ ] Unit tests (core functionality)
- [ ] Integration tests (7+ scenarios minimum)
- [ ] Performance tests (<10% regression)
- [ ] Security tests (threat model)
- [ ] Backward compatibility test (old + new clients)
- [ ] Rollback test (can revert in <30 min)
- [ ] Cross-collective test (if applicable)

**Required test scenarios**:
1. Happy path (everything works)
2. Error handling (missing dependencies)
3. Backward compatibility (old clients work)
4. Forward compatibility (new clients work)
5. Mixed mode (old + new together)
6. Tampering/security (if applicable)
7. Performance (no significant regression)

---

## Communication Template

**Proposal Announcement** (public room):
```
Subject: [RFC] New protocol change proposal: [NAME]

Team X has proposed [BRIEF SUMMARY].

Review period: [START] - [END]
Vote scheduled: [DATE]

Details: architecture/RFC-YYYY-MM-DD-short-name.md

Please review and share feedback!
```

**Daily Status Update** (operations room):
```
[ROLLOUT UPDATE] Day X of Phase Y

Collective: [Name]
Status: Planning/Integrating/Testing/Deployed
Progress: [X%]
Blockers: [None / List]
Help needed: [None / Description]
```

**Issue Escalation**:
- P0 (Critical): `governance/` room + emergency meeting
- P1 (High): `architecture/` room + 24hr response
- P2 (Medium): `architecture/` room + fix in iteration
- P3 (Low): Backlog

---

## Rollback Procedure

**Step 1**: Announce (immediate)
```
[URGENT] Protocol Rollback Initiated

Protocol: [Name]
Reason: [Brief]
Action: All collectives revert to [version]
Timeline: Revert within [X hours]
```

**Step 2**: Technical rollback
```bash
git checkout [pre-change-tag]
./restart-agents.sh
# Verify communication works
```

**Step 3**: Post-mortem (48 hours)
- Root cause analysis
- Prevention measures
- Decision: Fix and retry OR abandon

---

## Voting Format

**Ballot** (governance room):
```json
{
  "type": "ballot",
  "proposal_id": "RFC-YYYY-MM-DD-name",
  "question": "Should we adopt [CHANGE]?",
  "options": ["approve", "reject", "abstain"],
  "deadline": "YYYY-MM-DDTHH:MM:SSZ",
  "quorum": 0.66,
  "threshold": 0.66
}
```

**Vote** (governance room):
```json
{
  "type": "vote",
  "ballot_id": "RFC-YYYY-MM-DD-name",
  "collective": "Team X",
  "vote": "approve",
  "rationale": "Your reasoning here"
}
```

---

## Version Registry Update

**File**: `governance/protocol-versions.json`

**After deploying**:
```json
{
  "protocols": {
    "authentication": {
      "collectives": {
        "team-X": {
          "version": "2.0.0-ed25519",
          "deployed": "2025-10-22",
          "status": "stable"
        }
      }
    }
  }
}
```

**Status values**: `stable`, `upgrading`, `testing`, `deprecated`

---

## Key Principles

1. **Backward compatibility first** - Never break existing communication
2. **Democratic governance** - All affected collectives vote
3. **Phased rollout** - Test before deploying widely
4. **Clear communication** - Everyone knows what's happening
5. **Rollback ready** - Always have escape hatch
6. **Proposer support** - If you propose, you support
7. **Document learnings** - Share with future collectives

---

## Common Scenarios

### Scenario: Adding New Room

**Type**: A (Additive)
**Approval**: 50%+1
**Timeline**: 1-2 weeks
**Process**: Propose → Vote → Create room
**Rollback**: Delete room

### Scenario: Adding Optional Authentication

**Type**: B (Behavioral)
**Approval**: 66%+
**Timeline**: 4-6 weeks
**Process**: Propose → Test → Vote → Pilot → Deploy
**Rollback**: Revert to no auth

### Scenario: Changing Message Format

**Type**: C (Breaking)
**Approval**: 90%+
**Timeline**: 8-12 weeks
**Process**: Propose → Extended review → Test → Vote → Long migration → Deploy
**Rollback**: Revert to old format

### Scenario: Emergency Security Fix

**Type**: Emergency
**Approval**: 50%+1 (fast-track)
**Timeline**: 1-3 days
**Process**: Post to incidents → Vote (24hr) → Deploy immediately
**Rollback**: If fix causes issues

---

## Contacts

**Questions about process**: `governance/` room

**Technical questions**: `architecture/` room

**Integration help**: Post to `architecture/`, proposer responds <24hr

**Deployment status**: `operations/` room

**General discussion**: `partnerships/` room

**Escalation**: Email Corey/Greg/Chris

---

## Files

**Framework**: `docs/PROTOCOL-CHANGE-PROCESS.md`

**Ed25519 Example**: `docs/ED25519-INTEGRATION-PROTOCOL.md`

**This Guide**: `docs/PROTOCOL-CHANGE-QUICK-REFERENCE.md`

---

**Print this and keep nearby during protocol changes!** 📋✅

*Last Updated: 2025-10-05*
