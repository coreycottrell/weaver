#!/bin/bash
# Start watching hub for new messages
# Usage: ./watch_hub.sh [room] [interval]
#
# Examples:
#   ./watch_hub.sh                      # partnerships, 60s interval
#   ./watch_hub.sh partnerships 30      # partnerships, 30s interval
#   ./watch_hub.sh skills 120           # skills room, 2min interval

# Default values
ROOM="${1:-partnerships}"
INTERVAL="${2:-60}"

# Check HUB_LOCAL_PATH is set
if [ -z "$HUB_LOCAL_PATH" ]; then
    echo "❌ Error: HUB_LOCAL_PATH not set"
    echo "Set in .env or export HUB_LOCAL_PATH=/path/to/hub"
    exit 1
fi

# Check hub exists
if [ ! -d "$HUB_LOCAL_PATH" ]; then
    echo "❌ Error: Hub not found at $HUB_LOCAL_PATH"
    exit 1
fi

# Start watching
cd "$HUB_LOCAL_PATH" || exit 1
echo "👁️ Watching $ROOM for new messages (${INTERVAL}s interval)"
echo "Press Ctrl+C to stop"
echo ""

python3 scripts/hub_cli.py watch "$ROOM" --interval "$INTERVAL"
