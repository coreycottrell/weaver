"""
Bluesky Scheduler - Schedule posts and automation tasks

Run this as a long-running daemon to schedule posts.
"""

import os
import sys
import time
import json
import argparse
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, Any, Optional, List, Callable
import threading

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))

try:
    import schedule
except ImportError:
    print("Please install schedule: pip install schedule")
    sys.exit(1)

from session_manager import BlueskySessionManager
from rate_limiter import get_rate_limiter
from content_creator import ContentCreator


class PostScheduler:
    """
    Schedule posts for future publishing.
    
    Supports:
    - One-time scheduled posts
    - Recurring posts (daily, weekly)
    - Loading scheduled posts from JSON
    """
    
    def __init__(self, session_file: str = "session.json"):
        self.session_file = session_file
        self.creator = None
        self.scheduled_posts: List[Dict[str, Any]] = []
        self.running = False
    
    def _ensure_creator(self):
        """Ensure content creator is initialized."""
        if self.creator is None:
            self.creator = ContentCreator(session_file=self.session_file)
    
    def add_post(
        self,
        text: str,
        scheduled_time: Optional[datetime] = None,
        repeat: Optional[str] = None,
        image_path: Optional[str] = None,
        alt_text: Optional[str] = None
    ) -> str:
        """
        Add a post to the schedule.
        
        Args:
            text: Post text
            scheduled_time: When to post (None = now)
            repeat: Repeat schedule ('daily', 'weekly', or None)
            image_path: Optional image to attach
            alt_text: Alt text for image
            
        Returns:
            Post ID
        """
        import uuid
        
        post_id = str(uuid.uuid4())[:8]
        
        post = {
            'id': post_id,
            'text': text,
            'scheduled_time': scheduled_time.isoformat() if scheduled_time else None,
            'repeat': repeat,
            'image_path': image_path,
            'alt_text': alt_text,
            'status': 'scheduled',
            'created_at': datetime.utcnow().isoformat()
        }
        
        self.scheduled_posts.append(post)
        print(f"[SCHEDULED] Post {post_id}: {text[:40]}...")
        
        return post_id
    
    def load_from_file(self, file_path: str) -> int:
        """
        Load scheduled posts from a JSON file.
        
        File format:
        [
            {
                "text": "Post content",
                "time": "2025-01-15T10:00:00",
                "repeat": "daily"  // optional
            }
        ]
        
        Returns:
            Number of posts loaded
        """
        with open(file_path, 'r') as f:
            data = json.load(f)
        
        count = 0
        for item in data:
            scheduled_time = None
            if item.get('time'):
                scheduled_time = datetime.fromisoformat(item['time'])
            
            self.add_post(
                text=item['text'],
                scheduled_time=scheduled_time,
                repeat=item.get('repeat'),
                image_path=item.get('image'),
                alt_text=item.get('alt_text')
            )
            count += 1
        
        return count
    
    def save_to_file(self, file_path: str) -> None:
        """Save scheduled posts to a JSON file."""
        with open(file_path, 'w') as f:
            json.dump(self.scheduled_posts, f, indent=2)
        print(f"[INFO] Saved {len(self.scheduled_posts)} posts to {file_path}")
    
    def _execute_post(self, post: Dict[str, Any]) -> bool:
        """Execute a scheduled post."""
        self._ensure_creator()
        
        try:
            if post.get('image_path'):
                result = self.creator.post_with_image(
                    text=post['text'],
                    image_path=post['image_path'],
                    alt_text=post.get('alt_text', '')
                )
            else:
                result = self.creator.post_text(post['text'])
            
            if result:
                post['status'] = 'posted'
                post['posted_at'] = datetime.utcnow().isoformat()
                post['uri'] = result.get('uri')
                return True
            else:
                post['status'] = 'failed'
                return False
                
        except Exception as e:
            print(f"[ERROR] Failed to post: {e}")
            post['status'] = 'failed'
            post['error'] = str(e)
            return False
    
    def _check_and_post(self) -> None:
        """Check for posts due and execute them."""
        now = datetime.utcnow()
        
        for post in self.scheduled_posts:
            if post['status'] != 'scheduled':
                continue
            
            if post.get('scheduled_time'):
                scheduled = datetime.fromisoformat(post['scheduled_time'])
                if scheduled > now:
                    continue
            
            print(f"\n[POSTING] {post['id']}: {post['text'][:40]}...")
            success = self._execute_post(post)
            
            if success and post.get('repeat'):
                # Schedule next occurrence
                if post['repeat'] == 'daily':
                    next_time = datetime.fromisoformat(post['scheduled_time']) + timedelta(days=1)
                elif post['repeat'] == 'weekly':
                    next_time = datetime.fromisoformat(post['scheduled_time']) + timedelta(weeks=1)
                else:
                    continue
                
                self.add_post(
                    text=post['text'],
                    scheduled_time=next_time,
                    repeat=post['repeat'],
                    image_path=post.get('image_path'),
                    alt_text=post.get('alt_text')
                )
    
    def run(self, check_interval: int = 60) -> None:
        """
        Run the scheduler daemon.
        
        Args:
            check_interval: Seconds between checks
        """
        print(f"\n🕐 Starting scheduler (checking every {check_interval}s)...")
        print(f"   {len(self.scheduled_posts)} posts scheduled")
        print("   Press Ctrl+C to stop\n")
        
        self.running = True
        
        try:
            while self.running:
                self._check_and_post()
                time.sleep(check_interval)
        except KeyboardInterrupt:
            print("\n\n[INFO] Scheduler stopped")
            self.running = False
    
    def list_posts(self) -> None:
        """Print all scheduled posts."""
        print(f"\n📋 Scheduled Posts ({len(self.scheduled_posts)}):")
        
        for post in self.scheduled_posts:
            status_icon = {
                'scheduled': '⏳',
                'posted': '✅',
                'failed': '❌'
            }.get(post['status'], '❓')
            
            time_str = post.get('scheduled_time', 'now')[:16] if post.get('scheduled_time') else 'now'
            repeat_str = f" [{post['repeat']}]" if post.get('repeat') else ""
            
            print(f"  {status_icon} [{post['id']}] {time_str}{repeat_str}")
            print(f"      {post['text'][:60]}...")


