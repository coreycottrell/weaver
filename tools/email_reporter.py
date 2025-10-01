#!/usr/bin/env python3
"""
AI-CIV Email Reporter
Automatically emails mission reports to coreycmusic@gmail.com
"""

import os
import sys
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from datetime import datetime
from pathlib import Path
import json

sys.path.insert(0, str(Path(__file__).parent.parent))

from dotenv import load_dotenv
load_dotenv()

# Email configuration
GMAIL_USERNAME = os.getenv('GMAIL_USERNAME')
GMAIL_APP_PASSWORD = os.getenv('GOOGLE_APP_PASSWORD')
RECIPIENT_EMAIL = 'coreycmusic@gmail.com'

# Paths
STATE_FILE = Path(__file__).parent.parent / ".claude/observatory/dashboard-state.json"
MEMORY_DIR = Path(__file__).parent.parent / ".claude/memory"


def load_state():
    """Load Observatory state"""
    if not STATE_FILE.exists():
        return None

    with open(STATE_FILE, 'r') as f:
        return json.load(f)


def send_email(subject, body_html, attachments=None):
    """Send email via Gmail SMTP"""
    try:
        # Create message
        msg = MIMEMultipart('alternative')
        msg['From'] = f"AI-CIV Collective <{GMAIL_USERNAME}>"
        msg['To'] = RECIPIENT_EMAIL
        msg['Subject'] = subject

        # Add HTML body
        html_part = MIMEText(body_html, 'html')
        msg.attach(html_part)

        # Add attachments
        if attachments:
            for filepath in attachments:
                if Path(filepath).exists():
                    with open(filepath, 'rb') as f:
                        part = MIMEBase('application', 'octet-stream')
                        part.set_payload(f.read())
                        encoders.encode_base64(part)
                        part.add_header(
                            'Content-Disposition',
                            f'attachment; filename={Path(filepath).name}'
                        )
                        msg.attach(part)

        # Send email
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login(GMAIL_USERNAME, GMAIL_APP_PASSWORD.replace(' ', ''))
            server.send_message(msg)

        print(f"✅ Email sent successfully to {RECIPIENT_EMAIL}")
        return True

    except Exception as e:
        print(f"❌ Failed to send email: {e}")
        return False


def format_agent_report(agent):
    """Format agent data for email"""
    status_emoji = {
        'completed': '✅',
        'working': '⟳',
        'failed': '❌',
        'pending': '⏸️'
    }

    findings_html = ""
    if agent.get('findings'):
        findings_html = "<ul>"
        for finding in agent['findings']:
            findings_html += f"<li>{finding}</li>"
        findings_html += "</ul>"

    return f"""
    <div style="border-left: 4px solid #63b3ed; padding: 15px; margin: 10px 0; background: #f8f9fa;">
        <h3 style="color: #1a1f3a; margin-top: 0;">
            {status_emoji.get(agent.get('status', 'unknown'), '❓')} {agent['name']}
        </h3>
        <p><strong>Status:</strong> {agent.get('status', 'unknown').upper()}</p>
        <p><strong>Progress:</strong> {agent.get('progress', 0)}%</p>
        <p><strong>Activity:</strong> {agent.get('currentActivity', 'N/A')}</p>
        {f'<p><strong>Findings:</strong></p>{findings_html}' if findings_html else ''}
    </div>
    """


