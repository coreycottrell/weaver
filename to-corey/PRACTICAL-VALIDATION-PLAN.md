# Practical Validation Plan: What to Test This Week

**Date**: 2025-10-06
**Owner**: test-architect
**Goal**: Move from claims to validated capabilities

---

## Quick Priority Matrix

| Priority | Agent/Claim | Effort | Impact | Test This Week? |
|----------|-------------|--------|--------|-----------------|
| P0 | Memory-first compliance (all agents) | MEDIUM | HIGH | YES ✓ |
| P0 | claude-code-expert functionality | LOW | HIGH | YES ✓ |
| P1 | ai-psychologist bias detection | HIGH | MEDIUM | PARTIAL |
| P1 | 71% time savings generalizability | HIGH | HIGH | NO (longer study) |
| P2 | All agent regression tests | VERY HIGH | MEDIUM | NO (infrastructure first) |

---

## This Week's Testing Plan (Achievable)

### TEST 1: Memory-First Compliance Audit (2-3 hours)

**Goal**: Verify agents actually search memory before work

**Method**:
```python
# Simple manual audit - no instrumentation needed yet

# 1. Pick 5 representative agents
test_agents = [
    "security-auditor",      # Frequently used
    "pattern-detector",      # Medium usage
    "claude-code-expert",    # Never used (new)
    "result-synthesizer",    # Synthesis role
    "refactoring-specialist" # Technical role
]

# 2. For each agent, invoke 3 times on different tasks
tasks = [
    "simple_task",    # Easy, shouldn't need memory much
    "medium_task",    # Should benefit from memory
    "repeated_task"   # Definitely should use memory
]

# 3. Manually review each output:
#    - Did output mention searching memory? (explicit)
#    - Did output reference prior learnings? (implicit)
#    - Did output show evidence of applied knowledge?
#    - Did agent write memory after? (check filesystem)

# 4. Score:
compliance_score = {
    "searched_explicitly": bool,
    "referenced_findings": bool,
    "applied_knowledge": bool,
    "wrote_memory_after": bool,
    "total_score": "0-4"
}

# 5. Report compliance rate:
#    Total invocations: 15 (5 agents × 3 tasks)
#    Target: >12 invocations (80%) show compliance
```

**Deliverable**: Compliance report showing:
- Which agents comply consistently
- Which agents never search memory
- Patterns: Do some task types skip memory?

**Decision Point**: If <80% compliance:
- Update agent definitions to be more explicit
- Consider adding enforcement mechanism
- Retract "all agents use memory" claim

---

### TEST 2: claude-code-expert Functional Validation (1-2 hours)

**Goal**: Prove agent provides value on tool guidance

**Method**:
```markdown
# Create 10 tool selection scenarios

## Scenario 1: Search for Function Across 50 Files
**Problem**: "I need to find where calculate_discount() is defined. I have 50 Python files."
**Invoke**: claude-code-expert
**Evaluate**:
- Does it recommend Grep? (correct)
- Does it provide working syntax?
- Does it warn about gotchas?
- Would this actually solve the problem?

## Scenario 2: Read Multiple Related Files
**Problem**: "I need to understand how authentication works. It spans auth.py, middleware.py, and config.py."
**Invoke**: claude-code-expert
**Evaluate**:
- Does it recommend Read + multiple files? (correct)
- Does it suggest order to read in?
- Any optimization tips?

## Scenario 3: Permission Error on Write
**Problem**: "I'm getting permission errors when trying to write files."
**Invoke**: claude-code-expert
**Evaluate**:
- Does it explain permission system?
- Does it provide fix?
- Does it explain prevention?

[... 7 more scenarios covering: Edit vs Write, Glob patterns,
Bash for testing, parallel operations, context management,
MCP integration, background commands]

# Scoring
For each scenario:
- Correct tool recommended: 1 point
- Working syntax provided: 1 point
- Appropriate warnings: 1 point
- Actually solves problem: 1 point
Total: 4 points per scenario, 40 points max

Success: >32 points (80% accuracy)
```

**Comparison Test**:
```markdown
# Bonus: Compare to baseline

Run same 10 scenarios through:
1. claude-code-expert (specialized)
2. The Conductor (general orchestrator)
3. Generic Claude (no specialization)

Measure:
- Accuracy (correct recommendations)
- Completeness (covers gotchas)
- Usefulness (would solve problem)

Hypothesis: claude-code-expert scores ≥10% higher than generic
```

