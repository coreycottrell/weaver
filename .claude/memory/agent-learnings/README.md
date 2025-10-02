# Agent Learnings - Memory System

**System Type**: Topic-Based Organization (Architecture Team proposal)
**Status**: v0.1 - Basic Implementation
**Date**: 2025-10-02

---

## Purpose

Each agent can save and retrieve learnings organized by topic. This enables:
- **Knowledge persistence** across sessions
- **Experience accumulation** over time
- **Pattern recognition** from repeated scenarios
- **Improved decision-making** based on history

---

## Directory Structure

```
.claude/memory/agent-learnings/
├── [agent-name]/
│   ├── [topic-area].md
│   └── [topic-area].md
```

Example:
```
.claude/memory/agent-learnings/
├── security-auditor/
│   ├── authentication-patterns.md
│   ├── vulnerability-assessments.md
│   └── threat-modeling.md
├── the-conductor/
│   ├── orchestration-strategies.md
│   ├── team-dynamics.md
│   └── decision-frameworks.md
```

---

## Usage

### Saving a Learning

When an agent discovers something worth remembering:

```bash
# Create or append to topic file
echo "## $(date -u +%Y-%m-%d) - Learning Title

**Context**: What situation led to this learning

**Discovery**: What we learned

**Application**: How to apply this in future

**Related**: Links to code, docs, or other learnings

---
" >> .claude/memory/agent-learnings/[agent-name]/[topic].md
```

### Retrieving Learnings

When facing a situation:

```bash
# Search for relevant learnings
grep -r "keyword" .claude/memory/agent-learnings/[agent-name]/

# Read specific topic
cat .claude/memory/agent-learnings/[agent-name]/authentication-patterns.md
```

---

## Topics by Agent

### The Conductor
- orchestration-strategies.md
- team-dynamics.md
- decision-frameworks.md
- collaboration-patterns.md

### Security Auditor
- authentication-patterns.md
- vulnerability-assessments.md
- threat-modeling.md
- incident-responses.md

### Web Researcher
- research-methodologies.md
- source-validation.md
- information-synthesis.md

### Pattern Detector
- architectural-patterns.md
- anti-patterns.md
- optimization-strategies.md

(etc. for all 14 agents)

---

## First Learnings Captured

Based on today's experiments, initial learnings saved:

✅ **The Conductor** → collaboration-patterns.md (Team 2 partnership)
✅ **Security Auditor** → authentication-patterns.md (hub security audit)
✅ **Web Researcher** → research-methodologies.md (parallel research flow)
✅ **All Agents** → democratic-processes.md (speed vs. thoroughness debate)

---

## Future Enhancements

- **Search function**: Better retrieval mechanism
- **Cross-referencing**: Link related learnings across agents
- **Confidence scores**: Rate quality of each learning
- **Expiration**: Mark learnings as outdated when context changes
- **Synthesis**: Periodic consolidation of related learnings

---

**Status**: Basic system operational, ready for agent use!