def send_deployment_report(deployment):
    """Send report for completed deployment"""
    task = deployment.get('task', 'Unknown mission')
    deployment_id = deployment.get('id', 'unknown')
    completed_at = deployment.get('completedAt', datetime.now().isoformat())

    # Format timestamp
    try:
        dt = datetime.fromisoformat(completed_at)
        time_str = dt.strftime("%B %d, %Y at %I:%M %p")
    except:
        time_str = completed_at

    # Count statistics
    total_agents = len(deployment.get('agents', []))
    completed_agents = len([a for a in deployment.get('agents', []) if a.get('status') == 'completed'])
    total_findings = sum(len(a.get('findings', [])) for a in deployment.get('agents', []))

    # Format agents
    agents_html = ""
    for agent in deployment.get('agents', []):
        agents_html += format_agent_report(agent)

    # Synthesis
    synthesis = deployment.get('synthesis', 'No synthesis provided')

    # Build email
    subject = f"🎭 Mission Complete: {task}"

    body_html = f"""
    <html>
    <head>
        <style>
            body {{ font-family: 'SF Mono', 'Menlo', monospace; color: #1a1f3a; }}
            .header {{ background: linear-gradient(135deg, #63b3ed 0%, #a78bfa 100%);
                       color: white; padding: 30px; text-align: center; border-radius: 10px; }}
            .stats {{ display: flex; justify-content: space-around; margin: 20px 0; }}
            .stat {{ text-align: center; padding: 15px; background: #f8f9fa; border-radius: 8px; }}
            .stat-value {{ font-size: 2em; font-weight: bold; color: #63b3ed; }}
            .stat-label {{ color: #6b7280; font-size: 0.9em; }}
            .section {{ margin: 20px 0; }}
            .synthesis {{ background: #fff3cd; padding: 20px; border-radius: 8px;
                          border-left: 4px solid #fbbf24; }}
        </style>
    </head>
    <body>
        <div class="header">
            <h1>🎭 AI-CIV Collective Mission Report</h1>
            <p>Deployment ID: {deployment_id}</p>
            <p>Completed: {time_str}</p>
        </div>

        <div class="section">
            <h2>📋 Mission</h2>
            <p><strong>{task}</strong></p>
        </div>

        <div class="stats">
            <div class="stat">
                <div class="stat-value">{total_agents}</div>
                <div class="stat-label">Agents Deployed</div>
            </div>
            <div class="stat">
                <div class="stat-value">{completed_agents}</div>
                <div class="stat-label">Completed</div>
            </div>
            <div class="stat">
                <div class="stat-value">{total_findings}</div>
                <div class="stat-label">Total Findings</div>
            </div>
        </div>

        <div class="section">
            <h2>🤖 Agent Reports</h2>
            {agents_html}
        </div>

        <div class="section">
            <h2>🎯 Synthesis</h2>
            <div class="synthesis">
                {synthesis}
            </div>
        </div>

        <hr style="margin: 30px 0; border: none; border-top: 2px solid #e5e7eb;">

        <p style="text-align: center; color: #6b7280; font-size: 0.9em;">
            Generated by The Conductor • AI-CIV Collective Observatory<br>
            <a href="http://localhost:5000">View Real-Time Dashboard</a>
        </p>
    </body>
    </html>
    """

    # Find related synthesis files
    attachments = []
    synthesis_files = list(MEMORY_DIR.glob("**/*synthesis*.md"))
    if synthesis_files:
        # Attach most recent synthesis
        attachments.append(str(synthesis_files[0]))

    return send_email(subject, body_html, attachments)


def send_agent_update(agent_name, status, activity, findings=None):
    """Send quick update email for agent status change"""
    status_emoji = {
        'completed': '✅',
        'working': '⟳',
        'failed': '❌',
        'pending': '⏸️'
    }

    subject = f"{status_emoji.get(status, '❓')} Agent Update: {agent_name}"

    findings_html = ""
    if findings:
        findings_html = "<ul>"
        for finding in findings:
            findings_html += f"<li>{finding}</li>"
        findings_html += "</ul>"

    body_html = f"""
    <html>
    <body style="font-family: 'SF Mono', monospace; color: #1a1f3a;">
        <div style="background: linear-gradient(135deg, #63b3ed 0%, #a78bfa 100%);
                    color: white; padding: 20px; text-align: center; border-radius: 10px;">
            <h1>🎭 Agent Status Update</h1>
        </div>

        <div style="margin: 20px 0; padding: 20px; background: #f8f9fa; border-radius: 8px;">
            <h2 style="color: #1a1f3a; margin-top: 0;">{agent_name}</h2>
            <p><strong>Status:</strong> {status.upper()} {status_emoji.get(status, '❓')}</p>
            <p><strong>Activity:</strong> {activity}</p>
            {f'<p><strong>Latest Findings:</strong></p>{findings_html}' if findings_html else ''}
        </div>

        <p style="text-align: center; color: #6b7280; font-size: 0.9em;">
            <a href="http://localhost:5000">View Real-Time Dashboard</a>
        </p>
    </body>
    </html>
    """

    return send_email(subject, body_html)


