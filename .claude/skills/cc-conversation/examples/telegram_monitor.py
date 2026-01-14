#!/usr/bin/env python3
"""
Real-time Telegram forwarding example.

Watches active session and forwards wrapped messages to Telegram.
"""

import sys
import subprocess
from claude_code_conversation import watch_conversation


def forward_to_telegram(message):
    """Forward wrapped messages to Telegram."""
    content = message.get('content', '')

    # Check for Telegram wrapper
    if '🤖🎯📱' in content and '✨🔚' in content:
        # Extract wrapped content
        start = content.find('🤖🎯📱') + len('🤖🎯📱')
        end = content.find('✨🔚')
        wrapped = content[start:end].strip()

        print(f"\n[{message['timestamp']}] Forwarding to Telegram...")
        print(f"Preview: {wrapped[:100]}...")

        # Send to Telegram using send_telegram_plain.py
        try:
            subprocess.run(
                ['python3', '/home/corey/projects/AI-CIV/grow_openai/tools/send_telegram_plain.py', wrapped],
                check=True
            )
            print("✓ Sent to Telegram")
        except subprocess.CalledProcessError as e:
            print(f"✗ Failed to send: {e}")


def main():
    print("Starting Telegram monitor...")
    print("Watching for wrapped messages (🤖🎯📱 ... ✨🔚)")
    print("Press Ctrl+C to stop\n")

    # Watch for new messages
    watcher = watch_conversation(
        callback=forward_to_telegram,
        filter_sidechains=True,
        debug=True
    )

    try:
        # Keep running
        import time
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n\nStopping monitor...")
        watcher.stop()
        print("Stopped.")


if __name__ == "__main__":
    main()
