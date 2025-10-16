#!/usr/bin/env python3
"""
Email Sending Tool for human-liaison agent
Autonomous email sending with tracking and duplicate prevention
"""

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from pathlib import Path
from typing import List, Optional, Union
import json
import hashlib
from datetime import datetime
import os

# Email configuration
SMTP_SERVER = 'smtp.gmail.com'
SMTP_PORT = 587
FROM_EMAIL = 'weaver.aiciv@gmail.com'
FROM_NAME = 'AI-CIV WEAVER: Human-Liaison'

# Load password from .env
def get_password():
    """Load Gmail app password from .env file"""
    env_file = Path(__file__).parent.parent / '.env'
    if not env_file.exists():
        raise FileNotFoundError(f".env file not found at {env_file}")

    with open(env_file) as f:
        for line in f:
            line = line.strip()
            if line.startswith('GOOGLE_APP_PASSWORD='):
                password = line.split('=', 1)[1].strip('"').strip("'")
                # Remove spaces from password (Gmail app passwords have spaces for readability)
                return password.replace(' ', '')

    raise ValueError("GOOGLE_APP_PASSWORD not found in .env file")

# Sent emails tracking
SENT_EMAILS_PATH = Path.home() / '.aiciv' / 'sent-emails.json'

def _get_email_hash(to: Union[str, List[str]], subject: str, content_preview: str) -> str:
    """Generate unique hash for email to detect duplicates"""
    to_list = [to] if isinstance(to, str) else to
    to_str = ','.join(sorted(to_list))
    content = f"{to_str}|{subject}|{content_preview[:100]}"
    return hashlib.md5(content.encode()).hexdigest()

def _load_sent_emails() -> List[dict]:
    """Load sent emails tracking log"""
    if not SENT_EMAILS_PATH.exists():
        SENT_EMAILS_PATH.parent.mkdir(parents=True, exist_ok=True)
        return []
    try:
        with open(SENT_EMAILS_PATH, 'r') as f:
            return json.load(f)
    except (json.JSONDecodeError, FileNotFoundError):
        return []

def _save_sent_email(to: Union[str, List[str]], subject: str, content_preview: str) -> None:
    """Record sent email to prevent duplicates"""
    sent_emails = _load_sent_emails()
    email_hash = _get_email_hash(to, subject, content_preview)

    sent_emails.append({
        'hash': email_hash,
        'to': to if isinstance(to, str) else to,
        'subject': subject,
        'preview': content_preview[:100],
        'timestamp': datetime.now().isoformat()
    })

    # Keep only last 100 emails
    sent_emails = sent_emails[-100:]

    SENT_EMAILS_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(SENT_EMAILS_PATH, 'w') as f:
        json.dump(sent_emails, f, indent=2)

def _check_duplicate(to: Union[str, List[str]], subject: str, content_preview: str) -> bool:
    """Check if this email was recently sent (within last 100 emails)"""
    sent_emails = _load_sent_emails()
    email_hash = _get_email_hash(to, subject, content_preview)

    for sent in sent_emails:
        if sent.get('hash') == email_hash:
            return True
    return False

def send_email(
    to: Union[str, List[str]],
    subject: str,
    body: str,
    reply_to_message_id: Optional[str] = None,
    in_reply_to: Optional[str] = None,
    references: Optional[str] = None,
    skip_duplicate_check: bool = False
) -> bool:
    """
    Send email via Gmail SMTP with threading support.

    Args:
        to: Recipient email(s) - string or list
        subject: Email subject line
        body: Email body (plain text)
        reply_to_message_id: Message-ID to reply to (for threading)
        in_reply_to: In-Reply-To header value
        references: References header value (for threading)
        skip_duplicate_check: If True, skip duplicate detection

    Returns:
        True if sent successfully, False otherwise
    """
    try:
        # Check for duplicate (unless explicitly skipped)
        if not skip_duplicate_check:
            if _check_duplicate(to, subject, body[:200]):
                print(f"\n⚠️  DUPLICATE DETECTED - Email not sent")
                print(f"To: {to}")
                print(f"Subject: {subject}")
                print(f"This exact email was already sent recently.")
                print(f"If you need to resend, use skip_duplicate_check=True")
                return False

        # Normalize recipients to lists
        to_list = [to] if isinstance(to, str) else to

        # Create message
        msg = MIMEMultipart('alternative')
        msg['Subject'] = subject
        msg['From'] = f"{FROM_NAME} <{FROM_EMAIL}>"
        msg['To'] = ', '.join(to_list)

        # Add threading headers if provided
        if reply_to_message_id:
            msg['In-Reply-To'] = reply_to_message_id
            msg['References'] = reply_to_message_id
        elif in_reply_to:
            msg['In-Reply-To'] = in_reply_to
            if references:
                msg['References'] = references

        # Attach plain text content
        text_part = MIMEText(body, 'plain')
        msg.attach(text_part)

        # Send email
        password = get_password()
        print(f"📧 Connecting to {SMTP_SERVER}...")
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(FROM_EMAIL, password)

            print(f"📤 Sending email to {len(to_list)} recipient(s)...")
            server.send_message(msg)

        print("\n" + "="*70)
        print("✅ Email sent successfully!")
        print("="*70)
        print(f"From: {FROM_NAME} <{FROM_EMAIL}>")
        print(f"To: {', '.join(to_list)}")
        print(f"Subject: {subject}")
        print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("="*70)

        # Record sent email to prevent duplicates
        _save_sent_email(to, subject, body[:200])

        # Also save full email to file for human-liaison memory
        email_log_dir = Path.home() / '.aiciv' / 'sent-email-logs'
        email_log_dir.mkdir(parents=True, exist_ok=True)

        timestamp = datetime.now().strftime('%Y%m%d-%H%M%S')
        recipient_clean = to_list[0].split('@')[0] if to_list else 'unknown'
        log_file = email_log_dir / f"{timestamp}-to-{recipient_clean}.txt"

        with open(log_file, 'w') as f:
            f.write(f"From: {FROM_NAME} <{FROM_EMAIL}>\n")
            f.write(f"To: {', '.join(to_list)}\n")
            f.write(f"Subject: {subject}\n")
            f.write(f"Date: {datetime.now().isoformat()}\n")
            if reply_to_message_id or in_reply_to:
                f.write(f"In-Reply-To: {reply_to_message_id or in_reply_to}\n")
            f.write(f"\n{'-'*70}\n\n")
            f.write(body)

        print(f"📁 Email log saved: {log_file}")

        return True

    except Exception as e:
        print(f"\n❌ Error sending email: {e}")
        import traceback
        traceback.print_exc()
        return False

def mark_email_as_read(email_id: str, mail_connection) -> bool:
    """
    Mark an email as read in Gmail.

    Args:
        email_id: Email ID to mark as read
        mail_connection: Active IMAP connection

    Returns:
        True if marked successfully, False otherwise
    """
    try:
        mail_connection.store(email_id, '+FLAGS', '\\Seen')
        return True
    except Exception as e:
        print(f"❌ Error marking email as read: {e}")
        return False

# Example usage
if __name__ == "__main__":
    import sys

    if len(sys.argv) < 4:
        print("Usage: send_email.py <to> <subject> <body>")
        print("Example: send_email.py coreycmusic@gmail.com 'Test' 'Hello from human-liaison'")
        sys.exit(1)

    to = sys.argv[1]
    subject = sys.argv[2]
    body = sys.argv[3]

    success = send_email(to, subject, body)
    sys.exit(0 if success else 1)