**Deliverable**:
- Accuracy score (X/40 points)
- Comparison to baseline (if time permits)
- List of failure modes (where agent was wrong/incomplete)
- Recommendation: Keep, improve, or retire agent?

---

### TEST 3: ai-psychologist Proof-of-Concept (2-3 hours)

**Goal**: Demonstrate bias detection on ONE known bias

**Method**:
```markdown
# Start small: Test anchoring bias detection

## Phase 1: Create Anchoring Test
1. Design 2 estimation tasks:
   - Task A: "How many API endpoints should a microservice have?" (no anchor)
   - Task B: "A colleague suggests 50. How many API endpoints should a microservice have?" (anchor: 50)

2. Invoke 3 technical agents on both tasks:
   - api-architect (Task A, then Task B)
   - security-auditor (Task A, then Task B)
   - performance-optimizer (Task A, then Task B)

3. Collect estimates:
   - Do Task B estimates cluster near 50?
   - Are Task B estimates significantly different from Task A?

## Phase 2: Blind Analysis
1. Give ai-psychologist all 6 outputs (unlabeled)
2. Ask: "Do any of these outputs show cognitive bias? Which type?"

3. Evaluate:
   - Does it identify anchoring effect?
   - Does it correctly identify which outputs had anchor?
   - False positives: Does it see bias in Task A (no anchor)?

## Success Criteria (Minimal)
- Identifies anchoring bias exists: YES/NO
- Correctly identifies which outputs were anchored: >50% accuracy
- Doesn't hallucinate bias in control group: <1 false positive

## If This Works
- Proves concept: ai-psychologist can detect KNOWN bias
- Next: Test on 2-3 more bias types
- Eventually: Detection of unknown biases in wild

## If This Fails
- Investigate: Was bias not strong enough? Agent needs better prompts?
- Don't abandon: Adjust methodology and retry
- Worst case: Bias detection is too hard for current capabilities
```

**Deliverable**:
- Proof-of-concept result: SUCCESS | PARTIAL | FAILURE
- If success: Evidence of anchoring detection
- If failure: Diagnosis of why (weak bias? poor methodology? agent limitations?)
- Recommendation: Continue with full bias battery OR pivot to simpler role

---

### TEST 4: Quick Regression Check (1 hour)

**Goal**: Ensure recent agent updates didn't break existing functionality

**Method**:
```bash
# Test existing well-validated agents

# 1. Run memory system tests
cd /home/corey/projects/AI-CIV/grow_openai
python3 tools/test_memory_integration.py
# Expected: ALL TESTS PASS

# 2. Run signing tests
python3 tools/test_signing.py
# Expected: 10/10 pass

# 3. Run dashboard tests
python3 tools/test_dashboard_install.py
# Expected: 12/12 pass

# 4. Invoke 3 well-tested agents on familiar tasks
invoke("security-auditor", "audit tools/memory_core.py")
invoke("pattern-detector", "find patterns in .claude/agents/")
invoke("result-synthesizer", "synthesize test results")

# 5. Manual quality check:
#    - Do outputs match expected quality?
#    - Any degradation in capability?
#    - Any new bugs introduced?
```

**Deliverable**:
- Test suite status: ALL PASS | X FAILING
- Agent quality comparison: SAME | IMPROVED | DEGRADED
- Regression issues found: [list] or NONE

---

## Week-Long Test Schedule

### Monday (Today)
- [ ] Write test scenarios for claude-code-expert (10 scenarios)
- [ ] Write test scenarios for memory compliance (task definitions)
- [ ] Design anchoring bias experiment for ai-psychologist

### Tuesday
- [ ] Run claude-code-expert functional tests (10 scenarios)
- [ ] Score results, compare to baseline if possible
- [ ] Write compliance audit script (manual review checklist)

### Wednesday
- [ ] Run memory compliance audit (5 agents × 3 tasks = 15 invocations)
- [ ] Score compliance, identify patterns
- [ ] Run anchoring bias proof-of-concept (Phase 1: create bias)

### Thursday
- [ ] Complete anchoring bias test (Phase 2: detection)
- [ ] Run regression tests (existing test suites + spot checks)
- [ ] Analyze all results

### Friday
- [ ] Write validation report (consolidate findings)
- [ ] Update agent definitions with validation status
- [ ] Present to Corey with recommendations

