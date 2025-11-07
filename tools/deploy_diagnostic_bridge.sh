#!/bin/bash
# Deploy diagnostic Telegram bridge to investigate duplicate messages

set -e

echo "=================================================="
echo "Deploying Diagnostic Telegram Bridge"
echo "=================================================="
echo ""

# Configuration
PROD_BRIDGE="tools/prod/tg/openai_telegram_bridge.py"
DIAG_BRIDGE="tools/openai_telegram_bridge_diagnostic.py"
DIAG_LOG="/tmp/openai_telegram_bridge_diagnostic.log"
PROJECT_DIR="/home/corey/projects/AI-CIV/WEAVER"

cd "$PROJECT_DIR"

echo "Step 1: Stop production bridge..."
PROD_PID=$(ps aux | grep "$PROD_BRIDGE" | grep -v grep | awk '{print $2}')
if [ -n "$PROD_PID" ]; then
    echo "  Killing production bridge (PID: $PROD_PID)"
    kill $PROD_PID
    sleep 2
    echo "  ✓ Production bridge stopped"
else
    echo "  ⚠️ Production bridge not running (this is OK)"
fi

echo ""
echo "Step 2: Verify diagnostic bridge exists..."
if [ ! -f "$DIAG_BRIDGE" ]; then
    echo "  ❌ ERROR: $DIAG_BRIDGE not found!"
    exit 1
fi
echo "  ✓ Diagnostic bridge found"

echo ""
echo "Step 3: Clear old diagnostic log..."
if [ -f "$DIAG_LOG" ]; then
    mv "$DIAG_LOG" "${DIAG_LOG}.old"
    echo "  ✓ Old log backed up to ${DIAG_LOG}.old"
else
    echo "  ℹ️ No old log to clear"
fi

echo ""
echo "Step 4: Start diagnostic bridge..."
nohup python3 "$DIAG_BRIDGE" >> "$DIAG_LOG" 2>&1 &
sleep 3

DIAG_PID=$(ps aux | grep "$DIAG_BRIDGE" | grep -v grep | awk '{print $2}')
if [ -n "$DIAG_PID" ]; then
    echo "  ✓ Diagnostic bridge started (PID: $DIAG_PID)"
else
    echo "  ❌ ERROR: Diagnostic bridge failed to start!"
    echo "  Check log: tail -20 $DIAG_LOG"
    exit 1
fi

echo ""
echo "=================================================="
echo "Diagnostic Bridge Deployed Successfully"
echo "=================================================="
echo ""
echo "Status:"
echo "  Process: $DIAG_PID"
echo "  Log: $DIAG_LOG"
echo "  Production: STOPPED"
echo ""
echo "Next Steps:"
echo "  1. Watch log: tail -f $DIAG_LOG"
echo "  2. Send test message via Telegram"
echo "  3. Look for trace IDs and duplicate detection"
echo "  4. Use /status command for metrics"
echo ""
echo "Rollback:"
echo "  kill $DIAG_PID"
echo "  ./tools/prod/tg/start_telegram_infrastructure.sh"
echo ""
echo "See: tools/DUPLICATE-DIAGNOSTIC-PROCEDURE.md for full testing guide"
echo "=================================================="
