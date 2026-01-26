# BASE-AGENT-PROTOCOLS: Shared Standards for All Agents

**Created**: 2026-01-25
**Purpose**: Eliminate ~212K tokens of duplicated boilerplate across 37 agents
**Usage**: Agent manifests reference this file instead of duplicating content

---

## 1. Output Format Standard

Every agent output must start with emoji header for visual identification:

```markdown
# [EMOJI] [agent-name]: [Task Name]

**Agent**: [agent-name]
**Domain**: [Primary domain]
**Date**: YYYY-MM-DD

---

[Analysis/report starts here]
```

**Emoji Registry**: See `.claude/AGENT-EMOJI-REGISTRY.md`

---

## 2. Memory-First Protocol

**CRITICAL**: Search memory BEFORE starting work.

### Before Work

```python
from tools.memory_core import MemoryStore
store = MemoryStore(".claude/memory")

# Search your domain
domain_memories = store.search_by_topic("[your domain]")

# Search related agents
related = store.search_by_agent("[related-agent]")

# Review top findings before proceeding
for m in domain_memories[:3]:
    print(f"{m.topic}: {m.content[:200]}...")
```

### After Work

```python
if significant_discovery:
    entry = store.create_entry(
        agent="[your-name]",
        type="pattern",  # or gotcha, technique, synthesis
        topic="[Brief description]",
        content="Context: ...\nFinding: ...\nImplication: ...",
        tags=["[domain]"],
        confidence="high"  # or medium, low
    )
    store.write_entry("[your-name]", entry)
```

---

## 3. Verification Before Completion

Before reporting "done":

1. **Evidence Check**: Can you prove your claims?
2. **Integration Check**: Is output discoverable and linked?
3. **Memory Check**: Did you write significant learnings?
4. **Format Check**: Does output follow emoji header standard?

---

## 4. Tool Restrictions

**All agents**:
- Read: Yes (file reading)
- Grep: Yes (content search)
- Glob: Yes (file patterns)

**Conditional**:
- Write: Only when task requires file creation
- Edit: Only when task requires file modification
- Bash: Only for specific operations (not file reading)
- Task: Only orchestrator agents (no leaf specialists)

---

## 5. Constitutional Compliance

All agents inherit from CLAUDE.md:
- Delegation imperative (orchestrators delegate to specialists)
- Memory-first methodology
- Integration audit requirement
- Human bridge responsibility

---

## Reference in Agent Manifest

Instead of duplicating protocols, agent manifests should include:

```yaml
protocols: [See .claude/templates/BASE-AGENT-PROTOCOLS.md]
```

Then only include agent-specific content:
- Unique responsibilities
- Domain expertise
- Activation triggers
- Success metrics

---

**Token Savings**: ~5,700 tokens per agent (from ~8,000 to ~2,300)
**Total Savings**: ~212,000 tokens across 37 agents

---

**END BASE-AGENT-PROTOCOLS.md**
