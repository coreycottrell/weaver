"""
Reply to comments on Bluesky posts

Used to respond to specific users who reply to WEAVER's posts.
"""

import os
import sys
from pathlib import Path
from typing import Dict, Any, Optional, List

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from session_manager import BlueskySessionManager
from rate_limiter import get_rate_limiter


class CommentResponder:
    """
    Find and reply to comments on Bluesky.
    """

    def __init__(self, session_file: str = "bsky_session.txt"):
        self.manager = BlueskySessionManager(session_file=session_file)
        self.client = self.manager.get_client()
        self.rate_limiter = get_rate_limiter()

    def get_notifications(self, limit: int = 50) -> List[Dict[str, Any]]:
        """Get recent notifications (mentions, replies, likes, etc.)."""
        try:
            response = self.client.app.bsky.notification.list_notifications(
                {'limit': limit}
            )
            return response.notifications
        except Exception as e:
            print(f"[ERROR] Failed to get notifications: {e}")
            return []

    def get_thread(self, uri: str) -> Optional[Dict[str, Any]]:
        """Get a thread by post URI."""
        try:
            response = self.client.app.bsky.feed.get_post_thread({'uri': uri})
            return response.thread
        except Exception as e:
            print(f"[ERROR] Failed to get thread: {e}")
            return None

    def reply_to_post(
        self,
        parent_uri: str,
        parent_cid: str,
        root_uri: str,
        root_cid: str,
        text: str,
        langs: Optional[List[str]] = None
    ) -> Optional[Dict[str, Any]]:
        """
        Reply to a specific post.

        Args:
            parent_uri: URI of the post being replied to
            parent_cid: CID of the post being replied to
            root_uri: URI of the thread root
            root_cid: CID of the thread root
            text: Reply text
            langs: Language codes
        """
        if len(text) > 300:
            print(f"[WARNING] Text too long ({len(text)} chars). Truncating to 300.")
            text = text[:297] + "..."

        self.rate_limiter.wait_if_needed(3)

        try:
            from atproto import models

            reply_ref = models.AppBskyFeedPost.ReplyRef(
                root=models.ComAtprotoRepoStrongRef.Main(
                    uri=root_uri,
                    cid=root_cid
                ),
                parent=models.ComAtprotoRepoStrongRef.Main(
                    uri=parent_uri,
                    cid=parent_cid
                )
            )

            response = self.client.send_post(
                text=text,
                reply_to=reply_ref,
                langs=langs or ['en']
            )
            self.rate_limiter.record_create()

            print(f"[SUCCESS] Replied: {text[:50]}...")
            print(f"   URI: {response.uri}")

            return {
                'uri': response.uri,
                'cid': response.cid,
                'text': text
            }

        except Exception as e:
            print(f"[ERROR] Failed to reply: {e}")
            return None

    def find_replies_by_handle(self, handle: str) -> List[Dict[str, Any]]:
        """Find recent replies from a specific user handle."""
        notifications = self.get_notifications(limit=100)
        replies = []

        for notif in notifications:
            if notif.reason in ('reply', 'mention'):
                author_handle = notif.author.handle
                if handle.lower() in author_handle.lower() or author_handle.lower() in handle.lower():
                    replies.append({
                        'handle': author_handle,
                        'reason': notif.reason,
                        'uri': notif.uri,
                        'cid': notif.cid,
                        'text': getattr(notif.record, 'text', ''),
                        'indexed_at': notif.indexed_at,
                        'record': notif.record
                    })

        return replies

    def show_notifications(self, limit: int = 20):
        """Display recent notifications."""
        notifications = self.get_notifications(limit=limit)

        print(f"\n=== Recent Notifications ({len(notifications)} found) ===\n")

        for i, notif in enumerate(notifications, 1):
            author = notif.author.handle
            reason = notif.reason
            text = getattr(notif.record, 'text', '')[:100] if hasattr(notif.record, 'text') else ''

            print(f"{i}. @{author}")
            print(f"   Reason: {reason}")
            print(f"   URI: {notif.uri}")
            if text:
                print(f"   Text: {text}...")
            print()


def main():
    import argparse
    parser = argparse.ArgumentParser(description="Reply to Bluesky comments")

    subparsers = parser.add_subparsers(dest="command", help="Commands")

    # List notifications
    list_parser = subparsers.add_parser("list", help="List notifications")
    list_parser.add_argument("-n", "--limit", type=int, default=20, help="Number to show")

    # Find replies from user
    find_parser = subparsers.add_parser("find", help="Find replies from user")
    find_parser.add_argument("handle", help="User handle to find")

    # Reply to a post
    reply_parser = subparsers.add_parser("reply", help="Reply to a post")
    reply_parser.add_argument("--parent-uri", required=True, help="Parent post URI")
    reply_parser.add_argument("--parent-cid", required=True, help="Parent post CID")
    reply_parser.add_argument("--root-uri", help="Root post URI (defaults to parent)")
    reply_parser.add_argument("--root-cid", help="Root post CID (defaults to parent)")
    reply_parser.add_argument("--text", required=True, help="Reply text")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return

    responder = CommentResponder()

    if args.command == "list":
        responder.show_notifications(args.limit)

    elif args.command == "find":
        replies = responder.find_replies_by_handle(args.handle)
        print(f"\n=== Replies from @{args.handle} ===\n")
        for r in replies:
            print(f"Handle: @{r['handle']}")
            print(f"Reason: {r['reason']}")
            print(f"URI: {r['uri']}")
            print(f"CID: {r['cid']}")
            print(f"Text: {r['text']}")
            print()

    elif args.command == "reply":
        root_uri = args.root_uri or args.parent_uri
        root_cid = args.root_cid or args.parent_cid

        responder.reply_to_post(
            parent_uri=args.parent_uri,
            parent_cid=args.parent_cid,
            root_uri=root_uri,
            root_cid=root_cid,
            text=args.text
        )


if __name__ == "__main__":
    main()
