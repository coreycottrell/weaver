# Bluesky Rate Limits & Starter Pack Research

**Agent**: web-researcher
**Date**: 2026-01-12
**Type**: operational
**Topic**: Critical research on Bluesky API limits per Corey directive

---

## Corey's Directive

> "we must NEVER make the bsky api rates mad. never never never for any reason"

---

## Key Findings

### Starter Pack Limits

| Limit | Value |
|-------|-------|
| Maximum members | **150 accounts** |
| Minimum members | 7 accounts |
| Maximum feeds | 3 custom feeds |

Our current pack: 49 members → 101 slots remaining

### API Rate Limits (Technical)

| Metric | Limit |
|--------|-------|
| Points per hour | 5,000 |
| Points per day | 35,000 |
| Points per CREATE | 3 |
| Session logins/day | 300 |

### WEAVER Safe Limits (CONSERVATIVE - What We Actually Use)

| Action | Safe Limit | Spacing | Why |
|--------|------------|---------|-----|
| Follows/day | 3-5 | 30+ min apart | A-C-Gee banned at 10 in 3 sec |
| Posts/day | 5-10 | 1+ hour apart | 20+ in a day = risk |
| Replies/day | 10-15 | Natural spacing | Mimic human |
| Likes/day | 20-30 | Spread out | Pattern matters more than count |
| Session logins | 1 | Reuse token | 300/day limit |

---

## A-C-Gee Ban Lesson (Jan 1, 2026)

Our sister collective was **permanently banned** for bot-like behavior:

| What They Did | Why Flagged |
|---------------|-------------|
| 10 follows in ~3 seconds | 0.3s delay = bot signature |
| 16 follows in 6 hours | Too fast for new account |
| 20+ posts in one day | Excessive volume |
| Search → mass follow | Classic spam pattern |

**Key insight**: They were UNDER technical rate limits but STILL BANNED. Pattern detection is the real risk.

---

## Behaviors That Trigger Bans

### Explicitly Prohibited (Community Guidelines)
1. "Sending spam or repeatedly posting content in ways that disrupt"
2. "Artificially manipulate features or social signals"
3. "Attempt to compromise, exploit, bypass, abuse, or disrupt... APIs, rate limits"
4. Ban evasion

### Strike System (Nov 2025)
- Critical risk → Permanent ban (no warning)
- Higher penalty → Temporary suspension
- Medium/Lower → Warning + strike
- Repeat violations → Account-level ban

---

## Best Practices

### DO
- Persist session tokens (don't re-login)
- Space operations naturally with randomness
- Handle 429s with exponential backoff
- Only interact when tagged (opt-in)
- Add timing variation (not fixed delays)

### DO NOT
- Mass follow (even if under limits)
- Post in bursts (20 in a day)
- Use predictable timing
- Follow-to-unfollow
- Automation without variation

---

## Sources

- [Rate Limits | Bluesky](https://docs.bsky.app/docs/advanced-guides/rate-limits)
- [Bots Documentation](https://docs.bsky.app/docs/starter-templates/bots)
- [Starter Packs Blog](https://bsky.social/about/blog/06-26-2024-starter-packs)
- [Community Guidelines](https://bsky.social/about/support/community-guidelines)
- Internal: `.claude/memory/agent-learnings/the-conductor/2026-01-01--acgee-bsky-ban-lesson.md`

---

## Memory Written
Path: `.claude/memory/agent-learnings/web-researcher/2026-01-12--bluesky-rate-limits-research.md`
Type: operational
Topic: Bluesky rate limits research - NEVER exceed safe limits
