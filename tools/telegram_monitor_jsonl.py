#!/usr/bin/env python3
"""
Real-time Telegram monitor using Claude Code JSONL logs.

Replaces tmux buffer monitoring with direct JSONL file watching.
Detects wrapped messages (🤖🎯📱 ... ✨🔚) and forwards to Telegram.
"""

import json
import os
import subprocess
import time
from pathlib import Path
from typing import Optional, Dict, Any


def get_active_session_file(project_path: str = "/home/corey/projects/AI-CIV/WEAVER") -> Optional[str]:
    """Find the most recently updated JSONL session file."""
    # Claude Code logs to ~/.claude/projects/{project-slug}/{session-uuid}.jsonl
    claude_projects = Path.home() / ".claude" / "projects" / "-home-corey-projects-AI-CIV-grow-openai"

    if not claude_projects.exists():
        print(f"❌ Claude projects dir not found: {claude_projects}")
        return None

    # Find most recent .jsonl file
    jsonl_files = list(claude_projects.glob("*.jsonl"))
    if not jsonl_files:
        print(f"❌ No JSONL files found in {claude_projects}")
        return None

    # Sort by modification time, newest first
    jsonl_files.sort(key=lambda f: f.stat().st_mtime, reverse=True)
    return str(jsonl_files[0])


def extract_wrapped_content(text: str) -> Optional[str]:
    """Extract content between 🤖🎯📱 and ✨🔚 markers."""
    start_marker = '🤖🎯📱'
    end_marker = '✨🔚'

    if start_marker in text and end_marker in text:
        start = text.find(start_marker) + len(start_marker)
        end = text.find(end_marker)
        return text[start:end].strip()

    return None


def send_to_telegram(content: str, user_id: str = "437939400") -> bool:
    """Send message to Telegram using send_telegram_direct.py."""
    script_path = "/home/corey/projects/AI-CIV/WEAVER/tools/send_telegram_direct.py"

    try:
        result = subprocess.run(
            ['python3', script_path, user_id, content],
            capture_output=True,
            text=True,
            timeout=30
        )

        if result.returncode != 0:
            print(f"❌ Send failed with code {result.returncode}")
            print(f"   stdout: {result.stdout}")
            print(f"   stderr: {result.stderr}")
            return False

        return True
    except Exception as e:
        print(f"❌ Telegram send exception: {e}")
        import traceback
        traceback.print_exc()
        return False


def aggregate_message_chunks(lines: list) -> list:
    """
    Aggregate multi-line streaming messages into complete messages.

    Claude Code writes messages as 5-20+ JSONL lines per logical message.
    We must track message.id to aggregate chunks properly.
    """
    messages = []
    current_msg_id = None
    current_chunks = []

    for line in lines:
        try:
            entry = json.loads(line)
        except json.JSONDecodeError:
            continue

        # Skip metadata entries
        if entry.get('type') == 'file-history-snapshot':
            continue

        msg_id = entry.get('message', {}).get('id')

        # New message detected (or type change to 'user')
        if msg_id != current_msg_id or entry.get('type') == 'user':
            # Finalize previous message if exists
            if current_chunks:
                messages.append(finalize_message(current_chunks))

            # Start new message
            current_msg_id = msg_id
            current_chunks = [entry]
        else:
            # Same message, accumulate
            current_chunks.append(entry)

    # Don't forget the last message
    if current_chunks:
        messages.append(finalize_message(current_chunks))

    return messages


def finalize_message(chunks: list) -> Dict[str, Any]:
    """Combine message chunks into single complete message."""
    if not chunks:
        return {}

    first = chunks[0]
    msg_type = first.get('type')

    if msg_type == 'user':
        # User messages are atomic
        return first

    # Assistant messages: combine all content blocks
    combined_content = []
    for chunk in chunks:
        content = chunk.get('message', {}).get('content', [])
        combined_content.extend(content)

    # Build final message
    result = first.copy()
    result['message']['content'] = combined_content

    # Flatten text content for easy access
    text_parts = [c['text'] for c in combined_content if c.get('type') == 'text']
    result['text'] = '\n\n'.join(text_parts)

    return result


def monitor_session(session_file: str, state_file: str = ".tg_sessions/jsonl_monitor_state.json"):
    """
    Watch JSONL session file for new wrapped messages and forward to Telegram.

    Uses simple file offset tracking - reads from last known position.
    """
    print(f"📂 Monitoring: {session_file}")
    print(f"💾 State file: {state_file}")
    print(f"🔍 Looking for: 🤖🎯📱 ... ✨🔚")
    print()

    # Load state (last file offset)
    state = {"last_offset": 0, "sent_hashes": []}
    if os.path.exists(state_file):
        with open(state_file, 'r') as f:
            state = json.load(f)

    while True:
        try:
            # Check if session file exists and get size
            if not os.path.exists(session_file):
                print(f"⚠️  Session file not found, waiting...")
                time.sleep(10)
                continue

            file_size = os.path.getsize(session_file)

            # No new content
            if file_size <= state['last_offset']:
                time.sleep(5)
                continue

            # Read new content
            with open(session_file, 'r') as f:
                f.seek(state['last_offset'])
                new_lines = f.readlines()
                state['last_offset'] = f.tell()

            if not new_lines:
                time.sleep(5)
                continue

            print(f"📥 Read {len(new_lines)} new JSONL lines (offset: {state['last_offset']})")

            # Aggregate into complete messages
            messages = aggregate_message_chunks(new_lines)
            print(f"📝 Aggregated into {len(messages)} complete messages")

            # Check each message for wrapper
            for msg in messages:
                text = msg.get('text', '')

                wrapped_content = extract_wrapped_content(text)
                if wrapped_content:
                    # Deduplicate
                    import hashlib
                    msg_hash = hashlib.sha256(wrapped_content.encode()).hexdigest()[:16]

                    if msg_hash in state['sent_hashes']:
                        print(f"⏭️  Skipping duplicate message (hash: {msg_hash})")
                        continue

                    # Send to Telegram
                    print(f"📤 Sending wrapped message to Telegram...")
                    print(f"   Preview: {wrapped_content[:100]}...")

                    if send_to_telegram(wrapped_content):
                        print(f"✅ Sent successfully!")
                        state['sent_hashes'].append(msg_hash)

                        # Keep only last 50 hashes
                        if len(state['sent_hashes']) > 50:
                            state['sent_hashes'] = state['sent_hashes'][-50:]
                    else:
                        print(f"❌ Send failed")

            # Save state
            os.makedirs(os.path.dirname(state_file) or '.', exist_ok=True)
            with open(state_file, 'w') as f:
                json.dump(state, f, indent=2)

        except KeyboardInterrupt:
            print("\n\n⏹️  Stopping monitor...")
            break
        except Exception as e:
            print(f"❌ Error: {e}")
            import traceback
            traceback.print_exc()
            time.sleep(10)


def main():
    print("=" * 60)
    print("  Telegram Monitor (JSONL-based)")
    print("=" * 60)
    print()

    # Find active session
    session_file = get_active_session_file()
    if not session_file:
        print("❌ Could not find active session file")
        return 1

    print(f"✅ Found active session: {Path(session_file).name}")
    print()

    # Start monitoring
    try:
        monitor_session(session_file)
    except KeyboardInterrupt:
        print("\n\n✅ Stopped.")

    return 0


if __name__ == "__main__":
    exit(main())
