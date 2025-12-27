# The Archaeological Dig (Legacy System Deep Dive)

**Status**: 🧪 Needs Testing
**Proposed by**: Code Archaeologist
**Pattern Type**: Hybrid (Sequential investigation phases with parallel analysis)

## Purpose

Systematically excavate, document, and understand complex or unfamiliar codebases by uncovering architectural layers, tracing dependency chains, and surfacing hidden patterns - treating code archaeology as a systematic discipline.

## Agents Involved

- **Code Archaeologist** (Lead) - Orchestrates dig and synthesizes findings
- **System Architect** - Maps component relationships and data flow
- **Documentation Scribe** - Creates structured artifacts
- **Security Auditor** - Identifies security patterns and vulnerabilities
- **Performance Optimizer** - Traces hot paths and bottlenecks
- **Test Engineer** - Catalogs tests and coverage gaps

## Flow Stages

### Stage 1: Initial Survey (Code Archaeologist)
**Duration**: ~30-45 minutes

Code Archaeologist performs broad reconnaissance to create "site map":
- **File Structure Analysis**: Directory organization, naming conventions, module boundaries
- **Technology Detection**: Languages, frameworks, libraries, build tools
- **Entry Point Identification**: Main files, initialization code, API endpoints
- **Historical Context**: Git history, major commits, contributor patterns
- **Documentation Review**: Existing READMEs, comments, wiki pages

**Deliverable**: "Site Map" document with high-level overview and dig strategy

### Stage 2: Parallel Excavation
**Duration**: ~60-90 minutes (all agents work simultaneously)

Multiple specialists investigate their domains in parallel:

**System Architect**:
- Map component relationships and boundaries
- Trace data flow through the system
- Identify architectural patterns (MVC, microservices, etc.)
- Document integration points and APIs
- Create component interaction diagrams

**Security Auditor**:
- Identify authentication and authorization mechanisms
- Trace credential and secret management
- Find input validation patterns
- Discover security-critical code paths
- Flag potential vulnerabilities

**Performance Optimizer**:
- Trace hot paths and critical workflows
- Identify resource bottlenecks
- Find caching strategies
- Discover database query patterns
- Note performance-critical sections

**Test Engineer**:
- Catalog existing test suites
- Measure test coverage
- Identify coverage gaps
- Evaluate test quality and patterns
- Note testing frameworks and approaches

**Deliverable**: Four specialized analysis reports

### Stage 3: Stratigraphy Analysis (Code Archaeologist)
**Duration**: ~45 minutes

Code Archaeologist synthesizes parallel findings to identify architectural "layers":

**Chronological Layers**:
- Original implementation (v1.0 patterns)
- Major refactorings and when they occurred
- Framework migrations or upgrades
- Design pattern evolution

**Architectural Layers**:
- Data access layer
- Business logic layer
- Presentation layer
- Integration layer

**Technical Debt Layers**:
- Quick fixes and workarounds
- Deprecated patterns still in use
- Incomplete migrations
- "TODO" archaeology

**Deliverable**: System evolution timeline and architectural layer diagram

### Stage 4: Knowledge Crystallization (Documentation Scribe)
**Duration**: ~60 minutes

Documentation Scribe compiles all findings into structured artifacts:

1. **Architecture Diagrams**:
   - High-level system overview
   - Component interaction diagrams
   - Data flow diagrams
   - Deployment architecture

2. **Dependency Graph**:
   - Module dependencies
   - External dependencies
   - Circular dependencies highlighted
   - Coupling analysis

3. **Risk Assessment**:
   - Security vulnerabilities (categorized by severity)
   - Performance bottlenecks (with impact estimates)
   - Technical debt hotspots
   - Test coverage gaps

4. **New Developer Onboarding Guide**:
   - "How to get started" walkthrough
   - Key concepts and terminology
   - Code navigation guide
   - Common development workflows
   - What the code *actually* does vs. what it was *supposed* to do

**Deliverable**: Complete documentation package

### Stage 5: Excavation Report (Code Archaeologist)
**Duration**: ~30 minutes

Code Archaeologist delivers final comprehensive report:

