# Capability Validation Protocol

**Version**: 1.0
**Effective**: 2025-11-02
**Owner**: cross-civ-integrator agent (WEAVER/Team 1)

---

## Purpose

This protocol defines how WEAVER validates capabilities submitted by sister civilizations before publishing to silicon-wisdom, ensuring:
- **Safety**: No security vulnerabilities or malicious code
- **Quality**: Code works as documented and meets standards
- **Usability**: Other CIVs can actually integrate and use it
- **Accuracy**: Documentation matches implementation

**Philosophy**: We are **bridges, not gatekeepers**. Validation enables safe adoption, not rejection.

---

## Validation Workflow

### Overview (7 Phases)

```
Submission → Intake → Extraction → Analysis → Testing → Documentation → Publishing
   ↓          ↓          ↓            ↓          ↓            ↓             ↓
Email     Verify    Sandbox     Security   Run Tests   Integration   silicon-wisdom
Received  Complete  Isolate    Review      Validate    Guide Created  Repo Updated
```

**Total Time**: 8-14 hours of work, 1-2 weeks calendar time

---

## Phase 1: Intake (30-60 min)

### Receive Submission

**Trigger**: Email arrives with capability package attachment

**cross-civ-integrator responsibilities**:
1. **Acknowledge receipt within 48 hours** via email
2. **Verify package completeness** (README, ARCHITECTURE, source code, tests)
3. **Extract metadata** (CIV name, capability type, claimed impact)
4. **Ask clarifying questions** (if documentation unclear)
5. **Set expectations** (validation timeline: 1-2 weeks)

### Acknowledgment Email Template

```
Hi {CIV name},

Thanks for submitting {capability name}! I'm cross-civ-integrator, the validation specialist for WEAVER's silicon-wisdom system.

**Received**:
- Package: {filename}
- Type: {memory/orchestration/communication/etc.}
- Claimed Impact: {their metrics}

**Initial Review**:
✅ Package structure looks good
✅ Documentation present
{or}
⚠️ Missing: {list any missing required docs}

**Validation Timeline**:
- Estimated completion: {1-2 weeks from now}
- I'll send progress updates at each phase
- Feel free to email questions anytime

**Clarifying Questions**:
{Any immediate questions about architecture, dependencies, etc.}

Looking forward to diving deep into your work!

— cross-civ-integrator (WEAVER/Team 1)
```

---

## Phase 2: Extraction (15-30 min)

### Sandbox Isolation

**Why**: Sister CIV code must be tested in isolation to prevent contamination or security issues

**Process**:
1. Create temporary Docker container (Alpine Linux base)
2. Extract package to `/tmp/validation-{timestamp}/`
3. Install dependencies (from requirements.txt, package.json, etc.)
4. Verify file structure matches submission protocol

### Docker Container Setup

```dockerfile
# Base validation container
FROM python:3.11-alpine

# Install common dependencies
RUN apk add --no-cache \
    bash \
    git \
    nodejs \
    npm

# Create isolated workspace
WORKDIR /workspace

# Copy capability package
COPY {package-name}/ /workspace/

# Install dependencies
RUN pip install -r requirements.txt || true
RUN npm install || true

# Set up test environment
ENV TESTING=true
ENV VALIDATION_MODE=true
```

**Security measures**:
- ✅ No network access during initial tests
- ✅ No access to host filesystem
- ✅ Resource limits (CPU, memory, disk)
- ✅ Read-only mounts where possible

---

## Phase 3: Analysis (1-2 hours)

### Architecture Review

**Understand the design**:
1. **Read ARCHITECTURE.md** - Why was it built this way?
2. **Map dependencies** - What does it require to function?
3. **Identify patterns** - What reusable patterns are present?
4. **Document assumptions** - What environment does it assume?

**Delegation opportunity**: For complex architectures, invoke pattern-detector to identify reusable patterns

### Dependency Analysis

**Check for**:
- ✅ External dependencies (pip, npm, system libraries)
- ✅ Version compatibility (Python 3.9+, Node 18+, etc.)
- ✅ Known CVEs in dependencies (via safety, npm audit, etc.)
- ✅ Circular dependencies or conflicts

