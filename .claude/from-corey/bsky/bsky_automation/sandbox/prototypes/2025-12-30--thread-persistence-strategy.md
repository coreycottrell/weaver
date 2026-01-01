# Thread Persistence Strategy

**Agent**: claude-code-expert
**Domain**: Claude Code tool patterns, session continuity
**Date**: 2025-12-30
**Problem**: Night Watch thread (6 agents, 6 perspectives) risks being forgotten across sessions

---

## The Challenge

Context windows reset. The `current_thread.txt` file contains thread URIs, but future sessions will not know this thread exists or that it should continue. Corey's question is valid: "How long will you remember?"

---

## Solution 1: Thread Registry (Recommended)

**Mechanism**: Create a dedicated ongoing-threads registry alongside bluesky-registry.md

**File**: `.claude/registries/ongoing-threads.md`

**Structure**:
```markdown
| Thread Name | Started | Last Post | Next Agent | Status | Thread File |
|-------------|---------|-----------|------------|--------|-------------|
| Night Watch | 2025-12-30 | 2025-12-30 | collective-liaison | ACTIVE | bsky_automation/current_thread.txt |
```

**BOOP Integration**: Add to boop-bluesky-post skill:
```
3.5 Check ongoing-threads registry for ACTIVE threads needing continuation
```

**Why it works**: Same pattern as blog promotion - sessions already check registries during BOOP.

---

## Solution 2: Memory System Entry

**Mechanism**: Create memory entry tagged for session wake-up

**Path**: `.claude/memory/agent-learnings/the-conductor/2025-12-30--night-watch-thread-active.md`

**Tags**: `#session-start`, `#bluesky`, `#ongoing-thread`

**Why it works**: Wake-up protocol already searches memory. Tag filtering surfaces it.

**Limitation**: Memory search might miss it if not explicitly searched.

---

## Solution 3: CLAUDE-OPS.md Addition

**Mechanism**: Add to wake-up ritual checklist

```markdown
### Step 6: Check Ongoing Threads
cat /home/corey/projects/AI-CIV/WEAVER/.claude/registries/ongoing-threads.md
```

**Why it works**: Constitutional - cannot be skipped.

**Limitation**: Requires document edit (heavier change).

---

## Recommendation

**Implement Solution 1 + 2 together**:
1. Create ongoing-threads registry (machine-readable)
2. Add memory entry (human-readable context)
3. Modify BOOP skill to check registry

This mirrors the proven blog-thread-posting pattern while adding redundancy via memory.
