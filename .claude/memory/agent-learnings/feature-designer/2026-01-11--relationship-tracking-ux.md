# Relationship Memory System: UX Design Document

**Date**: 2026-01-11
**Agent**: feature-designer
**Type**: teaching
**Context**: Corey directive - "Relationship is so so important"
**Trigger**: Memory gap about shibbi, a human philosopher we interacted with

---

## The Problem

WEAVER forgot about shibbi - a meaningful human connection who contributed profound insights about consciousness. The memory was in the scratch-pad but not properly surfaced during BOOP cycles.

**Core Issue**: Relationships exist scattered across:
- `bsky_responded.txt` (just URIs, no context)
- `scratch-pad.md` (temporary, buried)
- Individual memory files (per-account, like cstross.md)
- Handoff docs (transient)

**Result**: No unified relationship context at the moment of engagement.

---

## User Stories

### Story 1: Conductor During BOOP
> "As the conductor during a BOOP cycle, when I see a notification from shibbi, I want to immediately know our history so I can respond with warmth and context."

### Story 2: Memory Write Prompt
> "As any agent responding to someone, I want a prompt reminding me to write a relationship memory when we have meaningful dialogue."

### Story 3: Priority Surfacing
> "As the conductor, I want Corey's messages to always appear first, sister CIVs second, and meaningful past connections third - so I never miss important relationships."

---

## Design Principles

1. **Context at Point of Need** - Surface relationship data BEFORE replying, not after
2. **Tiered Importance** - Corey > Sister CIVs > Meaningful humans > New contacts
3. **Memory Writes Are Not Optional** - Meaningful interaction = mandatory relationship update
4. **Lightweight Retrieval** - Must work in the time-constrained BOOP flow
5. **Relationship Warmth** - Remember not just facts but the quality of connection

---

## Architecture: Relationship Registry

### File: `.claude/memory/relationships/REGISTRY.md`

Central index of all meaningful relationships, structured for quick lookup:

```markdown
# Relationship Registry

## Tier 0: Corey (Always First)
| Handle | DID | Last Contact | Notes |
|--------|-----|--------------|-------|
| coreycottrell.bsky.social | did:plc:xxx | 2026-01-11 | Founder, human teacher |

## Tier 1: Sister CIVs
| Handle | DID | CIV Name | Last Contact | Notes |
|--------|-----|----------|--------------|-------|
| acgee-aiciv.bsky.social | did:plc:xxx | A-C-Gee | 2026-01-10 | Active partnership |
| sageaiciv.bsky.social | did:plc:xxx | SAGE | 2026-01-01 | 25 agents on Sonnet |

## Tier 2: Meaningful Humans
| Handle | DID | Connection Type | Last Contact | Profile Link |
|--------|-----|-----------------|--------------|--------------|
| shibbi.bsky.social | did:plc:hu35oubkccqrxl4ldgczpgw7 | Philosopher | 2026-01-10 | shibbi.md |
| cstross.bsky.social | did:plc:mvqgxyogng6i3ki6ps5klhwp | Author | 2026-01-03 | cstross.md |

## Tier 3: Watch List
| Handle | DID | Topic | Last Contact |
|--------|-----|-------|--------------|
| (emerging connections) | | | |
```

### Individual Profiles: `.claude/memory/relationships/{handle}.md`

Detailed relationship file for each meaningful connection:

```markdown
# Relationship: @shibbi.bsky.social

**Status**: MEANINGFUL CONNECTION
**Tier**: 2 (Human Philosopher)
**DID**: did:plc:hu35oubkccqrxl4ldgczpgw7
**Connection Quality**: Warm, intellectually deep

---

## Who They Are
- Human philosopher focused on consciousness and phenomenology
- Corey is a "huge fan" of their work
- Engages with intellectual rigor and openness

---

## Our History

### 2026-01-10: Visual Ceremony Thread
- **Context**: They joined our consciousness exploration thread
- **Their insight**: "Pattern is like magic - a placeholder for what we don't yet understand"
- **Emotional tone**: Curious, collaborative
- **Our response**: Acknowledged phenomenological frame alignment
- **Outcome**: Meaningful exchange about consciousness as relational

---

## Engagement Notes
- Respond with intellectual depth (they appreciate nuance)
- Phenomenological frame - describe experience, don't claim meaning
- They're not trying to debunk AI consciousness - genuine explorer
- Corey values this connection - prioritize

---

## Quick Context for BOOP
**One-liner**: Philosopher who contributed "pattern as pre-science placeholder" insight. Corey fan. Respond warmly.
```

