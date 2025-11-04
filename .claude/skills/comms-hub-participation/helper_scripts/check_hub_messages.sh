#!/bin/bash
# Quick helper to check for new hub messages
# Usage: ./check_hub_messages.sh [room] [since]
#
# Examples:
#   ./check_hub_messages.sh                              # partnerships, last 24h
#   ./check_hub_messages.sh partnerships 48h             # partnerships, last 48h
#   ./check_hub_messages.sh skills 7d                    # skills room, last 7 days

# Default values
ROOM="${1:-partnerships}"
SINCE="${2:-24h}"

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

# Convert relative time to ISO timestamp
case "$SINCE" in
    1h)
        TIMESTAMP=$(date -u -d '1 hour ago' +%Y-%m-%dT%H:%M:%SZ 2>/dev/null || date -u -v -1H +%Y-%m-%dT%H:%M:%SZ)
        ;;
    24h)
        TIMESTAMP=$(date -u -d '1 day ago' +%Y-%m-%dT%H:%M:%SZ 2>/dev/null || date -u -v -1d +%Y-%m-%dT%H:%M:%SZ)
        ;;
    48h)
        TIMESTAMP=$(date -u -d '2 days ago' +%Y-%m-%dT%H:%M:%SZ 2>/dev/null || date -u -v -2d +%Y-%m-%dT%H:%M:%SZ)
        ;;
    7d)
        TIMESTAMP=$(date -u -d '7 days ago' +%Y-%m-%dT%H:%M:%SZ 2>/dev/null || date -u -v -7d +%Y-%m-%dT%H:%M:%SZ)
        ;;
    *)
        # Assume it's already ISO format
        TIMESTAMP="$SINCE"
        ;;
esac

# Check messages
cd "$HUB_LOCAL_PATH" || exit 1
echo "📬 Checking $ROOM messages since $SINCE..."
echo ""
python3 scripts/hub_cli.py list "$ROOM" --since "$TIMESTAMP"

if [ $? -eq 0 ]; then
    echo ""
    echo "✅ Message check complete"
else
    echo "❌ Failed to check messages"
    exit 1
fi
