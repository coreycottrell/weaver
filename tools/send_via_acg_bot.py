#!/usr/bin/env python3
"""
Send message via A-C-Gee's bot (which Corey has a chat with).

This bypasses WEAVER's config and uses A-C-Gee's working bot token.
Use this until WEAVER's bot is properly initialized.

Usage:
    python3 tools/send_via_acg_bot.py <user_id> <message>
    python3 tools/send_via_acg_bot.py 437939400 "Test message"
"""

import sys
import requests

# A-C-Gee's working bot token
BOT_TOKEN = "8388754468:AAEROakhpBPR1KNHjravHx3CIMH-FIyIWEc"

def send_message(user_id: int, message: str) -> bool:
    """Send plain text message via A-C-Gee's bot."""
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

    payload = {
        "chat_id": user_id,
        "text": message
    }

    try:
        response = requests.post(url, json=payload, timeout=10)
        response.raise_for_status()
        print(f"SUCCESS: Message sent to {user_id}")
        return True
    except requests.exceptions.HTTPError as e:
        print(f"ERROR: HTTP {e.response.status_code}: {e.response.text}", file=sys.stderr)
        return False
    except Exception as e:
        print(f"ERROR: {e}", file=sys.stderr)
        return False

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python3 send_via_acg_bot.py <user_id> <message>", file=sys.stderr)
        sys.exit(1)

    user_id = int(sys.argv[1])
    message = sys.argv[2]

    success = send_message(user_id, message)
    sys.exit(0 if success else 1)
