#!/bin/bash
#
# 🔒 PRODUCTION FILE - DO NOT MODIFY 🔒
#
# This file is operational and tested in production.
# To make changes:
#   1. Create variant: tools/start_telegram_infrastructure_v2.sh
#   2. Test thoroughly
#   3. Copy to tools/prod/tg/ only after validation
#
# Location: tools/prod/tg/ (production lock - agents should not modify)
# Last Production Update: 2025-10-20
#
# ============================================================================
#
# Telegram Infrastructure Startup Script
# Starts both JSONL monitor and Telegram bridge for grow_openai
#
# Usage: ./tools/prod/tg/start_telegram_infrastructure.sh
#

set -e  # Exit on error

PROJECT_ROOT="/home/corey/projects/AI-CIV/grow_openai"
cd "$PROJECT_ROOT"

echo "=================================="
echo "  Telegram Infrastructure Startup"
echo "=================================="
echo ""

# Function to check if process is already running
check_running() {
    local process_name=$1
    if pgrep -f "$process_name" > /dev/null; then
        return 0  # Running
    else
        return 1  # Not running
    fi
}

# Function to start a process
start_process() {
    local script_path=$1
    local process_name=$2
    local log_file=$3

    echo "Starting $process_name..."

    if check_running "$script_path"; then
        echo "⚠️  $process_name already running"
        pgrep -f "$script_path" | while read pid; do
            echo "   PID: $pid"
        done
        return 0
    fi

    # Start process in background
    nohup python3 "$script_path" >> "$log_file" 2>&1 &
    local pid=$!

    sleep 2

    if ps -p $pid > /dev/null 2>&1; then
        echo "✅ $process_name started (PID: $pid)"
        return 0
    else
        echo "❌ $process_name failed to start"
        echo "   Check log: $log_file"
        return 1
    fi
}

# Start JSONL Monitor
echo ""
echo "1. JSONL Monitor"
echo "   Watches Claude Code logs for wrapped messages"
echo "   Sends to Telegram when detected"
echo ""

start_process \
    "tools/prod/tg/openai_telegram_jsonl_monitor.py" \
    "JSONL Monitor" \
    "/tmp/openai_telegram_jsonl_monitor.log"

# Start Telegram Bridge
echo ""
echo "2. Telegram Bridge"
echo "   Receives messages from Telegram"
echo "   Injects into tmux session 5"
echo ""

start_process \
    "tools/prod/tg/openai_telegram_bridge.py" \
    "Telegram Bridge" \
    "/tmp/openai_telegram_bridge.log"

# Summary
echo ""
echo "=================================="
echo "  Status Summary"
echo "=================================="
echo ""

if check_running "tools/prod/tg/openai_telegram_jsonl_monitor.py"; then
    echo "✅ JSONL Monitor: RUNNING"
    pgrep -f "tools/prod/tg/openai_telegram_jsonl_monitor.py" | while read pid; do
        echo "   PID: $pid"
    done
else
    echo "❌ JSONL Monitor: NOT RUNNING"
fi

if check_running "tools/prod/tg/openai_telegram_bridge.py"; then
    echo "✅ Telegram Bridge: RUNNING"
    pgrep -f "tools/prod/tg/openai_telegram_bridge.py" | while read pid; do
        echo "   PID: $pid"
    done
else
    echo "❌ Telegram Bridge: NOT RUNNING"
fi

echo ""
echo "Logs:"
echo "  JSONL Monitor: /tmp/openai_telegram_jsonl_monitor.log"
echo "  JSONL Errors:  /tmp/openai_telegram_jsonl_monitor_error.log"
echo "  Bridge:        /tmp/openai_telegram_bridge.log"
echo ""
echo "To stop:"
echo "  tools/prod/tg/stop_telegram_infrastructure.sh"
echo ""
echo "=================================="
