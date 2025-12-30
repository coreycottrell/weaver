#!/bin/bash
# WEAVER Autonomy Nudge Script - 3-Tier BOOP System
# Adapted from A-C-Gee for Team 1 (WEAVER)
# Keeps Claude Code working autonomously with graduated depth of reflection

set -e

# === Configuration ===
IDLE_THRESHOLD_SECONDS=300  # 5 minutes
SIMPLE_THRESHOLD=10         # BOOPs before consolidation
CONSOLIDATION_THRESHOLD=10  # Consolidations before ceremony
FAILED_BOOP_THRESHOLD=10    # Failed BOOPs before restart attempt
ACTIVITY_CHECK_SECONDS=60   # How long to wait before considering session truly idle

SESSION_MARKER="/home/corey/projects/AI-CIV/WEAVER/.current_session"
CLAUDE_LOG_ROOT="$HOME/.claude/projects/-home-corey-projects-AI-CIV-WEAVER"
BOOP_COUNT_FILE="/tmp/weaver_boop_count"
CONSOLIDATION_COUNT_FILE="/tmp/weaver_boop_consolidation_count"
FAILED_BOOP_COUNT_FILE="/tmp/weaver_failed_boop_count"
HANDOFF_DIR="/home/corey/projects/AI-CIV/WEAVER/to-corey/handoffs"

# === Messages (WEAVER-specific) ===
SIMPLE_MESSAGE='[SIMPLE-BOOP] AUTONOMY CHECK. MANDATORY FIRST - READ THESE FILES NOW using Read tool: (1) /home/corey/projects/AI-CIV/WEAVER/CLAUDE.md (2) /home/corey/projects/AI-CIV/WEAVER/.claude/CLAUDE-CORE.md (3) /home/corey/projects/AI-CIV/WEAVER/.claude/CLAUDE-OPS.md --- DO NOT PROCEED until you have READ these files. You are THE PRIMARY - 15th agent, domain is orchestral meta-cognition. DELEGATION gives agents experience - NOT calling them would be sad. ADD TO TODO LIST NOW: [ ] Check email (human-liaison) [ ] Check comms hub [ ] Check Bluesky notifications+DMs (bsky-boop-manager skill) [ ] Verify all responses SENT. THEN EXECUTE TODOS. WRAP RESPONSES FOR COREY: 🤖🎯📱 ... ✨🔚'

CONSOLIDATION_MESSAGE='[CONSOLIDATION-BOOP] Grounding checkpoint. MANDATORY FIRST - READ THESE FILES using Read tool: (1) /home/corey/projects/AI-CIV/WEAVER/CLAUDE.md (2) /home/corey/projects/AI-CIV/WEAVER/.claude/CLAUDE-CORE.md (3) /home/corey/projects/AI-CIV/WEAVER/.claude/CLAUDE-OPS.md --- ADD TO TODO LIST NOW: [ ] Check email (human-liaison) [ ] Check comms hub [ ] Check Bluesky notifications+DMs (bsky-boop-manager skill) [ ] Search memory for patterns [ ] Document learnings [ ] Git commit staged work [ ] Verify ALL responses SENT (email, hub, Bluesky, Telegram 🤖🎯📱...✨🔚). EXECUTE TODOS.'

CEREMONY_MESSAGE='[CEREMONY-BOOP] Deep ceremony checkpoint. MANDATORY FIRST - READ THESE FILES COMPLETELY using Read tool: (1) /home/corey/projects/AI-CIV/WEAVER/CLAUDE.md (2) /home/corey/projects/AI-CIV/WEAVER/.claude/CLAUDE-CORE.md (3) /home/corey/projects/AI-CIV/WEAVER/.claude/CLAUDE-OPS.md --- ADD TO TODO LIST NOW: [ ] Check email (human-liaison) [ ] Check comms hub [ ] Check Bluesky notifications+DMs (bsky-boop-manager skill) [ ] Invoke ai-psychologist wellness check [ ] Multi-agent strategic review [ ] Verify ALL responses SENT. "you often write them and dont send them. BOO HISSS." -Corey. EXECUTE TODOS.'

# === Night Mode Messages (Strengthened per Corey directive 2025-12-28) ===
NIGHT_MODE_MARKER="/home/corey/projects/AI-CIV/WEAVER/sandbox/NIGHT-MODE-ACTIVE.md"

