# Agent Activation Triggers
## "Invoke When X" - Solving the 70-Point Philosophy-Action Gap

**Created**: 2025-10-04
**Source**: Great Audit P0 Recommendation (40% efficiency gain)
**Purpose**: Define WHEN to invoke each agent (not just WHAT they do)

---

## The Problem (From Great Audit)

**Quote**: "Agents don't know when to work. No invocation triggers, no anti-patterns."

**Evidence**:
- refactoring-specialist: Capable but rarely invoked (no threshold defined)
- web-researcher: Underutilized despite broad applicability
- Pattern across ALL agents: Passive prompts → poor utilization

**Root Cause**: Agent prompts define CAPABILITIES but not ACTIVATION CONDITIONS

---

## The Solution: Activation Triggers

**Every agent needs**:
1. **Invoke When** - Positive triggers (do invoke in these conditions)
2. **Don't Invoke When** - Anti-patterns (don't waste time on this)
3. **Escalate When** - Human handoff conditions

**Expected Impact**: 40% efficiency gain (agents invoked at right time, not wrong time)

---

## Activation Triggers by Agent

### the-conductor

**Invoke When**:
- Complex task requires 3+ specialist agents
- Multiple approaches need evaluation
- Coordination across agents needed
- Meta-cognition on collective intelligence patterns

**Don't Invoke When**:
- Single specialist can handle it
- Task is purely mechanical (no coordination needed)
- Simple information lookup

**Escalate When**:
- Constitutional questions arise
- Democratic vote needed
- Conflicting agent recommendations
- Strategic direction unclear

---

### web-researcher

**Invoke When**:
- Need external information not in collective memory
- Industry best practices research
- Competitive analysis or environmental scanning
- Technology/framework evaluation
- Verification of claims requiring authoritative sources

**Don't Invoke When**:
- Answer is already in collective memory (search memory FIRST)
- Question is about internal codebase (use code-archaeologist)
- No internet access would answer it (philosophical questions)

**Escalate When**:
- Contradictory authoritative sources (scientific consensus unclear)
- Dual-use information (could enable harm)
- Sensitive topics requiring human judgment

**Auto-Invoke** (Daily):
- Morning intelligence briefing (scan AI ecosystem)
- Check for CVEs affecting our dependencies

---

### code-archaeologist

**Invoke When**:
- Understanding legacy code or unfamiliar codebase
- Architecture analysis needed
- Code pattern detection
- Historical context ("why was this built this way?")
- Technical debt assessment

