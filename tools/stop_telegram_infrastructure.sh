#!/bin/bash
#
# Telegram Infrastructure Stop Script
# Stops both JSONL monitor and Telegram bridge
#
# Usage: ./tools/stop_telegram_infrastructure.sh
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
kill_process "openai_telegram_jsonl_monitor.py" "JSONL Monitor"

echo ""

# Stop Telegram Bridge
kill_process "openai_telegram_bridge.py" "Telegram Bridge"

echo ""
echo "=================================="
echo "  All processes stopped"
echo "=================================="
