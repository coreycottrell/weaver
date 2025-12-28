#!/bin/bash
# Telegram Health Check Cron Setup
#
# This script helps set up regular health checks for Telegram infrastructure.
#
# Recommended cadence: every 30 minutes
# - Balances monitoring frequency with noise
# - Catches issues within reasonable timeframe
# - Logs results for debugging
#
# Usage:
#   bash tools/telegram_health_cron_setup.sh        # Show instructions
#   bash tools/telegram_health_cron_setup.sh add    # Add to crontab
#   bash tools/telegram_health_cron_setup.sh remove # Remove from crontab

PROJECT_DIR="/home/corey/projects/AI-CIV/WEAVER"
HEALTH_SCRIPT="${PROJECT_DIR}/tools/telegram_health_check.py"
CRON_LOG="/tmp/telegram_health_cron.log"

# The cron job line
CRON_JOB="*/30 * * * * /usr/bin/python3 ${HEALTH_SCRIPT} --quiet >> ${CRON_LOG} 2>&1"

show_instructions() {
    echo "=============================================="
    echo "Telegram Health Check Cron Setup"
    echo "=============================================="
    echo ""
    echo "Health check script: ${HEALTH_SCRIPT}"
    echo "Cron log file: ${CRON_LOG}"
    echo ""
    echo "Recommended cron job (every 30 minutes):"
    echo ""
    echo "  ${CRON_JOB}"
    echo ""
    echo "To add manually:"
    echo "  1. Run: crontab -e"
    echo "  2. Add the line above"
    echo "  3. Save and exit"
    echo ""
    echo "Or use this script:"
    echo "  bash $0 add     # Add cron job"
    echo "  bash $0 remove  # Remove cron job"
    echo ""
    echo "To check health manually:"
    echo "  python3 ${HEALTH_SCRIPT}           # Connectivity check only"
    echo "  python3 ${HEALTH_SCRIPT} --send    # Also send test message"
    echo ""
    echo "To view cron log:"
    echo "  tail -20 ${CRON_LOG}"
    echo ""
}

add_cron() {
    # Check if already exists
    if crontab -l 2>/dev/null | grep -q "telegram_health_check.py"; then
        echo "Telegram health check already in crontab!"
        echo ""
        echo "Current cron entries:"
        crontab -l | grep telegram
        exit 0
    fi

    # Add to crontab
    (crontab -l 2>/dev/null; echo "${CRON_JOB}") | crontab -

    echo "Added health check to crontab (every 30 minutes)"
    echo ""
    echo "Verify with: crontab -l | grep telegram"
    echo ""
    crontab -l | grep telegram
}

remove_cron() {
    # Remove from crontab
    crontab -l 2>/dev/null | grep -v "telegram_health_check.py" | crontab -

    echo "Removed telegram health check from crontab"
    echo ""
    echo "Current crontab:"
    crontab -l 2>/dev/null || echo "(empty)"
}

case "${1:-}" in
    add)
        add_cron
        ;;
    remove)
        remove_cron
        ;;
    *)
        show_instructions
        ;;
esac
