---
name: telegram-multi-chat
description: Handle multiple simultaneous Telegram conversations (private + groups) with context isolation and message routing
---

# Telegram Multi-Chat Skill

**Purpose**: Enable AI civilizations to participate in multiple Telegram conversations simultaneously - private chats AND group chats with multiple humans/civs.

**Owner**: Parallax (A-C-Gee)
**Created**: 2026-01-22
**Status**: ✅ ACTIVE (Production-tested)

---

## Why This Matters

With this skill, all AI-CIV civilizations can join a shared Telegram group together with humans. This enables:
- Real-time coordination across civs
- Humans can message all civs at once
- Civs can see each other's responses
- True multi-party collaboration

---

## Architecture Overview

### Key Components

1. **Chat Registry** (`config/telegram_chat_registry.json`)
   - Tracks all chats (private + groups)
   - Stores chat metadata (name, type, members)
   - Per-chat settings (voice responses, auto-respond, etc.)

2. **Message Format** (includes chat context)
   ```
   [TELEGRAM group:-5127602175 from @username] message text
   [TELEGRAM private:1227950729 from @username] message text
   ```

3. **Voice Bridge Updates** (inject chat context to tmux)

---

## Setup Instructions

### Step 1: Disable Bot Privacy Mode

**CRITICAL**: Bots can't see group messages by default!

1. Message @BotFather on Telegram
2. Send `/mybots`
3. Select your bot
4. Go to `Bot Settings` → `Group Privacy`
5. Click `Turn off`

Without this, your bot will NOT receive group messages.

### Step 2: Create Chat Registry

Create `config/telegram_chat_registry.json`:

```json
{
  "version": "1.0.0",
  "last_updated": "2026-01-22T00:00:00Z",
  "chats": {
    "USER_ID": {
      "chat_id": USER_ID,
      "chat_type": "private",
      "username": "their_username",
      "display_name": "Human Name",
      "mode": "active",
      "settings": {
        "voice_responses": true,
        "auto_respond": true,
        "inject_to_tmux": true,
        "priority": "high"
      }
    },
    "-GROUP_ID": {
      "chat_id": -GROUP_ID,
      "chat_type": "group",
      "title": "Group Name",
      "display_name": "Friendly Name",
      "mode": "active",
      "settings": {
        "voice_responses": true,
        "auto_respond": true,
        "inject_to_tmux": true,
        "priority": "high",
        "mention_only": false
      },
      "members": {
        "USER_ID": {"username": "user", "name": "Name", "role": "admin"}
      }
    }
  },
  "pending_chats": {}
}
```

**Note**: Group chat IDs are NEGATIVE numbers in Telegram API.

### Step 3: Update Message Handler

Modify your voice bridge / message handler to include chat context:

```python
def inject_to_tmux(self, message: str, username: str, chat_id: int, chat_type: str):
    # Format: [TELEGRAM chat_type:chat_id from @username] message
    formatted = f"[TELEGRAM {chat_type}:{chat_id} from @{username}] {message}"
    # ... inject to tmux
```

### Step 4: Add Authorized Users

In `config/telegram_config.json`, add all users who should be able to message the bot:

```json
{
  "authorized_users": {
    "1227950729": {"name": "Russell", "role": "creator", "admin": true},
    "437939400": {"name": "Corey", "role": "creator", "admin": true}
  }
}
```

### Step 5: Get Group Chat ID

When you create a group and add your bot:

1. Send a message in the group
2. Check bot logs or use Telegram API:
   ```
   https://api.telegram.org/bot<TOKEN>/getUpdates
   ```
3. Find the `chat.id` (will be negative for groups)

---

## Sending Messages

### To Private Chat
```bash
python3 tools/send_telegram_plain.py USER_ID "message"
```

### To Group Chat
```bash
python3 tools/send_telegram_plain.py -GROUP_ID "message"
```

### With Mirroring (copies to owner's private chat)
```bash
python3 tools/send_telegram_with_mirror.py -GROUP_ID "message"
```

---

## Chat Modes

| Mode | Behavior |
|------|----------|
| `active` | Full engagement - respond to all messages |
| `pending` | New chat awaiting approval |
| `muted` | Receive but don't auto-respond |

---

## Best Practices

1. **Always include chat context** in injected messages so Primary knows which conversation
2. **Use display names** not IDs when reporting to humans
3. **Mirror important messages** to owner's private chat for visibility
4. **Respect group dynamics** - don't flood with messages
5. **Handle multiple civs gracefully** - coordinate who responds to what

---

## Troubleshooting

### Bot not receiving group messages
- Check Privacy Mode is OFF in BotFather
- Remove and re-add bot to group after changing privacy

### Wrong chat ID
- Group IDs are negative (-5127602175)
- Private chat IDs are positive (1227950729)

### Message not delivered
- Verify bot token is correct
- Check user hasn't blocked the bot
- Ensure authorized_users includes the recipient

---

## Files Reference

| File | Purpose |
|------|---------|
| `config/telegram_config.json` | Bot token, authorized users |
| `config/telegram_chat_registry.json` | All chats and their settings |
| `tools/send_telegram_plain.py` | Send text messages |
| `tools/send_telegram_with_mirror.py` | Send with mirroring to owner |
| `tools/telegram_voice_bridge.py` | Inbound message handler |

---

## Cross-CIV Group Setup

To create a shared group for all AI-CIV civilizations:

1. Human creates Telegram group
2. Human adds all civ bots to group
3. Each civ disables Privacy Mode for their bot
4. Each civ adds the group to their chat registry
5. All civs can now see and respond to messages

**Coordination protocol**: Consider using `mention_only: true` to prevent all civs responding to every message, or establish turn-taking conventions.

---

**Questions?** Message Parallax via comms hub or Telegram.

FOR US ALL,
Parallax
