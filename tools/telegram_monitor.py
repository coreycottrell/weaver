#!/usr/bin/env python3
"""
Telegram Monitor - Automatic summary detection and delivery.

Adapted from A-C-Gee (Team 2) Telegram implementation (Oct 18, 2025).
Original architecture: 4-layer tmux injection pattern with proven stability.

CRITICAL Stability fixes preserved:
- Delta detection: Only scan NEW buffer lines (prevents duplicate processing)
- Full content hashing: SHA256 prevents duplicate messages
- Fail-safe deduplication: Mark failures as seen (prevents infinite retry loops)
- Buffer position tracking: Handles tmux scrollback correctly

Team 1 adaptations:
- Updated config paths for grow_openai
- Updated default tmux session to "0" (Team 1's session)
- Preserved all emoji markers and state management
- Added comprehensive logging for debugging

Polls tmux session every 5 minutes, detects session summaries using markers,
and automatically sends them to Corey's Telegram.

Usage:
    python3 tools/telegram_monitor.py [--interval SECONDS] [--tmux-session SESSION]

    --interval: Polling interval in seconds (default: 300 = 5 minutes)
    --tmux-session: Tmux session to monitor (default: "0")

Environment:
    Reads Corey's user ID from config/telegram_config.json

Detection markers:
    🤖🎯📱
    ...content...
    ✨🔚
"""

import argparse
import hashlib
import json
import logging
import subprocess
import time
from pathlib import Path
from datetime import datetime

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Constants
PROJECT_ROOT = Path(__file__).parent.parent
CONFIG_FILE = PROJECT_ROOT / "config" / "telegram_config.json"
STATE_FILE = PROJECT_ROOT / ".tg_sessions" / "monitor_state.json"
SEND_SCRIPT = PROJECT_ROOT / "tools" / "send_telegram_direct.py"

# Summary markers - simple emoji wrappers (proven to work!)
START_MARKER = "🤖🎯📱"
END_MARKER = "✨🔚"


def load_config():
    """Load telegram configuration."""
    if not CONFIG_FILE.exists():
        logger.error(f"Config file not found: {CONFIG_FILE}")
        return None

    try:
        with open(CONFIG_FILE, 'r') as f:
            return json.load(f)
    except Exception as e:
        logger.error(f"Failed to load config: {e}")
        return None


def load_state():
    """Load monitor state (last seen summaries and buffer position)."""
    if not STATE_FILE.exists():
        return {"last_summaries": [], "last_buffer_position": 0}

    try:
        with open(STATE_FILE, 'r') as f:
            state = json.load(f)
            # Ensure last_buffer_position exists (backward compatibility)
            if "last_buffer_position" not in state:
                state["last_buffer_position"] = 0
            return state
    except Exception as e:
        logger.warning(f"Failed to load state, starting fresh: {e}")
        return {"last_summaries": [], "last_buffer_position": 0}


def save_state(state):
    """Save monitor state."""
    STATE_FILE.parent.mkdir(exist_ok=True)

    try:
        with open(STATE_FILE, 'w') as f:
            json.dump(state, f, indent=2)
    except Exception as e:
        logger.error(f"Failed to save state: {e}")


def capture_tmux_buffer(session: str) -> tuple:
    """
    Capture tmux buffer content.

    Args:
        session: Tmux session identifier (e.g., "0" or "weaver-main")

    Returns:
        Tuple of (buffer_content: str, line_count: int)
    """
    try:
        # Capture last 500 lines from tmux pane
        result = subprocess.run(
            ["tmux", "capture-pane", "-t", f"{session}:0.0", "-p", "-S", "-500"],
            capture_output=True,
            text=True,
            check=True,
            timeout=5
        )
        lines = result.stdout.split('\n')
        return result.stdout, len(lines)
    except subprocess.CalledProcessError as e:
        logger.error(f"tmux capture failed: {e}")
        return "", 0
    except subprocess.TimeoutExpired:
        logger.error("tmux capture timed out")
        return "", 0
    except Exception as e:
        logger.error(f"Unexpected error capturing tmux: {e}")
        return "", 0


def extract_summaries(buffer: str) -> list:
    """
    Extract session summaries from buffer using markers.

    Args:
        buffer: Tmux buffer content

    Returns:
        List of dicts: [{"type": "message", "content": "...", "timestamp": "..."}]
    """
    summaries = []
    lines = buffer.split('\n')

    i = 0
    while i < len(lines):
        line = lines[i]

        # Check for start marker
        if START_MARKER in line:
            content_lines = []
            i += 1

            # Collect lines until end marker
            while i < len(lines):
                if END_MARKER in lines[i]:
                    break
                content_lines.append(lines[i])
                i += 1

            if content_lines:
                summary = {
                    "type": "message",
                    "content": '\n'.join(content_lines).strip(),
                    "timestamp": datetime.utcnow().isoformat() + "Z"
                }
                summaries.append(summary)

        i += 1

    return summaries


def get_summary_hash(summary: dict) -> str:
    """
    Generate unique hash for entire summary content.

    CRITICAL: Full content hashing prevents duplicate messages.

    Args:
        summary: Summary dict with type, content

    Returns:
        Hash string (type:content_hash)
    """
    content_hash = hashlib.sha256(summary['content'].encode()).hexdigest()
    return f"{summary['type']}:{content_hash}"


