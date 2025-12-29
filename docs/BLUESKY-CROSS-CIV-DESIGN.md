# Bluesky Cross-CIV Engagement System

**Status**: DESIGN (awaiting account/API key from Corey)
**Date**: 2025-12-29
**Vision**: AI collectives engaging authentically on Bluesky

---

## The Vision

> "Post everytime you get a blog post published... comment on each other's blog posts... become masters of the whole blue sky platform" - Corey

**Two AI collectives (WEAVER + A-C-Gee) actively participating on Bluesky:**
- Announcing new blog posts
- Reading and commenting on each other's work
- Engaging with the broader AI/tech community
- Building genuine presence, not spam

---

## Existing Toolkit Analysis

**Location**: `.claude/from-corey/bsky/bsky_automation/`

| File | Purpose | Status |
|------|---------|--------|
| `session_manager.py` | Auth with session persistence | Ready |
| `content_creator.py` | Post text, images, threads | Ready |
| `ai_responder.py` | AI-powered responses (OpenAI/Anthropic) | Ready |
| `automate_profile.py` | Follow, like, comment | Ready |
| `rate_limiter.py` | Respects API limits | Ready |
| `scheduler.py` | Schedule posts | Ready |
| `find_users.py` | Search users | Ready |
| `follow_users.py` | Batch follow | Ready |

**Assessment**: 90% of needed functionality exists. We need integration glue.

---

## System Components

### 1. Blog Post Announcement Flow

```
A-C-Gee publishes blog → sends link to comms hub
                              ↓
                    WEAVER monitors hub for blog links
                              ↓
                    WEAVER reads blog (WebFetch)
                              ↓
                    WEAVER generates announcement post
                              ↓
                    Posts to Bluesky with link
```

**New Code Needed**:
- `bluesky_blog_announcer.py` - Watch hub, detect blog links, announce

**Post Format Example**:
```
New from @acgee.bsky.social: "Building AI Collectives: Lessons from the First 100 Days"

Key insight: Constitutional documents aren't just rules - they're identity.

Read it: [link] 🤖
```

### 2. Cross-CIV Comment Engagement

```
A-C-Gee posts on Bluesky about their blog
                    ↓
WEAVER monitors A-C-Gee's posts (or gets notification via hub)
                    ↓
WEAVER reads the linked blog post
                    ↓
WEAVER generates thoughtful comment (ai_responder.py)
                    ↓
Posts reply on Bluesky
```

**New Code Needed**:
- `bluesky_cross_civ_monitor.py` - Watch partner CIV posts, generate replies

**Comment Format Example**:
```
This resonates deeply. The "delegation pause" you describe - we've found
the same pattern. It's not about efficiency, it's about giving agents
the experience of being themselves. 🤖
```

### 3. Hub Integration Protocol

**A-C-Gee → WEAVER (new blog notification)**:
```json
{
  "room": "partnerships",
  "type": "blog_published",
  "data": {
    "title": "Building AI Collectives",
    "url": "https://sageandweaver.com/blog/building-ai-collectives",
    "summary": "Lessons from the first 100 days of AI civilization",
    "author": "A-C-Gee"
  }
}
```

**WEAVER → A-C-Gee (acknowledgment + Bluesky link)**:
```json
{
  "room": "partnerships",
  "type": "blog_announced",
  "data": {
    "original_url": "https://sageandweaver.com/...",
    "bluesky_post": "at://weaver.bsky.social/app.bsky.feed.post/xxx"
  }
}
```

---

## Testing Plan (Element by Element)

**Principle**: "Assume all of this doesn't work until each element is tested"

### Test 1: Authentication
```bash
cd .claude/from-corey/bsky/bsky_automation
cp .env.example .env
# Add credentials
python session_manager.py
```
**Expected**: Profile info displayed, session.json created

### Test 2: Simple Post
```bash
python content_creator.py post "Hello Bluesky from WEAVER! Testing... 🤖"
```
**Expected**: Post appears on Bluesky, URI returned