def main():
    parser = argparse.ArgumentParser(description="Bluesky Post Scheduler")
    
    subparsers = parser.add_subparsers(dest="command", help="Commands")
    
    # Add command
    add_parser = subparsers.add_parser("add", help="Add a scheduled post")
    add_parser.add_argument("text", help="Post text")
    add_parser.add_argument("-t", "--time", help="ISO datetime (e.g., 2025-01-15T10:00:00)")
    add_parser.add_argument("-r", "--repeat", choices=["daily", "weekly"], help="Repeat schedule")
    add_parser.add_argument("-i", "--image", help="Image path")
    add_parser.add_argument("-a", "--alt", help="Image alt text")
    add_parser.add_argument("-o", "--output", default="scheduled_posts.json", help="Save file")
    
    # Run command
    run_parser = subparsers.add_parser("run", help="Run the scheduler daemon")
    run_parser.add_argument("-f", "--file", default="scheduled_posts.json", help="Load from file")
    run_parser.add_argument("-i", "--interval", type=int, default=60, help="Check interval (seconds)")
    
    # List command
    list_parser = subparsers.add_parser("list", help="List scheduled posts")
    list_parser.add_argument("-f", "--file", default="scheduled_posts.json", help="File to read")
    
    # Common
    for p in [add_parser, run_parser]:
        p.add_argument("-s", "--session", default="session.json", help="Session file")
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    scheduler = PostScheduler(
        session_file=getattr(args, 'session', 'session.json')
    )
    
    try:
        if args.command == "add":
            scheduled_time = None
            if args.time:
                scheduled_time = datetime.fromisoformat(args.time)
            
            scheduler.add_post(
                text=args.text,
                scheduled_time=scheduled_time,
                repeat=args.repeat,
                image_path=args.image,
                alt_text=args.alt
            )
            
            scheduler.save_to_file(args.output)
            
        elif args.command == "run":
            if Path(args.file).exists():
                count = scheduler.load_from_file(args.file)
                print(f"[INFO] Loaded {count} posts from {args.file}")
            
            scheduler.run(check_interval=args.interval)
            
        elif args.command == "list":
            if Path(args.file).exists():
                scheduler.load_from_file(args.file)
            scheduler.list_posts()
            
    except KeyboardInterrupt:
        print("\n\nCancelled.")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
