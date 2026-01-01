"""
Bluesky Profile Automation - Follow users and engage with their content

Updated for 2025 using the official atproto Python SDK.

IMPORTANT: 
- Automated engagement should be authentic and add value
- Clearly mark AI-generated content
- Respect rate limits and community guidelines
- Spammy behavior can result in account suspension
"""

import os
import sys
import time
import argparse
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, Optional, List

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from session_manager import BlueskySessionManager
from rate_limiter import get_rate_limiter
from ai_responder import AIResponder, create_responder


class BlueskyAutomation:
    """
    Main automation class for Bluesky engagement.
    
    Features:
    - Follow users
    - Comment on posts with AI-generated responses
    - Like posts
    - Respect rate limits
    """
    
    def __init__(
        self,
        session_file: str = "session.json",
        ai_provider: str = "openai",
        ai_model: Optional[str] = None
    ):
        """
        Initialize the automation.
        
        Args:
            session_file: Path to session storage
            ai_provider: AI provider for responses ("openai" or "anthropic")
            ai_model: Optional model override
        """
        self.manager = BlueskySessionManager(session_file=session_file)
        self.client = self.manager.get_client()
        self.rate_limiter = get_rate_limiter()
        
        # Initialize AI responder (optional)
        try:
            self.ai_responder = create_responder(provider=ai_provider, model=ai_model)
            print(f"[INFO] AI Responder initialized ({ai_provider})")
        except Exception as e:
            print(f"[WARNING] AI Responder not available: {e}")
            self.ai_responder = None
    
    def get_user_profile(self, handle: str) -> Optional[Dict[str, Any]]:
        """Get a user's profile information."""
        self.rate_limiter.wait_if_needed(1)
        
        try:
            profile = self.client.app.bsky.actor.get_profile({'actor': handle})
            return {
                'did': profile.did,
                'handle': profile.handle,
                'display_name': getattr(profile, 'display_name', '') or '',
                'bio': getattr(profile, 'description', '') or '',
                'avatar': getattr(profile, 'avatar', '') or '',
                'followers_count': getattr(profile, 'followers_count', 0) or 0,
                'follows_count': getattr(profile, 'follows_count', 0) or 0,
                'posts_count': getattr(profile, 'posts_count', 0) or 0,
            }
        except Exception as e:
            print(f"[ERROR] Failed to get profile for @{handle}: {e}")
            return None
    
    def follow_user(self, handle: str) -> bool:
        """Follow a user by their handle."""
        self.rate_limiter.wait_if_needed(3)  # Follow = 3 points
        
        try:
            self.client.follow(handle)
            self.rate_limiter.record_create()
            print(f"[SUCCESS] Followed @{handle}")
            return True
        except Exception as e:
            error_msg = str(e).lower()
            if 'already' in error_msg or 'duplicate' in error_msg:
                print(f"[INFO] Already following @{handle}")
                return True
            print(f"[ERROR] Failed to follow @{handle}: {e}")
            return False
    
    def get_user_posts(self, handle: str, limit: int = 10) -> List[Dict[str, Any]]:
        """Get a user's recent posts."""
        self.rate_limiter.wait_if_needed(1)
        
        try:
            response = self.client.app.bsky.feed.get_author_feed({
                'actor': handle,
                'limit': limit
            })
            
            posts = []
            for item in response.feed:
                post = item.post
                record = post.record
                
                posts.append({
                    'uri': post.uri,
                    'cid': post.cid,
                    'text': getattr(record, 'text', ''),
                    'created_at': getattr(record, 'created_at', ''),
                    'like_count': getattr(post, 'like_count', 0) or 0,
                    'reply_count': getattr(post, 'reply_count', 0) or 0,
                    'repost_count': getattr(post, 'repost_count', 0) or 0,
                })
            
            return posts
            
        except Exception as e:
            print(f"[ERROR] Failed to get posts for @{handle}: {e}")
            return []
    
    def like_post(self, uri: str, cid: str) -> bool:
        """Like a post."""
        self.rate_limiter.wait_if_needed(3)
        
        try:
            self.client.like(uri, cid)
            self.rate_limiter.record_create()
            return True
        except Exception as e:
            print(f"[ERROR] Failed to like post: {e}")
            return False
    
    def reply_to_post(
        self,
        post_uri: str,
        post_cid: str,
        text: str,
        root_uri: Optional[str] = None,
        root_cid: Optional[str] = None
    ) -> bool:
        """Reply to a post."""
        self.rate_limiter.wait_if_needed(3)
        
        try:
            # Use post as root if not specified (direct reply)
            from atproto import models
            
            reply_ref = models.AppBskyFeedPost.ReplyRef(
                root=models.ComAtprotoRepoStrongRef.Main(
                    uri=root_uri or post_uri,
                    cid=root_cid or post_cid
                ),
                parent=models.ComAtprotoRepoStrongRef.Main(
                    uri=post_uri,
                    cid=post_cid
                )
            )
            
            self.client.send_post(text=text, reply_to=reply_ref)
            self.rate_limiter.record_create()
            
            print(f"[SUCCESS] Posted reply: {text[:50]}...")
            return True
            
        except Exception as e:
            print(f"[ERROR] Failed to reply: {e}")
            return False
    
    def process_profile(
        self,
        handle: str,
        follow: bool = True,
        like: bool = True,
        comment: bool = False,
        use_ai: bool = True
    ) -> Dict[str, Any]:
        """
        Process a single profile - follow, like, and optionally comment.
        
        Args:
            handle: User's handle
            follow: Whether to follow the user
            like: Whether to like their latest post
            comment: Whether to comment on their latest post
            use_ai: Whether to use AI for generating comments
            
        Returns:
            Dictionary with results
        """
        print(f"\n{'='*50}")
        print(f"📝 Processing profile: @{handle}")
        
        results = {
            'handle': handle,
            'followed': False,
            'liked': False,
            'commented': False,
            'error': None
        }
        
        # Get user profile
        profile = self.get_user_profile(handle)
        if not profile:
            results['error'] = 'Could not get profile'
            return results
        
        print(f"   👤 {profile['display_name']} - {profile['followers_count']:,} followers")
        
        # Follow user
        if follow:
            results['followed'] = self.follow_user(handle)
            time.sleep(1)
        
        # Get their posts
        posts = self.get_user_posts(handle, limit=1)
        
        if not posts:
            print(f"   ℹ️ No posts found for @{handle}")
            return results
        
        latest_post = posts[0]
        print(f"   📄 Latest post: {latest_post['text'][:80]}...")
        
        # Like their latest post
        if like:
            if self.like_post(latest_post['uri'], latest_post['cid']):
                results['liked'] = True
                print(f"   ❤️ Liked post")
            time.sleep(1)
        
        # Comment on their latest post
        if comment and self.ai_responder and use_ai:
            try:
                # Generate AI response
                response = self.ai_responder.generate_response(
                    post_text=latest_post['text'],
                    user_bio=profile['bio'],
                    user_stats={'followers': profile['followers_count']}
                )
                
                if self.reply_to_post(
                    post_uri=latest_post['uri'],
                    post_cid=latest_post['cid'],
                    text=response
                ):
                    results['commented'] = True
                    print(f"   💬 Commented: {response}")
                    
            except Exception as e:
                print(f"   [ERROR] Failed to generate/post comment: {e}")
        
        return results
    
    def process_profiles(
        self,
        handles: List[str],
        follow: bool = True,
        like: bool = True,
        comment: bool = False,
        delay: float = 3.0,
        max_count: Optional[int] = None
    ) -> List[Dict[str, Any]]:
        """
        Process multiple profiles.
        
        Args:
            handles: List of handles to process
            follow: Whether to follow users
            like: Whether to like posts
            comment: Whether to comment on posts
            delay: Delay between profiles in seconds
            max_count: Maximum profiles to process
            
        Returns:
            List of result dictionaries
        """
        results = []
        count = min(len(handles), max_count) if max_count else len(handles)
        
        print(f"\n🚀 Processing {count} profiles...")
        
        for i, handle in enumerate(handles[:count], 1):
            try:
                result = self.process_profile(
                    handle=handle,
                    follow=follow,
                    like=like,
                    comment=comment
                )
                results.append(result)
                
                if i < count:
                    print(f"   ⏳ Waiting {delay}s before next profile...")
                    time.sleep(delay)
                    
            except KeyboardInterrupt:
                print("\n\n⚠️ Interrupted by user")
                break
            except Exception as e:
                print(f"   [ERROR] Failed to process @{handle}: {e}")
                results.append({
                    'handle': handle,
                    'error': str(e)
                })
        
        # Print summary
        print(f"\n{'='*50}")
        print("📊 Summary:")
        successful = sum(1 for r in results if not r.get('error'))
        followed = sum(1 for r in results if r.get('followed'))
        liked = sum(1 for r in results if r.get('liked'))
        commented = sum(1 for r in results if r.get('commented'))
        
        print(f"   Processed: {len(results)}")
        print(f"   Successful: {successful}")
        print(f"   Followed: {followed}")
        print(f"   Liked: {liked}")
        print(f"   Commented: {commented}")
        
        self.rate_limiter.print_status()
        
        return results


