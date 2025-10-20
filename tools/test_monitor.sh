#!/bin/bash
# Quick diagnostic for Telegram monitor issues
# Usage: bash tools/test_monitor.sh

echo "=== Telegram Monitor Diagnostic ==="
echo

echo "1. tmux session check:"
tmux has-session -t 0 && echo "  ✅ Session exists" || echo "  ❌ Session not found"
echo

echo "2. Buffer capture test:"
LINES=$(tmux capture-pane -t 0:0.0 -p -S -100 2>/dev/null | wc -l)
if [ "$LINES" -gt 0 ]; then
    echo "  ✅ Captured $LINES lines"
else
    echo "  ❌ Buffer capture failed (0 lines)"
fi
echo

echo "3. Marker detection:"
START_COUNT=$(tmux capture-pane -t 0:0.0 -p -S -500 2>/dev/null | grep -c "🤖🎯📱" || echo "0")
END_COUNT=$(tmux capture-pane -t 0:0.0 -p -S -500 2>/dev/null | grep -c "✨🔚" || echo "0")
echo "  Start markers (🤖🎯📱): $START_COUNT"
echo "  End markers (✨🔚): $END_COUNT"

if [ "$START_COUNT" -eq "$END_COUNT" ] && [ "$START_COUNT" -gt 0 ]; then
    echo "  ✅ Markers balanced ($START_COUNT pairs found)"
elif [ "$START_COUNT" -eq 0 ]; then
    echo "  ⚠️  No markers found (Primary may not have responded yet)"
else
    echo "  ❌ Marker mismatch (start: $START_COUNT, end: $END_COUNT)"
fi
echo

echo "4. State file:"
if [ -f ".tg_sessions/monitor_state.json" ]; then
    echo "  ✅ State file exists"
    POS=$(python3 -c "import json; print(json.load(open('.tg_sessions/monitor_state.json')).get('last_buffer_position', 0))" 2>/dev/null || echo "0")
    SEEN=$(python3 -c "import json; print(len(json.load(open('.tg_sessions/monitor_state.json')).get('last_summaries', [])))" 2>/dev/null || echo "0")
    echo "  Buffer position: $POS"
    echo "  Seen summaries: $SEEN"
else
    echo "  ⚠️  State file not found (fresh start)"
fi
echo

echo "5. Send script check:"
if [ -f "tools/send_telegram_direct.py" ]; then
    echo "  ✅ Send script exists"
    if [ -x "tools/send_telegram_direct.py" ]; then
        echo "  ✅ Send script executable"
    else
        echo "  ⚠️  Send script not executable (chmod +x tools/send_telegram_direct.py)"
    fi
else
    echo "  ❌ Send script missing"
fi
echo

echo "6. Config check:"
if [ -f "config/telegram_config.json" ]; then
    echo "  ✅ Config exists"
    python3 -c "
import json
try:
    c=json.load(open('config/telegram_config.json'))
    print(f\"  Bot token: {'✅ set' if c.get('bot_token') else '❌ MISSING'}\")
    print(f\"  Authorized users: {len(c.get('authorized_users', {}))} configured\")
except Exception as e:
    print(f'  ❌ Config parse error: {e}')
" 2>/dev/null
else
    echo "  ❌ Config missing"
fi
echo

echo "7. Monitor process check:"
if pgrep -f "telegram_monitor.py" > /dev/null; then
    PID=$(pgrep -f "telegram_monitor.py")
    echo "  ✅ Monitor running (PID: $PID)"
    echo "     To view logs: tail -f /proc/$PID/fd/1  (if running in tmux/screen)"
else
    echo "  ⚠️  Monitor not running"
    echo "     To start: python3 tools/telegram_monitor.py --interval 300 --tmux-session 0"
fi
echo

echo "8. Recent wrapped messages in buffer:"
RECENT=$(tmux capture-pane -t 0:0.0 -p -S -100 2>/dev/null | grep -A2 "🤖🎯📱" | head -20)
if [ -n "$RECENT" ]; then
    echo "  ✅ Found recent wrapped messages:"
    echo "$RECENT" | sed 's/^/    /'
else
    echo "  ⚠️  No recent wrapped messages in last 100 lines"
    echo "     Primary may not have generated responses yet"
fi
echo

echo "=== End Diagnostic ==="
echo
echo "Quick Tests:"
echo "  • View buffer: tmux capture-pane -t 0:0.0 -p -S -100"
echo "  • Count markers: tmux capture-pane -t 0:0.0 -p -S -500 | grep -c '🤖🎯📱'"
echo "  • Test send: python3 tools/send_telegram_direct.py USER_ID 'Test message'"
echo "  • Start monitor: python3 tools/telegram_monitor.py --interval 300 --tmux-session 0"
echo
