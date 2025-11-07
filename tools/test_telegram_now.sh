#!/bin/bash
# Immediate Telegram test - bypasses monitor, uses direct send
# Run this to verify bot token and user authorization work

PROJECT_DIR="/home/corey/projects/AI-CIV/WEAVER"
cd "$PROJECT_DIR"

echo "=================================================="
echo "Telegram Direct Send Test"
echo "=================================================="
echo ""
echo "Testing bot token and user authorization..."
echo "Sending to Corey (437939400)..."
echo ""

python3 tools/prod/tg/send_telegram_plain.py 437939400 "🚨 TELEGRAM DIAGNOSTIC TEST

If you receive this, direct send works.

ROOT CAUSE: Config pointed at grow_openai (old name), but project was renamed to WEAVER on Nov 2.

FIX: Run tools/fix_telegram_config.sh to update config and restart monitor.

Full diagnostic: to-corey/TELEGRAM-EMERGENCY-DIAGNOSTIC-2025-11-04.md

- tg-bridge
Time: $(date '+%Y-%m-%d %H:%M:%S')"

if [ $? -eq 0 ]; then
    echo "✅ SUCCESS - Message sent to Telegram"
    echo ""
    echo "This means:"
    echo "  ✓ Bot token valid"
    echo "  ✓ User authorized"
    echo "  ✓ Direct send works"
    echo ""
    echo "Next: Fix config and restart monitor"
    echo "  Run: bash tools/fix_telegram_config.sh"
else
    echo "❌ FAILED - Message could not be sent"
    echo ""
    echo "Possible issues:"
    echo "  - Bot token invalid or expired"
    echo "  - Network connectivity problem"
    echo "  - Telegram API down"
    echo ""
    echo "Check: Does tools/prod/tg/send_telegram_plain.py exist?"
    ls -la tools/prod/tg/send_telegram_plain.py
fi
echo ""
echo "=================================================="
