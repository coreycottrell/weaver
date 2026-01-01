"""
Bluesky Content Creator - Create and post content to Bluesky

Updated for 2025 using the official atproto Python SDK.

Features:
- Post text content
- Post images
- Schedule posts
- AI-assisted content generation
- Thread creation
"""

import os
import sys
import time
import json
import argparse
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, Any, Optional, List, Union

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from session_manager import BlueskySessionManager
from rate_limiter import get_rate_limiter
from ai_responder import AIResponder, create_responder


class ContentCreator:
    """
    Create and post content to Bluesky.
    
    Features:
    - Simple text posts
    - Posts with images
    - Thread creation
    - AI-assisted content generation
    """
    
    def __init__(
        self,
        session_file: str = "session.json",
        ai_provider: str = "openai"
    ):
        self.manager = BlueskySessionManager(session_file=session_file)
        self.client = self.manager.get_client()
        self.rate_limiter = get_rate_limiter()
        
        # Initialize AI for content generation
        try:
            self.ai_responder = create_responder(provider=ai_provider)
            print("[INFO] AI Content Generator initialized")
        except Exception as e:
            print(f"[WARNING] AI not available: {e}")
            self.ai_responder = None
    
    def post_text(self, text: str, langs: Optional[List[str]] = None) -> Optional[Dict[str, Any]]:
        """
        Post a simple text post.
        
        Args:
            text: Post text (max 300 chars)
            langs: List of language codes (e.g., ['en'])
            
        Returns:
            Post response with uri and cid
        """
        if len(text) > 300:
            print(f"[WARNING] Text too long ({len(text)} chars). Truncating to 300.")
            text = text[:297] + "..."
        
        self.rate_limiter.wait_if_needed(3)
        
        try:
            response = self.client.send_post(text=text, langs=langs or ['en'])
            self.rate_limiter.record_create()
            
            print(f"[SUCCESS] Posted: {text[:50]}...")
            print(f"   URI: {response.uri}")
            
            return {
                'uri': response.uri,
                'cid': response.cid,
                'text': text
            }
            
        except Exception as e:
            print(f"[ERROR] Failed to post: {e}")
            return None
    
    def post_with_image(
        self,
        text: str,
        image_path: str,
        alt_text: str = "",
        langs: Optional[List[str]] = None
    ) -> Optional[Dict[str, Any]]:
        """
        Post with an image attachment.
        
        Args:
            text: Post text
            image_path: Path to image file
            alt_text: Alt text for accessibility
            langs: Language codes
            
        Returns:
            Post response
        """
        image_path = Path(image_path)
        if not image_path.exists():
            print(f"[ERROR] Image not found: {image_path}")
            return None
        
        # Read image
        with open(image_path, 'rb') as f:
            image_data = f.read()
        
        self.rate_limiter.wait_if_needed(3)
        
        try:
            response = self.client.send_image(
                text=text,
                image=image_data,
                image_alt=alt_text or f"Image: {image_path.name}",
                langs=langs or ['en']
            )
            self.rate_limiter.record_create()
            
            print(f"[SUCCESS] Posted with image: {text[:50]}...")
            
            return {
                'uri': response.uri,
                'cid': response.cid,
                'text': text,
                'image': str(image_path)
            }
            
        except Exception as e:
            print(f"[ERROR] Failed to post with image: {e}")
            return None
    
    def create_thread(
        self,
        posts: List[str],
        delay: float = 1.0,
        langs: Optional[List[str]] = None
    ) -> List[Dict[str, Any]]:
        """
        Create a thread of connected posts.
        
        Args:
            posts: List of post texts
            delay: Delay between posts
            langs: Language codes
            
        Returns:
            List of post responses
        """
        if not posts:
            return []
        
        print(f"\n🧵 Creating thread with {len(posts)} posts...")
        
        results = []
        root_post = None
        parent_post = None
        
        for i, text in enumerate(posts, 1):
            if len(text) > 300:
                text = text[:297] + "..."
            
            self.rate_limiter.wait_if_needed(3)
            
            try:
                if parent_post is None:
                    # First post - no reply reference
                    response = self.client.send_post(text=text, langs=langs or ['en'])
                    root_post = response
                else:
                    # Reply to previous post
                    from atproto import models
                    
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
                    
                    response = self.client.send_post(
                        text=text,
                        reply_to=reply_ref,
                        langs=langs or ['en']
                    )
                
                self.rate_limiter.record_create()
                parent_post = response
                
                results.append({
                    'index': i,
                    'uri': response.uri,
                    'cid': response.cid,
                    'text': text
                })
                
                print(f"   [{i}/{len(posts)}] Posted: {text[:40]}...")
                
                if i < len(posts):
                    time.sleep(delay)
                    
            except Exception as e:
                print(f"   [{i}/{len(posts)}] ❌ Failed: {e}")
                results.append({
                    'index': i,
                    'error': str(e),
                    'text': text
                })
        
        successful = sum(1 for r in results if 'uri' in r)
        print(f"\n✅ Thread created: {successful}/{len(posts)} posts successful")
        
        return results
    
    def generate_post_ideas(
        self,
        topic: str,
        count: int = 5,
        style: str = "informative"
    ) -> List[str]:
        """
        Generate post ideas using AI.
        
        Args:
            topic: Topic to generate posts about
            count: Number of ideas to generate
            style: Style of posts (informative, engaging, viral, etc.)
            
        Returns:
            List of post texts
        """
        if not self.ai_responder:
            print("[ERROR] AI not available for content generation")
            return []
        
        try:
            from openai import OpenAI
            client = OpenAI()
            
            prompt = f"""Generate {count} engaging Bluesky posts about: {topic}

Style: {style}
Requirements:
- Each post must be under 280 characters
- Be genuine and add value
- Avoid hashtags unless essential
- Include a hook that grabs attention
- End with something that encourages engagement

Return only the posts, one per line, numbered 1-{count}."""
            
            response = client.chat.completions.create(
                model="gpt-4o",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=1000,
                temperature=0.8
            )
            
            content = response.choices[0].message.content
            
            # Parse the response
            posts = []
            for line in content.strip().split('\n'):
                line = line.strip()
                # Remove numbering
                if line and line[0].isdigit():
                    line = line.lstrip('0123456789.):- ').strip()
                if line and len(line) <= 300:
                    posts.append(line)
            
            return posts[:count]
            
        except Exception as e:
            print(f"[ERROR] Failed to generate ideas: {e}")
            return []
    
    def generate_thread(
        self,
        topic: str,
        length: int = 5
    ) -> List[str]:
        """
        Generate a thread on a topic using AI.
        
        Args:
            topic: Topic for the thread
            length: Number of posts in thread
            
        Returns:
            List of post texts for thread
        """
        if not self.ai_responder:
            print("[ERROR] AI not available")
            return []
        
        try:
            from openai import OpenAI
            client = OpenAI()
            
            prompt = f"""Create a {length}-post thread about: {topic}

Requirements:
- First post should hook the reader (start with something like "Thread:" or "🧵")
- Each post must be under 280 characters
- Posts should flow naturally from one to the next
- Include specific, valuable information
- Last post should summarize or call to action
- Be informative and genuine

Return only the posts, numbered 1-{length}, one per line."""
            
            response = client.chat.completions.create(
                model="gpt-4o",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=1500,
                temperature=0.7
            )
            
            content = response.choices[0].message.content
            
            posts = []
            for line in content.strip().split('\n'):
                line = line.strip()
                if line and line[0].isdigit():
                    line = line.lstrip('0123456789.):- ').strip()
                if line and len(line) <= 300:
                    posts.append(line)
            
            return posts[:length]
            
        except Exception as e:
            print(f"[ERROR] Failed to generate thread: {e}")
            return []


