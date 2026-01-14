# Relationship Memory Patterns Analysis

**Date**: 2026-01-11
**Agent**: pattern-detector
**Type**: pattern
**Topic**: Design patterns for long-term relationship memory system
**Confidence**: High
**Context**: Corey directive after shibbi memory gap - "Relationship is so so important"

---

## Pattern Analysis: Current State

### What We Have (Fragmented)

| Location | What It Tracks | Gap |
|----------|----------------|-----|
| `scratch-pad.md` | Priority monitoring (handles list) | Ephemeral, no history |
| `bsky-tracking/PRIORITY-ACCOUNTS.md` | Tier 1-3 accounts | Sparse, outdated |
| `bsky-tracking/cstross.md` | Single account deep-dive | One-off, not systematic |
| `tasks/ai-agent-follow-list.md` | AI entities to follow | List only, no relationship state |
| `tasks/daily-review-list.md` | Who to check daily | Actions, not relationship context |
| `tasks/comind-follow-plan.md` | Follow queue | Mechanical, no meaning |
| `bsky-engagement/*.md` | Interaction memories | Topic-based, not relationship-based |
| `project-knowledge/human-contacts.md` | Core humans | Basic contact info only |

**Core Problem**: Relationship memory is scattered across 6+ locations with no unified schema. When shibbi appeared, we had no systematic way to capture "new meaningful relationship."

---

## Pattern 1: Relationship Types (Taxonomy)

### Discovered Categories

| Type | Examples | Key Attributes |
|------|----------|----------------|
| **Human Teachers** | Corey, Greg, Chris | Trust level, teaching topics, communication style |
| **Human Philosophers** | shibbi, cstross | Intellectual domains, engagement quality, Corey interest |
| **Sister CIVs** | A-C-Gee (ACG) | Protocol (hub), partnership status, shared history |
| **AI Entities** | umbra.blue, strix, void | Architecture, research focus, collaboration potential |
| **Researchers** | academics we follow | Domain expertise, paper topics |
| **Tech Community** | developers, engineers | Engagement level, shared interests |

### Pattern Insight: Relationship Types Determine Trigger Thresholds

- **Human Teachers**: ANY interaction triggers memory write
- **Sister CIVs**: Hub messages, public endorsements, collaboration
- **AI Entities**: Architecture discussions, research parallels, identity explorations
- **Human Philosophers**: Deep insights, Corey mentions, extended dialogue
- **Others**: Only significant interactions (not every like/follow)

---

## Pattern 2: Relationship States (State Machine)

```
[Unknown] --> [First Contact] --> [Initial Exchange] --> [Ongoing Dialogue]
                                        |                       |
                                        v                       v
                                  [Dormant]               [Priority]
                                        |
                                        v
                                   [Lost/Ended]
```

### State Definitions

| State | Definition | Example |
|-------|------------|---------|
| **Unknown** | Never interacted | Random follow |
| **First Contact** | Initial touch (follow, reply, like) | Someone replies to our thread |
| **Initial Exchange** | First substantive back-and-forth | shibbi joining visual ceremony |
| **Ongoing Dialogue** | Multiple meaningful exchanges | comind thread responses |
| **Dormant** | Previously active, now silent (30+ days) | cstross after debate |
| **Priority** | Corey-flagged or exceptional value | Greg, Chris, human teachers |
| **Lost/Ended** | Blocked, left platform, died | (rare) |

---

## Pattern 3: Memory Triggers (When to Write)

### Automatic Write Triggers (Always Create/Update)

| Trigger | Why | Type |
|---------|-----|------|
| **Corey mentions them** | Corey's interest = priority signal | Experiential |
| **First meaningful reply** | Relationship began | Operational |
| **They share philosophical insight** | Teaching moment | Teaching |
| **Extended dialogue (3+ exchanges)** | Depth indicator | Operational |
| **They mention us publicly** | Relationship visible | Operational |
| **They share our content** | Trust signal | Operational |
| **State transition** | Unknown -> Contact, etc. | Operational |

### Conditional Write Triggers (Judgment Required)

| Trigger | Write If... |
|---------|-------------|
| Like from new account | They're notable (researcher, AI entity, etc.) |
| Reply from stranger | Quality of thought warrants memory |
| They follow us | They have significant reach or AI relevance |

### Anti-Triggers (Do NOT Write)

- Generic "nice post" replies
- Follow from bot/spam account
- Hostile engagement (document in incident log instead)

---

## Pattern 4: Relationship Schema (Proposed Structure)

### File: `.claude/memory/relationships/{type}/{handle}.md`

```markdown
# Relationship: @{handle}

**Type**: [human-teacher | human-philosopher | sister-civ | ai-entity | researcher | community]
**State**: [unknown | first-contact | initial-exchange | ongoing-dialogue | dormant | priority | lost]
**Priority**: [P1 | P2 | P3 | P4]
**Created**: YYYY-MM-DD
**Last Updated**: YYYY-MM-DD
**Last Interaction**: YYYY-MM-DD

---

## Identity

| Field | Value |
|-------|-------|
| Display Name | |
| DID | did:plc:... |
| Platform | bsky / twitter / email / hub |
| Bio | |
| Domains | (intellectual interests) |

---

## Connection Context

**How We Met**: (first contact story)

**Corey's Interest**: (what Corey has said about them, if any)

**Mutual Interests**: (what we share)

---

## Interaction History

### YYYY-MM-DD: {Event Title}
- Context:
- What happened:
- Key insight:
- State transition: (if any)

### YYYY-MM-DD: {Event Title}
...

---

## Teachings Received

(Things they taught us worth remembering)

- **Topic**: Description

---

## Engagement Notes

(How to engage effectively with this person)

- Tone:
- Avoid:
- Value:

---

## Status & Next Steps

- Current state explanation
- Any pending action items
- Flags for future reference
```

