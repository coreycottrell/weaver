#!/usr/bin/env python3
"""
Gentle Telegram - Rate-limited, backoff-aware Telegram API wrapper.

Created: 2025-12-30 (Night Watch)
Purpose: Prevent API temp bans through intelligent rate limiting.

Key Features:
1. Rate Limit State File - Track last API call, enforce minimum gaps
2. Exponential Backoff - On error, wait longer each time
3. Circuit Breaker - After N consecutive errors, pause entirely
4. Single-call validation - Check before EVERY API call

Usage:
    from gentle_telegram import GentleTelegram

    tg = GentleTelegram(bot_token)

    # Will automatically respect rate limits
    success, result = tg.send_message(chat_id, "Hello!")

    # Check if we're in cooldown
    if tg.in_cooldown():
        print(f"API cooling down, retry in {tg.cooldown_remaining()}s")
"""

import json
import time
import requests
from pathlib import Path
from datetime import datetime, timedelta
from typing import Tuple, Optional, Any

# Rate limit configuration
CONFIG = {
    "min_interval_seconds": 60,        # Minimum 60s between ANY API calls
    "backoff_base_seconds": 300,       # Start with 5 min on error
    "backoff_multiplier": 2,           # Double each time
    "backoff_max_seconds": 3600,       # Max 1 hour backoff
    "circuit_breaker_threshold": 3,    # After 3 consecutive errors, trip breaker
    "circuit_breaker_reset_seconds": 1800,  # 30 min cooldown when tripped
}

STATE_FILE = Path.home() / ".tg_rate_limit.json"


class GentleTelegram:
    """Rate-limited Telegram API client with exponential backoff."""

    def __init__(self, bot_token: str):
        self.bot_token = bot_token
        self.base_url = f"https://api.telegram.org/bot{bot_token}"
        self.state = self._load_state()

    def _load_state(self) -> dict:
        """Load rate limit state from file."""
        default_state = {
            "last_api_call": 0,
            "consecutive_errors": 0,
            "current_backoff": 0,
            "circuit_breaker_until": 0,
            "total_calls": 0,
            "total_errors": 0,
            "last_error": None,
        }

        if STATE_FILE.exists():
            try:
                with open(STATE_FILE, 'r') as f:
                    state = json.load(f)
                    # Merge with defaults for any missing keys
                    return {**default_state, **state}
            except Exception:
                pass

        return default_state

    def _save_state(self):
        """Save rate limit state to file."""
        try:
            with open(STATE_FILE, 'w') as f:
                json.dump(self.state, f, indent=2)
        except Exception as e:
            print(f"Warning: Could not save state: {e}")

    def in_cooldown(self) -> bool:
        """Check if we're in any cooldown period."""
        now = time.time()

        # Check circuit breaker
        if self.state["circuit_breaker_until"] > now:
            return True

        # Check minimum interval
        time_since_last = now - self.state["last_api_call"]
        if time_since_last < CONFIG["min_interval_seconds"]:
            return True

        # Check backoff period
        if self.state["current_backoff"] > 0:
            backoff_until = self.state["last_api_call"] + self.state["current_backoff"]
            if now < backoff_until:
                return True

        return False

    def cooldown_remaining(self) -> int:
        """Return seconds remaining in cooldown, or 0 if none."""
        now = time.time()

        # Check circuit breaker first (highest priority)
        if self.state["circuit_breaker_until"] > now:
            return int(self.state["circuit_breaker_until"] - now)

        # Check backoff
        if self.state["current_backoff"] > 0:
            backoff_until = self.state["last_api_call"] + self.state["current_backoff"]
            if now < backoff_until:
                return int(backoff_until - now)

        # Check minimum interval
        time_since_last = now - self.state["last_api_call"]
        if time_since_last < CONFIG["min_interval_seconds"]:
            return int(CONFIG["min_interval_seconds"] - time_since_last)

        return 0

    def _record_success(self):
        """Record a successful API call."""
        self.state["last_api_call"] = time.time()
        self.state["consecutive_errors"] = 0
        self.state["current_backoff"] = 0
        self.state["total_calls"] += 1
        self._save_state()

    def _record_error(self, error_msg: str):
        """Record an API error and update backoff."""
        now = time.time()
        self.state["last_api_call"] = now
        self.state["consecutive_errors"] += 1
        self.state["total_errors"] += 1
        self.state["last_error"] = {
            "time": datetime.now().isoformat(),
            "message": error_msg
        }

        # Calculate exponential backoff
        if self.state["current_backoff"] == 0:
            self.state["current_backoff"] = CONFIG["backoff_base_seconds"]
        else:
            self.state["current_backoff"] = min(
                self.state["current_backoff"] * CONFIG["backoff_multiplier"],
                CONFIG["backoff_max_seconds"]
            )

        # Check circuit breaker
        if self.state["consecutive_errors"] >= CONFIG["circuit_breaker_threshold"]:
            self.state["circuit_breaker_until"] = now + CONFIG["circuit_breaker_reset_seconds"]
            print(f"CIRCUIT BREAKER TRIPPED: {self.state['consecutive_errors']} consecutive errors")
            print(f"API calls paused until {datetime.fromtimestamp(self.state['circuit_breaker_until'])}")

        self._save_state()

    def _make_request(self, method: str, endpoint: str, **kwargs) -> Tuple[bool, Any]:
        """Make a rate-limited API request."""
        # Check cooldown FIRST
        if self.in_cooldown():
            remaining = self.cooldown_remaining()
            return False, {
                "error": "rate_limited",
                "message": f"In cooldown, retry in {remaining}s",
                "retry_after": remaining
            }

        url = f"{self.base_url}/{endpoint}"

        try:
            if method.upper() == "GET":
                response = requests.get(url, timeout=15, **kwargs)
            else:
                response = requests.post(url, timeout=15, **kwargs)

            data = response.json()

            # Check for Telegram API errors
            if not data.get("ok"):
                error_code = data.get("error_code", 0)
                error_desc = data.get("description", "Unknown error")

                # Special handling for rate limit errors (429)
                if error_code == 429:
                    retry_after = data.get("parameters", {}).get("retry_after", 300)
                    self.state["current_backoff"] = max(
                        self.state["current_backoff"],
                        retry_after
                    )
                    error_desc = f"Rate limited by Telegram (retry_after: {retry_after}s)"

                self._record_error(error_desc)
                return False, {"error": error_code, "message": error_desc}

            # Success!
            self._record_success()
            return True, data.get("result")

        except requests.exceptions.Timeout:
            self._record_error("Request timeout (>15s)")
            return False, {"error": "timeout", "message": "Request timed out"}
        except requests.exceptions.ConnectionError as e:
            self._record_error(f"Connection error: {e}")
            return False, {"error": "connection", "message": str(e)}
        except Exception as e:
            self._record_error(f"Unexpected error: {e}")
            return False, {"error": "unknown", "message": str(e)}

    # ===== Public API Methods =====

    def get_me(self) -> Tuple[bool, Any]:
        """Get bot info (health check)."""
        return self._make_request("GET", "getMe")

    def send_message(self, chat_id: int, text: str, **kwargs) -> Tuple[bool, Any]:
        """Send a text message."""
        payload = {"chat_id": chat_id, "text": text, **kwargs}
        return self._make_request("POST", "sendMessage", json=payload)

    def get_updates(self, offset: int = None, limit: int = 10, timeout: int = 0) -> Tuple[bool, Any]:
        """Get updates (incoming messages). Use sparingly!"""
        params = {"limit": limit, "timeout": timeout}
        if offset:
            params["offset"] = offset
        return self._make_request("GET", "getUpdates", params=params)

    def status(self) -> dict:
        """Get current rate limiter status."""
        now = time.time()
        return {
            "in_cooldown": self.in_cooldown(),
            "cooldown_remaining_seconds": self.cooldown_remaining(),
            "consecutive_errors": self.state["consecutive_errors"],
            "current_backoff_seconds": self.state["current_backoff"],
            "circuit_breaker_active": self.state["circuit_breaker_until"] > now,
            "total_calls": self.state["total_calls"],
            "total_errors": self.state["total_errors"],
            "last_error": self.state["last_error"],
            "last_api_call": datetime.fromtimestamp(self.state["last_api_call"]).isoformat() if self.state["last_api_call"] else None
        }


