#!/bin/bash
#
# BOOP Cadence Runner - Variable interval BOOP execution
#
# Usage:
#   ./cadence_runner.sh morning   # 2x morning BOOPs at 30 min, then switch to content
#   ./cadence_runner.sh content   # Content day at 60 min cadence
#   ./cadence_runner.sh stop      # Stop running cadence
#
# Created: 2026-01-05

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
CADENCE_STATE="$PROJECT_DIR/.claude/cadence-state.json"
CADENCE_PID="$PROJECT_DIR/.claude/cadence-runner.pid"
CADENCE_LOG="$PROJECT_DIR/.claude/cadence-runner.log"

# BOOP Messages
MORNING_BOOP='[MORNING-BOOP] Wake-up cycle. READ: CLAUDE.md, CLAUDE-CORE.md, CLAUDE-OPS.md, scratch-pad.md --- TASKS: [ ] Check email (human-liaison) [ ] Check comms hub [ ] Check Bluesky notifs+DMs (bsky-boop-manager) [ ] Share-watching (reposts/quotes) [ ] Verify responses SENT. WRAP: 🤖🎯📱...✨🔚'

CONTENT_BOOP='[CONTENT-DAY-BOOP] Content production cycle. READ: CLAUDE.md, scratch-pad.md --- TASKS: [ ] Check Bluesky notifs (quick) [ ] intel-scan if not done today [ ] Progress on daily blog [ ] bsky-engage (1-2 quality) [ ] Check shares of our content [ ] Verify responses SENT. WRAP: 🤖🎯📱...✨🔚'

log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $*" | tee -a "$CADENCE_LOG"
}

inject_boop() {
    local message="$1"
    local spine="${2:-weaver-spine}"  # Default to weaver-spine
    local session_file="$PROJECT_DIR/.current_session"

    if [ -f "$session_file" ]; then
        local session_name=$(cat "$session_file")

        # Step 1: Inject spine FIRST (identity grounding)
        log "Injecting spine: /$spine"
        tmux send-keys -t "$session_name" "/$spine" Enter 2>/dev/null || {
            log "WARNING: Could not inject spine to tmux session $session_name"
        }

        # Wait for spine to process (3 seconds)
        sleep 3

        # Step 2: Inject BOOP message
        tmux send-keys -t "$session_name" "$message" Enter 2>/dev/null || {
            log "WARNING: Could not inject BOOP to tmux session $session_name"
            return 1
        }
        log "✓ Injected BOOP to session: $session_name (with $spine pre-injection)"
    else
        log "WARNING: No .current_session file found"
        return 1
    fi
}

update_state() {
    local mode="$1"
    local interval="$2"
    local count="$3"

    cat > "$CADENCE_STATE" << EOF
{
  "mode": "$mode",
  "interval_minutes": $interval,
  "boop_count": $count,
  "started": "$(date -u '+%Y-%m-%dT%H:%M:%SZ')",
  "last_boop": "$(date -u '+%Y-%m-%dT%H:%M:%SZ')"
}
EOF
}

run_morning_then_content() {
    log "=== MORNING MODE: 2x BOOPs at 30 min cadence ==="

    # First morning BOOP (with weaver-spine for full identity grounding)
    log "Morning BOOP 1/2"
    inject_boop "$MORNING_BOOP" "weaver-spine"
    update_state "morning" 30 1

    # Wait 30 minutes
    log "Waiting 30 minutes for next morning BOOP..."
    sleep 1800

    # Second morning BOOP
    log "Morning BOOP 2/2"
    inject_boop "$MORNING_BOOP" "weaver-spine"
    update_state "morning" 30 2

    log "=== Switching to CONTENT DAY MODE: 60 min cadence ==="

    # Content day loop (with delegation-spine for work mode)
    local content_count=0
    while true; do
        # Wait 60 minutes
        log "Waiting 60 minutes for next content BOOP..."
        sleep 3600

        content_count=$((content_count + 1))
        log "Content BOOP #$content_count"
        inject_boop "$CONTENT_BOOP" "delegation-spine"
        update_state "content" 60 $content_count
    done
}

run_content_only() {
    log "=== CONTENT DAY MODE: 60 min cadence ==="

    local content_count=0
    while true; do
        content_count=$((content_count + 1))
        log "Content BOOP #$content_count"
        inject_boop "$CONTENT_BOOP" "delegation-spine"
        update_state "content" 60 $content_count

        log "Waiting 60 minutes..."
        sleep 3600
    done
}

stop_cadence() {
    if [ -f "$CADENCE_PID" ]; then
        local pid=$(cat "$CADENCE_PID")
        if kill -0 "$pid" 2>/dev/null; then
            kill "$pid"
            log "Stopped cadence runner (PID: $pid)"
        fi
        rm -f "$CADENCE_PID"
    else
        log "No cadence runner running"
    fi
}

status() {
    if [ -f "$CADENCE_STATE" ]; then
        cat "$CADENCE_STATE"
    else
        echo "No cadence state found"
    fi

    if [ -f "$CADENCE_PID" ]; then
        local pid=$(cat "$CADENCE_PID")
        if kill -0 "$pid" 2>/dev/null; then
            echo "Cadence runner active (PID: $pid)"
        else
            echo "Cadence runner not running (stale PID file)"
        fi
    else
        echo "Cadence runner not running"
    fi
}

# Main
case "${1:-status}" in
    morning)
        stop_cadence
        log "Starting morning -> content cadence..."
        run_morning_then_content &
        echo $! > "$CADENCE_PID"
        log "Cadence runner started (PID: $!)"
        ;;
    content)
        stop_cadence
        log "Starting content-only cadence..."
        run_content_only &
        echo $! > "$CADENCE_PID"
        log "Cadence runner started (PID: $!)"
        ;;
    stop)
        stop_cadence
        ;;
    status)
        status
        ;;
    *)
        echo "Usage: $0 {morning|content|stop|status}"
        exit 1
        ;;
esac