def main():
    parser = argparse.ArgumentParser(
        description="Bluesky Profile Automation"
    )
    parser.add_argument(
        "handles",
        nargs="*",
        help="Handles to process (or use --file)"
    )
    parser.add_argument(
        "-f", "--file",
        help="JSON file with handles"
    )
    parser.add_argument(
        "--no-follow",
        action="store_true",
        help="Don't follow users"
    )
    parser.add_argument(
        "--no-like",
        action="store_true",
        help="Don't like posts"
    )
    parser.add_argument(
        "--comment",
        action="store_true",
        help="Comment on posts (requires AI)"
    )
    parser.add_argument(
        "-d", "--delay",
        type=float,
        default=3.0,
        help="Delay between profiles (default: 3.0)"
    )
    parser.add_argument(
        "-m", "--max",
        type=int,
        help="Maximum profiles to process"
    )
    parser.add_argument(
        "-s", "--session",
        default="session.json",
        help="Session file path"
    )
    parser.add_argument(
        "--ai-provider",
        choices=["openai", "anthropic"],
        default="openai",
        help="AI provider for comments"
    )
    
    args = parser.parse_args()
    
    # Get handles
    handles = list(args.handles)
    
    if args.file:
        import json
        with open(args.file, 'r') as f:
            data = json.load(f)
            for item in data:
                if isinstance(item, str):
                    handles.append(item)
                elif isinstance(item, dict) and 'handle' in item:
                    handles.append(item['handle'])
    
    if not handles:
        print("No handles provided. Use positional arguments or --file")
        parser.print_help()
        return
    
    try:
        automation = BlueskyAutomation(
            session_file=args.session,
            ai_provider=args.ai_provider
        )
        
        automation.process_profiles(
            handles=handles,
            follow=not args.no_follow,
            like=not args.no_like,
            comment=args.comment,
            delay=args.delay,
            max_count=args.max
        )
        
    except KeyboardInterrupt:
        print("\n\nAutomation cancelled.")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
