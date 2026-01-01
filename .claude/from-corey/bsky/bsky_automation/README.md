# Bluesky Automation Toolkit

A complete toolkit for automating Bluesky social media activities using the official AT Protocol SDK.

**Updated for 2025** - Uses the latest `atproto` Python SDK with proper session management and rate limiting.

## ⚠️ Important Notes

- **Use responsibly** - Spammy behavior violates Bluesky's Community Guidelines and can result in account suspension
- **Rate limits are real** - The toolkit respects Bluesky's rate limits automatically
- **AI content should be marked** - Always disclose AI-generated content
- **Login limits are strict** - Only 10 logins per day per IP! Use session persistence.

## 🚀 Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure Environment

```bash
cp .env.example .env
```

Edit `.env` with your credentials:
- Get an app password from Bluesky: Settings > App Passwords
- Optionally add OpenAI API key for AI features

### 3. Test Your Setup

```bash
python session_manager.py
```

This will test authentication and show your profile info.

## 📁 Files Included

| File | Description |
|------|-------------|
| `session_manager.py` | **Core** - Handles authentication with session persistence |
| `rate_limiter.py` | **Core** - Manages rate limits to avoid API bans |
| `find_users.py` | Search for users by keyword |
| `follow_users.py` | Follow users from a JSON file |
| `automate_profile.py` | Full profile automation (follow, like, comment) |
| `ai_responder.py` | AI-powered response generation |
| `content_creator.py` | Create posts, threads, and AI-generated content |

## 📖 Usage Examples

### Find Users by Keyword

```bash
# Interactive mode
python find_users.py

# With arguments
python find_users.py "machine learning" --limit 50 --output data

# Output is saved to data/users_machine_learning_TIMESTAMP.json
```

### Follow Users from a File

```bash
# From a JSON file with handles
python follow_users.py data/users_ml.json

# Dry run (see what would happen without actually following)
python follow_users.py data/users_ml.json --dry-run

# With custom delay between follows
python follow_users.py data/users_ml.json --delay 3.0 --max 50
```

### Automate Profile Engagement

```bash
# Follow and like a single user's latest post
python automate_profile.py user.handle.bsky.social

# Process multiple users
python automate_profile.py user1 user2 user3

# From a file, with AI comments
python automate_profile.py -f users.json --comment

# Don't follow, just like posts
python automate_profile.py user.handle --no-follow
```

### Create Content

```bash
# Post a simple text
python content_creator.py post "Hello Bluesky! 👋"

# Post with an image
python content_creator.py post "Check this out!" -i photo.jpg -a "A beautiful sunset"

# Create a thread
python content_creator.py thread "First post" "Second post" "Third post"

# Generate AI thread and post it
python content_creator.py thread --generate "5 tips for productivity" -l 5

# Generate post ideas
python content_creator.py generate "AI trends in 2025" -n 10
```

## 📊 Rate Limits

Bluesky has the following rate limits (as of 2025):

| Limit Type | Amount | Notes |
|------------|--------|-------|
| Hourly points | 5,000 | Create=3, Update=2, Delete=1 |
| Daily points | 35,000 | Resets at midnight UTC |
| Login per IP | 10/day | **Use session persistence!** |
| Login per handle | 30/5min, 300/day | |

The toolkit automatically tracks and respects these limits.

Check your current status:
```bash
python rate_limiter.py
```

## 🔐 Session Management

**Critical**: Bluesky limits logins to 10/day per IP! The toolkit automatically:

1. Saves session tokens to `session.json`
2. Reuses sessions instead of re-authenticating
3. Automatically refreshes expired tokens
4. Only logs in fresh when absolutely necessary

If you're running multiple scripts, they'll all share the same session file.

## 🤖 AI Features

The toolkit supports AI-powered responses using:

- **OpenAI GPT-4** (default) - Set `OPENAI_API_KEY` in `.env`
- **Anthropic Claude** - Set `ANTHROPIC_API_KEY` in `.env`

AI responses are automatically:
- Limited to 250 characters
- Marked with 🤖 indicator
- Contextual to the post content

## 📋 JSON File Formats

### User List (for following)

```json
[
  {"handle": "user1.bsky.social"},
  {"handle": "user2.bsky.social"}
]
```

Or simple string list:
```json
["user1.bsky.social", "user2.bsky.social"]
```

### Search Results

The `find_users.py` script outputs:
```json
[
  {
    "handle": "user.bsky.social",
    "displayName": "Display Name",
    "bio": "User bio",
    "followersCount": 1000,
    "followsCount": 500,
    "postsCount": 200
  }
]
```

## 🛠️ Troubleshooting

### "Rate Limit Exceeded"
- Wait for the limit to reset (check `rate_limiter.py` status)
- The toolkit should handle this automatically

### "Token Expired"
- Delete `session.json` and re-run
- The session manager will create a fresh session

### "Login Failed"
- Check your credentials in `.env`
- Make sure you're using an app password, not your main password
- Check if you've hit the 10 logins/day IP limit

### "AI Response Failed"
- Check your OpenAI/Anthropic API key
- Ensure you have credits/quota available

## 📜 License

MIT License - Use responsibly!

## 🔗 Resources

- [Bluesky API Docs](https://docs.bsky.app)
- [AT Protocol SDK (Python)](https://github.com/MarshalX/atproto)
- [Rate Limits](https://docs.bsky.app/docs/advanced-guides/rate-limits)
- [Community Guidelines](https://bsky.social/about/support/community-guidelines)
