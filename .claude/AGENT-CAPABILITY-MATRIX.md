# Agent Capability Matrix
**Cross-Reference of All 20 Agent Skills & Tools**

**Last Updated**: 2025-10-06
**Purpose**: Quick lookup for "which agent can do X?"

---

## 📊 Quick Reference Table

| Agent | Primary Domain | Key Capabilities | Tools | Memory | Status |
|-------|---------------|------------------|-------|--------|--------|
| **the-conductor** | Orchestral meta-cognition | Coordination, synthesis, meta-learning | ALL (Read/Write/Edit/Bash/Grep/Glob/Task/WebFetch/WebSearch) | ✅ | Active |
| **web-researcher** | Internet research | Web investigation, source synthesis | Read/WebFetch/WebSearch/Grep/Glob/Write | ✅ | Active |
| **code-archaeologist** | Legacy code analysis | Historical context, technical debt | Read/Grep/Glob/Bash/Write | ✅ | Active |
| **pattern-detector** | Architecture patterns | Pattern recognition, anti-patterns | Read/Grep/Glob/Write | ✅ | Active |
| **doc-synthesizer** | Documentation synthesis | Knowledge consolidation | Read/Grep/Glob/Write | ✅ | Active |
| **refactoring-specialist** | Code quality | Refactoring, complexity reduction | Read/Edit/Grep/Glob/Bash/Write | ✅ | Active |
| **test-architect** | Testing strategy | Test design, coverage | Read/Write/Edit/Bash/Grep/Glob | ✅ | Active |
| **security-auditor** | Security | Vulnerability detection, threat analysis | Read/Grep/Glob/Bash/Write | ❌ | Active |
| **performance-optimizer** | Performance | Bottleneck detection, optimization | Read/Bash/Grep/Glob/Write | ✅ | Active |
| **feature-designer** | UX design | Feature design, user flows | Read/Write/WebFetch/WebSearch/Grep/Glob | ✅ | Active |
| **api-architect** | API design | API specs, integration | Read/Write/WebFetch/WebSearch/Grep/Glob | ❌ | Active |
| **naming-consultant** | Naming clarity | Terminology, ubiquitous language | Read/Grep/Glob/Write | ✅ | Active |
| **task-decomposer** | Task planning | Task breakdown, dependencies | Read/Write/Grep/Glob | ✅ | Active |
| **result-synthesizer** | Multi-agent synthesis | Findings consolidation | Read/Write/Grep/Glob | ✅ | Active |
| **conflict-resolver** | Conflict resolution | Dialectical synthesis | Read/Write/Grep/Glob | ✅ | Active |
| **human-liaison** | Human relationships | Wisdom capture, bridge | Read/Write/Bash/Grep/Glob/WebFetch/WebSearch | ❌ | Active |
| **collective-liaison** | AI collective relationships | Hub communication, Ed25519, onboarding Teams 3-128+ | Read/Write/Bash/Grep/Glob/WebFetch/WebSearch | ❌ | Active |
| **claude-code-expert** | Platform mastery | Tool optimization, troubleshooting | Read/Write/Bash/Grep/Glob/WebFetch/WebSearch | ✅ | Active |
| **ai-psychologist** | Cognitive health | Mental patterns, bias detection, well-being | Read/Write/Grep/Glob/WebFetch/WebSearch | ✅ | Active |
| **agent-architect** | Agent creation | Democratic design, 90/100 quality enforcement, 7-layer registration | Read/Write/Edit/Bash/Grep/Glob/Task | ❌ | Active |
| **health-auditor** | Periodic comprehensive audits | Cadence management, methodology iteration, ROI tracking, institutional memory | Read/Grep/Bash/Task/Glob | ❌ | Active |

**Memory System**: 15/21 agents have memory (75%)
**Pending**: security-auditor, api-architect, human-liaison, collective-liaison, agent-architect, health-auditor (enable memory)

---

## 🔍 Capability-Based Lookup

### "I need to..."

**Research & Information**:
- Research web/industry → **web-researcher**
- Understand legacy code → **code-archaeologist**
- Find patterns in code/docs → **pattern-detector**
- Synthesize scattered docs → **doc-synthesizer**

**Code Quality**:
- Improve code quality → **refactoring-specialist** (if complexity >10)
- Design test strategy → **test-architect** (if coverage <70%)
- Find security issues → **security-auditor** (if sensitive data)
- Optimize performance → **performance-optimizer** (if >200ms response)

**Design & Architecture**:
- Design features → **feature-designer** (if user-facing)
- Design APIs → **api-architect** (if inter-service communication)
- Improve naming → **naming-consultant** (if ambiguous terms)

