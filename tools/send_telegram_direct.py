#!/usr/bin/env python3
"""
Send message directly to Telegram via Bot API with rate limiting and Markdown fallback.

Updated 2025-12-30: Now uses GentleTelegram for rate limiting, exponential backoff,
and circuit breaker protection to prevent API temp bans.

Original architecture: A-C-Gee (Team 2) Telegram implementation (Oct 18, 2025).
Team 1 adaptations:
- Updated project root path detection for WEAVER
- Updated config file path: config/telegram_config.json
- Added GentleTelegram rate limiting (2025-12-30)
- Preserved graceful degradation logic (Markdown -> Plain text)

Usage:
    python3 tools/send_telegram_direct.py <user_id> <message>
    python3 tools/send_telegram_direct.py 437939400 "Hello from Primary AI!"

Environment:
    Reads bot token from config/telegram_config.json
    Rate limit state stored in ~/.tg_rate_limit.json
"""

import json
import logging
import sys
import time
from pathlib import Path

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Constants
PROJECT_ROOT = Path(__file__).parent.parent
CONFIG_FILE = PROJECT_ROOT / "config" / "telegram_config.json"

# Import GentleTelegram for rate limiting
try:
    from gentle_telegram import GentleTelegram
    GENTLE_AVAILABLE = True
except ImportError:
    GENTLE_AVAILABLE = False
    logger.warning("GentleTelegram not available, falling back to direct API calls")


def load_config():
    """Load telegram configuration."""
    if not CONFIG_FILE.exists():
        print(f"ERROR: Config file not found: {CONFIG_FILE}", file=sys.stderr)
        sys.exit(1)

    try:
        with open(CONFIG_FILE, 'r') as f:
            return json.load(f)
    except Exception as e:
        print(f"ERROR: Failed to load config: {e}", file=sys.stderr)
        sys.exit(1)


def send_with_gentle(tg: 'GentleTelegram', user_id: int, message: str, use_markdown: bool = True) -> bool:
    """
    Send message using GentleTelegram with rate limiting.

    Args:
        tg: GentleTelegram instance
        user_id: Telegram user ID
        message: Message text
        use_markdown: Whether to try Markdown first

    Returns:
        True if sent successfully
    """
    # Check cooldown first
    if tg.in_cooldown():
        remaining = tg.cooldown_remaining()
        print(f"RATE LIMITED: In cooldown, retry in {remaining}s", file=sys.stderr)
        logger.warning(f"Rate limited - {remaining}s remaining in cooldown")
        return False

    # Try with Markdown first
    if use_markdown:
        success, result = tg.send_message(user_id, message, parse_mode="Markdown")
        if success:
            logger.info("Message sent successfully with Markdown")
            return True

        # Check if it was a Markdown parse error (400)
        if isinstance(result, dict) and result.get("error") == 400:
            logger.info("Markdown parse failed, retrying as plain text")
            # Wait a moment before retry (gentler on API)
            time.sleep(2)
            success, result = tg.send_message(user_id, message)
            if success:
                logger.info("Message sent successfully as plain text")
                return True
    else:
        success, result = tg.send_message(user_id, message)
        if success:
            return True

    # Failed
    error_msg = result.get("message", str(result)) if isinstance(result, dict) else str(result)
    print(f"ERROR: {error_msg}", file=sys.stderr)
    return False


