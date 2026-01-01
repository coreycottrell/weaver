#!/bin/bash
# Send the Bluesky Growth Strategy file to Corey via Telegram
# Uses the fixed script that bypasses the blocked Telegram IP

cd /home/corey/projects/AI-CIV/WEAVER

python3 tools/send_telegram_file_fixed.py \
    437939400 \
    "/home/corey/projects/AI-CIV/WEAVER/exports/bluesky-growth-strategy-2025-12-30.md" \
    "Bluesky Growth Strategy - 5-agent brainstorm synthesis"
