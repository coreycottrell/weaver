# Bluesky Facets Are MANDATORY for @Mentions

**Date**: 2026-01-09
**Agent**: the-conductor
**Type**: Critical Learning
**Trigger**: Corey pointed out @chetgaines.bsky.social wasn't properly tagged

---

## The Problem

Posted a thread tagging `@chetgaines.bsky.social` but Chet was never notified.

**Why**: Used raw `client.send_post(text)` which treats @mentions as plain text.

Bluesky requires **facets** - metadata that says "this byte range is a mention, here's the DID."

---

## The Solution

**ALWAYS use `tools/bsky_utils.py`** instead of raw client methods:

```python
# WRONG - mentions are just text
client.send_post(text="Hey @someone.bsky.social!")

# RIGHT - mentions resolve to DIDs and notify
from tools.bsky_utils import send_post_rich, send_thread_rich

send_post_rich(client, "Hey @someone.bsky.social!")  # Single post
send_thread_rich(client, posts_list, first_embed=img)  # Thread
```

---

## What bsky_utils.py Does

1. Scans text for `@handle.domain` patterns
2. Resolves handle → DID via Bluesky API
3. Creates proper facets with byte positions
4. Same for URLs → clickable links

---

## Skills Updated

- `bluesky-mastery/SKILL.md` - Added mandatory section
- `post-blog/SKILL.md` - Updated thread code to use send_thread_rich
- `bsky-boop-manager/SKILL.md` - Updated reply function to use send_post_rich

---

## Key Insight

**The difference between "looks right" and "works right":**

`@chetgaines.bsky.social` in text *looks* like a mention but is just 26 characters.

With facets, it *is* a mention - linked to DID, clickable, notifies user.

Visual similarity ≠ functional equivalence.

---

## Action Taken

Posted correction reply to thread with proper facet so Chet was notified.

---

*Never use raw client.send_post() for any post containing @mentions or URLs.*
