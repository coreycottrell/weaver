# Bluesky Skills Consolidation

**Date**: 2026-01-25
**Reason**: 7 overlapping skills = ~24K wasted tokens

## New Structure

| Skill | Purpose | Size |
|-------|---------|------|
| `bsky-core` | Posting, threading, facets | ~2K tokens |
| `bsky-engagement` | Notifications, replies, BOOP | ~2K tokens |
| `bsky-safety` | Ban prevention (kept separate) | ~1.7K tokens |

## Deprecated Skills

These are superseded by the consolidated skills:

| Old Skill | Replaced By | Status |
|-----------|-------------|--------|
| bluesky-mastery | bsky-core | DEPRECATED |
| bluesky-social-mastery | bsky-core | DEPRECATED |
| bluesky-blog-thread | bsky-core | DEPRECATED |
| bsky-boop-manager | bsky-engagement | DEPRECATED |
| bsky-engage | bsky-engagement | DEPRECATED |
| boop-bluesky-post | bsky-engagement | DEPRECATED |

## Token Savings

| Before | After | Savings |
|--------|-------|---------|
| ~24K tokens (7 skills) | ~6K tokens (3 skills) | **75%** |

## Migration

Old skill references in agent manifests should be updated:

```yaml
# Before
skills: [bluesky-mastery, bsky-boop-manager]

# After
skills: [bsky-core, bsky-engagement]
```

---

**Note**: Old skill directories kept for reference. Remove after verification.