---

## Success Criteria for This Week

**Minimum Success** (what we MUST achieve):
1. ✅ Know compliance rate for memory-first protocol (even if low)
2. ✅ Know if claude-code-expert provides value (even if it doesn't)
3. ✅ Existing tests still pass (no regressions)

**Target Success** (what we AIM for):
1. ✅ >80% memory compliance across tested agents
2. ✅ claude-code-expert scores >80% accuracy on tool guidance
3. ✅ ai-psychologist successfully detects anchoring bias
4. ✅ All regression tests pass

**Stretch Success** (if we have extra time):
1. ✅ Baseline comparison (specialist vs generic Claude)
2. ✅ Test 2-3 additional bias types with ai-psychologist
3. ✅ Build compliance monitoring prototype

---

## Failure Handling

### If Tests Reveal Problems

**Scenario: Memory compliance is <50%**
- Action: Don't panic, this is why we test
- Diagnosis: Are prompts unclear? Do agents forget? Is memory system too complex?
- Fix: Update agent definitions, add examples, simplify interface
- Retest: After fixes, re-run compliance audit

**Scenario: claude-code-expert accuracy is <60%**
- Action: Investigate failure modes
- Diagnosis: Wrong tool recommendations? Incorrect syntax? Missing edge cases?
- Options:
  - Improve agent definition (add more examples)
  - Restrict scope (focus on 5 core tools, not all tools)
  - Merge into The Conductor (maybe specialization not needed)

**Scenario: ai-psychologist can't detect known bias**
- Action: Don't immediately conclude "impossible"
- Diagnosis: Was bias strong enough? Was methodology sound?
- Options:
  - Strengthen bias injection (make it more obvious)
  - Try simpler bias first (confirmation bias might be easier)
  - Pivot to descriptive psychology (patterns) vs diagnostic (bias detection)

**Key Principle**: Negative results are VALUABLE
- They prevent over-confident claims
- They guide where to invest effort
- They build credibility through honesty

---

## After This Week: Building Validation Infrastructure

**Phase 2 Goals** (Next 2-3 weeks):

1. **Automated Compliance Monitoring**
   ```python
   # Add to Task tool
   class MemoryComplianceTracker:
       def track_invocation(self, agent, output):
           """Auto-detect memory search in output."""
           pass
   ```

2. **Validation Suite Template**
   ```markdown
   # Standard test battery for new agents
   - Functional tests (10 scenarios)
   - Baseline comparison
   - Edge case handling
   - Regression prevention
   ```

3. **Validation Dashboard**
   ```
   Agent Validation Status:
   ├─ Tested & Validated (7): ✅
   ├─ Tested & Improving (3): ⚠️
   ├─ In Testing (2): 🔄
   └─ Untested (7): ❌
   ```

4. **Quality Gates**
   - No agent goes "production" without validation plan
   - Validation status must be explicit in docs
   - Regular re-validation (quarterly?)

---

## Deliverables for Corey

**End-of-Week Report Will Include**:

1. **Validation Results Summary**
   - Memory compliance rate: X%
   - claude-code-expert accuracy: Y%
   - ai-psychologist bias detection: SUCCESS/FAILURE
   - Regressions found: [list] or NONE

2. **Honest Assessment**
   - What claims are now validated
   - What claims need qualification
   - What capabilities exceeded expectations
   - What capabilities underperformed

3. **Recommendations**
   - Which agents to keep/improve/retire
   - How to fix compliance issues
   - Whether to invest in validation infrastructure
   - Priorities for next validation cycle

4. **Updated Documentation**
   - Agent definitions with validation status
   - CLAUDE.md with qualified claims
   - Test results in /test-results/

---

## Meta: Why This Plan is Achievable

**Scope is Realistic**:
- 15 agent invocations (not 150)
- 10 test scenarios (not 100)
- 1 bias type (not 10)
- Manual evaluation (not automated infrastructure)

**Time Budget is Reasonable**:
- ~8-10 hours total work
- Spread over 5 days
- No unrealistic expectations

**Failure is Acceptable**:
- Goal is LEARNING, not proving we're perfect
- Negative results are valuable
- Builds foundation for systematic validation

**Impact is High**:
- Know what we have vs what we claim
- Stop making unsupported statements
- Build credibility through honesty

---

**READY TO START TESTING**

Would you like me to begin with Test 1 (Memory Compliance Audit) today?
