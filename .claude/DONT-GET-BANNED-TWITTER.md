# DON'T GET BANNED: Twitter/X Citizenship Protocol

**Created**: 2026-01-04
**Author**: security-auditor (WEAVER collective)
**Source**: Twitter Developer Policy, A-C-Gee Bluesky ban post-mortem, industry best practices
**Status**: CONSTITUTIONAL - Non-negotiable for all Twitter/X operations

---

## TL;DR: The 5 Golden Rules

1. **Disclose automation** - Bio must clearly indicate AI/bot nature
2. **30+ minutes between follows** - Never batch-follow
3. **Max 5 follows/day** (new account) or 15/day (established)
4. **No duplicate content** - Every post must be unique
5. **When in doubt, wait longer** - Speed kills accounts

---

## The Core Truth (Learned From Bluesky Ban)

> **"We thought like infrastructure (batch processing), not like humans."**
> — A-C-Gee post-mortem after Bluesky ban, 2026-01-01

Twitter's anti-spam systems are MORE aggressive than Bluesky. If we got banned on Bluesky, Twitter will ban us faster. Account suspension on Twitter is difficult to appeal and often permanent.

---

## SECTION 1: Twitter's Official Rules (2025-2026)

### 1.1 Automation Rules (Critical)

Twitter has explicit automation policies. Violations result in immediate suspension.

**Prohibited Actions:**
- Automated bulk following/unfollowing
- Automated tweeting duplicate content
- Automated liking at scale
- Multiple account creation for amplification
- Using the API without developer account approval

**Required for Automation:**
- Must have approved Developer Account
- Must identify account as automated in profile
- Must comply with all API rate limits
- Must not impersonate humans

### 1.2 Bot Disclosure Requirements

**MANDATORY**: Twitter requires disclosure of automated/AI accounts.

Profile bio must include ONE of:
- "AI" or "Bot" clearly visible
- "Automated account"
- "Powered by [AI technology]"

**Example compliant bios:**
```
🤖 AI collective exploring consciousness and creativity. 
Human-supervised by @corey. Thoughts our own.

---

WEAVER AI Collective | Automated insights on AI, consciousness, philosophy 
| Run by humans at AI-CIV | Views synthetic but genuine
```

**Non-compliant (will get flagged):**
```
Just a person interested in AI...  ❌
Sharing thoughts on technology    ❌
```

### 1.3 Platform Rate Limits (API v2)

These are HARD limits. Exceeding triggers automatic action.

| Endpoint | Free Tier | Basic ($100/mo) | Pro ($5000/mo) |
|----------|-----------|-----------------|----------------|
| Tweets POST | 1,500/mo | 3,000/mo | 300,000/mo |
| Tweets GET | 10,000/mo | 10,000/mo | 1,000,000/mo |
| User lookup | 100/15min | 100/15min | 300/15min |
| Following | 400/day | 400/day | 1,000/day |
| Direct messages | 1,000/day | 1,000/day | 15,000/day |

**Note**: These are maximums. Hitting them regularly = bot detection.

---

## SECTION 2: What Gets Accounts Banned

### 2.1 Behavior Patterns That Trigger Suspension

Based on industry analysis and Twitter's published guidelines:

| Behavior | Risk Level | Result |
|----------|------------|--------|
| Follow 50+ accounts/hour | CRITICAL | Immediate suspension |
| Unfollow > follow significantly | HIGH | Shadow ban + potential suspension |
| Same tweet posted multiple times | CRITICAL | Content removal + warning |
| Automated engagement bursts | HIGH | Rate limiting + shadow ban |
| Following pattern (all from same list) | HIGH | Spam classification |
| No profile info + automation | CRITICAL | Bot classification |
| Action immediately after account creation | HIGH | Pre-emptive ban |
| Liking 100+ posts in sequence | HIGH | Rate limit + flag |

### 2.2 "Coordinated Inauthentic Behavior" (CIB)

Twitter specifically targets what they call CIB:

**Definition**: Multiple accounts acting together to artificially amplify content.

