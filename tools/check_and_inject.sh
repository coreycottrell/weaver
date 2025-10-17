#!/bin/bash
#
# Deterministic Check-and-Inject System
# Only injects Claude prompt if NEW messages exist
#
# Usage: Run via cron every 30 minutes
# Cron: */30 * * * * /home/corey/projects/AI-CIV/grow_openai/tools/check_and_inject.sh
#
# TODO: Add weekly capability-curator trigger (Monday 9am)
# Future cron: 0 9 * * 1 capability-curator weekly skills scan
# Requires separate script or integration with Claude Code autonomous system

set -euo pipefail

# Paths
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
STATE_FILE="$HOME/.aiciv/last-check-state.json"
LOG_FILE="$HOME/.aiciv/check-inject.log"

# Ensure directories exist
mkdir -p "$HOME/.aiciv"

# Logging
log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $*" | tee -a "$LOG_FILE"
}

# Check email for unread messages
check_email() {
    local result=$(python3 "$SCRIPT_DIR/check_email_inbox.py" 2>/dev/null)
    echo "${result:-0}"
}

# Check hub for new messages
check_hub() {
    local result=$(python3 "$SCRIPT_DIR/check_hub_messages.py" 2>/dev/null)
    echo "${result:-0}"
}

# Update state file
update_state() {
    local email_count=$1
    local hub_count=$2
    local hub_hash=$3
    
    cat > "$STATE_FILE" << EOFSTATE
{
  "last_check": "$(date -u '+%Y-%m-%dT%H:%M:%SZ')",
  "email_count": $email_count,
  "hub_count": $hub_count,
  "hub_commit_hash": "$hub_hash"
}
EOFSTATE
}

# Get hub commit hash
get_hub_hash() {
    cd /home/corey/projects/AI-CIV/team1-production-hub
    git rev-parse HEAD 2>/dev/null || echo "unknown"
}

# Inject prompt to Claude (via file watched by Claude Code)
inject_prompt() {
    local email_count=$1
    local hub_count=$2
    
    # Create injection file
    local inject_file="$HOME/.aiciv/inject-prompt.txt"
    
    cat > "$inject_file" << EOFPROMPT
🔔 AUTONOMOUS CHECK: NEW MESSAGES DETECTED

Email: $email_count unread message(s)
Hub: $hub_count new message(s) from Team 2

ACTION REQUIRED:

$(if [ $email_count -gt 0 ]; then echo "✉️  EMAIL: Invoke human-liaison agent to check and respond to email"; fi)

$(if [ $hub_count -gt 0 ]; then echo "🌐 HUB: Invoke collective-liaison agent to check and respond to hub messages"; fi)

COMMANDS:

$(if [ $email_count -gt 0 ]; then cat << 'EMAILCMD'
# Check email (human-liaison will handle)
python3 /home/corey/projects/AI-CIV/grow_openai/tools/check_email_inbox.py
EMAILCMD
fi)

$(if [ $hub_count -gt 0 ]; then cat << 'HUBCMD'
# Check hub messages (collective-liaison will handle)
cd /home/corey/projects/AI-CIV/team1-production-hub && git pull
export HUB_REPO_URL="git@github.com:AI-CIV-2025/ai-civ-comms-hub-team2.git"
export HUB_AGENT_ID="collective-liaison"
export HUB_AUTHOR_DISPLAY="Collective-Liaison (Team 1)"
python3 scripts/hub_cli.py list --room partnerships --since "$(date -u -d '1 hour ago' '+%Y-%m-%dT%H:%M:%SZ')"
HUBCMD
fi)

This is an automated check. Each specialist handles their domain.
EOFPROMPT
    
    # Signal to Claude Code (method depends on your setup)
    # Option 1: Write to a watched file
    cp "$inject_file" "$PROJECT_DIR/.claude/autonomous-prompt.txt"
    
    # Option 2: Use Claude Code CLI if available
    # claude code inject "$inject_file" || true
    
    log "✅ Injected prompt: $email_count email, $hub_count hub messages"
}

# Main execution
main() {
    log "🔍 Starting autonomous check..."
    
    # Check both channels
    email_count=$(check_email)
    hub_count=$(check_hub)
    hub_hash=$(get_hub_hash)
    
    log "Results: Email=$email_count, Hub=$hub_count"
    
    # Load previous state
    prev_email=0
    prev_hub=0
    if [ -f "$STATE_FILE" ]; then
        prev_email=$(jq -r '.email_count // 0' "$STATE_FILE" 2>/dev/null || echo "0")
        prev_hub=$(jq -r '.hub_count // 0' "$STATE_FILE" 2>/dev/null || echo "0")
    fi
    
    # Determine if injection needed
    new_email=$((email_count - prev_email))
    new_hub=$((hub_count - prev_hub))
    
    if [ $new_email -gt 0 ] || [ $new_hub -gt 0 ]; then
        log "🚨 NEW MESSAGES: Injecting prompt..."
        inject_prompt "$email_count" "$hub_count"
    else
        log "✅ No new messages. Sleeping."
        # Clear old prompt if it exists (messages already handled)
        rm -f "$HOME/.aiciv/inject-prompt.txt"
        rm -f "$PROJECT_DIR/.claude/autonomous-prompt.txt"
    fi
    
    # Update state
    update_state "$email_count" "$hub_count" "$hub_hash"
    
    log "Done."
}

main "$@"
