#!/usr/bin/env python3
"""
Send file attachments to Telegram users via Bot API.
FIXED VERSION: Uses working IP (149.154.175.50) to bypass DNS block.

Usage:
    python3 send_telegram_file_fixed.py <user_id> <file_path> [caption]

Example:
    python3 send_telegram_file_fixed.py 437939400 /path/to/doc.pdf "Documentation attached"

Features:
- Supports any file type (PDFs, docs, images, etc.)
- Optional caption (up to 1024 chars)
- Max file size: 50MB (Telegram Bot API limit)
- Auto-detects file type
- Comprehensive error handling
- FIXED: Uses alternate Telegram IP to bypass DNS issues

Author: tg-bridge agent
Created: 2025-12-30
Domain: Telegram infrastructure

DNS Workaround:
  The main Telegram IP (149.154.167.220) is blocked.
  This script uses alternate working IPs:
  - 149.154.175.50 (14.6ms)
  - 91.108.4.170 (115ms)
  - 91.108.56.130 (239ms)
"""

import json
import os
import sys
import requests
import urllib3.util.connection
from pathlib import Path

# Working Telegram IPs (api.telegram.org alternates)
WORKING_TELEGRAM_IPS = [
    "149.154.175.50",   # Best: 14.6ms
    "91.108.4.170",     # Backup: 115ms
    "91.108.56.130",    # Backup: 239ms
]

# Global override for DNS resolution
_dns_override = {}

def patched_create_connection(address, *args, **kwargs):
    """Create connection with DNS override."""
    from urllib3.util.connection import create_connection as orig_create
    host, port = address
    if host in _dns_override:
        host = _dns_override[host]
    return orig_create((host, port), *args, **kwargs)


def load_config():
    """Load Telegram configuration from config file or environment."""
    # First check environment variable (preferred)
    bot_token = os.environ.get('TELEGRAM_BOT_TOKEN')
    if bot_token and not bot_token.startswith('${'):
        print("Using bot token from TELEGRAM_BOT_TOKEN environment variable", file=sys.stderr)
        return bot_token

    # Try multiple config file locations
    config_paths = [
        "/home/corey/projects/AI-CIV/WEAVER/config/telegram_config.json",
        "/home/corey/projects/AI-CIV/grow_openai/config/telegram_config.json",
        Path.home() / ".telegram_bot_token",  # Simple file fallback
    ]

    for config_path in config_paths:
        config_path = Path(config_path)
        if config_path.exists():
            try:
                if config_path.suffix == '.json':
                    with open(config_path, 'r') as f:
                        config = json.load(f)
                    bot_token = config.get('bot_token')
                else:
                    # Plain text file with just token
                    bot_token = config_path.read_text().strip()

                if bot_token and not bot_token.startswith('${') and bot_token != 'YOUR_BOT_TOKEN_FROM_BOTFATHER':
                    print(f"Using bot token from {config_path}", file=sys.stderr)
                    return bot_token
            except (json.JSONDecodeError, IOError) as e:
                print(f"Warning: Could not read {config_path}: {e}", file=sys.stderr)
                continue

    print("ERROR: TELEGRAM_BOT_TOKEN not set in environment and no valid config found", file=sys.stderr)
    print("  Tried:", file=sys.stderr)
    for p in config_paths:
        print(f"    - {p}", file=sys.stderr)
    return None


def send_telegram_file(bot_token: str, user_id: int, file_path: str, caption: str = None) -> bool:
    """
    Send a file to a Telegram user via Bot API sendDocument method.
    Uses working Telegram IP to bypass DNS block.

    Args:
        bot_token: Telegram Bot API token
        user_id: Telegram user ID to send to
        file_path: Absolute path to file to send
        caption: Optional caption (max 1024 chars)

    Returns:
        True if sent successfully, False otherwise
    """
    global _dns_override

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

    # Prepare request data
    data = {'chat_id': user_id}

    if caption:
        # Telegram caption limit: 1024 chars
        if len(caption) > 1024:
            print("WARNING: Caption truncated to 1024 chars", file=sys.stderr)
            caption = caption[:1021] + "..."
        data['caption'] = caption

    # Use the normal URL
    url = f"https://api.telegram.org/bot{bot_token}/sendDocument"

    # Save original create_connection
    original_create_connection = urllib3.util.connection.create_connection

    # Try each working IP until success
    for telegram_ip in WORKING_TELEGRAM_IPS:
        print(f"Attempting connection via {telegram_ip}...", file=sys.stderr)

        # Set DNS override
        _dns_override['api.telegram.org'] = telegram_ip

        # Apply patch
        urllib3.util.connection.create_connection = patched_create_connection

        try:
            with open(file_path, 'rb') as f:
                files = {'document': f}
                response = requests.post(
                    url,
                    data=data,
                    files=files,
                    timeout=60,  # Longer timeout for file uploads
                )

            response.raise_for_status()
            result = response.json()

            if result.get('ok'):
                print(f"SUCCESS via {telegram_ip}")
                print(f"File sent successfully to user {user_id}")
                print(f"  File: {file_path_obj.name} ({file_size / 1024:.1f} KB)")
                if caption:
                    print(f"  Caption: {caption[:50]}{'...' if len(caption) > 50 else ''}")
                # Restore original
                urllib3.util.connection.create_connection = original_create_connection
                return True
            else:
                print(f"ERROR: Telegram API returned ok=false: {result}", file=sys.stderr)
                continue

        except requests.exceptions.SSLError as e:
            print(f"SSL Error with {telegram_ip}: {e}", file=sys.stderr)
            continue

        except requests.exceptions.HTTPError as e:
            if hasattr(e, 'response') and e.response is not None:
                if e.response.status_code == 400:
                    print(f"ERROR: Bad Request (400) - File may be invalid or unsupported", file=sys.stderr)
                    print(f"  Response: {e.response.text}", file=sys.stderr)
                else:
                    print(f"ERROR: HTTP {e.response.status_code}: {e}", file=sys.stderr)
            else:
                print(f"ERROR: HTTP error: {e}", file=sys.stderr)
            continue

        except requests.exceptions.Timeout:
            print(f"Timeout with {telegram_ip}, trying next...", file=sys.stderr)
            continue

        except requests.exceptions.ConnectionError as e:
            print(f"Connection error with {telegram_ip}: {e}", file=sys.stderr)
            continue

        except requests.exceptions.RequestException as e:
            print(f"Network error with {telegram_ip}: {e}", file=sys.stderr)
            continue

        except IOError as e:
            print(f"ERROR: Could not read file: {e}", file=sys.stderr)
            urllib3.util.connection.create_connection = original_create_connection
            return False

        except Exception as e:
            print(f"ERROR with {telegram_ip}: {e}", file=sys.stderr)
            continue

    # Restore original
    urllib3.util.connection.create_connection = original_create_connection
    print("ERROR: All Telegram IPs failed", file=sys.stderr)
    return False


def main():
    if len(sys.argv) < 3:
        print("Usage: python3 send_telegram_file_fixed.py <user_id> <file_path> [caption]", file=sys.stderr)
        print("", file=sys.stderr)
        print("Examples:", file=sys.stderr)
        print("  python3 send_telegram_file_fixed.py 437939400 /path/to/doc.pdf", file=sys.stderr)
        print("  python3 send_telegram_file_fixed.py 437939400 /path/to/report.md 'Session summary'", file=sys.stderr)
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
        print(f"Failed to send file to user {user_id}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
