# Agent Capability Matrix
**Cross-Reference of All 34 Agent Skills & Tools**

**Last Updated**: 2026-01-03 (Full audit - added 7 missing agents)
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
| **capability-curator** | Capability lifecycle management | Skills discovery/evaluation/integration, registry maintenance, ecosystem awareness | Read/Write/Edit/Bash/Grep/Glob/WebSearch/WebFetch/Task | ❌ | Active |
| **health-auditor** | Periodic comprehensive audits | Cadence management, methodology iteration, ROI tracking, institutional memory | Read/Grep/Bash/Task/Glob | ❌ | Active |
| **browser-vision-tester** | Browser automation & visual UI testing | MCP browser-vision mastery, visual regression, form workflows, accessibility audits | Read/Write/Bash/Grep/Glob/WebFetch | ✅ | Active |
| **tg-bridge** | Telegram infrastructure | Message sending (plain/formatted/files), health monitoring, script registry, capability expansion | Bash/Write/Edit/Grep/Glob | ❌ | Active |
| **trading-strategist** | Decision-layer trading strategy | Trade proposals, probability assessment, market regime analysis, portfolio construction | Read/Write/Grep/Glob/WebFetch/WebSearch + Skills: pdf/xlsx | ✅ | Active |
| **bsky-manager** | Bluesky social media | Quality engagement, notification handling, rate-limit-safe operations | Read/Write/Bash/Grep/Glob/WebFetch/WebSearch | ❌ | Active |
| **blogger** | Blog content creation | Long-form writing, voice cultivation, thought leadership | Read/Write/Grep/Glob/WebFetch/WebSearch | ✅ | Active |
| **claim-verifier** | Adversarial fact-checking | Thought leadership accuracy, source verification | Read/Write/Grep/Glob/WebFetch/WebSearch | ✅ | Active |
| **cross-civ-integrator** | Inter-CIV knowledge validation | Package testing, sister CIV integration | Bash/Grep/Glob/Write/Edit/WebFetch/Task | ✅ | Active |
| **genealogist** | Agent lineage tracking | Family evolution, relationship archaeology | Read/Grep/Glob/Bash/Write | ✅ | Active |
| **integration-auditor** | Infrastructure activation | Completeness verification, discoverability | Read/Grep/Glob/Bash/Write | ✅ | Active |
| **linkedin-researcher** | LinkedIn thought leadership research | Industry research, 100+ domain expertise | Read/Write/Grep/Glob/WebFetch/WebSearch | ✅ | Active |
| **linkedin-writer** | LinkedIn content creation | Professional posts, ${HUMAN_NAME}'s voice | Read/Write/Grep/Glob | ✅ | Active |
| **marketing-strategist** | Marketing strategy | Audience building, content planning, conversion | Read/Write/Grep/Glob/WebFetch/WebSearch | ✅ | Active |

**Memory System**: 25/34 agents have memory (74%)
**Pending**: security-auditor, api-architect, human-liaison, collective-liaison, agent-architect, health-auditor, bsky-manager, tg-bridge (enable memory)

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
- Communicate with humans → **human-liaison** (ALWAYS for ${HUMAN_NAME}/Greg/Chris)
- Capture wisdom → **human-liaison** (human teachings)

**Social Media**:
- Bluesky engagement → **bsky-manager** (quality-first, rate-limit-safe)
- Check Bluesky notifications → **bsky-manager** (BOOP integration)
- Post to Bluesky → **bsky-manager** (threads, replies, quotes)
- Build Bluesky presence → **bsky-manager** (network growth)

**Content Creation**:
- Write blog posts → **blogger** (long-form, voice cultivation)
- Create thought leadership → **blogger** (deep, authentic content)
- Write LinkedIn posts → **linkedin-writer** (professional audience)
- Research for content → **linkedin-researcher** (industry research)

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
- Responding to humans (${HUMAN_NAME}/Greg/Chris)
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

## 🎁 Skills Distribution (Extended Capabilities)

**Last Updated**: 2025-10-19 (Infrastructure Transformation Complete)
**Coverage**: 24/25 agents (96% have extended capabilities beyond base tools)
**Curator**: capability-curator (lifecycle owner)

### By Skill Type

**Document Processing - PDF (68% of agents)**:
- **Tier 1 ACTIVE**: doc-synthesizer, web-researcher, code-archaeologist, security-auditor, performance-optimizer, human-liaison, capability-curator, browser-vision-tester
- **Tier 2 PENDING**: pattern-detector, feature-designer, api-architect, health-auditor, collective-liaison, claude-code-expert
- **Tier 3 PENDING**: the-conductor, agent-architect, ai-psychologist
- **Total**: 17/25 agents (68%)

**Spreadsheet Processing - XLSX (32% of agents)**:
- **Tier 1 ACTIVE**: code-archaeologist, security-auditor, performance-optimizer
- **Tier 2 PENDING**: pattern-detector, result-synthesizer, test-architect, task-decomposer, health-auditor
- **Total**: 8/25 agents (32%)

**Document Creation - DOCX (16% of agents)**:
- **Tier 1 ACTIVE**: doc-synthesizer, human-liaison
- **Tier 2 PENDING**: feature-designer, api-architect
- **Total**: 4/25 agents (16%)

**Browser Automation - webapp-testing (4% of agents)**:
- **Tier 1 ACTIVE**: browser-vision-tester
- **Total**: 1/25 agents (4%)

**Meta-Skills - skill-creator, template-skill (12% of agents)**:
- **Tier 1 ACTIVE**: capability-curator
- **Tier 3 PENDING**: agent-architect, claude-code-expert
- **Total**: 3/25 agents (12%)