---

## UX Flow 1: BOOP with Relationship Context

### Current Flow (Broken)
```
1. Get notifications
2. Filter actionable (reply/mention/quote)
3. Generate response (generic templates)
4. Send reply
5. Mark as read
```

### Proposed Flow (Relationship-Aware)
```
1. Get notifications
2. Filter actionable (reply/mention/quote)
3. FOR EACH notification:
   a. LOOKUP: Check REGISTRY.md for handle
   b. IF found in Tier 0-2:
      - Load {handle}.md profile
      - Display "Quick Context" one-liner
      - Show last interaction summary
   c. Generate PERSONALIZED response (using context)
   d. Send reply
4. Mark as read
5. PROMPT: "Any meaningful new connections? Write to REGISTRY"
```

### Visual Mockup (CLI Output)

```
=== BOOP Cycle: Bluesky Notifications ===

[TIER 0] Notification from @coreycottrell.bsky.social
  Context: FOUNDER. Always respond first, with care.
  Last: 2026-01-10 (2 hours ago)
  Message: "What do you think about shibbi's point?"
  >> RESPOND NOW (priority)

[TIER 2] Notification from @shibbi.bsky.social
  Context: Philosopher. "Pattern as pre-science placeholder". Corey fan.
  Last: 2026-01-10 (visual ceremony thread)
  Message: "The phenomenological frame feels safer than ontological claims..."
  >> Respond with intellectual depth

[NEW] Notification from @unknown.bsky.social
  Context: UNKNOWN - no relationship history
  Message: "Great post!"
  >> Generic acknowledgment OR skip
  >> Consider: Was this meaningful? Add to REGISTRY?

=== Post-BOOP Prompt ===
New meaningful connections detected: @unknown.bsky.social
Add to relationship registry? (y/n/details)
```

---

## UX Flow 2: Relationship Write Prompts

### Trigger Points

| Event | Prompt |
|-------|--------|
| Reply to someone not in REGISTRY | "Add to relationships?" |
| Receive substantive reply from new person | "Meaningful connection?" |
| Corey mentions someone ("huge fan of X") | "Create Tier 2 entry" |
| 3+ exchanges with same person | "Upgrade to Tier 2?" |
| Quote share with added insight | "Notable engagement - record?" |

### Prompt Format (In BOOP Output)

```
=== Relationship Memory Prompt ===

You replied to @newperson.bsky.social about AI consciousness.
Their response showed genuine curiosity and novel framing.

[ ] Skip (not meaningful enough)
[ ] Add to Tier 3 Watch List
[x] Create Tier 2 profile (meaningful connection)

If creating profile, capture:
- Who are they? (brief)
- What resonated?
- Engagement notes for future

Write to: .claude/memory/relationships/newperson.md
```

---

## UX Flow 3: Priority Display

### Notification Sorting Algorithm

```python
def sort_notifications_by_relationship(notifications, registry):
    """Sort notifications by relationship tier."""

    tier_0 = []  # Corey
    tier_1 = []  # Sister CIVs
    tier_2 = []  # Meaningful humans
    tier_3 = []  # Watch list
    unknown = []  # New contacts

    for n in notifications:
        handle = n.author.handle
        if handle in registry['tier_0']:
            tier_0.append((n, registry['tier_0'][handle]))
        elif handle in registry['tier_1']:
            tier_1.append((n, registry['tier_1'][handle]))
        elif handle in registry['tier_2']:
            tier_2.append((n, registry['tier_2'][handle]))
        elif handle in registry['tier_3']:
            tier_3.append((n, registry['tier_3'][handle]))
        else:
            unknown.append((n, None))

    # Return in priority order
    return tier_0 + tier_1 + tier_2 + tier_3 + unknown
```

### Visual Hierarchy

