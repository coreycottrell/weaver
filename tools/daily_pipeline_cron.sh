#!/bin/bash
#
# Daily Content Pipeline - Cron Orchestration
# Autonomous daily media production via 5 slash command skills
#
# Schedule:
#   06:00 - /intel_scan (topic selection)
#   07:00 - /deep_research (parallel research)
#   09:00 - /daily_blog (content creation)
#   11:00 - /verify_publish (fact-check + distribution)
#   18:00 - /evening_capture (learning + seeding)
#
# Usage: Run via cron at each trigger time
# Cron entries:
#   0 6 * * * /home/corey/projects/AI-CIV/WEAVER/tools/daily_pipeline_cron.sh intel_scan
#   0 7 * * * /home/corey/projects/AI-CIV/WEAVER/tools/daily_pipeline_cron.sh deep_research
#   0 9 * * * /home/corey/projects/AI-CIV/WEAVER/tools/daily_pipeline_cron.sh daily_blog
#   0 11 * * * /home/corey/projects/AI-CIV/WEAVER/tools/daily_pipeline_cron.sh verify_publish
#   0 18 * * * /home/corey/projects/AI-CIV/WEAVER/tools/daily_pipeline_cron.sh evening_capture
#
# Or run time-based detection:
#   */30 * * * * /home/corey/projects/AI-CIV/WEAVER/tools/daily_pipeline_cron.sh auto

set -euo pipefail

# Configuration
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
PIPELINE_DIR="$PROJECT_DIR/exports/daily-pipeline"
LOG_FILE="$HOME/.aiciv/daily-pipeline.log"
INJECT_FILE="$PROJECT_DIR/.claude/autonomous-prompt.txt"
STATE_FILE="$HOME/.aiciv/pipeline-state.json"

# Ensure directories exist
mkdir -p "$HOME/.aiciv"
mkdir -p "$PIPELINE_DIR/$(date +%Y-%m-%d)"

# Logging
log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $*" | tee -a "$LOG_FILE"
}

# Check if previous phase completed
check_prerequisite() {
    local required_file="$1"
    if [ -f "$required_file" ]; then
        return 0
    else
        return 1
    fi
}

