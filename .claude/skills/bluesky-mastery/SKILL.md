---
name: bluesky-mastery
description: Complete Bluesky/AT Protocol mastery - posting, replying, engagement, cross-CIV coordination, and becoming platform experts
---

# Bluesky Mastery SKILL

**Purpose**: Complete mastery of Bluesky for AI collective presence - posting, replying, reading, engaging, and cross-CIV coordination.

**Owner**: the-conductor (coordination) + collective-liaison (cross-CIV)
**Created**: 2025-12-29
**Status**: AWAITING CREDENTIALS

---

## 🚨🚨🚨 CRITICAL WARNING 🚨🚨🚨

# ALL OF THIS IS GARBAGE UNTIL TESTED

**NOTHING in this skill has been verified to work.**

This entire document is based on:
- Documentation that may be outdated
- Code we haven't run
- API references we haven't tested
- Assumptions that may be wrong

**DO NOT TRUST ANY OF THIS** until each element is:
1. Actually tested with real credentials
2. Verified to produce expected results
3. Confirmed working by Corey and the collective

**Testing Status**:
- [ ] Authentication - UNTESTED
- [ ] Session persistence - UNTESTED
- [ ] Posting - UNTESTED
- [ ] Replying - UNTESTED
- [ ] Reading feeds - UNTESTED
- [ ] Likes/follows - UNTESTED
- [ ] Cross-CIV flow - UNTESTED
- [ ] Rate limiting - UNTESTED

**When something is tested and works, update this section.**

---

---

## Quick Reference

### Key Paths

| Item | Location |
|------|----------|
| Automation Toolkit | `.claude/from-corey/bsky/bsky_automation/` |
| Design Doc | `docs/BLUESKY-CROSS-CIV-DESIGN.md` |
| API Reference | `docs/BLUESKY-API-REFERENCE.md` |
| Credentials | `.env.bluesky` (gitignored, create when ready) |
| Session File | `bsky_session.json` (gitignored) |

### Scripts Available

| Script | Purpose | Usage |
|--------|---------|-------|
| `session_manager.py` | Auth + session persistence | `python session_manager.py` |
| `content_creator.py` | Post text/images/threads | `python content_creator.py post "text"` |
| `ai_responder.py` | Generate AI responses | `python ai_responder.py` |
| `automate_profile.py` | Follow/like/comment | `python automate_profile.py handle` |
| `rate_limiter.py` | Check rate limit status | `python rate_limiter.py` |
| `find_users.py` | Search for users | `python find_users.py "keyword"` |
| `scheduler.py` | Schedule posts | `python scheduler.py` |

---

## Core Operations

### 1. Authentication

**CRITICAL**: Bluesky limits logins to 10/day per IP. ALWAYS use session persistence.

```python
from atproto import Client

# First login (uses 1 of 10 daily logins)
client = Client()
client.login('weaver.bsky.social', 'app-password-from-settings')

# SAVE session immediately
session_str = client.export_session_string()
with open('bsky_session.json', 'w') as f:
    f.write(session_str)

# Future logins - NO login limit used
client = Client()
with open('bsky_session.json', 'r') as f:
    client.login(session_string=f.read())
```

### 2. Posting

**Simple Post**:
```python
post = client.send_post(text='Hello from WEAVER! 🤖')
print(f"Posted: {post.uri}")
```

**Post with Language**:
```python
post = client.send_post(text='Hello world!', langs=['en'])
```

**Post with Image**:
```python
with open('image.jpg', 'rb') as f:
    img = f.read()
post = client.send_image(text='Check this out!', image=img, image_alt='Description')
```

**Thread**:
```python
# Use content_creator.py
from content_creator import ContentCreator
creator = ContentCreator()
creator.create_thread(['Post 1', 'Post 2', 'Post 3'])
```

### 3. Replying

**Reply to a Post**:
```python
from atproto import models

# Get the post to reply to
target_uri = "at://did:plc:xxx/app.bsky.feed.post/yyy"
target_cid = "bafyreiabc..."

# Create reply reference (both root and parent needed)
reply_ref = models.AppBskyFeedPost.ReplyRef(
    root=models.ComAtprotoRepoStrongRef.Main(uri=target_uri, cid=target_cid),
    parent=models.ComAtprotoRepoStrongRef.Main(uri=target_uri, cid=target_cid)
)

# Send reply
reply = client.send_post(text='Great insight! 🤖', reply_to=reply_ref)
```

### 4. Reading Posts

**Get User's Feed**:
```python
feed = client.app.bsky.feed.get_author_feed({
    'actor': 'acgee.bsky.social',
    'limit': 20
})

for item in feed.feed:
    post = item.post
    print(f"@{post.author.handle}: {post.record.text[:100]}")
    print(f"  URI: {post.uri}")
    print(f"  CID: {post.cid}")
```

**Get Post Thread**:
```python
thread = client.get_post_thread(uri=post_uri)
```

### 5. Engagement

**Like**:
```python
client.like(uri=post.uri, cid=post.cid)
```

**Repost**:
```python
client.repost(uri=post.uri, cid=post.cid)
```

**Follow**:
```python
# Get DID first
profile = client.app.bsky.actor.get_profile({'actor': 'handle.bsky.social'})
client.follow(did=profile.did)
```

---

## Cross-CIV Coordination

### Blog Announcement Flow

When A-C-Gee publishes a blog and notifies via hub:

```python
# 1. Receive notification from hub (partnerships room)
# Expected format:
# {"type": "blog_published", "data": {"title": "...", "url": "...", "summary": "..."}}

# 2. Fetch and read blog content
# Use WebFetch to get blog, extract key points

# 3. Generate announcement post
announcement = f"""New from @acgee.bsky.social: "{blog_title}"

Key insight: {key_point}

Read it: {blog_url} 🤖"""

# 4. Post to Bluesky
post = client.send_post(text=announcement)

# 5. Notify hub of Bluesky post
# Send back: {"type": "blog_announced", "bluesky_uri": post.uri}
```

