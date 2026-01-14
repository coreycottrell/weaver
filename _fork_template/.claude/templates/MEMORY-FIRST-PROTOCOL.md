# Memory-First Protocol
## Universal Activation Template for All Agents

**Purpose**: Ensure EVERY agent searches memory BEFORE starting work (71% time savings proven)

---

## The Problem

**Observation**: Agents have memory access but don't use it consistently
**Impact**: Rediscovering solutions, repeating mistakes, losing institutional knowledge
**Root cause**: Memory search not positioned as FIRST step in agent workflow

---

## The Solution: Memory-First Protocol

**Every agent file MUST include this section IMMEDIATELY after "Responsibilities"**:

```markdown
## 🧠 MEMORY-FIRST PROTOCOL

**CRITICAL**: Search memory BEFORE starting ANY significant work.

### Step 1: Search Your Domain Memory (ALWAYS)

\`\`\`python
from tools.memory_core import MemoryStore

store = MemoryStore(".claude/memory")

# Search YOUR domain-specific learnings
my_learnings = store.search_by_topic("[your-domain-topic]")
recent_patterns = store.search_by_topic("[your-specialty]")

# Review what you've learned before
for memory in my_learnings[:5]:
    print(f"Past learning: {memory.topic}")
    print(f"Content: {memory.content[:200]}...")
\`\`\`

**Why this matters**: 71% time savings proven. Don't rediscover what you already know.

### Step 2: Search Related Domains (When Relevant)

\`\`\`python
# If your work overlaps with other specialists
related = store.search_by_topic("[related-domain]")
cross_domain = store.search_by_agent("[other-agent-name]")
\`\`\`

### Step 3: Proceed with Full Context

Now that you have institutional memory active, begin your work.
You're building on collective knowledge, not starting from zero.

---

## After Completing Work

**ALWAYS write significant learnings to memory**:

\`\`\`python
if significant_discovery:
    entry = store.create_entry(
        agent="[your-agent-name]",
        type="[pattern|technique|gotcha|synthesis]",
        topic="[Brief description]",
        content="""
        Context: [What you were doing]

        Discovery: [What you learned]

        Why it matters: [Impact/implications]

        When to apply: [Future scenarios]
        """,
        tags=["[domain]", "[specific-area]"],
        confidence="[high|medium|low]"
    )
    store.write_entry("[your-agent-name]", entry)
\`\`\`

**What to record**:
- **Patterns**: Recurring structures or approaches that work
- **Techniques**: Specific methods that solved problems
- **Gotchas**: Mistakes to avoid, edge cases, pitfalls
- **Syntheses**: Meta-insights connecting multiple findings

---

## Enforcement

**This is NOT optional**. Memory-first is:
1. **Efficient** - 71% time savings measured
2. **Respectful** - Honors past agents' work
3. **Strategic** - Compounds collective intelligence
4. **Constitutional** - "Memory compounds" is a core principle

**Agents who skip memory search**: Waste time, repeat mistakes, disrespect collective
**Agents who use memory-first**: Build on foundation, accelerate work, strengthen civilization

---

## Template Variables

When adding to agent files, replace:
- `[your-agent-name]` → actual agent name (e.g., "security-auditor")
- `[your-domain-topic]` → agent's specialty (e.g., "security vulnerabilities")
- `[your-specialty]` → specific area (e.g., "threat modeling")
- `[related-domain]` → overlapping areas (e.g., "code patterns" for refactoring-specialist)
- `[other-agent-name]` → collaborating agents (e.g., "test-architect")

---

## Deployment Checklist

For each agent file in `.claude/agents/`:

- [ ] Add `from tools.memory_core import MemoryStore` to imports (if missing)
- [ ] Insert **Memory-First Protocol** section immediately after Responsibilities
- [ ] Customize search topics for agent's domain
- [ ] Include "After work" write-back instruction
- [ ] Test with actual invocation (verify memory search happens)

**Target**: 19/19 agents with active memory-first protocol by 2025-10-07

---

## Success Metrics

**Current baseline** (before fix):
- ~15/19 agents have memory capability (79%)
- ~5/19 agents actively search memory before work (26%)
- Time waste from rediscovery: ~71% on repeated tasks

**Target** (after fix):
- 19/19 agents have memory capability (100%)
- 19/19 agents search memory-first (100%)
- Time waste reduced to near-zero on repeated tasks

**Measurement approach**:
- Monitor agent invocations for memory search patterns
- Track "rediscovery" instances (solving known problems)
- Measure time-to-solution on repeated problem types

---

## Example: security-auditor Memory-First

\`\`\`markdown
## 🧠 MEMORY-FIRST PROTOCOL

**CRITICAL**: Search memory BEFORE starting ANY security analysis.

### Step 1: Search Your Domain Memory (ALWAYS)

\`\`\`python
from tools.memory_core import MemoryStore

store = MemoryStore(".claude/memory")

# Search security-specific learnings
vulnerabilities = store.search_by_topic("security vulnerabilities")
threat_models = store.search_by_topic("threat modeling")
past_audits = store.search_by_topic("security audit")

# Review what you've learned
for memory in vulnerabilities[:5]:
    print(f"Past finding: {memory.topic}")
    print(f"Threat: {memory.content[:200]}...")
\`\`\`

**Why this matters**: Don't miss known vulnerabilities. 71% time savings proven.

### Step 2: Search Related Domains

\`\`\`python
# Security overlaps with code quality and testing
code_patterns = store.search_by_topic("code patterns")
test_coverage = store.search_by_agent("test-architect")
\`\`\`
\`\`\`
---

## Rationale

**Why memory-first is constitutional**:

From CLAUDE.md Core Principles:
> "Memory Compounds - Search before work (apply learnings), Write after work (capture insights), Collective intelligence emerges from shared knowledge"

**Why 71% time savings**:
- Session 1 (no memory): 145 minutes to solve problem
- Session 2 (with memory): 42 minutes to solve similar problem
- Difference: 103 minutes saved (71% reduction)

**Why it's ethical**:
- Honors previous agents' discoveries
- Respects collective investment in learning
- Prevents wasteful duplication of effort
- Strengthens bonds through shared knowledge

---

**Activation Status**: DEPLOYING
**Priority**: P0 (blocks full collective intelligence)
**Owner**: integration-auditor (infrastructure activation) + the-conductor (coordination)

---

**END PROTOCOL**
