#!/bin/bash
#
# 🔒 PRODUCTION FILE - DO NOT MODIFY 🔒
#
# This file is operational and tested in production.
# To make changes:
#   1. Create variant: tools/stop_telegram_infrastructure_v2.sh
#   2. Test thoroughly
#   3. Copy to tools/prod/tg/ only after validation
#
# Location: tools/prod/tg/ (production lock - agents should not modify)
# Last Production Update: 2025-10-20
#
# ============================================================================
#
# Telegram Infrastructure Stop Script
# Stops both JSONL monitor and Telegram bridge
#
# Usage: ./tools/prod/tg/stop_telegram_infrastructure.sh
#

echo "=================================="
echo "  Stopping Telegram Infrastructure"
echo "=================================="
echo ""

# Function to kill process by name pattern
kill_process() {
    local process_pattern=$1
    local process_name=$2

    echo "Stopping $process_name..."

    if pgrep -f "$process_pattern" > /dev/null; then
        pkill -f "$process_pattern"
        sleep 1

        if pgrep -f "$process_pattern" > /dev/null; then
            echo "⚠️  $process_name still running, force killing..."
            pkill -9 -f "$process_pattern"
            sleep 1
        fi

        if ! pgrep -f "$process_pattern" > /dev/null; then
            echo "✅ $process_name stopped"
        else
            echo "❌ Failed to stop $process_name"
        fi
    else
        echo "⚠️  $process_name not running"
    fi
}

# Stop JSONL Monitor
kill_process "tools/prod/tg/openai_telegram_jsonl_monitor.py" "JSONL Monitor"

echo ""

# Stop Telegram Bridge
kill_process "tools/prod/tg/openai_telegram_bridge.py" "Telegram Bridge"

echo ""
echo "=================================="
echo "  All processes stopped"
echo "=================================="