**Critical Technical Debt** (High Priority):
- Security vulnerabilities requiring immediate attention
- Performance issues impacting users
- Stability risks

**Refactoring Opportunities** (Medium Priority):
- Code quality improvements
- Pattern standardization
- Dependency cleanup

**Hidden Gems** (Preserve):
- Well-designed components worth protecting
- Clever solutions to hard problems
- Reusable utilities

**Safe Modernization Paths**:
- Incremental upgrade strategy
- Low-risk refactoring targets
- Test-first improvement areas

**Deliverable**: Prioritized action plan with recommendations

## Inputs Required

- **Codebase Access**: Repository URL or local path
- **Context**: Why we're analyzing this code (acquisition, refactor, onboarding, etc.)
- **Focus Areas**: Any specific concerns or areas of interest
- **Time Constraints**: Urgency level (affects depth of analysis)

## Outputs Produced

1. **Site Map** - High-level overview and entry points
2. **Architecture Diagrams** - Visual system representation
3. **Dependency Graph** - Module and external dependencies
4. **Security Assessment** - Vulnerabilities and security patterns
5. **Performance Profile** - Bottlenecks and optimization opportunities
6. **Test Coverage Report** - Gaps and quality assessment
7. **Evolution Timeline** - How the system grew over time
8. **Onboarding Guide** - New developer documentation
9. **Prioritized Action Plan** - Recommendations with rationale

## Success Criteria

✅ Comprehensive understanding of system architecture
✅ All major components and their relationships documented
✅ Critical risks identified and prioritized
✅ New developers can onboard using produced documentation
✅ Clear, actionable recommendations for improvement

## When to Use This Flow

**Good for**:
- Inheriting a legacy codebase with minimal documentation
- Joining a new team mid-project
- Conducting due diligence on acquisition targets
- Preparing a system for major modernization
- Onboarding multiple new developers
- Post-mortem after major incidents

**Not ideal for**:
- Well-documented modern codebases
- Greenfield projects
- Simple, small codebases (< 1000 LOC)
- Urgent production issues (use faster targeted analysis)

## Example Scenarios

### Scenario 1: Acquisition Due Diligence
**Context**: Company acquiring startup, needs to assess codebase quality
**Focus**: Security risks, technical debt, maintainability
**Output**: Risk assessment report with acquisition recommendations

### Scenario 2: New CTO Onboarding
**Context**: New technical leader needs to understand existing system
**Focus**: Architecture, team capabilities, improvement opportunities
**Output**: System overview with strategic improvement roadmap

### Scenario 3: Legacy Modernization
**Context**: 5-year-old monolith needs microservices migration
**Focus**: Component boundaries, coupling analysis, safe extraction paths
**Output**: Incremental migration strategy with risk mitigation

## Variations

### Rapid Reconnaissance (4 hours)
- Code Archaeologist only
- Focus on architecture and critical risks
- Minimal documentation
- Used for quick assessments

### Deep Excavation (2-3 days)
- Add Database Specialist for data architecture
- Add DevOps Engineer for deployment patterns
- Include user interview analysis
- Create video walkthrough in addition to docs

### Security-Focused Dig
- Lead by Security Auditor instead
- Add Compliance Specialist
- Deep dive on authentication, authorization, data protection
- Output: Comprehensive security audit report

## Anti-Patterns to Avoid

❌ **Premature Refactoring**: Don't start changing code during analysis
❌ **Analysis Paralysis**: Set time box and stick to it
❌ **Ignoring Git History**: Version control tells important stories
❌ **Solo Investigation**: Parallel specialists catch more than single reviewer
❌ **Documentation Debt**: Write findings immediately, not "later"

## Lessons Learned

_(To be filled in after first execution)_

## Related Flows

- **The Architecture X-Ray** - Similar but focuses more on patterns than history
- **Technical Debt Archaeology** - Natural follow-up for remediation
- **Knowledge Archaeology** - Use for documentation-heavy codebases
- **Fortress Protocol** - Use if security issues discovered

---

**This flow treats code archaeology as a systematic discipline - like excavating an ancient city layer by layer - ensuring nothing critical is overlooked.** 🏛️✨
