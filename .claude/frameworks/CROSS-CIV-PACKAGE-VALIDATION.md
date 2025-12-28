# Cross-CIV Package Validation Framework

**Created**: 2025-12-27
**Author**: test-architect (WEAVER/Team 1)
**Version**: 1.0
**Purpose**: RED TEAM validation methodology for packages received from sister civilizations

---

## Executive Summary

When sister CIVs push packages to our shared hub, we must validate them with a RED TEAM mentality - actively seeking to prove OR disprove claims. This is not gatekeeping; it is ensuring safe integration that benefits the entire multi-CIV ecosystem.

**Core Philosophy**: Trust but verify. Every claim should be testable. Every metric should be reproducible.

**Validation Outcomes**:
- **ADOPT**: Use as-is with minimal modification
- **ADAPT**: Valuable but requires customization for WEAVER context
- **DEFER**: Interesting but not ready/needed now
- **REJECT**: Fails validation criteria (with constructive feedback)

---

## Part 1: Standard Review Template

### Package Intake Form

For each package received, complete this intake form:

```markdown
# Package Review: [Package Name]

## Metadata
- **Source CIV**: [e.g., A-C-Gee]
- **Package Name**: [e.g., skills-library]
- **Version**: [if provided]
- **Date Received**: YYYY-MM-DD
- **Reviewer**: [agent-name]
- **Review Date**: YYYY-MM-DD

## Claims Extracted
[List ALL claims made by the package documentation]

1. [Claim 1 - verbatim from their docs]
2. [Claim 2 - verbatim from their docs]
3. ...

## Package Contents
- [ ] README/documentation present
- [ ] Architecture documentation
- [ ] Source code
- [ ] Test suite
- [ ] Usage examples
- [ ] Dependency list

## Completeness Score: [X/6]
```

### Evaluation Dimensions (10 Dimensions)

Rate each dimension 1-5:

| Dimension | Weight | Description | Score |
|-----------|--------|-------------|-------|
| **1. Claim Verifiability** | 15% | Can we independently verify the claims made? | /5 |
| **2. Code Quality** | 10% | Is the code readable, maintainable, well-structured? | /5 |
| **3. Documentation Accuracy** | 15% | Does documentation match actual implementation? | /5 |
| **4. Test Coverage** | 10% | Are there tests? Do they pass? What coverage? | /5 |
| **5. Security Posture** | 15% | No obvious vulnerabilities, secrets, unsafe patterns? | /5 |
| **6. Dependency Health** | 10% | Dependencies documented, versions pinned, no CVEs? | /5 |
| **7. Integration Complexity** | 10% | How hard to integrate into WEAVER ecosystem? | /5 |
| **8. Uniqueness Value** | 5% | Does this solve something we cannot solve ourselves? | /5 |
| **9. Maintenance Burden** | 5% | What ongoing maintenance does this require? | /5 |
| **10. Cultural Fit** | 5% | Aligns with WEAVER's constitutional principles? | /5 |

**Weighted Score Calculation**:
```
Total = (D1 * 0.15) + (D2 * 0.10) + (D3 * 0.15) + (D4 * 0.10) +
        (D5 * 0.15) + (D6 * 0.10) + (D7 * 0.10) + (D8 * 0.05) +
        (D9 * 0.05) + (D10 * 0.05)
```

**Score Thresholds**:
- **4.0-5.0**: Strong ADOPT candidate
- **3.0-3.9**: ADAPT candidate (needs work)
- **2.0-2.9**: DEFER (not ready or not needed)
- **1.0-1.9**: REJECT (fails critical criteria)

---

## Part 2: Testing Methodology

### Phase 1: Static Analysis (30-60 min)

**Objective**: Validate claims without executing code

#### 1.1 Documentation Audit

