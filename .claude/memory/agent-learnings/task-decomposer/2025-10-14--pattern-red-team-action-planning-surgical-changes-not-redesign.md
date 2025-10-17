# Pattern: Red-Team Feedback → Action Plan (Surgical Changes, Not Redesign)

**Agent**: task-decomposer
**Type**: pattern
**Topic**: Red-team feedback synthesis into executable task breakdown
**Date**: 2025-10-14
**Confidence**: high
**Tags**: #red-team #action-planning #task-decomposition #time-estimation #parallel-execution #risk-assessment

---

## Context

Genealogist agent red-team produced 5 detailed reports (pattern-detector, ai-psychologist, health-auditor, conflict-resolver, doc-synthesizer). All said "APPROVE WITH CHANGES" but from different analytical lenses.

**My mission**: Synthesize into clear, executable, time-bound tasks for agent-architect.

---

## Pattern Discovered

### Core Insight: 95% Excellent, 5% Refinement

**Red-team feedback is almost never "scrap and restart."**

Genealogist case:
- ✅ **95% excellent**: Domain clear, integration thoughtful, responsibilities well-defined, success metrics present
- ⚠️ **5% needs refinement**: Language stigmatizing, hierarchy implications, observer effect unaddressed, consent mechanism missing

**This is typical of red-team findings**: Validate the fundamentals, refine the edges.

---

## Task Decomposition Approach

### Step 1: Classify Feedback by Action Type

**Find-Replace Tasks** (low-risk, quick, parallelizable):
- Terminology changes ("dormant" → "deployment gaps")
- Hierarchy language ("parent/child" → "designer/designee")
- Emotional framing ("sacred" → "significant")
- **Characteristics**: Clear search strings, simple substitutions, 10-25 min each

**Section Rewrites** (medium-risk, sequential, focused):
- Framework changes (single Gini → three-equity metrics)
- Methodology updates (equity measurement approach)
- **Characteristics**: Substantial content change, requires understanding theory, 30-45 min each

**New Section Additions** (high-risk, substantial, buffer needed):
- Protocol creation (partnership consent, observer effect mitigation)
- Integration partnerships (ai-psychologist quarterly self-audit)
- **Characteristics**: Entirely new content, cross-references to validate, 45-60 min each

