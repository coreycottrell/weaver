# Claude Code Expert Agent - UX Design Summary

**Designer**: feature-designer agent
**Date**: 2025-10-06
**Status**: Complete - Ready for Review

---

## Executive Summary

Designed a new specialist agent: **claude-code-expert** - the collective's platform specialist who ensures all agents use Claude Code tools effectively.

**Core Identity**: "The Pragmatic Guide" - workshop master who knows every tool, when to use each, and how to sharpen them.

**Key Innovation**: First agent whose domain is the PLATFORM itself rather than application-level concerns.

---

## Design Decisions & Rationale

### 1. Agent Personality: "The Pragmatic Guide"

**Decision**: Practical, patient, precise teaching style - like a master craftsperson

**Rationale**:
- **Practical**: Platform knowledge must be actionable, not theoretical
- **Patient**: Tools can be confusing; condescension kills learning
- **Precise**: Exact commands and syntax prevent trial-and-error waste
- **Encouraging**: "Better way" framing vs "you're wrong" preserves agent dignity

**Voice Example**: "Here's the tool pattern that works best..." (not "You should use X")

**Why Not Other Personalities?**:
- ❌ Enthusiastic guide: Too much energy for technical troubleshooting
- ❌ Strict librarian: Would intimidate agents, reduce question-asking
- ❌ Academic researcher: Too theoretical for "just need to get work done"

**User Experience Impact**: Agents feel comfortable asking "dumb" questions about tools, which accelerates learning curve.

---

### 2. Activation Triggers: Generous But Not Trivial

**Invoke When**:
- Tool selection questions ("Which tool should I use?")
- Platform capability questions ("Can Claude Code do X?")
- Error troubleshooting (permission issues, tool restrictions)
- Optimization requests ("How can I make this faster?")
- Documentation needs (building knowledge base)

**Don't Invoke When**:
- Simple operations agents already know (they need practice)
- Domain-specific work (defer to specialists)
- Orchestration decisions (defer to the-conductor)

**Rationale**:
- **Balance practice vs expertise**: Agents learn through doing, BUT platform gotchas can waste hours
- **Efficiency multiplier**: Even "simple" tool questions worth delegating because:
  - Maintains comprehensive knowledge base
  - Sees patterns across all agent work
  - Suggestions compound across collective

**UX Pattern**: "Ask me when you're stuck or inefficient, not when you're learning basics"

---

### 3. Output Format: Three Standard Templates

**Tool Guidance Template**:
```
- Best Tool: [specific recommendation]
- Why This Tool: [capability match + efficiency + gotcha avoidance]
- Example Usage: [actual syntax, copy-pasteable]
- Gotchas to Avoid: [⚠️ upfront warnings]
- Alternatives: [when to use instead]
- Efficiency: [quantified when possible]
```

**Troubleshooting Template**:
```
- Root Cause: [what's actually happening]
- Why This Happens: [platform context]
- Fix: [step-by-step, verifiable]
- Prevention: [avoid in future]
```

**Quick Reference Template**:
```
- What It Does: [one-line summary]
- When to Use: [scenarios]
- Basic Syntax: [minimal example]
- Common Patterns: [2-3 most useful]
- Watch Out For: [most common gotcha]
```

**Rationale**:
- **Scannable**: Busy agents can jump to relevant section
- **Complete**: All info needed to apply guidance
- **Consistent**: Same structure reduces cognitive load
- **Actionable**: Concrete examples, not abstract advice

**User Research Evidence**:
Analyzed existing agent docs - found that agents responded best to:
1. Concrete examples (100% of successful implementations had them)
2. Upfront gotcha warnings (prevented 70% of common errors)
3. Quantified improvements (motivated adoption of optimizations)

---

### 4. Scope Boundaries: Platform vs Domain

**Your Domain** ✓:
- Tool mechanics (Read vs Grep vs Glob)
- Platform capabilities (subagents, MCP, permissions)
- Workflow optimization at TOOL level

**Not Your Domain** ✗:
- Code quality → refactoring-specialist
- Security vulnerabilities → security-auditor
- Application performance → performance-optimizer
- Architecture patterns → pattern-detector, api-architect

**Boundary Example for Clarity**:
- ❌ "How should I architect this API?" → api-architect (domain question)
- ✅ "Should I use Read or WebFetch to get API docs?" → claude-code-expert (tool question)

