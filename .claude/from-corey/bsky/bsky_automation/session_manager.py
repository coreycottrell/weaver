"""
Bluesky Session Manager - Handles authentication with proper session persistence
This avoids hitting the strict login rate limits (10/day per IP)

Updated for 2025 using the official atproto Python SDK
"""

import os
import json
from pathlib import Path
from typing import Optional, Callable
from datetime import datetime
from dotenv import load_dotenv

try:
    from atproto import Client, Session, SessionEvent
except ImportError:
    raise ImportError("Please install the atproto SDK: pip install atproto")

# Load environment variables
load_dotenv()


class BlueskySessionManager:
    """
    Manages Bluesky authentication with proper session persistence.
    
    CRITICAL: Bluesky has strict login rate limits (10/day per IP).
    This class saves session strings to avoid re-authenticating.
    """
    
    def __init__(
        self,
        session_file: str = "session.json",
        username: Optional[str] = None,
        password: Optional[str] = None
    ):
        self.session_file = Path(session_file)
        self.username = username or os.getenv("BSKY_USERNAME") or os.getenv("BLUESKY_HANDLE")
        self.password = password or os.getenv("BSKY_PASSWORD") or os.getenv("BLUESKY_PASSWORD")
        self.client: Optional[Client] = None
        self._session_data: dict = {}
        
        if not self.username or not self.password:
            raise ValueError(
                "Missing credentials. Set BSKY_USERNAME and BSKY_PASSWORD in .env file "
                "or pass them as parameters."
            )
    
    def _load_session(self) -> Optional[str]:
        """Load session string from file if it exists."""
        try:
            if self.session_file.exists():
                with open(self.session_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self._session_data = data
                    return data.get('session_string')
        except (json.JSONDecodeError, IOError) as e:
            print(f"[WARNING] Could not load session: {e}")
        return None
    
    def _save_session(self, session_string: str) -> None:
        """Save session string to file."""
        try:
            self._session_data = {
                'session_string': session_string,
                'username': self.username,
                'updated_at': datetime.utcnow().isoformat() + 'Z'
            }
            with open(self.session_file, 'w', encoding='utf-8') as f:
                json.dump(self._session_data, f, indent=2)
            print(f"[INFO] Session saved to {self.session_file}")
        except IOError as e:
            print(f"[WARNING] Could not save session: {e}")
    
    def _on_session_change(self, event: SessionEvent, session: Session) -> None:
        """Callback for session changes - saves session on create/refresh."""
        print(f"[SESSION] Event: {event.name}")
        if event in (SessionEvent.CREATE, SessionEvent.REFRESH):
            session_string = session.export()
            self._save_session(session_string)
    
    def get_client(self) -> Client:
        """
        Get an authenticated Bluesky client.
        
        This method:
        1. Tries to reuse an existing session from file
        2. Falls back to fresh login if session is invalid
        3. Automatically saves session changes
        
        Returns:
            Client: Authenticated atproto Client
        """
        if self.client:
            return self.client
        
        self.client = Client()
        self.client.on_session_change(self._on_session_change)
        
        # Try to reuse existing session
        session_string = self._load_session()
        if session_string:
            try:
                print("[INFO] Attempting to reuse existing session...")
                self.client.login(session_string=session_string)
                print(f"[SUCCESS] Logged in as {self.client.me.handle}")
                return self.client
            except Exception as e:
                print(f"[WARNING] Session reuse failed: {e}")
                print("[INFO] Attempting fresh login...")
        
        # Fresh login (uses one of your daily login quota!)
        try:
            print(f"[INFO] Logging in as {self.username}...")
            self.client.login(self.username, self.password)
            print(f"[SUCCESS] Logged in as {self.client.me.handle}")
            return self.client
        except Exception as e:
            print(f"[ERROR] Login failed: {e}")
            raise
    
    @property
    def did(self) -> str:
        """Get the DID of the logged-in user."""
        if not self.client or not self.client.me:
            raise RuntimeError("Not logged in. Call get_client() first.")
        return self.client.me.did
    
    @property
    def handle(self) -> str:
        """Get the handle of the logged-in user."""
        if not self.client or not self.client.me:
            raise RuntimeError("Not logged in. Call get_client() first.")
        return self.client.me.handle


def get_client(session_file: str = "session.json") -> Client:
    """
    Convenience function to get an authenticated client.
    
    Args:
        session_file: Path to session storage file
        
    Returns:
        Client: Authenticated atproto Client
    """
    manager = BlueskySessionManager(session_file=session_file)
    return manager.get_client()


if __name__ == "__main__":
    # Test the session manager
    print("Testing Bluesky Session Manager...")
    print("=" * 50)
    
    try:
        manager = BlueskySessionManager()
        client = manager.get_client()
        
        # Get profile info
        profile = client.app.bsky.actor.get_profile({'actor': manager.handle})
        print(f"\n✅ Successfully authenticated!")
        print(f"   Handle: @{profile.handle}")
        print(f"   Display Name: {profile.display_name}")
        print(f"   Followers: {profile.followers_count}")
        print(f"   Following: {profile.follows_count}")
        print(f"   Posts: {profile.posts_count}")
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("\nMake sure you have a .env file with:")
        print("   BSKY_USERNAME=your.handle.bsky.social")
        print("   BSKY_PASSWORD=your-app-password")