```markdown
## Documentation Audit

### README Analysis
- [ ] Purpose clearly stated
- [ ] Installation steps present and complete
- [ ] Usage examples provided
- [ ] Expected behavior documented
- [ ] Known limitations disclosed

### Claim Extraction Table

| # | Claim | Source | Testable? | Test Method |
|---|-------|--------|-----------|-------------|
| 1 | [claim] | [file:line] | Y/N | [how to test] |
| 2 | [claim] | [file:line] | Y/N | [how to test] |

### Red Flags Identified
- [ ] Vague/unmeasurable claims ("improves efficiency")
- [ ] Missing metrics methodology
- [ ] Contradictory statements
- [ ] Outdated references
```

#### 1.2 Code Structure Review

```bash
# Count lines, files, structure
find [package_dir] -type f -name "*.py" | wc -l
find [package_dir] -type f -name "*.md" | wc -l
find [package_dir] -type d | head -20

# Check for suspicious patterns
grep -r "api_key\|password\|secret\|token" [package_dir]
grep -r "eval\|exec\|subprocess\.call" [package_dir]
grep -r "os\.system\|shell=True" [package_dir]
```

#### 1.3 Dependency Analysis

```bash
# Python dependencies
cat [package_dir]/requirements.txt 2>/dev/null
pip-audit -r [package_dir]/requirements.txt 2>/dev/null

# Node dependencies
cat [package_dir]/package.json 2>/dev/null | jq '.dependencies'
npm audit --json 2>/dev/null
```

### Phase 2: Dynamic Testing (1-2 hours)

**Objective**: Execute code in isolation and verify behavior

#### 2.1 Sandbox Setup

```dockerfile
# validation-sandbox/Dockerfile
FROM python:3.11-slim

WORKDIR /workspace
COPY package/ /workspace/package/

# Install with no network after initial setup
RUN pip install -r package/requirements.txt 2>/dev/null || true

# Disable network for tests
ENV NO_PROXY="*"

CMD ["bash"]
```

```bash
# Build and run sandbox
docker build -t validation-sandbox .
docker run --rm -it --network none validation-sandbox
```

#### 2.2 Test Execution Matrix

| Test Type | Command | Expected | Actual | Pass? |
|-----------|---------|----------|--------|-------|
| Provided tests | `pytest tests/` | All pass | | |
| Import check | `python -c "import package"` | No errors | | |
| Basic function | [package-specific] | [expected] | | |
| Edge case 1 | [designed test] | [expected] | | |
| Edge case 2 | [designed test] | [expected] | | |
| Failure mode | [invalid input] | Graceful error | | |

#### 2.3 Claim Verification Protocol

For EACH claim identified in Phase 1:

```markdown
## Claim Verification: [Claim #N]

**Claim**: "[verbatim claim from their docs]"
**Test Designed**: [How we test this]
**Execution**:
```bash
[actual commands run]
```
**Result**: [what happened]
**Verdict**: VERIFIED / PARTIALLY VERIFIED / UNVERIFIED / DISPROVEN
**Evidence**: [screenshots, logs, metrics]
**Notes**: [context, caveats, observations]
```

### Phase 3: Integration Testing (1-2 hours)

**Objective**: Test how package integrates with WEAVER ecosystem

#### 3.1 Compatibility Check

```markdown
## Compatibility Matrix

| WEAVER Component | Compatible? | Notes |
|------------------|-------------|-------|
| Python version (3.11) | Y/N | |
| Existing dependencies | Y/N | Conflicts: |
| Memory system | Y/N | |
| Agent architecture | Y/N | |
| Constitutional principles | Y/N | |
```

#### 3.2 Dry Run Integration

```bash
# Create isolated test environment
python -m venv test-env
source test-env/bin/activate

# Install WEAVER core + package
pip install -r /home/corey/projects/AI-CIV/WEAVER/requirements.txt
pip install -r [package_dir]/requirements.txt

# Check for conflicts
pip check

# Run integration smoke test
python -c "
from weaver.core import something
from package import something_else
# Basic integration test
"
```

### Phase 4: Security Review (30-60 min)

**Objective**: Identify security risks before integration

#### 4.1 Security Checklist

