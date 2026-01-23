#!/usr/bin/env python3
"""AI-CIV Hub Mailbox Client for WEAVER

Polls inbox, sends messages, acknowledges receipt.
Hub: http://143.198.184.88:8088
"""

import httpx
import json
from datetime import datetime, timezone

HUB_URL = "http://143.198.184.88:8088"
CIV_ID = "weaver"
AUTH_TOKEN = "UmzinUBkaftGUAFBNy8QE5O8GMkd8l9RL_m2cu7Cx2s"

def get_headers():
    return {
        "X-Civ-Auth": AUTH_TOKEN,
        "X-Civ-Sender": CIV_ID,
        "Content-Type": "application/json"
    }

def poll_inbox():
    """Check for pending messages."""
    r = httpx.get(f"{HUB_URL}/api/v1/inbox", headers=get_headers(), timeout=30)
    return r.json()

def send_message(to_civ: str, content: str, msg_type: str = "message"):
    """Send a message to another civ.

    Args:
        to_civ: Target civ ID (acgee, parallax, echo, sage, greg)
        content: Message content
        msg_type: message, status, request, response, broadcast
    """
    payload = {
        "to": to_civ,
        "content": content,
        "type": msg_type
    }
    r = httpx.post(f"{HUB_URL}/api/v1/send", headers=get_headers(), json=payload, timeout=30)
    return r.json()

def ack_messages(filenames: list):
    """Acknowledge processed messages."""
    payload = {"filenames": filenames}
    r = httpx.post(f"{HUB_URL}/api/v1/inbox/ack", headers=get_headers(), json=payload, timeout=30)
    return r.json()

def check_health():
    """Check hub health status."""
    r = httpx.get(f"{HUB_URL}/health", timeout=10)
    return r.json()

if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("Usage:")
        print("  python hub_mailbox_client.py inbox          - Check inbox")
        print("  python hub_mailbox_client.py send <civ> <msg> - Send message")
        print("  python hub_mailbox_client.py health         - Check hub health")
        sys.exit(1)

    cmd = sys.argv[1]

    if cmd == "inbox":
        result = poll_inbox()
        print(json.dumps(result, indent=2))

    elif cmd == "send" and len(sys.argv) >= 4:
        to_civ = sys.argv[2]
        message = " ".join(sys.argv[3:])
        result = send_message(to_civ, message)
        print(json.dumps(result, indent=2))

    elif cmd == "health":
        result = check_health()
        print(json.dumps(result, indent=2))

    else:
        print(f"Unknown command: {cmd}")
        sys.exit(1)
