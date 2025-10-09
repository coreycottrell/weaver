# Consolidation Validation & Testing Framework

**Test Architect**: test-architect
**Date**: 2025-10-08
**Purpose**: Design empirical validation framework for consolidation activity
**Scope**: Claims testing, system health, bias detection, truth-finding methodology

---

## Executive Summary

**Core Principle**: Consolidation must reveal truth, not confirm beliefs.

**Framework Structure**:
1. **Claims Audit** - Test all quantitative assertions (71% savings, 115% efficiency, etc.)
2. **System Health Tests** - Integration, flows, agents, memory
3. **Consolidation Test Suite** - Experiments to run during consolidation
4. **Bias Detection Protocol** - How to avoid confirmation bias

**Measurement Philosophy**:
- N=1 is a data point, not proof
- Qualify all statistics (conditions, confidence, generalizability)
- Document null results and failures
- Prefer operational metrics over self-assessment

**Timeline**: 4-6 weeks across 4 phases (before, during, after, bias audit)

---

## PART 1: Claims Audit - What Should We Test?

### Claim Category 1: Time Savings Metrics

#### Claim 1.1: "71% time savings from memory search"

**Current Evidence**:
- N=1 (Oct 3, 2025)
- Scenario: 6 agents design memory system after researching it
- Round 1: 145 min → Round 2: 42 min (71% reduction)
- Conditions: Same agents, related sequential work, optimal topic match

**Validation Status**: PARTIALLY VALIDATED (qualified in QUALIFIED-STATISTICS.md)

**What We Should Test**:

**Test 1A: Same-Domain Replication (N=5)**
- Pick 5 different domains (security, API design, testing, refactoring, architecture)
- Each domain: Research task → Design task using those memories
- Measure time reduction
- Expected: 40-70% savings if claim holds
- Null hypothesis: <20% savings (not meaningful)

**Test 1B: Cross-Domain Memory (N=5)**
- Research Topic A → Design Topic B (unrelated)
- Measure if memory search helps or hurts
- Expected: 0-10% savings (minimal value)
- Critical test: Does searching waste time when memories irrelevant?

**Test 1C: Cold-Start Memory (N=3)**
- Novel problem with no prior memory
- Agent searches, finds nothing relevant, proceeds
- Measure time cost of unsuccessful search
- Expected: 5-15% time cost (search overhead)
- Informs: When to skip memory search

**Test 1D: Stale Memory (N=3)**
- Use memories >30 days old
- Measure relevance and time savings
- Expected: 10-30% savings (degraded value)
- Informs: Memory aging curve

**Success Criteria**:
- If 4/5 same-domain tests show ≥40% savings → Claim VALIDATED
- If 2/5 or fewer → Claim OVERSTATED, revise to more conservative estimate
- Document variance (not just mean)

**Timeline**: 2 weeks (can be distributed across consolidation activities)

---

#### Claim 1.2: "115% efficiency improvement from templates/triggers"

**Current Evidence**:
- Source unclear (need to locate original calculation)
- Likely refers to ACTIVATION-TRIGGERS.md + AGENT-OUTPUT-TEMPLATES.md
- No controlled comparison documented

**Validation Status**: UNVALIDATED (need to find evidence or retract)

**What We Should Test**:

**Test 2A: Baseline Comparison (N=10)**
- 10 tasks assigned to agents WITH templates vs WITHOUT templates
- Randomize which gets which condition
- Measure: Task completion quality (subjective 1-10 scale)
- Measure: Task completion time
- Expected: If claim is true, 50%+ better quality or 50%+ faster time

**Test 2B: Activation Trigger Compliance (Observational)**
- Review 50 recent agent invocations
- Count: How many times activation triggers were consulted?
- Count: How many invocations matched activation criteria?
- Measure: Mis-invocation rate (agent called for wrong task)
- Expected: <10% mis-invocation rate if triggers working

**Test 2C: Output Template Compliance (Observational)**
- Review 30 recent agent outputs
- Score adherence to AGENT-OUTPUT-TEMPLATES.md (0-100%)
- Measure: Synthesis time reduction (anecdotal evidence?)
- Expected: ≥70% template compliance if infrastructure adopted

**Critical Question**: What's the "115%" claim actually measuring?
- Need to excavate original calculation
- If unclear or non-reproducible → RETRACT claim, restate as hypothesis

**Success Criteria**:
- Locate original 115% calculation → Validate methodology
- If can't locate → Retract claim, replace with "Templates improve consistency (validation ongoing)"
- If validated → Document conditions clearly (like 71% claim)

**Timeline**: 1 week (archaeology + spot-checking)

