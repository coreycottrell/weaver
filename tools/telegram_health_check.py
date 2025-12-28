#!/usr/bin/env python3
"""
Telegram Health Check - Tests actual API connectivity.

This script provides a comprehensive health check that:
1. Validates config file exists and is readable
2. Tests Bot API connectivity (getMe)
3. Tests ability to send messages (optional, with --send flag)
4. Returns clear pass/fail exit codes for cron/monitoring

Usage:
    python3 telegram_health_check.py           # Check connectivity only (no message sent)
    python3 telegram_health_check.py --send    # Also send test message
    python3 telegram_health_check.py --quiet   # Minimal output (for cron)

Exit codes:
    0 = All checks passed
    1 = Config error
    2 = Bot API connection failed
    3 = Message send failed (only with --send)

Designed for cron jobs - recommended cadence: every 30 minutes
Add to crontab with: crontab -e
    */30 * * * * /usr/bin/python3 /home/corey/projects/AI-CIV/WEAVER/tools/telegram_health_check.py --quiet >> /tmp/telegram_health_cron.log 2>&1
"""

import json
import sys
import requests
from datetime import datetime
from pathlib import Path

# Constants
PROJECT_ROOT = Path(__file__).parent.parent
CONFIG_FILE = PROJECT_ROOT / "config" / "telegram_config.json"
HEALTH_LOG = Path("/tmp/telegram_health_check.log")


def log_result(message: str, quiet: bool = False):
    """Log result to file and optionally stdout."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_line = f"[{timestamp}] {message}"

    # Always write to log file
    with open(HEALTH_LOG, "a") as f:
        f.write(log_line + "\n")

    # Print to stdout unless quiet mode
    if not quiet:
        print(message)


def check_config(quiet: bool = False) -> dict:
    """Check config file exists and is valid."""
    if not CONFIG_FILE.exists():
        log_result(f"FAIL: Config file not found: {CONFIG_FILE}", quiet)
        return None

    try:
        with open(CONFIG_FILE, 'r') as f:
            config = json.load(f)

        # Validate required fields
        if not config.get("bot_token"):
            log_result("FAIL: bot_token missing from config", quiet)
            return None

        if not config.get("authorized_users"):
            log_result("FAIL: authorized_users missing from config", quiet)
            return None

        log_result("PASS: Config file valid", quiet)
        return config

    except json.JSONDecodeError as e:
        log_result(f"FAIL: Config JSON parse error: {e}", quiet)
        return None
    except Exception as e:
        log_result(f"FAIL: Config read error: {e}", quiet)
        return None


def check_bot_api(bot_token: str, quiet: bool = False) -> dict:
    """Check Bot API connectivity using getMe."""
    url = f"https://api.telegram.org/bot{bot_token}/getMe"

    try:
        response = requests.get(url, timeout=10)
        data = response.json()

        if data.get("ok"):
            bot_info = data["result"]
            bot_name = bot_info.get("first_name", "Unknown")
            bot_username = bot_info.get("username", "Unknown")
            log_result(f"PASS: Bot API connected - @{bot_username} ({bot_name})", quiet)
            return bot_info
        else:
            error_desc = data.get("description", "Unknown error")
            log_result(f"FAIL: Bot API error - {error_desc}", quiet)
            return None

    except requests.exceptions.Timeout:
        log_result("FAIL: Bot API timeout (>10s)", quiet)
        return None
    except requests.exceptions.ConnectionError as e:
        log_result(f"FAIL: Bot API connection error - {e}", quiet)
        return None
    except Exception as e:
        log_result(f"FAIL: Bot API unexpected error - {e}", quiet)
        return None


def send_test_message(bot_token: str, user_id: int, quiet: bool = False) -> bool:
    """Send a test message to verify full send capability."""
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    payload = {
        "chat_id": user_id,
        "text": f"[WEAVER Health Check] {timestamp} - Systems operational"
    }

    try:
        response = requests.post(url, json=payload, timeout=10)
        data = response.json()

        if data.get("ok"):
            msg_id = data["result"]["message_id"]
            log_result(f"PASS: Test message sent (ID: {msg_id})", quiet)
            return True
        else:
            error_desc = data.get("description", "Unknown error")
            log_result(f"FAIL: Message send error - {error_desc}", quiet)

            # Provide helpful hint for common issue
            if "chat not found" in error_desc.lower():
                log_result("HINT: User needs to start conversation with bot first (/start)", quiet)

            return False

    except requests.exceptions.Timeout:
        log_result("FAIL: Message send timeout (>10s)", quiet)
        return False
    except Exception as e:
        log_result(f"FAIL: Message send error - {e}", quiet)
        return False


def main():
    """Main health check entry point."""
    # Parse arguments
    send_test = "--send" in sys.argv
    quiet = "--quiet" in sys.argv

    if not quiet:
        print("=" * 50)
        print("Telegram Health Check")
        print("=" * 50)

    # Check 1: Config
    config = check_config(quiet)
    if not config:
        sys.exit(1)

    # Check 2: Bot API connectivity
    bot_token = config["bot_token"]
    bot_info = check_bot_api(bot_token, quiet)
    if not bot_info:
        sys.exit(2)

    # Check 3: Send test message (optional)
    if send_test:
        # Get first authorized user
        authorized_users = config.get("authorized_users", {})
        if not authorized_users:
            log_result("FAIL: No authorized users configured", quiet)
            sys.exit(3)

        user_id = int(list(authorized_users.keys())[0])
        if not send_test_message(bot_token, user_id, quiet):
            sys.exit(3)

    # All checks passed
    if not quiet:
        print("=" * 50)
        print("RESULT: All checks PASSED")
        print("=" * 50)
    else:
        log_result("PASS: All health checks passed", quiet)

    sys.exit(0)


if __name__ == "__main__":
    main()