def send_telegram_message_gentle(bot_token: str, user_id: int, message: str) -> bool:
    """
    Send message via GentleTelegram with rate limiting and chunking.

    Args:
        bot_token: Telegram bot token
        user_id: Telegram user ID (chat_id)
        message: Message text to send

    Returns:
        True if sent successfully, False otherwise
    """
    tg = GentleTelegram(bot_token)

    # Telegram message length limit
    MAX_LENGTH = 4096

    # Check cooldown before doing anything
    if tg.in_cooldown():
        remaining = tg.cooldown_remaining()
        status = tg.status()
        print(f"RATE LIMITED: API in cooldown for {remaining}s", file=sys.stderr)
        if status.get("circuit_breaker_active"):
            print(f"  Circuit breaker active ({status['consecutive_errors']} consecutive errors)", file=sys.stderr)
        return False

    # Split message if too long
    if len(message) > MAX_LENGTH:
        chunks = []
        current_chunk = ""

        for line in message.split('\n'):
            if len(current_chunk) + len(line) + 1 > MAX_LENGTH - 100:
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

        # Send all chunks with delays between them
        for i, chunk in enumerate(chunks):
            if i > 0:
                chunk = f"(continued {i+1}/{len(chunks)})\n\n{chunk}"
                # Wait between chunks to be gentle on API
                time.sleep(3)

            # Check cooldown before each chunk
            if tg.in_cooldown():
                remaining = tg.cooldown_remaining()
                print(f"RATE LIMITED during chunked send: {remaining}s remaining", file=sys.stderr)
                print(f"  Sent {i}/{len(chunks)} chunks before rate limit", file=sys.stderr)
                return False

            if not send_with_gentle(tg, user_id, chunk):
                print(f"ERROR: Failed to send chunk {i+1}/{len(chunks)}", file=sys.stderr)
                return False

            logger.info(f"Sent chunk {i+1}/{len(chunks)}")

        return True
    else:
        # Single message
        return send_with_gentle(tg, user_id, message)


def send_telegram_message_fallback(bot_token: str, user_id: int, message: str) -> bool:
    """
    Fallback: Send message directly without rate limiting.
    Only used if GentleTelegram is not available.
    """
    import requests

    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    MAX_LENGTH = 4096

    if len(message) > MAX_LENGTH:
        # Simplified chunking for fallback
        chunks = [message[i:i+MAX_LENGTH-100] for i in range(0, len(message), MAX_LENGTH-100)]
        for i, chunk in enumerate(chunks):
            payload = {"chat_id": user_id, "text": chunk}
            try:
                response = requests.post(url, json=payload, timeout=10)
                response.raise_for_status()
            except Exception as e:
                print(f"ERROR: Fallback send failed: {e}", file=sys.stderr)
                return False
        return True
    else:
        payload = {"chat_id": user_id, "text": message, "parse_mode": "Markdown"}
        try:
            response = requests.post(url, json=payload, timeout=10)
            response.raise_for_status()
            return True
        except Exception:
            # Try without Markdown
            payload = {"chat_id": user_id, "text": message}
            try:
                response = requests.post(url, json=payload, timeout=10)
                response.raise_for_status()
                return True
            except Exception as e:
                print(f"ERROR: Fallback send failed: {e}", file=sys.stderr)
                return False


def main():
    """Main entry point."""
    if len(sys.argv) < 3:
        print("Usage: python3 send_telegram_direct.py <user_id> <message>", file=sys.stderr)
        print("Example: python3 send_telegram_direct.py 437939400 'Hello!'", file=sys.stderr)
        sys.exit(1)

    user_id = sys.argv[1]
    message = sys.argv[2]

    # Validate user_id is numeric
    try:
        user_id = int(user_id)
    except ValueError:
        print(f"ERROR: user_id must be numeric, got: {user_id}", file=sys.stderr)
        sys.exit(1)

    # Load config
    config = load_config()
    bot_token = config.get("bot_token")

    if not bot_token:
        print("ERROR: bot_token not found in config", file=sys.stderr)
        sys.exit(1)

    # Send message (with rate limiting if available)
    if GENTLE_AVAILABLE:
        success = send_telegram_message_gentle(bot_token, user_id, message)
    else:
        logger.warning("Using fallback sender (no rate limiting)")
        success = send_telegram_message_fallback(bot_token, user_id, message)

    if success:
        print(f"Message sent to user {user_id}")
        sys.exit(0)
    else:
        print(f"Failed to send message to user {user_id}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