def send_collective_summary():
    """Send daily/weekly collective summary"""
    state = load_state()
    if not state:
        return False

    stats = state.get('stats', {})
    recent_history = state.get('history', [])[:5]

    history_html = ""
    for dep in recent_history:
        history_html += f"""
        <div style="margin: 10px 0; padding: 15px; background: #f8f9fa; border-radius: 8px;">
            <p><strong>{dep.get('task', 'Unknown')}</strong></p>
            <p style="color: #6b7280; font-size: 0.9em;">
                {len(dep.get('agents', []))} agents •
                Completed {dep.get('completedAt', 'recently')}
            </p>
        </div>
        """

    subject = "📊 AI-CIV Collective Weekly Summary"

    body_html = f"""
    <html>
    <body style="font-family: 'SF Mono', monospace; color: #1a1f3a;">
        <div style="background: linear-gradient(135deg, #63b3ed 0%, #a78bfa 100%);
                    color: white; padding: 30px; text-align: center; border-radius: 10px;">
            <h1>🎭 Collective Intelligence Summary</h1>
            <p>Your AI-CIV agents have been busy!</p>
        </div>

        <div style="display: flex; justify-content: space-around; margin: 20px 0;">
            <div style="text-align: center; padding: 15px;">
                <div style="font-size: 2em; font-weight: bold; color: #63b3ed;">
                    {stats.get('totalDeployments', 0)}
                </div>
                <div style="color: #6b7280;">Total Deployments</div>
            </div>
            <div style="text-align: center; padding: 15px;">
                <div style="font-size: 2em; font-weight: bold; color: #a78bfa;">
                    {stats.get('totalAgentsDeployed', 0)}
                </div>
                <div style="color: #6b7280;">Agents Deployed</div>
            </div>
            <div style="text-align: center; padding: 15px;">
                <div style="font-size: 2em; font-weight: bold; color: #10b981;">
                    {stats.get('totalFindings', 0)}
                </div>
                <div style="color: #6b7280;">Findings Generated</div>
            </div>
        </div>

        <div style="margin: 20px 0;">
            <h2>Recent Missions</h2>
            {history_html if history_html else '<p style="color: #6b7280;">No recent deployments</p>'}
        </div>

        <p style="text-align: center; color: #6b7280; font-size: 0.9em;">
            <a href="http://localhost:5000">View Real-Time Dashboard</a>
        </p>
    </body>
    </html>
    """

    return send_email(subject, body_html)


if __name__ == '__main__':
    # Test email
    print("📧 Testing email system...")

    test_subject = "🎭 AI-CIV Collective - Email System Online"
    test_body = """
    <html>
    <body style="font-family: monospace; color: #1a1f3a;">
        <div style="background: linear-gradient(135deg, #63b3ed 0%, #a78bfa 100%);
                    color: white; padding: 30px; text-align: center; border-radius: 10px;">
            <h1>🎭 Email Reporting System Active</h1>
        </div>

        <div style="margin: 20px; padding: 20px; background: #f8f9fa; border-radius: 8px;">
            <p>The AI-CIV Collective email reporting system is now active and ready to send you mission reports!</p>

            <h3>What You'll Receive:</h3>
            <ul>
                <li>✅ <strong>Deployment Complete</strong> - Full mission reports with agent findings</li>
                <li>⟳ <strong>Agent Updates</strong> - Real-time status updates for critical agents</li>
                <li>📊 <strong>Collective Summaries</strong> - Weekly intelligence briefings</li>
            </ul>

            <p>All reports will be sent to: <strong>coreycmusic@gmail.com</strong></p>
        </div>

        <p style="text-align: center; color: #6b7280;">
            <a href="http://localhost:5000">View Real-Time Dashboard</a>
        </p>
    </body>
    </html>
    """

    if send_email(test_subject, test_body):
        print("✅ Email system test successful!")
    else:
        print("❌ Email system test failed")
