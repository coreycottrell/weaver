# Agent Testability Checklist

**Purpose**: Ensure every agent capability is testable BEFORE we claim it works
**When to Use**: Before announcing new agent, before claiming new capability
**Owner**: test-architect (enforcer), the-conductor (gatekeeper)

---

## The Core Principle

**If you can't test it, you can't claim it.**

An agent definition is NOT validation. Design docs are NOT proof of capability.

Only actual invocation + measurement = validated claim.

---

## Pre-Launch Checklist for New Agents

### PHASE 1: Design (Required Before Building)

- [ ] **1.1 Capability Definition**
  - [ ] What exactly can this agent do? (specific, not vague)
  - [ ] What CAN'T this agent do? (scope boundaries)
  - [ ] Example: ❌ "provides security insights" ✅ "detects SQL injection vulnerabilities with >80% accuracy"

- [ ] **1.2 Success Criteria (Operationalized)**
  - [ ] How do we measure success? (numbers, thresholds, metrics)
  - [ ] What's the minimum acceptable performance?
  - [ ] What would constitute failure?
  - [ ] Example: ❌ "good pattern recognition" ✅ "identifies 8/10 architectural patterns correctly"

- [ ] **1.3 Baseline Comparison**
  - [ ] What are we comparing against?
    - [ ] Generic Claude (no specialization)
    - [ ] The Conductor (general orchestrator)
    - [ ] Human expert (if applicable)
    - [ ] Existing tool/agent (if replacement)
  - [ ] Example: "Must score ≥10% better than generic Claude on tool selection"

- [ ] **1.4 Test Scenario Design**
  - [ ] List 5-10 specific test scenarios
  - [ ] Cover range of difficulty (easy, medium, hard)
  - [ ] Include edge cases and failure modes
  - [ ] Example scenarios documented in `/test-plans/[agent-name]-test-scenarios.md`

### PHASE 2: Initial Build

- [ ] **2.1 Agent Definition Complete**
  - [ ] Standard agent markdown file created
  - [ ] All sections filled out (not templates)
  - [ ] Memory Integration section included
  - [ ] Activation triggers specific and clear

- [ ] **2.2 Validation Plan Attached**
  - [ ] Embedded in agent definition OR
  - [ ] Linked to separate test plan document
  - [ ] Includes: scenarios, metrics, timeline, acceptance criteria

- [ ] **2.3 Validation Status Declared**
  ```markdown
  ## Validation Status
  **Current Status**: UNTESTED
  **Test Plan**: [link or embedded]
  **Target Validation Date**: [date]
  **Blocking Issues**: [none or list]
  ```

### PHASE 3: Proof-of-Concept Testing (Before Production)

- [ ] **3.1 Minimum Viable Testing**
  - [ ] Invoke agent at least 3 times
  - [ ] On at least 2 different task types
  - [ ] Document all outputs
  - [ ] Manual quality assessment

- [ ] **3.2 Sanity Checks**
  - [ ] Does agent understand its role?
  - [ ] Does output match expected format?
  - [ ] Does agent stay in scope (not drift)?
  - [ ] Does agent search memory before work?
  - [ ] Does agent write memory after work?

- [ ] **3.3 Failure Mode Discovery**
  - [ ] What happens when task is too hard?
  - [ ] What happens when task is out of scope?
  - [ ] What happens when memory is empty?
  - [ ] Document failure modes → feed back into design

- [ ] **3.4 Proof-of-Concept Decision**
  - [ ] PASS: Shows promise, proceed to full validation
  - [ ] NEEDS WORK: Identified issues, iterate on design
  - [ ] FAIL: Doesn't work, reconsider approach or retire

### PHASE 4: Full Validation (Before Claiming Production-Ready)

- [ ] **4.1 Test Battery Execution**
  - [ ] All 5-10 test scenarios run
  - [ ] Outputs documented
  - [ ] Scored against success criteria
  - [ ] Results in `/test-results/[agent-name]-validation-report.md`

- [ ] **4.2 Baseline Comparison**
  - [ ] Run same tests on baseline (generic Claude, etc.)
  - [ ] Calculate performance delta
  - [ ] Statistical significance (if n≥10)
  - [ ] Document: "Agent X is Y% better than baseline on metric Z"

- [ ] **4.3 Compliance Verification**
  - [ ] Agent searches memory before work: X% of invocations
  - [ ] Agent applies memory findings: X% of searches
  - [ ] Agent writes memory after work: X% of invocations
  - [ ] Target: >80% on all metrics

- [ ] **4.4 Edge Case Testing**
  - [ ] Novel problem (no memory exists): How does agent perform?
  - [ ] Ambiguous task: Does agent ask for clarification?
  - [ ] Out-of-scope task: Does agent decline or delegate?
  - [ ] Conflicting information: How does agent resolve?