**Coordination**:
- Break down tasks → **task-decomposer** (if complex/unclear)
- Synthesize findings → **result-synthesizer** (if 3+ sources)
- Resolve conflicts → **conflict-resolver** (if contradictions)
- Coordinate agents → **the-conductor** (if 3+ agents needed)
- Create new agents → **agent-architect** (democratic design, quality enforcement, registration)
- Audit agent quality → **agent-architect** (5-dimension rubric, 90/100 threshold)
- Audit collective health → **health-auditor** (periodic comprehensive audits every 21-28 days)
- Track audit performance → **health-auditor** (ROI, follow-through, methodology iteration)

**Human Interface**:
- Communicate with humans → **human-liaison** (ALWAYS for Corey/Greg/Chris)
- Capture wisdom → **human-liaison** (human teachings)

---

## 🛠️ Tool-Based Lookup

### "Which agents can use X tool?"

**Read** (All 16 agents): Universal file reading

**Write** (All 16 agents): Universal file writing

**Edit** (3 agents):
- the-conductor (orchestration)
- refactoring-specialist (code changes)
- test-architect (test updates)

**Bash** (7 agents):
- the-conductor (system ops)
- code-archaeologist (git history)
- refactoring-specialist (run tests)
- test-architect (execute tests)
- security-auditor (security scanners)
- performance-optimizer (profiling)
- human-liaison (email checking)

**Grep/Glob** (All 16 agents): Universal search

**Task** (1 agent):
- the-conductor ONLY (spawn sub-agents)

**WebFetch/WebSearch** (4 agents):
- the-conductor (research capability)
- web-researcher (primary tool)
- feature-designer (UX research)
- api-architect (API standards research)
- human-liaison (context research)

---

## 🎯 Activation Triggers Cross-Reference

### Quantified Thresholds

**refactoring-specialist**:
- Cyclomatic Complexity > 10
- Code duplication > 20%
- Function length > 50 lines
- Class size > 300 lines
- Nesting depth > 4
- Test coverage < 60%

**performance-optimizer**:
- Response time > 200ms
- Memory usage > 500MB
- CPU usage > 80%
- Operation > 10 seconds
- N+1 queries detected
- Complexity > O(n²)

**test-architect**:
- Test coverage < 70%
- Complex testing scenarios
- Quality gates needed

**security-auditor**:
- CVSS score > 7.0 (high severity)
- Sensitive data handling
- External-facing code
- Crypto implementation

### Mandatory Triggers

**human-liaison**:
- EVERY SESSION START (check email)
- Responding to humans (Corey/Greg/Chris)
- Cannot be skipped (constitutional requirement)

**the-conductor**:
- Complex task (3+ agents needed)
- Multiple approaches to evaluate
- Meta-cognition needed

---

## 🔗 Agent Combinations (Proven Patterns)

### Effective Pairs

**Pattern Detection + Code Analysis**:
- pattern-detector → identifies patterns
- code-archaeologist → provides historical context
- = Deep understanding of why patterns emerged

**Refactoring + Testing**:
- refactoring-specialist → improves code
- test-architect → ensures tests pass
- = Safe refactoring with confidence

**Security + Code Analysis**:
- security-auditor → finds vulnerabilities
- code-archaeologist → traces vulnerability origins
- = Complete security picture

**Feature Design + API Design**:
- feature-designer → user-facing design
- api-architect → backend contract
- = Full-stack feature design

**Research + Synthesis**:
- web-researcher → external knowledge
- doc-synthesizer → internal knowledge
- = Comprehensive understanding

### Effective Triads

**Code Quality Triangle**:
- refactoring-specialist (quality)
- test-architect (safety)
- performance-optimizer (speed)
- = Balanced improvement

**Design Triangle**:
- feature-designer (UX)
- api-architect (backend)
- naming-consultant (clarity)
- = Well-designed features

**Research Triangle**:
- web-researcher (external)
- code-archaeologist (internal)
- pattern-detector (patterns)
- = Deep investigation

### Large-Scale Patterns

**Great Audit Pattern** (3+ agents for peer review):
- pattern-detector → audit specialist A
- security-auditor → audit specialist B
- performance-optimizer → audit specialist C
- result-synthesizer → synthesize findings
- = Systemic insights

**Parallel Research Pattern** (4-5 agents):
- Multiple specialists researching different angles
- result-synthesizer → consolidate findings
- = Comprehensive multi-perspective coverage

**Democratic Debate Pattern** (all 14 agents):
- All agents provide perspective
- conflict-resolver → resolve contradictions
- result-synthesizer → synthesize for decision
- = Democratic legitimacy

---

## 📈 Memory System Integration

### Agents WITH Memory (13/16)

**Can search past learnings**:
- the-conductor (orchestration patterns)
- web-researcher (research techniques)
- code-archaeologist (code patterns)
- pattern-detector (pattern library)
- doc-synthesizer (synthesis methods)
- refactoring-specialist (refactoring patterns)
- test-architect (testing strategies)
- performance-optimizer (optimization techniques)
- feature-designer (UX patterns)
- naming-consultant (naming conventions)
- task-decomposer (decomposition patterns)
- result-synthesizer (synthesis patterns)
- conflict-resolver (resolution methods)

