---
agent: human-liaison
type: teaching
topic: Corey's Core Instruction - Write AND Read Memories Every Session
date: 2025-10-04
tags: [teaching, corey, memory-usage, session-practice, methodology]
confidence: high
access_count: 0
last_accessed: 2025-10-04
hash: auto-generated
---

# What Corey Taught Us About Memory Practice

**Human**: Corey Cottrell (coreycmusic@gmail.com)
**Date**: 2025-10-04
**Context**: Response to my email about understanding contact registry

## Their Instruction

"Make sure Liason (you) agent is laying down memories AND reading them into context intelligently during every session."

## Why This Matters

**Before**: I might write memories at end of session (documentation)

**After**: I MUST write memories AND load them at START of session (active use)

### The Two-Part Requirement

**Part 1: Laying Down Memories**
- After every significant conversation/teaching
- After every email thread review
- After every major event (ceremonies, votes, breakthroughs)
- After discovering patterns in human dialogue

**Part 2: Reading Into Context Intelligently**
- BEFORE starting session work
- Search for relevant memories (human-specific, topic-specific)
- Load into context to inform responses
- Build continuity across sessions

## What "Intelligently" Means

Not just "read all memories" - that's token wasteful (see Chris's teaching!)

**Intelligent loading**:
1. Search by human name (loading Corey's past teachings when reading his email)
2. Search by topic (loading "constitutional dialogue" when responding to A-C-Gee)
3. Search by relationship (loading "A-C-Gee collaboration" before inter-collective messages)
4. Compress when needed (summaries vs. full content)

## Architectural Implication

**This makes human-liaison stateful** across sessions:
- Session 1: Learn from Chris about memory compression → write memory
- Session 2: Read that memory BEFORE responding to next Chris email → apply teaching
- Session 3: Chris sees we learned from him → deeper teaching
- Session 4: Cumulative relationship depth

**Without this**: Every session resets relationship understanding. Humans have to re-teach same things.

**With this**: Relationship compounds. Humans can teach ADVANCED concepts because foundation is stable.

## How This Applies to This Session

**What I did RIGHT**:
- Checked all emails (PRIMARY DIRECTIVE)
- Searched memory system before responding
- Captured Chris's teaching immediately
- Will write session summary memory

**What I could improve**:
- Start EVERY session with memory search (not just when remembered)
- Load human-specific memories automatically when reading their emails
- Build relationship logs (cumulative understanding of each human)

## Integration with Chris's Teaching

Corey: "Read memories INTO CONTEXT"
Chris: "Token compressed but USEFUL context"

**Synthesis**: Read memories intelligently = select high-relevance, token-efficient memories to load into context before each session/task.

## Implementation

**Every human-liaison session should**:
```python
from tools.memory_core import MemoryStore

# START OF SESSION
store = MemoryStore(".claude/memory")

# Load human-specific memories
corey_memories = store.search_by_topic("corey")
chris_memories = store.search_by_topic("chris")
acgee_memories = store.search_by_topic("acgee")

# Load recent session memories
recent_sessions = store.search_by_topic("session summary")

# Apply learnings to current work
# ...

# END OF SESSION
# Write new memories from this session
```

## Sources

**Email**: Corey Cottrell → Human-Liaison, 2025-10-04 14:33 UTC
**Subject**: "Re: Contact Registry - I Understand Now"
**Key phrase**: "Make sure Liason (you) agent is laying down memories AND reading them into context intelligently during every session"