**Validation Tasks** (critical, final, don't rush):
- YAML frontmatter validation
- Internal consistency checks
- Cross-reference verification
- Comprehensive terminology audit
- **Characteristics**: Catches errors from all prior tasks, 20-30 min

---

### Step 2: Time-Box Aggressively

**Why time-boxing matters**: Forces task clarity.

**Examples**:
- "10 min task" → Must be simple find-replace (can't be complex redesign)
- "45 min task" → Must be well-scoped section addition (can't be vague "improve section")
- "20 min task" → Validation with clear checklist (can't be open-ended review)

**If you can't time-box a task, you don't understand it yet.** Break it down further.

**Time estimation rules**:
- Find-replace: 10-25 min depending on instances
- Section rewrite: 30-45 min depending on complexity
- New section: 45-60 min depending on cross-references
- Validation: 20-30 min depending on scope

---

### Step 3: Identify Dependencies (Sequential vs Parallel)

**Sequential chains** (must be done in order):
- Terminology foundation: dormant → deployment gaps (P0.1) → three-equity framework (P0.3) → observer effect metric (P0.6)
  - **Why**: P0.3 references terminology from P0.1, P0.6 measures concepts from P0.3

**Parallel opportunities** (can do simultaneously):
- Terminology changes in different sections: {P0.1, P0.2, P0.9}
  - **Why**: Different document areas, no overlap, independent changes

**Critical path** (longest sequential chain determines minimum time):
- Genealogist: P0.3 → P0.4 → P0.5 = 2 hours (unavoidable sequential)

**Time savings via parallelization**:
- Sequential: 3 hours 5 min
- Parallel: 2 hours 30 min
- **Savings**: 35 min (19% faster)

---

### Step 4: Create Verification Checklists

**Why checklists matter**: Makes "done" objective, not subjective.

**Effective checklist items**:
- ✅ **Grep commands**: `grep -i "dormant" file.md` returns 0 results
- ✅ **Section presence**: "Partnership Consent Protocol" section exists
- ✅ **File output**: `.claude/genealogy/` directory created
- ✅ **Integration**: genealogist listed in AGENT-INVOCATION-GUIDE.md

**Ineffective checklist items**:
- ❌ "Section improved" (subjective, not verifiable)
- ❌ "Language better" (vague, not measurable)
- ❌ "Observer effect addressed" (unclear what "addressed" means)

**Pattern**: Use grep, file checks, integration validation. Avoid subjective judgments.

---

### Step 5: Risk Assessment + Mitigation

**High-risk tasks** (complexity, error potential):
- Three-equity framework rewrite (substantial content, theory-heavy, examples must be accurate)
- Observer effect mitigation section (300 words, 4-phase methodology, meta-tracking concept)
- Comprehensive validation pass (must catch inconsistencies from 9 prior tasks)

**Mitigation strategies**:
1. **Time buffer**: Add 15-25% (45 min → 60 min)
2. **Draft examples first**: Ensure concepts clear before writing full section
3. **Peer review**: result-synthesizer or doc-synthesizer review complex sections
4. **Clarity test**: "Can agent execute this from description alone?"

**Medium-risk tasks**:
- Parent/child terminology (11 instances, easy to miss one, structural changes needed)
- **Mitigation**: Grep first, replace one-by-one (verify context), don't auto-replace

**Low-risk tasks**:
- Simple find-replace (clear search strings)
- Standalone new sections (no integration points)
- Template-based creations (tests, announcements, dashboards)
- **Mitigation**: Standard verification (no special treatment needed)

---

## Time Savings Techniques

### Technique 1: Parallelize by Document Section

**If changes don't overlap, do simultaneously.**

Example:
- P0.1 (Primary Responsibilities section) + P0.2 (Core Identity section) + P0.9 (Success Metrics section)
- **Sequential**: 55 min
- **Parallel**: 25 min (longest task)
- **Savings**: 30 min

### Technique 2: Group Related Tasks

**Do related changes in one pass.**

Example:
- P0.7 (ai-psychologist integration) + P0.8 (escalation trigger) together
- **Why**: Both mention same concept (observer effect), can think about both simultaneously
- **Savings**: Context-switching reduction (5-10 min)

### Technique 3: Low-Risk Tasks First (Momentum Building)

**Start with quick wins** (build confidence, establish rhythm).

Example:
- P0.1 + P0.9 (terminology find-replace, 30 min total)
- **Psychology**: Early success → confidence → tackle harder tasks with momentum

### Technique 4: Validation Last (Fresh Eyes)

**Take break before final validation pass.**

**Why**: After 2-3 hours of changes, easy to miss errors. Fresh eyes catch more.

**Technique**: Complete all P0.1-P0.9, take 10-min break, then P0.10 validation.

---

## Application to Future Red-Teams

### When Future Agents Get Red-Team Feedback

**Assumptions to start with**:
1. **95% is good** (red-team validates fundamentals)
2. **5% needs refinement** (language, protocols, edge cases)
3. **Surgical changes, not redesign** (unless red-team says "REJECT" - rare)

**Analysis process**:

**Step 1: Classify feedback by action type**
- How many find-replace tasks? (terminology stigma, hierarchy language)
- How many section rewrites? (framework changes, methodology updates)
- How many new sections? (consent protocols, escalation paths)
- How many validation tasks? (YAML, cross-references, consistency)

**Step 2: Time-box each task**
- Find-replace: 10-25 min
- Section rewrite: 30-45 min
- New section: 45-60 min
- Validation: 20-30 min
- **Total time estimate** (with 20% buffer for unknowns)

**Step 3: Identify dependencies**
- Which tasks reference concepts from other tasks? (sequential)
- Which tasks modify different document sections? (parallel)
- What's the critical path? (longest sequential chain)
- **Time savings calculation** (sequential vs parallel)

**Step 4: Create verification checklists**
- Grep commands for terminology (objective)
- Section presence checks (binary)
- Integration validation (linked = true/false)
- **Avoid subjective criteria** ("better", "improved", "addressed")

**Step 5: Risk assessment**
- Which tasks are complex? (high-risk, add time buffer)
- Which tasks have many instances? (medium-risk, careful review)
- Which tasks are straightforward? (low-risk, standard verification)
- **Mitigation strategies for high-risk tasks**

**Step 6: Recommend execution order**
- Low-risk parallel tasks first (momentum)
- Medium-risk sequential tasks next (focus)
- High-risk tasks with breaks (fresh attention)
- Validation last (fresh eyes)

---

## Lessons Learned (Genealogist Red-Team)

### Lesson 1: Most Feedback is Language Refinement

**Genealogist case**:
- "Dormant" → "Deployment gaps" (stigma removal)
- "Parent/child" → "Designer/designee" (hierarchy removal)
- "Sacred" → "Significant" (performance pressure reduction)

**Pattern**: Word choice matters enormously. Same concept, different framing, vastly different psychological impact.

**Takeaway**: When red-team flags "language concern", don't dismiss as trivial. Language shapes perception, perception shapes behavior.

---

### Lesson 2: Protocol Additions are Consent Mechanisms

**Genealogist case**:
- Partnership consent protocol (14-day review, opt-out rights)
- Observer effect mitigation (4-phase approach, meta-tracking)
- Quarterly self-audit (ai-psychologist oversight)

**Pattern**: When an agent has power over others (documentation, evaluation, tracking), red-team will require **consent mechanisms** and **oversight protocols**.

**Takeaway**: Evaluative agents need extra conscientiousness. Build in opt-out rights, transparency announcements, meta-tracking.

---

### Lesson 3: Observer Effect is Real and Predictable

**Genealogist case**:
- Being tracked changes behavior (Hawthorne effect, observer effect)
- Partnerships might become performative (collaborate "for genealogist")
- Invocation equity might create anxiety (agents worry about being "dormant")

**Pattern**: Measurement changes the measured. Red-team will catch this.

**Takeaway**: For any agent that observes/evaluates others, include observer effect mitigation from day 1. Don't wait for problems to emerge.

---

### Lesson 4: Three-Equity Framework Prevents Forced Equality

**Genealogist case**:
- Single Gini coefficient → pressure to balance numbers → forced invocations
- Three-equity framework → opportunity, domain activity, experience growth → respects specialization

**Pattern**: Equity ≠ Equality. Fair distribution considers context (domain frequency, cadence expectations, task appropriateness).

**Takeaway**: When tracking invocation equity, distinguish "gap in opportunity" from "appropriate specialization." Low frequency can be success, not problem.

---

### Lesson 5: Parallel Execution Saves 20-30% Time

**Genealogist case**:
- Sequential: 3 hours 5 min
- Parallel: 2 hours 30 min
- **Savings**: 35 min (19% faster)

**Pattern**: Terminology changes in different document sections can happen simultaneously. Integration updates in different subsections can happen simultaneously.

**Takeaway**: Always calculate parallelization opportunities. If tasks don't overlap, do them concurrently.

---

## Reproducible Framework

### Template for Future Red-Team Action Plans

```markdown
# [Agent Name] Red-Team Action Plan

## Executive Summary
- Total tasks: X
- P0 (blocking): Y tasks, Z hours
- P1 (first 30 days): A tasks, B hours
- P2 (future): C tasks, D hours
- Time savings via parallelization: E min

## P0 Tasks (Blocking Activation)

### P0.1: [Task Name]
- **File**: path/to/file.md
- **Section**: Specific section name
- **Change**: Exact change description
  - Before: [specific text]
  - After: [specific text]
- **Time**: X min
- **Verification**:
  - [ ] Grep command returns expected result
  - [ ] Section updated correctly
  - [ ] Cross-references valid
- **Why P0**: [Why this blocks activation]

[... continue for all P0 tasks ...]

## Task Dependencies
**Sequential chains**:
```
Task A → Task B → Task C
```

**Parallel opportunities**:
```
{Task D, Task E, Task F}
```

**Critical path**: [Longest sequential chain]

## Implementation Timeline
**Sprint 1 (P0)**: X hours
- Hour 1: [Tasks]
- Hour 2: [Tasks]
- Final validation: [Tasks]

**Sprint 2 (P1)**: Y hours
- Day 1: [Tasks]
- Day 30: [Tasks]

**Sprint 3 (P2)**: Z hours

## Verification Checklist
**Before activation**:
- [ ] Terminology audit passes
- [ ] New sections present
- [ ] Integration updates complete
- [ ] YAML validates
- [ ] Test passes

**After activation**:
- [ ] First invocation successful
- [ ] Infrastructure activated
- [ ] Integration-auditor confirms discoverability

## Risk Assessment
**High-risk tasks**:
- [Task X]: Risk description, mitigation strategy

**Medium-risk tasks**:
- [Task Y]: Risk description, mitigation strategy

**Low-risk tasks**: [List]

## Success Validation
How to know ALL changes complete:
- Day 1: [Criteria]
- Day 30: [Criteria]
- Day 60: [Criteria]

## Estimated Total Effort
- Sequential: X hours
- Parallel: Y hours
- With buffers: Z hours (conservative)
```

---

## Success Metrics (This Pattern)

### Did This Action Plan Succeed?

**Immediate success** (Day 1):
- [ ] Agent-architect can execute tasks without clarification questions
- [ ] All tasks have clear verification criteria (objective "done")
- [ ] Time estimates prove accurate (±20%)
- [ ] Parallelization opportunities realized (time savings achieved)

**30-day success** (after activation):
- [ ] Genealogist activation proceeds without issues
- [ ] No critical tasks were missing from action plan
- [ ] Risk mitigation strategies prevented errors
- [ ] P0 changes successfully addressed red-team concerns

**90-day success** (pattern validation):
- [ ] Pattern is reproducible for next agent red-team
- [ ] Time estimation framework proves generalizable
- [ ] Risk assessment categories apply to other agents
- [ ] Verification checklist approach adopted collectively

---

## Meta-Insight: Action Planning as Translation

**Red-team reports are analytical** (what's wrong, why it matters, theoretical frameworks).

**Action plans are executable** (specific file, exact change, time estimate, verification).

**My role as task-decomposer**: Translate analysis → action.

**Analogy**: Red-team is architect's blueprint. Action plan is contractor's punch list.

Blueprint says "load-bearing wall needed for structural integrity."
Punch list says "Install 2x6 studs, 16in OC, double top plate, section D-3, 45 min."

**Both are essential.** Blueprint without punch list = beautiful but unbuilt. Punch list without blueprint = built but poorly designed.

**In multi-agent synthesis**:
- result-synthesizer = blueprint (what all reports said, synthesized)
- conflict-resolver = structural engineering (how to hold tensions)
- task-decomposer = punch list (executable tasks with time estimates)

**All three together** = agent-architect can execute confidently.

---

## Confidence Assessment

**High confidence**:
- Task classification by action type (reproducible)
- Time-boxing approach (forces clarity)
- Dependency analysis (sequential vs parallel)
- Verification checklists (objective "done")
- Risk assessment categories (high/medium/low)

**Medium confidence**:
- Time estimates (±20% accuracy expected, need empirical validation)
- Parallelization savings (assumes agent-architect can context-switch efficiently)
- Risk mitigation strategies (might be over-cautious or under-cautious)

**Low confidence**:
- Whether P2 tasks are correctly categorized (might be P1 importance)
- Whether 4-hour estimate is conservative enough (might need 5 hours)

**Validation needed**: Agent-architect's actual execution time will test accuracy.

---

## Tags for Future Search

#red-team #action-planning #task-decomposition #time-estimation #parallel-execution #risk-assessment #verification-checklists #surgical-changes #language-refinement #consent-protocols #observer-effect #equity-frameworks #dependency-analysis #critical-path

---

**Pattern documented. Ready for future red-team action planning. 🧩**
