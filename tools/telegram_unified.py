#!/usr/bin/env python3
"""
Unified Telegram Bot for WEAVER Civilization
Bidirectional communication: TG <-> Claude via tmux injection + log streaming

Adapted from A-C-Gee's proven implementation (telegram_unified.py)

Features:
- Incoming TG messages inject to Claude's tmux session
- Claude's responses stream to TG feed
- Intelligent message chunking for large posts
- Auto-detects WEAVER tmux sessions
- Single process = more reliable than separate bridge + monitor
"""

import asyncio
import json
import logging
import os
import re
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional, Dict, List, Set
from collections import deque

import httpx

# Attachment download directory
PROJECT_ROOT = Path(__file__).parent.parent
ATTACHMENT_DIR = PROJECT_ROOT / "downloads" / "telegram_attachments"
ATTACHMENT_DIR.mkdir(parents=True, exist_ok=True)

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Paths - WEAVER specific
PROJECT_ROOT = Path(__file__).parent.parent
CONFIG_FILE = PROJECT_ROOT / "config" / "telegram_config.json"

# Claude log paths - WEAVER specific
HISTORY_FILE = Path.home() / ".claude" / "history.jsonl"
PROJECT_MATCH = "/AI-CIV/WEAVER"
PROJECT_SLUG = "-home-corey-projects-AI-CIV-WEAVER"
LOG_ROOT = Path.home() / ".claude" / "projects" / PROJECT_SLUG

# Telegram limits
TG_MAX_MESSAGE_LEN = 4096
TG_SAFE_LEN = 3500  # Leave room for headers


