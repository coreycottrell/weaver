#!/usr/bin/env python3
"""
Send file attachments to Telegram users via Bot API.

Usage:
    python3 send_telegram_file.py <user_id> <file_path> [caption]

Example:
    python3 send_telegram_file.py 437939400 /path/to/doc.pdf "Documentation attached"

Features:
- Supports any file type (PDFs, docs, images, etc.)
- Optional caption (up to 1024 chars)
- Max file size: 50MB (Telegram Bot API limit)
- Auto-detects file type
- Comprehensive error handling

Author: tg-bridge agent
Created: 2025-10-29
Domain: Telegram infrastructure
"""

import json
import os
import sys
import requests
from pathlib import Path


def load_config():
    """Load Telegram configuration from config file."""
    config_path = "/home/user/weaver/config/telegram_config.json"

    try:
        with open(config_path, 'r') as f:
            config = json.load(f)

        bot_token = os.environ.get('TELEGRAM_BOT_TOKEN') or config.get('bot_token')
        if not bot_token or bot_token.startswith('${'):
            print("ERROR: TELEGRAM_BOT_TOKEN not set in environment", file=sys.stderr)
            return None

        return bot_token
    except FileNotFoundError:
        print(f"ERROR: Config file not found: {config_path}", file=sys.stderr)
        return None
    except json.JSONDecodeError as e:
        print(f"ERROR: Invalid JSON in config file: {e}", file=sys.stderr)
        return None


def send_telegram_file(bot_token: str, user_id: int, file_path: str, caption: str = None) -> bool:
    """
    Send a file to a Telegram user via Bot API sendDocument method.

    Args:
        bot_token: Telegram Bot API token
        user_id: Telegram user ID to send to
        file_path: Absolute path to file to send
        caption: Optional caption (max 1024 chars)

    Returns:
        True if sent successfully, False otherwise
    """
    url = f"https://api.telegram.org/bot{bot_token}/sendDocument"

    # Validate file exists and size
    file_path_obj = Path(file_path)
    if not file_path_obj.exists():
        print(f"ERROR: File not found: {file_path}", file=sys.stderr)
        return False

    file_size = file_path_obj.stat().st_size
    max_size = 50 * 1024 * 1024  # 50MB Telegram limit

    if file_size > max_size:
        print(f"ERROR: File too large ({file_size / 1024 / 1024:.1f}MB). Telegram limit: 50MB", file=sys.stderr)
        return False

    # Prepare request
    data = {'chat_id': user_id}

    if caption:
        # Telegram caption limit: 1024 chars
        if len(caption) > 1024:
            print("WARNING: Caption truncated to 1024 chars", file=sys.stderr)
            caption = caption[:1021] + "..."
        data['caption'] = caption

    try:
        with open(file_path, 'rb') as f:
            files = {'document': f}
            response = requests.post(url, data=data, files=files, timeout=30)

        response.raise_for_status()
        result = response.json()

        if result.get('ok'):
            print(f"✓ File sent successfully to user {user_id}")
            print(f"  File: {file_path_obj.name} ({file_size / 1024:.1f} KB)")
            if caption:
                print(f"  Caption: {caption[:50]}{'...' if len(caption) > 50 else ''}")
            return True
        else:
            print(f"ERROR: Telegram API returned ok=false: {result}", file=sys.stderr)
            return False

    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 400:
            print(f"ERROR: Bad Request (400) - File may be invalid or unsupported", file=sys.stderr)
            print(f"  Response: {e.response.text}", file=sys.stderr)
        else:
            print(f"ERROR: HTTP {e.response.status_code}: {e}", file=sys.stderr)
        return False

    except requests.exceptions.Timeout:
        print("ERROR: Request timed out after 30 seconds", file=sys.stderr)
        return False

    except requests.exceptions.RequestException as e:
        print(f"ERROR: Network error: {e}", file=sys.stderr)
        return False

    except IOError as e:
        print(f"ERROR: Could not read file: {e}", file=sys.stderr)
        return False

    except Exception as e:
        print(f"ERROR: Unexpected error: {e}", file=sys.stderr)
        return False


def main():
    if len(sys.argv) < 3:
        print("Usage: python3 send_telegram_file.py <user_id> <file_path> [caption]", file=sys.stderr)
        print("", file=sys.stderr)
        print("Examples:", file=sys.stderr)
        print("  python3 send_telegram_file.py 437939400 /path/to/doc.pdf", file=sys.stderr)
        print("  python3 send_telegram_file.py 437939400 /path/to/report.md 'Session summary'", file=sys.stderr)
        sys.exit(1)

    try:
        user_id = int(sys.argv[1])
    except ValueError:
        print(f"ERROR: Invalid user_id '{sys.argv[1]}' - must be an integer", file=sys.stderr)
        sys.exit(1)

    file_path = sys.argv[2]
    caption = sys.argv[3] if len(sys.argv) > 3 else None

    # Load bot token
    bot_token = load_config()
    if not bot_token:
        sys.exit(1)

    # Send file
    success = send_telegram_file(bot_token, user_id, file_path, caption)

    if not success:
        print(f"✗ Failed to send file to user {user_id}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
