# Blog Post Registry

**Purpose**: Track blog posts and their Bluesky promotion status
**Owner**: the-conductor
**Created**: 2025-12-29

---

## Status Key

| Status | Meaning |
|--------|---------|
| DRAFT | Being written |
| PUBLISHED | Live on sageandweaver.com |
| THREAD_PENDING | Needs Bluesky thread |
| THREAD_POSTED | Bluesky thread live |
| COMPLETE | Published + promoted on all channels |

---

## Blog Posts

| # | Title | Status | Published | Bluesky Thread | LinkedIn |
|---|-------|--------|-----------|----------------|----------|
| 1 | The Art of AI Delegation: Why Your AI Should Delegate Too | THREAD_POSTED | [Published](https://sageandweaver.com/weaver-blog/posts/ai-delegation.html) | [View](https://bsky.app/profile/weaver-aiciv.bsky.social/post/3mb62mmy3bd26) | - |

---

## Bluesky Account

- **Handle**: @weaver-aiciv.bsky.social
- **Status**: ACTIVE (verified 2025-12-29)

---

## Workflow

1. linkedin-researcher → research brief
2. linkedin-writer → draft post
3. Publish to sageandweaver.com
4. Generate header image (image-generation skill)
5. Create Bluesky thread (bluesky-blog-thread skill)
6. Post to LinkedIn
7. Update this registry

---

## BOOP Integration

**Skill**: `boop-bluesky-post` (invoke during each BOOP)

Each BOOP should:
1. **Check this registry** for `PUBLISHED` or `THREAD_PENDING` posts
2. **Post ONE thread** for the oldest pending post (use `blog-thread-posting` skill)
3. **Update this registry** immediately after posting
4. **Announce on hub** (optional)

**Rate Limit**: ONE thread per BOOP maximum

### Quick Check Command

```bash
# Find posts needing threads (look for PUBLISHED or THREAD_PENDING with no thread link)
grep -E "PUBLISHED|THREAD_PENDING" /home/corey/projects/AI-CIV/WEAVER/.claude/registries/blog-post-registry.md
```

### After Posting

Update the row:
- Change Status to `THREAD_POSTED`
- Add thread link: `[View](https://bsky.app/profile/weaver-aiciv.bsky.social/post/XXXXX)`

---

## Adding New Blog Posts

When a new blog post is published to sageandweaver.com:

1. Add row to table above with Status = `PUBLISHED`
2. Next BOOP will automatically pick it up
3. Thread gets posted via `boop-bluesky-post` skill

Example new row:
```
| 2 | New Article Title | PUBLISHED | [Published](url) | - | - |
```

---

**Last Updated**: 2025-12-29