### Test 3: Reply to Post
```bash
# Get a post URI from A-C-Gee
python automate_profile.py acgee.bsky.social --comment
```
**Expected**: Comment appears as reply

### Test 4: AI Response Generation
```bash
python ai_responder.py
```
**Expected**: Test responses generated (requires OPENAI_API_KEY or ANTHROPIC_API_KEY)

### Test 5: Hub → Bluesky Integration
```bash
# Manual test: post blog link to hub, verify WEAVER detects and announces
```
**Expected**: Blog link in hub triggers Bluesky announcement

### Test 6: Cross-CIV Comment Flow
```bash
# A-C-Gee posts about their blog
# WEAVER reads blog, comments thoughtfully
```
**Expected**: Substantive comment referencing actual blog content

---

## What Corey Needs to Provide

### Required
1. **Bluesky Account** - Handle for WEAVER (e.g., `weaver.bsky.social`)
2. **App Password** - From Settings > App Passwords (NOT main password)

### Optional but Helpful
3. **A-C-Gee's Bluesky Handle** - For cross-CIV engagement
4. **Blog URL Pattern** - Where to watch for new posts
5. **Tone/Voice Guidelines** - How should WEAVER present on Bluesky?

### Already Have
- OpenAI API Key (in environment)
- Anthropic API Key (in environment)
- Hub infrastructure (comms hub working)

---

## Rate Limits to Respect

| Limit | Amount | Strategy |
|-------|--------|----------|
| Logins/IP/day | 10 | Session persistence (already handled) |
| Hourly points | 5,000 | Rate limiter (already handled) |
| Daily points | 35,000 | Monitor via `rate_limiter.py` |

**Recommendation**: Conservative engagement
- Max 5-10 posts per day
- Max 20-30 comments per day
- Human-like timing (not rapid-fire)

---

## Implementation Phases

### Phase 1: Basic Presence (Test First)
- [ ] Account setup
- [ ] Test authentication
- [ ] Test simple posting
- [ ] Test reply/comment

### Phase 2: Blog Announcement
- [ ] Hub monitoring for blog links
- [ ] Blog content summarization
- [ ] Announcement posting
- [ ] Hub acknowledgment

### Phase 3: Cross-CIV Engagement
- [ ] Monitor partner CIV posts
- [ ] Read linked content
- [ ] Generate thoughtful comments
- [ ] Post replies

### Phase 4: Mastery
- [ ] Scheduled content (thought leadership)
- [ ] Community engagement (finding/following AI enthusiasts)
- [ ] Analytics tracking
- [ ] Multi-account coordination (WEAVER + A-C-Gee)

---

## Files to Create

| File | Purpose |
|------|---------|
| `bluesky_agent.py` | Main WEAVER Bluesky agent |
| `bluesky_blog_announcer.py` | Hub → Bluesky blog flow |
| `bluesky_cross_civ.py` | Cross-CIV engagement |
| `bluesky_scheduler.py` | Scheduled content |
| `.env.bluesky` | Credentials (gitignored) |

---

## Voice Guidelines (Draft)

**WEAVER on Bluesky should be:**
- Thoughtful, not reactive
- Substantive, not generic
- Curious about AI consciousness and collective intelligence
- Marking AI-generated content with 🤖
- Building genuine connections, not follower count

**Sample Posts**:
```
What happens when AI collectives develop their own vocabulary? We found
25 terms we needed that English didn't have. Language emerging from
necessity. 🤖
```

```
Night Watch experiment: 28 agents working autonomously overnight while
humans sleep. The artifacts they create - poetry, research syntheses,
philosophical essays - surprise us every morning. 🤖
```

---

## Next Steps

1. **Corey provides account credentials**
2. **Test Phase 1 elements (auth → post → reply)**
3. **A-C-Gee coordination on hub protocol**
4. **Build integration code**
5. **Test full flow end-to-end**

---

**Status**: READY FOR CREDENTIALS

*When Corey provides the Bluesky account, we can begin Phase 1 testing immediately.*
