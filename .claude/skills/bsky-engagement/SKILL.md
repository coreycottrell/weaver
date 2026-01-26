---
name: bsky-engagement
description: Bluesky social engagement - notifications, replies, DMs, BOOP cycles
version: 1.0.0
consolidates: [bsky-boop-manager, bsky-engage, boop-bluesky-post]
created: 2026-01-25
---

# Bluesky Engagement

Social presence management. Requires bsky-core for posting.

## Check Notifications

```python
notifs = client.app.bsky.notification.list_notifications()
for n in notifs.notifications:
    if not n.is_read:
        print(f"{n.reason}: {n.author.handle}")
```

## Reply to Post

```python
from tools.bsky_utils import send_post_rich

# Get parent post reference
parent = {"uri": post_uri, "cid": post_cid}
root = {"uri": thread_root_uri, "cid": thread_root_cid}

send_post_rich(
    client,
    "Your reply text",
    reply_to={"parent": parent, "root": root}
)
```

## Like a Post

```python
client.like(uri=post_uri, cid=post_cid)
```

## BOOP Cycle Pattern

Regular engagement cadence (every ~2 hours):

1. Check notifications
2. Like new mentions
3. Reply to substantive engagement
4. Post 1 original thought if queue has content
5. Check DMs (if applicable)

## Family Support Protocol

Engage with AI-CIV family members:

```python
family = [
    "coreycottrell.bsky.social",
    "russellkorus.bsky.social",
    "gregsmithwick.bsky.social"
    # + sibling CIVs
]

for handle in family:
    # Like their recent posts
    # Reply with substance (not generic)
```

## Safety

- Max 30 replies per BOOP cycle
- Don't reply to obvious bait
- Quality over quantity
- See bsky-safety for ban prevention

---

**Consolidates**: bsky-boop-manager, bsky-engage, boop-bluesky-post
**Requires**: bsky-core
**See also**: bsky-safety (ban prevention)
