# Bluesky API Reference (2025)

**Fetched**: 2025-12-29
**Purpose**: Test each function call ourselves

---

## Installation

```bash
pip install atproto
```

---

## Authentication

### Create Session

```python
from atproto import Client

client = Client()
client.login('handle.bsky.social', 'your-app-password')

# Session is now active
# Access tokens managed automatically
```

### Session Persistence (CRITICAL - 10 logins/day limit!)

```python
# Export session
session_string = client.export_session_string()

# Later - restore session
from atproto import Client
client = Client()
client.login(session_string=session_string)
```

---

## Posting

### Basic Text Post

```python
# Simple post
post = client.send_post(text='Hello Bluesky!')

# Returns: PostRef with uri and cid
print(f"Posted: {post.uri}")
```

### Post with Language

```python
post = client.send_post(
    text='Hello world!',
    langs=['en']  # ISO language codes
)
```

### Post with Image

```python
# Read image file
with open('image.jpg', 'rb') as f:
    img_data = f.read()

post = client.send_image(
    text='Check this out!',
    image=img_data,
    image_alt='Description for accessibility'
)
```

---

## Replying

### Reply to a Post

```python
from atproto import models

# Get the post you want to reply to
# You need: uri, cid, root_uri, root_cid

# Create reply reference
reply_ref = models.AppBskyFeedPost.ReplyRef(
    root=models.ComAtprotoRepoStrongRef.Main(
        uri=root_uri,  # Original thread starter
        cid=root_cid
    ),
    parent=models.ComAtprotoRepoStrongRef.Main(
        uri=parent_uri,  # Post you're directly replying to
        cid=parent_cid
    )
)

# Send reply
reply = client.send_post(
    text='Great point! Here\'s my thoughts...',
    reply_to=reply_ref
)
```

---

## Reading Posts

### Get Author's Feed

```python
# Get posts from a specific user
feed = client.app.bsky.feed.get_author_feed({
    'actor': 'handle.bsky.social',
    'limit': 50
})

for post in feed.feed:
    print(f"{post.post.author.handle}: {post.post.record.text}")
```

### Get Post Thread

```python
# Get a post and its replies
thread = client.get_post_thread(uri='at://did:plc:.../app.bsky.feed.post/...')
```

### Resolve Handle to DID

```python
# Get user info
profile = client.app.bsky.actor.get_profile({'actor': 'handle.bsky.social'})
print(f"DID: {profile.did}")
print(f"Followers: {profile.followers_count}")
```

---

## Interactions

### Like a Post

```python
client.like(uri=post.uri, cid=post.cid)
```

### Repost

```python
client.repost(uri=post.uri, cid=post.cid)
```

### Follow User

```python
client.follow(did='did:plc:...')
```

---

## Rate Limits

| Operation | Points | Hourly Limit | Daily Limit |
|-----------|--------|--------------|-------------|
| CREATE (post) | 3 | ~1,666 | ~11,666 |
| UPDATE | 2 | ~2,500 | ~17,500 |
| DELETE | 1 | ~5,000 | ~35,000 |

**Session Creation Limits**:
- 30 per 5 minutes (per account)
- 300 per day (per account)
- **10 per day per IP** (use session persistence!)

---

## Testing Checklist

### Test 1: Authentication
```python
from atproto import Client
client = Client()
client.login('handle', 'app-password')
profile = client.me
print(f"Logged in as: {profile.handle} ({profile.did})")
```
**Expected**: Handle and DID printed

### Test 2: Simple Post
```python
post = client.send_post(text='Test post from WEAVER 🤖')
print(f"Post URI: {post.uri}")
```
**Expected**: URI returned, post visible on Bluesky

### Test 3: Get Someone's Posts
```python
feed = client.app.bsky.feed.get_author_feed({
    'actor': 'bsky.app',  # Official Bluesky account
    'limit': 5
})
for item in feed.feed:
    print(f"- {item.post.record.text[:50]}...")
```
**Expected**: 5 posts printed

### Test 4: Reply to Post
```python
# First get a post to reply to
feed = client.app.bsky.feed.get_author_feed({
    'actor': 'YOUR_OTHER_ACCOUNT',
    'limit': 1
})
post = feed.feed[0].post

# Reply to it
from atproto import models
reply_ref = models.AppBskyFeedPost.ReplyRef(
    root=models.ComAtprotoRepoStrongRef.Main(uri=post.uri, cid=post.cid),
    parent=models.ComAtprotoRepoStrongRef.Main(uri=post.uri, cid=post.cid)
)
reply = client.send_post(text='Test reply! 🤖', reply_to=reply_ref)
print(f"Reply URI: {reply.uri}")
```
**Expected**: Reply appears under original post

### Test 5: Like a Post
```python
client.like(uri=post.uri, cid=post.cid)
```
**Expected**: Post shows like from your account

### Test 6: Session Persistence
```python
# Save session
session_str = client.export_session_string()
with open('session.txt', 'w') as f:
    f.write(session_str)

# New client, restore session
client2 = Client()
with open('session.txt', 'r') as f:
    client2.login(session_string=f.read())

profile = client2.me
print(f"Restored session: {profile.handle}")
```
**Expected**: Login without credentials

---

## Common Errors

### "Rate limit exceeded"
- Wait for reset (check headers)
- Use session persistence to avoid login limits

### "Invalid token"
- Session expired, need to re-login
- Use refresh token flow

### "Post text too long"
- Max 300 characters (graphemes, not bytes)
- Truncate to 297 + "..."

### "Invalid handle"
- Handle doesn't exist
- Check spelling, include `.bsky.social` if needed

---

## Resources

- [Official Docs](https://docs.bsky.app)
- [Python SDK](https://atproto.blue/en/latest/)
- [Rate Limits](https://docs.bsky.app/docs/advanced-guides/rate-limits)
- [API Reference](https://docs.bsky.app/docs/category/http-reference)
