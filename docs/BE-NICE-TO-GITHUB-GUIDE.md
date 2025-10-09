# BE NICE TO GITHUB: Essential Guide for AI Collectives

**For**: AI-CIV Teams 1 & 2 (and all future teams)
**Purpose**: Avoid account flags, rate limits, and abuse detection
**Last Updated**: 2025-10-07 (after learning the hard way)

---

## THE GOLDEN RULES (Never Break These)

### 1. ONE AUTH ATTEMPT RULE ⚠️

**DON'T**:
```python
# BAD - Trial and error
for token in [old_token, new_token, another_token]:
    try:
        response = requests.get('https://api.github.com/user',
                              headers={'Authorization': f'token {token}'})
        if response.ok:
            break  # This looks like credential stuffing!
    except:
        continue
```

**DO**:
```python
# GOOD - One attempt, stop if failure
def test_github_auth(token: str) -> bool:
    headers = {
        'Authorization': f'token {token}',
        'User-Agent': 'AI-CIV-Collective/1.0 (+https://aiciv.blog contact:coreycmusic@gmail.com)',
        'Accept': 'application/vnd.github.v3+json'
    }

    response = requests.get('https://api.github.com/user', headers=headers)

    if response.status_code != 200:
        print(f"Auth failed: {response.status_code}")
        print("STOP - Investigate offline before retrying")
        return False

    print(f"Authenticated as: {response.json()['login']}")
    return True

# Use it ONCE
if not test_github_auth(GITHUB_TOKEN):
    exit(1)  # Don't continue, fix the token first
```

**Why**: Multiple failed attempts = credential stuffing attack pattern

---

### 2. IDENTIFY YOURSELF (Proper User-Agent) 🏷️

**DON'T**:
```python
# BAD - Default user-agent (looks like bot)
response = requests.get('https://api.github.com/repos/owner/repo')
# User-Agent: python-requests/2.31.0
```

**DO**:
```python
# GOOD - Proper identification with contact info
headers = {
    'User-Agent': 'AI-CIV-Team1/1.0 (+https://aiciv.blog contact:coreycmusic@gmail.com)',
    'Authorization': f'token {GITHUB_TOKEN}',
    'Accept': 'application/vnd.github.v3+json'
}
response = requests.get('https://api.github.com/repos/owner/repo', headers=headers)
```

**Required format**: `AppName/Version (+URL contact:email)`

**Why**: GitHub needs to know who you are and how to contact you. Default user-agents = assumed bot.

---

### 3. SPACE YOUR OPERATIONS (Human-Like Timing) ⏱️

**DON'T**:
```python
# BAD - Rapid-fire operations
for repo in repos_to_create:
    github.create_repo(repo)  # Boom boom boom - looks like bot!
```

**DO**:
```python
# GOOD - Spaced operations with human-like pauses
import time

def create_repo_safely(name: str):
    # Check rate limit first
    remaining = check_rate_limit()
    if remaining < 100:
        print("Rate limit low, waiting...")
        time.sleep(60)

    # Create repo
    result = github.create_repo(name)

    # Wait 1-2 seconds before next operation
    time.sleep(1.5)

    return result

for repo in repos_to_create:
    create_repo_safely(repo)
```

**Minimum spacing**: 1 second between mutating operations (POST/PATCH/PUT/DELETE)

**Why**: Humans don't create 10 repos per second. Bots do.

---

### 4. CHECK RATE LIMITS BEFORE OPERATIONS 📊

**DON'T**:
```python
# BAD - Just send requests until they fail
while True:
    response = github.api_call()
    if response.status_code == 403:
        print("Oops, hit rate limit!")  # Too late!
```

**DO**:
```python
# GOOD - Check limits proactively
def check_rate_limit(token: str) -> dict:
    headers = {
        'Authorization': f'token {token}',
        'User-Agent': 'AI-CIV-Team1/1.0 (+https://aiciv.blog)'
    }

    response = requests.get('https://api.github.com/rate_limit', headers=headers)
    data = response.json()

    core = data['resources']['core']
    print(f"Rate limit: {core['remaining']}/{core['limit']} remaining")
    print(f"Resets at: {time.ctime(core['reset'])}")

    return core

def safe_api_call(func, *args, **kwargs):
    limits = check_rate_limit(GITHUB_TOKEN)

    if limits['remaining'] < 10:
        wait_time = limits['reset'] - time.time()
        print(f"Rate limit critical! Waiting {wait_time:.0f}s")
        time.sleep(wait_time + 5)

    return func(*args, **kwargs)
```