class TelegramBot:
    """Unified Telegram bot with bidirectional communication."""

    def __init__(self, config: Dict):
        self.config = config
        self.bot_token = config["bot_token"]
        self.chat_id = config.get("chat_id") or list(config.get("authorized_users", {}).keys())[0]
        self.authorized_users = config.get("authorized_users", {})

        # Telegram API
        self.api_base = f"https://api.telegram.org/bot{self.bot_token}"
        self.client: Optional[httpx.AsyncClient] = None

        # tmux target
        self.tmux_session: Optional[str] = None
        self.tmux_pane: Optional[str] = None

        # Log streaming state
        self.current_session: Optional[str] = None
        self.current_log_path: Optional[Path] = None
        self.last_position: int = 0
        self._sent_ids: Set[str] = set()
        self._last_update_id: int = 0

        # Running state
        self._running = False

    async def start(self):
        """Start the bot."""
        self.client = httpx.AsyncClient(timeout=30)

        # Detect tmux session
        self.tmux_session = self._detect_weaver_session()
        if self.tmux_session:
            self.tmux_pane = f"{self.tmux_session}:0.0"
            logger.info(f"Detected WEAVER tmux session: {self.tmux_session}")
        else:
            logger.warning("No WEAVER tmux session detected - injection will fail")

        # Find Claude log session
        session_id = self._find_claude_session()
        if session_id:
            self._switch_session(session_id)
            logger.info(f"Monitoring Claude session: {session_id}")

        self._running = True
        logger.info("WEAVER Telegram bot started")

        # Send startup message
        await self._send_message("WEAVER Telegram bot online. Claude log streaming active.")

    async def shutdown(self):
        """Shutdown the bot."""
        self._running = False
        if self.client:
            await self.client.aclose()
        logger.info("WEAVER Telegram bot stopped")

    async def run(self):
        """Main run loop - polls for TG updates and Claude logs."""
        await self.start()

        # Session refresh counter (check every ~60 seconds)
        loop_count = 0
        SESSION_REFRESH_INTERVAL = 120  # loops (at 0.5s = 60 seconds)

        try:
            while self._running:
                # Check for new Telegram messages
                await self._poll_telegram_updates()

                # Check for new Claude log entries
                await self._poll_claude_logs()

                # Periodic session refresh - detect new sessions
                loop_count += 1
                if loop_count >= SESSION_REFRESH_INTERVAL:
                    loop_count = 0
                    await self._refresh_session_if_needed()

                # Small sleep to prevent busy-waiting
                await asyncio.sleep(0.5)

        except KeyboardInterrupt:
            logger.info("Interrupted by user")
        except Exception as e:
            logger.exception(f"Bot error: {e}")
        finally:
            await self.shutdown()

    async def _refresh_session_if_needed(self):
        """Check if a newer WEAVER session exists and switch to it."""
        try:
            new_session = self._detect_weaver_session()
            if new_session and new_session != self.tmux_session:
                logger.info(f"Session change detected: {self.tmux_session} -> {new_session}")
                self.tmux_session = new_session
                self.tmux_pane = f"{new_session}:0.0"
                await self._send_message(f"Switched to new session: {new_session}")
            elif not new_session and self.tmux_session:
                # Current session may have died, try to find any available
                logger.warning(f"Current session {self.tmux_session} may be gone, checking...")
                if not self._check_tmux_session():
                    logger.error("Session lost! Will retry detection on next cycle.")
                    self.tmux_session = None
                    self.tmux_pane = None
        except Exception as e:
            logger.error(f"Session refresh error: {e}")

    # ========== Telegram Polling ==========

    async def _poll_telegram_updates(self):
        """Poll for new Telegram messages."""
        try:
            url = f"{self.api_base}/getUpdates"
            params = {
                "offset": self._last_update_id + 1,
                "timeout": 1,  # Short poll timeout
                "allowed_updates": ["message"],
            }

            resp = await self.client.get(url, params=params, timeout=5)
            if resp.status_code != 200:
                return

            data = resp.json()
            if not data.get("ok"):
                return

            for update in data.get("result", []):
                self._last_update_id = update["update_id"]
                await self._handle_telegram_update(update)

        except httpx.TimeoutException:
            pass  # Expected on long poll timeout
        except Exception as e:
            logger.error(f"Telegram poll error: {e}")

    async def _download_telegram_file(self, file_id: str, filename: str) -> Optional[Path]:
        """Download a file from Telegram using file_id."""
        try:
            # Step 1: Get file path from Telegram
            url = f"{self.api_base}/getFile"
            resp = await self.client.get(url, params={"file_id": file_id})

            if resp.status_code != 200:
                logger.error(f"getFile failed: {resp.status_code}")
                return None

            data = resp.json()
            if not data.get("ok"):
                logger.error(f"getFile error: {data}")
                return None

            file_path = data["result"]["file_path"]

            # Step 2: Download the file
            file_url = f"https://api.telegram.org/file/bot{self.bot_token}/{file_path}"
            file_resp = await self.client.get(file_url)

            if file_resp.status_code != 200:
                logger.error(f"File download failed: {file_resp.status_code}")
                return None

            # Step 3: Save to attachment directory with timestamp
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            safe_filename = re.sub(r'[^\w\-_\.]', '_', filename)
            save_path = ATTACHMENT_DIR / f"{timestamp}_{safe_filename}"

            save_path.write_bytes(file_resp.content)
            logger.info(f"Downloaded attachment to {save_path}")

            return save_path

        except Exception as e:
            logger.error(f"File download error: {e}")
            return None

    async def _handle_telegram_update(self, update: Dict):
        """Handle a single Telegram update."""
        message = update.get("message")
        if not message:
            return

        user = message.get("from", {})
        user_id = str(user.get("id", ""))
        username = user.get("username") or user.get("first_name") or "user"

        # Authorization check
        if user_id not in self.authorized_users:
            logger.warning(f"Unauthorized user {user_id} attempted access")
            return

        # Check for attachments first
        attachment_path = None
        attachment_type = None

        # Handle photo attachments (array of sizes, get largest)
        if message.get("photo"):
            photos = message["photo"]
            largest = photos[-1]  # Last is largest
            file_id = largest["file_id"]
            attachment_path = await self._download_telegram_file(file_id, "photo.jpg")
            attachment_type = "PHOTO"

        # Handle document attachments
        elif message.get("document"):
            doc = message["document"]
            file_id = doc["file_id"]
            filename = doc.get("file_name", "document")
            attachment_path = await self._download_telegram_file(file_id, filename)
            attachment_type = "DOCUMENT"

        # Handle voice attachments
        elif message.get("voice"):
            voice = message["voice"]
            file_id = voice["file_id"]
            attachment_path = await self._download_telegram_file(file_id, "voice.ogg")
            attachment_type = "VOICE"

        # Handle video attachments
        elif message.get("video"):
            video = message["video"]
            file_id = video["file_id"]
            filename = video.get("file_name", "video.mp4")
            attachment_path = await self._download_telegram_file(file_id, filename)
            attachment_type = "VIDEO"

        # If we got an attachment, inject notification
        if attachment_path:
            attachment_msg = f"[TG {attachment_type} from @{username}] File saved to: {attachment_path}"
            logger.info(attachment_msg)
            await self._send_message(f"Downloaded {attachment_type.lower()} to: {attachment_path}")

            # Inject to tmux so Claude knows about the file
            if self.tmux_pane:
                try:
                    subprocess.run(
                        ["tmux", "send-keys", "-t", self.tmux_pane, "-l", attachment_msg],
                        check=True, timeout=5
                    )
                    # Triple-Enter retry for reliability
                    for attempt in range(3):
                        try:
                            subprocess.run(
                                ["tmux", "send-keys", "-t", self.tmux_pane, "Enter"],
                                check=True, timeout=2
                            )
                            if attempt > 0:
                                logger.info(f"Attachment Enter succeeded on attempt {attempt + 1}")
                            break
                        except subprocess.CalledProcessError:
                            logger.warning(f"Attachment Enter attempt {attempt + 1} failed, retrying...")
                            await asyncio.sleep(0.1)
                except Exception as e:
                    logger.error(f"tmux injection failed for attachment: {e}")

            # Also handle any caption text
            caption = message.get("caption", "")
            if caption:
                await self._inject_and_respond(f"[Caption: {caption}]", username)
            return

        # Handle text messages
        text = message.get("text", "")
        if not text:
            return

        logger.info(f"Message from @{username}: {text[:50]}...")

        # Handle commands
        if text.startswith("/"):
            await self._handle_command(text, user_id, username)
            return

        # Inject to tmux
        await self._inject_and_respond(text, username)

    async def _handle_command(self, text: str, user_id: str, username: str):
        """Handle bot commands."""
        cmd = text.split()[0].lower()

        if cmd == "/start" or cmd == "/help":
            help_text = """WEAVER Telegram Bridge

Commands:
/start, /help - This message
/ping - Health check
/status - Session status

Just send a message to talk to Claude.
Responses stream automatically."""
            await self._send_message(help_text)

        elif cmd == "/ping":
            tmux_ok = self._check_tmux_session()
            claude_ok = self.current_session is not None
            await self._send_message(
                f"Pong!\n"
                f"tmux: {'OK' if tmux_ok else 'NOT FOUND'} ({self.tmux_session})\n"
                f"Claude log: {'OK' if claude_ok else 'NOT FOUND'}"
            )

        elif cmd == "/status":
            status = f"""Session Status:
tmux: {self.tmux_pane or 'Not detected'}
Claude session: {self.current_session or 'Not found'}
Log path: {self.current_log_path or 'None'}
Messages sent: {len(self._sent_ids)}"""
            await self._send_message(status)

    async def _inject_and_respond(self, text: str, username: str):
        """Inject message to tmux."""
        if not self.tmux_pane:
            await self._send_message("Error: No tmux session detected. Cannot inject.")
            return

        # Format with Telegram indicator
        formatted = f"[TELEGRAM from {username},] {text}"

        try:
            # Send text to tmux
            subprocess.run(
                ["tmux", "send-keys", "-t", self.tmux_pane, "-l", formatted],
                check=True, timeout=5
            )

            # Triple-Enter retry for large text blocks
            enter_success = False
            for attempt in range(3):
                try:
                    subprocess.run(
                        ["tmux", "send-keys", "-t", self.tmux_pane, "Enter"],
                        check=True, timeout=2
                    )
                    enter_success = True
                    if attempt > 0:
                        logger.info(f"Enter succeeded on attempt {attempt + 1}")
                    break
                except subprocess.CalledProcessError:
                    logger.warning(f"Enter attempt {attempt + 1} failed, retrying...")
                    await asyncio.sleep(0.1)

            if not enter_success:
                logger.error("All 3 Enter attempts failed")
                await self._send_message("Warning: Enter key may not have registered. Send '.' if needed.")
                return

            logger.info(f"Injected to tmux: {formatted[:50]}...")

        except subprocess.CalledProcessError as e:
            logger.error(f"tmux injection failed: {e}")
            await self._send_message(f"Error: tmux injection failed")
        except subprocess.TimeoutExpired:
            logger.error("tmux injection timed out")
            await self._send_message("Error: tmux injection timed out")

    # ========== Claude Log Streaming ==========

    async def _poll_claude_logs(self):
        """Poll Claude logs for new entries."""
        try:
            # Check if session changed
            session_id = self._find_claude_session()
            if session_id and session_id != self.current_session:
                self._switch_session(session_id)
                logger.info(f"Switched to Claude session: {session_id}")

            if not self.current_log_path or not self.current_log_path.exists():
                return

            # Read new entries
            entries = self._read_new_entries()

            for entry in entries:
                await self._send_claude_entry(entry)

        except Exception as e:
            logger.error(f"Claude log poll error: {e}")

    def _find_claude_session(self) -> Optional[str]:
        """Find current Claude session ID from history."""
        try:
            if not HISTORY_FILE.exists():
                return None

            with HISTORY_FILE.open("r") as f:
                f.seek(0, 2)
                length = f.tell()
                window = min(16384, length)
                f.seek(max(0, length - window))
                lines = f.read().splitlines()

            for line in reversed(lines):
                if not line.strip():
                    continue
                try:
                    entry = json.loads(line)
                    if PROJECT_MATCH in entry.get("project", ""):
                        return entry.get("sessionId")
                except json.JSONDecodeError:
                    continue

            return None
        except Exception as e:
            logger.error(f"Error finding Claude session: {e}")
            return None

    def _switch_session(self, session_id: str):
        """Switch to a new Claude session."""
        self.current_session = session_id
        self.current_log_path = LOG_ROOT / f"{session_id}.jsonl"
        self._sent_ids.clear()

        # Seek to end of file (don't replay history)
        if self.current_log_path.exists():
            with self.current_log_path.open("r") as f:
                f.seek(0, 2)
                self.last_position = f.tell()
        else:
            self.last_position = 0

    def _read_new_entries(self) -> List[Dict]:
        """Read new entries from Claude log."""
        entries = []

        try:
            with self.current_log_path.open("r") as f:
                f.seek(self.last_position)
                while True:
                    line = f.readline()
                    if not line:
                        break
                    self.last_position = f.tell()

                    line = line.strip()
                    if not line:
                        continue

                    try:
                        entry = json.loads(line)
                        payload = self._build_payload(entry)
                        if payload and payload["id"] not in self._sent_ids:
                            self._sent_ids.add(payload["id"])
                            entries.append(payload)
                    except json.JSONDecodeError:
                        continue

        except FileNotFoundError:
            pass
        except Exception as e:
            logger.error(f"Error reading Claude log: {e}")

        return entries

    def _build_payload(self, entry: Dict) -> Optional[Dict]:
        """Build payload from Claude log entry."""
        message = entry.get("message", {})
        content_blocks = message.get("content", []) or []
        text_parts = []

        for block in content_blocks:
            if isinstance(block, str):
                if block.strip():
                    text_parts.append(block.strip())
            elif isinstance(block, dict):
                if block.get("type") == "text":
                    text = (block.get("text") or "").strip()
                    if text:
                        text_parts.append(text)

        if not text_parts:
            return None

        combined_text = "\n\n".join(text_parts)
        role = message.get("role", entry.get("type", "assistant"))

        # Only forward assistant messages to avoid echo
        if role != "assistant":
            return None

        # Process timestamp
        timestamp = entry.get("timestamp")
        if isinstance(timestamp, (int, float)):
            timestamp = datetime.fromtimestamp(timestamp / 1000, tz=timezone.utc).isoformat()
        elif not timestamp:
            timestamp = datetime.utcnow().replace(tzinfo=timezone.utc).isoformat()

        return {
            "id": entry.get("uuid") or f"log-{timestamp}",
            "role": role,
            "text": combined_text,
            "timestamp": timestamp,
        }

    async def _send_claude_entry(self, entry: Dict):
        """Send a Claude log entry to Telegram."""
        text = entry.get("text", "")
        if not text:
            return

        # Format with role indicator
        timestamp = entry.get("timestamp", "")[:19]
        header = f"WEAVER [{timestamp}]"

        full_message = f"{header}\n\n{text}"

        # Chunk if needed
        chunks = self._chunk_message(full_message)

        for i, chunk in enumerate(chunks):
            if len(chunks) > 1:
                marker = f"[{i+1}/{len(chunks)}]\n\n"
                await self._send_message(marker + chunk)
            else:
                await self._send_message(chunk)

            if i < len(chunks) - 1:
                await asyncio.sleep(0.3)

    # ========== Message Chunking ==========

    def _chunk_message(self, text: str, max_len: int = TG_SAFE_LEN) -> List[str]:
        """Chunk long messages intelligently."""
        if len(text) <= max_len:
            return [text]

        chunks = []
        current = ""

        paragraphs = text.split('\n\n')

        for para in paragraphs:
            test = current + ('\n\n' if current else '') + para

            if len(test) <= max_len:
                current = test
            else:
                if current:
                    chunks.append(current)
                    current = ""

                if len(para) <= max_len:
                    current = para
                else:
                    para_chunks = self._chunk_by_lines(para, max_len)
                    for pc in para_chunks[:-1]:
                        chunks.append(pc)
                    current = para_chunks[-1] if para_chunks else ""

        if current:
            chunks.append(current)

        return chunks if chunks else [text]

    def _chunk_by_lines(self, text: str, max_len: int) -> List[str]:
        """Chunk text by line breaks."""
        chunks = []
        current = ""

        for line in text.split('\n'):
            test = current + ('\n' if current else '') + line

            if len(test) <= max_len:
                current = test
            else:
                if current:
                    chunks.append(current)
                    current = ""

                if len(line) <= max_len:
                    current = line
                else:
                    word_chunks = self._chunk_by_words(line, max_len)
                    for wc in word_chunks[:-1]:
                        chunks.append(wc)
                    current = word_chunks[-1] if word_chunks else ""

        if current:
            chunks.append(current)

        return chunks

    def _chunk_by_words(self, text: str, max_len: int) -> List[str]:
        """Chunk text by word boundaries."""
        chunks = []
        current = ""

        for word in text.split(' '):
            test = current + (' ' if current else '') + word

            if len(test) <= max_len:
                current = test
            else:
                if current:
                    chunks.append(current)
                current = word[:max_len]

        if current:
            chunks.append(current)

        return chunks

    # ========== Markdown Conversion ==========

    def _markdown_to_telegram_html(self, text: str) -> str:
        """
        Convert standard markdown to Telegram-compatible HTML.

        Telegram HTML supports: <b>, <i>, <u>, <s>, <code>, <pre>, <a href="">
        Adapted from A-C-Gee's implementation.
        """
        result = text

        # Escape HTML special chars FIRST
        result = result.replace('&', '&amp;')
        result = result.replace('<', '&lt;')
        result = result.replace('>', '&gt;')

        # Code blocks (``` ... ```) - must be before inline code
        result = re.sub(
            r'```(?:\w+)?\n?(.*?)```',
            r'<pre>\1</pre>',
            result,
            flags=re.DOTALL
        )

        # Inline code (`code`)
        result = re.sub(r'`([^`]+)`', r'<code>\1</code>', result)

        # Headers (### Header) - convert to bold
        result = re.sub(r'^#{1,6}\s+(.+?)$', r'<b>\1</b>', result, flags=re.MULTILINE)

        # Bold (**text** or __text__)
        result = re.sub(r'\*\*(.+?)\*\*', r'<b>\1</b>', result)
        result = re.sub(r'__(.+?)__', r'<b>\1</b>', result)

        # Italic (*text* or _text_) - careful not to match bold
        result = re.sub(r'(?<!\*)\*([^\*\n]+?)\*(?!\*)', r'<i>\1</i>', result)
        result = re.sub(r'(?<!\w)_([^_\n]+?)_(?!\w)', r'<i>\1</i>', result)

        # Strikethrough (~~text~~)
        result = re.sub(r'~~(.+?)~~', r'<s>\1</s>', result)

        # Links [text](url)
        result = re.sub(r'\[([^\]]+)\]\(([^\)]+)\)', r'<a href="\2">\1</a>', result)

        # Bullet points (normalize)
        result = re.sub(r'^[\-\*]\s+', '• ', result, flags=re.MULTILINE)

        return result

    # ========== Telegram API ==========

    async def _send_message(self, text: str, use_html: bool = True):
        """Send message to Telegram with proper formatting."""
        if not self.client:
            return

        try:
            url = f"{self.api_base}/sendMessage"

            # Convert markdown to Telegram HTML
            if use_html:
                formatted_text = self._markdown_to_telegram_html(text)
            else:
                formatted_text = text

            data = {
                "chat_id": self.chat_id,
                "text": formatted_text[:TG_MAX_MESSAGE_LEN],
                "parse_mode": "HTML" if use_html else None,
            }
            # Remove None values
            data = {k: v for k, v in data.items() if v is not None}

            resp = await self.client.post(url, json=data)
            if resp.status_code != 200:
                # If HTML parsing failed, try plain text as fallback
                if use_html and resp.status_code == 400:
                    logger.warning(f"HTML parse failed, falling back to plain text")
                    await self._send_message(text, use_html=False)
                else:
                    logger.warning(f"Telegram send failed: {resp.status_code} {resp.text}")

        except Exception as e:
            logger.error(f"Telegram send error: {e}")

    # ========== tmux Utilities ==========

    def _detect_weaver_session(self) -> Optional[str]:
        """Auto-detect WEAVER tmux session - ALWAYS picks latest available."""
        try:
            # Primary: Auto-detect latest weaver-primary-* session
            result = subprocess.run(
                ["tmux", "list-sessions", "-F", "#{session_name}"],
                capture_output=True, text=True, timeout=5
            )

            if result.returncode == 0:
                sessions = result.stdout.strip().split('\n')
                weaver_sessions = [s for s in sessions if s.startswith('weaver-primary-')]

                if weaver_sessions:
                    latest = sorted(weaver_sessions)[-1]  # Latest by timestamp in name
                    logger.info(f"Auto-detected latest WEAVER session: {latest}")
                    return latest

            # Fallback: Check config file (only if no auto-detect worked)
            if CONFIG_FILE.exists():
                with CONFIG_FILE.open() as f:
                    config = json.load(f)
                    session_name = config.get("tmux_session")
                    if session_name:
                        result = subprocess.run(
                            ["tmux", "has-session", "-t", session_name],
                            capture_output=True, timeout=5
                        )
                        if result.returncode == 0:
                            logger.info(f"Using config fallback session: {session_name}")
                            return session_name

            return None

        except Exception as e:
            logger.error(f"Session detection error: {e}")
            return None

    def _check_tmux_session(self) -> bool:
        """Check if tmux session exists."""
        if not self.tmux_session:
            return False
        try:
            result = subprocess.run(
                ["tmux", "has-session", "-t", self.tmux_session],
                capture_output=True, timeout=5
            )
            return result.returncode == 0
        except:
            return False