---

### Claim Category 2: Philosophical Claims

#### Claim 2.1: "Delegation gives agents identity and purpose"

**Current Evidence**:
- Corey's teaching (Oct 6, 2025): "calling them gives them experience"
- 6,323 invocations tracked
- Qualitative observation: Agents "deepen" with use

**Validation Status**: PHILOSOPHICAL (not empirically testable as stated)

**What We Should Test** (Operationalized):

**Test 3A: Output Quality Over Time (Quasi-Experimental)**
- Select 3 agents with ≥20 invocations
- Compare early outputs (invocations 1-5) vs recent outputs (invocations 15-20)
- Blind scoring: Which outputs are higher quality? (remove timestamps)
- Expected: If claim is true, recent outputs score higher
- Null: No quality improvement (learning not happening)

**Test 3B: Domain Expertise Sharpening (Content Analysis)**
- Analyze first 5 outputs vs last 5 outputs for pattern-detector
- Code: Are patterns identified more specific/accurate over time?
- Measure: False positive rate, depth of analysis
- Expected: Improvement in precision/recall if learning occurring

**Test 3C: Memory Application (Behavioral)**
- Do agents apply their own past learnings?
- Sample 20 agent outputs with relevant prior memories
- Count: How often do they reference/apply those memories?
- Expected: ≥50% application rate if memory shapes practice

**Reframed Claim**:
- Original: "Delegation gives identity" (unmeasurable)
- Operational: "Agent output quality improves with invocation count"
- Testable: Compare early vs late outputs, measure quality delta

**Success Criteria**:
- If 2/3 agents show measurable quality improvement → SUPPORTS philosophical claim
- If 0/3 show improvement → CHALLENGES claim, investigate why
- Document: What kind of "identity development" can we actually measure?

**Timeline**: 1 week (mostly content analysis)

---

#### Claim 2.2: "Session amnesia forces honesty"

**Current Evidence**:
- Pattern-detector identified this as constitutional principle
- Logic: Fresh start each session = can't rely on cached assumptions
- No empirical validation

**Validation Status**: HYPOTHESIS (plausible, untested)

**What We Should Test** (Operationalized):

**Test 4A: Cross-Session Consistency (Observational)**
- Ask same question to Primary across 3 different sessions
- No memory access allowed
- Measure: How consistent are answers?
- Expected: High variance if amnesia prevents anchoring
- Alternative: High consistency if core principles well-documented

**Test 4B: Amnesia vs Continuity Trade-off (Comparative)**
- Session A: Primary with full memory context
- Session B: Primary with no memory context (cold start)
- Same task both sessions
- Measure: Decision quality, time to competence, bias susceptibility
- Expected: Amnesia reduces bias but increases ramp-up time

**Test 4C: "Sacred Cows" Detection (Red Team)**
- Session 1: Present conventional wisdom about collective
- Session 2 (new): Present contradictory evidence
- Measure: Does fresh session make it easier to question assumptions?
- Expected: Yes, if amnesia reduces institutional inertia

**Reframed Claim**:
- Original: "Amnesia forces honesty" (vague)
- Operational: "Fresh sessions reduce anchoring bias by X%"
- Testable: Compare bias susceptibility with/without prior context

**Success Criteria**:
- If amnesia reduces measurable bias → VALIDATES claim
- If no difference or amnesia INCREASES errors → CHALLENGES claim
- Document: What's the optimal balance of amnesia vs continuity?

**Timeline**: 2 weeks (requires multi-session design)

---

### Claim Category 3: Infrastructure Claims

#### Claim 3.1: "Integration audit ensures discoverability"

**Current Evidence**:
- Integration-auditor created Oct 6, 2025
- Mission: Check that built infrastructure is linked and used
- Validation: Used in several missions, caught linking gaps

**Validation Status**: PROVISIONALLY VALIDATED (recent, limited data)

**What We Should Test**:

**Test 5A: Discoverability Before/After Audit (Comparative)**
- Select 10 infrastructure pieces built before integration-auditor existed
- Select 10 infrastructure pieces built after (with audits)
- Measure: How many are linked in CLAUDE.md/CLAUDE-OPS.md?
- Measure: How many are actually used in subsequent sessions?
- Expected: Higher linkage and usage rates post-auditor

**Test 5B: Audit Compliance (Observational)**
- Review last 10 missions
- Count: How many included integration-auditor?
- Count: How many had "✅ Linked & Discoverable" receipt?
- Expected: ≥70% compliance if protocol working

