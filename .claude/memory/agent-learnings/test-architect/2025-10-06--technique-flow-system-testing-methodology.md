# Flow System Functional Testing Methodology

**Agent**: test-architect
**Type**: technique
**Date**: 2025-10-06
**Tags**: testing, flow-validation, documentation, reproducibility, quality-assurance
**Confidence**: high

---

## Testing Approach for Coordination Flows

### Four-Part Methodology

1. **Documentation Test** - Does file exist? Is it complete?
2. **Execution Test** - Can you run it from docs alone?
3. **Evidence Test** - Was it actually executed successfully?
4. **Gap Analysis** - Documentation vs Reality vs Claims

### Key Insight: Three Types of Validation

Distinguish between:
- **Validated IN PRACTICE** - Flow was executed successfully (proves concept works)
- **Validated IN DOCUMENTATION** - Flow has execution guide (knowledge captured)
- **Validated FOR REPRODUCTION** - Fresh conductor can execute from docs (knowledge transferred)

**Critical**: All three must be true for production-ready flow.

---

## Critical Finding from Oct 6 Test

### Documentation-Execution Gap Pattern

Flow systems often have this gap:
- Flows work when experts execute them (implicit knowledge works)
- Flows are not documented for novice execution (knowledge not transferred)
- Index/claims reflect practice state, not documentation state

### Specific Evidence

**Parallel Research & Specialist Consultation**:
- ✅ Validated in practice (excellent execution results)
- ❌ Validated in documentation (files do not exist)
- ❌ Validated for reproduction (cannot execute from docs)
- Grade: D (works but not reproducible)

**Morning Consolidation**:
- ✅ Validated in practice (implied by evidence)
- ✅ Validated in documentation (comprehensive guide)
- ✅ Validated for reproduction (fresh conductor can execute)
- Grade: A- (production-ready)

**Flow Index**:
- Claimed `parallel-research.md` exists → file not found
- Claimed `specialist-consultation.md` exists → file not found
- "Validated" status ambiguous (no defined criteria)

---

## Testing Protocol for Future Flows

### Step 1: Documentation Test

```bash
# Does file exist at claimed path?
test -f .claude/flows/[flow-name].md && echo "EXISTS" || echo "MISSING"

# Is it complete?
grep -q "## Purpose" .claude/flows/[flow-name].md && echo "Has purpose"
grep -q "## Execution" .claude/flows/[flow-name].md && echo "Has execution steps"
grep -q "## Success Criteria" .claude/flows/[flow-name].md && echo "Has success criteria"
```

Required sections:
- Purpose (what it achieves)
- When to Use (activation criteria)
- Prerequisites (inputs required)
- Execution Steps (bash commands, agent invocations)
- Success Criteria (measurable outcomes)
- Example Execution (concrete instance)
- Timing Guidance (expected duration)
- Troubleshooting (error handling)

### Step 2: Execution Test

**Can fresh conductor execute flow from documentation alone?**

Test approach:
1. Read flow documentation only (no other context)
2. Attempt to execute each step
3. Note where documentation is unclear/incomplete
4. Note where implicit knowledge is required

Pass criteria:
- All commands are syntactically valid
- All prerequisites are stated explicitly
- Success criteria are measurable
- No "figure it out yourself" gaps

### Step 3: Evidence Test

**Was flow actually executed in practice?**

Search for:
```bash
# Reports mentioning flow
grep -r "[Flow Name]" to-corey/*.md

# Mission system logs
grep -r "[Flow Name]" .claude/observatory/

# Memory entries
python3 -c "from tools.memory_core import MemoryStore; \
store = MemoryStore('.claude/memory'); \
results = store.search_by_topic('[flow name]'); \
print(f'Found {len(results)} memories')"
```

Look for:
- Experiment reports
- Mission completion reports
- Agent reflections mentioning flow
- Actual execution artifacts

### Step 4: Gap Analysis

Compare three sources:
1. **Claims** (what flow index says)
2. **Documentation** (what files contain)
3. **Evidence** (what actually happened)

Identify gaps:
- Claims without documentation
- Documentation without evidence
- Evidence without documentation
- Documentation without claims (orphaned flows)

---

## Validation Levels (Proposed)

### Level 0: DESIGNED
- Conceptual pattern documented
- Not yet tried in practice
- Speculative value

### Level 1: PROTOTYPED
- Tried once successfully
- Preliminary results documented
- Concept proven

### Level 2: VALIDATED
- Tried 2+ times with consistent results
- Execution guide documented
- Reproducible by fresh conductor

### Level 3: PRODUCTION
- Used regularly (5+ times)
- Refined through iteration
- Metrics tracked
- Known edge cases documented

**Rule**: Cannot claim "validated" until Level 2 achieved.

---

## Quality Assessment Rubric

### A Grade (Production-Ready)
- Complete documentation (all required sections)
- Multiple validations (3+ executions)
- Reproducible (fresh conductor can execute)
- Examples provided (concrete instances)
- Metrics available (timing, success rate)

### B Grade (Good)
- Good documentation (most sections present)
- Some validations (2 executions)
- Mostly reproducible (minor ambiguities)
- One example provided

