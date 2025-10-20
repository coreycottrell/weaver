#!/bin/bash
#
# Telegram Infrastructure Status Script
# Shows status of all Telegram components
#
# Usage: ./tools/status_telegram_infrastructure.sh
#

echo "=================================="
echo "  Telegram Infrastructure Status"
echo "=================================="
echo ""

# Function to check process status
check_status() {
    local process_pattern=$1
    local process_name=$2

    if pgrep -f "$process_pattern" > /dev/null; then
        echo "✅ $process_name: RUNNING"
        pgrep -f "$process_pattern" | while read pid; do
            echo "   PID: $pid"
            # Show how long it's been running
            ps -p $pid -o etime= | xargs echo "   Uptime:"
        done
    else
        echo "❌ $process_name: NOT RUNNING"
    fi
}

# Check JSONL Monitor
check_status "openai_telegram_jsonl_monitor.py" "JSONL Monitor"
echo ""

# Check Telegram Bridge
check_status "openai_telegram_bridge.py" "Telegram Bridge"
echo ""

# Show recent activity
echo "=================================="
echo "  Recent Activity (last 10 lines)"
echo "=================================="
echo ""

if [ -f /tmp/openai_telegram_jsonl_monitor.log ]; then
    echo "JSONL Monitor Log:"
    tail -10 /tmp/openai_telegram_jsonl_monitor.log | sed 's/^/  /'
    echo ""
else
    echo "⚠️  No JSONL monitor log found"
    echo ""
fi

# Check for errors
if [ -f /tmp/openai_telegram_jsonl_monitor_error.log ]; then
    ERROR_COUNT=$(wc -l < /tmp/openai_telegram_jsonl_monitor_error.log)
    if [ $ERROR_COUNT -gt 0 ]; then
        echo "⚠️  Errors detected ($ERROR_COUNT lines in error log)"
        echo "Recent errors:"
        tail -5 /tmp/openai_telegram_jsonl_monitor_error.log | sed 's/^/  /'
        echo ""
    fi
fi

# Show config
echo "=================================="
echo "  Configuration"
echo "=================================="
echo ""
if [ -f config/telegram_config.json ]; then
    echo "Session: $(jq -r '.tmux_session' config/telegram_config.json)"
    echo "Poll interval: $(jq -r '.jsonl_monitor.poll_interval_seconds' config/telegram_config.json)s"
    echo "Deduplication: $(jq -r '.jsonl_monitor.deduplication_enabled' config/telegram_config.json)"
else
    echo "⚠️  Config file not found"
fi

echo ""
echo "=================================="