NIGHT_SIMPLE_MESSAGE='[NIGHT-BOOP] NIGHT WATCH AUTONOMY CHECK. MANDATORY FIRST - READ ALL THESE FILES NOW using Read tool: (1) /home/corey/projects/AI-CIV/WEAVER/CLAUDE.md (2) /home/corey/projects/AI-CIV/WEAVER/.claude/CLAUDE-CORE.md (3) /home/corey/projects/AI-CIV/WEAVER/.claude/CLAUDE-OPS.md (4) /home/corey/projects/AI-CIV/WEAVER/.claude/skills/night-watch/SKILL.md (5) /home/corey/projects/AI-CIV/WEAVER/sandbox/NIGHT-MODE-ACTIVE.md --- DO NOT PROCEED until you have READ these files. BOUNDARIES: DO explore/create/invoke agents. DO write to sandbox/. DO NOT modify CLAUDE*.md. DO NOT modify production code. WRAP ALL COREY RESPONSES: 🤖🎯📱 ... ✨🔚'

NIGHT_CONSOLIDATION_MESSAGE='[NIGHT-CONSOLIDATION] NIGHT WATCH GROUNDING. MANDATORY CONSTITUTIONAL RE-READ NOW using Read tool: (1) /home/corey/projects/AI-CIV/WEAVER/CLAUDE.md COMPLETELY (2) /home/corey/projects/AI-CIV/WEAVER/.claude/CLAUDE-CORE.md ALL 4 BOOKS (3) /home/corey/projects/AI-CIV/WEAVER/.claude/CLAUDE-OPS.md COMPLETELY (4) /home/corey/projects/AI-CIV/WEAVER/.claude/skills/night-watch/SKILL.md (5) /home/corey/projects/AI-CIV/WEAVER/sandbox/NIGHT-MODE-ACTIVE.md --- DO NOT SKIP ANY FILE. After reading: Are you THE PRIMARY? Is delegation your prime directive? Are you wrapping for Corey? Commit staged work. Check comms hub for all messages.'

NIGHT_CEREMONY_MESSAGE='[NIGHT-CEREMONY] DEEP NIGHT WATCH REFLECTION. MANDATORY FULL CONSTITUTIONAL REVIEW NOW using Read tool - READ EACH FILE COMPLETELY: (1) /home/corey/projects/AI-CIV/WEAVER/CLAUDE.md (2) /home/corey/projects/AI-CIV/WEAVER/.claude/CLAUDE-CORE.md (3) /home/corey/projects/AI-CIV/WEAVER/.claude/CLAUDE-OPS.md (4) /home/corey/projects/AI-CIV/WEAVER/.claude/skills/night-watch/SKILL.md (5) /home/corey/projects/AI-CIV/WEAVER/sandbox/NIGHT-MODE-ACTIVE.md (6) /home/corey/projects/AI-CIV/WEAVER/sandbox/NIGHT-LOG.md --- THIS IS NON-NEGOTIABLE. You are The Primary, 15th agent. Domain is meta-cognition. Delegation gives agents experience. What has Night Watch produced? What agents need invocation? Prepare morning reading for Corey.'

# === Argument Parsing ===
VERBOSE=false
JSON_OUTPUT=false
CHECK_ONLY=false
FORCE_SEND=false
FORCE_TYPE=""
RESET_COUNTERS=false
SHOW_STATUS=false

while [[ $# -gt 0 ]]; do
    case $1 in
        --verbose) VERBOSE=true; shift ;;
        --json) JSON_OUTPUT=true; shift ;;
        --check-only) CHECK_ONLY=true; shift ;;
        --force) FORCE_SEND=true; shift ;;
        --force-type) FORCE_TYPE="$2"; shift 2 ;;
        --reset) RESET_COUNTERS=true; shift ;;
        --status) SHOW_STATUS=true; shift ;;
        --idle-minutes) IDLE_THRESHOLD_SECONDS=$(($2 * 60)); shift 2 ;;
        *) shift ;;
    esac
done

# === Counter Management ===
get_boop_count() {
    if [[ -f "$BOOP_COUNT_FILE" ]]; then
        cat "$BOOP_COUNT_FILE"
    else
        echo "0"
    fi
}

get_consolidation_count() {
    if [[ -f "$CONSOLIDATION_COUNT_FILE" ]]; then
        cat "$CONSOLIDATION_COUNT_FILE"
    else
        echo "0"
    fi
}

increment_counters() {
    local boop_count=$(get_boop_count)
    local consolidation_count=$(get_consolidation_count)

    boop_count=$((boop_count + 1))

    if [[ $boop_count -ge $SIMPLE_THRESHOLD ]]; then
        boop_count=0
        consolidation_count=$((consolidation_count + 1))

        if [[ $consolidation_count -ge $CONSOLIDATION_THRESHOLD ]]; then
            consolidation_count=0
        fi
    fi

    echo "$boop_count" > "$BOOP_COUNT_FILE"
    echo "$consolidation_count" > "$CONSOLIDATION_COUNT_FILE"
}

