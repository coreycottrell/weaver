#!/bin/bash
# Setup and manage persistent Claude Code tmux session

set -euo pipefail

TMUX_SESSION="3"
PROJECT_DIR="/home/corey/projects/AI-CIV/grow_openai"

###############################################################################
# Functions
###############################################################################

start_session() {
    if tmux has-session -t "$TMUX_SESSION" 2>/dev/null; then
        echo "✅ Session '$TMUX_SESSION' already running"
        echo "Attach with: tmux attach -t $TMUX_SESSION"
        return 0
    fi

    echo "🚀 Starting persistent Claude Code session..."

    # Create detached tmux session with Claude Code
    tmux new-session -d -s "$TMUX_SESSION" -c "$PROJECT_DIR" \
        "claude"

    echo "✅ Session '$TMUX_SESSION' started!"
    echo ""
    echo "Commands:"
    echo "  Attach:  tmux attach -t $TMUX_SESSION"
    echo "  Detach:  Ctrl+B, then D"
    echo "  Status:  ./cron/tmux-setup.sh status"
}

stop_session() {
    if ! tmux has-session -t "$TMUX_SESSION" 2>/dev/null; then
        echo "❌ Session '$TMUX_SESSION' not running"
        return 1
    fi

    echo "🛑 Stopping session '$TMUX_SESSION'..."
    tmux send-keys -t "${TMUX_SESSION}.0" C-c
    sleep 1
    tmux kill-session -t "$TMUX_SESSION"
    echo "✅ Session stopped"
}

attach_session() {
    if ! tmux has-session -t "$TMUX_SESSION" 2>/dev/null; then
        echo "❌ Session '$TMUX_SESSION' not running"
        echo "Start with: ./cron/tmux-setup.sh start"
        return 1
    fi

    echo "📎 Attaching to session '$TMUX_SESSION'..."
    echo "(Press Ctrl+B then D to detach)"
    sleep 1
    tmux attach -t "$TMUX_SESSION"
}

show_status() {
    echo "🎯 Claude Code Persistent Session Status"
    echo "========================================"
    echo ""

    if tmux has-session -t "$TMUX_SESSION" 2>/dev/null; then
        echo "✅ Status: RUNNING"
        echo "Session: $TMUX_SESSION"
        echo ""

        # Show session info
        echo "Session info:"
        tmux list-sessions -F "  #{session_name}: #{session_windows} windows, created #{session_created_string}" | grep "$TMUX_SESSION" || true
        echo ""

        # Show last few lines of output
        echo "Recent output (last 10 lines):"
        tmux capture-pane -t "${TMUX_SESSION}.0" -p -S -10 | sed 's/^/  /'
    else
        echo "❌ Status: NOT RUNNING"
        echo ""
        echo "Start with: ./cron/tmux-setup.sh start"
    fi
}

peek_session() {
    if ! tmux has-session -t "$TMUX_SESSION" 2>/dev/null; then
        echo "❌ Session '$TMUX_SESSION' not running"
        return 1
    fi

    echo "👀 Last 50 lines from session '$TMUX_SESSION':"
    echo "=============================================="
    tmux capture-pane -t "${TMUX_SESSION}.0" -p -S -50
}

send_test() {
    if ! tmux has-session -t "$TMUX_SESSION" 2>/dev/null; then
        echo "❌ Session '$TMUX_SESSION' not running"
        return 1
    fi

    local message="${1:-Hello from tmux send-keys! This is a test injection.}"

    echo "📤 Sending test message to session..."
    tmux send-keys -t "${TMUX_SESSION}.0" -l "$message"
    tmux send-keys -t "${TMUX_SESSION}.0" Enter

    echo "✅ Test message sent!"
    echo ""
    echo "View response with: ./cron/tmux-setup.sh peek"
}

###############################################################################
# Main
###############################################################################

case "${1:-help}" in
    start)
        start_session
        ;;

    stop)
        stop_session
        ;;

    restart)
        stop_session
        sleep 2
        start_session
        ;;

    attach)
        attach_session
        ;;

    status)
        show_status
        ;;

    peek)
        peek_session
        ;;

    test)
        send_test "${2:-}"
        ;;

    help|*)
        echo "Usage: $0 {start|stop|restart|attach|status|peek|test}"
        echo ""
        echo "Commands:"
        echo "  start    - Start persistent Claude Code session in tmux"
        echo "  stop     - Stop the session"
        echo "  restart  - Stop and start the session"
        echo "  attach   - Attach to running session (Ctrl+B D to detach)"
        echo "  status   - Show session status and recent output"
        echo "  peek     - Show last 50 lines without attaching"
        echo "  test     - Send test message to session"
        echo ""
        echo "Examples:"
        echo "  $0 start                           # Start session"
        echo "  $0 status                          # Check if running"
        echo "  $0 test 'Hello Claude!'            # Send test message"
        echo "  $0 attach                          # Interactive attach"
        ;;
esac
