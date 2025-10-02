#!/usr/bin/env bash
#
# AI-CIV Autonomous Queue Processor
# Processes queue files and sends prompts to Claude Code CLI
#

set -uo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
QUEUE="$SCRIPT_DIR"
PROCESSED="$QUEUE/processed"
LOG="$QUEUE/queue.log"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

mkdir -p "$PROCESSED"

# Function to log messages
log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $*" | tee -a "$LOG"
}

# Process all .txt files in queue
shopt -s nullglob
processed_count=0

for f in "$QUEUE"/*.txt; do
    log "Processing: $(basename "$f")"

    # Read the entire file as the prompt
    prompt=$(cat "$f")

    # Skip empty files
    if [ -z "$prompt" ]; then
        log "  Skipping empty file"
        continue
    fi

    log "  Executing Claude Code with prompt from $(basename "$f")"

    # Execute claude in the project root directory
    cd "$PROJECT_ROOT"

    # Run claude with the prompt, capture output
    if timeout 300 claude --dangerously-skip-permissions "$prompt" > "$QUEUE/last-output.txt" 2>&1; then
        log "  ✓ Completed successfully"
        # Show last few lines of output
        tail -5 "$QUEUE/last-output.txt" | while IFS= read -r line; do
            log "    $line"
        done
    else
        exit_code=$?
        log "  ✗ Failed with exit code: $exit_code"
        tail -10 "$QUEUE/last-output.txt" | while IFS= read -r line; do
            log "    ERROR: $line"
        done
    fi

    # Move to processed with timestamp
    timestamp=$(date +%Y%m%d-%H%M%S)
    processed_name="$PROCESSED/${timestamp}-$(basename "$f")"
    mv "$f" "$processed_name"
    log "  Archived → $processed_name"
    ((processed_count++))
done

if [ $processed_count -eq 0 ]; then
    log "No queue files found"
else
    log "Processed $processed_count queue file(s)"
fi