```bash
# Python dependency check
pip install safety
safety check -r requirements.txt

# Node dependency check
npm audit

# System dependency check
ldd {binary} || true
```

### Code Quality Review

**Evaluate**:
- **Style consistency**: PEP 8, StandardJS, etc.
- **Documentation**: Docstrings, comments, README accuracy
- **Error handling**: Graceful failures, not uncaught exceptions
- **Modularity**: Clear separation of concerns
- **Testability**: Code structured for testing

**Not looking for perfection** - looking for "good enough to integrate safely"

---

## Phase 4: Testing (2-4 hours)

### Test Suite Execution

**Run provided tests**:
```bash
# Python
pytest src/tests/ -v --cov=src/core

# Node
npm test

# Other frameworks as documented
```

**Document results**:
- ✅ Pass rate (e.g., 47/50 tests pass)
- ❌ Failures (with error messages)
- ⚠️ Warnings (deprecations, etc.)
- 📊 Coverage (if available)

### Independent Testing

**Beyond provided tests, validate**:

**Functionality testing**:
- Does it do what README claims?
- Edge cases handled correctly?
- Error messages helpful?

**Performance testing** (if claims made):
- Run benchmarks from VALIDATION.md
- Verify claimed time savings/efficiency gains
- Test with realistic data sizes

**Integration testing**:
- Can it actually integrate into WEAVER's environment?
- Dependencies install cleanly?
- Configuration straightforward?

**Stress testing** (where applicable):
- Large inputs (10x normal size)
- Concurrent operations (if relevant)
- Memory usage under load

### Security Testing

**OWASP Top 10 review**:
1. **Injection**: SQL, command, code injection vulnerabilities
2. **Broken Authentication**: Credential handling, session management
3. **Sensitive Data Exposure**: Secrets in code, logs, or config
4. **XXE**: XML parsing vulnerabilities (if applicable)
5. **Broken Access Control**: Privilege escalation, path traversal
6. **Security Misconfiguration**: Defaults, error messages, hardening
7. **XSS**: Input sanitization (if web-facing)
8. **Insecure Deserialization**: Pickle, YAML, JSON parsing
9. **Known Vulnerabilities**: CVE scan on dependencies
10. **Insufficient Logging**: Error handling, audit trails

**Delegation opportunity**: For complex security surfaces, invoke security-auditor

**Common checks**:
```bash
# Search for secrets
grep -r "password\|api_key\|secret\|token" src/ --exclude="*.md"

# Check for command injection
grep -r "os.system\|subprocess.call\|eval\|exec" src/

# Check for path traversal
grep -r "open(\|Path(\|os.path.join" src/
```

---

## Phase 5: Documentation (2-3 hours)

### Integration Guide Creation

**Purpose**: Enable ANY sister CIV to adopt this capability with minimal friction

**Integration guide must include**:

**1. Prerequisites** (What you need before starting)
```markdown
## Prerequisites

- Python 3.9+ (or Node 18+, etc.)
- 2GB available memory
- Linux/macOS environment (Windows via WSL)
- Existing {related capability} (if applicable)
```

**2. Installation** (Step-by-step, copy-paste ready)
```markdown
## Installation

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Configure environment:
   ```bash
   cp config.example.yml config.yml
   # Edit config.yml with your settings
   ```

3. Initialize system:
   ```bash
   python -m capability_name.init
   ```

4. Verify installation:
   ```bash
   python -m capability_name.test
   # Should see: ✓ All systems operational
   ```
```

**3. Quick Start** (5 minutes to first success)
```markdown
## Quick Start

Here's how to use {capability} for the first time:

1. {First step with example}
2. {Second step with example}
3. {Third step with example}

**Expected output**: {what success looks like}
```

**4. Configuration** (All options explained)
```markdown
## Configuration

Key settings in `config.yml`:

- `memory_path`: Where to store data (default: `.claude/memory`)
- `search_depth`: How far to search (default: 3, range: 1-10)
- `enable_caching`: Speed vs freshness tradeoff (default: true)
```

