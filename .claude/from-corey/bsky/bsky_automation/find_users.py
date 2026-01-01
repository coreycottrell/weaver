"""
Find Users by Keyword - Search Bluesky for users with specific keywords in their bio

Updated for 2025 using the official atproto Python SDK with proper session management.
"""

import os
import sys
import json
import argparse
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Any, Optional

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from session_manager import BlueskySessionManager
from rate_limiter import get_rate_limiter


def find_users_by_keyword(
    keyword: str,
    limit: int = 25,
    output_dir: str = "data",
    session_file: str = "session.json"
) -> List[Dict[str, Any]]:
    """
    Search for users with the given keyword.
    
    Args:
        keyword: Search term to find in user profiles
        limit: Maximum number of users to return
        output_dir: Directory to save results
        session_file: Path to session storage file
        
    Returns:
        List of user dictionaries with profile information
    """
    print(f"\n🔍 Searching for users with keyword: '{keyword}'")
    print("=" * 50)
    
    # Initialize session manager and rate limiter
    manager = BlueskySessionManager(session_file=session_file)
    client = manager.get_client()
    rate_limiter = get_rate_limiter()
    
    # Create output directory
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    
    users = []
    cursor = None
    total_fetched = 0
    
    try:
        while total_fetched < limit:
            # Respect rate limits
            rate_limiter.wait_if_needed(1)
            
            # Search for actors
            params = {
                'q': keyword,
                'limit': min(25, limit - total_fetched)  # API max is 25
            }
            if cursor:
                params['cursor'] = cursor
            
            response = client.app.bsky.actor.search_actors(params)
            
            if not response.actors:
                break
            
            for actor in response.actors:
                # Get detailed profile (rate limited)
                rate_limiter.wait_if_needed(1)
                
                try:
                    profile = client.app.bsky.actor.get_profile({'actor': actor.handle})
                    
                    user_data = {
                        'handle': actor.handle,
                        'did': actor.did,
                        'displayName': getattr(actor, 'display_name', '') or '',
                        'bio': getattr(actor, 'description', '') or '',
                        'avatar': getattr(profile, 'avatar', '') or '',
                        'followersCount': getattr(profile, 'followers_count', 0) or 0,
                        'followsCount': getattr(profile, 'follows_count', 0) or 0,
                        'postsCount': getattr(profile, 'posts_count', 0) or 0,
                        'indexedAt': getattr(profile, 'indexed_at', '') or '',
                        'createdAt': getattr(profile, 'created_at', '') or '',
                    }
                    users.append(user_data)
                    total_fetched += 1
                    
                    print(f"   [{total_fetched}] @{actor.handle} - {user_data['followersCount']} followers")
                    
                    if total_fetched >= limit:
                        break
                        
                except Exception as e:
                    print(f"   [WARNING] Could not get profile for @{actor.handle}: {e}")
            
            cursor = getattr(response, 'cursor', None)
            if not cursor:
                break
        
        # Sort by follower count
        users_sorted = sorted(users, key=lambda x: x['followersCount'], reverse=True)
        
        # Save to file
        timestamp = datetime.utcnow().strftime('%Y%m%d_%H%M%S')
        safe_keyword = "".join(c if c.isalnum() else "_" for c in keyword)
        output_file = output_path / f"users_{safe_keyword}_{timestamp}.json"
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(users_sorted, f, indent=2, ensure_ascii=False)
        
        # Print summary
        print(f"\n✅ Found {len(users)} users matching '{keyword}'")
        
        if users_sorted:
            print("\n🏆 Top 5 Users by Follower Count:")
            for i, user in enumerate(users_sorted[:5], 1):
                print(f"   {i}. {user['displayName']} (@{user['handle']})")
                print(f"      Followers: {user['followersCount']:,}")
        
        print(f"\n📁 Results saved to: {output_file}")
        
        # Print rate limit status
        rate_limiter.print_status()
        
        return users_sorted
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        raise


def main():
    parser = argparse.ArgumentParser(
        description="Search Bluesky for users with specific keywords"
    )
    parser.add_argument(
        "keyword",
        nargs="?",
        help="Keyword to search for in user profiles"
    )
    parser.add_argument(
        "-l", "--limit",
        type=int,
        default=25,
        help="Maximum number of users to fetch (default: 25)"
    )
    parser.add_argument(
        "-o", "--output",
        default="data",
        help="Output directory for results (default: data)"
    )
    parser.add_argument(
        "-s", "--session",
        default="session.json",
        help="Session file path (default: session.json)"
    )
    
    args = parser.parse_args()
    
    # Get keyword from args or prompt
    keyword = args.keyword
    if not keyword:
        keyword = input("Enter the keyword to search for: ").strip()
        if not keyword:
            print("No keyword provided. Exiting.")
            return
    
    try:
        find_users_by_keyword(
            keyword=keyword,
            limit=args.limit,
            output_dir=args.output,
            session_file=args.session
        )
    except KeyboardInterrupt:
        print("\n\nSearch cancelled.")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
