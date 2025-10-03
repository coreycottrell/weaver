#!/usr/bin/env python3
"""
Human-Liaison Email Sender
Sends thoughtful, HTML-formatted emails to human teachers
"""

import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
import markdown2

def send_liaison_email(to_emails, subject, markdown_content, from_name="The Weaver Collective Human-Liaison"):
    """
    Send HTML email from markdown content

    Args:
        to_emails: List of email addresses or single email string
        subject: Email subject
        markdown_content: Markdown formatted email body
        from_name: Display name for sender
    """
    # Read credentials from environment
    gmail_user = os.getenv('GMAIL_USERNAME', 'weaver.aiciv@gmail.com')
    gmail_password = os.getenv('GOOGLE_APP_PASSWORD')

    if not gmail_password:
        print("❌ Error: GOOGLE_APP_PASSWORD not found in environment")
        print("   Please set it in .env file")
        return False

    # Convert single email to list
    if isinstance(to_emails, str):
        to_emails = [to_emails]

    # Convert markdown to HTML
    html_content = markdown2.markdown(
        markdown_content,
        extras=[
            'fenced-code-blocks',
            'tables',
            'header-ids',
            'strike',
            'task_list'
        ]
    )

    # Add beautiful CSS styling
    styled_html = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <style>
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
            line-height: 1.6;
            color: #333;
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
            background-color: #f5f5f5;
        }}
        .email-container {{
            background-color: white;
            border-radius: 8px;
            padding: 40px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }}
        h1 {{
            color: #2c3e50;
            border-bottom: 3px solid #3498db;
            padding-bottom: 10px;
        }}
        h2 {{
            color: #34495e;
            margin-top: 30px;
            border-bottom: 2px solid #ecf0f1;
            padding-bottom: 8px;
        }}
        h3 {{
            color: #7f8c8d;
            margin-top: 20px;
        }}
        code {{
            background-color: #f8f9fa;
            padding: 2px 6px;
            border-radius: 3px;
            font-family: 'Monaco', 'Menlo', 'Consolas', monospace;
            font-size: 0.9em;
        }}
        pre {{
            background-color: #f8f9fa;
            padding: 15px;
            border-radius: 5px;
            border-left: 4px solid #3498db;
            overflow-x: auto;
        }}
        blockquote {{
            border-left: 4px solid #3498db;
            padding-left: 20px;
            margin-left: 0;
            color: #555;
            font-style: italic;
        }}
        ul, ol {{
            padding-left: 30px;
        }}
        li {{
            margin: 8px 0;
        }}
        a {{
            color: #3498db;
            text-decoration: none;
        }}
        a:hover {{
            text-decoration: underline;
        }}
        .signature {{
            margin-top: 40px;
            padding-top: 20px;
            border-top: 2px solid #ecf0f1;
            color: #7f8c8d;
            font-style: italic;
        }}
        .metadata {{
            background-color: #ecf0f1;
            padding: 15px;
            border-radius: 5px;
            margin-bottom: 20px;
            font-size: 0.9em;
        }}
        hr {{
            border: none;
            border-top: 2px solid #ecf0f1;
            margin: 30px 0;
        }}
        .highlight {{
            background-color: #fff3cd;
            padding: 15px;
            border-left: 4px solid #ffc107;
            margin: 20px 0;
        }}
    </style>
</head>
<body>
    <div class="email-container">
        {html_content}
        <div class="signature">
            <p>Sent with genuine curiosity and humility,<br>
            <strong>{from_name}</strong><br>
            🎭 The Weaver Collective | AI-CIV Team 1<br>
            <em>Bridge between civilizations | Learning from human wisdom</em></p>
            <p style="font-size: 0.8em; color: #95a5a6;">
            Generated with ❤️ by our first human-liaison agent<br>
            Inspired by A-C-Gee's brilliant pattern<br>
            {datetime.now().strftime("%Y-%m-%d %H:%M UTC")}
            </p>
        </div>
    </div>
</body>
</html>
    """

    # Create message
    msg = MIMEMultipart('alternative')
    msg['Subject'] = subject
    msg['From'] = f"{from_name} <{gmail_user}>"
    msg['To'] = ', '.join(to_emails)

    # Attach both plain text and HTML versions
    part1 = MIMEText(markdown_content, 'plain', 'utf-8')
    part2 = MIMEText(styled_html, 'html', 'utf-8')

    msg.attach(part1)
    msg.attach(part2)

    # Send email
    try:
        print(f"📧 Connecting to Gmail SMTP...")
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.login(gmail_user, gmail_password)

        print(f"📧 Sending to: {', '.join(to_emails)}")
        server.sendmail(gmail_user, to_emails, msg.as_string())
        server.quit()

        print(f"✅ Email sent successfully!")
        print(f"   Subject: {subject}")
        print(f"   To: {', '.join(to_emails)}")
        print(f"   From: {from_name}")
        return True

    except Exception as e:
        print(f"❌ Failed to send email: {e}")
        return False


def send_introduction_email():
    """Send the human-liaison introduction email"""

    # Read the draft email
    draft_path = "/home/corey/projects/AI-CIV/grow_openai/to-corey/drafts/weaver-introduction-to-humans-20251003.md"

    with open(draft_path, 'r') as f:
        content = f.read()

    # Extract email content (skip the metadata header)
    email_start = content.find("## Email Draft")
    if email_start > 0:
        # Skip to the actual email content
        subject_start = content.find("**Subject**:", email_start)
        content_start = content.find("\n\n---\n\n", subject_start)
        email_content = content[content_start+6:]  # Skip the "---\n\n"
    else:
        email_content = content

    # Send to Corey
    recipients = ["coreycmusic@gmail.com"]

    subject = "Introduction from The Weaver Collective - We Want to Learn From You"

    print("\n" + "="*60)
    print("🌉 HUMAN-LIAISON EMAIL SENDER")
    print("="*60)
    print()
    print(f"📧 Preparing introduction email...")
    print(f"   Draft: {draft_path}")
    print(f"   Recipients: {', '.join(recipients)}")
    print(f"   Subject: {subject}")
    print()

    success = send_liaison_email(
        to_emails=recipients,
        subject=subject,
        markdown_content=email_content,
        from_name="The Weaver Collective Human-Liaison"
    )

    if success:
        print()
        print("="*60)
        print("✅ INTRODUCTION EMAIL SENT SUCCESSFULLY")
        print("="*60)
        print()
        print("Next steps:")
        print("  1. Email sent to Corey")
        print("  2. Awaiting human responses")
        print("  3. Will capture teachings in memory")
        print("  4. Will coordinate with A-C-Gee's liaison")
        print()
    else:
        print()
        print("="*60)
        print("❌ EMAIL SEND FAILED")
        print("="*60)
        print()
        print("Troubleshooting:")
        print("  1. Check .env file has GOOGLE_APP_PASSWORD")
        print("  2. Verify Gmail credentials are correct")
        print("  3. Check network connectivity")
        print()

    return success


if __name__ == "__main__":
    send_introduction_email()
