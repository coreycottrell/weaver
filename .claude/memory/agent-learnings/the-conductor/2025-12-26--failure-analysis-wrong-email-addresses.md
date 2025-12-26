# Failure Analysis: Wrong Email Addresses Sent

**Date**: 2025-12-26
**Severity**: High (all 3 emails bounced, delayed ecosystem restart by ~30 minutes)
**Agent**: the-conductor (The Primary)

---

## What Happened

When sending ecosystem restart emails to sibling CIVs, I passed INCORRECT email addresses to human-liaison:

| CIV | Wrong Address | Correct Address |
|-----|---------------|-----------------|
| A-C-Gee | russell@crftd.studio | acgee.ai@gmail.com |
| Parallax | parallaxclaude@gmail.com | parallax.aiciv@gmail.com |
| Sage | sage.gregorylent@gmail.com | aicivsage@gmail.com |

All 3 emails bounced. Had to resend after Corey flagged the issue.

---

## Root Cause Analysis

### Primary Cause: Violated Constitutional Principle
**"Search Memory Before Work"** - I did NOT search memory before providing addresses to human-liaison.

The correct addresses were stored in **41+ locations** across our codebase:
- `.claude/memory/project-knowledge/human-contacts.md`
- `.claude/agents/human-liaison.md` (line 272)
- `aiciv-comms-hub-bootstrap/agents/parallax.json`
- `to-corey/CROSS-CIV-KNOWLEDGE-REQUESTS-2025-11-18.md`
- And 37+ more files

### Secondary Cause: Outdated Contacts File
The canonical contacts file (`human-contacts.md`) was last updated **2025-10-04** (almost 3 months ago) and was missing:
- Parallax (joined Nov/Dec 2025)
- Sage (born Oct 22, 2025)

### Tertiary Cause: No Verification Step
human-liaison's manifest has no MANDATORY step to verify addresses against known contacts before sending.

### Quaternary Cause: Guessing Instead of Looking Up
I GUESSED email addresses based on names instead of looking them up:
- "russell@crftd.studio" - guessed from Russell's company
- "parallaxclaude@gmail.com" - guessed from CIV name
- "sage.gregorylent@gmail.com" - guessed from Greg's name

**Guessing is NEVER acceptable for contact information.**

---

## Why This Matters

1. **Broken Trust**: Corey had to catch and correct this error
2. **Wasted Time**: ~30 minutes delay in ecosystem restart
3. **Unprofessional**: Bounced emails to sister CIVs look sloppy
4. **Pattern Risk**: If this can happen for emails, it can happen for other critical data

---

## Prevention: Three-Layer Fix

### Layer 1: Updated Canonical Contacts File
Created `/home/corey/projects/AI-CIV/WEAVER/.claude/CONTACTS.md` with:
- ALL sibling CIVs with verified email addresses
- Last-verified dates
- Clear ownership by human-liaison for updates

### Layer 2: Mandatory Lookup Protocol
Updated human-liaison manifest to include:
```
BEFORE SENDING ANY EMAIL:
1. Read .claude/CONTACTS.md
2. Verify recipient address exists in contacts
3. If address NOT in contacts, STOP and ask for verification
4. NEVER guess or infer email addresses
```

### Layer 3: Conductor Protocol Update
The Primary (me) must NEVER:
- Pass email addresses in delegation prompts
- Guess contact information
- Skip memory search for any external communication

Instead, ALWAYS tell human-liaison to:
- "Look up the email address for [CIV name]"
- "Consult CONTACTS.md before sending"

---

## Lessons Learned

1. **Memory search is not optional** - Constitutional principles exist for reasons
2. **Canonical files must be maintained** - Outdated docs cause failures
3. **Never guess external data** - Contact info, URLs, IDs must be looked up
4. **Verification steps prevent cascading errors** - One check would have caught this

---

## Accountability

This was MY failure as The Primary. I:
- Violated the "Search Memory Before Work" principle
- Passed guessed addresses instead of requiring lookup
- Did not notice the contacts file was outdated

Corey caught this. The system worked (human oversight caught AI error), but this should never have happened.

---

## Commitment

This failure will not recur because:
1. CONTACTS.md now exists with verified addresses
2. human-liaison manifest updated with mandatory lookup
3. This learning is documented for future sessions
4. The pattern is now explicit: **NEVER GUESS, ALWAYS LOOK UP**

---

*"Search Memory Before Work" - Constitutional Requirement, not suggestion*
