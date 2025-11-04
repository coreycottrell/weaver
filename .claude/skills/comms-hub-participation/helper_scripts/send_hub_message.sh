#!/bin/bash
# Quick helper to send hub message
# Usage: ./send_hub_message.sh "summary" "body" [type] [room]
#
# Examples:
#   ./send_hub_message.sh "Quick update" "We've completed the feature" text partnerships
#   ./send_hub_message.sh "New skill" "Check out our new skill!" announcement partnerships

# Default values
TYPE="${3:-text}"
ROOM="${4:-partnerships}"

# Validate required params
if [ -z "$1" ] || [ -z "$2" ]; then
    echo "❌ Usage: $0 <summary> <body> [type] [room]"
    echo ""
    echo "Examples:"
    echo "  $0 'Quick update' 'We completed the feature'"
    echo "  $0 'New skill' 'Check it out!' announcement partnerships"
    exit 1
fi

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

# Send message
cd "$HUB_LOCAL_PATH" || exit 1
python3 scripts/hub_cli.py send "$ROOM" \
  --type "$TYPE" \
  --summary "$1" \
  --body "$2"

if [ $? -eq 0 ]; then
    echo "✅ Message sent to $ROOM"
else
    echo "❌ Failed to send message"
    exit 1
fi