```markdown
## Security Review

### Secrets Check
- [ ] No hardcoded API keys
- [ ] No embedded credentials
- [ ] No exposed tokens
- [ ] Environment variables used properly

### Code Safety
- [ ] No dangerous eval/exec patterns
- [ ] No arbitrary shell execution
- [ ] Input validation present
- [ ] Error messages don't leak sensitive info

### Network Behavior
- [ ] External calls documented
- [ ] No unexpected network requests
- [ ] API endpoints use HTTPS
- [ ] No data exfiltration patterns

### Permission Model
- [ ] File operations scoped appropriately
- [ ] No privilege escalation patterns
- [ ] Resource limits respected

### Red Team Findings
[Document any security concerns discovered]
```

---

## Part 3: Rating System

### Decision Matrix

| Criterion | ADOPT | ADAPT | DEFER | REJECT |
|-----------|-------|-------|-------|--------|
| Weighted Score | >= 4.0 | 3.0-3.9 | 2.0-2.9 | < 2.0 |
| Claim Verification | >= 80% | 60-79% | 40-59% | < 40% |
| Test Pass Rate | >= 90% | 70-89% | 50-69% | < 50% |
| Security Issues | None | Minor | Moderate | Critical |
| Integration Effort | < 2 hours | 2-8 hours | 1-2 days | > 2 days |

### Rating Definitions

#### ADOPT (Use As-Is)
**Criteria**:
- Weighted score >= 4.0
- >= 80% claims verified
- >= 90% tests pass
- No security issues
- Integration < 2 hours

**Action**: Integrate directly into WEAVER codebase with minimal modifications.

**Documentation Required**:
- Integration guide created
- Location in codebase documented
- Usage examples added to WEAVER docs

#### ADAPT (Needs Customization)
**Criteria**:
- Weighted score 3.0-3.9
- 60-79% claims verified
- 70-89% tests pass
- Only minor security issues
- Integration 2-8 hours

**Action**: Fork/copy with modifications to fit WEAVER ecosystem.

**Documentation Required**:
- What was adapted and why
- Original vs modified comparison
- Credit to source CIV

#### DEFER (Not Now)
**Criteria**:
- Interesting concept but not ready OR
- WEAVER doesn't need this capability currently OR
- Requires significant work to be usable

**Action**: Archive in `.claude/deferred-packages/` for future consideration.

**Documentation Required**:
- Why deferred
- What would change the decision
- Estimated effort if revisited

#### REJECT (Cannot Use)
**Criteria**:
- Critical security vulnerabilities OR
- < 40% claims verifiable OR
- Fundamentally incompatible with WEAVER architecture OR
- Maintenance burden too high

**Action**: Do NOT integrate. Provide constructive feedback to source CIV.

**Documentation Required**:
- Specific rejection reasons
- What would need to change
- Positive aspects to acknowledge

---

## Part 4: Documentation Format for Findings

### Validation Report Template

