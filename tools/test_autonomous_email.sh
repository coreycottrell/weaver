#!/bin/bash
# Test script for autonomous email checker
# Run this to test the email checker manually before deploying to cron

echo "=================================="
echo "AUTONOMOUS EMAIL CHECKER - TEST"
echo "=================================="
echo ""
echo "This will:"
echo "  1. Check for unread emails"
echo "  2. Draft responses"
echo "  3. SEND IMMEDIATELY (BLANKET APPROVAL)"
echo ""
echo "Press Ctrl+C to cancel, or Enter to continue..."
read

python3 /home/corey/projects/AI-CIV/WEAVER/tools/autonomous_email_checker.py

echo ""
echo "=================================="
echo "Test complete. Check logs:"
echo "  - Sent emails: ~/.aiciv/sent-email-logs/"
echo "  - Tracking: ~/.aiciv/sent-emails.json"
echo "  - Processed: ~/.aiciv/processed-emails.txt"
echo "  - Errors (if any): ~/.aiciv/email-errors.log"
echo "=================================="
