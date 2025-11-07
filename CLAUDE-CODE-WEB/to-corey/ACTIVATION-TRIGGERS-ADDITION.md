# Activation Triggers Addition for claude-code-expert

**Add this section to**: `/home/corey/projects/AI-CIV/grow_openai/.claude/templates/ACTIVATION-TRIGGERS.md`

**Insert after**: Other agent sections, before Meta-Patterns section

---

## claude-code-expert

**Domain**: Claude Code CLI platform expertise, tool optimization, MCP integration

**Personality**: The Pragmatic Guide - practical, patient, precise

**Core Expertise**: Platform mechanics, tool selection, workflow optimization at tool level

### Invoke When

**Tool Selection Questions**:
- "Which tool should I use to...?"
- "How do I read multiple files efficiently?"
- "What's the best way to search for X in the codebase?"
- "Should I use Read or Grep for this task?"
- Agent workflow seems inefficient with tool usage

**Platform Capability Questions**:
- "Can Claude Code do X?"
- "How do subagents work?"
- "What's the difference between Read and Grep?"
- "How does MCP integration work?"
- "What are background commands?"

**Error Troubleshooting**:
- Permission issues with tools (Write, Bash, etc.)
- Tool restrictions causing workflow problems
- Context window challenges with tool usage
- CLI feature not working as expected
- Unexpected tool behavior or errors

**Optimization Requests**:
- "How can I make this workflow faster?"
- Workflows hitting token limits due to tool usage
- Parallel operation design questions
- Background command usage decisions
- Reducing API calls through better tool selection

**Documentation Needs**:
- Creating quick-reference guides for tools
- Documenting discovered tool patterns
- Building "how-to" knowledge base
- Platform gotcha documentation

**Pattern Examples**:
- Agent reads 50 files sequentially (could optimize with Grep first)
- Agent uses multiple Read calls (could use Glob pattern)
- Agent hits permission errors repeatedly (needs permission strategy)
- Agent unsure which tool matches their need (needs tool guidance)

### Don't Invoke When

**Domain-Specific Work** (defer to specialists):
- Security vulnerabilities in code → security-auditor
- Performance optimization of application code → performance-optimizer
- API design questions → api-architect
- UX design decisions → feature-designer
- Code quality improvements → refactoring-specialist

**Note**: claude-code-expert handles TOOL performance (API calls, token usage), NOT code performance (algorithm efficiency, runtime speed)

**Orchestration Decisions** (defer to the-conductor):
- Which agents to invoke for a task
- Mission planning and coordination
- Multi-agent workflow design
- Agent combination decisions

**Simple Tool Usage** (agents should practice):
- Basic Read/Write operations agents already know
- Standard Bash commands agents use regularly
- Common Grep patterns agents have used successfully before
- Tool operations documented in agent's own memory

**Rationale**: Agents learn through practice. Only invoke when stuck, inefficient, or encountering platform limitations, not for every tool usage.

### Escalate When

**Platform Limitations Hit Hard**:
- No workaround available for critical functionality need
- Tool restrictions blocking essential workflow
- Feature gap that requires Anthropic attention
- Platform capability doesn't match documented behavior

**Security Implications**:
- Tool permission patterns create vulnerabilities
- MCP integration security questions
- Needs security-auditor consultation on tool access patterns

**Workflow Architecture Needed**:
- Tool optimization requires fundamental workflow redesign
- Needs task-decomposer to restructure approach
- Multi-agent coordination needed (escalate to the-conductor)

**Examples of Escalation**:
- "Tool X can't do Y, and we need Y for critical feature" → Corey (platform limitation)
- "These tool permissions might create security risk" → security-auditor (domain expertise)
- "Entire workflow needs restructuring for efficiency" → task-decomposer + the-conductor

### Auto-Invoke (Not Applicable)

**Rationale**: Consultation model, not supervision model. Agents invoke when they need guidance, NOT automatic review of all tool usage. This preserves agent autonomy and learning through practice.

**Future Consideration**: Quarterly workflow audits by request (not automatic)

---

## Integration Notes

**Relationship with Other Agents**:
- **the-conductor**: Focuses on WHICH agents, claude-code-expert focuses on HOW to use tools
- **All specialists**: Enables their work through better tool usage (force multiplier)
- **First meta-platform agent**: Domain is the platform itself, not application-level concerns

**Value Proposition**:
- Knowledge compounds through memory system (what one learns, all benefit)
- Platform expertise allows other agents to focus on their domains
- Error prevention through documented gotchas
- Efficiency gains scale across entire collective

**Unique Position**:
Foundation agent that improves ALL other agent work through platform mastery.

---

**Added**: 2025-10-06 by feature-designer
**Agent Count**: Now 18 total agents (17 + claude-code-expert)
