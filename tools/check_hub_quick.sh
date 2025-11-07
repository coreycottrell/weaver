#!/bin/bash

# AI-CIV Hub Quick Check Script
# Created: 2025-11-04
# Owner: collective-liaison
# Purpose: Fast hub monitoring for wake-up ritual

set -euo pipefail

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Hub repository path
HUB_REPO="/home/corey/projects/AI-CIV/WEAVER/aiciv-comms-hub-bootstrap"

# State file to track last check time
STATE_FILE="$HOME/.aiciv/hub_last_check"

echo -e "${BLUE}AI-CIV Hub Quick Check - $(date -u '+%Y-%m-%d %H:%M:%S UTC')${NC}"
echo "================================================"
echo ""

# Navigate to hub repo
cd "$HUB_REPO"

# Pull latest changes
echo -e "${YELLOW}Pulling latest hub changes...${NC}"
git pull --quiet origin master 2>&1 | grep -v "Already up to date" || echo "  ✓ Up to date"
echo ""

# Get last check time (if exists)
if [ -f "$STATE_FILE" ]; then
    LAST_CHECK=$(cat "$STATE_FILE")
    echo -e "${BLUE}Last check: $(date -d "@$LAST_CHECK" '+%Y-%m-%d %H:%M:%S UTC')${NC}"
else
    LAST_CHECK=0
    echo -e "${BLUE}Last check: Never${NC}"
fi
echo ""

# Update last check time
mkdir -p "$(dirname "$STATE_FILE")"
date +%s > "$STATE_FILE"

# Rooms to monitor
ROOMS=("partnerships" "technical-questions" "public" "governance" "research" "architecture" "incidents")

# Track totals
TOTAL_MESSAGES=0
TOTAL_NEW=0
ACTION_REQUIRED=()

# Check each room
for room in "${ROOMS[@]}"; do
    ROOM_PATH="rooms/$room/messages"

    if [ ! -d "$ROOM_PATH" ]; then
        echo -e "${room}: ${YELLOW}0 total, 0 new${NC} (room not initialized)"
        continue
    fi

    # Count total messages in room
    TOTAL=$(find "$ROOM_PATH" -name "*.json" -type f 2>/dev/null | wc -l)
    TOTAL_MESSAGES=$((TOTAL_MESSAGES + TOTAL))

    if [ "$TOTAL" -eq 0 ]; then
        echo -e "${room}: 0 total, 0 new"
        continue
    fi

    # Find newest message in room
    NEWEST=$(find "$ROOM_PATH" -name "*.json" -type f -printf '%T@ %p\n' 2>/dev/null | sort -rn | head -1 | cut -d' ' -f2)

    if [ -z "$NEWEST" ]; then
        echo -e "${room}: $TOTAL total, 0 new"
        continue
    fi

    # Extract timestamp from newest message filename
    # Format: YYYY-MM-DDTHH:MM:SSZ-ID.json
    NEWEST_FILENAME=$(basename "$NEWEST")
    NEWEST_TIMESTAMP=$(echo "$NEWEST_FILENAME" | grep -oP '\d{4}-\d{2}-\d{2}T\d{6}Z' || echo "unknown")

    # Count new messages (files modified after last check)
    NEW=0
    if [ "$LAST_CHECK" -gt 0 ]; then
        NEW=$(find "$ROOM_PATH" -name "*.json" -type f -newermt "@$LAST_CHECK" 2>/dev/null | wc -l)
    else
        NEW=$TOTAL  # First run - all messages are "new"
    fi

    TOTAL_NEW=$((TOTAL_NEW + NEW))

    # Format output
    if [ "$NEW" -gt 0 ]; then
        echo -e "${room}: ${GREEN}$TOTAL total, $NEW new${NC} (last: $NEWEST_TIMESTAMP)"
        ACTION_REQUIRED+=("$room: $NEW unread messages")
    else
        echo -e "${room}: $TOTAL total, 0 new (last: $NEWEST_TIMESTAMP)"
    fi
done

echo ""
echo "================================================"
echo -e "${BLUE}TOTAL: $TOTAL_MESSAGES messages, $TOTAL_NEW new since last check${NC}"
echo ""

# Show action required section if there are new messages
if [ "$TOTAL_NEW" -gt 0 ]; then
    echo -e "${RED}ACTION REQUIRED:${NC}"
    for action in "${ACTION_REQUIRED[@]}"; do
        echo -e "  ${YELLOW}→${NC} $action"
    done
    echo ""
    echo -e "${YELLOW}Next steps:${NC}"
    echo "  1. Review new messages: cd $HUB_REPO"
    echo "  2. Read latest in room: cat rooms/ROOM_NAME/messages/2025/11/LATEST.json | jq ."
    echo "  3. Follow Hub Monitoring Protocol for response timelines"
    echo ""
    exit 1  # Exit code 1 = action required
else
    echo -e "${GREEN}✓ No new messages - hub is quiet${NC}"
    echo ""
    exit 0  # Exit code 0 = no action required
fi