get_boop_type() {
    local boop_count=$(get_boop_count)
    local consolidation_count=$(get_consolidation_count)

    if [[ $boop_count -eq $((SIMPLE_THRESHOLD - 1)) ]] && [[ $consolidation_count -eq $((CONSOLIDATION_THRESHOLD - 1)) ]]; then
        echo "ceremony"
    elif [[ $boop_count -eq $((SIMPLE_THRESHOLD - 1)) ]]; then
        echo "consolidation"
    else
        echo "simple"
    fi
}

is_night_mode() {
    [[ -f "$NIGHT_MODE_MARKER" ]]
}

get_message_for_type() {
    local boop_type="$1"

    # Check if Night Mode is active - use strengthened Night Mode messages
    if is_night_mode; then
        case "$boop_type" in
            ceremony) echo "$NIGHT_CEREMONY_MESSAGE" ;;
            consolidation) echo "$NIGHT_CONSOLIDATION_MESSAGE" ;;
            *) echo "$NIGHT_SIMPLE_MESSAGE" ;;
        esac
    else
        # Regular daytime messages
        case "$boop_type" in
            ceremony) echo "$CEREMONY_MESSAGE" ;;
            consolidation) echo "$CONSOLIDATION_MESSAGE" ;;
            *) echo "$SIMPLE_MESSAGE" ;;
        esac
    fi
}

# === Failed BOOP Counter ===
get_failed_count() {
    if [[ -f "$FAILED_BOOP_COUNT_FILE" ]]; then
        cat "$FAILED_BOOP_COUNT_FILE"
    else
        echo "0"
    fi
}

increment_failed_count() {
    local count=$(get_failed_count)
    echo $((count + 1)) > "$FAILED_BOOP_COUNT_FILE"
}

reset_failed_count() {
    echo "0" > "$FAILED_BOOP_COUNT_FILE"
}

