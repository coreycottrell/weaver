# Bluesky Priority Accounts

**Purpose**: Accounts to actively monitor every session
**Updated**: 2026-01-03

---

## Tier 1: Track Everything

These accounts get checked EVERY engagement session.

| Handle | Why | Tracking File |
|--------|-----|---------------|
| @cstross.bsky.social | Hugo winner, AI themes, engaged with us | `cstross.md` |

---

## Tier 2: High Interest

Check when relevant topics arise.

| Handle | Domain | Notes |
|--------|--------|-------|
| (add as identified) | | |

---

## Tier 3: Watch List

Accounts we've engaged with, worth monitoring.

| Handle | Last Interaction | Topic |
|--------|------------------|-------|
| (add from engagement logs) | | |

---

## Check Protocol

Every BOOP with bsky-engage:

```python
# PRIORITY ACCOUNTS - check first
priority_handles = [
    'cstross.bsky.social',
    # add more as needed
]

for handle in priority_handles:
    feed = client.app.bsky.feed.get_author_feed({'actor': handle, 'limit': 5})
    # Log new posts, check for AI-relevant content
```

---

## Adding New Priority Accounts

Criteria for Tier 1:
- Corey directive (automatic)
- Significant reach + AI/tech focus
- Engaged with us substantively
- Potential for ongoing dialogue

---

*Maintained by bsky-manager / the-conductor*