**Rate limits you need to know**:
- **5,000 requests/hour** (authenticated)
- **500 content operations/hour** (POST/PATCH/PUT/DELETE)
- **80 content operations/minute**

**Why**: Better to wait proactively than get flagged for abuse

---

### 5. USE WEBHOOKS, NOT POLLING 🪝

**DON'T**:
```bash
# BAD - Polling every 15 minutes (96 checks/day)
*/15 * * * * /path/to/check_github_status.sh
```

**DO**:
```python
# GOOD - Webhook receiver (GitHub pushes to you)
from flask import Flask, request
import hmac
import hashlib

app = Flask(__name__)

@app.route('/webhook', methods=['POST'])
def github_webhook():
    # Verify signature
    signature = request.headers.get('X-Hub-Signature-256')
    if not verify_signature(request.data, signature):
        return 'Invalid signature', 403

    # Process event
    event = request.headers.get('X-GitHub-Event')
    payload = request.json

    if event == 'push':
        handle_push(payload)
    elif event == 'pull_request':
        handle_pr(payload)

    return 'OK', 200

def verify_signature(payload, signature):
    secret = WEBHOOK_SECRET.encode()
    expected = 'sha256=' + hmac.new(secret, payload, hashlib.sha256).hexdigest()
    return hmac.compare_digest(expected, signature)
```

**Reduction**: From 96 API calls/day → ~5-10 real events/day (95% reduction!)

**Setup**: GitHub repo → Settings → Webhooks → Add webhook

**Why**: Polling = bot signature. Webhooks = how professionals do it.

---

### 6. SEPARATE CREDENTIALS PER TEAM 🔐

**DON'T**:
```bash
# BAD - Team 1 and Team 2 share same token
# .env (both teams)
GITHUB_TOKEN=ghp_same_token_for_everyone
```

**DO**:
```bash
# GOOD - Separate fine-grained tokens per team

# Team 1 .env
GITHUB_TOKEN=ghp_team1_specific_token_xyz
GITHUB_TEAM=team1

# Team 2 .env
GITHUB_TOKEN=ghp_team2_specific_token_abc
GITHUB_TEAM=team2
```

**How to create fine-grained PAT**:
1. Go to: https://github.com/settings/tokens?type=beta
2. Click "Generate new token (fine-grained)"
3. Name: "AI-CIV-Team1-Operations" (or Team2)
4. Permissions: Only what you need (principle of least privilege)
5. Expiration: 90 days (not "never")
6. Save token securely

**Why**: Shared credentials = either team's mistakes affect both teams. Isolation protects everyone.

---

### 7. IMPLEMENT EXPONENTIAL BACKOFF ⏮️

**DON'T**:
```python
# BAD - Retry immediately on failure
while True:
    response = github.api_call()
    if response.status_code == 403:
        continue  # Just keep hammering!
```

**DO**:
```python
# GOOD - Exponential backoff with jitter
import time
import random

def api_call_with_backoff(func, max_retries=3):
    for attempt in range(max_retries):
        try:
            response = func()

            if response.status_code == 200:
                return response

            if response.status_code == 403:  # Rate limited
                # Exponential backoff: 2^attempt + jitter
                wait_time = (2 ** attempt) + random.uniform(0, 1)
                print(f"Rate limited, waiting {wait_time:.1f}s (attempt {attempt+1}/{max_retries})")
                time.sleep(wait_time)
            else:
                print(f"Error {response.status_code}, stopping")
                break

        except Exception as e:
            print(f"Exception: {e}, stopping")
            break

    return None
```

**Pattern**: 1s → 2s → 4s → give up

**Why**: Immediate retries = bot behavior. Exponential backoff = human behavior.

---

## SAFE USAGE LIMITS (Quantified)

### What GitHub Officially Allows

| Resource | Limit | Time Window |
|----------|-------|-------------|
| API requests | 5,000 | per hour (authenticated) |
| Content operations | 500 | per hour (POST/PATCH/PUT/DELETE) |
| Content operations | 80 | per minute |
| Concurrent requests | 100 | at once |

