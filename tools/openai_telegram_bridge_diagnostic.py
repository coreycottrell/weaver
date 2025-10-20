#!/usr/bin/env python3
"""
🔍 DIAGNOSTIC VERSION - Telegram Bridge with Trace IDs

This is a diagnostic variant of openai_telegram_bridge.py with enhanced logging
to identify the source of duplicate message injections.

Changes from production:
1. Unique trace ID for each message (UUID)
2. Enhanced logging at every step
3. Update ID tracking to detect Telegram API duplicates
4. Injection timestamp tracking
5. Lock mechanism to prevent concurrent processing

Location: tools/openai_telegram_bridge_diagnostic.py (diagnostic)
Production: tools/prod/tg/openai_telegram_bridge.py
"""

import os
import sys
import json
import time
import uuid
import asyncio
import subprocess
import logging
from pathlib import Path
from typing import Dict, Optional
from datetime import datetime
from threading import Lock

# Telegram imports
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    filters,
    ContextTypes,
)

# Configure logging with TRACE level detail
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - [%(funcName)s:%(lineno)d] - %(message)s',
    handlers=[
        logging.FileHandler('/tmp/openai_telegram_bridge_diagnostic.log'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

# Global state tracking
PROCESSED_UPDATES = {}  # update_id -> {timestamp, trace_id, message}
INJECTED_MESSAGES = {}  # trace_id -> {timestamp, message, update_id}
INJECTION_LOCK = Lock()

class TelegramBridge:
    """
    Diagnostic Telegram Bridge with comprehensive trace logging.
    """

    def __init__(self, config_path: str = "config/telegram_config.json"):
        """Initialize bridge with config."""
        logger.info("=" * 80)
        logger.info("DIAGNOSTIC BRIDGE INITIALIZING")
        logger.info("=" * 80)

        self.config_path = Path(config_path)
        self.config = self._load_config()
        self.bot_token = self._get_bot_token()
        self.authorized_users = self.config.get("authorized_users", {})
        self.tmux_session = self.config.get("tmux_session", "1")
        self.tmux_pane = f"{self.tmux_session}:0.0"
        self.working_dir = self.config.get(
            "working_directory",
            "/home/corey/projects/AI-CIV/grow_openai"
        )
        self.response_timeout = self.config.get("response_timeout", 10)

        logger.info(f"Bot token: {self.bot_token[:20]}... (masked)")
        logger.info(f"Authorized users: {list(self.authorized_users.keys())}")
        logger.info(f"tmux session: {self.tmux_session}")
        logger.info(f"tmux pane: {self.tmux_pane}")
        logger.info(f"Working directory: {self.working_dir}")
        logger.info(f"Response timeout: {self.response_timeout}s")

    def _load_config(self) -> dict:
        """Load configuration from JSON file."""
        try:
            with open(self.config_path) as f:
                config = json.load(f)
                logger.info(f"✓ Config loaded from {self.config_path}")
                return config
        except FileNotFoundError:
            logger.error(f"❌ Config not found: {self.config_path}")
            sys.exit(1)
        except json.JSONDecodeError as e:
            logger.error(f"❌ Invalid JSON in config: {e}")
            sys.exit(1)

    def _get_bot_token(self) -> str:
        """Get bot token from config or environment."""
        token = self.config.get("bot_token", "")

        # Support environment variable substitution
        if token.startswith("${") and token.endswith("}"):
            env_var = token[2:-1]
            token = os.getenv(env_var)
            if not token:
                logger.error(f"❌ Environment variable {env_var} not set")
                sys.exit(1)
            logger.info(f"✓ Bot token loaded from ${env_var}")

        if not token:
            logger.error("❌ No bot token found in config or environment")
            sys.exit(1)

        return token

    def is_authorized(self, user_id: int) -> bool:
        """Check if user is authorized."""
        authorized = str(user_id) in self.authorized_users
        logger.debug(f"Authorization check for {user_id}: {authorized}")
        return authorized

    def inject_to_tmux(self, message: str, username: str, trace_id: str, update_id: int) -> bool:
        """
        Inject message to Primary AI tmux session with diagnostic tracing.

        Args:
            message: User message to inject
            username: Telegram username for context
            trace_id: Unique trace ID for this message
            update_id: Telegram update ID

        Returns:
            True if injection succeeded, False otherwise
        """
        with INJECTION_LOCK:
            injection_time = datetime.now().isoformat()

            logger.info("=" * 80)
            logger.info(f"🔍 INJECTION ATTEMPT")
            logger.info(f"  Trace ID: {trace_id}")
            logger.info(f"  Update ID: {update_id}")
            logger.info(f"  Timestamp: {injection_time}")
            logger.info(f"  Username: {username}")
            logger.info(f"  Message: {message[:100]}...")
            logger.info("=" * 80)

            # Check if we've already injected this trace ID
            if trace_id in INJECTED_MESSAGES:
                prev = INJECTED_MESSAGES[trace_id]
                logger.error("⚠️ DUPLICATE INJECTION ATTEMPT DETECTED!")
                logger.error(f"  Previous injection: {prev['timestamp']}")
                logger.error(f"  Previous update_id: {prev['update_id']}")
                logger.error(f"  Time delta: {time.time() - prev.get('time', 0):.2f}s")
                logger.error("  This is the source of the duplicate!")
                return False

            try:
                # Format message with Telegram indicator
                formatted = f"[TELEGRAM from {username}] {message}"

                logger.debug(f"Formatted message: {formatted[:100]}...")
                logger.debug(f"tmux target: {self.tmux_pane}")

                # Send to tmux using literal mode (-l) for special characters
                result = subprocess.run(
                    ["tmux", "send-keys", "-t", self.tmux_pane, "-l", formatted],
                    check=True,
                    capture_output=True,
                    text=True
                )

                logger.debug(f"tmux send-keys stdout: {result.stdout}")
                logger.debug(f"tmux send-keys stderr: {result.stderr}")

                # Send Enter key separately to avoid issues
                subprocess.run(
                    ["tmux", "send-keys", "-t", self.tmux_pane, "Enter"],
                    check=True,
                    capture_output=True,
                    text=True
                )

                # Record successful injection
                INJECTED_MESSAGES[trace_id] = {
                    'timestamp': injection_time,
                    'time': time.time(),
                    'message': message,
                    'update_id': update_id,
                    'username': username
                }

                logger.info(f"✓ tmux injection successful (trace: {trace_id})")
                logger.info(f"  Total injections so far: {len(INJECTED_MESSAGES)}")

                return True

            except subprocess.CalledProcessError as e:
                logger.error(f"❌ tmux injection failed: {e}")
                logger.error(f"  stdout: {e.stdout}")
                logger.error(f"  stderr: {e.stderr}")
                return False
            except Exception as e:
                logger.error(f"❌ Unexpected error during injection: {e}", exc_info=True)
                return False


# Global bridge instance
bridge = None


async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /start command."""
    user = update.effective_user
    logger.info(f"/start command from {user.first_name} (ID: {user.id})")

    if bridge.is_authorized(user.id):
        welcome = (
            f"Welcome {user.first_name}!\n\n"
            f"This is the DIAGNOSTIC Telegram Bridge for Team 1 Primary AI.\n\n"
            f"Enhanced logging active - check /tmp/openai_telegram_bridge_diagnostic.log\n\n"
            f"Send any message and it will be injected to the AI with trace ID."
        )
    else:
        welcome = (
            f"Hello {user.first_name}.\n\n"
            f"You are not authorized. Contact Corey for access."
        )

    await update.message.reply_text(welcome)


async def status_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /status command - show diagnostic info."""
    user = update.effective_user
    logger.info(f"/status command from {user.first_name} (ID: {user.id})")

    if not bridge.is_authorized(user.id):
        await update.message.reply_text("Unauthorized.")
        return

    status = (
        f"📊 Diagnostic Bridge Status\n\n"
        f"Updates processed: {len(PROCESSED_UPDATES)}\n"
        f"Messages injected: {len(INJECTED_MESSAGES)}\n"
        f"Duplicates blocked: {len(PROCESSED_UPDATES) - len(INJECTED_MESSAGES)}\n\n"
        f"Recent injections:\n"
    )

    # Show last 5 injections
    recent = sorted(
        INJECTED_MESSAGES.items(),
        key=lambda x: x[1]['timestamp'],
        reverse=True
    )[:5]

    for trace_id, data in recent:
        status += f"  {data['timestamp']}: {data['message'][:30]}...\n"

    await update.message.reply_text(status)


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Handle regular messages - inject to tmux with diagnostic tracing.
    """
    # Generate unique trace ID for this message
    trace_id = str(uuid.uuid4())
    update_id = update.update_id
    receive_time = datetime.now().isoformat()

    logger.info("=" * 80)
    logger.info(f"📨 MESSAGE RECEIVED")
    logger.info(f"  Trace ID: {trace_id}")
    logger.info(f"  Update ID: {update_id}")
    logger.info(f"  Receive time: {receive_time}")
    logger.info("=" * 80)

    user = update.effective_user
    user_id = user.id

    # Check if we've already processed this update_id
    if update_id in PROCESSED_UPDATES:
        prev = PROCESSED_UPDATES[update_id]
        logger.warning("⚠️ DUPLICATE UPDATE_ID DETECTED!")
        logger.warning(f"  Previous processing: {prev['timestamp']}")
        logger.warning(f"  Previous trace: {prev['trace_id']}")
        logger.warning(f"  This means Telegram API sent the same update twice!")
        logger.warning(f"  Time since first: {time.time() - prev.get('time', 0):.2f}s")

        # Don't process duplicate updates
        await update.message.reply_text(
            f"⚠️ Duplicate update detected (update_id: {update_id})\n"
            f"Already processed {time.time() - prev.get('time', 0):.1f}s ago\n"
            f"This is a Telegram API issue, not our bridge."
        )
        return

    # Record this update as processed
    PROCESSED_UPDATES[update_id] = {
        'timestamp': receive_time,
        'time': time.time(),
        'trace_id': trace_id
    }

    # Authorization check
    if not bridge.is_authorized(user_id):
        logger.warning(f"Unauthorized access attempt from {user_id}")
        await update.message.reply_text(
            "Unauthorized. Contact Corey for access."
        )
        return

    message_text = update.message.text
    username = user.first_name or user.username or "Corey"

    logger.info(f"Message from {username} (ID: {user_id}): {message_text[:50]}...")
    logger.info(f"Proceeding to injection with trace {trace_id}...")

    # Inject message to tmux with trace ID
    injection_success = bridge.inject_to_tmux(message_text, username, trace_id, update_id)

    if not injection_success:
        logger.error(f"Injection failed for trace {trace_id}")
        await update.message.reply_text(
            f"❌ Injection failed (trace: {trace_id[:8]})\n"
            f"Check /tmp/openai_telegram_bridge_diagnostic.log"
        )
        return

    logger.info(f"✓ Message handling complete for trace {trace_id}")


async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle photo messages - inject to tmux with trace."""
    trace_id = str(uuid.uuid4())
    update_id = update.update_id

    logger.info(f"📸 PHOTO RECEIVED (trace: {trace_id}, update: {update_id})")

    user = update.effective_user
    user_id = user.id

    # Check for duplicate update_id
    if update_id in PROCESSED_UPDATES:
        logger.warning(f"⚠️ DUPLICATE PHOTO UPDATE {update_id}")
        return

    PROCESSED_UPDATES[update_id] = {
        'timestamp': datetime.now().isoformat(),
        'time': time.time(),
        'trace_id': trace_id
    }

    if not bridge.is_authorized(user_id):
        await update.message.reply_text("Unauthorized.")
        return

    username = user.first_name or user.username or "Corey"
    caption = update.message.caption or ""

    message = f"[PHOTO] {caption}" if caption else "[PHOTO received]"

    injection_success = bridge.inject_to_tmux(message, username, trace_id, update_id)

    if not injection_success:
        await update.message.reply_text(
            f"❌ Photo notification injection failed (trace: {trace_id[:8]})"
        )


def main():
    """Start the diagnostic bridge."""
    global bridge

    logger.info("=" * 80)
    logger.info("🔍 DIAGNOSTIC TELEGRAM BRIDGE STARTING")
    logger.info("=" * 80)

    # Initialize bridge
    bridge = TelegramBridge()

    # Create application
    application = Application.builder().token(bridge.bot_token).build()

    # Register handlers
    application.add_handler(CommandHandler("start", start_command))
    application.add_handler(CommandHandler("status", status_command))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    application.add_handler(MessageHandler(filters.PHOTO, handle_photo))

    logger.info("✓ Handlers registered")
    logger.info(f"✓ Authorized users: {list(bridge.authorized_users.keys())}")
    logger.info("=" * 80)
    logger.info("🔍 DIAGNOSTIC BRIDGE READY - Enhanced logging active")
    logger.info("=" * 80)

    try:
        application.run_polling(allowed_updates=Update.ALL_TYPES)
    except KeyboardInterrupt:
        logger.info("Bot stopped by user")
    except Exception as e:
        logger.error(f"Fatal error: {e}", exc_info=True)
        sys.exit(1)


if __name__ == "__main__":
    main()