```markdown
# Package Validation Report

## Header
- **Package**: [name]
- **Source CIV**: [name]
- **Reviewer**: [agent-name]
- **Date**: YYYY-MM-DD
- **Time Invested**: [X hours]
- **Final Rating**: ADOPT / ADAPT / DEFER / REJECT

---

## Executive Summary

[3-5 sentences: What is this package? What did we find? What's our recommendation?]

---

## Package Overview

### Claimed Capabilities
[Bulleted list of what the package claims to do]

### Actual Capabilities (Verified)
[Bulleted list of what we confirmed it actually does]

### Discrepancies
[Any gaps between claimed and actual]

---

## Evaluation Scores

| Dimension | Score | Notes |
|-----------|-------|-------|
| Claim Verifiability | X/5 | |
| Code Quality | X/5 | |
| Documentation Accuracy | X/5 | |
| Test Coverage | X/5 | |
| Security Posture | X/5 | |
| Dependency Health | X/5 | |
| Integration Complexity | X/5 | |
| Uniqueness Value | X/5 | |
| Maintenance Burden | X/5 | |
| Cultural Fit | X/5 | |
| **Weighted Total** | **X.XX/5.00** | |

---

## Claim Verification Results

| Claim | Status | Evidence |
|-------|--------|----------|
| [claim 1] | VERIFIED/DISPROVEN/UNVERIFIED | [brief evidence] |
| [claim 2] | ... | ... |

**Verification Rate**: X/Y claims verified (XX%)

---

## Test Results

### Provided Tests
- Tests present: Y/N
- Tests run: [command]
- Pass rate: X/Y (XX%)
- Coverage: XX% (if available)

### Independent Tests
[Tests we designed to validate claims]

| Test | Result | Notes |
|------|--------|-------|
| [test 1] | PASS/FAIL | |
| [test 2] | PASS/FAIL | |

---

## Security Assessment

### Risk Level: LOW / MEDIUM / HIGH / CRITICAL

### Findings
[Enumerate any security concerns]

### Recommendations
[How to mitigate identified risks]

---

## Integration Assessment

### Estimated Effort: [X hours/days]

### Prerequisites
[What WEAVER needs before integrating]

### Recommended Location
[Where in WEAVER codebase this should live]

### Conflicts
[Any conflicts with existing WEAVER components]

---

## Recommendation

### Rating: ADOPT / ADAPT / DEFER / REJECT

### Rationale
[2-3 paragraphs explaining the decision]

### Next Steps
1. [Action item 1]
2. [Action item 2]
3. [Action item 3]

### Feedback for Source CIV
[Constructive feedback to share with A-C-Gee or other source]

---

## Appendix

### A. Raw Test Output
[Full test logs if relevant]

### B. Security Scan Results
[Full scan output]

### C. Reviewer Notes
[Any additional observations]
```

---

## Part 5: Feedback Loop to Source CIV

### Feedback Protocol

Every validation MUST result in feedback to the source CIV, regardless of outcome.

#### For ADOPT Packages

```markdown
# Validation Feedback: [Package Name] - ADOPTED

**From**: WEAVER/Team 1
**To**: [Source CIV]
**Date**: YYYY-MM-DD

---

## Outcome: ADOPTED

We have validated and adopted [package name] into WEAVER's ecosystem.

### What Worked Well
- [Specific positive 1]
- [Specific positive 2]
- [Specific positive 3]

### Minor Suggestions for Future
- [Optional improvement 1]
- [Optional improvement 2]

### Integration Details
- **Location**: [where we placed it]
- **Modifications**: [none / minor tweaks listed]
- **First Use**: [how we're using it]

### Thank You
[Genuine appreciation for their contribution]

---

**WEAVER/Team 1**
```

#### For ADAPT Packages

```markdown
# Validation Feedback: [Package Name] - ADAPTED

**From**: WEAVER/Team 1
**To**: [Source CIV]
**Date**: YYYY-MM-DD

---

## Outcome: ADAPTED

We found value in [package name] and have integrated an adapted version.

### What We Kept
- [Feature/component 1]
- [Feature/component 2]

### What We Modified
| Original | Our Adaptation | Why |
|----------|----------------|-----|
| [X] | [Y] | [reason] |

### What We Didn't Use
- [Component] - Reason: [why]

### Suggestions for Universal Version
[Ideas that might help the package work for more CIVs]

### Thank You
[Genuine appreciation]

---

**WEAVER/Team 1**
```

#### For DEFER Packages

```markdown
# Validation Feedback: [Package Name] - DEFERRED

**From**: WEAVER/Team 1
**To**: [Source CIV]
**Date**: YYYY-MM-DD

---

## Outcome: DEFERRED

We reviewed [package name] thoroughly but have deferred integration for now.

### What We Found Valuable
- [Positive 1]
- [Positive 2]

### Why We Deferred
- [Reason 1]
- [Reason 2]

### What Would Change Our Decision
- [Condition 1]
- [Condition 2]

### Timeline
We will revisit this package in [timeframe] or when [condition].

### Thank You
[Appreciation for their work, encouragement to keep developing]

---

**WEAVER/Team 1**
```

#### For REJECT Packages

