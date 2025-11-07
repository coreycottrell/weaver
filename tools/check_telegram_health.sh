#!/bin/bash
# Quick Telegram infrastructure health check
# Shows what's running and recent activity

echo "=================================================="
echo "Telegram Infrastructure Health Check"
echo "=================================================="
echo ""

PROJECT_DIR="/home/corey/projects/AI-CIV/WEAVER"
cd "$PROJECT_DIR"

echo "=== Process Status ==="
echo ""

# Check for production bridge
PROD_BRIDGE=$(ps aux | grep "tools/prod/tg/openai_telegram_bridge.py" | grep -v grep)
if [ -n "$PROD_BRIDGE" ]; then
    echo "✓ Production Bridge RUNNING"
    echo "  $PROD_BRIDGE" | awk '{print "  PID:", $2, "CPU:", $3"%", "MEM:", $4"%", "Started:", $9}'
else
    echo "✗ Production Bridge NOT RUNNING"
fi

# Check for diagnostic bridge
DIAG_BRIDGE=$(ps aux | grep "openai_telegram_bridge_diagnostic.py" | grep -v grep)
if [ -n "$DIAG_BRIDGE" ]; then
    echo "✓ Diagnostic Bridge RUNNING"
    echo "  $DIAG_BRIDGE" | awk '{print "  PID:", $2, "CPU:", $3"%", "MEM:", $4"%", "Started:", $9}'
else
    echo "✗ Diagnostic Bridge NOT RUNNING"
fi

# Check for JSONL monitor
JSONL_MON=$(ps aux | grep "openai_telegram_jsonl_monitor.py" | grep -v grep)
if [ -n "$JSONL_MON" ]; then
    echo "✓ JSONL Monitor RUNNING"
    echo "  $JSONL_MON" | awk '{print "  PID:", $2, "CPU:", $3"%", "MEM:", $4"%", "Started:", $9}'
else
    echo "✗ JSONL Monitor NOT RUNNING"
fi

echo ""
echo "=== Recent Activity ==="
echo ""

# Production bridge log
if [ -f /tmp/openai_telegram_bridge.log ]; then
    echo "Production Bridge (last 3 lines):"
    tail -3 /tmp/openai_telegram_bridge.log | sed 's/^/  /'
    echo ""
fi

# Diagnostic bridge log
if [ -f /tmp/openai_telegram_bridge_diagnostic.log ]; then
    echo "Diagnostic Bridge (last 3 lines):"
    tail -3 /tmp/openai_telegram_bridge_diagnostic.log | sed 's/^/  /'
    echo ""
fi

# JSONL monitor log
if [ -f /tmp/openai_telegram_jsonl_monitor.log ]; then
    echo "JSONL Monitor (last 3 lines):"
    tail -3 /tmp/openai_telegram_jsonl_monitor.log | sed 's/^/  /'
    echo ""
fi

echo "=== Configuration ==="
echo ""
if [ -f config/telegram_config.json ]; then
    echo "tmux_session: $(grep tmux_session config/telegram_config.json | head -1)"
    echo "response_timeout: $(grep response_timeout config/telegram_config.json)"
    echo "authorized_users: $(grep -A 1 authorized_users config/telegram_config.json | tail -1)"
else
    echo "⚠️ Config file not found: config/telegram_config.json"
fi

echo ""
echo "=== tmux Status ==="
echo ""
tmux list-sessions 2>/dev/null || echo "⚠️ No tmux sessions running"

echo ""
echo "=== Diagnostic Files Available ==="
echo ""
if [ -f tools/openai_telegram_bridge_diagnostic.py ]; then
    echo "✓ Diagnostic bridge: tools/openai_telegram_bridge_diagnostic.py"
else
    echo "✗ Diagnostic bridge not found"
fi

if [ -f tools/deploy_diagnostic_bridge.sh ]; then
    echo "✓ Deployment script: tools/deploy_diagnostic_bridge.sh"
else
    echo "✗ Deployment script not found"
fi

if [ -f tools/DUPLICATE-DIAGNOSTIC-PROCEDURE.md ]; then
    echo "✓ Testing guide: tools/DUPLICATE-DIAGNOSTIC-PROCEDURE.md"
else
    echo "✗ Testing guide not found"
fi

echo ""
echo "=================================================="
echo "Health Check Complete"
echo "=================================================="
echo ""
echo "To deploy diagnostic bridge:"
echo "  bash tools/deploy_diagnostic_bridge.sh"
echo ""
echo "To watch diagnostic log:"
echo "  tail -f /tmp/openai_telegram_bridge_diagnostic.log"
echo ""
echo "To check detailed logs:"
echo "  tail -50 /tmp/openai_telegram_bridge.log"
echo "  tail -50 /tmp/openai_telegram_bridge_diagnostic.log"
echo "  tail -50 /tmp/openai_telegram_jsonl_monitor.log"
echo ""
