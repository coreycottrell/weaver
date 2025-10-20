"""
Real-time conversation monitoring with inotify.

Watches JSONL files for changes and triggers callbacks on new messages.
"""

import os
import time
import threading
from typing import Callable, Optional, Any, Dict
from datetime import datetime


class ConversationWatcher:
    """
    Watch a conversation session file for new messages.

    Uses inotify for efficient file monitoring. Aggregates messages
    properly before triggering callbacks.
    """

    def __init__(
        self,
        jsonl_path: str,
        callback: Callable[[Dict[str, Any]], None],
        filter_sidechains: bool = False,
        filter_snapshots: bool = True,
        poll_interval: float = 0.5,
        debug: bool = False
    ):
        """
        Initialize watcher.

        Args:
            jsonl_path: Path to JSONL file to watch.
            callback: Function to call with each new message.
            filter_sidechains: If True, skip sidechain messages.
            filter_snapshots: If True, skip file-history-snapshot entries.
            poll_interval: Seconds between file checks (fallback if inotify unavailable).
            debug: Enable debug logging.
        """
        self.jsonl_path = jsonl_path
        self.callback = callback
        self.filter_sidechains = filter_sidechains
        self.filter_snapshots = filter_snapshots
        self.poll_interval = poll_interval
        self.debug = debug

        self._stop_event = threading.Event()
        self._thread = None
        self._file_position = 0
        self._current_uuid = None
        self._current_lines = []

        # Try to use inotify
        self._use_inotify = self._init_inotify()

    def _init_inotify(self) -> bool:
        """Initialize inotify if available."""
        try:
            import inotify_simple
            self._inotify = inotify_simple.INotify()
            self._watch_descriptor = self._inotify.add_watch(
                self.jsonl_path,
                inotify_simple.flags.MODIFY
            )
            if self.debug:
                print(f"Using inotify for {self.jsonl_path}")
            return True
        except ImportError:
            if self.debug:
                print("inotify not available, using polling")
            return False
        except Exception as e:
            if self.debug:
                print(f"inotify initialization failed: {e}, using polling")
            return False

    def start(self):
        """Start watching in background thread."""
        if self._thread and self._thread.is_alive():
            raise RuntimeError("Watcher already started")

        # Seek to end of file (only watch new messages)
        if os.path.exists(self.jsonl_path):
            with open(self.jsonl_path, 'r') as f:
                f.seek(0, os.SEEK_END)
                self._file_position = f.tell()

        self._stop_event.clear()
        self._thread = threading.Thread(target=self._watch_loop, daemon=True)
        self._thread.start()

        if self.debug:
            print(f"Watcher started for {self.jsonl_path}")

    def stop(self):
        """Stop watching."""
        if self._thread and self._thread.is_alive():
            self._stop_event.set()
            self._thread.join(timeout=2.0)

        if self._use_inotify:
            try:
                self._inotify.rm_watch(self._watch_descriptor)
                self._inotify.close()
            except:
                pass

        if self.debug:
            print("Watcher stopped")

    def _watch_loop(self):
        """Main watch loop (runs in background thread)."""
        if self._use_inotify:
            self._watch_with_inotify()
        else:
            self._watch_with_polling()

    def _watch_with_inotify(self):
        """Watch using inotify (efficient)."""
        import inotify_simple

        while not self._stop_event.is_set():
            # Wait for file modification (with timeout)
            events = self._inotify.read(timeout=1000)  # 1 second timeout

            if events:
                self._process_new_content()

    def _watch_with_polling(self):
        """Watch using polling (fallback)."""
        while not self._stop_event.is_set():
            try:
                stat = os.stat(self.jsonl_path)
                if stat.st_size > self._file_position:
                    self._process_new_content()
            except FileNotFoundError:
                pass  # File may not exist yet

            time.sleep(self.poll_interval)

    def _process_new_content(self):
        """Process new content added to file."""
        import json
        from .parser import merge_message_lines, parse_message

        try:
            with open(self.jsonl_path, 'r', encoding='utf-8', errors='ignore') as f:
                f.seek(self._file_position)

                for line in f:
                    line = line.strip()
                    if not line:
                        continue

                    try:
                        entry = json.loads(line)
                    except json.JSONDecodeError:
                        continue  # Skip corrupted lines

                    entry_uuid = entry.get('uuid')

                    # Message completion detection
                    if entry_uuid and entry_uuid != self._current_uuid:
                        # Complete previous message
                        if self._current_lines:
                            self._trigger_callback(self._current_lines)

                        # Start new message
                        self._current_lines = [entry]
                        self._current_uuid = entry_uuid

                    elif not entry_uuid:
                        # Standalone entry
                        if self._current_lines:
                            self._trigger_callback(self._current_lines)
                            self._current_lines = []
                            self._current_uuid = None

                        # Trigger for standalone
                        self._trigger_callback([entry])

                    else:
                        # Same UUID = continuation
                        self._current_lines.append(entry)

                self._file_position = f.tell()

        except Exception as e:
            if self.debug:
                print(f"Error processing new content: {e}")

    def _trigger_callback(self, lines):
        """Merge lines and trigger callback if filters pass."""
        from .parser import merge_message_lines, parse_message

        try:
            merged = merge_message_lines(lines)
            parsed = parse_message(merged)

            # Apply filters
            if self.filter_snapshots and parsed.get('type') == 'file-history-snapshot':
                return

            if self.filter_sidechains and parsed.get('is_sidechain', False):
                return

            # Trigger callback
            self.callback(parsed)

        except Exception as e:
            if self.debug:
                print(f"Error in callback: {e}")


def watch_conversation(
    session_id: Optional[str] = None,
    project_path: Optional[str] = None,
    callback: Optional[Callable[[Dict[str, Any]], None]] = None,
    filter_sidechains: bool = False,
    filter_snapshots: bool = True,
    debug: bool = False
) -> ConversationWatcher:
    """
    Watch conversation for new messages in real-time.

    Args:
        session_id: Session UUID to watch. If None, watches most recent session.
        project_path: Path to project directory. If None, auto-detects.
        callback: Function to call with each new message.
        filter_sidechains: If True, skip sidechain messages.
        filter_snapshots: If True, skip file-history-snapshot entries.
        debug: Enable debug logging.

    Returns:
        ConversationWatcher instance (already started).

    Example:
        >>> def handler(msg):
        ...     print(f"[{msg['role']}]: {msg['content'][:100]}")
        >>> watcher = watch_conversation(callback=handler)
        >>> # ... later ...
        >>> watcher.stop()
    """
    from .utils import get_active_session, get_session_path

    # Find session file
    if session_id:
        jsonl_path = get_session_path(session_id, project_path)
    else:
        session_info = get_active_session(project_path)
        jsonl_path = session_info['file_path']

    if not os.path.exists(jsonl_path):
        raise FileNotFoundError(f"Session file not found: {jsonl_path}")

    # Create and start watcher
    watcher = ConversationWatcher(
        jsonl_path=jsonl_path,
        callback=callback or (lambda msg: None),
        filter_sidechains=filter_sidechains,
        filter_snapshots=filter_snapshots,
        debug=debug
    )

    watcher.start()
    return watcher
