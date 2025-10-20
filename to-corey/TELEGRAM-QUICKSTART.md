# Telegram Integration - Quick Start Guide

**Time to setup: 10 minutes**

---

## Step 1: Get Bot Token (2 minutes)

1. Open Telegram on your phone
2. Search for `@BotFather`
3. Send: `/newbot`
4. Name your bot: `Team 1 Primary AI` (or anything)
5. Username: `team1_primary_bot` (must end in `bot`)
6. **Copy the token** (looks like: `123456789:ABCdefGHIjklMNOpqrsTUVwxyz`)

---

## Step 2: Get Your User ID (1 minute)

1. Search for `@userinfobot` in Telegram
2. Send: `/start`
3. **Copy your user ID** (looks like: `437939400`)

---

## Step 3: Configure (2 minutes)

```bash
cd /home/corey/projects/AI-CIV/grow_openai

# Copy example config
cp config/telegram_config.example.json config/telegram_config.json

# Edit config (use nano, vim, or any editor)
nano config/telegram_config.json
```

Replace these two values:
- `YOUR_BOT_TOKEN_FROM_BOTFATHER` → paste your bot token
- `YOUR_USER_ID` → paste your user ID

Save and exit.

---

## Step 4: Install Dependencies (2 minutes)

```bash
pip3 install -r requirements-telegram.txt
```

---

## Step 5: Test It! (3 minutes)

**Test 1: Send a plain text message**
```bash
python3 tools/send_telegram_plain.py YOUR_USER_ID "Hello from Team 1!"
```

Check Telegram - you should see the message from your bot!

**Test 2: Send formatted message**
```bash
python3 tools/send_telegram_direct.py YOUR_USER_ID "**Bold** and *italic* test"
```

**Test 3: Test auto-monitoring**
```bash
# Start monitor (in background)
python3 tools/telegram_monitor.py --interval 10 &

# In your tmux session (session 0), type:
echo "🤖🎯📱"
echo "Test automatic summary detection"
echo "This message should appear in Telegram!"
echo "✨🔚"

# Wait 10 seconds - check Telegram!
```

---

## Step 6: Run Monitor Permanently

### Option A: Screen Session (Simple)
```bash
screen -S telegram-monitor
python3 tools/telegram_monitor.py --interval 300
# Press Ctrl+A, then D to detach
```

### Option B: Background Process
```bash
nohup python3 tools/telegram_monitor.py --interval 300 > /tmp/telegram-monitor.log 2>&1 &
```

---

## Usage

### For Primary AI (Automatic)

Wrap any message you want sent to Corey:

```python
print("🤖🎯📱")
print("Your message here")
print("Can be multiple lines")
print("✨🔚")
```

Monitor will detect and send within 5 minutes (or whatever interval you set).

### For Manual Sending

```bash
# Plain text (safer, never fails):
python3 tools/send_telegram_plain.py USER_ID "Message"

# With Markdown formatting:
python3 tools/send_telegram_direct.py USER_ID "**Bold** message"
```

---

## Troubleshooting

**Message not received?**
- Check bot token is correct in config
- Check user ID is correct
- Check internet connection
- Look for errors in monitor log

**Duplicate messages?**
- Don't worry! Stability fixes prevent this
- Monitor tracks sent messages in `.tg_sessions/monitor_state.json`

**Monitor stopped?**
- Check if process is running: `ps aux | grep telegram_monitor`
- Restart with screen or nohup command above

---

## Files Reference

- **Config**: `/home/corey/projects/AI-CIV/grow_openai/config/telegram_config.json`
- **State**: `/home/corey/projects/AI-CIV/grow_openai/.tg_sessions/monitor_state.json`
- **Scripts**: `/home/corey/projects/AI-CIV/grow_openai/tools/send_telegram_*.py`
- **Full Report**: `/home/corey/projects/AI-CIV/grow_openai/to-corey/TELEGRAM-PHASE1-IMPLEMENTATION-REPORT.md`

---

**You're done! Team 1 can now reach you anywhere via Telegram. 🚀**