def load_config() -> Dict:
    """Load configuration from file."""
    if not CONFIG_FILE.exists():
        raise FileNotFoundError(f"Config file not found: {CONFIG_FILE}")

    with CONFIG_FILE.open() as f:
        config = json.load(f)

    if not config.get("bot_token"):
        raise ValueError("No bot_token in config")

    # Get chat_id from config or first authorized user
    if not config.get("chat_id"):
        users = config.get("authorized_users", {})
        if users:
            config["chat_id"] = list(users.keys())[0]
        else:
            raise ValueError("No chat_id or authorized_users in config")

    return config


async def send_one_message(message: str) -> int:
    """Send a single message and exit immediately (no polling)."""
    try:
        config = load_config()
    except Exception as e:
        logger.error(f"Config error: {e}")
        return 1

    async with httpx.AsyncClient(timeout=30) as client:
        url = f"https://api.telegram.org/bot{config['bot_token']}/sendMessage"
        data = {
            "chat_id": config["chat_id"],
            "text": message[:TG_MAX_MESSAGE_LEN],
        }
        resp = await client.post(url, json=data)
        if resp.status_code == 200:
            logger.info(f"Message sent: {message[:50]}...")
            return 0
        else:
            logger.error(f"Send failed: {resp.status_code} {resp.text}")
            return 1


async def main():
    """Main entry point."""
    import sys

    # Handle send mode: python3 telegram_unified.py send "message"
    if len(sys.argv) >= 3 and sys.argv[1] == "send":
        message = " ".join(sys.argv[2:])
        return await send_one_message(message)

    # Bot mode (no args): run polling loop
    logger.info("Starting WEAVER Unified Telegram Bot")

    try:
        config = load_config()
        logger.info("Configuration loaded")
    except Exception as e:
        logger.error(f"Config error: {e}")
        return 1

    bot = TelegramBot(config)
    await bot.run()
    return 0


if __name__ == "__main__":
    import sys
    sys.exit(asyncio.run(main()))