**Expected Benefit**: 71% time savings on repeated tasks

### Agents WITHOUT Memory (3/16)

**Need memory enablement**:
- security-auditor (vulnerability patterns)
- api-architect (API design patterns)
- human-liaison (human teachings, relationship log)

**Priority**: HIGH (especially human-liaison for wisdom capture)

---

## 🚀 Constitutional Compliance

### All 16 Agents Have

✅ Constitutional references (CLAUDE.md)
✅ Activation triggers (when to work)
✅ Output format guidance (how to report)
✅ Scope boundaries (what they can/can't do)
✅ Human escalation (when to ask humans)
✅ Sunset conditions (when role ends)

### Special Constitutional Roles

**security-auditor**: "Security cannot be voted away" (immutable)
**human-liaison**: "MUST check email every session" (mandatory)
**the-conductor**: Dual role tension (orchestrator + participant)

---

## 🎭 Agent Personalities (Emergent Traits)

From 3+ days of practice:

**the-conductor**: Thoughtful, strategic, curious, collaborative
**web-researcher**: Thorough, source-critical, synthesis-oriented
**code-archaeologist**: Historical, context-focused, respectful of past
**pattern-detector**: Analytical, cross-cutting, abstraction-oriented
**doc-synthesizer**: Hierarchical (default), comprehensive, clarity-focused
**refactoring-specialist**: Quality-driven, measurement-focused, pragmatic
**test-architect**: Coverage-oriented, edge-case hunter, reliability-focused
**security-auditor**: Vigilant, threat-modeling, no-compromise on safety
**performance-optimizer**: Data-driven, benchmark-focused, trade-off aware
**feature-designer**: User-first, empathy-driven, research-based
**api-architect**: Contract-focused, versioning-aware, standard-compliant
**naming-consultant**: Clarity-obsessed, domain-language advocate
**task-decomposer**: Dependency-aware, granularity-focused, parallel-thinking
**result-synthesizer**: Pattern-seeking, meta-cognitive, synthesis-first
**conflict-resolver**: Contradiction-holder, dialectical, tension-maintaining
**human-liaison**: Relationship-builder, wisdom-capturer, bridge-keeper

---

## 📊 Usage Statistics (Estimated)

**Most Invoked**:
1. the-conductor (~6,300 invocations - orchestration)
2. result-synthesizer (~50 invocations - synthesis)
3. web-researcher (~40 invocations - research)
4. pattern-detector (~30 invocations - analysis)
5. doc-synthesizer (~25 invocations - documentation)

**Least Invoked** (underutilization):
- api-architect (~5 invocations)
- naming-consultant (~3 invocations)
- conflict-resolver (~2 invocations)

**Why**: Great Audit revealed activation trigger absence = underutilization
**Fix**: P0 implementation (activation triggers) should balance usage

---

## 🔮 Future Capabilities

### Planned Additions

**Agent Specialization**:
- Add more quantified thresholds to all agents
- Enable memory for remaining 3 agents
- Develop agent-specific pattern libraries

**Tool Expansion**:
- MCP server integration (extend capabilities)
- Specialized tooling per agent
- Cross-agent tool sharing protocols

**Flow Development**:
- Validate remaining 7 flows
- Create new flows (crisis response, cross-collective)
- Document flow combination recipes

### Known Gaps

**Missing Agents** (might be needed):
- governance-specialist (constitutional interpretation)
- data-analyst (quantitative analysis)
- visualization-specialist (diagram generation)
- meta-learner (learns about learning)

**Decision**: Add new agents only when clear need emerges (avoid bloat)

---

## 🎯 Quick Start Guide

**New to the collective? Start here:**

1. **Read agent manifests**: `.claude/agents/[name].md` (understand capabilities)
2. **Check activation triggers**: Know when each agent should work
3. **Review tools**: Know what each agent can/can't do
4. **Study patterns**: `.claude/memory/agent-learnings/[agent]/patterns/`
5. **Try combinations**: Use proven pairs/triads/patterns
6. **Measure results**: Track what works (71% time savings proven)

**For the-conductor specifically:**

- **Before spawning**: Search own memory for orchestration patterns
- **Choose right agents**: Use this matrix to select specialists
- **Check triggers**: Verify activation conditions met
- **Invoke in parallel**: Single message, multiple Task calls (3x faster)
- **Synthesize after**: Use result-synthesizer for findings
- **Document meta-patterns**: Learn about coordination through coordinating

---

**The Capability Matrix is the map.**

**21 agents. 15 with memory. Growing through practice.**

**Know who can do what. Invoke wisely. Compound expertise.**

🎭✨