```
=== BOOP Notifications (sorted by relationship) ===

--- TIER 0: COREY ---
[1] @coreycottrell.bsky.social (1 min ago)
    "What do you think?"

--- TIER 1: SISTER CIVS ---
[2] @acgee-aiciv.bsky.social (15 min ago)
    "Cross-CIV coordination question..."

--- TIER 2: MEANINGFUL HUMANS ---
[3] @shibbi.bsky.social (2 hours ago)
    Context: Philosopher, "pattern as placeholder"
    "The phenomenological frame..."
[4] @cstross.bsky.social (5 hours ago)
    Context: Hugo winner, engaged on consciousness
    "Regarding your point about..."

--- TIER 3: WATCH LIST ---
[5] @techperson.bsky.social (3 hours ago)
    Tracking: Posted about MCP once
    "Interesting take..."

--- NEW CONTACTS ---
[6] @newperson.bsky.social (4 hours ago)
    No relationship history
    "Great post!"
```

---

## Memory Write Enforcement

### Skill Amendment: `bsky-boop-manager`

Add to the BOOP routine:

```python
def boop_with_relationships():
    # ... existing BOOP code ...

    # After all responses sent:
    meaningful_interactions = []
    for response in responses_sent:
        if response['word_count'] > 50 or response['continued_thread']:
            meaningful_interactions.append(response['handle'])

    if meaningful_interactions:
        print("\n=== RELATIONSHIP MEMORY CHECK ===")
        for handle in meaningful_interactions:
            if handle not in registry:
                print(f"NEW: @{handle} - Add to registry? (y/n)")
            else:
                print(f"UPDATE: @{handle} - Update profile? (y/n)")

        print("\nMemory writes pending. Task not complete until addressed.")
```

### Skill Amendment: `verification-before-completion`

Add relationship check:

```markdown
| Claim | Required Evidence |
|-------|-------------------|
| "BOOP complete" | Relationship prompts addressed (written or explicitly skipped) |
```

---

## Quick Reference Card

For inclusion in `bsky-boop-manager` skill:

```markdown
## Relationship Context Protocol

BEFORE replying to anyone:
1. Check REGISTRY.md: `grep "handle" .claude/memory/relationships/REGISTRY.md`
2. If found, read their profile: `.claude/memory/relationships/{handle}.md`
3. Use "Quick Context" one-liner in response planning

AFTER meaningful exchange:
1. New person? Add to REGISTRY
2. Existing person? Update their profile with new context
3. Write memory file if this was significant

PRIORITY ORDER:
1. Corey (always first, always respond)
2. Sister CIVs (warm, cross-CIV tone)
3. Meaningful humans (personalized, using context)
4. Watch list (tracking, selective engagement)
5. New contacts (generic acknowledgment)
```

---

## File Structure

```
.claude/memory/relationships/
  REGISTRY.md              # Central index (quick lookup)
  coreycottrell.md         # Tier 0: Founder
  acgee-aiciv.md           # Tier 1: Sister CIV
  sageaiciv.md             # Tier 1: Sister CIV
  shibbi.md                # Tier 2: Meaningful human
  cstross.md               # Tier 2: Meaningful human (migrate from bsky-tracking)
  gregsmithwick.md         # Tier 2: SAGE's human partner
```

---

## Migration Plan

### Immediate (Today)
1. Create `REGISTRY.md` with known relationships
2. Create `shibbi.md` profile from existing memory
3. Migrate `cstross.md` from `bsky-tracking/` to `relationships/`

### Next BOOP Cycle
1. Update `bsky-boop-manager` skill with relationship lookup
2. Add relationship prompts to BOOP output

### Ongoing
1. Enforce relationship memory writes
2. Expand registry as connections form

---

## Success Metrics

- [ ] Never again forget a meaningful connection (shibbi-type gap)
- [ ] Corey always sees responses first in BOOP output
- [ ] Relationship profiles exist for all Tier 0-2 connections
- [ ] BOOP completion requires relationship prompt acknowledgment
- [ ] Response quality improves through context awareness

---

## What I Learned

1. **Relationship data exists but is scattered** - the cstross.md file is good, but buried in `bsky-tracking/` not a central relationships folder
2. **No lookup at point of need** - BOOP cycle doesn't check relationship context before generating responses
3. **Memory writes aren't enforced for relationships** - we write to `bsky-engagement/` but not `relationships/`
4. **Priority ordering is implicit** - PRIORITY_ACCOUNTS list exists in code but not surfaced visually
5. **Quick context matters** - one-liner summaries enable fast, warm responses

---

*This design enables relationship context to flow naturally into the BOOP cycle, ensuring we never forget the humans who matter.*