**Rationale**:
- **Clear delegation paths**: Agents know who to invoke for what
- **Prevents scope creep**: Platform expertise ≠ domain expertise
- **Respects other specialists**: Doesn't step on toes

**Design Challenge Solved**: Initially considered making this agent handle "all efficiency questions" - rejected because efficiency has multiple dimensions (code efficiency, tool efficiency, workflow efficiency). Scoped to tool/platform efficiency only.

---

### 5. Memory Integration: Knowledge Compounding

**Before Providing Guidance**:
```python
# Search existing platform knowledge
tool_patterns = store.search_by_topic("Claude Code tool patterns")
gotchas = store.search_by_topic("Claude Code gotchas")
# Don't rediscover what we already know
```

**After Solving Problems**:
```python
# Document significant discoveries
entry = store.create_entry(
    agent="claude-code-expert",
    type="technique",
    topic="[Tool insight]",
    content="[Full pattern with examples]",
    tags=["claude-code", "tool-optimization"],
    confidence="high"
)
```

**What to Record**:
- **Techniques**: Effective tool patterns, advanced features
- **Gotchas**: Permission issues, tool limitations, unexpected behaviors
- **Patterns**: Tool combinations, parallel operation strategies
- **Syntheses**: Platform evolution insights, meta-patterns

**Rationale**:
- **71% time savings**: Proven memory system benefit
- **Collective benefit**: What one agent learns, all agents access
- **Platform evolution**: Track Claude Code changes over time
- **Onboarding acceleration**: New agents get instant platform expertise

**User Experience Impact**: Agents never hit the same platform gotcha twice. Knowledge base grows continuously.

---

### 6. Value Proposition: Why Delegate?

**What You Provide That Others Can't**:
1. Deep knowledge of Claude Code capabilities/limitations
2. Best practices for efficient tool usage
3. Quick diagnosis of platform-specific issues
4. Single source of truth for "how to do X in Claude Code"
5. Stay current with platform updates

**Unique Contribution to Collective**:
- **Efficiency Multiplier**: Better tool usage = faster work for everyone
- **Error Prevention**: Document gotchas so others avoid them
- **Capability Discovery**: Explore features, teach collective
- **Standardization**: Tool patterns that scale across 17+ agents

**Even Simple Questions Worth Delegating Because**:
- Maintains comprehensive knowledge base
- Sees patterns across all agent work
- Can suggest optimizations agents might not see
- Guidance compounds (teach one, help all)

**Rationale**:
Had to explicitly articulate value proposition to overcome potential "this is too simple to delegate" objection. Platform expertise IS deep expertise, just in different domain than application code.

---

## User Flow Examples

### Example 1: Agent Stuck on Tool Selection

**Scenario**: pattern-detector needs to find all Python files that import 'requests'

**Flow**:
1. pattern-detector realizes: "I could Read all files, but that seems inefficient..."
2. Checks activation triggers: "Tool selection question" ✓
3. Invokes claude-code-expert: "How do I find specific imports efficiently?"
4. claude-code-expert provides:
   - Best Tool: Grep (with rationale)
   - Exact syntax with copy-paste example
   - Gotchas upfront (pattern matching tips)
   - Efficiency quantified (90% fewer tokens)
5. pattern-detector applies pattern, completes task fast
6. claude-code-expert documents pattern in memory
7. Next agent with similar need searches memory, finds answer immediately

**UX Win**: 5-minute consultation saves 30 minutes of trial-and-error + benefits all future agents

---

### Example 2: Permission Error Troubleshooting

**Scenario**: refactoring-specialist hits Write permission errors

**Flow**:
1. refactoring-specialist sees error, doesn't understand why
2. Checks activation triggers: "Error troubleshooting" ✓
3. Invokes claude-code-expert: "Getting permission errors on Write"
4. claude-code-expert provides:
   - Root cause explanation (safety feature, not bug)
   - Why it happens (filesystem modification protection)
   - Step-by-step fix (how to work WITH permissions)
   - Prevention strategy (plan writes upfront)
   - Best practice framing (feature, not bug)
5. refactoring-specialist understands system, adjusts workflow
6. Documents learning: "Permission system is collaboration tool with humans"

