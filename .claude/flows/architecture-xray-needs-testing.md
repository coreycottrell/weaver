# The Architecture X-Ray

**Status**: 🧪 Needs Testing
**Proposed by**: Pattern Detector
**Pattern Type**: Hybrid (Parallel Investigation → Sequential Analysis → Parallel Documentation)

## Purpose

Deep-dive analysis of an unfamiliar codebase to extract architectural patterns, conventions, anti-patterns, and create a comprehensive understanding map - providing "X-ray vision" into the system's design philosophy.

## Agents Involved

- **Pattern Detector** (Lead) - Orchestrates analysis and synthesizes patterns
- **Code Archaeologist** - Discovers historical context and evolution
- **Security Sentinel** - Identifies security patterns and risks
- **Performance Optimizer** - Spots performance patterns and inefficiencies
- **Documentation Sage** - Creates final knowledge artifacts

## Flow Stages

### Stage 1: Parallel Discovery Phase
**Duration**: ~60 minutes

Three specialists simultaneously scan codebase from specialized perspectives:

**Code Archaeologist**:
- File organization and module structure
- Technology choices and their evolution
- Code style and formatting patterns
- Historical decision points (via git history)

**Security Sentinel**:
- Authentication and authorization patterns
- Input validation approaches
- Secret management strategies
- Security-critical code paths

**Performance Optimizer**:
- Caching strategies
- Database access patterns
- Resource management approaches
- Performance-critical code paths

**Deliverable**: Three specialized perspective reports

### Stage 2: Pattern Synthesis (Pattern Detector)
**Duration**: ~45 minutes

Pattern Detector receives all findings and identifies:

**Cross-Cutting Architectural Patterns**:
- Overall architectural style (layered, hexagonal, microservices, etc.)
- Communication patterns (event-driven, synchronous, async)
- State management approach
- Error handling philosophy

**Common Design Principles**:
- Separation of concerns
- Dependency injection usage
- Interface abstraction levels
- Code organization philosophy

**Prevalent Anti-Patterns**:
- God objects or classes
- Circular dependencies
- Tight coupling hotspots
- Violation of SOLID principles

**Underlying Philosophy**:
- Pragmatic vs. idealistic
- Performance vs. maintainability priorities
- Security posture (defense in depth vs. trust-based)

**Deliverable**: Pattern synthesis document with examples

### Stage 3: Convention Mapping (Pattern Detector)
**Duration**: ~30 minutes

Create hierarchical map of discovered patterns from high-level to code-level:

**High-Level Architecture**:
- System decomposition strategy
- Component boundaries and responsibilities
- Integration and communication patterns

**Mid-Level Patterns**:
- Module organization
- Class design patterns (Factory, Strategy, Observer, etc.)
- Data access patterns

**Code-Level Conventions**:
- Naming conventions (variables, functions, classes, files)
- Error handling conventions
- Testing approaches and patterns
- Comment and documentation style

**Deliverable**: Hierarchical convention map

### Stage 4: Anti-Pattern Triage (Pattern Detector)
**Duration**: ~30 minutes

Categorize identified anti-patterns by severity and impact:

**Critical (Fix Immediately)**:
- Security vulnerabilities
- Data corruption risks
- Performance killers

**High (Fix Soon)**:
- Major maintainability issues
- Significant technical debt
- Architectural violations blocking new features

**Medium (Refactor Opportunistically)**:
- Code smells
- Minor inconsistencies
- Suboptimal patterns

**Low (Document and Monitor)**:
- Style inconsistencies
- Optimization opportunities
- Nice-to-have improvements

Each categorized issue includes:
- Specific file locations and line numbers
- Why it's problematic
- Refactoring recommendations
- Estimated effort to fix

**Deliverable**: Anti-pattern triage report

### Stage 5: Knowledge Crystallization (Documentation Sage)
**Duration**: ~45 minutes

Create multiple knowledge artifacts:

**1. Architecture Diagram** (ASCII/Mermaid):
```
┌─────────────┐
│   Client    │
└──────┬──────┘
       │
┌──────▼──────┐
│  API Layer  │
└──────┬──────┘
       │
┌──────▼──────┐
│   Business  │
│    Logic    │
└──────┬──────┘
       │
┌──────▼──────┐
│ Data Access │
└─────────────┘
```

**2. Pattern Catalog**:
- Name and description of each pattern
- Where it's used (file locations)
- Why it's appropriate (or not)
- Examples from codebase

**3. Convention Guide**:
- "How we do X in this codebase"
- Naming standards
- File organization rules
- Testing conventions
- Documentation expectations

**4. Technical Debt Map**:
- Visual representation of anti-patterns
- Severity heat map
- Refactoring priority order
- Estimated effort and impact

**Deliverable**: Complete documentation package

## Inputs Required

- **Codebase Path**: Repository or local directory
- **Analysis Scope**: Full codebase or specific modules
- **Focus Areas**: Any particular concerns (security, performance, maintainability)
- **Existing Documentation**: Links to any existing architecture docs

## Outputs Produced

1. **Pattern Synthesis Document** - Cross-cutting patterns and philosophy
2. **Hierarchical Convention Map** - From architecture to code-level conventions
3. **Anti-Pattern Triage Report** - Prioritized issues with locations and fixes
4. **Architecture Diagram** - Visual system representation
5. **Pattern Catalog** - Detailed pattern documentation
6. **Convention Guide** - How to write code consistent with codebase
7. **Technical Debt Map** - Visual representation of issues

## Success Criteria

✅ All major architectural patterns identified and documented
✅ Conventions cataloged at all levels (architecture to code)
✅ Anti-patterns categorized by severity with specific locations
✅ New developers can understand "how we do things here"
✅ Technical debt is visible and prioritized

## When to Use This Flow

**Good for**:
- Joining a new project
- Inheriting legacy code
- Evaluating acquisition targets
- Onboarding new developers
- Before major refactoring initiatives
- After discovering "mystery" behavior

**Not ideal for**:
- Well-documented codebases with current architecture docs
- Greenfield projects
- Codebases under 500 LOC
- When you just need to fix one specific bug

## Example Scenarios

### Scenario 1: New Team Member Onboarding
**Input**: React/Node.js web application (10K LOC)
**Output**: Comprehensive guide showing "this is how we organize components, handle state, test features, etc."

### Scenario 2: Pre-Refactor Assessment
**Input**: Monolithic Rails app being considered for microservices
**Output**: Pattern analysis showing which boundaries are clean and which are tangled

### Scenario 3: Technical Debt Planning
**Input**: 3-year-old codebase with growing maintenance burden
**Output**: Prioritized technical debt map guiding quarterly improvement sprints

## Variations

### Quick Pattern Scan (2 hours)
- Pattern Detector works solo
- Focus only on high-level architecture patterns
- Minimal documentation

### Security-Focused X-Ray
- Security Sentinel leads analysis
- Deep dive on security patterns
- Threat modeling based on discovered patterns

### Performance-Focused X-Ray
- Performance Optimizer leads analysis
- Focus on performance patterns and anti-patterns
- Includes profiling data analysis

## Lessons Learned

_(To be filled in after first execution)_

## Related Flows

- **The Archaeological Dig** - More focused on history and evolution
- **Technical Debt Archaeology** - Natural follow-up for remediation
- **Semantic Harmonization** - Use if naming inconsistencies discovered

---

**This flow provides X-ray vision into a codebase, revealing the implicit design philosophy and patterns that define "how we do things here."** 🔬✨
