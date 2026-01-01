"""
Follow Users - Follow Bluesky users from a JSON file

Updated for 2025 using the official atproto Python SDK with proper session management.

IMPORTANT: Bulk following is against Bluesky Community Guidelines if used for spam.
Use this responsibly for genuine engagement only.
"""

import os
import sys
import json
import time
import argparse
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Any, Optional

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from session_manager import BlueskySessionManager
from rate_limiter import get_rate_limiter, RateLimiter


def load_handles_from_file(file_path: str) -> List[Dict[str, Any]]:
    """
    Load handles from a JSON file.
    
    Supports formats:
    - List of strings: ["handle1", "handle2"]
    - List of objects: [{"handle": "handle1"}, {"handle": "handle2"}]
    
    Args:
        file_path: Path to JSON file
        
    Returns:
        List of handle dictionaries
    """
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    if not isinstance(data, list):
        raise ValueError("JSON file must contain a list")
    
    handles = []
    for item in data:
        if isinstance(item, str):
            handles.append({'handle': item})
        elif isinstance(item, dict) and 'handle' in item:
            handles.append(item)
        else:
            print(f"[WARNING] Skipping invalid entry: {item}")
    
    return handles


def follow_users(
    handles_file: str,
    delay: float = 2.0,
    max_per_session: int = 100,
    session_file: str = "session.json",
    dry_run: bool = False
) -> Dict[str, Any]:
    """
    Follow users from a JSON file.
    
    Args:
        handles_file: Path to JSON file with handles
        delay: Seconds between follow actions (default: 2.0)
        max_per_session: Maximum follows per session (default: 100)
        session_file: Path to session storage file
        dry_run: If True, don't actually follow, just simulate
        
    Returns:
        Dictionary with results statistics
    """
    print(f"\n👥 Follow Users from: {handles_file}")
    print("=" * 50)
    
    if dry_run:
        print("🧪 DRY RUN MODE - No actual follows will be made")
    
    # Load handles
    handles = load_handles_from_file(handles_file)
    print(f"📋 Loaded {len(handles)} handles")
    
    if not handles:
        print("No handles to process. Exiting.")
        return {'success': 0, 'failed': 0, 'skipped': 0}
    
    # Initialize session manager and rate limiter
    manager = BlueskySessionManager(session_file=session_file)
    client = manager.get_client()
    rate_limiter = get_rate_limiter()
    
    # Track results
    results = {
        'success': 0,
        'failed': 0,
        'skipped': 0,
        'already_following': 0,
        'details': []
    }
    
    # Get current following list to avoid duplicates
    print("\n📊 Checking current following list...")
    following_set = set()
    cursor = None
    
    try:
        while True:
            rate_limiter.wait_if_needed(1)
            params = {'actor': manager.handle, 'limit': 100}
            if cursor:
                params['cursor'] = cursor
            
            response = client.app.bsky.graph.get_follows(params)
            
            for follow in response.follows:
                following_set.add(follow.handle.lower())
            
            cursor = getattr(response, 'cursor', None)
            if not cursor:
                break
        
        print(f"   Currently following: {len(following_set)} users")
        
    except Exception as e:
        print(f"[WARNING] Could not fetch following list: {e}")
    
    # Process handles
    print(f"\n🚀 Starting to follow users (max {max_per_session} per session)...")
    
    for i, entry in enumerate(handles[:max_per_session], 1):
        handle = entry.get('handle', '').strip()
        
        if not handle:
            print(f"   [{i}] ⚠️ Empty handle, skipping")
            results['skipped'] += 1
            continue
        
        # Normalize handle
        if not handle.startswith('@'):
            handle_clean = handle
        else:
            handle_clean = handle[1:]
        
        # Check if already following
        if handle_clean.lower() in following_set:
            print(f"   [{i}] ⏭️ Already following @{handle_clean}")
            results['already_following'] += 1
            results['skipped'] += 1
            continue
        
        # Rate limit check
        rate_limiter.wait_if_needed(3)  # Follow = create = 3 points
        
        try:
            if dry_run:
                print(f"   [{i}] 🧪 Would follow @{handle_clean}")
                results['success'] += 1
            else:
                # Follow the user using the SDK's high-level method
                client.follow(handle_clean)
                rate_limiter.record_create()
                
                print(f"   [{i}] ✅ Followed @{handle_clean}")
                results['success'] += 1
                following_set.add(handle_clean.lower())
            
            results['details'].append({
                'handle': handle_clean,
                'status': 'success',
                'timestamp': datetime.utcnow().isoformat()
            })
            
            # Delay between actions
            if i < len(handles) and i < max_per_session:
                time.sleep(delay)
                
        except Exception as e:
            error_msg = str(e)
            print(f"   [{i}] ❌ Failed to follow @{handle_clean}: {error_msg}")
            results['failed'] += 1
            results['details'].append({
                'handle': handle_clean,
                'status': 'failed',
                'error': error_msg,
                'timestamp': datetime.utcnow().isoformat()
            })
    
    # Print summary
    print(f"\n" + "=" * 50)
    print("📊 Summary:")
    print(f"   ✅ Successfully followed: {results['success']}")
    print(f"   ⏭️ Already following: {results['already_following']}")
    print(f"   ⚠️ Skipped: {results['skipped']}")
    print(f"   ❌ Failed: {results['failed']}")
    
    # Print rate limit status
    rate_limiter.print_status()
    
    # Save results log
    log_file = Path(handles_file).parent / f"follow_log_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}.json"
    with open(log_file, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2)
    print(f"\n📁 Log saved to: {log_file}")
    
    return results


def main():
    parser = argparse.ArgumentParser(
        description="Follow Bluesky users from a JSON file"
    )
    parser.add_argument(
        "file",
        nargs="?",
        help="JSON file containing handles to follow"
    )
    parser.add_argument(
        "-d", "--delay",
        type=float,
        default=2.0,
        help="Delay between follows in seconds (default: 2.0)"
    )
    parser.add_argument(
        "-m", "--max",
        type=int,
        default=100,
        help="Maximum follows per session (default: 100)"
    )
    parser.add_argument(
        "-s", "--session",
        default="session.json",
        help="Session file path (default: session.json)"
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Simulate follows without actually following"
    )
    
    args = parser.parse_args()
    
    # Get file from args or prompt
    file_path = args.file
    if not file_path:
        file_path = input("Enter path to JSON file with handles: ").strip()
        if not file_path:
            print("No file provided. Exiting.")
            return
    
    if not Path(file_path).exists():
        print(f"File not found: {file_path}")
        sys.exit(1)
    
    try:
        follow_users(
            handles_file=file_path,
            delay=args.delay,
            max_per_session=args.max,
            session_file=args.session,
            dry_run=args.dry_run
        )
    except KeyboardInterrupt:
        print("\n\nFollow operation cancelled.")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
