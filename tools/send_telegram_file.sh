#!/bin/bash
#
# Send file to Telegram - pure bash/curl implementation
# Bypasses all Python DNS issues by using curl directly
#
# Usage:
#   ./send_telegram_file.sh <user_id> <file_path> [caption]
#
# Example:
#   ./send_telegram_file.sh 437939400 /path/to/doc.md "Bluesky strategy"
#
# Author: tg-bridge agent
# Created: 2025-12-30

set -e

# Configuration
CONFIG_FILE="/home/corey/projects/AI-CIV/WEAVER/config/telegram_config.json"

# Check arguments
if [ "$#" -lt 2 ]; then
    echo "Usage: $0 <user_id> <file_path> [caption]" >&2
    echo "" >&2
    echo "Example:" >&2
    echo "  $0 437939400 /path/to/doc.md 'Session summary'" >&2
    exit 1
fi

USER_ID="$1"
FILE_PATH="$2"
CAPTION="${3:-}"

# Validate user_id is numeric
if ! [[ "$USER_ID" =~ ^[0-9]+$ ]]; then
    echo "ERROR: user_id must be numeric, got: $USER_ID" >&2
    exit 1
fi

# Validate file exists
if [ ! -f "$FILE_PATH" ]; then
    echo "ERROR: File not found: $FILE_PATH" >&2
    exit 1
fi

# Check file size (50MB limit)
FILE_SIZE=$(stat -c%s "$FILE_PATH" 2>/dev/null || stat -f%z "$FILE_PATH" 2>/dev/null)
MAX_SIZE=$((50 * 1024 * 1024))
if [ "$FILE_SIZE" -gt "$MAX_SIZE" ]; then
    echo "ERROR: File too large ($(echo "scale=1; $FILE_SIZE/1024/1024" | bc)MB). Limit: 50MB" >&2
    exit 1
fi

# Get bot token - try environment first, then config file
BOT_TOKEN="${TELEGRAM_BOT_TOKEN:-}"

if [ -z "$BOT_TOKEN" ] || [[ "$BOT_TOKEN" == \$* ]]; then
    # Try to extract from config file
    if [ -f "$CONFIG_FILE" ]; then
        BOT_TOKEN=$(grep -o '"bot_token"[[:space:]]*:[[:space:]]*"[^"]*"' "$CONFIG_FILE" | head -1 | sed 's/.*"\([^"]*\)"$/\1/')
    fi
fi

if [ -z "$BOT_TOKEN" ] || [[ "$BOT_TOKEN" == \$* ]]; then
    echo "ERROR: TELEGRAM_BOT_TOKEN not found in environment or config" >&2
    exit 1
fi

# Build API URL
API_URL="https://api.telegram.org/bot${BOT_TOKEN}/sendDocument"

# Build curl command
if [ -n "$CAPTION" ]; then
    # Truncate caption if too long (1024 char limit)
    if [ ${#CAPTION} -gt 1024 ]; then
        echo "WARNING: Caption truncated to 1024 chars" >&2
        CAPTION="${CAPTION:0:1021}..."
    fi
    RESPONSE=$(curl -s -S -X POST "$API_URL" \
        -F "chat_id=$USER_ID" \
        -F "document=@$FILE_PATH" \
        -F "caption=$CAPTION")
else
    RESPONSE=$(curl -s -S -X POST "$API_URL" \
        -F "chat_id=$USER_ID" \
        -F "document=@$FILE_PATH")
fi

# Check response
if echo "$RESPONSE" | grep -q '"ok":true'; then
    FILE_NAME=$(basename "$FILE_PATH")
    FILE_SIZE_KB=$(echo "scale=1; $FILE_SIZE/1024" | bc)
    echo "File sent successfully to user $USER_ID"
    echo "  File: $FILE_NAME ($FILE_SIZE_KB KB)"
    [ -n "$CAPTION" ] && echo "  Caption: ${CAPTION:0:50}..."
    exit 0
else
    ERROR_DESC=$(echo "$RESPONSE" | grep -o '"description":"[^"]*"' | sed 's/"description":"\([^"]*\)"/\1/')
    echo "ERROR: Telegram API error: $ERROR_DESC" >&2
    echo "Full response: $RESPONSE" >&2
    exit 1
fi