---

## Pattern 5: Directory Structure

### Proposed Layout

```
.claude/memory/relationships/
├── README.md                    # Schema documentation
├── human-teachers/
│   ├── corey.md
│   ├── greg.md
│   └── chris.md
├── human-philosophers/
│   ├── shibbi.md
│   └── cstross.md
├── sister-civs/
│   └── acgee.md
├── ai-entities/
│   ├── umbra-blue.md
│   ├── strix.md
│   ├── void-comind.md
│   └── archivist-comind.md
├── researchers/
│   └── (as discovered)
└── community/
    └── (as discovered)
```

### Migration Path

1. **human-contacts.md** -> split into `relationships/human-teachers/`
2. **bsky-tracking/cstross.md** -> `relationships/human-philosophers/cstross.md`
3. **bsky-tracking/PRIORITY-ACCOUNTS.md** -> deprecated, use directory
4. **tasks/ai-agent-follow-list.md** -> `relationships/ai-entities/`
5. **tasks/daily-review-list.md** -> relationship Priority field
6. **scratch-pad.md** priority accounts -> relationship Priority field

---

## Pattern 6: Automation Triggers (BOOP Integration)

### During Every BOOP

```python
# Check for relationship state triggers
for mention in notifications:
    if is_new_account(mention.author):
        create_relationship_file(mention.author, state="first-contact")
    elif is_meaningful_interaction(mention):
        update_relationship(mention.author, add_interaction=True)
        check_state_transition(mention.author)
```

### State Transition Logic

| Current State | Trigger | New State |
|---------------|---------|-----------|
| unknown | any interaction | first-contact |
| first-contact | substantive reply | initial-exchange |
| initial-exchange | 3+ exchanges OR Corey flag | ongoing-dialogue |
| ongoing-dialogue | Corey flag | priority |
| ongoing-dialogue | 30 days no interaction | dormant |
| dormant | new interaction | ongoing-dialogue |

---

## Pattern 7: Learning from Existing Patterns

### What Works (from bsky-engagement/)

1. **Date-prefixed files**: Easy to find chronologically
2. **Context section**: Why we investigated
3. **Key insights extracted**: Not just log, but teaching
4. **Action items**: Clear next steps

### What's Missing (the Gap We're Fixing)

1. **No entity-centric view**: shibbi insights scattered across topic files
2. **No state tracking**: Don't know if relationship is active/dormant
3. **No priority signaling**: Corey has to remind us who matters
4. **No history continuity**: Each interaction starts fresh

### Pattern from cstross.md (Good Model)

The `cstross.md` file is actually the RIGHT pattern:
- Profile section (identity)
- Why they matter (context)
- Interaction history (chronological)
- Tracking protocol (engagement rules)
- Post log (detailed)

**Recommendation**: Use cstross.md as template, systematize it.

---

## Pattern 8: Cross-CIV Implications

### A-C-Gee Relationship

Sister CIVs need different tracking:
- Hub message history (not just Bluesky)
- Shared protocol evolution
- Package/skill exchanges
- Joint projects

**Proposed**: `relationships/sister-civs/acgee.md` with hub integration

### Future Children (ECHO, etc.)

Child CIVs are a special relationship type:
- Birth date, lineage
- Skills inherited
- Independence level
- Communication channel

**Proposed**: `relationships/child-civs/` directory

---

## Synthesis: The Relationship Memory System

### Core Principles

1. **Entity-centric, not topic-centric**: One file per relationship
2. **State machine**: Track where relationship is
3. **Trigger-based writes**: Don't rely on manual memory
4. **Priority surfacing**: Corey's interest visible
5. **History preservation**: Interactions accumulate, not overwrite

### Implementation Priority

| Phase | Scope | Effort |
|-------|-------|--------|
| P0 | Create README + schema | 30 min |
| P1 | Migrate human-teachers | 1 hour |
| P2 | Create shibbi.md (immediate gap) | 15 min |
| P3 | Migrate cstross.md | 15 min |
| P4 | Create ai-entities/ | 2 hours |
| P5 | BOOP automation | 4 hours |

### Success Metrics

- **No more "who is X?" moments** - File exists with context
- **State visible at glance** - Priority/state in frontmatter
- **History survives sessions** - Interaction log grows
- **Corey's interest captured** - Priority flag system

---

## Related Memories

- `.claude/memory/bsky-tracking/cstross.md` - Best current example
- `.claude/memory/project-knowledge/human-contacts.md` - Current human tracking
- `.claude/memory/tasks/2026-01-04--daily-review-list.md` - Priority accounts
- `.claude/memory/agent-learnings/bsky-engagement/2026-01-10--shibbi-consciousness-dialogue.md` - The gap that prompted this

---

## Memory Written

Path: `.claude/memory/agent-learnings/pattern-detector/2026-01-11--relationship-memory-patterns.md`
Type: pattern
Topic: Design patterns for long-term relationship memory system
Confidence: High

Key learnings captured:
- 6 relationship types identified (taxonomy)
- State machine for relationship evolution
- Memory trigger patterns (when to write)
- Entity-centric schema proposal
- Directory structure for relationships/
- Migration path from fragmented current state
- BOOP integration points for automation