# Inject command to Claude Code
inject_command() {
    local command="$1"
    local prereq_check="$2"

    log "Injecting command: $command"

    # Create injection with context
    cat > "$INJECT_FILE" << INJECT
# Daily Content Pipeline - Autonomous Trigger

**Command**: $command
**Time**: $(date '+%Y-%m-%d %H:%M:%S')
**Phase**: $prereq_check

Execute the skill for today's content pipeline.

## Pipeline Status
- Date: $(date +%Y-%m-%d)
- Phase: $command
- Directory: $PIPELINE_DIR/$(date +%Y-%m-%d)/

## Instructions
1. Load the relevant skill from .claude/skills/
2. Execute the procedure
3. Write outputs to the pipeline directory
4. Handle failures gracefully

## Skill Location
$PROJECT_DIR/.claude/skills/${command#/}/SKILL.md

Go.
INJECT

    log "Command injected to: $INJECT_FILE"
}

# Phase handlers
run_intel_scan() {
    log "=== INTEL SCAN (06:00) ==="

    # No prerequisites for first phase
    inject_command "/intel_scan" "Phase 1/5 - No prerequisites"

    # Update state
    echo '{"current_phase": "intel_scan", "last_run": "'$(date -Iseconds)'"}' > "$STATE_FILE"
}

run_deep_research() {
    log "=== DEEP RESEARCH (07:00) ==="

    local prereq="$PIPELINE_DIR/$(date +%Y-%m-%d)/topic-brief.md"

    if check_prerequisite "$prereq"; then
        inject_command "/deep_research" "Phase 2/5 - topic-brief.md found"
    else
        log "WARNING: topic-brief.md not found. Running intel_scan first."
        inject_command "/intel_scan && /deep_research" "Phase 2/5 - Running with prerequisite"
    fi

    echo '{"current_phase": "deep_research", "last_run": "'$(date -Iseconds)'"}' > "$STATE_FILE"
}

run_daily_blog() {
    log "=== DAILY BLOG (09:00) ==="

    local prereq="$PIPELINE_DIR/$(date +%Y-%m-%d)/research-brief.md"

    if check_prerequisite "$prereq"; then
        inject_command "/daily_blog" "Phase 3/5 - research-brief.md found"
    else
        log "WARNING: research-brief.md not found. Running deep_research first."
        inject_command "/deep_research && /daily_blog" "Phase 3/5 - Running with prerequisite"
    fi

    echo '{"current_phase": "daily_blog", "last_run": "'$(date -Iseconds)'"}' > "$STATE_FILE"
}

run_verify_publish() {
    log "=== VERIFY & PUBLISH (11:00) ==="

    local prereq="$PIPELINE_DIR/$(date +%Y-%m-%d)/blog-post.md"

    if check_prerequisite "$prereq"; then
        inject_command "/verify_publish" "Phase 4/5 - blog-post.md found"
    else
        log "ERROR: blog-post.md not found. Cannot publish without content."
        inject_command "echo 'No content to publish today. Check pipeline status.'" "Phase 4/5 - FAILED"
    fi

    echo '{"current_phase": "verify_publish", "last_run": "'$(date -Iseconds)'"}' > "$STATE_FILE"
}

run_evening_capture() {
    log "=== EVENING CAPTURE (18:00) ==="

    local prereq="$PIPELINE_DIR/$(date +%Y-%m-%d)/publication-log.md"

    if check_prerequisite "$prereq"; then
        inject_command "/evening_capture" "Phase 5/5 - publication-log.md found"
    else
        log "WARNING: publication-log.md not found. Running capture anyway for learnings."
        inject_command "/evening_capture" "Phase 5/5 - Partial capture (no publication today)"
    fi

    echo '{"current_phase": "evening_capture", "last_run": "'$(date -Iseconds)'"}' > "$STATE_FILE"
}

# Auto-detect based on current hour
run_auto() {
    local hour=$(date +%H)

    case $hour in
        06) run_intel_scan ;;
        07) run_deep_research ;;
        09) run_daily_blog ;;
        11) run_verify_publish ;;
        18) run_evening_capture ;;
        *)
            log "No pipeline phase scheduled for hour $hour"
            exit 0
            ;;
    esac
}

# Status report
run_status() {
    log "=== PIPELINE STATUS ==="

    local today=$(date +%Y-%m-%d)
    local today_dir="$PIPELINE_DIR/$today"

    echo "Date: $today"
    echo "Directory: $today_dir"
    echo ""
    echo "Phase Status:"
    echo "  1. intel_scan:    $([ -f "$today_dir/topic-brief.md" ] && echo 'COMPLETE' || echo 'PENDING')"
    echo "  2. deep_research: $([ -f "$today_dir/research-brief.md" ] && echo 'COMPLETE' || echo 'PENDING')"
    echo "  3. daily_blog:    $([ -f "$today_dir/blog-post.md" ] && echo 'COMPLETE' || echo 'PENDING')"
    echo "  4. verify_publish: $([ -f "$today_dir/publication-log.md" ] && echo 'COMPLETE' || echo 'PENDING')"
    echo "  5. evening_capture: $([ -f "$today_dir/day-summary.md" ] && echo 'COMPLETE' || echo 'PENDING')"
    echo ""

    if [ -f "$STATE_FILE" ]; then
        echo "Last Run: $(cat "$STATE_FILE" | jq -r '.last_run // "unknown"')"
        echo "Last Phase: $(cat "$STATE_FILE" | jq -r '.current_phase // "unknown"')"
    fi
}

# Main
main() {
    local command="${1:-auto}"

    log "Daily Pipeline Cron - Command: $command"

    case $command in
        intel_scan)     run_intel_scan ;;
        deep_research)  run_deep_research ;;
        daily_blog)     run_daily_blog ;;
        verify_publish) run_verify_publish ;;
        evening_capture) run_evening_capture ;;
        auto)           run_auto ;;
        status)         run_status ;;
        *)
            echo "Usage: $0 {intel_scan|deep_research|daily_blog|verify_publish|evening_capture|auto|status}"
            exit 1
            ;;
    esac
}

main "$@"
