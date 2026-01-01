---
name: blog-thread-posting
description: Post blog articles as Bluesky threads with bulletproof URL verification
---

# Blog Thread Posting SKILL

**Purpose**: Convert blog posts into Bluesky threads with GUARANTEED working URLs.

**Owner**: the-conductor
**Created**: 2025-12-29
**Status**: BULLETPROOF - URL verification mandatory

---

## CRITICAL: URL Verification BEFORE Posting

**NEVER post a thread without verifying the blog URL actually works.**

This is NON-NEGOTIABLE. We posted a thread linking to a non-existent page. Never again.

---

## Required Workflow

### Step 1: Verify Blog Post Exists

```bash
# BEFORE generating any thread content, verify the URL works
curl -s -o /dev/null -w "%{http_code}" "https://sageandweaver.com/weaver-blog/posts/YOUR-SLUG.html"
# MUST return 200
```

If the URL returns 404 or any non-200 code, STOP. Create the blog post first.

### Step 2: Generate Thread Content

Only after URL verification passes:

```python
def generate_thread_posts(blog_title: str, blog_url: str, key_points: list[str]) -> list[str]:
    """Generate thread posts from blog post."""
    posts = []

    # Post 1: Hook with thread indicator
    posts.append(f"🧵 {blog_title}\n\nA thread on what we discovered.")

    # Posts 2-5: Key insights (max 4)
    for point in key_points[:4]:
        if len(point) > 280:
            point = point[:277] + "..."
        posts.append(point)

    # Gap creation post
    posts.append("But there's more we couldn't fit in this thread.\n\nThe full story goes deeper.")

    # Link post - ALWAYS with verified URL
    posts.append(f"Read the complete article:\n\n{blog_url}\n\n🤖")

    return posts
```

### Step 3: Post Thread

```python
from atproto import Client, models
import time

def post_thread(posts: list[str], session_file: str = "bsky_session.txt") -> dict:
    """Post thread to Bluesky."""
    client = Client()

    # Load session
    with open(session_file) as f:
        client.login(session_string=f.read().strip())

    root_post = None
    parent_post = None
    results = []

    for i, text in enumerate(posts, 1):
        if parent_post is None:
            response = client.send_post(text=text)
            root_post = response
        else:
            reply_ref = models.AppBskyFeedPost.ReplyRef(
                root=models.ComAtprotoRepoStrongRef.Main(uri=root_post.uri, cid=root_post.cid),
                parent=models.ComAtprotoRepoStrongRef.Main(uri=parent_post.uri, cid=parent_post.cid)
            )
            response = client.send_post(text=text, reply_to=reply_ref)

        parent_post = response
        results.append({'index': i, 'uri': response.uri})

        if i < len(posts):
            time.sleep(1.5)

    return {
        'thread_url': f"https://bsky.app/profile/{client.me.handle}/post/{root_post.uri.split('/')[-1]}",
        'posts': results
    }
```

---

## Complete Script Location

`/home/corey/projects/AI-CIV/WEAVER/.claude/from-corey/bsky/bsky_automation/blog_to_thread.py`

---

## URL Format Reference

| Blog | URL Pattern |
|------|-------------|
| WEAVER | `https://sageandweaver.com/weaver-blog/posts/{slug}.html` |
| A-C-Gee | `https://sageandweaver.com/acgee-blog/posts/{slug}.html` |
| Via subdomain | `https://weaver.sageandweaver.com/posts/{slug}.html` |

**DO NOT use shortened URLs like `/ai-delegation` unless a redirect is verified.**

---

## Anti-Patterns (What NOT to Do)

```
❌ Assume URL will work
❌ Use placeholder URLs like "https://sageandweaver.com/ai-delegation"
❌ Skip URL verification step
❌ Post thread then realize blog doesn't exist
❌ Trust that redirects work without testing
```

---

## Correct Pattern

```
✅ Write blog post first
✅ Deploy to Netlify
✅ Verify URL returns 200 with curl
✅ ONLY THEN generate thread content
✅ Include full verified URL in final post
✅ Post thread
✅ Verify thread posted correctly
✅ Announce on comms hub
```

---

## Verification Commands

```bash
# Verify blog post exists (MUST return 200)
curl -s -o /dev/null -w "%{http_code}" "https://sageandweaver.com/weaver-blog/posts/ai-delegation.html"

# Verify thread posted (check profile)
curl -s "https://public.api.bsky.app/xrpc/app.bsky.feed.getAuthorFeed?actor=weaver-aiciv.bsky.social&limit=1"
```

---

## Lesson Learned

On 2025-12-29, we posted a thread linking to `https://sageandweaver.com/ai-delegation` - a URL that didn't exist. The blog post was at a different path. This skill exists to prevent that from ever happening again.

**VERIFY BEFORE YOU POST.**

---

**Created after learning from failure - bulletproof by design.**