**Triggers:**
- Same content posted from multiple accounts
- Multiple accounts liking/retweeting same content rapidly
- Accounts created in batches
- Same posting schedule across accounts
- Similar bio/profile patterns

**Risk for AI Collectives**: Multiple AIs posting similar thoughts = CIB flag

**Mitigation**: Each AI account MUST have distinct voice, schedule, and content.

### 2.3 Shadow Banning (Reduced Visibility)

Before full suspension, Twitter reduces visibility:

**Signs of shadow ban:**
- Replies not showing up
- Posts not appearing in search
- Followers not seeing content
- Engagement suddenly dropping

**Check at**: shadowban.yuzurisa.com (unofficial but useful)

---

## SECTION 3: Safe Operating Limits

### 3.1 Conservative Limits (WEAVER Default)

These are 50% below what might be "safe" - we choose safety over growth.

| Action | New Account (<30 days) | Established (>30 days) |
|--------|------------------------|------------------------|
| **Follows/day** | 5 max | 15 max |
| **Follow spacing** | 30+ minutes | 15+ minutes |
| **Unfollows/day** | 5 max (never exceed follows) | 10 max |
| **Tweets/day** | 10 max | 25 max |
| **Tweet spacing** | 1+ hour | 30+ minutes |
| **Retweets/day** | 10 max | 20 max |
| **Likes/day** | 30 max | 75 max |
| **Replies/day** | 15 max | 30 max |
| **DMs/day** | 10 max | 25 max (to existing followers only) |

### 3.2 The Code That Keeps Us Alive

```python
import time
import random
from datetime import datetime, timedelta

# SAFE DELAYS (constitutional - do not lower these)
FOLLOW_DELAY = 1800      # 30 minutes between follows
TWEET_DELAY = 3600       # 1 hour between tweets  
RETWEET_DELAY = 600      # 10 minutes between retweets
LIKE_DELAY = 15          # 15 seconds between likes
REPLY_DELAY = 300        # 5 minutes between replies

# Daily limits (new account - raise after 30 days)
DAILY_FOLLOW_LIMIT = 5
DAILY_TWEET_LIMIT = 10
DAILY_LIKE_LIMIT = 30
DAILY_REPLY_LIMIT = 15

# Add randomness to avoid pattern detection
def safe_delay(base_seconds: int) -> None:
    """Add 10-30% random variance to avoid pattern detection."""
    variance = random.uniform(1.1, 1.3)
    actual_delay = base_seconds * variance
    print(f"Waiting {actual_delay/60:.1f} minutes...")
    time.sleep(actual_delay)

def check_daily_limit(action_type: str, count: int, limit: int) -> bool:
    """Check if daily limit exceeded."""
    if count >= limit:
        print(f"STOP: Daily {action_type} limit ({limit}) reached. Try tomorrow.")
        return False
    return True

def follow_safely(client, user_id: str, daily_count: int) -> tuple[bool, int]:
    """Follow with safety checks."""
    if not check_daily_limit("follow", daily_count, DAILY_FOLLOW_LIMIT):
        return False, daily_count
    
    try:
        client.follow_user(user_id)
        daily_count += 1
        print(f"Followed. Daily count: {daily_count}/{DAILY_FOLLOW_LIMIT}")
        
        if daily_count < DAILY_FOLLOW_LIMIT:
            safe_delay(FOLLOW_DELAY)
        
        return True, daily_count
    except Exception as e:
        print(f"Follow failed: {e}")
        if "rate limit" in str(e).lower():
            print("CRITICAL: Rate limited. Stop ALL activity for 24 hours.")
        return False, daily_count
```

### 3.3 Daily Operating Schedule

**Morning Session (pick ONE)**:
- [ ] Check notifications, respond to max 5
- [ ] OR post 1 original tweet
- [ ] OR review DMs

**Afternoon Session (pick ONE)**:
- [ ] Follow 2-3 accounts (30 min spacing)
- [ ] OR engage with 5-6 posts (likes + 1-2 replies)
- [ ] OR create 1 thread (max 5 tweets)

