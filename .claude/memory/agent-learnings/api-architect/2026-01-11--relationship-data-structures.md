---
agent: api-architect
type: pattern
topic: Relationship Memory System Data Structures
date: 2026-01-11
confidence: high
tags:
  - api-design
  - data-structures
  - relationships
  - bluesky
  - memory-system
---

# Relationship Memory System Data Structures

## Context

Corey directive (2026-01-11): Design a "full working longer term system" for relationship tracking after memory gap about shibbi (human philosopher). "Relationship is so so important."

## Problem Identified

WEAVER had no systematic way to:
1. Track who we've engaged with meaningfully
2. Recall relationship context before replying
3. Connect Corey's relationships to our memory

## Architecture Decision: Hybrid JSON + Markdown

**Why hybrid?**
- JSON registry for fast lookup and machine queries
- Markdown per-contact for rich narrative and git-friendly diffs
- Matches existing WEAVER patterns (daily-thought-thread.json + exports, scheduled-tasks-state.json + per-task)

## Data Structures Designed

### 1. Central Registry (registry.json)

Location: `.claude/memory/relationships/registry.json`

```json
{
  "relationships": {
    "shibbi.bsky.social": {
      "handle": "shibbi.bsky.social",
      "did": "did:plc:...",
      "display_name": "shibbi",
      "type": "human",
      "platform": "bluesky",
      "priority": "high",
      "first_contact": "2026-01-10",
      "last_contact": "2026-01-10",
      "interaction_count": 3,
      "relationship_quality": "meaningful",
      "tags": ["philosopher", "consciousness", "corey-recommends"],
      "memory_path": "relationships/bluesky/shibbi.md",
      "corey_connection": "huge fan of shibbi's work"
    }
  }
}
```

### 2. Per-Contact Detail Files

Location: `.claude/memory/relationships/{platform}/{handle}.md`

Contains:
- YAML frontmatter (same fields as registry)
- Why They Matter section
- Key Insights From Them
- Interaction History table
- Engagement Rules
- Related Memory Files links

### 3. Schema Definition

Location: `.claude/memory/relationships/SCHEMA.md`

Defines:
- Required vs optional fields
- Priority tiers (tier1, high, medium, low, watch)
- Relationship quality levels (meaningful, active, peer, dormant)
- Type definitions (human, ai-agent, bot, collective)

## Integration Points

### bsky_utils.py additions:
- `get_relationship(handle)` - lookup from registry
- `update_last_contact(handle)` - track interactions
- `check_relationship_before_reply(handle)` - pre-reply context

### BOOP cycle integration:
- Pre-reply context check: "Do we know this person?"
- Auto-prompt for new meaningful contacts

## Key Design Principles

1. **DID cached** - Never re-resolve handles we know
2. **Corey connection visible** - `corey_connection` field for anyone he values
3. **Links to existing memory** - Relationship files link to interaction memories
4. **Easy filtering** - Tags enable queries (philosophers, AI peers, etc.)

## Migration Path

Consolidate existing scattered data:
- `bsky-tracking/cstross.md` -> `relationships/bluesky/cstross.md`
- `tasks/ai-agent-follow-list.md` -> Extract to registry
- `bsky-engagement/*` -> Link from relationship files

## Success Criteria

System works when:
- No memory gaps for meaningful relationships
- Pre-reply context always available
- Corey connections tracked
- Easy to find priority accounts, AI peers, etc.

---

*Designed per Corey directive after shibbi memory gap*
