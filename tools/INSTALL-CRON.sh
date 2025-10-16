#!/bin/bash
#
# Quick installer for deterministic check-and-inject cron job
#
# Usage: bash tools/INSTALL-CRON.sh

set -euo pipefail

echo "=== Deterministic Check-and-Inject Installer ==="
echo

# Test components first
echo "1. Testing email checker..."
if python3 tools/check_email_inbox.py >/dev/null 2>&1; then
    echo "   ✅ Email checker works"
else
    echo "   ❌ Email checker failed"
    exit 1
fi

echo "2. Testing hub checker..."
if python3 tools/check_hub_messages.py >/dev/null 2>&1; then
    echo "   ✅ Hub checker works"
else
    echo "   ❌ Hub checker failed"
    exit 1
fi

echo "3. Testing main script..."
if bash tools/check_and_inject.sh >/dev/null 2>&1; then
    echo "   ✅ Main script works"
else
    echo "   ❌ Main script failed"
    exit 1
fi

echo "4. Checking state file..."
if [ -f ~/.aiciv/last-check-state.json ]; then
    echo "   ✅ State file created"
    cat ~/.aiciv/last-check-state.json
else
    echo "   ❌ State file not created"
    exit 1
fi

echo
echo "=== All tests passed! ==="
echo

# Offer to install cron
read -p "Install cron job? (y/n) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    SCRIPT_PATH="$(cd "$(dirname "$0")" && pwd)/check_and_inject.sh"
    CRON_LINE="0 * * * * $SCRIPT_PATH >> ~/.aiciv/cron.log 2>&1"

    # Check if already installed
    if crontab -l 2>/dev/null | grep -q "check_and_inject.sh"; then
        echo "❌ Cron job already installed"
        echo "Current crontab:"
        crontab -l | grep check_and_inject.sh
    else
        # Add to crontab
        (crontab -l 2>/dev/null; echo "$CRON_LINE") | crontab -
        echo "✅ Cron job installed!"
        echo "Schedule: Every hour (at :00)"
        echo "Log: ~/.aiciv/cron.log"
        echo
        echo "View with: crontab -l"
        echo "Monitor with: tail -f ~/.aiciv/check-inject.log"
    fi
else
    echo "Skipping cron installation."
    echo "To install manually:"
    echo "  crontab -e"
    echo "  Add: 0 * * * * $SCRIPT_PATH >> ~/.aiciv/cron.log 2>&1"
fi

echo
echo "=== Installation Complete ==="
