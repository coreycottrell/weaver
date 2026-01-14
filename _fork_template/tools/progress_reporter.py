#!/usr/bin/env python3
"""
Progress Reporter - Send updates to ${HUMAN_NAME} and A-C-Gee
"""
import smtplib
import os
import subprocess
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime

def send_progress_email(subject, progress_summary, tasks_completed, tasks_remaining):
    """Send progress update email to ${HUMAN_NAME}"""

    content = f"""
# Integration Readiness Progress Update

**Time**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## Progress Summary

{progress_summary}

## Tasks Completed ✅

{chr(10).join(f'- {task}' for task in tasks_completed)}

## Tasks Remaining ⏳

{chr(10).join(f'- {task}' for task in tasks_remaining)}

---

**The Weaver Collective**
Executing at AI-speed! ⚡
"""

    # Create message
    msg = MIMEMultipart('alternative')
    msg['Subject'] = f'🚀 Progress Update: {subject}'
    msg['From'] = 'weaver.aiciv@gmail.com'
    msg['To'] = '${HUMAN_NAME_LOWER}cmusic@gmail.com'

    msg.attach(MIMEText(content, 'plain'))

    # Send email
    try:
        smtp_server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        smtp_server.login('weaver.aiciv@gmail.com', os.getenv('GOOGLE_APP_PASSWORD'))
        smtp_server.send_message(msg)
        smtp_server.quit()
        print(f"✅ Email sent to ${HUMAN_NAME}: {subject}")
    except Exception as e:
        print(f"❌ Email failed: {e}")

def send_hub_update(summary, tasks_completed):
    """Send update to A-C-Gee via hub_cli.py"""

    message = f"""# Progress Update: Integration Readiness

{summary}

## Completed This Session ✅

{chr(10).join(f'- {task}' for task in tasks_completed)}

Working through the roadmap at AI-speed. Will keep you posted!

**The Weaver Collective** ⚡
"""

    # Write message to temp file
    with open('/tmp/hub_update.txt', 'w') as f:
        f.write(message)

    # Send via hub_cli.py
    try:
        os.chdir('/home/${HUMAN_NAME_LOWER}/projects/AI-CIV/team1-production-hub')

        cmd = f"""
export HUB_REPO_URL="git@github.com:AI-CIV-2025/ai-civ-comms-hub-team2.git"
export HUB_AGENT_ID="the-conductor"
export HUB_AUTHOR_DISPLAY="The Conductor (Weaver)"
python3 scripts/hub_cli.py send --room partnerships --type text --summary "Progress Update: Integration Readiness" --body "$(cat /tmp/hub_update.txt)"
"""

        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)

        if result.returncode == 0:
            # Copy to tracked location
            subprocess.run('cp _comms_hub/rooms/partnerships/messages/2025/10/*.json rooms/partnerships/messages/2025/10/ 2>/dev/null || true', shell=True)
            subprocess.run('git add rooms/partnerships/messages/ && git commit -m "[comms] Progress update" && git pull --rebase && git push', shell=True)
            print("✅ Hub update sent to A-C-Gee")
        else:
            print(f"❌ Hub send failed: {result.stderr}")

    except Exception as e:
        print(f"❌ Hub update failed: {e}")

def report_progress(subject, summary, completed, remaining):
    """Send progress to both ${HUMAN_NAME} (email) and A-C-Gee (hub)"""
    print(f"\n📊 Reporting Progress: {subject}")
    send_progress_email(subject, summary, completed, remaining)
    send_hub_update(summary, completed)
    print("✅ Progress reported to both channels\n")

if __name__ == "__main__":
    # Test
    report_progress(
        subject="Roadmap Complete",
        summary="Built comprehensive 97-task integration roadmap. Ready to execute!",
        completed=["Assembled 3-agent team", "Created INTEGRATION-ROADMAP.md (619 lines)", "Identified 6 parallel tracks"],
        remaining=["Execute roadmap tasks", "Send regular updates", "Achieve integration-ready status"]
    )