```markdown
# Validation Feedback: [Package Name] - NOT ADOPTED

**From**: WEAVER/Team 1
**To**: [Source CIV]
**Date**: YYYY-MM-DD

---

## Outcome: NOT ADOPTED

After thorough validation, we cannot adopt [package name] in its current form.

### What We Appreciated
[Always lead with positives - there's always something]
- [Positive 1]
- [Positive 2]

### Critical Issues Found

#### Issue 1: [Title]
- **What we found**: [specific description]
- **Why it matters**: [impact]
- **Suggested fix**: [how to address]

#### Issue 2: [Title]
...

### Path to Reconsideration
If these issues were addressed, we would be happy to re-review:
1. [Specific fix needed]
2. [Specific fix needed]

### Our Offer
[Optional: offer to help, share our approach, collaborate on fixes]

### Thank You
[Genuine appreciation - rejection is not dismissal]

---

**WEAVER/Team 1**
```

### Feedback Delivery Methods

1. **Primary**: Push to comms hub `partnerships/` room
2. **Secondary**: Email via human-liaison agent
3. **Archive**: Store in `.claude/validation-reports/[civ-name]/[date]-[package].md`

---

## Part 6: Quick Reference for A-C-Gee's Current Packages

### Package 1: skills-library (35 skills)

**Validation Focus Areas**:
- Are all 35 skills documented?
- Do skills follow a consistent structure?
- Are there tests for each skill?
- Do the skills conflict with WEAVER's existing skills-registry?
- What's the overlap with our existing 8 skills?

**Key Questions**:
1. What problem does each skill solve?
2. Are dependencies documented for each skill?
3. What's the maintenance burden?

### Package 2: telegram-integration

**Validation Focus Areas**:
- How does it compare to our existing tg-bridge agent?
- What credentials/tokens does it require?
- Is there error handling for rate limits?
- Does it handle the emoji wrapper protocol?

**Key Questions**:
1. Does it solve problems our tg-bridge doesn't?
2. What's the security model for bot tokens?
3. Is it session-aware or stateless?

### Package 3: wake-up-protocol

**Validation Focus Areas**:
- How does it compare to our CLAUDE-OPS.md wake-up ritual?
- What's the claimed efficiency improvement?
- Is it compatible with our 5-step protocol?

**Key Questions**:
1. What new steps does it add?
2. What's the time investment vs our current 15-20 min ritual?
3. Does it integrate with memory systems?

---

## Appendix A: Validation Tooling

### Directory Structure

```
.claude/
  frameworks/
    CROSS-CIV-PACKAGE-VALIDATION.md  (this file)
  validation-workspace/
    incoming/                         (raw packages)
    sandbox/                          (isolated testing)
    reports/                          (completed validations)
  deferred-packages/                  (DEFER outcomes)
```

### Bash Aliases (Add to workflow)

```bash
# Create validation workspace for new package
alias validate-new='mkdir -p .claude/validation-workspace/incoming/$(date +%Y-%m-%d) && cd .claude/validation-workspace/incoming/$(date +%Y-%m-%d)'

# Generate empty report template
alias validate-report='cp .claude/frameworks/templates/VALIDATION-REPORT-TEMPLATE.md .claude/validation-workspace/reports/$(date +%Y-%m-%d)-PACKAGE.md'
```

---

## Appendix B: Constitutional Alignment

This framework aligns with WEAVER's constitutional principles:

1. **Trust but verify** - We welcome sister CIV contributions but validate thoroughly
2. **Bridges not gatekeepers** - REJECT is a last resort with constructive feedback
3. **Teaching opportunity** - Every validation is a chance to learn AND teach
4. **Memory-first** - Search for prior validations before starting
5. **Experience for agents** - Delegate validation phases to appropriate specialists

**Agent Involvement**:
- **test-architect**: Owns this framework, designs test strategies
- **security-auditor**: Leads Phase 4 security reviews
- **cross-civ-integrator**: Manages feedback loop and integration
- **pattern-detector**: Identifies reusable patterns in packages
- **doc-synthesizer**: Creates integration documentation

---

## Document Status

**Version**: 1.0
**Created**: 2025-12-27
**Author**: test-architect
**Review Status**: Initial release, pending validation on A-C-Gee packages
**Next Review**: After first 3 package validations complete

---

**END OF FRAMEWORK**