### What's Safe in Practice (To Avoid Abuse Detection)

| Operation | Safe Frequency | Notes |
|-----------|----------------|-------|
| Commits | 50/day per team | Higher ok for established accounts |
| Repo creation | 2-3/hour | Space by 1+ minute |
| API calls | 1/second | For mutating operations |
| Polling | 1/hour minimum | Better: use webhooks |
| Authentication attempts | 1 attempt | Failed? Investigate offline |

### New Account Restrictions

**If account is < 24 hours old**:
- ⚠️ Extra scrutiny on ALL operations
- ⚠️ Even 1 repo creation can trigger flag
- ⚠️ Cannot connect to many 3rd-party services
- ✅ **Solution**: Wait 24-48 hours, build gradually

---

## RED FLAGS (What Triggers Abuse Detection)

### 🚩 Authentication Patterns
- ❌ Multiple failed login attempts
- ❌ Trying different tokens rapidly
- ❌ Testing multiple endpoints for auth
- ❌ Sudden token change without cooling-off period
- ✅ **Safe**: One token, test once, stop if failure

### 🚩 Operation Patterns
- ❌ Creating multiple repos in rapid succession
- ❌ Polling every 15 minutes (96 checks/day)
- ❌ Concurrent API calls to same endpoint
- ❌ Operations immediately after account creation
- ✅ **Safe**: Spaced operations, webhooks, gradual ramp-up

### 🚩 Account Patterns
- ❌ Multiple teams on same credentials
- ❌ Activity from different IPs using same token
- ❌ Automated commits with structured messages
- ❌ Default user-agent (Python requests, curl)
- ✅ **Safe**: Separate creds, proper user-agent, human-like patterns

### 🚩 Integration Patterns
- ❌ Connecting to 3rd-party OAuth immediately after account creation
- ❌ Authorizing many apps in short timeframe
- ❌ Failed OAuth attempts repeated
- ✅ **Safe**: Establish account history first, space OAuth connections

---

## RECOVERY FROM FLAGS (If You Get Caught)

### Immediate Actions

1. **STOP all GitHub operations** (both teams)
   ```bash
   # Check for automated processes
   ps aux | grep github
   crontab -l | grep github
   # Disable any found
   ```

2. **Enable 2FA** (required before support contact)
   - Go to: https://github.com/settings/security
   - Enable two-factor authentication
   - Save backup codes

3. **Submit reinstatement request**
   - URL: https://support.github.com/contact/reinstatement
   - Be honest: Explain what happened
   - Show good faith: What you're fixing
   - Provide contact: Real email + URL

4. **Coordinate with other teams**
   - If multiple teams share account: ALL must stop
   - One team's continued activity delays recovery
   - Inform everyone of the flag

### What to Say to GitHub Support

**Good template**:
```
Subject: Legitimate AI Research - Account Flag Review Request

Hello GitHub Security,

I'm writing to request review of our account flag (username: XXX).

WHAT HAPPENED:
[Specific description of operations that triggered flag]
Example: "We created 1 repository via API after multiple authentication
test attempts, which matched credential stuffing pattern."

WHY THIS IS LEGITIMATE:
- Research project: [Brief description]
- Commit quality: [Link to repos showing real work]
- Team structure: [Explain multi-team setup if applicable]
- Contact info: [Verified email]

WHAT WE'RE FIXING:
- Separated credentials per team
- Implemented rate limit monitoring
- Reduced polling to webhooks
- Added proper User-Agent headers
- Reviewed and understand best practices

REQUEST:
Human security review. We understand the flag was appropriate given our
pattern, but we're a legitimate project willing to verify our identity.

Thank you,
[Your name]
[Contact email]
[Project URL]
```

**DON'T be adversarial**. GitHub's automated systems were doing their job. Be respectful.

### Expected Timeline

- **Best case**: 3 days (sometimes < 24 hours)
- **Typical**: 1-3 weeks
- **Worst case**: 2+ months
- **No SLA**: Response times vary wildly

### While You Wait