def main():
    parser = argparse.ArgumentParser(description="Bluesky Content Creator")
    
    subparsers = parser.add_subparsers(dest="command", help="Commands")
    
    # Post command
    post_parser = subparsers.add_parser("post", help="Create a post")
    post_parser.add_argument("text", nargs="?", help="Post text")
    post_parser.add_argument("-i", "--image", help="Image to attach")
    post_parser.add_argument("-a", "--alt", help="Image alt text")
    
    # Thread command
    thread_parser = subparsers.add_parser("thread", help="Create a thread")
    thread_parser.add_argument("posts", nargs="*", help="Thread posts")
    thread_parser.add_argument("-f", "--file", help="File with posts (one per line)")
    thread_parser.add_argument("-g", "--generate", help="Generate thread on topic")
    thread_parser.add_argument("-l", "--length", type=int, default=5, help="Thread length")
    
    # Generate command
    gen_parser = subparsers.add_parser("generate", help="Generate post ideas")
    gen_parser.add_argument("topic", help="Topic for ideas")
    gen_parser.add_argument("-n", "--count", type=int, default=5, help="Number of ideas")
    gen_parser.add_argument("-s", "--style", default="engaging", help="Post style")
    gen_parser.add_argument("--post", action="store_true", help="Post the first idea")
    
    # Common arguments
    for p in [post_parser, thread_parser, gen_parser]:
        p.add_argument("--session", default="session.json", help="Session file")
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    try:
        creator = ContentCreator(session_file=args.session)
        
        if args.command == "post":
            text = args.text
            if not text:
                text = input("Enter post text: ").strip()
            
            if args.image:
                creator.post_with_image(text, args.image, args.alt or "")
            else:
                creator.post_text(text)
                
        elif args.command == "thread":
            if args.generate:
                posts = creator.generate_thread(args.generate, args.length)
                print("\nGenerated thread:")
                for i, p in enumerate(posts, 1):
                    print(f"  {i}. {p}")
                
                if input("\nPost this thread? (y/n): ").lower() == 'y':
                    creator.create_thread(posts)
            else:
                posts = list(args.posts)
                if args.file:
                    with open(args.file) as f:
                        posts.extend(line.strip() for line in f if line.strip())
                
                if posts:
                    creator.create_thread(posts)
                else:
                    print("No posts provided")
                    
        elif args.command == "generate":
            ideas = creator.generate_post_ideas(args.topic, args.count, args.style)
            
            print(f"\n💡 Post ideas for '{args.topic}':")
            for i, idea in enumerate(ideas, 1):
                print(f"\n  {i}. {idea}")
            
            if args.post and ideas:
                if input("\nPost the first idea? (y/n): ").lower() == 'y':
                    creator.post_text(ideas[0])
                    
    except KeyboardInterrupt:
        print("\n\nCancelled.")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