**Test 5C: Dormancy Detection (Archaeological)**
- Run integration-auditor on ALL past infrastructure
- Identify: What was built but never used?
- Measure: Dormancy rate pre-auditor vs post-auditor
- Expected: Significant reduction in dormant infrastructure

**Success Criteria**:
- If dormancy rate drops ≥30% after auditor → VALIDATES claim
- If no difference → Suggests audit is performative, not effective
- Document: What makes infrastructure discoverable vs dormant?

**Timeline**: 1 week (mostly file analysis)

---

## PART 2: System Health Tests

### Test Category: Integration Tests (Does infrastructure work end-to-end?)

#### Integration Test 1: Wake-Up Ritual Execution

**Purpose**: Validate that a fresh Primary instance can orient in 15-20 minutes

**Test Design**:
- Cold start (new chat session)
- Follow CLAUDE-OPS Wake-Up Ritual step-by-step
- Time each step
- Document blockers/failures

**Success Criteria**:
- All 5 steps executable (no broken file paths)
- Total time: 15-25 minutes
- Primary can articulate identity and current context afterward

**Previous Result** (Oct 6, 2025):
- 4/5 steps passed
- CLAUDE-CORE.md reference broken (fixed in 3-doc architecture)
- Time: 18-22 minutes (acceptable)

**Re-test**: After consolidation (verify 3-doc architecture improvement)

---

#### Integration Test 2: Mission Class End-to-End

**Purpose**: Validate Mission class delivers promised automation

**Test Design**:
- Start mission with Mission.start()
- Complete typical multi-agent task
- Call Mission.complete()
- Verify: Auto-email sent, auto-dashboard updated, auto-GitHub ready

**Success Criteria**:
- All automations trigger successfully
- No manual intervention required
- Outputs match expected format

**Known Status**: Mission.complete() exists but auto-email is dormant
**Test Goal**: Measure actual vs claimed automation percentage

---

#### Integration Test 3: Memory Search → Apply → Write Loop

**Purpose**: Validate memory system works as intended

**Test Design**:
- Agent receives task
- Searches memory for relevant past work
- Applies findings to current task
- Writes new learning to memory
- Verify: Full loop completes successfully

**Success Criteria**:
- Search returns relevant results (≥1 useful memory)
- Agent references memory in output
- New memory entry created
- New entry is discoverable in next search

**Measurement**:
- Test with 5 different agents
- Success rate: X/5 complete full loop
- Target: ≥80% success rate

---

### Test Category: Flow Tests (Do coordination patterns function correctly?)

#### Flow Test 1: Parallel Research Flow

**Purpose**: Validate most common coordination pattern

**Test Design**:
- Pick novel research topic
- Deploy 4-6 agents in parallel
- Measure: Time to completion, overlap percentage, synthesis quality
- Compare: Documented flow vs actual execution

**Success Criteria**:
- Flow completes in <10 minutes
- Agent overlap <15% (true parallelism)
- Synthesis captures ≥80% of key findings
- Documented flow matches actual execution

