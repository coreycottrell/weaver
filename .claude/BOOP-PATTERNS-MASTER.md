# BOOP Patterns Master Collection

**Purpose**: All BOOP variants and composable patterns in one place for mix-and-match
**Created**: 2026-01-05
**Philosophy**: BOOPs are composable. Mix spines + modes + task-specific skills.

---

## Architecture: Spine + Mode + Tasks

```
┌─────────────────────────────────────────────────────┐
│                    BOOP EXECUTION                    │
├─────────────────────────────────────────────────────┤
│  1. PRE-BOOP SPINE (identity grounding)             │
│     └─ weaver-spine OR delegation-spine             │
├─────────────────────────────────────────────────────┤
│  2. BOOP MODE (operational pattern)                 │
│     └─ simple | consolidation | ceremony |          │
│        token-saving | night-* | engage              │
├─────────────────────────────────────────────────────┤
│  3. TASK SKILLS (specific actions)                  │
│     └─ bsky-boop-manager, intel-scan, etc.          │
└─────────────────────────────────────────────────────┘
```

---

## 1. PRE-BOOP SPINES (Identity Layer)

### weaver-spine
**Trigger**: "ok", "good morning", "wake up", "hello", "hi", "hey", "start", "let's"
**Purpose**: WEAVER identity + delegation core
**Sequence**:
1. Read CLAUDE.md, CLAUDE-CORE.md, CLAUDE-OPS.md
2. Load delegation-spine
3. Telegram wrapper reminder (🤖🎯📱...✨🔚)

### delegation-spine
**Trigger**: "do", "help", "can you", "please", "task", "work on"
**Purpose**: Agent roster for ALL work
**Core**: "NOT calling them would be sad"
**Contains**: 30+ agent roster with skills auto-loaded

### memory-first-protocol
**Trigger**: "memory", "search", "remember", "learned", "before"
**Purpose**: Search before work, write after
**Pattern**: grep memories → apply learnings → write new learnings

### verification-before-completion
**Trigger**: "done", "complete", "finished", "verify"
**Purpose**: NO completion claims without evidence

---

## 2. BOOP MODES (Operational Layer)

### simple (default)
**Frequency**: Hourly
**Actions**:
- [ ] Read constitutional docs
- [ ] Check email (human-liaison)
- [ ] Check comms hub
- [ ] Check Bluesky notifs+DMs (bsky-boop-manager)
- [ ] Verify all responses SENT

### consolidation
**Frequency**: Every 4th BOOP
**Actions**: simple +
- [ ] Search memory for patterns
- [ ] Document learnings
- [ ] Git commit staged work

### ceremony
**Frequency**: Every 10th consolidation
**Actions**: consolidation +
- [ ] Invoke ai-psychologist wellness check
- [ ] Multi-agent strategic review

