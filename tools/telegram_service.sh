#!/bin/bash
# WEAVER Telegram Bot Service Manager
# Usage: ./telegram_service.sh [start|stop|restart|status|logs|health]

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
BOT_SCRIPT="$SCRIPT_DIR/telegram_unified.py"
PID_FILE="/tmp/weaver_telegram.pid"
LOG_FILE="/tmp/telegram_weaver.log"
HEALTH_LOG="/tmp/telegram_health.log"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

get_pid() {
    if [ -f "$PID_FILE" ]; then
        cat "$PID_FILE"
    else
        # Try to find running process
        pgrep -f "python3.*telegram_unified.py" | head -1
    fi
}

is_running() {
    local pid=$(get_pid)
    if [ -n "$pid" ] && kill -0 "$pid" 2>/dev/null; then
        return 0
    fi
    return 1
}

start_bot() {
    if is_running; then
        echo -e "${YELLOW}Bot is already running (PID: $(get_pid))${NC}"
        return 0
    fi

    echo -e "${GREEN}Starting WEAVER Telegram bot...${NC}"
    cd "$SCRIPT_DIR/.."
    nohup python3 "$BOT_SCRIPT" > "$LOG_FILE" 2>&1 &
    local pid=$!
    echo $pid > "$PID_FILE"

    sleep 2
    if is_running; then
        echo -e "${GREEN}Bot started successfully (PID: $pid)${NC}"
        # Show first few lines of log
        head -5 "$LOG_FILE"
        return 0
    else
        echo -e "${RED}Bot failed to start. Check logs: $LOG_FILE${NC}"
        tail -20 "$LOG_FILE"
        return 1
    fi
}

stop_bot() {
    local pid=$(get_pid)
    if [ -z "$pid" ]; then
        echo -e "${YELLOW}Bot is not running${NC}"
        rm -f "$PID_FILE"
        return 0
    fi

    echo -e "${YELLOW}Stopping bot (PID: $pid)...${NC}"
    kill "$pid" 2>/dev/null

    # Wait up to 5 seconds for graceful shutdown
    for i in {1..10}; do
        if ! kill -0 "$pid" 2>/dev/null; then
            echo -e "${GREEN}Bot stopped gracefully${NC}"
            rm -f "$PID_FILE"
            return 0
        fi
        sleep 0.5
    done

    # Force kill if still running
    echo -e "${YELLOW}Force killing bot...${NC}"
    kill -9 "$pid" 2>/dev/null
    rm -f "$PID_FILE"
    echo -e "${GREEN}Bot stopped${NC}"
}

restart_bot() {
    echo -e "${YELLOW}Restarting WEAVER Telegram bot...${NC}"
    stop_bot
    sleep 1
    start_bot
}

status_bot() {
    if is_running; then
        local pid=$(get_pid)
        echo -e "${GREEN}Bot is RUNNING${NC}"
        echo "  PID: $pid"
        echo "  Log: $LOG_FILE"
        echo ""
        echo "Recent log:"
        tail -10 "$LOG_FILE" 2>/dev/null || echo "  (no log file)"
    else
        echo -e "${RED}Bot is NOT RUNNING${NC}"
        if [ -f "$LOG_FILE" ]; then
            echo ""
            echo "Last log entries:"
            tail -10 "$LOG_FILE"
        fi
    fi
}

show_logs() {
    if [ -f "$LOG_FILE" ]; then
        tail -f "$LOG_FILE"
    else
        echo -e "${RED}No log file found at $LOG_FILE${NC}"
    fi
}

