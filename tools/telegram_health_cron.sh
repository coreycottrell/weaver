#!/bin/bash
# WEAVER Telegram Health Check - Run via cron
# Add to crontab: */5 * * * * /home/corey/projects/AI-CIV/WEAVER/tools/telegram_health_cron.sh
#
# This script checks if the Telegram bot is healthy and restarts it if needed.

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
LOG_FILE="/tmp/telegram_health_cron.log"
BOT_LOG="/tmp/telegram_weaver.log"
MAX_LOG_AGE=300  # 5 minutes - restart if log is older

log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" >> "$LOG_FILE"
}

# Check if bot process is running
is_running() {
    pgrep -f "python3.*telegram_unified.py" > /dev/null 2>&1
}

# Check if log file is fresh (updated recently)
is_log_fresh() {
    if [ ! -f "$BOT_LOG" ]; then
        return 1
    fi
    local age=$(($(date +%s) - $(stat -c %Y "$BOT_LOG")))
    [ "$age" -lt "$MAX_LOG_AGE" ]
}

# Check if tmux session exists
has_tmux_session() {
    tmux list-sessions -F "#{session_name}" 2>/dev/null | grep -q "weaver-primary-"
}

# Start the bot
start_bot() {
    log "Starting bot..."
    cd "$SCRIPT_DIR/.."
    pkill -f "telegram_unified.py" 2>/dev/null
    sleep 1
    nohup python3 "$SCRIPT_DIR/telegram_unified.py" > "$BOT_LOG" 2>&1 &
    sleep 2
    if is_running; then
        log "Bot started successfully (PID: $(pgrep -f 'telegram_unified.py'))"
        return 0
    else
        log "ERROR: Failed to start bot"
        return 1
    fi
}

# Main health check
main() {
    local needs_restart=0
    local reason=""

    # Check 1: Is process running?
    if ! is_running; then
        needs_restart=1
        reason="Process not running"
    fi

    # Check 2: Is log fresh? (only if process is "running")
    if [ "$needs_restart" -eq 0 ] && ! is_log_fresh; then
        needs_restart=1
        reason="Log file stale (possible hang)"
    fi

    # Check 3: Does tmux session exist? (if not, bot can't inject)
    if ! has_tmux_session; then
        # Don't restart, but log warning
        log "WARNING: No WEAVER tmux session found - bot will wait"
    fi

    # Restart if needed
    if [ "$needs_restart" -eq 1 ]; then
        log "Health check FAILED: $reason"
        start_bot
    fi
}

# Run
main