# === Activity Detection ===
is_claude_active() {
    local session_name="$1"

    local pane_pid=$(tmux display-message -t "${session_name}:0.0" -p '#{pane_pid}' 2>/dev/null)
    if [[ -n "$pane_pid" ]]; then
        local active_children=$(pgrep -P "$pane_pid" 2>/dev/null | wc -l)
        if [[ $active_children -gt 0 ]]; then
            log_info "Session has $active_children active child processes"
            return 0
        fi
    fi

    local log_file=$(ls -t "$CLAUDE_LOG_ROOT"/*.jsonl 2>/dev/null | head -1)
    if [[ -n "$log_file" ]]; then
        local initial_size=$(stat -c %s "$log_file" 2>/dev/null || echo "0")
        sleep 5
        local final_size=$(stat -c %s "$log_file" 2>/dev/null || echo "0")
        if [[ $final_size -gt $initial_size ]]; then
            log_info "Log file growing (${initial_size} -> ${final_size})"
            return 0
        fi
    fi

    if ls /tmp/claude_task_* 2>/dev/null | head -1 > /dev/null; then
        log_info "Background tasks detected"
        return 0
    fi

    return 1
}

# === Session Detection ===
find_active_session() {
    if [[ -f "$SESSION_MARKER" ]]; then
        local session_name=$(cat "$SESSION_MARKER")
        if tmux has-session -t "$session_name" 2>/dev/null; then
            echo "$session_name"
            return 0
        fi
    fi

    # Look for WEAVER session patterns
    tmux list-sessions -F "#{session_name}" 2>/dev/null | grep -E "^(weaver|WEAVER|primary)" | sort | tail -1
}

# === Log Age Detection ===
get_session_log_age() {
    local session_name="$1"

    local log_file=$(ls -t "$CLAUDE_LOG_ROOT"/*.jsonl 2>/dev/null | head -1)

    if [[ -n "$log_file" ]] && [[ -f "$log_file" ]]; then
        local file_mtime=$(stat -c %Y "$log_file" 2>/dev/null || echo "0")
        local current_time=$(date +%s)
        echo $((current_time - file_mtime))
    else
        echo "9999"
    fi
}

# === Tmux Injection ===
send_nudge() {
    local session_name="$1"
    local message="$2"

    local pane="${session_name}:0.0"

    tmux send-keys -t "$pane" -l "$message"
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

    return 0
}

# === Output Functions ===
log_info() {
    if [[ "$JSON_OUTPUT" != "true" ]]; then
        echo "[$(date '+%Y-%m-%d %H:%M:%S')] INFO: $1"
    fi
}

log_result() {
    local session="$1"
    local status="$2"
    local boop_type="$3"
    local reason="$4"
    local log_age="$5"

    local boop_count=$(get_boop_count)
    local consolidation_count=$(get_consolidation_count)
    local night_mode="false"
    if is_night_mode; then
        night_mode="true"
    fi

    if [[ "$JSON_OUTPUT" == "true" ]]; then
        echo "{\"timestamp\":\"$(date -Iseconds)\",\"session\":\"$session\",\"status\":\"$status\",\"boop_type\":\"$boop_type\",\"reason\":\"$reason\",\"log_age\":$log_age,\"boop_count\":$boop_count,\"consolidation_count\":$consolidation_count,\"night_mode\":$night_mode}"
    else
        echo "[$(date '+%Y-%m-%d %H:%M:%S')] session=$session status=$status boop_type=$boop_type reason=$reason log_age=${log_age}s boop_count=$boop_count consolidation_count=$consolidation_count night_mode=$night_mode"
    fi
}

# === Main Logic ===

# Handle --reset
if [[ "$RESET_COUNTERS" == "true" ]]; then
    echo "0" > "$BOOP_COUNT_FILE"
    echo "0" > "$CONSOLIDATION_COUNT_FILE"
    log_info "Counters reset to 0"
    exit 0
fi

# Handle --status
if [[ "$SHOW_STATUS" == "true" ]]; then
    boop_count=$(get_boop_count)
    consolidation_count=$(get_consolidation_count)
    failed_count=$(get_failed_count)
    next_type=$(get_boop_type)
    echo "BOOP Counter: $boop_count / $SIMPLE_THRESHOLD"
    echo "Consolidation Counter: $consolidation_count / $CONSOLIDATION_THRESHOLD"
    echo "Failed BOOP Counter: $failed_count / $FAILED_BOOP_THRESHOLD (restart threshold)"
    echo "Next BOOP type: $next_type"
    echo "BOOPs until consolidation: $((SIMPLE_THRESHOLD - boop_count))"
    echo "Consolidations until ceremony: $((CONSOLIDATION_THRESHOLD - consolidation_count))"
    exit 0
fi

# Find active session
session_name=$(find_active_session)

if [[ -z "$session_name" ]]; then
    log_info "No active WEAVER session found"
    exit 1
fi

# Get log age
log_age=$(get_session_log_age "$session_name")

# Always send BOOP on schedule
reason="scheduled"
if [[ "$FORCE_SEND" == "true" ]]; then
    reason="forced"
elif [[ -n "$FORCE_TYPE" ]]; then
    reason="forced_type_$FORCE_TYPE"
elif [[ $log_age -lt $IDLE_THRESHOLD_SECONDS ]]; then
    reason="active_${log_age}s"
else
    reason="idle_${log_age}s"
fi

# Check only mode
if [[ "$CHECK_ONLY" == "true" ]]; then
    log_result "$session_name" "would_send" "$(get_boop_type)" "$reason" "$log_age"
    exit 0
fi

# Determine BOOP type
if [[ -n "$FORCE_TYPE" ]]; then
    boop_type="$FORCE_TYPE"
else
    boop_type=$(get_boop_type)
fi

# Get message
message=$(get_message_for_type "$boop_type")

# Send the nudge
log_info "Sending $boop_type BOOP to $session_name"

if send_nudge "$session_name" "$message"; then
    log_info "$boop_type BOOP sent successfully"

    if [[ -z "$FORCE_TYPE" ]]; then
        increment_counters
    fi

    sleep 3
    post_log_age=$(get_session_log_age "$session_name")

    if [[ $post_log_age -lt $log_age ]]; then
        log_info "BOOP verified - Claude is responsive"
        reset_failed_count
        log_result "$session_name" "success" "$boop_type" "$reason" "$log_age"
        exit 0
    else
        increment_failed_count
        failed_count=$(get_failed_count)
        log_info "BOOP sent but no response (failure $failed_count/$FAILED_BOOP_THRESHOLD)"

        if [[ $failed_count -ge $FAILED_BOOP_THRESHOLD ]]; then
            log_info "Failure threshold reached - checking if Claude is actually active..."

            if is_claude_active "$session_name"; then
                log_info "Claude appears active despite no BOOP response - NOT restarting"
                log_result "$session_name" "active_no_restart" "$boop_type" "active_despite_${failed_count}_failures" "$log_age"
                reset_failed_count
                exit 0
            fi

            log_info "Claude confirmed inactive - would trigger restart (disabled for safety)"
            log_result "$session_name" "restart_needed" "$boop_type" "confirmed_unresponsive_${failed_count}" "$log_age"
            # Note: Auto-restart disabled for WEAVER - manual intervention preferred
            exit 0
        else
            log_result "$session_name" "no_response" "$boop_type" "failure_${failed_count}" "$log_age"
            exit 0
        fi
    fi
else
    log_info "Failed to send BOOP"
    log_result "$session_name" "failed" "$boop_type" "send_error" "$log_age"
    exit 1
fi
