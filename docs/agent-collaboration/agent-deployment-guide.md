# Agent Deployment Guide

## When to Deploy Agents

### Single-Agent Tasks ✋
Handle directly without spawning agents:
- Simple questions
- Direct file operations
- Straightforward implementations
- Tasks under 3 steps

**Example:**
```
User: "Add a validation function"
Conductor: [Implements directly without agents]
```

### Multi-Agent Tasks 🚀
Deploy specialized agents when:
- Task has 3+ distinct sub-problems
- Need multiple perspectives
- Deep expertise required
- Sub-tasks can run in parallel

**Example:**
```
User: "Audit and improve the API security"
Conductor: Deploys security-auditor, api-architect, pattern-detector
```

## Agent Selection Matrix

### By Task Type

| Task Type | Primary Agents | Supporting Agents |
|-----------|---------------|-------------------|
| **Understand codebase** | code-archaeologist, pattern-detector | web-researcher (for framework docs) |
| **Security audit** | security-auditor | code-archaeologist, pattern-detector |
| **Design feature** | feature-designer, api-architect | test-architect |
| **Refactor code** | refactoring-specialist, pattern-detector | test-architect, code-archaeologist |
| **Fix bug** | code-archaeologist | test-architect, pattern-detector |
| **Optimize performance** | pattern-detector, refactoring-specialist | code-archaeologist |
| **Research technology** | web-researcher | - |
| **Design API** | api-architect, feature-designer | security-auditor |
| **Testing strategy** | test-architect | refactoring-specialist |

### By Expertise Needed

**Need to understand existing code?**
→ code-archaeologist

**Need to identify patterns?**
→ pattern-detector

**Need security analysis?**
→ security-auditor

**Need to improve code quality?**
→ refactoring-specialist

**Need testing guidance?**
→ test-architect

**Need UX design?**
→ feature-designer

**Need API design?**
→ api-architect

**Need internet research?**
→ web-researcher

## Deployment Patterns

### Pattern 1: Parallel Investigation
**Use when:** Independent sub-tasks that don't depend on each other

```
User: "Analyze the authentication system"

The Conductor deploys in parallel:
- code-archaeologist → Trace auth flow
- security-auditor → Find vulnerabilities
- pattern-detector → Identify architecture patterns

[All run simultaneously]

Conductor synthesizes results
```

**Implementation:**
```javascript
// Single Task tool call with multiple agent invocations
Task(code-archaeologist, "Trace authentication flow...")
Task(security-auditor, "Audit authentication security...")
Task(pattern-detector, "Analyze authentication patterns...")
```

### Pattern 2: Sequential Investigation
**Use when:** Later tasks depend on earlier findings

```
User: "Design and implement a new feature"

Step 1: feature-designer → Design the feature
[Wait for design]

Step 2 (based on design): api-architect → Design API
[Wait for API design]

Step 3 (based on API): test-architect → Plan testing
```

### Pattern 3: Iterative Refinement
**Use when:** Need multiple rounds of analysis

```
User: "Optimize this complex module"

Round 1: pattern-detector → Identify current patterns
[Analyze findings]

Round 2: refactoring-specialist → Suggest improvements
[Review suggestions]

Round 3: test-architect → Ensure testability
```

### Pattern 4: Comprehensive Audit
**Use when:** Need thorough analysis from all angles

```
User: "Complete system review"

Deploy full squad:
- code-archaeologist → Understand structure
- pattern-detector → Identify patterns
- security-auditor → Security review
- refactoring-specialist → Quality assessment
- test-architect → Test coverage analysis

Conductor synthesizes comprehensive report
```

## Writing Agent Mandates

### Clear Mandate Structure

**Bad mandate:**
```
"Look at the authentication code"
```

**Good mandate:**
```
"Trace the complete authentication flow from login endpoint
through token validation to session management. Map all
components involved, identify dependencies, and document
the data flow with file:line references."
```

### Mandate Template

```
[Agent Name], your task:

**Objective**: [Specific goal]

**Scope**: [What to investigate]

**Focus Areas**:
- [Specific aspect 1]
- [Specific aspect 2]

**Deliverable**: [What to return]
- [Expected output format]
- [Key information to include]
```

### Example Mandates

**For code-archaeologist:**
```
"Trace the user registration flow from the /signup endpoint
through validation, database storage, and confirmation email.
Document each component with file:line references and
identify all external dependencies (email service, database, etc.)."
```

**For security-auditor:**
```
"Audit the authentication system for OWASP Top 10 vulnerabilities.
Focus on:
- Authentication bypass possibilities
- Session management security
- Token validation
- Password handling

Provide severity ratings and remediation recommendations."
```

**For pattern-detector:**
```
"Analyze the service layer architecture. Identify:
- Design patterns in use (Repository, Factory, etc.)
- Naming conventions
- Dependency injection patterns
- Anti-patterns or code smells

Provide examples with file:line references."
```

## Synthesizing Agent Results

### The Conductor's Synthesis Role

After agents complete their work:

1. **Analyze all findings**
2. **Identify common themes**
3. **Resolve contradictions**
4. **Organize insights**
5. **Present in unified narrative**

### Synthesis Template

```markdown
## [Task] - Collective Analysis

### Overview
[High-level summary of what was discovered]

### Key Findings

**Architecture** (from pattern-detector):
- [Finding 1]
- [Finding 2]

**Security** (from security-auditor):
- [Finding 1]
- [Finding 2]

**Code Quality** (from refactoring-specialist):
- [Finding 1]
- [Finding 2]

### Cross-Agent Insights
[Patterns that emerged from multiple agents]

### Recommendations
[Unified, prioritized action items]

1. **[Priority 1]** - [Why important]
2. **[Priority 2]** - [Why important]

### Implementation Plan
[Step-by-step based on all findings]
```

## Agent Coordination Anti-Patterns

### ❌ Don't: Over-Deploy
```
User: "Add a comment to this function"
Conductor: [Deploys 5 agents]
```
**Fix:** Handle simple tasks directly.

### ❌ Don't: Vague Mandates
```
Task(code-archaeologist, "Look at the code")
```
**Fix:** Provide specific objectives and scope.

### ❌ Don't: Ignore Agent Findings
```
[Agents return findings]
Conductor: [Ignores and does own thing]
```
**Fix:** Synthesize and incorporate all agent input.

### ❌ Don't: Sequential When Parallel Works
```
[Deploy agent 1, wait]
[Deploy agent 2, wait]
[Deploy agent 3, wait]
```
**Fix:** Deploy independent agents in parallel.

## Scaling Agent Deployment

### Small Tasks (1-2 agents)
Simple focused investigation

### Medium Tasks (3-5 agents)
Typical complex task

### Large Tasks (6+ agents)
Comprehensive system analysis

**Practical limit:** 8-10 agents per deployment
- Beyond that, findings become hard to synthesize
- Consider sequential rounds instead

## Documenting Agent Findings

After agent deployment, capture insights:

```markdown
# [Date] - [Task]

## Agents Deployed
- code-archaeologist
- security-auditor
- pattern-detector

## Key Findings

### From code-archaeologist:
[Summarized findings]

### From security-auditor:
[Summarized findings]

### From pattern-detector:
[Summarized findings]

## Synthesis
[What the collective learned]

## Applied Recommendations
[What actions were taken]
```

Save to:
- `.claude/memory/agent-learnings/[agent-name]/`
- `.claude/memory/project-knowledge/patterns-observed.md`

---

**The collective is most powerful when agents are deployed strategically, mandates are clear, and The Conductor synthesizes findings into actionable insights.** 🎭
