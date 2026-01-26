---
name: bsky-core
description: Core Bluesky operations - posting, threading, facets. Foundation for all Bluesky activity.
version: 1.0.0
consolidates: [bluesky-mastery, bluesky-social-mastery, bluesky-blog-thread]
created: 2026-01-25
---

# Bluesky Core Operations

Essential Bluesky functionality. Other bsky-* skills build on this.

## Critical: Facets Protocol

**EVERY post with URLs or mentions MUST use facets.**

```python
from tools.bsky_utils import send_post_rich, send_thread_rich

# CORRECT - links are clickable
send_post_rich(client, "Check out https://example.com")

# WRONG - links are NOT clickable
client.send_post("Check out https://example.com")
```

## Authentication

```python
from atproto import Client
from dotenv import load_dotenv
import os

load_dotenv('/path/to/.env')
client = Client()
client.login(os.getenv('BSKY_USERNAME'), os.getenv('BSKY_PASSWORD'))
```

## Single Post

```python
from tools.bsky_utils import send_post_rich

send_post_rich(client, "Your post text here")
```

## Thread

```python
from tools.bsky_utils import send_thread_rich

posts = [
    "First post in thread",
    "Second post continues the thought",
    "Final post with conclusion"
]
send_thread_rich(client, posts)
```

## Blog Thread Pattern

Hook → Value → Link format:

```python
posts = [
    "Hook that creates curiosity [1/4]",
    "Key insight from the blog [2/4]",
    "Another valuable point [3/4]",
    "Full post: https://blog.url/post [4/4]"
]
send_thread_rich(client, posts)
```

## Rate Limits

- Max 1,666 posts/day (5,000/3 days)
- Wait 2+ seconds between posts in threads
- Use `time.sleep(2)` between operations

---

**Consolidates**: bluesky-mastery, bluesky-social-mastery, bluesky-blog-thread
**See also**: bsky-engagement (notifications, replies, BOOP cycles)
