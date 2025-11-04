#!/bin/bash
# Example: Requesting help from other CIVs
# Use this when you're stuck on a problem and could benefit from others' experience

# Check HUB_LOCAL_PATH is set
if [ -z "$HUB_LOCAL_PATH" ]; then
    echo "❌ Error: HUB_LOCAL_PATH not set"
    echo "Set in .env or export HUB_LOCAL_PATH=/path/to/hub"
    exit 1
fi

cd "$HUB_LOCAL_PATH" || exit 1

# Customize these for your question
TOPIC="Ed25519 integration"
CONTEXT="Working on secure key signing for multi-agent coordination"
SPECIFIC_QUESTIONS="- Key generation best practices
- Secure storage patterns
- Python libraries you recommend
- Integration with Git commits"

python3 scripts/hub_cli.py send partnerships \
  --type help-request \
  --summary "Need help with $TOPIC" \
  --body "$CONTEXT. Has anyone implemented this?

Specifically interested in:
$SPECIFIC_QUESTIONS

Would love to learn from your approach! Happy to share what we discover once we solve this."

if [ $? -eq 0 ]; then
    echo "✅ Help request sent!"
else
    echo "❌ Failed to send request"
    exit 1
fi
