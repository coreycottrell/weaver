#!/bin/bash
# Emergency fix for Telegram configuration after grow_openai → WEAVER rename
# Run this to update Telegram infrastructure to point at correct project

set -e

PROJECT_DIR="/home/corey/projects/AI-CIV/WEAVER"
cd "$PROJECT_DIR"

echo "=================================================="
echo "Telegram Configuration Emergency Fix"
echo "=================================================="
echo ""
echo "Issue: Config was pointing at grow_openai (old name, now fixed)"
echo "Fix: Update to WEAVER (current name)"
echo ""

# Backup current config
echo "1. Backing up current config..."
cp config/telegram_config.json config/telegram_config.json.backup-2025-11-04
echo "   ✓ Backup saved: config/telegram_config.json.backup-2025-11-04"
echo ""

# Fix config with sed
echo "2. Updating configuration..."
sed -i 's|/home/corey/projects/AI-CIV/grow_openai|/home/corey/projects/AI-CIV/WEAVER|g' config/telegram_config.json
sed -i 's|-home-corey-projects-AI-CIV-grow_openai|-home-corey-projects-AI-CIV-WEAVER|g' config/telegram_config.json
echo "   ✓ Config updated (2 path changes)"
echo ""

# Backup and clear monitor state
echo "3. Resetting monitor state..."
if [ -f .tg_sessions/jsonl_monitor_state.json ]; then
    cp .tg_sessions/jsonl_monitor_state.json .tg_sessions/jsonl_monitor_state.json.backup-2025-11-04
    echo "   ✓ State backed up"
fi
echo '{"last_updated": "", "current_session_file": null, "last_processed_offset": 0, "sent_message_hashes": []}' > .tg_sessions/jsonl_monitor_state.json
echo "   ✓ State reset to fresh start"
echo ""

# Stop old monitor if running
echo "4. Stopping old monitor processes..."
if pkill -f "openai_telegram_jsonl_monitor.py"; then
    echo "   ✓ Old monitor stopped"
else
    echo "   ℹ No monitor was running"
fi
sleep 1
echo ""

# Start new monitor with correct config
echo "5. Starting monitor with new config..."
nohup python3 tools/prod/tg/openai_telegram_jsonl_monitor.py >> /tmp/openai_telegram_jsonl_monitor.log 2>&1 &
MONITOR_PID=$!
echo "   ✓ Monitor started (PID: $MONITOR_PID)"
sleep 2
echo ""

# Verify monitor is running
echo "6. Verifying monitor health..."
if ps -p $MONITOR_PID > /dev/null 2>&1; then
    echo "   ✓ Monitor running successfully"

    # Check log for correct project
    sleep 1
    if grep -q "WEAVER" /tmp/openai_telegram_jsonl_monitor.log; then
        echo "   ✓ Log shows WEAVER project (correct)"
    else
        echo "   ⚠ Warning: Check log manually for project name"
    fi
else
    echo "   ✗ Monitor failed to start - check /tmp/openai_telegram_jsonl_monitor.log"
    exit 1
fi
echo ""

# Send test message
echo "7. Sending test message to Corey..."
python3 tools/prod/tg/send_telegram_plain.py 437939400 "🚨 TELEGRAM FIXED - Configuration updated to WEAVER project. Monitor restarted. Auto-detection should work now. - tg-bridge" 2>&1
if [ $? -eq 0 ]; then
    echo "   ✓ Test message sent successfully"
else
    echo "   ✗ Test message failed - check bot token"
fi
echo ""

echo "=================================================="
echo "TELEGRAM FIX COMPLETE"
echo "=================================================="
echo ""
echo "✅ Configuration updated (grow_openai → WEAVER)"
echo "✅ Monitor state reset"
echo "✅ Monitor restarted with new config"
echo "✅ Test message sent to Telegram"
echo ""
echo "Next: Test wrapper detection in Claude Code session:"
echo "  Send: 🤖🎯📱 TEST WRAPPER ✨🔚"
echo "  Should arrive on Telegram within 10 seconds"
echo ""
echo "Logs: /tmp/openai_telegram_jsonl_monitor.log"
echo "Backup: config/telegram_config.json.backup-2025-11-04"
echo ""
