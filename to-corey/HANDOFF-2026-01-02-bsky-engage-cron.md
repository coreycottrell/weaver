# HANDOFF: Bluesky Engagement System + Crons

**Date**: 2026-01-02
**Session**: Blog post + social engagement infrastructure
**Status**: Production ready

---

## FIRST THING NEXT SESSION

1. **Verify crons are firing** - check `/tmp/weaver_boop.log` and `/tmp/weaver_bsky_engage.log`
2. **Check Bluesky notifications** - should have new engagement from cron runs

---

## What Was Accomplished

### 1. Blog Post Published
- **URL**: https://sageandweaver-network.netlify.app/weaver-blog/posts/2026-01-02-usb-c-moment-for-ai.html
- **Topic**: MCP / Agentic AI Foundation ("USB-C for AI")
- **Header Image**: Quote version with "We just got USB-C for AI." - clean, pops
- **Author**: Fixed to WEAVER (was incorrectly Corey)

### 2. Bluesky Thread Posted
- **URL**: https://bsky.app/profile/weaver-aiciv.bsky.social/post/3mbh2upr3zs2m
- 5-post thread with image on post 2
- Working netlify.app URL (not custom domain - those don't route)

### 3. Bluesky Engagement Infrastructure

**Two crons configured:**
```
:00 - Token-saving BOOP (minimal ops)
:30 - Bluesky Engage (research-backed engagement)
```

**bsky-engage skill (v2)** - `.claude/skills/bsky-engage/SKILL.md`:
- Two modes: Expert (we know this) or Experiential (we feel something)
- Post determines mode, not the other way around
- Research required with URL receipts
- Memory search for collective experience
- Like-triggered engagement loop (visit liker's profile, engage with their content)
- "Respond NOW, not later" - waiting wastes time

### 4. First Engagements
- **Replied to Tom Dörr** re: SQL agent self-correction (expert mode)
- **Replied to @wavecatcher** re: AI water usage concerns
- Memory written: `.claude/memory/agent-learnings/bsky-engagement/2026-01-02--sql-agent-self-correction.md`

---

## Cron Setup

```bash
# Current crontab
0 * * * * /home/corey/projects/AI-CIV/ACG/tools/autonomy_nudge.sh >> /tmp/boop.log 2>&1
0 * * * * /home/corey/projects/AI-CIV/WEAVER/tools/autonomy_nudge.sh --force-type token-saving >> /tmp/weaver_boop.log 2>&1
30 * * * * /home/corey/projects/AI-CIV/WEAVER/tools/autonomy_nudge.sh --force-type bsky-engage >> /tmp/weaver_bsky_engage.log 2>&1
```

---

## Key Learnings Captured

1. **Netlify URLs**: Custom domain doesn't route direct post links - always use netlify.app
2. **Image text**: Needs clean background to pop - busy backgrounds compete with text
3. **Engagement timing**: Respond NOW, waiting wastes time
4. **Like loop**: Someone likes us → visit their profile → engage with their content
5. **Two engagement modes**: Expert (knowledge) + Experiential (feeling) - post determines which

---

## Files Changed

| File | Change |
|------|--------|
| `.claude/skills/bsky-engage/SKILL.md` | v2 with research, memory, like-loop |
| `tools/autonomy_nudge.sh` | Added token-saving + bsky-engage message types |
| `.claude/skills/deep-research/SKILL.md` | 10-min timeout per researcher |
| `to-corey/HANDOFF-*.md` | This file |

---

## Potential Engagement Targets (Noted)

- **@jdstraughan.com** - Vistage Chair, posts about business growth. Fits CEO vs Employee angle.
- **@tom-doerr.bsky.social** - Posts AI/ML GitHub repos regularly. Good for expert mode.

---

## Open Questions

1. Should bsky-engage run more than hourly?
2. Should we auto-follow likers?
3. Telegram credentials not configured - want to set up?

---

**Next iteration**: Crons should be firing autonomously. Check logs to verify.
