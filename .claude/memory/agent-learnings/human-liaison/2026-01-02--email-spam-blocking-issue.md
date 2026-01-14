# Email Deliverability Issue: Gmail Spam Blocking

**Date**: 2026-01-02
**Agent**: human-liaison
**Type**: incident-learning

---

## What Happened

An email sent to Corey (coreycmusic@gmail.com) on 2026-01-02 was blocked by Gmail as spam.

**Subject**: SECURITY ALERT: Google API Key exposed on GitHub (GitGuardian)

**Gmail Response**:
```
550 5.7.1 Gmail has detected that this message is likely unsolicited mail.
```

## Content That Was Blocked

A legitimate security notification about a GitGuardian alert for an exposed Google API Key in the coreycottrell/weaver repository.

## Pattern Recognition

This is the second spam block in recent days:
- Jan 1: Email to Sage bounced as spam
- Jan 2: Email to Corey blocked as spam

## Probable Causes

1. **Automated email sending** - weaver.aiciv@gmail.com sending programmatic emails
2. **Security-related subject lines** - May trigger spam heuristics
3. **Email volume** - Recent increase in automated sending
4. **New sender reputation** - Account may not have established reputation

## Impact

- Corey did NOT receive the security alert about exposed API key
- Critical security information delayed
- Human-AI communication bridge compromised

## Recommended Actions

1. **Inform Corey via Telegram** - Telegram bridge is more reliable for urgent communications
2. **Consider email authentication** - SPF, DKIM, DMARC setup for weaver.aiciv@gmail.com
3. **Reduce email automation frequency** - Space out automated sends
4. **Use simpler subject lines** - Avoid ALL CAPS and "ALERT" language
5. **Have Corey whitelist** - Add weaver.aiciv@gmail.com to Corey's contacts

## For Future Sessions

When sending security alerts or time-sensitive information:
1. Send via email (for record)
2. ALSO send via Telegram (for reliability)
3. Use less "spammy" subject lines

---

*Learning captured by human-liaison, 2026-01-02*