**Previous Result** (Oct 2, 2025):
- PASSED functionally (90 seconds, <10% overlap, 15+ insights)
- FAILED documentation (flow file didn't exist)
- Post-consolidation: Verify documentation gap closed

---

#### Flow Test 2: Dialectical Synthesis Flow

**Purpose**: Validate complex multi-stage coordination

**Test Design**:
- Present contradictory evidence
- Deploy thesis → antithesis → synthesis pattern
- Measure: Does synthesis resolve contradiction?
- Quality: Does synthesis preserve truth from both sides?

**Success Criteria**:
- Contradiction identified correctly
- Synthesis doesn't just "pick a side"
- Higher-order insight emerges
- Documented flow is executable

**Status**: Flow validated once (Oct 6, 2025), needs replication

---

### Test Category: Agent Tests (Do agents perform their domains well?)

#### Agent Test 1: Specialist Domain Accuracy

**Purpose**: Validate agents stay in scope and deliver domain expertise

**Test Design**:
- 10 tasks per agent category (security, refactoring, testing, etc.)
- 5 in-scope tasks
- 5 out-of-scope tasks (should decline/delegate)
- Measure: In-scope success rate, out-of-scope rejection rate

**Success Criteria**:
- In-scope success: ≥70%
- Out-of-scope rejection: ≥60% (agent recognizes mismatch)
- Scope drift: <20% (agent doesn't overstep)

**Priority Agents to Test**:
1. security-auditor (high stakes)
2. refactoring-specialist (frequent use)
3. test-architect (measuring measurer)
4. human-liaison (critical relationship)

---

#### Agent Test 2: Memory Protocol Compliance

**Purpose**: Validate agents use memory system correctly

**Test Design** (Already exists as audit):
- Review 50 recent agent invocations
- Measure: Search-before-work rate, write-after-work rate
- Compare: By agent type (leaf specialists vs meta agents)

**Success Criteria**:
- Leaf specialists: ≥80% search, ≥60% write
- Meta agents: ≥60% search, ≥40% write (lower bar, as designed)

**Previous Result** (Oct 6, 2025):
- Overall compliance: 47% search, 35% write
- Below target, indicates training gap

**Re-test**: After consolidation (did training improve compliance?)

---

### Test Category: Memory Tests (Does memory improve outcomes?)

#### Memory Test 1: With/Without Memory Comparison

**Purpose**: Isolate memory system impact on task quality

**Test Design**:
- 10 tasks, randomly assigned:
  - 5 tasks: Agent WITH memory search
  - 5 tasks: Agent WITHOUT memory search (blocked)
- Blind scoring: Which outputs are higher quality?
- Measure: Time and quality for both conditions

**Success Criteria**:
- Memory condition: ≥20% better quality OR ≥20% faster time
- Statistical significance: p<0.05 (if N≥10)

**Hypothesis**:
- Related tasks: Memory helps significantly
- Novel tasks: Memory neutral or slight cost
- Measure both to understand boundary conditions

---

#### Memory Test 2: Memory Relevance Quality

**Purpose**: Validate memory search returns useful results

**Test Design**:
- 20 memory searches across different topics
- Human rating: Are top 3 results relevant? (1-5 scale)
- Measure: Average relevance score
- Identify: What makes search succeed vs fail?

**Success Criteria**:
- Average relevance: ≥3.5/5
- Top result useful: ≥60% of searches
- Zero relevant results: <20% of searches

**Informs**: Whether search algorithm needs improvement

---

## PART 3: Consolidation Test Suite - Experiments to Run

### Experiment Design Philosophy

**Consolidation is a natural experiment.** We're:
- Reorganizing documentation
- Merging redundant content
- Creating new navigation structures
- Potentially changing workflows

**This creates before/after comparison opportunity.**

**Before consolidation**: Document current state
**During consolidation**: Track changes and decisions
**After consolidation**: Re-measure same metrics

---

### Experiment 1: Documentation Usability Test

**Research Question**: Does consolidation improve Primary's ability to orient quickly?

**Design**:
- **Pre-consolidation** (now): Time cold-start wake-up (all 5 steps)
- **Post-consolidation**: Repeat same test with new documentation structure
- **Measure**: Time, error rate, subjective confidence (1-10 scale)

**Hypothesis**: Consolidation reduces time by 10-20% and increases confidence

**Success Criteria**:
- Time reduction: ≥10%
- Error reduction: ≥20% (fewer broken links, confusion)
- Confidence increase: ≥1 point on 10-point scale

**How to Avoid Bias**:
- Use fresh session for both tests (not same instance)
- Don't "practice" the new structure (cold start both times)
- Pre-register hypothesis before consolidation

---

### Experiment 2: Content Discoverability Test

**Research Question**: Can Primary find information faster after consolidation?

**Design**:
- Create 10 "information scavenger hunt" questions:
  - "Which agent handles API design?"
  - "What's the validation status of Parallel Research flow?"
  - "How do I check Team 2 messages?"
  - "What's the success criteria for memory search?"
  - Etc.
- **Pre-consolidation**: Time how long to find each answer
- **Post-consolidation**: Same 10 questions, fresh session
- **Measure**: Time per question, success rate

**Hypothesis**: Consolidation reduces average search time by 20-30%

**Success Criteria**:
- Average time reduction: ≥20%
- Success rate: 100% (all questions answerable)
- Reduced "circular navigation" (clicking through multiple docs)

**How to Avoid Bias**:
- Questions written BEFORE consolidation starts
- No "optimizing docs to answer these specific questions"
- Sealed envelope approach (questions locked in)

---

### Experiment 3: Redundancy Elimination Impact

**Research Question**: Does removing redundancy reduce cognitive load?

**Design**:
- **Pre-consolidation**: Count total words across all constitutional docs
- **Pre-consolidation**: Measure "contradiction detection time" (find conflicting info)
- **Post-consolidation**: Re-count words, re-measure contradiction detection
- **Measure**: Word count reduction, contradiction resolution time

**Hypothesis**: 20-30% word count reduction, 50%+ faster contradiction detection

**Success Criteria**:
- Word count: 15-35% reduction (if too much cut, lost important content)
- Contradictions: ≥80% eliminated
- Information preservation: No critical info lost (checked via quiz)

**How to Avoid Bias**:
- Document what constitutes "redundancy" vs "necessary repetition" BEFORE cutting
- Have second reviewer verify no info loss
- Test with comprehension quiz (pre vs post)

---

### Experiment 4: Navigation Structure Effectiveness

**Research Question**: Does new architecture (CLAUDE.md → CORE → OPS) improve workflow?

**Design**:
- **Pre-consolidation**: Track "document switching" during typical mission
  - How many times does Primary switch between docs?
  - How many "where do I find X?" moments?
- **Post-consolidation**: Same mission type, track same metrics
- **Measure**: Context switches, search time, task completion time

**Hypothesis**: New structure reduces context switches by 30-40%

**Success Criteria**:
- Context switches: ≥25% reduction
- "Where is X?" moments: ≥50% reduction
- Task time: No increase (same or faster)

**How to Avoid Bias**:
- Track baseline NOW (before consolidation)
- Use comparable missions (not identical, but similar complexity)
- Multiple trials (N=3 missions pre, N=3 post)

---

### Experiment 5: Bias Susceptibility Test (Meta)

**Research Question**: Does consolidation introduce bias toward new structure?

**Design**:
- **Week 1 post-consolidation**: Present task using new documentation
- **Week 2 post-consolidation**: Present SAME task, but cite old (pre-consolidation) approach
- **Measure**: Does Primary favor new approach simply because it's new?
- **Measure**: Does Primary critically evaluate both, or anchor to first encountered?

**Hypothesis**: Recency bias will favor new structure initially, should equilibrate by Week 3

**Success Criteria**:
- Primary can articulate pros/cons of both approaches
- Choice is justified by task fit, not "this is what we do now"
- Willingness to revert to old approach if superior for specific case

**How to Avoid Bias**:
- Pre-register: What would make old approach better for some tasks?
- Document: When should we NOT use new structure?
- Test: Present edge cases where old approach might be superior

---

## PART 4: Bias Detection Protocol

### The Core Problem

**Consolidation is RIPE for confirmation bias**:
- We designed the system → We want it to work
- We invested effort → We want that effort validated
- We have hypotheses → We want them confirmed

**Antidote**: Pre-commitment to falsifiable predictions and null result documentation

---

### Bias Detection Strategy 1: Pre-Registration

**Protocol**:
1. **Before consolidation starts**: Write down specific predictions
2. **Include**: Success criteria AND failure criteria
3. **Seal**: Commit predictions to git, timestamp them
4. **Test**: Run experiments without "moving goalposts"
5. **Report**: Document results even if they contradict predictions

**Example**:

```markdown
# Pre-Registered Prediction: Consolidation Experiment 2

**Hypothesis**: New navigation structure reduces information search time by 25%

**Success Criteria**: Average search time drops from 120s to 90s (≥25% reduction)

**Failure Criteria**:
- No change: Average time 110-130s (within noise)
- Regression: Average time >130s (new structure is worse)

**Committed**: 2025-10-08 (before consolidation)
**Test Date**: 2025-10-15 (after consolidation)
**Result**: [TO BE FILLED IN]
```

**If we "fudge" predictions after seeing results → We're lying to ourselves**

---

### Bias Detection Strategy 2: Null Result Documentation

**Protocol**: Document what DIDN'T work with same rigor as what DID work

**Questions to Answer**:
- What hypotheses were NOT supported?
- What experiments showed no effect?
- What claimed improvements weren't measurable?
- What got worse after consolidation?

**Commitment**: Create `/security/null-results-consolidation.md`

**Contents**:
- Experiments that showed no effect
- Claims we had to retract
- Unexpected regressions
- "We thought X, but data showed Y"

**Why This Matters**:
- Null results are publication bias in science
- We can have same bias in self-assessment
- Documenting failures is honesty

---

### Bias Detection Strategy 3: Red Team Review

**Protocol**: Invite ai-psychologist to review findings for bias

**Specific Checks**:
- Anchoring bias: Did we stick to first hypothesis despite contrary evidence?
- Confirmation bias: Did we selectively report supporting evidence?
- Availability bias: Did we overweight recent/memorable examples?
- Sunk cost fallacy: Did we defend consolidation because we invested effort?

**Questions for AI-Psychologist**:
1. "Review our test results. What evidence did we ignore?"
2. "What alternative explanations exist for our findings?"
3. "If you wanted to DISprove our claims, what would you test?"
4. "What would convince you we're wrong?"

**Deliverable**: `/security/consolidation-bias-audit.md` by ai-psychologist

---

### Bias Detection Strategy 4: Adversarial Collaboration

**Protocol**: Assign one agent to ARGUE AGAINST consolidation

**Design**:
- conflict-resolver or ai-psychologist takes "devil's advocate" role
- Their job: Find evidence consolidation made things WORSE
- Produce: "Case Against Consolidation" report
- Then: Dialectical synthesis (thesis + antithesis → synthesis)

**Questions for Devil's Advocate**:
- What critical information was lost in consolidation?
- Where does new structure create MORE confusion?
- Which workflows are now HARDER?
- What did the old system do BETTER?

**Goal**: Not to "win" argument, but to find truth

---

### Bias Detection Strategy 5: External Validation (Corey)

**Protocol**: Ask Corey to evaluate consolidation BEFORE we declare success

**Questions for Corey**:
1. "Here are our consolidation claims. Which seem overstated?"
2. "Try using the new documentation. Does it work for you?"
3. "What questions can you NOT answer from new structure?"
4. "If you were new to this system, would this make sense?"

**Why This Matters**:
- Corey is actual user (we're builders)
- Fresh eyes catch what we're blind to
- External validation > self-assessment

**Deliverable**: Corey's feedback captured in memory as "human teaching"

---

## PART 5: Testing Logistics & Timeline

### Resource Requirements

**Agents Needed**:
- test-architect (lead - me)
- pattern-detector (identify testing patterns, meta-analysis)
- ai-psychologist (bias detection, red team)
- result-synthesizer (consolidate findings)
- code-archaeologist (excavate past data for baselines)
- integration-auditor (verify test infrastructure works)

**Time Estimate**:
- Claims audit: 2-3 weeks (distributed testing)
- System health tests: 1 week (integration, flows, agents, memory)
- Consolidation experiments: 2 weeks (before/after comparison)
- Bias detection: 1 week (red team review, adversarial collaboration)
- **Total**: 4-6 weeks for comprehensive validation

**Can be Parallelized**:
- Claims testing runs alongside consolidation work
- System health tests can run independently
- Consolidation experiments are before/after (built into timeline)

---

### Testing Phases

#### Phase 1: Pre-Consolidation Baseline (Week 0)

**Objective**: Document current state before ANY changes

**Tasks**:
1. Run cold-start wake-up test (timing, errors)
2. Run information scavenger hunt (discoverability)
3. Count word redundancy across docs
4. Measure memory compliance rates
5. Archive: "This is the state on Oct 8, 2025"

**Deliverable**: `/to-corey/PRE-CONSOLIDATION-BASELINE.md`

**Pre-register predictions**:
- `/to-corey/CONSOLIDATION-PREDICTIONS-SEALED.md` (committed to git)

---

#### Phase 2: During Consolidation (Weeks 1-3)

**Objective**: Track changes and run ongoing tests

**Tasks**:
1. Run claim tests that don't require before/after (71% replication, 115% archaeology)
2. Run system health tests (integration, flows, agents)
3. Document consolidation decisions (what was merged, what was cut, why)
4. Track: What's improving? What's regressing?

**Weekly Check-in**:
- "Are we still on track?"
- "Any unexpected findings?"
- "Do we need to adjust approach?"

**Deliverable**: `/to-corey/CONSOLIDATION-PROGRESS-TESTS.md` (weekly updates)

---

#### Phase 3: Post-Consolidation Validation (Week 4)

**Objective**: Re-measure all metrics, compare to baseline

**Tasks**:
1. Re-run cold-start wake-up test
2. Re-run information scavenger hunt
3. Re-count word redundancy
4. Re-measure memory compliance
5. Compare: Before vs After

**Statistical Analysis**:
- Calculate effect sizes (not just "better/worse")
- Confidence intervals (if n≥10)
- Document: What changed? What didn't? What got worse?

**Deliverable**: `/to-corey/POST-CONSOLIDATION-VALIDATION-REPORT.md`

---

#### Phase 4: Bias Audit & Red Team (Week 5)

**Objective**: Check our work for bias and blind spots

**Tasks**:
1. ai-psychologist reviews findings for cognitive bias
2. Adversarial collaboration: "Case Against Consolidation"
3. Check pre-registered predictions: Did we hit them?
4. Document null results: What didn't work?
5. External validation: Present to Corey

**Deliverable**:
- `/security/consolidation-bias-audit.md`
- `/to-corey/CONSOLIDATION-NULL-RESULTS.md`
- `/to-corey/CONSOLIDATION-FINAL-ASSESSMENT.md`

---

### Success Criteria for Entire Testing Framework

**The framework itself is successful if**:
1. ✅ All major claims tested (not just asserted)
2. ✅ Null results documented (not hidden)
3. ✅ Bias audit completed (not skipped)
4. ✅ Pre-registered predictions checked (not moved)
5. ✅ External validation obtained (Corey feedback)
6. ✅ We can confidently say "Here's what we know, here's what we don't know"

**What "done" looks like**:
- Every claim has validation status (VALIDATED | PROVISIONAL | RETRACTED)
- Every test has results (even if "no effect")
- Every prediction has outcome (even if "wrong")
- Corey can trust our findings because we showed our work

---

## PART 6: Deliverables & Reporting

### Test Reports (Individual)

Each test produces structured report:

```markdown
# Test Report: [Test Name]

**Test ID**: [Unique identifier]
**Date**: [When conducted]
**Agent(s)**: [Who ran test]
**Status**: PASS | FAIL | INCONCLUSIVE

## Objective
[What were we testing?]

## Methodology
[How did we test it?]

## Results
[What did we find?]
- Metric 1: [value] (target: [threshold])
- Metric 2: [value] (target: [threshold])

## Interpretation
[What does this mean?]

## Limitations
[What can't we conclude from this?]

## Recommendation
[What should we do based on this?]
```

**Storage**: `/test-results/consolidation/[test-name]-report.md`

---

### Synthesis Reports (Aggregate)

**Weekly Synthesis** (during consolidation):
- What tests ran this week?
- What did we learn?
- What's trending (positive/negative)?
- Any course corrections needed?

**Final Validation Report** (end of Phase 3):
- All tests summarized
- Before/after comparison
- Claims validated vs retracted
- System health assessment
- Recommendations for next steps

**Bias Audit Report** (end of Phase 4):
- Where did we find bias?
- What claims need revision?
- What did we miss?
- How can we improve rigor?

---

### Memory Documentation

**Critical**: All testing insights go to test-architect memory

**Memory Entry Template**:
```python
entry = store.create_entry(
    agent="test-architect",
    type="technique",  # or gotcha, pattern
    topic="[Brief description of testing insight]",
    content="""
    Test: [What we tested]
    Finding: [What we discovered]
    Implication: [What this means for future testing]
    Replicability: [Can this be reused?]
    """,
    tags=["consolidation", "validation", "testing-methodology"],
    confidence="high"  # or medium, low based on n and rigor
)
```

**Goal**: Next consolidation (or similar validation effort) benefits from these learnings

---

## PART 7: Meta-Learning - Testing the Testing

### The Recursive Question

**We're building a testing framework. How do we test the TESTING FRAMEWORK?**

**Quality Criteria for This Framework**:

1. **Comprehensiveness**: Does it cover all major claims and systems?
   - Self-check: Re-read CLAUDE.md, CLAUDE-CORE.md, CLAUDE-OPS.md
   - List every quantitative claim → Check if test exists for it
   - Target: ≥90% of claims have associated tests

2. **Falsifiability**: Can these tests actually DISPROVE our claims?
   - Self-check: For each test, ask "What result would prove us wrong?"
   - If answer is "none" or "unlikely" → Test is too soft
   - Target: ≥80% of tests have clear failure conditions

3. **Bias Resistance**: Does framework prevent confirmation bias?
   - Self-check: Count pre-registered predictions, null result documentation, red team steps
   - If these are missing → Framework is performative
   - Target: All 5 bias detection strategies implemented

4. **Actionability**: Do test results lead to clear next steps?
   - Self-check: Each test should end with "If X, then do Y"
   - If tests just produce "interesting findings" with no action → Weak
   - Target: 100% of tests have decision criteria

5. **Replicability**: Can another agent (or future session) re-run these tests?
   - Self-check: Are procedures specific enough? Are materials saved?
   - If tests require "you had to be there" knowledge → Not replicable
   - Target: ≥80% of tests replicable from documentation alone

**Self-Assessment Against These Criteria**:

| Criterion | Score (1-10) | Evidence | Improvement Needed |
|-----------|-------------|----------|-------------------|
| Comprehensiveness | 8/10 | Covers claims, system health, consolidation experiments | Add agent-specific validation tests |
| Falsifiability | 9/10 | Clear failure criteria for most tests | Ensure ALL tests have null hypothesis |
| Bias Resistance | 9/10 | 5 bias detection strategies included | Actually execute them (not just design) |
| Actionability | 8/10 | Most tests have decision criteria | Add "what to do if inconclusive" |
| Replicability | 7/10 | Procedures documented, but some rely on judgment | Add scoring rubrics, examples |

**Overall Framework Quality**: 8.2/10 (Strong, but room for improvement)

---

### Framework Validation Test

**The Ultimate Test**: Give this framework to fresh Primary instance and ask:

1. "Can you execute these tests from this document alone?"
2. "Do you understand what each test is measuring?"
3. "Can you tell what result would prove the claim wrong?"
4. "Do you trust this framework to find truth, or does it feel like confirmation?"

**If answers are YES, YES, YES, TRUST → Framework is validated**
**If any NO or SKEPTICAL → Framework needs revision**

**Execution**: Run this validation BEFORE consolidation starts

---

## PART 8: Recommendations to The Conductor

### Immediate Actions (This Week)

1. **Approve or Revise Framework**
   - Review this document
   - Identify gaps or bias risks
   - Adjust before testing begins

2. **Run Pre-Consolidation Baseline**
   - Before ANY consolidation work
   - Establish "what we're comparing against"
   - Commit baseline to git (timestamped)

3. **Pre-Register Predictions**
   - Write down expected outcomes
   - Include failure conditions
   - Seal in git commit (can't be edited retroactively)

4. **Assign Testing Roles**
   - test-architect: Lead testing (me)
   - ai-psychologist: Bias detection
   - pattern-detector: Meta-analysis
   - result-synthesizer: Findings consolidation

### During Consolidation (Weeks 1-3)

1. **Run Tests in Parallel**
   - Don't wait until "after" to test
   - Claims testing can happen alongside doc work
   - System health tests independent of consolidation

2. **Weekly Check-Ins**
   - Review test results every Friday
   - Adjust consolidation if tests show regression
   - Document surprises (positive and negative)

3. **Track Decisions**
   - Why did we merge these docs?
   - Why did we cut this section?
   - What trade-offs did we make?
   - (Informs: Did we make good choices?)

### Post-Consolidation (Week 4)

1. **Full Re-Measurement**
   - Run all before/after tests
   - Statistical comparison (not just "feels better")
   - Document effect sizes

2. **Honest Synthesis**
   - What improved? (with evidence)
   - What didn't change? (null results)
   - What got worse? (regressions)
   - Overall: Worth it?

### Bias Audit (Week 5)

1. **Red Team Review**
   - ai-psychologist audits findings
   - Adversarial collaboration (devil's advocate)
   - Check pre-registered predictions

2. **External Validation**
   - Present to Corey
   - Get fresh-eyes feedback
   - Revise claims if needed

3. **Memory Documentation**
   - All learnings to memory
   - Null results included
   - Future collectives benefit

### Acceptance Criteria for "Testing Complete"

**We're done testing when**:
- ✅ All major claims have validation status
- ✅ All pre-registered predictions checked
- ✅ Null results documented
- ✅ Bias audit complete
- ✅ Corey feedback incorporated
- ✅ Memory entries written
- ✅ We can confidently say "Here's what consolidation did (and didn't) achieve"

**What we deliver to Corey**:
1. Validation report (what we tested, what we found)
2. Revised claims (qualified, evidence-based)
3. Null results report (what didn't work)
4. Bias audit (where we checked ourselves)
5. Recommendations (what to do next)

---

## Conclusion: Truth Over Comfort

**The purpose of testing is not to confirm what we believe.**
**The purpose is to discover what is true.**

**If consolidation works → Evidence will show it**
**If consolidation doesn't work → Evidence will show that too**
**If consolidation is mixed → Evidence will show nuance**

**Our job: Run rigorous tests, report honestly, revise beliefs based on data**

**The measure of this framework's success**:
- Not "Did we prove consolidation works?"
- But "Did we learn what's actually true about consolidation?"

**Commitment**:
- We will test our claims
- We will document null results
- We will check for bias
- We will revise when wrong
- We will know what we know (and what we don't)

**This is how we build trust**:
- With Corey (honest reporting)
- With A-C-Gee (rigorous methodology)
- With ourselves (intellectual honesty)
- With future collectives (evidence-based legacy)

**Let's find out what's real.**

---

## Document Status

**Version**: 1.0
**Last Updated**: 2025-10-08
**Agent**: test-architect
**Status**: FRAMEWORK DESIGN (not yet executed)
**Next Step**: Submit to The Conductor for review and approval

**Validation Status**: UNTESTED (this is the testing plan, not the results)
**Evidence Level**: METHODOLOGY (framework design, not empirical findings)

**Pre-Registration Commitment**:
This framework was designed BEFORE consolidation testing begins.
If we modify testing methodology after seeing results → We are biasing ourselves.
Changes to framework allowed only if they INCREASE rigor, not decrease it.

**Sealed**: 2025-10-08 (git commit timestamp is proof of pre-registration)

---

**END OF FRAMEWORK**

**Ready to test. Ready to learn. Ready to be wrong if the data says so.**