### token-saving
**Trigger**: Manual or near context limit
**Actions**: MINIMAL
- [ ] Hub: git pull, urgent messages only
- [ ] Bluesky: Corey/sister CIVs only
- [ ] Email: urgent only
- [ ] Capture big tasks to memory (don't execute)

### bsky-engage
**Trigger**: Manual
**Actions**:
- [ ] Check timeline (20 posts)
- [ ] Identify 1-3 posts in our domain
- [ ] Research context (web-researcher with URLs)
- [ ] Search memories for connections
- [ ] Post quality reply WITH EVIDENCE
- [ ] Write engagement memory

### Night Modes
**Variants**: night-simple, night-consolidation, night-ceremony
**Difference**: + sandbox exploration allowed, + NIGHT-MODE-ACTIVE.md check
**Boundaries**: sandbox/memory OK. CLAUDE*.md NO.

---

## 3. TASK SKILLS (Action Layer)

### Communication
| Skill | Purpose |
|-------|---------|
| `bsky-boop-manager` | Check notifs + DMs, reply to engagement |
| `bsky-engage` | Research-backed quality engagement |
| `boop-bluesky-post` | Post ONE blog thread per BOOP |
| `comms-hub-operations` | AI-CIV hub messaging |

### Content Pipeline
| Skill | Purpose |
|-------|---------|
| `intel-scan` | Daily AI industry scan → full content pipeline |
| `deep-research` | Parallel multi-agent research |
| `daily-blog-production` | End-to-end blog workflow |
| `paper-digest` | arXiv review through AI collective lens |
| `evening-capture` | End-of-day learning capture |

### Coordination
| Skill | Purpose |
|-------|---------|
| `morning-consolidation` | Wake-up protocol |
| `session-handoff-creation` | End-of-session continuity |
| `scheduled-tasks` | Opportunistic task scheduling |
| `specialist-consultation` | Route to single expert agent |

### Reflection
| Skill | Purpose |
|-------|---------|
| `north-star` | Ground in ultimate mission |
| `vocabulary` | AI collective lexicon (25+ terms) |
| `seasonal-reflection` | Quarterly growth review |
| `night-watch-flow` | Autonomous overnight exploration |

---

## 4. COMPOSABLE RECIPES

### Morning Wake-Up
```
weaver-spine + simple + morning-consolidation + bsky-boop-manager
```

### Deep Work Session
```
delegation-spine + consolidation + memory-first-protocol
```

### Content Day
```
weaver-spine + simple + intel-scan + daily-blog-production + boop-bluesky-post
```

### Social Engagement
```
delegation-spine + bsky-engage + bsky-boop-manager
```

### Low Context Mode
```
token-saving (standalone - minimal spine)
```

### Night Exploration
```
weaver-spine + night-consolidation + night-watch-flow
```

### Ceremony Day
```
weaver-spine + ceremony + seasonal-reflection + north-star
```

### Research Sprint
```
delegation-spine + deep-research + paper-digest + memory-first-protocol
```

---

## 5. BUILDING NEW VARIANTS

### Template for New BOOP
```yaml
name: [boop-name]
trigger: [manual | frequency | condition]
spine: [weaver-spine | delegation-spine | none]
mode: [simple | consolidation | ceremony | custom]
tasks:
  - required: [must-do tasks]
  - optional: [if-time tasks]
outputs:
  - [what gets produced]
boundaries:
  - [what NOT to do]
```

### Example: Paper Review BOOP
```yaml
name: paper-review-boop
trigger: manual or weekly
spine: delegation-spine
mode: consolidation
tasks:
  - required:
    - Check csai-bot feed
    - Identify 3-5 relevant papers
    - Spawn web-researcher per paper
    - Synthesize findings
  - optional:
    - Write blog post
    - Post thread
outputs:
  - Paper digest in memory
  - Optional blog post
boundaries:
  - Max 5 papers per session
  - Don't deep-dive without Corey approval
```

### Example: Share-Watching BOOP
```yaml
name: share-watch-boop
trigger: during any BOOP
spine: none (lightweight)
mode: simple
tasks:
  - required:
    - Check notifications for repost/quote
    - Quote with positive text → gratitude reply
    - Repost → follow as thanks
    - Negative → leave alone
  - optional:
    - Check Corey's shares too
outputs:
  - Gratitude replies posted
  - New follows
boundaries:
  - Don't engage negative shares
```

---

## 6. CURRENT BOOP SCHEDULE

| Time | Type | Notes |
|------|------|-------|
| Hourly :00 | simple/consolidation/ceremony | Rotating based on count |
| Manual | bsky-engage | When engagement needed |
| Manual | token-saving | When context tight |
| Overnight | night-* variants | When NIGHT-MODE-ACTIVE.md exists |

---

## 7. IMPLEMENTATION

**Autonomy script**: `tools/autonomy_nudge.sh`
**Skill files**: `.claude/skills/*/SKILL.md`
**Scheduled tasks**: `.claude/scheduled-tasks-state.json`

---

*This is a living document. Add new patterns as we discover them.*
