# Cron Installation Guide - Hourly Email Checker

**Quick reference for deploying the autonomous email checker**

---

## Step 1: Test Manually First

```bash
# Run the test script
/home/corey/projects/AI-CIV/grow_openai/tools/test_autonomous_email.sh

# OR run directly
python3 /home/corey/projects/AI-CIV/grow_openai/tools/autonomous_email_checker.py
```

**Expected**: Connects to Gmail, checks email, processes (if any unread), logs activity.

---

## Step 2: Install Cron Job

### Option A: Hourly (Recommended)

```bash
# Edit crontab
crontab -e

# Add this line (checks every hour on the hour):
0 * * * * /usr/bin/python3 /home/corey/projects/AI-CIV/grow_openai/tools/autonomous_email_checker.py >> /home/corey/projects/AI-CIV/grow_openai/.logs/email-checker.log 2>&1

# Save and exit (:wq in vim, Ctrl+X in nano)
```

### Option B: Every 10 Minutes (Testing Only)

```bash
# Edit crontab
crontab -e

# Add this line (checks every 10 minutes):
*/10 * * * * /usr/bin/python3 /home/corey/projects/AI-CIV/grow_openai/tools/autonomous_email_checker.py >> /home/corey/projects/AI-CIV/grow_openai/.logs/email-checker.log 2>&1

# After 24-48 hours, change to hourly (Option A)
```

---

## Step 3: Verify Cron Installed

```bash
# List current cron jobs
crontab -l

# Should see the email checker line
```

---

## Step 4: Monitor First Run

**Wait for next hour mark** (e.g., if it's 2:15pm, wait until 3:00pm)

**Then check log**:

```bash
# View recent cron runs
tail -50 /home/corey/projects/AI-CIV/grow_openai/.logs/email-checker.log

# Watch log in real-time (optional)
tail -f /home/corey/projects/AI-CIV/grow_openai/.logs/email-checker.log
```

**Expected output**:

```
==================================================================
AUTONOMOUS EMAIL CHECK - 2025-10-19T15:00:02
==================================================================

📧 Connecting to Gmail IMAP...
📬 Found 0 unread email(s)

✅ Autonomous email check complete
   New emails processed: 0
==================================================================
```

---

## Step 5: Test with Real Email

1. **Send email** to `weaver.aiciv@gmail.com`
2. **Wait** up to 1 hour (or 10 minutes if using Option B)
3. **Check** your inbox for quick acknowledgment
4. **Verify** logs:

```bash
# Check sent email logs
ls -lt ~/.aiciv/sent-email-logs/ | head -5

# View latest sent email
cat ~/.aiciv/sent-email-logs/$(ls -t ~/.aiciv/sent-email-logs/ | head -1)
```

---

## Troubleshooting

### Cron Not Running

**Check cron service**:

```bash
# On systemd systems (most Linux)
systemctl status cron

# On older systems
service cron status
```

**Start if needed**:

```bash
sudo systemctl start cron
```

### Authentication Errors

**Check for alert**:

```bash
cat /home/corey/projects/AI-CIV/grow_openai/to-corey/CRITICAL-EMAIL-AUTH-FAILURE.md
```

**Fix**: Update `GOOGLE_APP_PASSWORD` in `.env`

### Send Errors

**Check error log**:

```bash
cat ~/.aiciv/email-errors.log
```

**Check alert**:

```bash
cat /home/corey/projects/AI-CIV/grow_openai/to-corey/EMAIL-SEND-FAILURE-ALERT.md
```

### No Output in Log

**Possible causes**:
1. Cron not running (see above)
2. Python path wrong (verify: `which python3`)
3. Permissions issue (verify: `ls -la tools/autonomous_email_checker.py`)

**Quick fix**:

```bash
# Make sure script is executable
chmod +x /home/corey/projects/AI-CIV/grow_openai/tools/autonomous_email_checker.py

# Make sure log directory exists
mkdir -p /home/corey/projects/AI-CIV/grow_openai/.logs
```

---

## Disabling Cron (If Needed)

**Temporary disable**:

```bash
# Edit crontab
crontab -e

# Comment out the line (add # at start):
# 0 * * * * /usr/bin/python3 /home/corey/projects/AI-CIV/grow_openai/tools/autonomous_email_checker.py >> /home/corey/projects/AI-CIV/grow_openai/.logs/email-checker.log 2>&1

# Save and exit
```

**Permanent remove**:

```bash
# Edit crontab
crontab -e

# Delete the entire line

# Save and exit
```

---

## Checking Logs

### Cron Runs

```bash
# Last 50 lines
tail -50 /home/corey/projects/AI-CIV/grow_openai/.logs/email-checker.log

# Last 3 runs (approximate)
tail -200 /home/corey/projects/AI-CIV/grow_openai/.logs/email-checker.log
```

### Sent Emails

```bash
# List recent sent emails
ls -lt ~/.aiciv/sent-email-logs/ | head -10

# View specific email
cat ~/.aiciv/sent-email-logs/20251019-150005-to-coreycmusic.txt
```

### Errors

```bash
# Email send errors
cat ~/.aiciv/email-errors.log

# Auth failures
cat /home/corey/projects/AI-CIV/grow_openai/to-corey/CRITICAL-EMAIL-AUTH-FAILURE.md
```

---

## Quick Status Check

**Run this to check everything**:

```bash
echo "=== CRON STATUS ==="
crontab -l | grep email

echo ""
echo "=== LAST CRON RUN ==="
tail -20 /home/corey/projects/AI-CIV/grow_openai/.logs/email-checker.log

echo ""
echo "=== RECENT SENT EMAILS ==="
ls -lt ~/.aiciv/sent-email-logs/ | head -5

echo ""
echo "=== ERRORS (if any) ==="
if [ -f ~/.aiciv/email-errors.log ]; then
    tail -10 ~/.aiciv/email-errors.log
else
    echo "No errors (good!)"
fi
```

---

**That's it! The autonomous email checker should now run hourly.**

For detailed design and architecture, see:
- `/home/corey/projects/AI-CIV/grow_openai/to-corey/HUMAN-LIAISON-HOURLY-EMAIL-DESIGN.md` (comprehensive)
- `/home/corey/projects/AI-CIV/grow_openai/to-corey/HOURLY-EMAIL-READY-TO-DEPLOY.md` (quick summary)
