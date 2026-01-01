#!/usr/bin/env python3
"""
Send file attachments to Telegram users via Bot API.
V2: Uses raw http.client to bypass DNS block entirely (no urllib3 patching).

Usage:
    python3 send_telegram_file_v2.py <user_id> <file_path> [caption]

DNS Workaround:
  The main Telegram IP (149.154.167.220) is blocked.
  This script connects directly to alternate working IPs using http.client.
"""

import json
import os
import sys
import ssl
import socket
import http.client
import mimetypes
from pathlib import Path

# Working Telegram IPs (api.telegram.org alternates)
WORKING_TELEGRAM_IPS = [
    "149.154.175.50",   # Best: 14.6ms
    "91.108.4.170",     # Backup: 115ms
    "91.108.56.130",    # Backup: 239ms
]

TELEGRAM_HOST = "api.telegram.org"


def load_config():
    """Load Telegram configuration from config file or environment."""
    bot_token = os.environ.get('TELEGRAM_BOT_TOKEN')
    if bot_token and not bot_token.startswith('${'):
        return bot_token

    config_paths = [
        "/home/corey/projects/AI-CIV/WEAVER/config/telegram_config.json",
        "/home/corey/projects/AI-CIV/grow_openai/config/telegram_config.json",
    ]

    for config_path in config_paths:
        config_path = Path(config_path)
        if config_path.exists():
            try:
                with open(config_path, 'r') as f:
                    config = json.load(f)
                bot_token = config.get('bot_token')
                if bot_token and not bot_token.startswith('${'):
                    return bot_token
            except:
                continue

    return None


def send_file_via_ip(ip: str, bot_token: str, user_id: int, file_path: str, caption: str = None) -> dict:
    """Send file using direct IP connection with http.client."""

    # Create SSL context with SNI support
    context = ssl.create_default_context()

    # Create raw socket connection to IP
    sock = socket.create_connection((ip, 443), timeout=60)

    # Wrap with SSL, using proper hostname for SNI/cert validation
    ssl_sock = context.wrap_socket(sock, server_hostname=TELEGRAM_HOST)

    # Create HTTP connection using our SSL socket
    conn = http.client.HTTPSConnection(TELEGRAM_HOST, context=context)
    conn.sock = ssl_sock

    # Read file
    with open(file_path, 'rb') as f:
        file_data = f.read()

    filename = os.path.basename(file_path)
    mime_type = mimetypes.guess_type(file_path)[0] or 'application/octet-stream'

    # Build multipart form data
    boundary = '----TelegramBotAPI7MA4YWxkTrZu0gW'

    body_parts = []

    # chat_id field
    body_parts.append(f'--{boundary}'.encode())
    body_parts.append(b'Content-Disposition: form-data; name="chat_id"')
    body_parts.append(b'')
    body_parts.append(str(user_id).encode())

    # caption field (if provided)
    if caption:
        body_parts.append(f'--{boundary}'.encode())
        body_parts.append(b'Content-Disposition: form-data; name="caption"')
        body_parts.append(b'')
        body_parts.append(caption.encode('utf-8'))

    # document field
    body_parts.append(f'--{boundary}'.encode())
    body_parts.append(f'Content-Disposition: form-data; name="document"; filename="{filename}"'.encode())
    body_parts.append(f'Content-Type: {mime_type}'.encode())
    body_parts.append(b'')
    body_parts.append(file_data)

    # End boundary
    body_parts.append(f'--{boundary}--'.encode())
    body_parts.append(b'')

    body = b'\r\n'.join(body_parts)

    headers = {
        'Host': TELEGRAM_HOST,
        'Content-Type': f'multipart/form-data; boundary={boundary}',
        'Content-Length': str(len(body)),
        'Connection': 'close',
    }

    path = f'/bot{bot_token}/sendDocument'

    conn.request('POST', path, body=body, headers=headers)
    response = conn.getresponse()

    response_data = response.read().decode('utf-8')
    status = response.status

    conn.close()
    ssl_sock.close()
    sock.close()

    return {
        'status': status,
        'data': json.loads(response_data) if response_data else {}
    }


def send_telegram_file(bot_token: str, user_id: int, file_path: str, caption: str = None) -> bool:
    """Send file to Telegram, trying multiple IPs."""

    file_path_obj = Path(file_path)
    if not file_path_obj.exists():
        print(f"ERROR: File not found: {file_path}", file=sys.stderr)
        return False

    file_size = file_path_obj.stat().st_size
    max_size = 50 * 1024 * 1024  # 50MB

    if file_size > max_size:
        print(f"ERROR: File too large ({file_size / 1024 / 1024:.1f}MB). Limit: 50MB", file=sys.stderr)
        return False

    print(f"Sending: {file_path_obj.name} ({file_size / 1024:.1f} KB)")
    print(f"To user: {user_id}")
    if caption:
        print(f"Caption: {caption[:50]}{'...' if len(caption) > 50 else ''}")
    print()

    for ip in WORKING_TELEGRAM_IPS:
        print(f"Trying IP: {ip}...", end=" ", flush=True)
        try:
            result = send_file_via_ip(ip, bot_token, user_id, file_path, caption)

            if result['status'] == 200 and result['data'].get('ok'):
                print("SUCCESS!")
                msg = result['data'].get('result', {})
                doc = msg.get('document', {})
                print(f"  Message ID: {msg.get('message_id')}")
                print(f"  File ID: {doc.get('file_id', 'N/A')[:30]}...")
                return True
            else:
                error_desc = result['data'].get('description', f'HTTP {result["status"]}')
                print(f"FAILED: {error_desc}")

        except ssl.SSLCertVerificationError as e:
            print(f"SSL cert error")
        except socket.timeout:
            print(f"timeout")
        except ConnectionRefusedError:
            print(f"refused")
        except Exception as e:
            print(f"error: {type(e).__name__}: {e}")

    print("\nFAILED: Could not send via any IP", file=sys.stderr)
    return False


def main():
    if len(sys.argv) < 3:
        print("Usage: python3 send_telegram_file_v2.py <user_id> <file_path> [caption]")
        sys.exit(1)

    try:
        user_id = int(sys.argv[1])
    except ValueError:
        print(f"ERROR: Invalid user_id '{sys.argv[1]}'", file=sys.stderr)
        sys.exit(1)

    file_path = sys.argv[2]
    caption = sys.argv[3] if len(sys.argv) > 3 else None

    bot_token = load_config()
    if not bot_token:
        print("ERROR: No bot token found. Set TELEGRAM_BOT_TOKEN env var.", file=sys.stderr)
        sys.exit(1)

    success = send_telegram_file(bot_token, user_id, file_path, caption)
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