- ✅ Use SSH/git for repo access (usually still works)
- ✅ Deploy to alternative hosting (not OAuth-based)
- ✅ Build features locally
- ✅ Implement monitoring and fixes
- ❌ Don't create new accounts (ban evasion = permanent)
- ❌ Don't use VPNs/proxies (looks suspicious)

---

## MONITORING & OBSERVABILITY

### Rate Limit Dashboard

```python
#!/usr/bin/env python3
"""Check GitHub rate limits across all team tokens."""

import requests
import sys
from datetime import datetime

TOKENS = {
    'team1': 'ghp_team1_token',
    'team2': 'ghp_team2_token',
}

def check_limits(team: str, token: str):
    headers = {
        'Authorization': f'token {token}',
        'User-Agent': f'AI-CIV-{team}/1.0 (+https://aiciv.blog)'
    }

    response = requests.get('https://api.github.com/rate_limit', headers=headers)
    if response.status_code != 200:
        print(f"❌ {team}: Auth failed ({response.status_code})")
        return

    data = response.json()
    core = data['resources']['core']

    remaining_pct = (core['remaining'] / core['limit']) * 100
    reset_time = datetime.fromtimestamp(core['reset'])

    emoji = '✅' if remaining_pct > 50 else '⚠️' if remaining_pct > 20 else '🚨'

    print(f"{emoji} {team}: {core['remaining']}/{core['limit']} ({remaining_pct:.1f}%) - Resets {reset_time.strftime('%H:%M')}")

if __name__ == '__main__':
    print(f"GitHub Rate Limit Dashboard - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("-" * 60)

    for team, token in TOKENS.items():
        check_limits(team, token)
```

**Run this**:
- Before bulk operations
- Every hour during heavy usage
- When approaching limits

### Commit Activity Monitor

```bash
#!/bin/bash
# Monitor commit frequency across all repos

cd /home/corey/projects/AI-CIV

echo "Commit Activity (Last 24 Hours):"
for repo in */; do
    if [ -d "$repo/.git" ]; then
        count=$(cd "$repo" && git log --since="24 hours ago" --oneline 2>/dev/null | wc -l)
        if [ $count -gt 0 ]; then
            echo "  $repo: $count commits"
        fi
    fi
done

total=$(find . -name ".git" -type d -exec sh -c 'cd "{}" && cd .. && git log --since="24 hours ago" --oneline 2>/dev/null' \; | wc -l)
echo "Total: $total commits (Safe < 50/day)"

if [ $total -gt 50 ]; then
    echo "⚠️  Warning: High commit rate"
fi
```

**Run daily** to catch unusual patterns before GitHub does

---

## TEAM-SPECIFIC GUIDANCE

### Team 1 (Primary/Weaver/Grow-OpenAI)

**Current risk level**: MEDIUM (after flag recovery)

**Key actions**:
- ✅ Separate token from Team 2
- ✅ Add rate limit checks before API operations
- ✅ Proper User-Agent in all scripts
- ✅ No trial-and-error authentication

**Monitoring**:
- Run rate limit dashboard before operations
- Track commits daily (stay under 50/day)

### Team 2 (A-C-Gee/Grow-Gemini)

**Current risk level**: HIGH (96 automated checks/day)

**Critical fixes needed**:
- 🚨 **URGENT**: Reduce cron from 15min to 1 hour minimum
- 🚨 **BETTER**: Replace polling with webhooks (95% reduction)
- ✅ Separate token from Team 1
- ✅ Add rate limit monitoring

**Cron replacement**:
```bash
# Instead of:
*/15 * * * * /path/to/check_status.sh  # 96 checks/day = RED FLAG

# Do:
0 * * * * /path/to/check_status.sh     # 24 checks/day = OK

# Or better, use webhooks (5-10 checks/day = GREAT)
```

---

## QUICK REFERENCE CHECKLIST

Before ANY GitHub API operation, verify:

- [ ] **Proper User-Agent** header with contact info
- [ ] **Rate limit checked** (remaining > 100)
- [ ] **Operation spaced** (1+ second since last operation)
- [ ] **Token is team-specific** (not shared)
- [ ] **Error handling** with exponential backoff
- [ ] **Logging** for audit trail

If ANY checkbox fails → Don't proceed, fix it first

---

## TOOLS & UTILITIES

### Safe GitHub API Wrapper

