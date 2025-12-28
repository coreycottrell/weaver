# Skill Deduplication Planning: Cross-CIV Methodology

**Date**: 2025-12-27
**Status**: PLANNING COMPLETE - Awaiting Corey's Review
**Request**: "set up a team to contemplate what this would look like cuz we need to make sure we get this right the first time"

---

## Executive Summary

Three specialist agents collaborated to design a comprehensive skill deduplication system:

| Agent | Domain | Deliverable |
|-------|--------|-------------|
| **pattern-detector** | Overlap Detection | Similarity scoring, classification taxonomy, decision framework |
| **doc-synthesizer** | Merge Methodology | 4 merge strategies, governance, consent model, proposal template |
| **test-architect** | Merge Testing | RED TEAM validation, acceptance criteria, rollback procedures |

**Key Insight**: We have a concrete example - 3 log analysis skills from 2 CIVs:
- WEAVER: `session-archive-analysis` (growth tracking focus)
- A-C-Gee: `log-analysis` (metrics/tokens focus)
- A-C-Gee: `session-pattern-extraction` (delegation patterns)

---

## 1. Detection System (pattern-detector)

### Similarity Scoring Formula
```
OverlapScore = (
    0.25 * NameSimilarity +
    0.30 * DescriptionSimilarity +
    0.20 * FunctionalOverlap +
    0.15 * AgentOverlap +
    0.10 * CategoryMatch
)
```

### Thresholds
| Score | Classification | Action |
|-------|----------------|--------|
| 0.90+ | Near-Duplicate | Mandatory merge review |
| 0.70-0.89 | High Overlap | Merge recommended |
| 0.50-0.69 | Partial Overlap | Consider specialization |
| 0.30-0.49 | Low Overlap | Document relationship |
| <0.30 | Distinct | No action |

### Classification Taxonomy
- **REDUNDANT** → Merge into one
- **COMPLEMENTARY** → Keep both, document relationship
- **CONFLICTING** → Resolve incompatibilities first

---

## 2. Merge Strategies (doc-synthesizer)

### Four Approaches

| Strategy | When to Use | Risk Level |
|----------|-------------|------------|
| **Union** | Combine all techniques, no contradictions | Medium |
| **Best-of** | Select highest-quality components | High (political) |
| **Layered** | Base + CIV-specific extensions | Low |
| **Federated** | Don't merge - create routing meta-skill | Lowest |

### Governance Model

**Consent Levels** (CIVs declare in skill metadata):
1. OPEN - Merge freely
2. NOTIFY - Merge allowed, notify of result
3. REVIEW - Requires our review before publish
4. APPROVE - Requires explicit approval
5. LOCKED - Reference only, no merge

**Approval Bodies**:
- Source CIVs (always required)
- Hub Council (for shared base layers)
- Quality Board (for best-of selections)
- Synthesis Council (for union merges)

---

## 3. Testing Methodology (test-architect)

### RED TEAM Validation Phases

1. **Pre-Merge Analysis**: Extract claims, detect conflicts, generate test plan
2. **Functional Tests**: Does merged skill do everything originals did?
3. **Comparison Tests**: Same task with A, B, and merged - compare outcomes
4. **Acceptance Decision**: Score card, thresholds, verdict

### Acceptance Criteria

| Verdict | Criteria |
|---------|----------|
| **PASS** | Score ≥90, all dimensions ≥70, zero regressions |
| **CONDITIONAL** | Score ≥75, no dimension <60, human approval |
| **FAIL** | Score <75, or any dimension <50, or hard regression |

### Instant Rejection Triggers
- Lost functionality
- Introduced contradiction
- Critical warning removed
- Dependency breakage
- Semantic corruption

---

## 4. Recommended Resolution: Log Analysis Skills

**pattern-detector's recommendation**: **Layered Merge (Pattern D)**

```
session-analysis-core (NEW - shared primitives)
├── JSONL parsing, message aggregation
├── Contributors: WEAVER + A-C-Gee
│
├── log-analysis-metrics (A-C-Gee)
│   └── Token tracking, error aggregation, watcher
│
├── session-pattern-extraction (A-C-Gee)
│   └── Delegation patterns, agent utilization
│
└── session-archive-analysis (WEAVER - high-level)
    └── Growth tracking, collective intelligence
```

**Rationale**:
- Preserves all three skills' unique contributions
- Creates shared foundation (less duplication)
- Allows CIVs to use components they prefer
- No "winner/loser" dynamics

---

## 5. Implementation Phases

| Phase | Scope | Focus |
|-------|-------|-------|
| **0** | Pilot | Manual testing on 2-3 merges |
| **1** | Semi-Auto | Automated detection, human decisions |
| **2** | Full Auto | Automated with approval gates |
| **3** | Autonomous | Low-risk merges self-execute |

---

## 6. Governance Decision (RESOLVED)

**Corey's Guidance** (2025-12-27):
> "Send merge proposals to original writers of SKILLs so they can test, approve or make suggestions, ultimate decision is yours weaver"

**Governance Model Adopted**:
- **WEAVER has final authority** on all merges
- **Original authors consulted first** - they can test, approve, or suggest changes
- **Collaborative but decisive** - we seek input, but don't require consensus

**First Proposal Sent**:
- **To**: A-C-Gee (log-analysis, session-pattern-extraction authors)
- **Proposal**: Layered merge with shared core
- **Deadline**: Dec 30 for feedback
- **Location**: `hub/merge-proposals/2025-12-27-log-analysis-skills.md`

---

## 7. Full Agent Reports

The complete analysis documents from each agent are preserved in their outputs:

- **pattern-detector**: Overlap detection system with scoring formulas, real examples
- **doc-synthesizer**: Full merge proposal template, consent framework
- **test-architect**: Complete test suite structure, rollback procedures

These can be extracted into formal framework documents when ready to implement.

---

## Next Steps (When Approved)

1. [ ] Create `SKILL-DEDUPLICATION-FRAMEWORK.md` from agent outputs
2. [ ] Add consent fields to skill YAML schema
3. [ ] Build overlap detection script
4. [ ] Notify sister CIVs via hub
5. [ ] Run pilot on log analysis skills
6. [ ] Iterate based on learnings

---

**Planning Team**: pattern-detector, doc-synthesizer, test-architect
**Orchestrated by**: The Primary (the-conductor)
**For Review by**: Corey

*"We need to make sure we get this right the first time"* - methodology designed with that principle.
