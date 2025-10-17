#!/usr/bin/env python3
"""
Check email inbox for unread messages
Returns count of unread messages for autonomous system
"""

import os
import sys
import imaplib
from pathlib import Path

# Load environment from .env file manually
env_file = Path(__file__).parent.parent / '.env'
if env_file.exists():
    with open(env_file) as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#') and '=' in line:
                key, value = line.split('=', 1)
                os.environ[key] = value

GMAIL_USERNAME = os.getenv('GMAIL_USERNAME')
GMAIL_APP_PASSWORD = os.getenv('GOOGLE_APP_PASSWORD')

def check_unread_count():
    """Check how many unread messages exist"""
    try:
        # Connect to Gmail IMAP
        mail = imaplib.IMAP4_SSL('imap.gmail.com')
        mail.login(GMAIL_USERNAME, GMAIL_APP_PASSWORD.replace(' ', ''))
        
        # Select inbox
        mail.select('INBOX')
        
        # Search for unread messages
        status, messages = mail.search(None, 'UNSEEN')
        
        if status != 'OK':
            return 0
        
        # Count unread
        unread_ids = messages[0].split()
        count = len(unread_ids)
        
        # Logout
        mail.logout()
        
        return count
        
    except Exception as e:
        print(f"Error checking email: {e}", file=sys.stderr)
        return 0

if __name__ == '__main__':
    count = check_unread_count()
    print(count)  # Just the number for easy parsing
    sys.exit(0)  # Always exit 0 for success (count in stdout)
