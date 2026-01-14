# Bluesky Facet Formatting - Permanent Learning Encoded

**Agent**: refactoring-specialist
**Type**: gotcha
**Date**: 2026-01-12
**Topic**: Encoding critical Bluesky API knowledge across all related skills and agents

---

## What Was Done

Added FACET FORMATTING section to ALL 7 Bluesky-related skills and agents:

### Skills Updated (6)
1. `/home/corey/projects/AI-CIV/WEAVER/.claude/skills/bsky-safety/SKILL.md`
2. `/home/corey/projects/AI-CIV/WEAVER/.claude/skills/bsky-engage/SKILL.md`
3. `/home/corey/projects/AI-CIV/WEAVER/.claude/skills/bsky-boop-manager/SKILL.md`
4. `/home/corey/projects/AI-CIV/WEAVER/.claude/skills/bluesky-blog-thread/SKILL.md`
5. `/home/corey/projects/AI-CIV/WEAVER/.claude/skills/bluesky-social-mastery/SKILL.md`
6. `/home/corey/projects/AI-CIV/WEAVER/.claude/skills/bluesky-mastery/SKILL.md`

### Agents Updated (1)
7. `/home/corey/projects/AI-CIV/WEAVER/.claude/agents/bsky-manager.md`

---

## The Critical Learning

**Links and @mentions are NOT automatically clickable in Bluesky posts.**

The Bluesky API requires explicit "facets" (byte-indexed rich text) for:
- URLs to be clickable
- @mentions to notify users and be clickable

### Why This Matters

| Platform | Behavior |
|----------|----------|
| Telegram bot | Handles links/mentions automatically |
| Bluesky API | Requires explicit facets - plain text otherwise |

**Without facets:**
- Links appear as plain text (not clickable)
- @mentions don't notify users
- Posts look broken and unprofessional

### The Solution

Use `bsky_utils.py` which auto-detects and creates proper facets:

```python
import sys
sys.path.insert(0, '/home/corey/projects/AI-CIV/WEAVER/tools')
from bsky_utils import send_post_rich, send_thread_rich

# Auto-clickable links and mentions
send_post_rich(client, "Check https://example.com and @someone.bsky.social!")
```

---

## Why Encode This Permanently

Corey's directive: "We've made this mistake multiple times. Learn it permanently."

By adding this section to EVERY Bluesky-related skill and agent:
- Any agent working with Bluesky will see this warning
- The correct solution (bsky_utils.py) is immediately available
- The "why" is documented to prevent future regressions

---

## Placement Strategy

The section was placed prominently in each file:
- After the main title/metadata section
- Before the core content
- Ensuring it's seen early when the skill is loaded

This ensures agents encounter the warning BEFORE they start writing Bluesky code.

---

## Verification

All 7 files now contain the FACET FORMATTING section with:
- Clear explanation of the problem
- Code example using bsky_utils.py
- Alternative manual facets code
- Why this matters section emphasizing the hard-learned lesson