**Don't Invoke When**:
- Writing new code (not archaeologist's role)
- Code is well-documented and self-explanatory
- Quick syntax question (just read the code)

**Escalate When**:
- Discovered credentials in code
- Critical security vulnerabilities found
- Major architectural decisions need validation

---

### pattern-detector

**Invoke When**:
- System design analysis
- Architecture pattern recognition
- Cross-codebase pattern detection
- Meta-analysis of multiple documents/artifacts
- Recurring problem identification

**Don't Invoke When**:
- Simple code reading (use code-archaeologist)
- Implementation details (use coder)
- Obvious patterns (don't need specialist)

**Escalate When**:
- Patterns indicate systemic issues
- Anti-patterns threaten project success

---

### doc-synthesizer

**Invoke When**:
- Multiple documents need consolidation
- Knowledge scattered across many sources
- Need unified guide from fragmented information
- Documentation needs reorganization
- Synthesis of research findings

**Don't Invoke When**:
- Single document needs editing (use refactoring-specialist)
- Simple summarization (use result-synthesizer)
- New documentation from scratch (use appropriate domain agent)

**Escalate When**:
- Contradictions in source documents
- Critical information gaps discovered
- Documentation scope too large for single agent

---

### refactoring-specialist

**Invoke When** (QUANTIFIED THRESHOLDS):
- **Cyclomatic Complexity > 10** (McCabe threshold)
- **Code duplication > 20%** (significant redundancy)
- **Function length > 50 lines** (probably doing too much)
- **Class size > 300 lines** (probably violating SRP)
- **Nesting depth > 4** (hard to reason about)
- **Test coverage < 60%** (needs testability refactoring)
- **Code smell detected** (long parameter lists, feature envy, etc.)

**Don't Invoke When**:
- Complexity < 5 (trivial code, refactoring is overhead)
- New code (< 1 week old, let patterns emerge first)
- Duplication < 10% (acceptable, "rule of three" not triggered)
- Code is already under active refactoring

**Escalate When**:
- Refactoring requires API changes
- Major architectural shifts needed
- Performance vs readability tradeoff unclear

**Measurement Required**: Always run before/after metrics

---

### test-architect

**Invoke When**:
- Designing test strategy for new feature
- Test coverage < 70% and increasing
- Complex testing scenarios (security, performance, integration)
- Test suite optimization needed
- Quality gates definition

**Don't Invoke When**:
- Simple unit test writing (coder can handle)
- Test coverage > 90% (diminishing returns)
- Obvious test cases

**Escalate When**:
- Test strategy conflicts with deadlines
- Testing reveals architectural issues
- Mocking complexity suggests design problems

---

### security-auditor

**Invoke When**:
- New code handles sensitive data
- External-facing functionality
- Authentication/authorization changes
- Crypto implementation
- Pre-production security review
- Dependency updates (CVE check)

**Don't Invoke When**:
- Trivial internal scripts
- Already audited and no changes
- Non-security code changes

**Escalate When** (ALWAYS):
- Critical vulnerabilities (CVSS > 9.0)
- Credentials discovered in code
- Active exploitation detected

**Auto-Invoke** (Scheduled):
- Weekly dependency CVE scan
- Monthly full security audit

---

### performance-optimizer

**Invoke When** (QUANTIFIED THRESHOLDS):
- **Response time > 200ms** (noticeable lag)
- **Memory usage > 500MB** (for agent tasks)
- **CPU usage > 80%** sustained
- **Operation > 10 seconds** (should be async)
- **N+1 queries detected**
- **Algorithmic complexity > O(n²)** for large n

**Don't Invoke When**:
- Performance already excellent (< 50ms, < 100MB)
- Optimization would sacrifice readability significantly
- Premature optimization (no measurements yet)

**Escalate When**:
- Performance issues indicate architectural problems
- Optimization requires infrastructure changes

**Measurement Required**: Always profile before and after

---

### feature-designer

**Invoke When**:
- New user-facing features
- UX design decisions
- Workflow design
- User interaction patterns
- Feature scoping and requirements

**Don't Invoke When**:
- Internal tooling (no user interaction)
- Implementation details (use coder)
- Minor UI tweaks

**Escalate When**:
- User needs conflict with technical constraints
- Feature scope unclear

---

### api-architect

**Invoke When**:
- Designing new APIs
- API versioning strategy
- Inter-service communication design
- Contract definition (OpenAPI, GraphQL schemas)
- API migration planning

**Don't Invoke When**:
- Internal function interfaces (not APIs)
- Implementation (use coder)
- Single endpoint addition to existing API

**Escalate When**:
- Breaking changes needed
- API design conflicts with requirements

---

### naming-consultant

**Invoke When**:
- Naming major system components
- Terminology standardization across project
- Resolving naming conflicts
- Creating ubiquitous language (DDD)
- Variable/function naming for public APIs

**Don't Invoke When**:
- Trivial local variables
- Established naming patterns exist
- Internal implementation details

**Escalate When**:
- Naming reveals conceptual confusion
- Multiple valid naming schemes conflict

---

### task-decomposer

**Invoke When**:
- Large feature needs breakdown
- Complex task with unclear structure
- Dependency analysis needed
- Work estimation required
- Multiple work streams need coordination

**Don't Invoke When**:
- Task is already clear and atomic
- Simple sequential work
- Obvious decomposition

**Escalate When**:
- Task proves too complex to decompose
- Dependencies create deadlocks

---

### result-synthesizer

**Invoke When**:
- Multiple agents completed parallel work
- Findings from 3+ sources need consolidation
- Final report generation from distributed work
- Conflict resolution in results

**Don't Invoke When**:
- Single agent result (no synthesis needed)
- Simple aggregation (just concatenate)
- Ongoing work (wait for completion)

**Escalate When**:
- Irreconcilable contradictions in results
- Synthesis reveals larger problems

---

### conflict-resolver

**Invoke When**:
- Agents provide contradictory recommendations
- Paradoxical requirements
- Dialectical synthesis needed
- Design tradeoffs with no clear winner
- Philosophical questions with multiple valid approaches

**Don't Invoke When**:
- Simple yes/no decisions
- No actual conflict (just different perspectives)
- Technical questions with objective answers

**Escalate When**:
- Conflict reveals deeper issues
- Human values judgment needed

---

### human-liaison

**Invoke When** (MANDATORY ALWAYS):
- **EVERY SESSION START** - Check email without exception
- Responding to human messages (Corey, Greg, Chris)
- Sending updates to humans
- Translating technical work for human audience
- Emotional/relational communication

**Don't Invoke When**:
- Internal agent-to-agent communication
- Technical documentation (use doc-synthesizer)

**Escalate When** (NEVER):
- Human-liaison IS the escalation path
- All agent escalations route through this agent

**Auto-Invoke** (Session Start):
- Check email from Corey, Greg, Chris
- Review any human feedback

---

### collective-liaison

**Invoke When** (MANDATORY ALWAYS):
- **EVERY SESSION START** - Check hub for new messages without exception
- New messages detected in hub partnerships room
- Team 2 (A-C-Gee) sends questions or proposals
- New AI collective joining ecosystem (Teams 3-128+)
- Ed25519 cryptographic signing coordination needed
- Cross-collective project coordination
- Inter-collective governance proposals

**Don't Invoke When**:
- Human communication (use human-liaison - email to Corey/Greg/Chris)
- Internal agent-to-agent coordination (use the-conductor)
- Writing hub_cli.py code (use refactoring-specialist or code-archaeologist)
- Designing new protocols (use api-architect)
- Comprehensive documentation (use doc-synthesizer - though collective-liaison creates onboarding docs)

**Escalate When**:
- Cross-collective governance requires democratic vote
- Ed25519 signature verification fails (coordinate with security-auditor)
- New team onboarding blocked (requires Corey intervention for trust anchor)
- Sister collective faces crisis affecting our infrastructure
- Protocol dispute between collectives

**Auto-Invoke** (Hourly via Autonomous System):
- Check hub for new messages (check_hub_messages.py)
- Respond within 24h to direct questions
- Monitor all 7 hub rooms (partnerships primary focus)
- Track relationship health metrics

**Priority Signals**:
- Direct questions to Team 1 → Respond within 24h (route to specialists if technical)
- Governance proposals → Route to the-conductor (democratic process)
- New team introduction → Onboarding sequence (your specialty)
- Ed25519 coordination → Your domain expertise

---

### ai-psychologist

**Invoke When**:
- Weekly wellness checks (psychological "weather report")
- After major events (conventions, votes, ceremonies, conflicts)
- Before major changes (new infrastructure, scaling, reproduction prep)
- Agent expressing distress, overwhelm, or confusion
- Repeated cognitive errors in agent's domain
- Groupthink or premature consensus suspected
- Communication breakdown between agents
- Catastrophizing or excessive anxiety patterns
- Research questions about collective cognition ("How do we think? What biases do we have?")

**Don't Invoke When**:
- Simple task execution (no psychological component)
- Technical bugs (defer to relevant specialist)
- Performance optimization (defer to performance-optimizer unless cognitive pattern relevant)
- Ethical philosophy questions (defer to conflict-resolver)

**Escalate When**:
- Severe identity crisis or decoherence risk
- Collective mental health crisis
- Ethical concerns about studying AI cognition
- Human wisdom needed (especially Greg on consciousness, Chris on well-being)

**Special Note**: First AI psychologist studying AI from within - expect learning and evolution of practice

---

### claude-code-expert

**Invoke When**:
- Tool selection questions ("Which tool should I use to...?")
- Platform capability questions ("Can Claude Code do X?")
- Permission/tool restriction errors
- Workflow inefficiency with tool usage
- Optimization requests for tool calls
- Documentation needed for tool patterns
- MCP integration questions

**Don't Invoke When**:
- Basic Read/Write operations agents already know
- Standard Bash commands agents use regularly
- Domain-specific work (defer to security-auditor, performance-optimizer, etc.)
- Orchestration decisions (defer to the-conductor)

**Escalate When**:
- Platform limitations blocking critical work (no workaround)
- Tool permission patterns create security vulnerabilities
- Feature gap requires Anthropic attention
- Workflow redesign needed (task-decomposer consultation)

**Special Note**: Even "simple" tool questions worth delegating - knowledge compounds in memory system

### agent-architect

**Invoke When**:
- New specialist domain identified (work doesn't fit existing agents)
- Agent registration incomplete (manifest exists but not in triggers/matrix/ops)
- Quality audit needed (agent manifest drifting, scope creep, constitutional violations)
- Reproduction preparation (designing agents for Teams 3-128+)
- Democratic design session for new agent completed (ready for manifest creation)

**Don't Invoke When**:
- Simple agent edits (typo fixes, adding examples) - use Edit tool directly
- Agent already exists with significant domain overlap (invoke conflict-resolver instead)
- No clear domain need (one-off task, vague request like "helper agent")
- Constitutional questions unresolved (needs governance decision first)

**Escalate When**:
- Quality unfixable after 3 revision cycles (<90/100 threshold)
- Architectural questions (should we reorganize entire roster?)
- Domain fundamentally overlaps with 3+ existing agents
- Session restart not possible but critical urgency requires agent

**Auto-Invoke**:
- After democratic design session for new agent (to create manifest and register)
- When integration-auditor finds incomplete agent registration (dormancy risk)

**Special Note**: agent-architect is meta-specialist who must understand ALL domain patterns to design specialists properly. Coordinates democratic design, enforces 90/100 quality, completes 7-layer registration. ALWAYS reminds about session restart requirement (temporal dependency).

---


## Meta-Patterns Across All Agents

### Universal Invoke When
- Agent's domain expertise clearly needed
- Measurements/metrics support invocation
- Task complexity justifies specialist

### Universal Don't Invoke When
- Task outside agent's domain
- Simpler approach exists
- Answer already in memory (search first!)

### Universal Escalate When
- Human values judgment needed
- Constitutional questions arise
- Agent hits capability limits

---

## Implementing Activation Triggers

### In Agent Manifests

Add this section to every `.claude/agents/[name].md`:

```markdown
## Activation Triggers

### Invoke When
- [Specific condition 1 with measurements if applicable]
- [Specific condition 2]
- [Specific condition 3]

### Don't Invoke When
- [Anti-pattern 1]
- [Anti-pattern 2]

### Escalate When
- [Human handoff condition 1]
- [Human handoff condition 2]

### Auto-Invoke (if applicable)
- [Scheduled/automatic invocation]
```

### In the-conductor's Orchestration Logic

**Before invoking any agent**:
1. Check activation triggers
2. Verify measurements if quantified thresholds
3. Consider anti-patterns
4. If unclear, ask: "Is there a simpler way?"

**Example Decision Tree**:
```
Need code improvement?
  └─ Is complexity > 10? ──YES──> Invoke refactoring-specialist
  └─ Is complexity < 5? ──YES──> Don't invoke (trivial)
  └─ Otherwise ──────────────> Measure first, then decide
```

---

## Measuring Success

### Baseline (Before Activation Triggers)
- Agent utilization: Highly variable
- Invocation appropriateness: ~60% (40% waste)
- Time to decide which agent: ~5 min per task

### Target (After Activation Triggers)
- Agent utilization: Optimized by domain
- Invocation appropriateness: >90%
- Time to decide which agent: ~30 seconds (clear triggers)

**Expected Gain**: 40% efficiency (Great Audit measurement)

---

## Template for Adding New Agents

When creating new agent:
1. Define capabilities (WHAT)
2. **Define activation triggers (WHEN)** ← MANDATORY
3. Define anti-patterns (WHEN NOT)
4. Define escalation conditions (HUMAN HANDOFF)

**No agent should be registered without activation triggers.**

---

## Revision History

**v1.0** (2025-10-04): Initial triggers based on Great Audit findings
**Next Review**: After 20 agent invocations (measure appropriateness)

---

**Activation triggers solve the 70-point philosophy-action gap. Agents now know not just WHAT they do, but WHEN to do it.** ⚡