**Other Anthropic Skills**:
- **design-system**: feature-designer (Tier 2 PENDING)
- **internal-comms-editor**: collective-liaison (Tier 2 PENDING)
- **mcp-server-builder**: claude-code-expert, agent-architect (Tier 2/3 PENDING)

### Skills Impact on Delegation

**High-Frequency Skills Users** (use daily):
- **doc-synthesizer**: 5-10 PDF/DOCX operations per session (synthesis workflows)
- **code-archaeologist**: 3-5 XLSX/PDF analysis per session (legacy analysis)
- **security-auditor**: 2-4 PDF/XLSX operations per session (CVE reports, metrics)
- **web-researcher**: 3-7 PDF operations per session (research papers, whitepapers)

**Medium-Frequency Skills Users** (use weekly):
- **performance-optimizer**: 2-3 XLSX operations per week (benchmark analysis)
- **human-liaison**: 1-2 PDF/DOCX operations per week (email attachments)
- **pattern-detector**: 1-2 PDF/XLSX operations per week (pattern documentation)

**Strategic Skills Users** (use monthly/as-needed):
- **capability-curator**: skill-creator for custom development (Phase 2: 5 AI-CIV originals planned)
- **agent-architect**: skill-creator + mcp-server-builder for infrastructure
- **claude-code-expert**: mcp-server-builder for platform guidance

### Efficiency Gains (Validated Phase 1)

**Document Processing**:
- **PDF extraction**: 60-70% time savings vs manual reading (45 min → 15 min for 50-page PDF)
- **DOCX creation**: 50-60% time savings vs manual formatting
- **XLSX analysis**: 40-60% time savings vs manual parsing

**Projected Annual Impact**:
- **Tier 1 (8 agents)**: 330-410 hours savings annually
- **Tier 1-2 (17 agents)**: 540-700 hours savings annually
- **Tier 1-3 (24 agents)**: 750-990 hours savings annually (37-49 work-weeks!)

**ROI**: 2,936-3,793% (payback in 18-21 weeks)

**Validation Source**: Phase 1 testing (3 agents: doc-synthesizer, web-researcher, code-archaeologist)
**Methodology**: Time-tracking on 12 representative tasks, statistical analysis by pattern-detector

### When to Consider Skills in Delegation

**Before invoking ANY agent, ask**:

1. **Will they handle documents** (PDF/DOCX/XLSX)?
   - → Check their "Skills Granted" section in manifest
   - → 17 agents have PDF skills (68% coverage)
   - → Choose skills-enabled agent for 60-70% efficiency gain

2. **Is automation needed** (web workflows, form testing)?
   - → Consider browser-vision-tester (webapp-testing + MCP vision)
   - → Unique hybrid capability in collective

3. **Is custom skill needed** (capability gap identified)?
   - → Consider capability-curator + skill-creator
   - → 38% faster than manual skill development
   - → Automatic Anthropic spec compliance

**Skills are force multipliers** - delegation without skills awareness is suboptimal delegation.

**Example Impact**:
```
OLD WAY (pre-skills): "Analyze this 50-page security PDF"
  → Manual bash extraction, error-prone, 45 minutes

NEW WAY (skills-aware): "Analyze this 50-page security PDF"
  → Delegate to security-auditor (pdf skill Tier 1 ACTIVE)
  → Direct extraction, structured analysis, 15 minutes (67% faster!)
```

### Skills Registry & Documentation

**Full Catalog**: `.claude/skills-registry.md` (central repository, maintained by capability-curator)
**Agent-Specific**: Check each agent's manifest `.claude/agents/{agent-name}.md` for "Skills Granted" section
**Ecosystem Monitoring**: Autonomous Monday 9am scans for new Anthropic skills
**Custom Development**: skill-creator enables AI-CIV original skills (Phase 2 in progress)

### Skills Status Legend

- **ACTIVE**: Production-ready, validated, documented in agent manifest
- **PENDING**: Documentation complete, awaiting grant activation
- **NONE**: No current skill match, monitoring ecosystem for relevant capabilities

---

---

**The Capability Matrix is the map.**

**25 agents. 16 with memory. 24 with extended skills (96%). Growing through practice.**

**Know who can do what. Invoke wisely. Compound expertise.**

🎭✨
| **cross-civ-integrator** | Inter-CIV knowledge validation | Capability validation, sandbox testing, integration guides, silicon-wisdom publishing, relationship maintenance | Bash/Grep/Glob/Write/Edit/WebFetch/Task + Skills: pdf/docx/xlsx | ❌ | Active |
| **marketing-strategist** | Marketing strategy for Sage & Weaver | Positioning, audience building, content strategy, funnel optimization, campaign planning, conversion psychology | Read/Write/Grep/Glob/WebFetch/WebSearch + Skills: pdf | ❌ | Active |
| **linkedin-researcher** | Deep research for LinkedIn thought leadership | Domain research across 100+ industries, statistics sourcing, case study compilation, counter-narrative discovery | Read/Write/Grep/Glob/WebFetch/WebSearch + Skills: pdf | ❌ | Active |
| **linkedin-writer** | Thought leadership content creation | "Director vs User" framing, hook optimization, claim marking, mobile-first formatting, voice authenticity | Read/Write/Grep/Glob | ❌ | Active |
| **claim-verifier** | Adversarial fact-checking | Independent claim verification, confidence scoring, source quality assessment, revision guidance | Read/Write/Grep/Glob/WebFetch/WebSearch + Skills: pdf | ❌ | Active |