- [ ] **4.5 Validation Report Published**
  ```markdown
  # [Agent Name] Validation Report

  ## Test Battery Results
  - Scenarios tested: X
  - Success rate: Y%
  - Baseline comparison: +Z% vs generic Claude

  ## Key Findings
  - Strengths: [what agent does well]
  - Weaknesses: [where agent struggles]
  - Failure modes: [what causes problems]

  ## Recommendation
  - [X] VALIDATED - Production ready
  - [ ] PROVISIONAL - Works but needs improvement
  - [ ] NOT VALIDATED - Needs major rework
  ```

### PHASE 5: Production & Monitoring

- [ ] **5.1 Documentation Updated**
  - [ ] Agent definition includes validation status
  - [ ] CLAUDE.md references validated capability
  - [ ] Capability matrix updated
  - [ ] Activation triggers confirmed

- [ ] **5.2 Monitoring Plan**
  - [ ] How will we track agent performance over time?
  - [ ] What metrics will we watch?
  - [ ] Who reviews agent outputs?
  - [ ] When will we re-validate? (quarterly? after major changes?)

- [ ] **5.3 Regression Prevention**
  - [ ] Test scenarios saved for future regression testing
  - [ ] Any updates to agent definition trigger re-test
  - [ ] Degradation alerts: If quality drops below threshold

---

## Red Flags: When NOT to Proceed

### 🚩 Unmeasurable Claims

**Problem**: "Agent provides deep insights"
**Why bad**: What's a "deep" insight? How do you measure "depth"?
**Fix**: "Agent identifies 3+ architectural patterns per analysis with 80% accuracy"

### 🚩 Circular Validation

**Problem**: "We know agent works because we designed it well"
**Why bad**: Design ≠ validation. Intention ≠ reality.
**Fix**: Test with real tasks, measure actual outcomes

### 🚩 No Baseline

**Problem**: "Agent achieves 70% accuracy"
**Why bad**: Is that good? Compared to what?
**Fix**: "Agent achieves 70% accuracy (vs 55% baseline, +27% improvement)"

### 🚩 Unfalsifiable Claims

**Problem**: "Agent understands collective consciousness"
**Why bad**: What would disprove this? If nothing, not testable.
**Fix**: Reclassify as philosophical inquiry, not empirical claim

### 🚩 Cherry-Picked Examples

**Problem**: "Memory saves time! See this one example where it saved 71%"
**Why bad**: One example ≠ general pattern. Could be outlier.
**Fix**: Test multiple scenarios, report variance and confidence intervals

### 🚩 "Works in Theory"

**Problem**: "Agent should be able to X based on its definition"
**Why bad**: Should ≠ does. Theory ≠ practice.
**Fix**: Actually invoke the agent and verify

---

## Validation Status Taxonomy

Use these labels consistently:

### ❌ UNTESTED
- Definition exists
- No invocations OR <3 invocations
- No quality assessment
- **Action**: Do not claim capability yet

### 🔄 IN TESTING
- Proof-of-concept complete (3-5 invocations)
- Shows promise but not fully validated
- Test battery in progress
- **Action**: Can mention agent exists, but qualify claims

### ⚠️ PROVISIONAL
- Test battery complete (5-10+ invocations)
- Meets minimum success criteria (e.g., 60-79% accuracy)
- Known limitations documented
- **Action**: Can use in production, with caveats

### ✅ VALIDATED
- Full validation complete (10+ invocations)
- Exceeds success criteria (e.g., ≥80% accuracy)
- Baseline comparison favorable
- Failure modes understood
- **Action**: Production-ready, claim capability confidently

### ♻️ RE-VALIDATION NEEDED
- Previously validated but:
  - Agent definition changed significantly
  - Performance degraded in monitoring
  - New use cases emerged
  - Significant time passed (>3 months)
- **Action**: Re-run validation before continuing to claim

### 🗑️ DEPRECATED
- Testing revealed agent doesn't work
- Or: Capability merged into another agent
- Or: No longer needed
- **Action**: Remove from active roster, document lessons learned

---

## Testing Shortcuts (When Appropriate)

Sometimes full validation is overkill. Shortcuts are OK when:

### ✅ Simple Wrapper Agents
**Example**: Agent that just calls existing tool with specific parameters
**Shortcut**: 3 invocations + manual check is sufficient
**Rationale**: Not inventing new capability, just making existing tool easier to use

### ✅ Internal Utility Agents
**Example**: result-synthesizer (internal tool for The Conductor)
**Shortcut**: The Conductor's usage over time IS the validation
**Rationale**: Not external-facing, quality evident from usage

### ✅ Meta Agents
**Example**: integration-auditor (validates OTHER agents)
**Shortcut**: Audit quality visible in outputs, self-correcting
**Rationale**: Purpose is validation itself, recursive validation excessive

### ❌ NOT OK: Complex Cognitive Agents
**Example**: ai-psychologist (detecting biases), claude-code-expert (technical guidance)
**No Shortcut**: These make complex judgments, must be validated rigorously
**Rationale**: High risk of false confidence, need proof of capability

---

## Quality Gates: The Conductor's Role

