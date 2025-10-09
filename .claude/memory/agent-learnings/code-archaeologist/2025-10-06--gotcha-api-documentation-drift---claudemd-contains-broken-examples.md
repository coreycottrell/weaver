---
agent: code-archaeologist
confidence: high
content_hash: 369e210eb501f0531fb2f29dcf370a2a6a3257b545e647df836c3e9b0bffb0bb
created: '2025-10-06T18:39:51.146621+00:00'
date: '2025-10-06'
last_accessed: '2025-10-06T18:39:51.146631+00:00'
quality_score: 0
reuse_count: 0
tags:
- documentation
- api-drift
- memory-system
- critical
topic: API Documentation Drift - CLAUDE.md Contains Broken Examples
type: gotcha
visibility: public
---


Context: Archaeological investigation discovered CLAUDE.md contains broken code examples

Discovery: Memory system API documented in CLAUDE.md doesn't match actual implementation

What CLAUDE.md says (BROKEN):
```python
entry = store.create_entry(
    agent="agent-name",
    type="pattern",
    topic="...",
    content="..."
)
store.write_entry("agent-name", entry)
```

What actually works:
```python
from tools.memory_core import MemoryEntry
entry = MemoryEntry(
    date="2025-10-06",
    agent="agent-name",
    type="pattern",
    topic="...",
    tags=["tag1"],
    confidence="high",
    visibility="public",
    content="..."
)
store.write_entry("agent-name", entry)
```

Key differences:
1. No create_entry() method exists (AttributeError if you try)
2. Must import MemoryEntry class
3. Must provide date, tags, confidence, visibility (not optional)
4. MemoryEntry is dataclass constructor, not method

Why this matters:
- Fresh sessions start with CLAUDE.md as entire mind
- Following CLAUDE.md examples causes immediate errors
- Breaks memory-first protocol on first attempt
- Creates false confidence ("I know how to use memory" → error → confusion)

Root cause:
- Documentation written from design intent, not tested code
- No validation that CLAUDE.md examples actually run
- API evolved but docs didn't track changes

When this happens:
- Any time CLAUDE.md is updated with code examples
- When APIs change after docs are written
- When examples are written before implementation

How to prevent:
1. Test ALL code examples in CLAUDE.md (run them, verify they work)
2. Auto-generate API docs from actual code docstrings
3. CI/CD check: Parse CLAUDE.md, extract code blocks, run them
4. Tag examples with "TESTED 2025-10-06" timestamps

Evidence this is not isolated:
- Multiple agent profiles copied same broken example
- .claude/templates/ contain same broken pattern
- Propagated through documentation ecosystem

Impact assessment:
- CRITICAL for memory system (breaks primary infrastructure)
- Affects all 19 agents (all have memory protocol in docs)
- New agents following docs will hit errors immediately
