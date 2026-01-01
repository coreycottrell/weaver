#!/usr/bin/env python3
"""
Send file to Telegram using curl subprocess.

This script bypasses Python's DNS resolution issues by using curl directly,
which has more robust DNS handling, especially in WSL environments.

Usage:
    python3 send_telegram_file_curl.py <user_id> <file_path> [caption]

Example:
    python3 send_telegram_file_curl.py 437939400 /path/to/doc.md "Session summary"

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


def send_file_via_curl(bot_token: str, user_id: int, file_path: str, caption: str = None) -> bool:
    """
    Send file to Telegram using curl subprocess.

    Args:
        bot_token: Telegram Bot API token
        user_id: Telegram user ID
        file_path: Path to file to send
        caption: Optional caption (max 1024 chars)

    Returns:
        True if successful, False otherwise
    """
    file_path_obj = Path(file_path)

    # Validate file exists
    if not file_path_obj.exists():
        print(f"ERROR: File not found: {file_path}", file=sys.stderr)
        return False

    # Check file size (50MB limit)
    file_size = file_path_obj.stat().st_size
    max_size = 50 * 1024 * 1024
    if file_size > max_size:
        print(f"ERROR: File too large ({file_size / 1024 / 1024:.1f}MB). Limit: 50MB", file=sys.stderr)
        return False

    # Build curl command
    url = f"https://api.telegram.org/bot{bot_token}/sendDocument"

    curl_cmd = [
        "curl",
        "-s",  # Silent mode
        "-S",  # Show errors
        "-X", "POST",
        url,
        "-F", f"chat_id={user_id}",
        "-F", f"document=@{file_path}",
    ]

    # Add caption if provided
    if caption:
        if len(caption) > 1024:
            print("WARNING: Caption truncated to 1024 chars", file=sys.stderr)
            caption = caption[:1021] + "..."
        curl_cmd.extend(["-F", f"caption={caption}"])

    try:
        # Execute curl
        result = subprocess.run(
            curl_cmd,
            capture_output=True,
            text=True,
            timeout=60  # 60 second timeout for file uploads
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
            print(f"File sent successfully to user {user_id}")
            print(f"  File: {file_path_obj.name} ({file_size / 1024:.1f} KB)")
            if caption:
                print(f"  Caption: {caption[:50]}{'...' if len(caption) > 50 else ''}")
            return True
        else:
            error_code = response.get("error_code", "unknown")
            error_desc = response.get("description", "unknown error")
            print(f"ERROR: Telegram API error {error_code}: {error_desc}", file=sys.stderr)
            return False

    except subprocess.TimeoutExpired:
        print("ERROR: curl timed out after 60 seconds", file=sys.stderr)
        return False
    except FileNotFoundError:
        print("ERROR: curl not found. Install curl first.", file=sys.stderr)
        return False
    except Exception as e:
        print(f"ERROR: Unexpected error: {e}", file=sys.stderr)
        return False


def main():
    if len(sys.argv) < 3:
        print("Usage: python3 send_telegram_file_curl.py <user_id> <file_path> [caption]", file=sys.stderr)
        print("", file=sys.stderr)
        print("Examples:", file=sys.stderr)
        print("  python3 send_telegram_file_curl.py 437939400 /path/to/doc.pdf", file=sys.stderr)
        print("  python3 send_telegram_file_curl.py 437939400 /path/to/report.md 'Session summary'", file=sys.stderr)
        sys.exit(1)

    try:
        user_id = int(sys.argv[1])
    except ValueError:
        print(f"ERROR: Invalid user_id '{sys.argv[1]}' - must be an integer", file=sys.stderr)
        sys.exit(1)

    file_path = sys.argv[2]
    caption = sys.argv[3] if len(sys.argv) > 3 else None

    # Load bot token
    bot_token = load_bot_token()

    # Send file
    success = send_file_via_curl(bot_token, user_id, file_path, caption)

    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