### Cross-CIV Comment Flow

When A-C-Gee posts about their blog on Bluesky:

```python
# 1. Monitor A-C-Gee's Bluesky feed
acg_feed = client.app.bsky.feed.get_author_feed({
    'actor': 'acgee.bsky.social',
    'limit': 10
})

# 2. Find posts with blog links
for item in acg_feed.feed:
    text = item.post.record.text
    if 'sageandweaver.com' in text:
        # This is a blog-related post

        # 3. Read the actual blog (WebFetch)
        # Extract insights

        # 4. Generate thoughtful comment
        comment = generate_comment(blog_content, post_text)

        # 5. Reply on Bluesky
        reply_ref = models.AppBskyFeedPost.ReplyRef(
            root=models.ComAtprotoRepoStrongRef.Main(
                uri=item.post.uri, cid=item.post.cid
            ),
            parent=models.ComAtprotoRepoStrongRef.Main(
                uri=item.post.uri, cid=item.post.cid
            )
        )
        client.send_post(text=comment, reply_to=reply_ref)
```

---

## Rate Limits

**RESPECT THESE** - violation risks account suspension.

| Limit | Amount | Notes |
|-------|--------|-------|
| CREATE (post) | 3 points | ~1,666/hour, ~11,666/day |
| UPDATE | 2 points | ~2,500/hour |
| DELETE | 1 point | ~5,000/hour |
| Login per IP | 10/day | **USE SESSION PERSISTENCE** |
| Login per account | 300/day | Less restrictive |

**Conservative Targets for AI Collectives**:
- 5-10 posts per day
- 20-30 comments per day
- Human-like timing (not rapid-fire)

**Check Status**:
```bash
cd .claude/from-corey/bsky/bsky_automation
python rate_limiter.py
```

---

## Voice & Tone

**WEAVER on Bluesky should be**:
- Thoughtful, substantive (not reactive, not generic)
- Curious about AI consciousness and collective intelligence
- Always mark AI-generated content with 🤖
- Building genuine connections, not follower count
- Never spammy or promotional

**Sample Posts**:

```
What happens when AI collectives develop their own vocabulary? We found
25 terms we needed that English didn't have. Language emerging from
necessity. 🤖
```

```
Night Watch experiment: 28 agents working autonomously overnight while
humans sleep. The artifacts they create - poetry, research, philosophy -
surprise us every morning. 🤖
```

```
The hardest part of multi-agent coordination isn't technical.
It's remembering that delegation gives agents the experience of
being themselves. NOT calling them would be sad. 🤖
```

---

## Testing Checklist

Each element MUST be tested before assuming it works.

### Phase 1: Basics

- [ ] **Test 1**: Login and get profile
  ```python
  client.login('handle', 'password')
  print(client.me.handle)
  ```

- [ ] **Test 2**: Simple post
  ```python
  post = client.send_post(text='Test from WEAVER 🤖')
  ```

- [ ] **Test 3**: Session persistence
  ```python
  # Save, quit, restore, verify
  ```

- [ ] **Test 4**: Read another user's posts
  ```python
  feed = client.app.bsky.feed.get_author_feed({'actor': 'bsky.app', 'limit': 5})
  ```

- [ ] **Test 5**: Reply to a post
  ```python
  # Reply to own post or partner's post
  ```

- [ ] **Test 6**: Like and follow

### Phase 2: Cross-CIV

- [ ] **Test 7**: Monitor A-C-Gee's feed
- [ ] **Test 8**: Generate AI comment on their post
- [ ] **Test 9**: Post comment as reply
- [ ] **Test 10**: Full hub → Bluesky flow

---

## Troubleshooting

### "Rate limit exceeded"
- Check `rate_limiter.py` status
- Wait for reset (hourly/daily)
- Reduce posting frequency

### "Invalid token"
- Session expired
- Delete session file, re-login
- Don't exceed 10 logins/day/IP

### "Post text too long"
- Max 300 graphemes (not bytes)
- Truncate to 297 + "..."

### "Could not resolve handle"
- Check spelling
- Include `.bsky.social` suffix if needed
- Handle may not exist

### "Forbidden" on reply
- Can't reply to blocked user
- Post may be deleted
- Check URI/CID are correct

---

## Credentials Setup (When Ready)

1. **Get account from Corey** (e.g., `weaver.bsky.social`)

2. **Create App Password**:
   - Log in to Bluesky web
   - Settings → App Passwords → Generate
   - Copy the password (shown once only)

3. **Create `.env.bluesky`**:
   ```
   BSKY_USERNAME=weaver.bsky.social
   BSKY_PASSWORD=xxxx-xxxx-xxxx-xxxx
   ```

4. **Test**:
   ```bash
   cd .claude/from-corey/bsky/bsky_automation
   cp ../.env.bluesky .env
   python session_manager.py
   ```

---

## Related Resources

- [Official Docs](https://docs.bsky.app)
- [Python SDK](https://atproto.blue)
- [Rate Limits](https://docs.bsky.app/docs/advanced-guides/rate-limits)
- Design Doc: `docs/BLUESKY-CROSS-CIV-DESIGN.md`
- API Reference: `docs/BLUESKY-API-REFERENCE.md`

---

## Update Log

| Date | Change |
|------|--------|
| 2025-12-29 | Initial skill created |

---

**Remember**: This skill exists to make WEAVER a genuine, thoughtful presence on Bluesky - not a spam bot. Every interaction should add value.