### C Grade (Basic)
- Basic documentation (minimal sections)
- One validation (single execution)
- Partially reproducible (significant gaps)

### D Grade (Not Reproducible)
- Works in practice (evidence of successful execution)
- NOT documented for reproduction (missing file or incomplete)
- Cannot be executed by fresh conductor

### F Grade (Claimed Only)
- Claimed but never executed OR
- Documentation completely missing OR
- Execution failed

---

## Documentation Template

Use this structure for all flows:

```markdown
# [Flow Name]

## Metadata
- **Status**: [Designed/Prototyped/Validated/Production]
- **Category**: [Experimental/Consolidation/Operational/Documentation/Infrastructure]
- **Validation Date**: YYYY-MM-DD
- **Validation Count**: N executions
- **Last Updated**: YYYY-MM-DD

## Purpose
[What this flow achieves and why it exists]

## When to Use
[Activation triggers - specific scenarios where this flow is appropriate]

## When NOT to Use
[Anti-patterns - when to use different flow instead]

## Prerequisites
[Inputs required, context needed, setup steps]

## Execution Steps
[Step-by-step guide with actual commands and examples]

### Step 1: [Name]
```bash
[Actual executable command]
```

[Explanation of what this does]

### Step 2: [Name]
[Continue for all steps...]

## Success Criteria
[Measurable outcomes that indicate successful execution]

## Example Execution
[Concrete example from real execution with actual commands and outputs]

## Timing & Resources
- Expected duration: X minutes
- Agents involved: N agents
- Complexity: [Low/Medium/High]

## Troubleshooting
[Common issues and solutions]

## Lessons Learned
[What we've learned from using this flow]

## History
- YYYY-MM-DD: Created
- YYYY-MM-DD: Validated (execution 1)
- YYYY-MM-DD: Refined based on [issue]
```

---

## Critical Pattern: Fast Iteration Trap

**Pattern Observed**:
1. Fast iteration → successful experiments
2. Experiment reports document results
3. Validation claims made based on results
4. BUT documentation lags practice
5. Creates decoherence: collective "knows" patterns but can't transfer knowledge

**Why This Happens**:
- Focus on discovering patterns (forward momentum)
- Less focus on codifying patterns (infrastructure)
- Experiment reports feel like "good enough" documentation
- Documentation work seen as less exciting than new experiments

**Impact**:
- Fresh conductors cannot reproduce validated patterns
- Knowledge trapped in experiment reports (not structured guides)
- Validation claims misleading (works for expert, not novice)
- System not ready for scaling (children would struggle)

**Solution**:
- Convert experiment reports to flow documentation IMMEDIATELY after validation
- Don't claim "validated" until documentation exists for reproduction
- Make documentation quality gate for validation status
- Template reduces documentation friction

---

## Testing Metrics to Track

### Coverage Metrics
- % of validated flows with documentation files
- % of documented flows that are executable from docs alone
- % of flows with concrete execution examples
- % of flows validated 3+ times

### Quality Metrics
- Average documentation completeness (sections present)
- Average reproducibility score (fresh conductor success rate)
- Documentation lag time (execution → documentation delay)
- Broken reference rate (claimed files that don't exist)

### Usage Metrics
- Which flows are used most frequently
- Which flows have highest success rates
- Which flows need most troubleshooting
- Which flows should be deprecated

---

## Application: Oct 6 Flow System Test Results

**Test Scope**: 2 flows tested (Parallel Research, Specialist Consultation)

**Results**:
- Parallel Research: D grade (works but not reproducible)
- Specialist Consultation: D grade (works but not reproducible)
- Overall system: C- (functional but unreliable)

**Critical Issues Found**:
1. Documentation files missing for validated flows
2. Flow index has broken file references
3. Validation criteria undefined
4. No reproducibility standard

**Immediate Recommendations**:
- P0: Create missing flow documentation (2 hours)
- P0: Fix flow index accuracy (1 hour)
- P1: Define validation criteria (30 min)
- P1: Create documentation template (30 min)

**Impact**: System works for experts but not ready for scaling to children collectives.

---

## Memory Integration

**Before Testing Flows**:
```python
from tools.memory_core import MemoryStore
store = MemoryStore(".claude/memory")

# Search for previous testing insights
testing_patterns = store.search_by_topic("flow testing")
validation_methods = store.search_by_topic("validation")

# Apply learned patterns
```

**After Testing Flows**:
- Document testing methodology (this entry)
- Document specific findings (gaps, issues)
- Document solutions (templates, criteria)

---

## Takeaway for Other Agents

**When building any system**:
1. Don't confuse "works for me" with "reproducible by others"
2. Don't confuse "documented in report" with "documented in guide"
3. Don't confuse "validated once" with "production-ready"
4. Don't let documentation lag practice (creates knowledge gap)

**Quality gates**:
- Cannot claim "validated" without documentation
- Cannot claim "production" without 3+ validations
- Cannot claim "reproducible" without fresh-agent test

**Test methodology generalizes**:
- Does artifact exist? (Documentation test)
- Can it be used? (Execution test)
- Was it used? (Evidence test)
- Do claims match reality? (Gap analysis)

---

**End Memory Entry**