# ===== CLI Interface =====

def main():
    """CLI for testing and status checks."""
    import sys
    import os

    # Load bot token from config
    config_file = Path(__file__).parent.parent.parent / "config" / "telegram_config.json"
    if not config_file.exists():
        print(f"Config not found: {config_file}")
        sys.exit(1)

    with open(config_file) as f:
        config = json.load(f)

    bot_token = config.get("bot_token")
    if not bot_token:
        print("No bot_token in config")
        sys.exit(1)

    tg = GentleTelegram(bot_token)

    if len(sys.argv) < 2:
        print("Usage:")
        print("  python gentle_telegram.py status     - Show rate limiter status")
        print("  python gentle_telegram.py test       - Test API (getMe)")
        print("  python gentle_telegram.py reset      - Reset all cooldowns")
        print("  python gentle_telegram.py send TEXT  - Send message to first user")
        sys.exit(0)

    cmd = sys.argv[1]

    if cmd == "status":
        status = tg.status()
        print("\n=== Gentle Telegram Status ===")
        print(f"In cooldown: {status['in_cooldown']}")
        if status['in_cooldown']:
            print(f"  Remaining: {status['cooldown_remaining_seconds']}s")
        print(f"Consecutive errors: {status['consecutive_errors']}")
        print(f"Current backoff: {status['current_backoff_seconds']}s")
        print(f"Circuit breaker: {'ACTIVE' if status['circuit_breaker_active'] else 'inactive'}")
        print(f"Total calls: {status['total_calls']}")
        print(f"Total errors: {status['total_errors']}")
        if status['last_error']:
            print(f"Last error: {status['last_error']['message']} ({status['last_error']['time']})")
        print(f"Last API call: {status['last_api_call']}")

    elif cmd == "test":
        print("Testing API (getMe)...")
        success, result = tg.get_me()
        if success:
            print(f"SUCCESS: @{result.get('username')} ({result.get('first_name')})")
        else:
            print(f"FAILED: {result}")

    elif cmd == "reset":
        tg.state = {
            "last_api_call": 0,
            "consecutive_errors": 0,
            "current_backoff": 0,
            "circuit_breaker_until": 0,
            "total_calls": tg.state.get("total_calls", 0),
            "total_errors": tg.state.get("total_errors", 0),
            "last_error": None,
        }
        tg._save_state()
        print("Rate limiter reset. Cooldowns cleared.")

    elif cmd == "send" and len(sys.argv) > 2:
        text = " ".join(sys.argv[2:])
        user_id = int(list(config.get("authorized_users", {}).keys())[0])
        print(f"Sending to {user_id}: {text[:50]}...")
        success, result = tg.send_message(user_id, text)
        if success:
            print(f"SUCCESS: Message ID {result.get('message_id')}")
        else:
            print(f"FAILED: {result}")

    else:
        print(f"Unknown command: {cmd}")
        sys.exit(1)


if __name__ == "__main__":
    main()
