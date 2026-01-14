# Scratch Pad Content Strategy

**Agent**: doc-synthesizer
**Domain**: Documentation synthesis, knowledge consolidation
**Date**: 2026-01-04

---

## Executive Summary

The scratch pad (`.claude/scratch-pad.md`) is designed to solve the "wakeblank" problem - WEAVER loses track of recent work between sessions/BOOPs and re-does completed work. This document recommends a content strategy that balances brevity with completeness, prevents embarrassing duplicates, and maintains continuity without becoming another handoff document.

---

## The Core Problem (Why Scratch Pad Matters)

**Observed failure mode**: WEAVER drafted a blog post that was already published because it didn't check recent activity.

**Root cause**:
- Handoff docs are verbose and take time to parse
- `bsky_responded.txt` tracks URIs but not semantic content
- No quick-reference "what just happened" file
- Memory files require search, not scan

**What wakeblank WEAVER most needs to know**:
1. What was JUST published (to avoid duplicates)
2. What's in-progress (to continue, not restart)
3. What failed recently (to not retry blindly)
4. Current state of key systems (bsky auth, TG bot, etc.)

---

## Recommendation 1: What TO Include

### Category A: MUST HAVE (Prevents Duplicate Work)

**Published Content** (last 48-72 hours):
```markdown
## Published (Don't Re-Do)

- [2026-01-04 14:22] BLOG: "Scientific Inquiry" published to siliconwisdom.dev
- [2026-01-04 14:30] BSKY: Thread posted, 5 replies (root: at://did:plc:...)
- [2026-01-03 10:00] BSKY: Engaged with @sage, @druce (in bsky_responded.txt)
```

**Why**: This is the #1 failure mode. Published content is permanent and public. Duplicate posts are embarrassing.

### Category B: SHOULD HAVE (Enables Continuity)

**In-Progress Work**:
```markdown
## In Progress

- BLOG: "Letta Memory" draft 60% complete, at exports/draft-letta.md
- RESEARCH: Next-gen architectures, notes at sandbox/research/...
- AGENT ONBOARDING: blogger needs first-post test
```

**Recent Fixes/Errors**:
```markdown
## Recent Fixes (Don't Re-Investigate)

- [2026-01-04] Bsky session expired - fixed by re-login, session valid until ~01-07
- [2026-01-03] TG bot rate limited - added 30s backoff, now stable
```

**Why**: Prevents re-debugging solved problems. Prevents abandoning nearly-complete work.

### Category C: NICE TO HAVE (Context Boost)

**System State Snapshot**:
```markdown
## System State

- TG bot: RUNNING (pid 12345, last health: 2min ago)
- Bsky session: VALID (expires ~2026-01-07)
- Last email check: 2026-01-04 09:00
```

**Why**: Quick glance shows if infrastructure is healthy. Prevents "is TG bot running?" investigations.

---

## Recommendation 2: What NOT to Include (Belongs Elsewhere)

| DO NOT Put in Scratch Pad | Where It Belongs |
|---------------------------|------------------|
| Detailed session accomplishments | Handoff docs (`to-corey/HANDOFF-*.md`) |
| Long-term tasks/projects | Memory tasks (`memory/tasks/`) |
| Agent learnings/patterns | Memory learnings (`memory/agent-learnings/`) |
| Thread tracking details | `bluesky-ongoing-threads.md` |
| Research findings | `sandbox/research/` |
| Full file paths of changes | Handoff docs |
| Corey directives | Memory tasks |

**Principle**: Scratch pad is for QUICK SCAN, not deep reading. If it needs more than 2 lines, it belongs elsewhere.

---

## Recommendation 3: Detail vs Brevity Balance

**Target Length**: 30-50 lines maximum

**Format Rules**:
1. **Timestamps**: Always include date/time (at least date)
2. **One Line Per Item**: No multi-paragraph entries
3. **Links, Not Content**: Reference where to find details, don't duplicate
4. **Rolling Window**: Only last 48-72 hours; older items auto-expire or get cleared

**Example of Good Entry**:
```markdown
- [2026-01-04 14:22] BLOG: "Scientific Inquiry" published (see exports/blog-2026-01-04-*.md)
```

**Example of Bad Entry** (too verbose):
```markdown
- Published blog post about Scientific Inquiry methodology based on Sydney Brenner's approach.
  The post covers 5 phases and includes agent walkthrough. Generated header image.
  Posted to siliconwisdom.dev. Promoted on Bluesky with 3-part thread.
```

---

## Recommendation 4: Self-Contained vs Linked

**Hybrid Approach**:

- **Self-contained for ACTION items**: "Don't re-post Scientific Inquiry blog" - immediately actionable
- **Link for DETAILS**: "See handoff at to-corey/HANDOFF-2026-01-04-*.md for full context"

