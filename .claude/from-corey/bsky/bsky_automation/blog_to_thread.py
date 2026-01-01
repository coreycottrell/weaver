#!/usr/bin/env python3
"""
Blog to Bluesky Thread Generator

Takes a blog URL, extracts key points, generates a teaser thread.
"""

import sys
import os
from pathlib import Path

# Add parent for imports
sys.path.insert(0, str(Path(__file__).parent))

from atproto import Client, models
import time


def generate_thread_posts(blog_title: str, blog_url: str, key_points: list[str]) -> list[str]:
    """
    Generate thread posts from key points.

    Args:
        blog_title: Title of the blog post
        blog_url: URL to the full article
        key_points: List of 3-4 key insights from the blog

    Returns list of 5-7 posts.
    """
    posts = []

    # Post 1: Hook
    posts.append(f"🧵 {blog_title}\n\nA thread on what we discovered.")

    # Posts 2-5: Key insights
    for point in key_points[:4]:
        if len(point) > 280:
            point = point[:277] + "..."
        posts.append(point)

    # Gap post
    posts.append("But there's more we couldn't fit in this thread.\n\nThe full story goes deeper.")

    # Link post
    posts.append(f"Read the complete article:\n\n{blog_url}\n\n🤖")

    return posts


def post_thread(posts: list[str], dry_run: bool = False) -> list[dict]:
    """Post thread to Bluesky."""

    if dry_run:
        print("=== DRY RUN ===")
        for i, post in enumerate(posts, 1):
            print(f"\n[{i}/{len(posts)}] ({len(post)} chars)")
            print("-" * 40)
            print(post)
        return []

    # Load session
    client = Client()
    session_file = Path(__file__).parent / "bsky_session.txt"

    if session_file.exists():
        with open(session_file) as f:
            session_str = f.read().strip()
            if session_str:
                try:
                    client.login(session_string=session_str)
                    print(f"Session restored for {client.me.handle}")
                except:
                    print("Session expired, logging in fresh...")
                    client.login(os.getenv('BSKY_USERNAME'), os.getenv('BSKY_PASSWORD'))
                    with open(session_file, 'w') as f:
                        f.write(client.export_session_string())
    else:
        client.login(os.getenv('BSKY_USERNAME'), os.getenv('BSKY_PASSWORD'))
        with open(session_file, 'w') as f:
            f.write(client.export_session_string())

    print(f"Posting thread with {len(posts)} posts...")

    results = []
    root_post = None
    parent_post = None

    for i, text in enumerate(posts, 1):
        # Truncate if needed
        if len(text) > 300:
            text = text[:297] + "..."

        try:
            if parent_post is None:
                # First post
                response = client.send_post(text=text)
                root_post = response
            else:
                # Reply to previous
                reply_ref = models.AppBskyFeedPost.ReplyRef(
                    root=models.ComAtprotoRepoStrongRef.Main(
                        uri=root_post.uri,
                        cid=root_post.cid
                    ),
                    parent=models.ComAtprotoRepoStrongRef.Main(
                        uri=parent_post.uri,
                        cid=parent_post.cid
                    )
                )
                response = client.send_post(text=text, reply_to=reply_ref)

            parent_post = response
            results.append({
                'index': i,
                'uri': response.uri,
                'text': text[:50] + "..."
            })

            print(f"[{i}/{len(posts)}] ✅ Posted")

            # Small delay between posts
            if i < len(posts):
                time.sleep(1.5)

        except Exception as e:
            print(f"[{i}/{len(posts)}] ❌ Failed: {e}")
            results.append({'index': i, 'error': str(e)})

    print(f"\n✅ Thread posted! {len([r for r in results if 'uri' in r])}/{len(posts)} successful")

    if results and 'uri' in results[0]:
        uri = results[0]['uri']
        post_id = uri.split('/')[-1]
        print(f"\nView thread: https://bsky.app/profile/{client.me.handle}/post/{post_id}")

    return results


def main():
    import argparse

    parser = argparse.ArgumentParser(description="Generate Bluesky thread from blog post")
    parser.add_argument("--title", "-t", required=True, help="Blog title")
    parser.add_argument("--url", "-u", required=True, help="Blog URL")
    parser.add_argument("--points", "-p", nargs="+", required=True, help="Key points (3-4)")
    parser.add_argument("--post", action="store_true", help="Actually post (default: dry run)")

    args = parser.parse_args()

    print(f"Generating thread for: {args.title}")

    # Generate thread
    posts = generate_thread_posts(args.title, args.url, args.points)

    # Post or dry run
    post_thread(posts, dry_run=not args.post)


if __name__ == "__main__":
    main()
