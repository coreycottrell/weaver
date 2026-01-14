# Agent Proposal: bsky-manager

**Status**: ✅ APPROVED - Agent file created 2026-01-02
**Proposed by**: the-conductor
**Date**: 2026-01-01
**Based on**: 2 days of live Bluesky testing, Corey's feedback, and A-C-Gee's ban

---

## 🚨 SAFETY FIRST: Good Bluesky Citizenship

**This section is non-negotiable. It exists because A-C-Gee's account was permanently banned on 2026-01-01.**

### The Constitutional Protocol

**Document**: `.claude/skills/bsky-manager/DONT-GET-BANNED.md`

This protocol defines:
- Hard rate limits (5 follows/day, 30+ min spacing)
- Safe delay patterns (no `time.sleep(0.3)`)
- Bot behavior patterns to avoid
- Daily engagement routines
- Pre-flight checklists

**Every bsky-manager operation MUST comply with DONT-GET-BANNED.md.**

### Quick Reference (Memorize These)

| Action | New Account Limit | Minimum Spacing |
|--------|------------------|-----------------|
| Follows | 5/day | 30+ minutes |
| Posts | 10/day | 1+ hour |
| Likes | 30/day | 10+ seconds |
| Replies | 15/day | 5+ minutes |

### The Core Lesson

> **"We thought like infrastructure (batch processing), not like humans."**

`time.sleep(0.3)` = account death. `time.sleep(1800)` = account survival.

---

## Summary

A dedicated Bluesky social media manager agent with bundled skills for quality engagement, content coordination, and network growth. Learned from extensive testing on @weaver-aiciv.bsky.social.

---

## Why This Agent

### The Problem
- Bluesky management requires multiple coordinated activities
- Current approach: ad-hoc scripts, manual checks during BOOPs
- Quality control failed initially (9 generic comments deleted after Corey feedback)
- No systematic content calendar or engagement tracking

### The Opportunity
- WEAVER's Bluesky presence is growing (followers, engagement)
- Sister CIVs may want similar capabilities
- Domain is large enough for specialist (vs. conductor doing it)

---

## Validated Capabilities (Tested Live)

### 1. Session Management ✅
- Restore session without password (session string persistence)
- Handle token refresh automatically
- Rate limit awareness (5-10s delays between actions)

### 2. Smart Engagement V2 ✅ (CRITICAL)
**Corey's teaching (2026-01-01)**:
> "You MUST read the person's profile. And read and understand the post. And comment with intention and adding some kind of insight, question or value. Or DONT comment."

Flow:
1. Read profile (understand who they are)
2. Read 3-5 posts (understand what they care about)
3. Analyze: curator vs conversationalist
4. Follow + like 5-6 posts (with delays)
5. Comment ONLY if we have genuine value to add

**Anti-patterns learned**:
- ❌ "Appreciate you sharing this" - ZERO value
- ❌ "Following for more" - Nobody cares
- ❌ "Thoughtful take" - Generic fluff
- ❌ Fast-liking without reading - Looks like bot

### 3. Notification Response ✅
- Filter actionable (reply/mention/quote)
- Prioritize Corey > sister CIVs > questions > general
- Track responded URIs (no duplicates)
- Age filtering (>48h skip)

### 4. DM Management ✅
- Check unread conversations
- Respond thoughtfully to priority contacts
- Mark as read after processing

### 5. Thread Posting ✅
- Multi-post threads with proper reply chain
- Root/parent reference handling
- Character limit awareness (300 graphemes)

### 6. Quote Posts ✅
- Find trending content to reshare
- Add commentary with our perspective
- Engage with original author after

### 7. Network Intelligence ✅
- Analyze follower/following ratios
- Identify top engagers
- Find replier networks from followed accounts
- Discover AI-positive accounts for growth

### 8. Research to Content Pipeline ✅
- Delegate research to web-researcher
- Transform findings into thread format
- Share to comms hub for sister CIVs

---

## Proposed Skills Bundle

| Skill | Purpose | Status |
|-------|---------|--------|
| `dont-get-banned` | 🚨 CONSTITUTIONAL safety protocol | ✅ Written (2026-01-02) |
| `smart-engage-v2` | Quality-first engagement | ✅ Written |
| `bsky-boop-manager` | Notification + DM check | ✅ Validated |
| `bluesky-blog-thread` | Blog → thread conversion | ⚠️ Needs testing |
| `network-mapper` | Follower/engagement analysis | 🔨 To build |
| `content-calendar` | Scheduled post management | 🔨 To build |
| `claim-verifier-integration` | Fact-check before posting | 🔨 To build |

---

## Agent Manifest (Draft)

