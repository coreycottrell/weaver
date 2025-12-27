---
name: quality-gate
description: Sequential approval checkpoints before code, decisions, or artifacts are accepted
version: 1.0.0
source: AI-CIV/WEAVER
allowed-tools: [Task, Read, Bash, Grep, Glob]
agents-required: [varies by gate type]
portability: cross-civ
status: VALIDATED
---

# Quality Gate Flow

Sequential checkpoints where specialists must approve before proceeding. Each gate has clear criteria. Failure at any gate blocks progress until resolved.

## When to Use

- Before merging significant code changes
- Before deploying to production
- Before publishing documentation
- Before adopting external packages
- Any high-stakes transition requiring verification

## Core Principle

**Quality is not a phase, it's gates throughout**. Each specialist owns their domain's quality. Nothing passes without their approval.

## Gate Types

### Code Quality Gates

```
GATE SEQUENCE: Code Changes

Gate 1: FUNCTIONALITY (test-architect)
- [ ] All tests pass
- [ ] New functionality has tests
- [ ] Edge cases covered
- [ ] No regressions

Gate 2: SECURITY (security-auditor)
- [ ] No vulnerabilities introduced
- [ ] Input validation present
- [ ] Auth/authz correct
- [ ] No secrets exposed

Gate 3: ARCHITECTURE (pattern-detector)
- [ ] Follows established patterns
- [ ] No unnecessary complexity
- [ ] Appropriate abstractions
- [ ] Documentation updated

Gate 4: INTEGRATION (integration-auditor)
- [ ] Integrates with existing systems
- [ ] No broken dependencies
- [ ] Discoverable to future sessions
- [ ] Activation verified
```

### Decision Quality Gates

```
GATE SEQUENCE: Major Decisions

Gate 1: RESEARCH (web-researcher or domain expert)
- [ ] Alternatives explored
- [ ] Evidence gathered
- [ ] Assumptions validated

Gate 2: ANALYSIS (pattern-detector)
- [ ] Trade-offs identified
- [ ] Risks assessed
- [ ] Reversibility evaluated

Gate 3: CONSENSUS (conflict-resolver)
- [ ] Stakeholders consulted
- [ ] Objections addressed
- [ ] Agreement documented

Gate 4: DOCUMENTATION (doc-synthesizer)
- [ ] Decision recorded
- [ ] Rationale captured
- [ ] Context preserved
```

### Deployment Quality Gates

```
GATE SEQUENCE: Production Deployment

Gate 1: BUILD (test-architect)
- [ ] Build succeeds
- [ ] All tests pass
- [ ] No new warnings

Gate 2: SECURITY SCAN (security-auditor)
- [ ] Dependency vulnerabilities checked
- [ ] Secrets scan passed
- [ ] Permissions appropriate

Gate 3: PERFORMANCE (performance-optimizer)
- [ ] No performance regressions
- [ ] Resource usage acceptable
- [ ] Scaling considered

Gate 4: ROLLBACK READY (code-archaeologist)
- [ ] Rollback procedure documented
- [ ] Previous version accessible
- [ ] Data migration reversible
```

## Procedure

### Step 1: Define Gate Sequence

```
QUALITY GATE CONFIGURATION

Subject: [What's being gated]
Transition: [From state] -> [To state]

Gates (in order):
1. [Gate name] - Owner: [Agent] - Blocking: [Yes/No]
2. [Gate name] - Owner: [Agent] - Blocking: [Yes/No]
...

Bypass authority: [Who can skip gates in emergency]
```

### Step 2: Execute Gates Sequentially

For each gate:

```
GATE CHECK: [Gate Name]

Subject: [What's being evaluated]
Owner: [Agent responsible]
Criteria:

[ ] Criterion 1: [Description]
    Status: [PASS/FAIL/N/A]
    Evidence: [How verified]

[ ] Criterion 2: [Description]
    Status: [PASS/FAIL/N/A]
    Evidence: [How verified]

...

GATE VERDICT: [PASS / FAIL / CONDITIONAL PASS]

If FAIL:
  Blockers:
  - [What must be fixed]
  - [What must be fixed]

  Re-check after: [What needs to happen]

If CONDITIONAL PASS:
  Conditions:
  - [Must be true for passage to remain valid]

Signed: [Agent]
Date: [Timestamp]
```

### Step 3: Track Progress

```
GATE PROGRESS TRACKER

Subject: [What's being gated]
Started: [Timestamp]

| Gate | Owner | Status | Verdict | Notes |
|------|-------|--------|---------|-------|
| Gate 1 | [Agent] | COMPLETE | PASS | [Notes] |
| Gate 2 | [Agent] | IN PROGRESS | - | [Notes] |
| Gate 3 | [Agent] | PENDING | - | - |
| Gate 4 | [Agent] | PENDING | - | - |

Current blocker: [If any]
ETA to completion: [Estimate]
```

### Step 4: Final Approval

```
GATE COMPLETION CERTIFICATE

Subject: [What passed]
All gates: PASSED
Date: [Timestamp]

Gate Summary:
1. [Gate 1]: PASS - [Key finding]
2. [Gate 2]: PASS - [Key finding]
...

Conditions/Caveats:
- [Any conditional passes noted]

Approved for: [What this enables]
Approved by: [Final authority]

This certificate valid until: [Expiry/condition]
```

## Emergency Bypass

When gates must be skipped:

```
GATE BYPASS REQUEST

Gates bypassed: [List]
Reason: [Emergency justification]
Risk accepted by: [Authority]
Compensating controls: [What we're doing instead]
Remediation plan: [How we'll address skipped gates later]
Expiry: [When bypass is no longer valid]
```

## Anti-Patterns

- **Gate theater**: Checking boxes without real verification
- **Wrong owners**: Gates owned by agents without domain expertise
- **Too many gates**: Paralysis from excessive checkpoints
- **Permanent bypass**: Emergencies that never get remediated
- **Sequential when parallel OK**: Some gates can run concurrently

## Success Indicators

- Clear pass/fail for each gate
- Blockers identified early (not at final gate)
- Evidence documented for each criterion
- Bypass used rarely and remediated
- Quality visibly improved over time

## Portability Notes

Works on any CIV with:
- Agents with domain expertise to own gates
- Task tool for sequential invocation
- Documentation capability for certificates

Customize gate sequences for local needs. The checkpoint pattern is universal.

---

**Source**: WEAVER quality assurance patterns
**Validated**: December 2025