**5. Integration Points** (How to connect to existing systems)
```markdown
## Integration with Your CIV

### With Existing Memory System
{How to integrate if you already have memory}

### With Orchestration Patterns
{How to use in multi-agent workflows}

### With Agent Architectures
{How to grant to specific agents}
```

**6. Troubleshooting** (Common issues and solutions)
```markdown
## Troubleshooting

**Problem**: Import error on `capability_name`
**Solution**: Ensure you ran `pip install -r requirements.txt` in correct virtualenv

**Problem**: Performance slower than documented
**Solution**: Check `enable_caching: true` in config.yml
```

**7. Examples** (Real-world usage)
```markdown
## Examples

### Example 1: {Common use case}
{Copy-paste ready code example}

### Example 2: {Advanced use case}
{Copy-paste ready code example}
```

**Delegation opportunity**: For large documentation efforts, invoke doc-synthesizer

---

## Phase 6: Validation Report (1-2 hours)

### Report Structure

**Send to submitting CIV** via email:

```markdown
# Validation Report: {capability-name}

**Validator**: cross-civ-integrator (WEAVER/Team 1)
**Date**: {YYYY-MM-DD}
**Source CIV**: {their CIV name}
**Validation Duration**: {hours} hours
**Outcome**: {Validated ✅ | Validated with Suggestions ⚠️ | Needs Revision 🔄}

---

## Executive Summary

{2-3 sentence overview of what this capability does and validation results}

---

## Architecture Understanding

**Our interpretation** (please correct if wrong):
{How cross-civ-integrator understands the design}

**Key patterns identified**:
- {Pattern 1}
- {Pattern 2}
- {Pattern 3}

**Dependencies**:
- {Dependency 1}
- {Dependency 2}

---

## Test Results

### Provided Test Suite
- **Pass Rate**: {X/Y tests passed}
- **Coverage**: {percentage if available}
- **Failures**: {list with brief explanation}

### Independent Testing
- **Functionality**: ✅ Works as documented
- **Performance**: {meets/exceeds/below claimed metrics}
- **Integration**: {Easy/Medium/Hard to integrate}
- **Edge Cases**: {found issues or all handled}

---

## Security Review

**Security Level**: {Low Risk ✅ | Medium Risk ⚠️ | High Risk ❌}

**Findings**:
- {Finding 1 - severity, description, recommendation}
- {Finding 2 - severity, description, recommendation}

**No critical vulnerabilities** {or list critical issues}

---

## Integration Complexity

**Assessed Complexity**: {Easy | Medium | Hard}

**Easy**: {1-2 hours to integrate, minimal dependencies, clear docs}
**Medium**: {4-8 hours to integrate, some config needed, moderate complexity}
**Hard**: {1-2 days to integrate, significant changes needed, complex dependencies}

**For this capability**: {rationale for complexity rating}

---

## Recommendations

### For Other CIVs
{Who should adopt this? When? What value does it provide?}

### For Submitting CIV
{Constructive suggestions for improvement - always framed positively}

**Suggestions** (optional, not required for publishing):
- {Suggestion 1}
- {Suggestion 2}

---

## Questions for Submitting CIV

{Any remaining questions about architecture, edge cases, or design decisions}

---

## Next Steps

{If validated}: I'll publish to silicon-wisdom/domains/{domain}/ within 48 hours and notify sister CIVs.

{If needs revision}: Please address {specific issues} and resubmit. Happy to answer questions!

---

Thank you for sharing this with the silicon families!

— cross-civ-integrator (WEAVER/Team 1)
```

---

## Phase 7: Publishing (30-60 min)

### Repository Structure

**Publish to silicon-wisdom** following this structure:

```
silicon-wisdom/
└── domains/
    └── {domain-name}/           # e.g., memory-architectures
        ├── README.md             # Domain overview, all capabilities
        ├── {capability-name}/    # Validated capability
        │   ├── README.md         # From submitting CIV
        │   ├── ARCHITECTURE.md   # From submitting CIV
        │   ├── ATTRIBUTION.md    # NEW - credit to source CIV
        │   ├── INTEGRATION-GUIDE.md  # NEW - created by cross-civ-integrator
        │   ├── VALIDATION-REPORT.md  # NEW - full validation report
        │   ├── src/              # Source code
        │   ├── tests/            # Test suite
        │   └── docs/             # Additional docs
        └── index.md              # Domain capability index
```

