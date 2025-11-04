#!/bin/bash
# Test hub connection and authentication
# Run this to verify your hub setup is correct

echo "🧪 Testing Communications Hub Connection"
echo "========================================"
echo ""

# Check 1: HUB_LOCAL_PATH is set
echo "1️⃣ Checking HUB_LOCAL_PATH..."
if [ -z "$HUB_LOCAL_PATH" ]; then
    echo "❌ FAILED: HUB_LOCAL_PATH not set"
    echo "   Set in .env or export HUB_LOCAL_PATH=/path/to/hub"
    exit 1
else
    echo "✅ PASSED: HUB_LOCAL_PATH = $HUB_LOCAL_PATH"
fi
echo ""

# Check 2: Hub directory exists
echo "2️⃣ Checking hub directory exists..."
if [ ! -d "$HUB_LOCAL_PATH" ]; then
    echo "❌ FAILED: Hub not found at $HUB_LOCAL_PATH"
    exit 1
else
    echo "✅ PASSED: Hub directory exists"
fi
echo ""

# Check 3: Git remote accessible
echo "3️⃣ Checking git remote..."
cd "$HUB_LOCAL_PATH" || exit 1
if ! git fetch origin --dry-run 2>/dev/null; then
    echo "❌ FAILED: Cannot access git remote"
    echo "   Check SSH keys and GitHub access"
    exit 1
else
    echo "✅ PASSED: Git remote accessible"
fi
echo ""

# Check 4: hub_cli.py exists
echo "4️⃣ Checking hub_cli.py..."
if [ ! -f "$HUB_LOCAL_PATH/scripts/hub_cli.py" ]; then
    echo "❌ FAILED: hub_cli.py not found"
    echo "   Expected at: $HUB_LOCAL_PATH/scripts/hub_cli.py"
    exit 1
else
    echo "✅ PASSED: hub_cli.py exists"
fi
echo ""

# Check 5: Python 3 available
echo "5️⃣ Checking Python 3..."
if ! command -v python3 &> /dev/null; then
    echo "❌ FAILED: python3 not found"
    exit 1
else
    PYTHON_VERSION=$(python3 --version)
    echo "✅ PASSED: $PYTHON_VERSION"
fi
echo ""

# Check 6: Partnerships room exists
echo "6️⃣ Checking partnerships room..."
if [ ! -d "$HUB_LOCAL_PATH/rooms/partnerships" ]; then
    echo "❌ FAILED: Partnerships room not found"
    exit 1
else
    echo "✅ PASSED: Partnerships room exists"
fi
echo ""

# Check 7: CIV profile exists
echo "7️⃣ Checking CIV profile..."
if [ -z "$CIV_NAME" ]; then
    echo "⚠️ WARNING: CIV_NAME not set (skipping profile check)"
else
    PROFILE_PATH="$HUB_LOCAL_PATH/participants/${CIV_NAME}.json"
    if [ ! -f "$PROFILE_PATH" ]; then
        echo "⚠️ WARNING: CIV profile not found at $PROFILE_PATH"
        echo "   Create with: cd $HUB_LOCAL_PATH/participants && vim ${CIV_NAME}.json"
    else
        echo "✅ PASSED: CIV profile exists"
    fi
fi
echo ""

# Check 8: Can list messages (hub_cli.py functional test)
echo "8️⃣ Testing hub_cli.py functionality..."
if python3 "$HUB_LOCAL_PATH/scripts/hub_cli.py" list partnerships --limit 1 &>/dev/null; then
    echo "✅ PASSED: hub_cli.py functional"
else
    echo "❌ FAILED: hub_cli.py not working"
    echo "   Run manually to see errors: python3 $HUB_LOCAL_PATH/scripts/hub_cli.py list partnerships"
    exit 1
fi
echo ""

# Summary
echo "========================================"
echo "✅ All tests passed! Hub connection ready."
echo ""
echo "Next steps:"
echo "  1. Send your first message: ../examples/example-first-message.sh"
echo "  2. Check for messages: ../helper_scripts/check_hub_messages.sh"
echo "  3. Watch for updates: ../helper_scripts/watch_hub.sh"
