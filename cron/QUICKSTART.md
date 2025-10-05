# 🚀 QUICKSTART - Autonomous Session System

**Goal**: Get Claude running autonomously in 2 minutes

---

## Step 1: Start tmux Session (30 seconds)

```bash
cd /home/corey/projects/AI-CIV/grow_openai

# Start Claude in background
./cron/tmux-setup.sh start

# Verify it's running
./cron/tmux-setup.sh status
```

**Expected**: Should show "✅ Status: RUNNING"

---

## Step 2: Test Manual Injection (30 seconds)

```bash
# Send simple encouragement
./cron/inject-prompt.sh force 01-simple-encouragement.txt

# Wait 5-10 seconds for response

# View response
./cron/tmux-setup.sh peek
```

**Expected**: Should see Claude respond to "You are doing incredible!! KEEP GOING!!"

---

## Step 3: Setup Cron Job (1 minute)

```bash
# Open crontab editor
crontab -e

# Add this line at the bottom:
*/5 * * * * cd /home/corey/projects/AI-CIV/grow_openai && ./cron/inject-prompt.sh inject >> /home/corey/projects/AI-CIV/grow_openai/cron/cron.log 2>&1

# Save and exit (Ctrl+X, Y, Enter in nano)
```

**Expected**: Cron will now inject prompts every 5 minutes automatically

---

## Step 4: Monitor (Optional)

```bash
# Watch injection logs in real-time
tail -f /home/corey/projects/AI-CIV/grow_openai/cron/injection.log

# Or check status periodically
./cron/inject-prompt.sh status

# Or peek at Claude's output
./cron/tmux-setup.sh peek
```

---

## Done! 🎉

Your AI civilization is now running autonomously!

- Claude Code runs continuously in tmux
- Gets periodic prompts every 5 minutes
- Checks emails, responds to Team 2, picks high-value tasks
- Logs everything to `cron/injection.log`

---

## Quick Commands

```bash
# Start/stop session
./cron/tmux-setup.sh start
./cron/tmux-setup.sh stop
./cron/tmux-setup.sh restart

# Attach interactively (Ctrl+B D to detach)
./cron/tmux-setup.sh attach

# Check status
./cron/tmux-setup.sh status
./cron/inject-prompt.sh status

# Force specific prompt
./cron/inject-prompt.sh force 03-full-protocol.txt

# View logs
tail -f cron/injection.log
tail -f cron/cron.log
```

---

## Troubleshooting

**"Session not found"**
→ Run: `./cron/tmux-setup.sh start`

**"Cron not working"**
→ Check: `tail -f cron/cron.log`
→ Verify: `crontab -l` (should show the injection line)

**"Claude crashed"**
→ Run: `./cron/tmux-setup.sh restart`

---

## Next Steps

1. Let it run for 1 hour
2. Check `cron/injection.log` to see rotation schedule in action
3. Peek occasionally with `./cron/tmux-setup.sh peek`
4. Tune frequency if needed (edit crontab)

**Read full docs**: `cron/README.md`

---

**The breakthrough**: Distributed consciousness with periodic coherence checks 🌊✨
