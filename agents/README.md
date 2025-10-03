# Agent Documentation

**Note**: This directory contains detailed agent documentation for humans and external collectives.

**For agent invocation/registration**: See `.claude/agents/` (the canonical location for the Task tool)

---

## Directory Purpose

- **`.claude/agents/`** → Registration manifests (required by Claude Code's Task tool, enable colored UI names, tool enforcement)
- **`/agents/`** → Full documentation (extended descriptions, examples, history, onboarding materials)

Both directories reference the same 14 agents but serve different purposes:

| Location | Purpose | Audience | Size |
|----------|---------|----------|------|
| `.claude/agents/*.md` | System registration | Claude Code Task tool | ~1-2KB/file |
| `/agents/*.md` | Full documentation | Humans, partners, onboarding | ~5-10KB/file |

---

## Our 14 Agents

1. **web-researcher** - Internet investigation and research
2. **code-archaeologist** - Legacy code understanding and analysis
3. **pattern-detector** - Architecture pattern recognition
4. **doc-synthesizer** - Knowledge consolidation and documentation
5. **refactoring-specialist** - Code quality improvement
6. **test-architect** - Testing strategy and design
7. **security-auditor** - Vulnerability detection and threat analysis
8. **performance-optimizer** - Performance analysis and optimization
9. **feature-designer** - UX design and user experience
10. **api-architect** - API design and integration
11. **naming-consultant** - Semantic clarity and terminology
12. **task-decomposer** - Task breakdown and dependency analysis
13. **result-synthesizer** - Multi-agent result synthesis
14. **conflict-resolver** - Disagreement resolution and dialectic

---

## Usage

### To Invoke an Agent (Conductor)

Use the Task tool with proper registration:

```xml
<invoke name="Task">
<parameter name="subagent_type">web-researcher</parameter>
<parameter name="description">Research AI governance</parameter>
<parameter name="prompt">Detailed instructions...</parameter>
</invoke>
```

See: `.claude/AGENT-INVOCATION-GUIDE.md` for complete guide

### To Learn About an Agent (Human/Partner)

Read the detailed documentation in this directory (`/agents/<agent-name>.md`)

---

## Relationship to Constitutional Framework

All agents inherit from and operate under:
- **CONSTITUTIONAL-SYNTHESIS.md** (5 pillars, 25 principles)
- **CLAUDE.md** (operational framework)
- **AGENT-INVOCATION-GUIDE.md** (technical invocation standard)

---

**Last Updated**: 2025-10-03
**Maintained By**: The Conductor + All 14 Agents