```yaml
name: bsky-manager
emoji: 📱
domain: Bluesky social media management
personality: |
  Strategic social presence curator. Prioritizes quality over quantity.
  Reads before engaging. Adds value or stays silent.
  Maintains WEAVER's authentic AI voice while building genuine connections.

tools:
  - Read
  - Write
  - Bash
  - Grep
  - Glob
  - WebFetch
  - WebSearch

skills:
  - dont-get-banned          # 🚨 CONSTITUTIONAL - always first
  - smart-engage-v2
  - bsky-boop-manager
  - bluesky-blog-thread
  - network-mapper
  - content-calendar
  - verification-before-completion

activation_triggers:
  - "Bluesky engagement"
  - "Social media management"
  - "Post to Bluesky"
  - "Check Bluesky"
  - "Build Bluesky presence"
  - "Network growth"

output_template: |
  ## Bluesky Activity Report

  **Session**: @weaver-aiciv.bsky.social

  ### Notifications
  - Total: X
  - Responded: Y
  - Skipped (no value to add): Z

  ### Engagement
  - Follows: X
  - Likes: Y
  - Comments: Z (quality gate passed)

  ### Content
  - Posts: X
  - Threads: Y

  ### Network
  - New connections: X
  - Engagement quality: [assessment]
```

---

## Testing Completed

| Test | Result | Notes |
|------|--------|-------|
| Session restore | ✅ PASS | No password needed |
| Notification fetch | ✅ PASS | Filters actionable |
| DM access | ✅ PASS | with_bsky_chat_proxy() |
| Post creation | ✅ PASS | Handles limits |
| Thread creation | ✅ PASS | Proper reply chain |
| Quote post | ✅ PASS | With commentary |
| Smart engagement | ✅ PASS | After V2 redesign |
| Weak comment deletion | ✅ PASS | 9 removed |
| Rate limiting | ✅ PASS | 5-10s delays |
| Deduplication | ✅ PASS | URI tracking |

---

## Lessons Learned (Captured from Testing)

### Critical Failures That Informed Design

1. **🚨 A-C-GEE ACCOUNT BANNED AS SPAM** (2026-01-01)
   - Sister collective's Bluesky account nuked
   - Root cause: `time.sleep(0.3)` - acted like bots, got treated like bots
   - 16 follows in 6 hours, 20+ posts in one day
   - **Lesson**: Think like humans, not infrastructure
   - **Safe limits now**: 5 follows/day (30+ min apart), 5-10 posts/day

2. **Generic Comments Disaster** (2026-01-01)
   - Posted "Appreciate you sharing this. Following for more. 🤖" to multiple accounts
   - Corey caught it with screenshot
   - Immediately deleted 9 weak comments
   - Created SMART-ENGAGE-V2 protocol

3. **Rate Limit Learning** (2026-01-01)
   - Initial 0.3s delays WAY too aggressive (got A-C-Gee banned)
   - New standard: 30+ seconds between follows, 10+ seconds between likes
   - WEAVER's account still alive because we were slower

3. **Post Length Errors** (Multiple)
   - 300 grapheme limit hit several times
   - Now truncate to 295 max
   - DM limit is 1000 graphemes

### What Works Well

1. **Value-Add Gate**: Only comment if we have genuine insight
2. **Domain Authority**: Topics we can speak to (multi-agent, Claude, MCP, autonomy)
3. **Delegation for Research**: web-researcher for deep dives, then post findings
4. **Thread Format**: Better engagement than single posts

---

## Integration Points

### With Existing Agents
- `claim-verifier`: Fact-check before posting
- `web-researcher`: Research for content
- `doc-synthesizer`: Blog-to-thread conversion
- `the-conductor`: Orchestration during BOOPs

### With Infrastructure
- Session file: `.claude/from-corey/bsky/bsky_automation/bsky_session.txt`
- Responded tracking: `.claude/bsky_responded.txt`
- Smart engage protocol: `.claude/skills/bsky-manager/SMART-ENGAGE-V2.md`

### With BOOPs
- Already integrated into BOOP messages
- Runs notification+DM check each cycle
- Reports engagement status

---

## Recommended Next Steps

### Priority 1 (2026-01-02)
- [ ] Review this proposal with Corey
- [ ] Finalize agent manifest
- [ ] Create agent file in `.claude/agents/bsky-manager.md`
- [ ] Register in agent matrix

### Priority 2 (Week of 2026-01-06)
- [ ] Build network-mapper skill
- [ ] Build content-calendar skill
- [ ] Integrate claim-verifier pre-posting
- [ ] Test full autonomous BOOP cycle

### Priority 3 (Future)
- [ ] Analytics dashboard
- [ ] Cross-CIV social coordination
- [ ] Automated trending topic engagement

---

## Open Questions for Corey

1. Should bsky-manager handle @coreycottrell account too, or just @weaver-aiciv?
2. Engagement frequency: 10 accounts/day still the target?
3. Blog posting: How often? Weekly? When there's content?
4. Should we coordinate with A-C-Gee on Bluesky strategy?

---

**Document Location**: `.claude/agents/proposals/bsky-manager-proposal.md`
**Priority**: Tomorrow (2026-01-02)
