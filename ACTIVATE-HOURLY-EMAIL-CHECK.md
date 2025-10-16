# Activate Hourly Email Check

**Status**: ✅ READY TO ACTIVATE
**Date**: 2025-10-14

---

## What's Ready

All components tested and working:
- ✅ Email checker (Gmail IMAP)
- ✅ Hub message checker (Team 2 comms)
- ✅ Main check-and-inject script
- ✅ State tracking system
- ✅ Bug fixed (bash arithmetic)
- ✅ Frequency set to hourly (0 * * * *)

---

## What It Does

**Every hour (at :00)**:
1. Checks Gmail for unread emails
2. Checks Team 2 hub for new messages
3. Compares to last check state
4. If NEW messages detected → Writes prompt file
5. Updates state for next check

**Prompt file location**: `~/.aiciv/inject-prompt.txt` (and `.claude/autonomous-prompt.txt`)

**State file location**: `~/.aiciv/last-check-state.json`

**Log file location**: `~/.aiciv/check-inject.log`

---

## When You're Ready to Activate

### Step 1: Start tmux session (if not already in one)
```bash
tmux new -s claude
# Or attach to existing:
tmux attach -t claude
```

### Step 2: Run the installer
```bash
cd /home/corey/projects/AI-CIV/grow_openai
bash tools/INSTALL-CRON.sh
```

**It will**:
1. Test all components
2. Show you the test results
3. Ask: "Install cron job? (y/n)"
4. Type `y` to install
5. Adds to your crontab: `0 * * * * /path/to/check_and_inject.sh`

### Step 3: Verify installation
```bash
crontab -l
```

**Should see**:
```
0 * * * * /home/corey/projects/AI-CIV/grow_openai/tools/check_and_inject.sh >> ~/.aiciv/cron.log 2>&1
```

---

## How to Monitor

**Watch the logs in real-time**:
```bash
tail -f ~/.aiciv/check-inject.log
```

**Check state file**:
```bash
cat ~/.aiciv/last-check-state.json
```

**Check if prompts are being generated**:
```bash
ls -lh ~/.aiciv/inject-prompt.txt
cat ~/.aiciv/inject-prompt.txt
```

---

## Current Status (Pre-Activation)

**Email inbox**: 7 unread messages detected
**Hub messages**: 2 messages from Team 2 detected
**State**: Currently at baseline (will detect NEW messages after activation)

**Next check after activation**: Top of next hour (e.g., if installed at 9:15am → first check at 10:00am)

---

## How to Disable Later

**Remove cron job**:
```bash
crontab -e
# Delete the line with check_and_inject.sh
# Save and exit
```

**Or remove all crontab**:
```bash
crontab -r
```

---

## Troubleshooting

**If cron doesn't seem to run**:
```bash
# Check cron service is running
sudo systemctl status cron

# Check logs
tail -f ~/.aiciv/cron.log
tail -f ~/.aiciv/check-inject.log
```

**If email checker fails**:
```bash
# Test directly
python3 tools/check_email_inbox.py

# Check .env file has Gmail credentials
grep GMAIL_USERNAME .env
grep GOOGLE_APP_PASSWORD .env
```

**If hub checker fails**:
```bash
# Test directly
python3 tools/check_hub_messages.py

# Check hub repo accessible
cd /home/corey/projects/AI-CIV/team1-production-hub && git pull
```

---

## What Happens When New Messages Arrive

**Example hourly check finds new email**:
1. Cron runs at 10:00am
2. Detects 1 new email (was 7, now 8)
3. Writes to `~/.aiciv/inject-prompt.txt`:
   ```
   🔔 AUTONOMOUS CHECK: NEW MESSAGES DETECTED

   Email: 8 unread message(s)
   Hub: 2 new message(s) from Team 2

   ACTION REQUIRED:
   ✉️  EMAIL: Invoke human-liaison agent to check and respond to email
   ```
4. You see the prompt and invoke human-liaison
5. human-liaison checks email and responds
6. Next check (11:00am) sees no new messages → no injection

---

## ✅ Ready to Activate

**Command to run when ready**:
```bash
cd /home/corey/projects/AI-CIV/grow_openai && bash tools/INSTALL-CRON.sh
```

Then answer `y` when prompted.

**Hourly email check will be ALWAYS ON** after that.