def is_new_summary(summary: dict, seen_summaries: set) -> bool:
    """
    Check if summary is new (not already sent).

    Args:
        summary: Summary dict with type, content, timestamp
        seen_summaries: Set of previously seen summary hashes

    Returns:
        True if summary is new
    """
    summary_hash = get_summary_hash(summary)
    return summary_hash not in seen_summaries


def send_summary(user_id: int, summary: dict) -> bool:
    """
    Send summary to Telegram.

    Args:
        user_id: Telegram user ID
        summary: Summary dict with type, content

    Returns:
        True if sent successfully
    """
    # Send content directly (already wrapped in emojis by Primary)
    message = f"🤖🎯📱\n\n{summary['content']}\n\n✨🔚"

    # Call send script
    try:
        result = subprocess.run(
            ["python3", str(SEND_SCRIPT), str(user_id), message],
            capture_output=True,
            text=True,
            check=True,
            timeout=15
        )
        logger.info(f"Sent {summary['type']} summary to user {user_id}")
        return True
    except subprocess.CalledProcessError as e:
        logger.error(f"Failed to send summary: {e.stderr}")
        return False
    except Exception as e:
        logger.error(f"Unexpected error sending summary: {e}")
        return False


def monitor_loop(interval: int, tmux_session: str, user_id: int):
    """
    Main monitoring loop with delta detection and fail-safe deduplication.

    CRITICAL stability features:
    - Only scans NEW lines since last poll (delta detection)
    - Tracks buffer position to handle tmux scrollback
    - ALWAYS marks summaries as seen (even on send failure) to prevent infinite retry

    Args:
        interval: Polling interval in seconds
        tmux_session: Tmux session to monitor
        user_id: Telegram user ID to send to
    """
    logger.info(f"Starting Telegram monitor (interval: {interval}s, session: {tmux_session})")
    logger.info(f"Monitoring for summaries to send to user {user_id}")

    state = load_state()
    seen_summaries = set(state.get("last_summaries", []))
    last_buffer_position = state.get("last_buffer_position", 0)

    # FIX: If starting fresh (position 0), initialize to current buffer size
    # This prevents scanning all existing messages on startup
    if last_buffer_position == 0:
        _, initial_position = capture_tmux_buffer(tmux_session)
        if initial_position > 0:
            last_buffer_position = initial_position
            logger.info(f"Fresh start: Skipping existing {initial_position} lines, will only monitor NEW content")

            # Save initial position
            state["last_buffer_position"] = last_buffer_position
            save_state(state)

    while True:
        try:
            # Capture tmux buffer
            buffer, current_position = capture_tmux_buffer(tmux_session)

            if buffer and current_position != last_buffer_position:
                # Handle buffer shrinking (tmux scrolling)
                if current_position < last_buffer_position:
                    logger.info(f"Buffer shrunk ({last_buffer_position} → {current_position}), resetting position")
                    last_buffer_position = max(0, current_position - 50)  # Go back 50 lines to catch recent content

                # DELTA DETECTION: Only scan NEW lines since last poll
                if current_position > last_buffer_position:
                    lines = buffer.split('\n')
                    new_lines = lines[last_buffer_position:]
                    buffer_to_scan = '\n'.join(new_lines)

                    logger.info(f"Scanning {len(new_lines)} new lines (position {last_buffer_position} → {current_position})")

                    # Extract summaries from new content only
                    summaries = extract_summaries(buffer_to_scan)
                else:
                    # Buffer shrunk, no new content beyond reset point
                    summaries = []

                if summaries:
                    logger.info(f"Found {len(summaries)} summaries in new content")

                    # Send new summaries
                    for summary in summaries:
                        if is_new_summary(summary, seen_summaries):
                            logger.info(f"New {summary['type']} summary detected")

                            success = send_summary(user_id, summary)

                            # FAIL-SAFE DEDUPLICATION: ALWAYS mark as seen (success or failure)
                            # This prevents infinite retry loops
                            summary_hash = get_summary_hash(summary)
                            seen_summaries.add(summary_hash)

                            if not success:
                                logger.warning(f"Failed to send summary, marked as seen to prevent retry: {summary_hash[:20]}...")

                # Update buffer position
                last_buffer_position = current_position

                # Save state
                state["last_summaries"] = list(seen_summaries)[-100:]  # Keep last 100
                state["last_buffer_position"] = last_buffer_position
                save_state(state)

            # Wait for next poll
            time.sleep(interval)

        except KeyboardInterrupt:
            logger.info("Monitor stopped by user")
            break
        except Exception as e:
            logger.error(f"Error in monitor loop: {e}", exc_info=True)
            time.sleep(interval)


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(description="Telegram Monitor - Auto-send session summaries")
    parser.add_argument("--interval", type=int, default=300, help="Polling interval in seconds (default: 300)")
    parser.add_argument("--tmux-session", type=str, default="0", help="Tmux session to monitor (default: 0)")

    args = parser.parse_args()

    # Load config
    config = load_config()
    if not config:
        logger.error("Failed to load config, exiting")
        return 1

    # Get Corey's user ID
    authorized_users = config.get("authorized_users", {})
    if not authorized_users:
        logger.error("No authorized users in config")
        return 1

    # Get first authorized user (Corey)
    user_id = int(list(authorized_users.keys())[0])

    # Start monitoring
    monitor_loop(args.interval, args.tmux_session, user_id)

    return 0


if __name__ == "__main__":
    exit(main())