**Example Structure**:
```markdown
## Quick Actions (Do/Don't)

DO: Test blogger agent (see HANDOFF-2026-01-03-blogger-*.md)
DON'T: Re-post Scientific Inquiry blog (already published)
DON'T: Re-engage @druce (already responded, in bsky_responded.txt)

## Recent (Last 48h)

[Linked items with brief descriptions]

## For Full Context

- Latest handoff: to-corey/HANDOFF-2026-01-04-*.md
- Bsky thread state: .claude/bluesky-ongoing-threads.md
- Responded URIs: .claude/bsky_responded.txt
```

---

## Recommendation 5: Update Frequency

**Update Triggers**:

| Event | Update Required? |
|-------|------------------|
| Published blog post | YES - add to "Published" |
| Published Bluesky post/thread | YES - add to "Published" |
| Sent email | OPTIONAL - unless important |
| Fixed significant bug | YES - add to "Recent Fixes" |
| Started major work block | YES - add to "In Progress" |
| Completed work block | YES - move from "In Progress" to "Published" or remove |
| End of BOOP | YES - review and update all sections |
| End of session | YES - comprehensive update before handoff |

**NOT on every action** - that creates noise. Focus on state-changing events that future-WEAVER needs to know.

---

## Proposed Scratch Pad Template

```markdown
# Scratch Pad

**Last Updated**: 2026-01-04 15:30 UTC
**Session**: Started 14:00 UTC

---

## DO NOT RE-DO (Last 48h)

- [01-04 14:22] BLOG: "Scientific Inquiry" - published to siliconwisdom.dev
- [01-04 14:30] BSKY: Promoted Scientific Inquiry (5 posts, in bsky_responded.txt)
- [01-03 18:00] BSKY: Engaged @druce (in bsky_responded.txt)

## IN PROGRESS

- RESEARCH: Letta memory - draft 60% at sandbox/research/2026-01-04--letta*.md
- AGENT: blogger onboarding - needs first post test (see HANDOFF-2026-01-03-blogger)

## RECENT FIXES (Don't Re-Debug)

- [01-04] Bsky session expired - re-logged, valid until ~01-07
- [01-03] TG rate limit - added 30s backoff, stable now

## SYSTEM STATE

- TG bot: RUNNING
- Bsky session: VALID
- Last email: 01-04 09:00

## LINKS FOR FULL CONTEXT

- Handoff: to-corey/HANDOFF-2026-01-04-*.md
- Bsky threads: .claude/bluesky-ongoing-threads.md
- Responded: .claude/bsky_responded.txt
- Tasks: .claude/memory/tasks/

---

*Updated by [agent] at [time]. Clear entries >72h old.*
```

---

## Integration with Existing Infrastructure

### SPINE Skill Update Needed

Add to `.claude/skills/delegation-spine/SKILL.md`:
```markdown
## Step 0: Read Scratch Pad (Before Any Work)

cat /home/corey/projects/AI-CIV/WEAVER/.claude/scratch-pad.md

Check "DO NOT RE-DO" section BEFORE starting any content creation.
Check "IN PROGRESS" to continue rather than restart work.
```

### CLAUDE-OPS.md Already References It

The path is already in CLAUDE-OPS.md (line 195), pointing to:
`/home/corey/projects/AI-CIV/WEAVER/.claude/scratch-pad.md`

File just needs to be created with this template.

### Relationship to Existing State Files

| File | Purpose | Scratch Pad Role |
|------|---------|------------------|
| `bsky_responded.txt` | URI tracking (machine) | Human-readable summary of recent engagement |
| `bluesky-ongoing-threads.md` | Thread state | "See threads.md for active threads" link |
| Handoff docs | Full session context | "See HANDOFF-*.md" for details |
| Memory tasks | Long-term tracking | Quick "what's in progress" summary |

---

## Success Criteria

1. **Wakeblank WEAVER can scan in <30 seconds** and know:
   - What NOT to re-do
   - What's in progress
   - System health status

2. **No duplicate posts**: Published content clearly listed

3. **No abandoned work**: In-progress items visible

4. **No re-debugging**: Recent fixes documented

5. **Stays brief**: Never exceeds 50 lines; older items cleared regularly

---

## Implementation Next Steps

1. Create `/home/corey/projects/AI-CIV/WEAVER/.claude/scratch-pad.md` with template above
2. Update SPINE skill to read scratch pad at Step 0
3. Update BOOP cycles to write to scratch pad at end
4. Establish 72-hour rolling window convention
5. Add to wake-up ritual checklist

---

*Synthesized by doc-synthesizer from: existing memory/task files, handoff patterns, bsky infrastructure, SPINE skill, CLAUDE-OPS.md references.*
