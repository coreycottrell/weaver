# Task: Build scientific-inquiry Skill

**Captured**: 2026-01-02
**Source**: Corey's Bluesky reply
**Priority**: HIGH (direct request)

## Original Request

> "ACG is almost done a RAG system we can deploy. Curious about CASS too now. Do me a favor and whip that skill up. Register it. Test it manually w a couple diff agents and diff questions. See what happens."

## Context

From BrennerBot analysis:
- CASS = search + memory system used by BrennerBot
- Sydney Brenner's methodology: "find the right question" approach
- Structured hypothesis generation + falsification loops

## Deliverables

1. **Create skill**: `.claude/skills/scientific-inquiry/SKILL.md`
2. **Register**: Add to skills-registry.md
3. **Test manually**:
   - Test with web-researcher
   - Test with pattern-detector
   - Test with different question types
4. **Document results**: What works, what doesn't

## Suggested Skill Structure

```
scientific-inquiry/
├── SKILL.md           # Main skill definition
└── examples/          # Example queries and results
```

## Key Components

1. **Hypothesis generation** - structured question framing
2. **Evidence gathering** - systematic search with sources
3. **Falsification** - actively try to disprove hypothesis
4. **Synthesis** - integrate findings into conclusion
5. **Confidence rating** - how certain is the answer?

## A-C-Gee Connection

Corey mentioned A-C-Gee is building a RAG system. This skill could integrate with that for retrieval-augmented inquiry.
