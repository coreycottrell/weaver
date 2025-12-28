#!/bin/bash
# Telegram Quick Fix - Stop all, verify config, restart, test
#
# Use this when Telegram is reported down.
# It will:
#   1. Stop any running telegram processes
#   2. Verify config is valid
#   3. Test API connectivity
#   4. Restart bridge (if needed)
#   5. Send test message
#
# Usage: bash tools/telegram_quick_fix.sh

set -e

PROJECT_DIR="/home/corey/projects/AI-CIV/WEAVER"
cd "$PROJECT_DIR"

echo "=============================================="
echo "Telegram Quick Fix"
echo "=============================================="
echo ""

# Step 1: Stop existing processes
echo "[Step 1] Stopping existing Telegram processes..."
pkill -f "telegram_bridge" 2>/dev/null || true
pkill -f "telegram_monitor" 2>/dev/null || true
pkill -f "telegram_jsonl" 2>/dev/null || true
sleep 2
echo "Done."
echo ""

# Step 2: Verify config
echo "[Step 2] Verifying configuration..."
if [ ! -f config/telegram_config.json ]; then
    echo "ERROR: Config file not found at config/telegram_config.json"
    exit 1
fi

# Check if bot_token exists and is not empty
BOT_TOKEN=$(python3 -c "import json; print(json.load(open('config/telegram_config.json')).get('bot_token', ''))")
if [ -z "$BOT_TOKEN" ]; then
    echo "ERROR: bot_token is missing or empty in config"
    exit 1
fi
echo "Config valid. Bot token: ${BOT_TOKEN:0:10}...${BOT_TOKEN: -5}"
echo ""

# Step 3: Test API connectivity
echo "[Step 3] Testing Telegram Bot API..."
python3 tools/telegram_health_check.py
HEALTH_EXIT=$?
if [ $HEALTH_EXIT -ne 0 ]; then
    echo ""
    echo "ERROR: Health check failed with exit code $HEALTH_EXIT"
    echo "Cannot proceed with fix until API connection works."
    exit 1
fi
echo ""

# Step 4: Ask about bridge restart
echo "[Step 4] Bridge process status..."
if ps aux | grep -E "(openai_telegram_bridge|telegram_bridge)" | grep -v grep | grep -v quick_fix > /dev/null; then
    echo "Bridge already running:"
    ps aux | grep -E "(openai_telegram_bridge|telegram_bridge)" | grep -v grep | grep -v quick_fix
else
    echo "No bridge process running."
    echo ""
    echo "To start the bridge (for bidirectional messaging), run:"
    echo "  nohup python3 tools/openai_telegram_bridge.py > /tmp/openai_telegram_bridge.log 2>&1 &"
    echo ""
    echo "Note: Bridge is optional for outbound-only messaging."
fi
echo ""

# Step 5: Send test message
echo "[Step 5] Sending test message to verify full connectivity..."
python3 tools/telegram_health_check.py --send
TEST_EXIT=$?
if [ $TEST_EXIT -ne 0 ]; then
    echo ""
    echo "WARNING: Test message send failed."
    echo "This might mean Corey needs to /start the bot conversation."
    echo ""
    echo "Manual test:"
    echo "  python3 tools/send_telegram_plain.py 437939400 'Test from WEAVER'"
else
    echo ""
    echo "=============================================="
    echo "Telegram Fixed and Working!"
    echo "=============================================="
fi

echo ""
echo "Summary of available commands:"
echo ""
echo "  # Send message manually:"
echo "  python3 tools/send_telegram_plain.py 437939400 'Your message here'"
echo ""
echo "  # Run health check:"
echo "  python3 tools/telegram_health_check.py --send"
echo ""
echo "  # Check logs:"
echo "  tail -20 /tmp/telegram_health_check.log"
echo "  tail -20 /tmp/openai_telegram_bridge.log"
echo ""
