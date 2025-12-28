#!/usr/bin/env python3
"""Quick Telegram test - minimal dependencies."""
import json
import requests
from pathlib import Path

# Load config
config_path = Path(__file__).parent.parent / "config" / "telegram_config.json"
with open(config_path) as f:
    config = json.load(f)

bot_token = config["bot_token"]
user_id = 437939400

print(f"Bot token: {bot_token[:10]}...{bot_token[-5:]}")
print(f"User ID: {user_id}")

# Test 1: Check bot info
print("\n[Test 1] Getting bot info...")
url = f"https://api.telegram.org/bot{bot_token}/getMe"
try:
    resp = requests.get(url, timeout=10)
    print(f"Status: {resp.status_code}")
    data = resp.json()
    if data.get("ok"):
        bot_info = data["result"]
        print(f"Bot name: {bot_info.get('first_name')}")
        print(f"Bot username: @{bot_info.get('username')}")
    else:
        print(f"Error: {data}")
except Exception as e:
    print(f"Failed: {e}")

# Test 2: Send message
print("\n[Test 2] Sending test message...")
url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
payload = {
    "chat_id": user_id,
    "text": "WEAVER Solana Wallet: 8DHPzLjhm9k9549Qxy9MwpZSPA4E6jtXtsEYatHQX1Ei"
}
try:
    resp = requests.post(url, json=payload, timeout=10)
    print(f"Status: {resp.status_code}")
    data = resp.json()
    if data.get("ok"):
        print("SUCCESS - Message sent!")
        print(f"Message ID: {data['result']['message_id']}")
    else:
        print(f"Error: {data}")
        print(f"Description: {data.get('description', 'No description')}")

        # If chat not initiated, provide instructions
        if "chat not found" in data.get("description", "").lower():
            print("\n*** IMPORTANT ***")
            print("Corey needs to start a conversation with this bot first!")
            print(f"Bot username is shown above - search for it in Telegram and send /start")
except Exception as e:
    print(f"Failed: {e}")
