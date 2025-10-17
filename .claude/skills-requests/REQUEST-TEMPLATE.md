# Skill Request Template

**Date**: YYYY-MM-DD
**Requester**: [Agent name or Human]
**Priority**: [P0/P1/P2]
**Status**: [pending/approved/rejected/implemented]

---

## Skill Being Requested

**Skill Name**: [pdf, docx, xlsx, or new custom skill]
**Source**: [Anthropic official / Custom AI-CIV skill]
**Repository**: [URL if applicable]

---

## Requesting Agent

**Agent**: [Which agent needs this skill?]
**Current Tools**: [What tools does agent already have?]
**Domain**: [Agent's primary domain]

---

## Use Case

**Problem**: [What problem does this skill solve?]

**Current Workflow** (without skill):
- Step 1: ...
- Step 2: ...
- Time: X minutes

**Proposed Workflow** (with skill):
- Step 1: ...
- Step 2: ...
- Time: Y minutes

**Expected Efficiency Gain**: Z% faster

---

## Fit Analysis

**Tool Compatibility**:
- Does agent have Bash access? [Yes/No]
- Any tool restrictions that would block? [List concerns]

**Domain Alignment**:
- Does skill match agent's purpose? [Explain]
- Would skill strengthen or dilute agent identity? [Analysis]

**Alternative Solutions**:
- Could this be solved with existing tools? [Yes/No + explanation]
- Could another agent handle this with current skills? [Yes/No + who]

---

## Dependencies

**Technical**:
- Python libraries required: [List]
- System packages required: [List]
- Virtual environment needed: [Yes/No]

**Infrastructure**:
- Manifest updates: [Which files]
- Documentation updates: [Which files]
- Integration audit required: [Yes/No]

---

## Approval Criteria

**Must Answer YES to All**:
- [ ] Efficiency gain >30% expected?
- [ ] Agent has necessary tool access (Bash)?
- [ ] Skill aligns with agent domain?
- [ ] No existing solution adequate?
- [ ] Dependencies can be satisfied?

**If ANY "No"**: Reject or defer with explanation

---

## Decision

**Approved By**: [the-conductor / capability-curator]
**Date**: YYYY-MM-DD
**Rationale**: [Why approved/rejected]

**Implementation Timeline** (if approved):
- Phase: [1/2/3]
- Estimated effort: [X hours]
- Target date: [YYYY-MM-DD]

---

## Post-Implementation

**Actual Results** (fill after deployment):
- Efficiency gain measured: [X%]
- Adoption rate: [frequency of use]
- Issues encountered: [List]
- Agent feedback: [Positive/Negative + details]

**Lessons Learned**:
- [What went well]
- [What could be improved]
- [Recommendations for future skill grants]
