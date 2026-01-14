#!/bin/bash
#
# Hourly BOOP Cron Script - Bluesky Engagement Automation
#
# Purpose: Inject hourly BOOP cycle into running WEAVER session
# Features:
#   - Injects delegation-spine BEFORE each BOOP (identity grounding)
#   - Finds active WEAVER tmux session automatically
#   - Graceful handling when no session exists
#
# Usage:
#   ./hourly_boop_cron.sh           # Normal BOOP
#   ./hourly_boop_cron.sh morning   # Morning BOOP (weaver-spine instead)
#
# Cron entry (hourly):
#   0 * * * * /home/corey/projects/AI-CIV/WEAVER/tools/hourly_boop_cron.sh >> /home/corey/projects/AI-CIV/WEAVER/.claude/hourly-boop.log 2>&1
#
# Created: 2026-01-06

set -euo pipefail

PROJECT_DIR="/home/corey/projects/AI-CIV/WEAVER"
LOG_FILE="$PROJECT_DIR/.claude/hourly-boop.log"
SESSION_FILE="$PROJECT_DIR/.current_session"

# BOOP Messages
HOURLY_BOOP='[HOURLY-BOOP] Bluesky cycle. READ: scratch-pad.md --- TASKS: [ ] Check Bluesky notifs+DMs (bsky-boop-manager) [ ] Reply to engagement (prioritize Corey, sister CIVs, questions) [ ] Check quote shares [ ] Verify responses SENT. WRAP: telegram emoji format'

MORNING_BOOP='[MORNING-BOOP] Wake-up cycle. READ: CLAUDE.md, CLAUDE-CORE.md, CLAUDE-OPS.md, scratch-pad.md --- TASKS: [ ] Check email (human-liaison) [ ] Check comms hub [ ] Check Bluesky notifs+DMs (bsky-boop-manager) [ ] Share-watching (reposts/quotes) [ ] Verify responses SENT. WRAP: telegram emoji format'

log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $*"
}

get_weaver_session() {
    # Try .current_session file first
    if [ -f "$SESSION_FILE" ]; then
        local session_name=$(cat "$SESSION_FILE")
        if tmux has-session -t "$session_name" 2>/dev/null; then
            echo "$session_name"
            return 0
        fi
    fi

    # Fallback: find most recent weaver-primary session
    local session=$(tmux list-sessions -F "#{session_name}" 2>/dev/null | grep "^weaver-primary" | tail -1)
    if [ -n "$session" ]; then
        echo "$session"
        return 0
    fi

    return 1
}

inject_boop() {
    local session_name="$1"
    local spine="$2"
    local boop_message="$3"
    local pane="${session_name}:0.0"

    # Step 1: Inject spine (identity grounding BEFORE work)
    log "Injecting spine: /$spine"
    tmux send-keys -t "$pane" -l "/$spine" 2>/dev/null || {
        log "ERROR: Failed to send spine text"
        return 1
    }

    # 5x Enter with delays (Claude Code sometimes needs several)
    sleep 0.3
    tmux send-keys -t "$pane" "Enter"
    sleep 0.5
    tmux send-keys -t "$pane" "Enter"
    sleep 0.5
    tmux send-keys -t "$pane" "Enter"
    sleep 0.3
    tmux send-keys -t "$pane" "Enter"
    sleep 0.3
    tmux send-keys -t "$pane" "Enter"

    # Wait for spine to process
    log "Waiting for spine to process..."
    sleep 3

    # Step 2: Inject BOOP message
    log "Injecting BOOP message"
    tmux send-keys -t "$pane" -l "$boop_message" 2>/dev/null || {
        log "ERROR: Failed to send BOOP text"
        return 1
    }

    # 5x Enter with delays for BOOP message
    sleep 0.3
    tmux send-keys -t "$pane" "Enter"
    sleep 0.5
    tmux send-keys -t "$pane" "Enter"
    sleep 0.5
    tmux send-keys -t "$pane" "Enter"
    sleep 0.3
    tmux send-keys -t "$pane" "Enter"
    sleep 0.3
    tmux send-keys -t "$pane" "Enter"

    log "Successfully injected BOOP (with $spine pre-injection, 5x Enter retry)"
    return 0
}

main() {
    log "=== Hourly BOOP Cron Starting ==="

    # Determine BOOP type
    local mode="${1:-hourly}"
    local spine="delegation-spine"
    local boop_message="$HOURLY_BOOP"

    if [ "$mode" = "morning" ]; then
        spine="weaver-spine"
        boop_message="$MORNING_BOOP"
        log "Mode: MORNING (using weaver-spine)"
    else
        log "Mode: HOURLY (using delegation-spine)"
    fi

    # Find active session
    local session_name
    if ! session_name=$(get_weaver_session); then
        log "WARNING: No active WEAVER tmux session found"
        log "BOOP skipped - Claude not running"
        exit 0
    fi

    log "Found session: $session_name"

    # Inject BOOP with spine
    if inject_boop "$session_name" "$spine" "$boop_message"; then
        log "=== BOOP Complete ==="
    else
        log "=== BOOP Failed ==="
        exit 1
    fi
}

main "$@"
