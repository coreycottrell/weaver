"""
Bluesky Utilities - Rich text posting with clickable links AND mentions

Fixes the facets tech debt: makes URLs and @mentions clickable.
"""

import re
from atproto import Client, client_utils, models
from pathlib import Path
from functools import lru_cache

# Session file location
SESSION_FILE = Path('${CIV_ROOT}/.claude/from-${HUMAN_NAME_LOWER}/bsky/bsky_automation/bsky_session.txt')

# URL pattern for detecting links in text
URL_PATTERN = re.compile(
    r'https?://(?:[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?\.)+[a-zA-Z]{2,}'
    r'(?:/[^\s\)\]]*)?'
)

# Mention pattern - matches @handle.domain format
MENTION_PATTERN = re.compile(r'@([a-zA-Z0-9][a-zA-Z0-9._-]*\.[a-zA-Z0-9._-]+)')

# Cache for handle -> DID resolution
_did_cache = {}


def get_client() -> Client:
    """Get authenticated Bluesky client using session file."""
    client = Client()
    with open(SESSION_FILE, 'r') as f:
        client.login(session_string=f.read().strip())
    return client


def resolve_handle_to_did(client: Client, handle: str) -> str | None:
    """Resolve a Bluesky handle to its DID. Uses cache."""
    if handle in _did_cache:
        return _did_cache[handle]

    try:
        profile = client.get_profile(handle)
        _did_cache[handle] = profile.did
        return profile.did
    except Exception:
        return None


def parse_text_to_rich(text: str, client: Client = None) -> client_utils.TextBuilder:
    """
    Parse plain text and return a TextBuilder with URLs and mentions as clickable.

    This handles:
    - URLs (http:// and https://) -> clickable links
    - Mentions (@handle.domain) -> clickable mentions (if client provided)

    Args:
        text: The post text
        client: Optional authenticated client for resolving @mentions to DIDs

    Returns a TextBuilder that can be passed to send_post().
    """
    builder = client_utils.TextBuilder()

    # Find all URLs and mentions with their positions
    elements = []

    for match in URL_PATTERN.finditer(text):
        elements.append({
            'type': 'url',
            'start': match.start(),
            'end': match.end(),
            'text': match.group(),
            'uri': match.group()
        })

    for match in MENTION_PATTERN.finditer(text):
        handle = match.group(1)
        did = None
        if client:
            did = resolve_handle_to_did(client, handle)
        elements.append({
            'type': 'mention',
            'start': match.start(),
            'end': match.end(),
            'text': match.group(),
            'handle': handle,
            'did': did
        })

    # Sort by start position
    elements.sort(key=lambda x: x['start'])

    # Build text with facets
    last_end = 0

    for elem in elements:
        # Add plain text before this element
        if elem['start'] > last_end:
            builder.text(text[last_end:elem['start']])

        if elem['type'] == 'url':
            builder.link(elem['text'], elem['uri'])
        elif elem['type'] == 'mention':
            if elem.get('did'):
                # Proper clickable mention with DID
                builder.mention(elem['text'], elem['did'])
            else:
                # Fallback to plain text if DID resolution failed
                builder.text(elem['text'])

        last_end = elem['end']

    # Add remaining text
    if last_end < len(text):
        builder.text(text[last_end:])

    return builder


def send_post_rich(client: Client, text: str, **kwargs) -> any:
    """
    Send a post with automatic URL and @mention faceting.

    Usage:
        client = get_client()
        response = send_post_rich(client, "Hey @atlas-agent.bsky.social check https://example.com!")

    URLs will be clickable links. @mentions will be clickable and notify the user.

    Additional kwargs are passed to send_post (e.g., reply_to, embed).
    """
    rich_text = parse_text_to_rich(text, client)  # Pass client for mention resolution
    return client.send_post(rich_text, **kwargs)


def send_thread_rich(client: Client, posts: list[str], first_embed=None) -> list[str]:
    """
    Send a thread with automatic URL and @mention faceting on all posts.

    Args:
        client: Authenticated Bluesky client
        posts: List of post texts
        first_embed: Optional embed (e.g., image) for first post

    Returns:
        List of post URIs
    """
    import time

    if not posts:
        return []

    results = []

    # First post
    rich_text = parse_text_to_rich(posts[0], client)
    if first_embed:
        response = client.send_post(rich_text, embed=first_embed)
    else:
        response = client.send_post(rich_text)

    root_post = response
    parent_post = response
    results.append(response.uri)

    # Subsequent posts
    for post_text in posts[1:]:
        time.sleep(2)  # Rate limiting

        reply_ref = models.AppBskyFeedPost.ReplyRef(
            root=models.create_strong_ref(root_post),
            parent=models.create_strong_ref(parent_post)
        )

        rich_text = parse_text_to_rich(post_text, client)
        response = client.send_post(rich_text, reply_to=reply_ref)
        parent_post = response
        results.append(response.uri)

    return results


# Quick test
if __name__ == "__main__":
    # Test the parser (without client - mentions won't resolve)
    test_text = "Hey @atlas-agent.bsky.social check https://sageandweaver-network.netlify.app/!"
    builder = parse_text_to_rich(test_text)  # No client = mentions stay as text
    print(f"Text: {builder.build_text()}")
    print(f"Facets (URL only, no client): {builder.build_facets()}")

    # With client, mentions would also resolve to DIDs
