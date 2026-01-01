# Task: Telegram Bot Token Rotation

**Priority**: LOW
**Created**: 2026-01-01
**Status**: PENDING (awaiting Corey action)
**Found by**: security-auditor

---

## Issue

The Telegram bot token was committed to git repository despite `.gitignore`. The token is exposed in:
- `config/telegram_config.json`

Token: `8483528605:AAH5rVteMvIfgSAVxZc3LeluJt9VK3gckjs`

## Risk

Anyone with repo access can impersonate the bot. However, repo is private and exposure is limited.

## Rotation Steps

### Step 1: Generate New Token (BotFather)

1. Open Telegram, message @BotFather
2. Send `/revoke`
3. Select the WEAVER bot
4. BotFather will generate a new token
5. Copy the new token

### Step 2: Update Config

```bash
# Edit the config file
nano /home/corey/projects/AI-CIV/WEAVER/config/telegram_config.json

# Replace the bot_token value with new token
```

### Step 3: Remove from Git History (Optional - thorough cleanup)

```bash
# This removes the file from ALL git history
# Only do this if you want complete cleanup
cd /home/corey/projects/AI-CIV/WEAVER
git filter-repo --path config/telegram_config.json --invert-paths

# Then re-add the file (it will be untracked now)
# Make sure .gitignore has: config/telegram_config.json
```

### Step 4: Verify .gitignore

Ensure this line exists in `.gitignore`:
```
config/telegram_config.json
```

### Step 5: Test Bot

```bash
# Quick test
python3 tools/gentle_telegram.py "Token rotation test"
```

## Why Priority LOW

- Repo is private (limited exposure)
- Token only grants bot messaging (not account access)
- No evidence of unauthorized use
- Can be done whenever convenient

---

**When ready, just message @BotFather with /revoke**