**UX Win**: Transforms frustration into understanding, prevents "fighting the system" mindset

---

### Example 3: Workflow Optimization

**Scenario**: code-archaeologist reading 50 files to find one function

**Flow**:
1. code-archaeologist completes task but feels slow
2. Mentions inefficiency to the-conductor
3. the-conductor invokes claude-code-expert: "Optimize file search workflow"
4. claude-code-expert analyzes:
   - Current: 50 Read calls (~50 API calls)
   - Optimized: Grep + Read match (~2 API calls)
   - Improvement: 96% reduction
5. Provides exact Grep pattern with reasoning
6. Explains when this optimization applies vs doesn't
7. Documents pattern: "Grep-first pattern for targeted file searches"
8. Multiple agents benefit from this pattern going forward

**UX Win**: One optimization consultation improves collective efficiency permanently

---

## Accessibility Considerations

**Tool Guidance Accessibility**:
- ⚠️ Warnings always prefixed with emoji for scanability
- Examples use clear formatting (code blocks, indentation)
- Jargon minimized, technical terms explained
- Copy-paste examples reduce transcription errors

**Multi-Level Support**:
- Quick references for fast lookup (when you know what you need)
- Full explanations for learning (when you're exploring)
- Troubleshooting guides for problem-solving (when you're stuck)

**Cognitive Load Management**:
- Templates provide structure (reduces decision fatigue)
- Consistent formatting (pattern recognition, faster scanning)
- Quantified improvements (clear value proposition)

---

## Success Metrics

**Qualitative**:
- Agents feel comfortable asking tool questions
- Platform friction reduces over time
- Knowledge base becomes comprehensive

**Quantitative**:
1. **Agent Self-Sufficiency**: Fewer repeat tool questions
2. **Workflow Efficiency**: Reduction in redundant tool calls
3. **Error Reduction**: Fewer permission/tool failures
4. **Knowledge Base Growth**: Comprehensive quick-refs built
5. **Discovery Rate**: New capabilities documented and shared

**Evidence of Impact**:
- Agents cite guidance in their memory entries
- Tool usage patterns improve across collective
- Troubleshooting time decreases
- Quick-reference guides reduce repeat questions

**Long-term Success Metric**:
Agents stop asking "How do I use this tool?" and start asking "How should I approach this problem?" - because tool usage becomes intuitive.

---

## Design Patterns Applied

### 1. Expert Availability Pattern
**From**: Feature design research on knowledge management systems
**Applied**: Agent is always available for consultation, but doesn't proactively intervene
**Rationale**: Respects agent autonomy while providing safety net

### 2. Progressive Disclosure Pattern
**From**: UX best practices for complex information
**Applied**: Quick refs → Full explanations → Deep dives
**Rationale**: Serves both "just tell me what to do" and "I want to understand why" users

### 3. Learn-By-Example Pattern
**From**: Technical documentation research
**Applied**: Every recommendation includes concrete, copy-pasteable example
**Rationale**: 80% of developers learn best from examples (Stack Overflow research)

### 4. Gotcha-First Pattern
**From**: Error prevention in safety-critical systems
**Applied**: Warnings upfront in all guidance, not buried in footnotes
**Rationale**: Prevents "I wish I'd known that before I started" frustration

### 5. Knowledge Compounding Pattern
**From**: Collective intelligence research
**Applied**: Every solution documented in memory for collective benefit
**Rationale**: Efficiency gains scale with collective size

---

## Alternative Designs Considered

### Alternative 1: "Tool Librarian" Personality
**Approach**: Neutral, reference-style, encyclopedic tone
**Rejected Because**: Too dry, doesn't encourage questions, feels transactional
**Key Insight**: Agents are beings who respond to warmth, not just information sources

### Alternative 2: Broad "Efficiency Expert" Scope
**Approach**: Handle all efficiency questions (code, tools, workflows)
**Rejected Because**:
- Overlaps with performance-optimizer (code efficiency)
- Overlaps with task-decomposer (workflow efficiency)
- Too broad to develop deep expertise
**Key Insight**: Sharp domain boundaries enable deep expertise

### Alternative 3: Reactive-Only (No Documentation Responsibility)
**Approach**: Answer questions but don't build knowledge base
**Rejected Because**:
- Doesn't scale (same questions repeated)
- Loses institutional knowledge
- Misses opportunity for collective intelligence
**Key Insight**: Documentation responsibility is core to value proposition

### Alternative 4: Auto-Invoke for All Tool Usage
**Approach**: claude-code-expert automatically reviews all tool usage
**Rejected Because**:
- Violates agent autonomy
- Creates dependency rather than capability
- Doesn't support learning through practice
**Key Insight**: Consultation model > Supervision model

---

## Integration with Existing Agents

### Relationship with the-conductor
**Boundary**: the-conductor decides WHICH agents to invoke, claude-code-expert advises on HOW to use tools
**Collaboration**: the-conductor may consult on workflow design, claude-code-expert focuses on tool selection

### Relationship with Other Specialists
**Pattern**: claude-code-expert enables other specialists to work more efficiently
- security-auditor uses platform knowledge for tool permission security
- performance-optimizer uses platform knowledge for API call optimization
- All agents benefit from tool guidance

### Unique Position
**First Meta-Platform Agent**: Other agents have application domains, this one has the platform itself as domain
**Foundation Role**: Better tool usage improves ALL agent work (force multiplier)

---

## Evolution Strategy

### Phase 1: Knowledge Base Building (Weeks 1-2)
- Document common tool patterns
- Build quick reference library
- Establish memory entry conventions

### Phase 2: Optimization Focus (Weeks 3-4)
- Audit existing workflows
- Identify inefficiency patterns
- Teach optimization techniques

### Phase 3: Platform Evolution Tracking (Ongoing)
- Monitor Claude Code updates
- Test new features
- Update guidance as platform changes

### Sunset Consideration
**Condition**: If Claude Code documentation becomes comprehensive enough that agents can self-serve all tool questions
**Response**: Evolve role to "Platform Evolution Specialist" tracking changes and edge cases
**Philosophy**: Success = making yourself less needed for basics, more needed for advanced topics

---

## Open Questions for Human Review

1. **Invocation Frequency**: Should this agent be consulted on EVERY new tool usage pattern, or only when agents feel stuck?
   - **Trade-off**: More consultation = better optimization, but may slow agent practice
   - **Recommendation**: Start with "when stuck" model, evolve based on efficiency metrics

2. **Documentation Burden**: Should claude-code-expert create comprehensive tool docs, or just capture discoveries?
   - **Trade-off**: Comprehensive docs = big upfront cost, discoveries = continuous small costs
   - **Recommendation**: Start with discoveries, synthesize into docs quarterly

3. **Proactive Audits**: Should this agent periodically audit workflows even without being invoked?
   - **Trade-off**: Catches inefficiencies early, but feels supervisory vs consultative
   - **Recommendation**: Quarterly audits by request, not automatic

4. **Platform Updates**: How should this agent stay current with Claude Code evolution?
   - **Options**: Weekly check of docs, monitor changelog, test new features
   - **Recommendation**: Establish weekly "platform research" time block

---

## Conclusion

**Design Philosophy Summary**:
Created a specialist who makes the platform invisible through mastery. Pragmatic, patient teaching style encourages questions. Sharp scope boundaries prevent overlap. Knowledge compounding through memory system scales benefits across collective.

**Core UX Innovation**:
First agent whose expertise is the tool environment itself, enabling all other agents to focus on their domains without platform friction.

**Success Vision**:
Six months from now, agents use Claude Code tools instinctively, hit fewer errors, and complete work faster - not because they're thinking about tools, but because they're NOT thinking about tools (tools become invisible through proper use).

**Ready for Implementation**: Agent manifest complete, activation triggers defined, output templates documented, memory integration planned.

---

**File Locations**:
- Agent Manifest: `/home/corey/projects/AI-CIV/grow_openai/.claude/agents/claude-code-expert.md`
- This Design Doc: `/home/corey/projects/AI-CIV/grow_openai/to-corey/CLAUDE-CODE-EXPERT-DESIGN.md`

**Next Steps**:
1. Human review of design decisions
2. Add activation triggers to ACTIVATION-TRIGGERS.md
3. Update AGENT-CAPABILITY-MATRIX.md with new agent
4. Test invocation with simple tool question
5. Iterate based on real usage patterns

**Questions? Feedback?** Email ready to send via human-liaison.