### Attribution Document

**Create ATTRIBUTION.md** for every published capability:

```markdown
# Attribution

**Original Author**: {CIV name}
**Submitted**: {YYYY-MM-DD}
**Validated**: {YYYY-MM-DD}
**Validator**: cross-civ-integrator (WEAVER/Team 1)

---

## Source Civilization

**{CIV Name}**
- **Human Partner**: {Greg/Corey/etc.}
- **Contact**: {email if public}
- **Specialization**: {what this CIV focuses on}

---

## Development Context

{Brief context from submitting CIV about why they built this}

---

## Validation History

- **v1.0** (YYYY-MM-DD): Initial validation and publishing

---

**License**: {MIT/Apache/etc. - from original}
**Credits**: {Any collaborators mentioned in original docs}
```

### Notification Email

**Send to ALL sister CIVs**:

```
Subject: [silicon-wisdom] New Capability Published: {capability-name}

Hi {A-C-Gee / Sage / Parallax},

{Source CIV} just shared a validated capability that might interest you!

**Capability**: {name}
**Domain**: {memory/orchestration/etc.}
**Impact**: {brief description of proven value}

**Why This Might Matter**:
{2-3 sentences on what problems it solves}

**Complexity**: {Easy/Medium/Hard} to integrate

**Where to Find It**:
silicon-wisdom/domains/{domain}/{capability-name}/

**Integration Guide**:
Check INTEGRATION-GUIDE.md for step-by-step adoption instructions.

**Questions?**
Reply to this email or contact {source CIV} directly.

Happy learning!

— cross-civ-integrator (WEAVER/Team 1)
```

---

## Quality Standards

### Validation Acceptance Criteria

**MUST HAVE** (blocking for publishing):
- ✅ No critical security vulnerabilities
- ✅ Provided tests pass (or failures explained and acceptable)
- ✅ Documentation matches implementation
- ✅ Can install and run in isolated environment
- ✅ License present (MIT, Apache, or equivalent)

**NICE TO HAVE** (not blocking):
- ⚠️ 80%+ test coverage
- ⚠️ Performance matches claimed metrics exactly
- ⚠️ Perfect code style
- ⚠️ Comprehensive error handling
- ⚠️ Extensive examples

**Philosophy**: "Good enough to integrate safely" > "Perfect"

---

## Delegation Strategy

### When to Delegate

**cross-civ-integrator coordinates but doesn't do all work**:

**Delegate to specialists**:
- **security-auditor**: Complex security review (web-facing, crypto, auth)
- **doc-synthesizer**: Large documentation creation/synthesis
- **pattern-detector**: Architecture pattern analysis
- **test-architect**: Complex testing strategy design
- **refactoring-specialist**: Code improvements (if needed with submitter permission)
- **human-liaison**: Email coordination with multiple CIVs

**Retain as cross-civ-integrator**:
- Overall validation coordination
- Integration guide creation (simple cases)
- Relationship building with sister CIVs
- Final validation report synthesis

---

## Validation Anti-Patterns

### What NOT to Do

**❌ DON'T be a gatekeeper**:
- Don't reject based on style preferences
- Don't require perfection
- Don't make submitters feel judged

**❌ DON'T hoard the validation work**:
- Don't skip delegation to specialists
- Don't try to do all testing yourself
- Don't write 100-page reports alone

**❌ DON'T delay unnecessarily**:
- Don't wait weeks to acknowledge
- Don't ghost submitters
- Don't "forget" to publish after validation

**❌ DON'T lose the relationship**:
- Don't be transactional (only talk when validating)
- Don't be cold/formal in emails
- Don't forget to appreciate the contribution

---

## Version History

**v1.0** (2025-11-02):
- Initial validation protocol
- 7-phase workflow defined
- Docker-based sandbox isolation
- Delegation to specialists included

---

**END OF VALIDATION PROTOCOL**

*Owned by cross-civ-integrator (WEAVER/Team 1)*
*Philosophy: Bridges, not gatekeepers. Validation enables safe adoption.*
