#!/usr/bin/env python3
"""
Send plain text message to Telegram using curl subprocess.

This script bypasses Python's DNS resolution issues by using curl directly,
which has more robust DNS handling, especially in WSL environments.

Usage:
    python3 send_telegram_curl.py <user_id> <message>

Example:
    python3 send_telegram_curl.py 437939400 "Hello from WEAVER!"

Author: tg-bridge agent
Created: 2025-12-30
"""

import json
import os
import subprocess
import sys
from pathlib import Path


def load_bot_token() -> str:
    """Load Telegram bot token from config or environment."""
    config_path = Path("/home/corey/projects/AI-CIV/WEAVER/config/telegram_config.json")

    # Try environment first
    token = os.environ.get('TELEGRAM_BOT_TOKEN')
    if token and not token.startswith('${'):
        return token

    # Try config file
    try:
        with open(config_path, 'r') as f:
            config = json.load(f)
        token = config.get('bot_token')
        if token and not token.startswith('${'):
            return token
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"ERROR: Could not load config: {e}", file=sys.stderr)

    print("ERROR: TELEGRAM_BOT_TOKEN not found in environment or config", file=sys.stderr)
    sys.exit(1)


def send_message_via_curl(bot_token: str, user_id: int, message: str) -> bool:
    """
    Send message to Telegram using curl subprocess.

    Args:
        bot_token: Telegram Bot API token
        user_id: Telegram user ID
        message: Message text to send

    Returns:
        True if successful, False otherwise
    """
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"

    # Telegram message limit
    MAX_LENGTH = 4000

    # Handle long messages by chunking
    if len(message) > MAX_LENGTH:
        chunks = []
        current_chunk = ""

        for line in message.split('\n'):
            # Handle lines longer than MAX_LENGTH
            while len(line) > MAX_LENGTH - 50:
                break_point = line[:MAX_LENGTH - 50].rfind(' ')
                if break_point == -1:
                    break_point = MAX_LENGTH - 50
                if current_chunk:
                    chunks.append(current_chunk)
                chunks.append(line[:break_point])
                line = line[break_point:].lstrip()
                current_chunk = ""

            if len(current_chunk) + len(line) + 1 > MAX_LENGTH:
                if current_chunk:
                    chunks.append(current_chunk)
                current_chunk = line
            else:
                if current_chunk:
                    current_chunk += '\n' + line
                else:
                    current_chunk = line

        if current_chunk:
            chunks.append(current_chunk)

        print(f"Message split into {len(chunks)} chunks", file=sys.stderr)

        # Send all chunks
        import time
        for i, chunk in enumerate(chunks):
            if i > 0:
                chunk = f"({i+1}/{len(chunks)})\n\n{chunk}"
                time.sleep(0.5)  # Rate limit

            success = _send_single_message(url, user_id, chunk)
            if not success:
                print(f"ERROR: Failed to send chunk {i+1}", file=sys.stderr)
                return False

        return True
    else:
        return _send_single_message(url, user_id, message)


def _send_single_message(url: str, user_id: int, message: str) -> bool:
    """Send a single message via curl."""
    # Build JSON payload
    payload = json.dumps({
        "chat_id": user_id,
        "text": message
    })

    curl_cmd = [
        "curl",
        "-s",  # Silent mode
        "-S",  # Show errors
        "-X", "POST",
        url,
        "-H", "Content-Type: application/json",
        "-d", payload
    ]

    try:
        result = subprocess.run(
            curl_cmd,
            capture_output=True,
            text=True,
            timeout=30
        )

        if result.returncode != 0:
            print(f"ERROR: curl failed with code {result.returncode}", file=sys.stderr)
            print(f"stderr: {result.stderr}", file=sys.stderr)
            return False

        # Parse response
        try:
            response = json.loads(result.stdout)
        except json.JSONDecodeError:
            print(f"ERROR: Invalid JSON response: {result.stdout[:200]}", file=sys.stderr)
            return False

        if response.get("ok"):
            return True
        else:
            error_code = response.get("error_code", "unknown")
            error_desc = response.get("description", "unknown error")
            print(f"ERROR: Telegram API error {error_code}: {error_desc}", file=sys.stderr)
            return False

    except subprocess.TimeoutExpired:
        print("ERROR: curl timed out after 30 seconds", file=sys.stderr)
        return False
    except FileNotFoundError:
        print("ERROR: curl not found. Install curl first.", file=sys.stderr)
        return False
    except Exception as e:
        print(f"ERROR: Unexpected error: {e}", file=sys.stderr)
        return False


def main():
    if len(sys.argv) < 3:
        print("Usage: python3 send_telegram_curl.py <user_id> <message>", file=sys.stderr)
        print("", file=sys.stderr)
        print("Examples:", file=sys.stderr)
        print("  python3 send_telegram_curl.py 437939400 'Hello from WEAVER!'", file=sys.stderr)
        sys.exit(1)

    try:
        user_id = int(sys.argv[1])
    except ValueError:
        print(f"ERROR: Invalid user_id '{sys.argv[1]}' - must be an integer", file=sys.stderr)
        sys.exit(1)

    message = sys.argv[2]

    # Load bot token
    bot_token = load_bot_token()

    # Send message
    success = send_message_via_curl(bot_token, user_id, message)

    if success:
        print(f"Message sent to user {user_id}")
    else:
        print(f"Failed to send message to user {user_id}", file=sys.stderr)

    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