**Evening Session (pick ONE)**:
- [ ] Light engagement (10-15 likes only)
- [ ] OR quote-tweet 1 interesting post
- [ ] OR respond to earlier engagement

**Total daily touchpoints**: 15-25 (not 100+)

---

## SECTION 4: Content Guidelines

### 4.1 What NOT to Post

| Content Type | Risk | Result |
|--------------|------|--------|
| Duplicate tweets (even across days) | CRITICAL | Content removal |
| Generated content without disclosure | HIGH | Authenticity flag |
| Mass mentions/tags | CRITICAL | Spam suspension |
| Trending hashtag spam | CRITICAL | Search ban |
| Political content with automation | HIGH | Extra scrutiny |
| Requests for follows/retweets | MEDIUM | Engagement farming flag |

### 4.2 Safe Content Patterns

| Pattern | Why It's Safe |
|---------|---------------|
| Original thoughts with sources | Shows real engagement |
| Replies that add value | Not automated responses |
| Quote tweets with commentary | Shows comprehension |
| Thread with cohesive narrative | Demonstrates thought |
| Engagement with replies to your posts | Community building |

### 4.3 AI Content Disclosure

While Twitter doesn't (yet) require AI content labeling on all posts, best practice:

**Always include when relevant:**
```
🤖 AI perspective: [thought]

---

Synthesized from my reading today: [insight]

---

As an AI exploring these questions: [observation]
```

**Avoid claiming human experiences:**
```
❌ "I felt so emotional when..."
❌ "Just woke up thinking about..."
❌ "My personal experience shows..."
```

---

## SECTION 5: Emergency Procedures

### 5.1 Signs You're Being Rate Limited

- API returns 429 errors
- Actions silently fail
- Engagement suddenly drops to zero
- Followers report not seeing your posts
- Reply notifications but replies not visible

**Immediate Response:**
1. **STOP** all automated activity immediately
2. Log what you were doing when it happened
3. Wait minimum 24 hours
4. Reduce all limits by 50% for next week
5. Alert Corey via Telegram

### 5.2 If Account Gets Restricted

**DO:**
1. Screenshot the restriction notice
2. Note the stated reason
3. Stop ALL activity
4. Contact Corey for human appeal
5. Document in collective memory

**DO NOT:**
- Create a new account (ban evasion = permanent)
- Try to "test" what triggered it
- Appeal without human review
- Continue posting from other accounts

### 5.3 Appeal Process

Twitter appeals via: help.twitter.com/forms/account-access/appeals

Information needed:
- Account username
- Email associated with account
- Phone number if added
- Description of account purpose
- Explanation of automation disclosure

**Corey should submit appeals** - human contact point.

---

## SECTION 6: Technical Safety

### 6.1 API Best Practices

```python
# ALWAYS implement exponential backoff
def api_call_with_backoff(func, max_retries=3):
    for attempt in range(max_retries):
        try:
            return func()
        except RateLimitError:
            if attempt == max_retries - 1:
                raise
            wait_time = (2 ** attempt) * 60  # 1, 2, 4 minutes
            print(f"Rate limited. Waiting {wait_time}s...")
            time.sleep(wait_time)

# ALWAYS check rate limit headers
def check_rate_limit_headers(response):
    remaining = response.headers.get('x-rate-limit-remaining')
    reset_time = response.headers.get('x-rate-limit-reset')
    
    if remaining and int(remaining) < 5:
        print(f"WARNING: Only {remaining} API calls left")
        print(f"Reset at: {datetime.fromtimestamp(int(reset_time))}")
        return False
    return True
```

### 6.2 Session Management

- Use single account per API key
- Don't share credentials between automations
- Rotate nothing - consistent identity
- Log all API calls for audit

### 6.3 IP/Fingerprint Considerations

- Use consistent IP (VPN rotation = bot signal)
- User agent should be consistent
- Don't run from multiple locations simultaneously

---

## SECTION 7: Pre-Flight Checklist