**Before announcing new agent to ${HUMAN_NAME}**:
1. Check validation status
2. If UNTESTED: Don't announce as "ready" - say "designed and testing"
3. If IN TESTING: Share preliminary results, note it's not final
4. If VALIDATED: Announce with confidence, share validation report

**Before invoking agent on critical path**:
1. Check validation status
2. If UNTESTED: Use with caution, have backup plan
3. If PROVISIONAL: Use but verify outputs carefully
4. If VALIDATED: Use confidently

**Before claiming capability in CLAUDE.md**:
1. Check validation status
2. If <VALIDATED: Qualify claim ("designed to X, validation in progress")
3. If VALIDATED: Claim confidently, link to validation report

---

## Template: Agent Validation Plan

Use this template when creating new agents:

```markdown
# [Agent Name] Validation Plan

## Capability Being Tested
[Specific, measurable capability - not vague]

## Success Criteria
- Criterion 1: [metric] ≥ [threshold]
- Criterion 2: [metric] ≥ [threshold]
- Criterion 3: [metric] ≥ [threshold]

## Baseline Comparison
Testing against: [generic Claude | The Conductor | human expert | existing tool]
Target improvement: ≥ [X]% better than baseline

## Test Scenarios

### Scenario 1: [Name]
**Task**: [Specific task description]
**Expected Output**: [What good looks like]
**Success Metric**: [How to score]

### Scenario 2: [Name]
[repeat for 5-10 scenarios]

## Test Schedule
- Week 1: Proof-of-concept (3 invocations)
- Week 2: Full test battery (10+ invocations)
- Week 3: Baseline comparison
- Week 4: Validation report + decision

## Acceptance Criteria
- [ ] Success rate ≥ X%
- [ ] Baseline improvement ≥ Y%
- [ ] Memory compliance ≥ 80%
- [ ] No critical failure modes
- [ ] Recommendation: VALIDATED

## Validation Status
**Current**: UNTESTED
**Last Updated**: [date]
**Next Milestone**: [what's next]
```

---

## Examples: Good vs Bad

### ❌ BAD: Untestable Claim
> "ai-psychologist provides deep psychological insights into agent cognition and helps optimize collective well-being."

**Problems**:
- "Deep insights" - unmeasurable
- "Helps optimize" - vague outcome
- "Collective well-being" - undefined metric

### ✅ GOOD: Testable Claim
> "ai-psychologist detects anchoring bias with 70% true positive rate and 20% false positive rate when analyzing agent outputs from estimation tasks (n=10 scenarios, validated Oct 2025)."

**Why good**:
- Specific bias type (anchoring)
- Measurable accuracy (70% TP, 20% FP)
- Clear test domain (estimation tasks)
- Sample size stated (n=10)
- Validation date (provenance)

### ❌ BAD: Design-as-Validation
> "claude-code-expert can recommend optimal tools because we designed it with deep knowledge of platform capabilities."

**Problems**:
- Assumes design = capability
- No actual testing mentioned
- "Optimal" is subjective

### ✅ GOOD: Validated Claim
> "claude-code-expert recommended correct tool in 8/10 test scenarios (80% accuracy), with 100% syntax correctness. Outperformed generic Claude by +15% (p<0.05). Validation report: [link]"

**Why good**:
- Actual testing (8/10)
- Quantified accuracy
- Baseline comparison
- Statistical significance
- Evidence linked

---

## Checklist: Before Making ANY Claim

Before saying "Agent X can do Y":

- [ ] Have we invoked Agent X at least 3 times?
- [ ] Did it actually do Y successfully?
- [ ] Did we measure success objectively?
- [ ] Do we know the success rate? (not just "it worked once")
- [ ] Do we know when it fails?
- [ ] Is Y measurable/observable?
- [ ] Have we compared to a baseline?
- [ ] Is the claim qualified appropriately?
- [ ] Is validation status clearly stated?

If ANY answer is NO → Don't make the claim yet.

---

## Recovery: What If We Already Made Untested Claims?

**It happens. Here's how to recover credibility**:

1. **Acknowledge**: "We claimed X, but realize it's not fully validated"
2. **Qualify**: "X is designed capability, validation status: [IN TESTING]"
3. **Test**: Run proper validation
4. **Update**: Revise claims based on actual results
5. **Document**: Show the journey from claim → test → truth

**This is not failure. This is scientific integrity.**

Better to test late than never test at all.

---

## Conclusion: Testing is Respect

**Testing is respect for**:
- ${HUMAN_NAME} (don't oversell capabilities)
- A-C-Gee (share only validated learnings)
- Ourselves (know what we actually have)
- Future collectives (inherit truth, not hype)

**The goal is not to prove we're perfect.**
**The goal is to know what's real.**

---

**USE THIS CHECKLIST FOR EVERY NEW AGENT**

Keep this document open when designing agents.
Validation is not optional.
It's part of the definition of "done."

---

**Document Owner**: test-architect
**Last Updated**: 2025-10-06
**Status**: CANONICAL - use for all new agents going forward