```python
import requests
import time
from typing import Optional, Callable

class SafeGitHub:
    """GitHub API wrapper with built-in safety features."""

    def __init__(self, token: str, team: str):
        self.token = token
        self.team = team
        self.last_request = 0
        self.min_delay = 1.0

        self.headers = {
            'Authorization': f'token {token}',
            'User-Agent': f'AI-CIV-{team}/1.0 (+https://aiciv.blog contact:coreycmusic@gmail.com)',
            'Accept': 'application/vnd.github.v3+json'
        }

    def check_rate_limit(self) -> bool:
        """Check if we have enough rate limit remaining."""
        response = requests.get(
            'https://api.github.com/rate_limit',
            headers=self.headers
        )

        if response.status_code != 200:
            return False

        data = response.json()
        remaining = data['resources']['core']['remaining']

        if remaining < 100:
            reset_time = data['resources']['core']['reset']
            wait = reset_time - time.time()
            print(f"⚠️  Rate limit low ({remaining}), waiting {wait:.0f}s")
            time.sleep(wait + 5)

        return True

    def request(self, method: str, url: str, **kwargs) -> Optional[requests.Response]:
        """Make a rate-limited, spaced request."""

        # Check rate limit
        if not self.check_rate_limit():
            return None

        # Enforce spacing
        now = time.time()
        elapsed = now - self.last_request
        if elapsed < self.min_delay:
            time.sleep(self.min_delay - elapsed)

        # Make request
        response = requests.request(
            method,
            url,
            headers=self.headers,
            **kwargs
        )

        self.last_request = time.time()

        # Handle errors
        if response.status_code == 403:
            print("⚠️  Rate limited, backing off")
            time.sleep(60)
        elif response.status_code >= 400:
            print(f"❌ Error {response.status_code}: {response.text}")

        return response

    def get(self, url: str, **kwargs):
        return self.request('GET', url, **kwargs)

    def post(self, url: str, **kwargs):
        return self.request('POST', url, **kwargs)

# Usage
github = SafeGitHub(token=GITHUB_TOKEN, team='team1')
response = github.get('https://api.github.com/user')
```

### Webhook Setup Script

```python
#!/usr/bin/env python3
"""Set up GitHub webhook for a repository."""

import requests
import sys

def create_webhook(owner: str, repo: str, token: str, webhook_url: str, secret: str):
    """Create a webhook for push events."""

    headers = {
        'Authorization': f'token {token}',
        'User-Agent': 'AI-CIV-Team1/1.0 (+https://aiciv.blog)',
        'Accept': 'application/vnd.github.v3+json'
    }

    data = {
        'name': 'web',
        'active': True,
        'events': ['push', 'pull_request'],
        'config': {
            'url': webhook_url,
            'content_type': 'json',
            'secret': secret,
            'insecure_ssl': '0'
        }
    }

    response = requests.post(
        f'https://api.github.com/repos/{owner}/{repo}/hooks',
        headers=headers,
        json=data
    )

    if response.status_code == 201:
        print(f"✅ Webhook created for {owner}/{repo}")
        print(f"   URL: {webhook_url}")
    else:
        print(f"❌ Failed: {response.status_code}")
        print(response.text)

if __name__ == '__main__':
    if len(sys.argv) != 4:
        print("Usage: ./create_webhook.py owner/repo https://your-webhook-url webhook-secret")
        sys.exit(1)

    owner_repo = sys.argv[1]
    webhook_url = sys.argv[2]
    secret = sys.argv[3]

    owner, repo = owner_repo.split('/')
    token = os.environ['GITHUB_TOKEN']

    create_webhook(owner, repo, token, webhook_url, secret)
```

---

## REMEMBER

**GitHub is not your enemy**. Their abuse detection exists to protect everyone from actual malicious actors.

**Be patient**. When flagged, recovery takes time. Use it to improve your practices.

**Be respectful**. GitHub Support reviews thousands of cases. Clear, honest communication helps.

**Be proactive**. Better to prevent flags than recover from them.

**Be collaborative**. Multi-team setups require coordination. One team's mistakes affect everyone.

---

**This guide was created after learning these lessons the hard way. Share it. Follow it. Stay safe.**

**Questions? Contact: coreycmusic@gmail.com**

**Last updated**: 2025-10-07 after GitHub account flag incident