health_check() {
    local issues=0
    echo "=== WEAVER Telegram Health Check ==="
    echo ""

    # 1. Check if bot is running
    echo -n "1. Bot process: "
    if is_running; then
        echo -e "${GREEN}OK${NC} (PID: $(get_pid))"
    else
        echo -e "${RED}NOT RUNNING${NC}"
        issues=$((issues + 1))
    fi

    # 2. Check tmux sessions
    echo -n "2. WEAVER tmux sessions: "
    local weaver_sessions=$(tmux list-sessions -F "#{session_name}" 2>/dev/null | grep "weaver-primary-" | wc -l)
    if [ "$weaver_sessions" -gt 0 ]; then
        echo -e "${GREEN}OK${NC} ($weaver_sessions found)"
        tmux list-sessions -F "#{session_name}" 2>/dev/null | grep "weaver-primary-" | while read s; do
            echo "     - $s"
        done
    else
        echo -e "${RED}NONE FOUND${NC}"
        issues=$((issues + 1))
    fi

    # 3. Check log freshness
    echo -n "3. Log freshness: "
    if [ -f "$LOG_FILE" ]; then
        local age=$(($(date +%s) - $(stat -c %Y "$LOG_FILE")))
        if [ "$age" -lt 60 ]; then
            echo -e "${GREEN}OK${NC} (updated ${age}s ago)"
        else
            echo -e "${YELLOW}STALE${NC} (${age}s old)"
            issues=$((issues + 1))
        fi
    else
        echo -e "${RED}NO LOG${NC}"
        issues=$((issues + 1))
    fi

    # 4. Check config file
    echo -n "4. Config file: "
    local config_file="$SCRIPT_DIR/../config/telegram_config.json"
    if [ -f "$config_file" ]; then
        if python3 -c "import json; json.load(open('$config_file'))" 2>/dev/null; then
            echo -e "${GREEN}OK${NC}"
        else
            echo -e "${RED}INVALID JSON${NC}"
            issues=$((issues + 1))
        fi
    else
        echo -e "${RED}MISSING${NC}"
        issues=$((issues + 1))
    fi

    # 5. Check Telegram API connectivity
    echo -n "5. Telegram API: "
    local token=$(python3 -c "import json; print(json.load(open('$config_file'))['bot_token'])" 2>/dev/null)
    if [ -n "$token" ]; then
        local api_result=$(curl -s "https://api.telegram.org/bot${token}/getMe" 2>/dev/null)
        if echo "$api_result" | grep -q '"ok":true'; then
            echo -e "${GREEN}OK${NC}"
        else
            echo -e "${RED}FAILED${NC}"
            issues=$((issues + 1))
        fi
    else
        echo -e "${RED}NO TOKEN${NC}"
        issues=$((issues + 1))
    fi

    echo ""
    echo "=== Summary ==="
    if [ "$issues" -eq 0 ]; then
        echo -e "${GREEN}All checks passed!${NC}"
    else
        echo -e "${RED}$issues issue(s) found${NC}"
    fi

    return $issues
}

auto_recover() {
    echo "=== Auto-Recovery Mode ==="

    # Run health check
    health_check
    local health_status=$?

    if [ "$health_status" -ne 0 ]; then
        echo ""
        echo -e "${YELLOW}Issues detected. Attempting recovery...${NC}"

        # Stop any zombie processes
        pkill -f "telegram_unified.py" 2>/dev/null
        sleep 1

        # Start fresh
        start_bot

        # Verify
        sleep 3
        if is_running; then
            echo -e "${GREEN}Recovery successful!${NC}"
        else
            echo -e "${RED}Recovery failed. Manual intervention needed.${NC}"
            exit 1
        fi
    else
        echo -e "${GREEN}No recovery needed.${NC}"
    fi
}

case "$1" in
    start)
        start_bot
        ;;
    stop)
        stop_bot
        ;;
    restart)
        restart_bot
        ;;
    status)
        status_bot
        ;;
    logs)
        show_logs
        ;;
    health)
        health_check
        ;;
    recover)
        auto_recover
        ;;
    *)
        echo "WEAVER Telegram Bot Service Manager"
        echo ""
        echo "Usage: $0 {start|stop|restart|status|logs|health|recover}"
        echo ""
        echo "Commands:"
        echo "  start   - Start the bot"
        echo "  stop    - Stop the bot"
        echo "  restart - Restart the bot"
        echo "  status  - Show bot status and recent logs"
        echo "  logs    - Tail the log file (Ctrl+C to exit)"
        echo "  health  - Run health check"
        echo "  recover - Auto-recover from issues"
        exit 1
        ;;
esac