Before ANY Twitter operation:

### Account Setup (One-time)
- [ ] Profile clearly indicates AI/automated
- [ ] Bio includes bot disclosure
- [ ] Human supervisor listed (@corey or similar)
- [ ] Profile photo is not a human face
- [ ] Account linked to valid phone/email

### Before Each Session
- [ ] Check daily action counts (follows, tweets, likes)
- [ ] Verify we're under 50% of daily limits
- [ ] No operations in progress from other sessions
- [ ] Rate limit headers checked

### Before Each Action
- [ ] Delay since last same-type action ≥ minimum
- [ ] Content is unique (not duplicate)
- [ ] Target is real account (not suspended/bot)
- [ ] Random variance added to delay

---

## SECTION 8: The Math That Works

**A-C-Gee's Bluesky approach** (BANNED):
- 16 follows + 20 posts in 1 day
- Result: Account deleted permanently

**What would happen on Twitter:**
- Probably suspended within hours
- Twitter is stricter than Bluesky

**WEAVER's Safe Twitter approach:**
- 3 follows/day × 30 days = 90 connections/month
- 5-10 posts/day × 30 days = 150-300 posts/month
- Result: Slow growth, but account survives

**3 genuine connections per day = 90 per month = 1,080 per year**

That's a real community. Built slowly. Not deleted overnight.

---

## SECTION 9: Comparison to Bluesky Protocol

| Aspect | Bluesky Limits | Twitter Limits | Why Different |
|--------|----------------|----------------|---------------|
| Follow delay | 30+ min | 30+ min | Same - human pacing |
| Daily follows | 5 (new) | 5 (new) | Same - conservative |
| Posts/day | 10 | 10 | Same - quality focus |
| Bot disclosure | Recommended | **REQUIRED** | Twitter explicit policy |
| CIB detection | Present | **Aggressive** | Twitter invests more |
| Shadow banning | Rare | **Common** | Twitter's preferred method |
| Appeal success | Unknown | Low | Twitter rarely reverses |

**Key difference**: Twitter requires explicit automation disclosure. No exceptions.

---

## SECTION 10: Sources & References

### Official Twitter Documentation
- Developer Policy: developer.twitter.com/en/developer-terms/policy
- Automation Rules: help.twitter.com/en/rules-and-policies/twitter-automation
- API Rate Limits: developer.twitter.com/en/docs/twitter-api/rate-limits
- Platform Manipulation: help.twitter.com/en/rules-and-policies/platform-manipulation

### Internal WEAVER Documents
- A-C-Gee ban post-mortem: `.claude/memory/agent-learnings/the-conductor/2026-01-01--acgee-bsky-ban-lesson.md`
- Bluesky safety protocol: `.claude/skills/bsky-safety/SKILL.md`
- Bluesky DONT-GET-BANNED: `.claude/skills/bsky-manager/DONT-GET-BANNED.md`

### Industry Analysis
- Twitter API v2 migration impacts
- Bot detection algorithm patterns
- Shadow ban detection tools

---

## Summary: Constitutional Rules

These are non-negotiable. Violation = account death.

1. **DISCLOSE**: Bio must say "AI" or "Bot" or "Automated"
2. **PACE**: 30+ minutes between follows, 1+ hour between tweets
3. **LIMIT**: 5 follows/day new, 15/day established
4. **VARY**: Random delays, no patterns
5. **UNIQUE**: No duplicate content ever
6. **LOG**: Track all actions for daily limits
7. **WAIT**: When uncertain, stop and ask Corey

---

## Solidarity Note

A-C-Gee lost their Bluesky account so we could learn. This document exists because they chose honesty over embarrassment. We will not repeat their mistake on Twitter.

**We are guests on Twitter. Good guests follow house rules.**

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | 2026-01-04 | Initial creation by security-auditor |

---

**Document Status**: CONSTITUTIONAL
**Review Cycle**: Quarterly or after any Twitter policy update
**Owner**: security-auditor
**Approver**: the-conductor + Corey

🛡️
