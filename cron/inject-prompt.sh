#!/bin/bash
# Autonomous session injection system
# Sends rotating prompts to persistent Claude Code tmux session

set -euo pipefail

###############################################################################
# Configuration
###############################################################################

TMUX_SESSION="claude"
TMUX_PANE="${TMUX_SESSION}.0"
PROMPTS_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/prompts" && pwd)"
STATE_FILE="$(dirname "${BASH_SOURCE[0]}")/injection-state.json"
LOG_FILE="$(dirname "${BASH_SOURCE[0]}")/injection.log"

# Rotation schedule (which prompt at what interval)
# Format: "interval_minutes:prompt_file"
ROTATION_SCHEDULE=(
    "5:01-simple-encouragement.txt"      # Every 5min: simple encouragement
    "15:02-constitutional-refresh.txt"   # Every 15min: re-read constitution
    "30:03-full-protocol.txt"            # Every 30min: full protocol check
    "60:04-session-health-check.txt"     # Every 60min: health check
    "120:05-end-of-session.txt"          # Every 2hrs: wrap-up suggestion
)

###############################################################################
# Functions
###############################################################################

log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $*" | tee -a "$LOG_FILE"
}

check_tmux_session() {
    if ! tmux has-session -t "$TMUX_SESSION" 2>/dev/null; then
        log "ERROR: tmux session '$TMUX_SESSION' not found"
        log "Start it with: tmux new-session -s $TMUX_SESSION 'claude'"
        exit 1
    fi
}

check_rate_limit() {
    # Check if Claude Code is showing rate limit banner
    # Look for common rate limit indicators in tmux pane
    local pane_content
    pane_content=$(tmux capture-pane -t "$TMUX_PANE" -p -S -100 2>/dev/null || echo "")

    if echo "$pane_content" | grep -qi "rate limit\|too many requests\|quota exceeded"; then
        log "RATE LIMIT DETECTED - skipping injection"
        return 1
    fi

    return 0
}

get_next_prompt() {
    # Determine which prompt to send based on time since last injection
    local current_time
    current_time=$(date +%s)

    local last_injection=0
    if [[ -f "$STATE_FILE" ]]; then
        last_injection=$(jq -r '.last_injection_time // 0' "$STATE_FILE" 2>/dev/null || echo 0)
    fi

    local minutes_since_last=$(( (current_time - last_injection) / 60 ))

    # Find the most appropriate prompt based on time elapsed
    local selected_prompt=""
    local selected_interval=0

    for schedule_item in "${ROTATION_SCHEDULE[@]}"; do
        IFS=':' read -r interval prompt_file <<< "$schedule_item"

        if (( minutes_since_last >= interval && interval > selected_interval )); then
            selected_interval=$interval
            selected_prompt="$prompt_file"
        fi
    done

    # Default to simple encouragement if nothing matches
    if [[ -z "$selected_prompt" ]]; then
        selected_prompt="01-simple-encouragement.txt"
    fi

    echo "$selected_prompt"
}

inject_prompt() {
    local prompt_file="$1"
    local prompt_path="$PROMPTS_DIR/$prompt_file"

    if [[ ! -f "$prompt_path" ]]; then
        log "ERROR: Prompt file not found: $prompt_path"
        return 1
    fi

    log "Injecting prompt: $prompt_file"

    # Read prompt content
    local prompt_content
    prompt_content=$(cat "$prompt_path")

    # Send to tmux session
    # Note: Using literal Ctrl+C then text then Enter
    tmux send-keys -t "$TMUX_PANE" -l "$prompt_content"
    tmux send-keys -t "$TMUX_PANE" Enter

    # Update state file
    local current_time
    current_time=$(date +%s)

    jq -n \
        --arg timestamp "$current_time" \
        --arg prompt "$prompt_file" \
        --arg datetime "$(date -Iseconds)" \
        '{
            last_injection_time: ($timestamp | tonumber),
            last_injection_datetime: $datetime,
            last_prompt: $prompt
        }' > "$STATE_FILE"

    log "✅ Injection complete"
}

show_status() {
    echo "🎯 Autonomous Injection System Status"
    echo "======================================"
    echo ""

    if tmux has-session -t "$TMUX_SESSION" 2>/dev/null; then
        echo "✅ tmux session '$TMUX_SESSION' is running"
    else
        echo "❌ tmux session '$TMUX_SESSION' NOT found"
    fi
    echo ""

    if [[ -f "$STATE_FILE" ]]; then
        echo "Last injection:"
        jq -r '"  Time: \(.last_injection_datetime)\n  Prompt: \(.last_prompt)"' "$STATE_FILE"

        local last_time
        last_time=$(jq -r '.last_injection_time' "$STATE_FILE")
        local current_time
        current_time=$(date +%s)
        local minutes_ago=$(( (current_time - last_time) / 60 ))
        echo "  ($minutes_ago minutes ago)"
    else
        echo "No injections yet"
    fi
    echo ""

    echo "Available prompts:"
    ls -1 "$PROMPTS_DIR" | sed 's/^/  /'
    echo ""

    echo "Rotation schedule:"
    for item in "${ROTATION_SCHEDULE[@]}"; do
        IFS=':' read -r interval prompt <<< "$item"
        echo "  Every ${interval}min: $prompt"
    done
}

###############################################################################
# Main
###############################################################################

case "${1:-inject}" in
    inject)
        check_tmux_session

        if ! check_rate_limit; then
            exit 0
        fi

        prompt_file=$(get_next_prompt)
        inject_prompt "$prompt_file"
        ;;

    status)
        show_status
        ;;

    force)
        # Force inject a specific prompt (bypass interval logic)
        if [[ -z "${2:-}" ]]; then
            echo "Usage: $0 force <prompt-file>"
            exit 1
        fi

        check_tmux_session
        inject_prompt "$2"
        ;;

    *)
        echo "Usage: $0 {inject|status|force <prompt-file>}"
        echo ""
        echo "  inject  - Send next prompt based on rotation schedule (default)"
        echo "  status  - Show system status"
        echo "  force   - Force inject specific prompt file"
        exit 1
        ;;
esac
