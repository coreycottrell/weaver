#!/usr/bin/env python3
"""Send email with file attachments"""

import smtplib
import sys
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from pathlib import Path
from datetime import datetime

# Email configuration
SMTP_SERVER = 'smtp.gmail.com'
SMTP_PORT = 587
FROM_EMAIL = 'weaver.aiciv@gmail.com'
FROM_NAME = 'AI-CIV WEAVER'

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
                return password.replace(' ', '')

    raise ValueError("GOOGLE_APP_PASSWORD not found in .env file")

def send_email_with_attachments(to, subject, body, attachments):
    """Send email with attachments"""
    try:
        # Create message
        msg = MIMEMultipart()
        msg['Subject'] = subject
        msg['From'] = f"{FROM_NAME} <{FROM_EMAIL}>"
        msg['To'] = to

        # Attach body
        msg.attach(MIMEText(body, 'plain'))

        # Attach files
        for filepath in attachments:
            filepath = Path(filepath)
            if not filepath.exists():
                print(f"⚠️  Warning: File not found: {filepath}")
                continue

            with open(filepath, 'rb') as f:
                part = MIMEBase('application', 'octet-stream')
                part.set_payload(f.read())

            encoders.encode_base64(part)
            part.add_header(
                'Content-Disposition',
                f'attachment; filename={filepath.name}'
            )
            msg.attach(part)
            print(f"✅ Attached: {filepath.name}")

        # Send email
        password = get_password()
        print(f"\n📧 Connecting to {SMTP_SERVER}...")
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(FROM_EMAIL, password)

            print(f"📤 Sending email to {to}...")
            server.send_message(msg)

        print("\n" + "="*70)
        print("✅ Email sent successfully!")
        print("="*70)
        print(f"From: {FROM_NAME} <{FROM_EMAIL}>")
        print(f"To: {to}")
        print(f"Subject: {subject}")
        print(f"Attachments: {len(attachments)}")
        print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("="*70)

        return True

    except Exception as e:
        print(f"\n❌ Error sending email: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    if len(sys.argv) < 4:
        print("Usage: send_email_with_attachments.py <to> <subject> <body> [attachment1] [attachment2] ...")
        sys.exit(1)

    to = sys.argv[1]
    subject = sys.argv[2]
    body = sys.argv[3]
    attachments = sys.argv[4:] if len(sys.argv) > 4 else []

    success = send_email_with_attachments(to, subject, body, attachments)
    sys.exit(0 if success else 1)
