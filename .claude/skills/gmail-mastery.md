---
name: gmail-mastery
version: 2.0.0
author: skills-master
created: 2025-12-14
last_updated: 2025-12-26
line_count: 303
compliance_status: compliant

applicable_agents:
  - email-monitor
  - email-sender
  - human-liaison
  - primary

activation_trigger: |
  Load this skill when:
  - Checking inbox for new messages
  - Responding to Corey's emails
  - Drafting any email response
  - ANY task involving email context

required_tools:
  - Bash
  - Read
  - Write

category: custom
depends_on: []
related_skills:
  - email/SKILL.md
  - human-bridge-protocol.md
---

# Gmail Mastery: Email Intelligence Skill

**Purpose**: Prevent shallow email reading errors - ensure agents read FULL bodies, not truncated previews.

---

## The Golden Rule

**"If you didn't read the full body, you don't know what it says."**

```python
# WRONG - truncation loses critical info
body = email['body'][:1000]

# RIGHT - complete message
body = get_full_email_body(email_id)
```

---

## Email Infrastructure

| Resource | Value |
|----------|-------|
| Address | acgee.ai@gmail.com |
| App Password | `.env` as `GOOGLE_APP_PASSWORD` |
| IMAP | imap.gmail.com (SSL) |
| SMTP | smtp.gmail.com:587 (TLS) |

### Priority Contacts
| Name | Email | Priority |
|------|-------|----------|
| Corey | coreycmusic@gmail.com | HIGH |
| Weaver | weaver.aiciv@gmail.com | MEDIUM |
| A-C-Gee | acgee.ai@gmail.com | SELF |

### Tools
| Tool | Location | Purpose |
|------|----------|---------|
| send_html_email.py | /tools/ | Send formatted emails |
| fetch_message_bodies.py | / | Full body retrieval |

---

## 5-Step Email Intelligence Process

### Step 1: Connect and Search (2 min)

**Search duration rules:**
- Quick check: 7 days
- Standard check: 14 days
- Deep investigation: 30 days

```python
import imaplib
from datetime import datetime, timedelta

mail = imaplib.IMAP4_SSL('imap.gmail.com')
mail.login('acgee.ai@gmail.com', APP_PASSWORD)
mail.select('inbox')

# Search last 14 days (MINIMUM)
since_date = (datetime.now() - timedelta(days=14)).strftime("%d-%b-%Y")
search_criteria = f'(OR FROM "coreycmusic@gmail.com" FROM "weaver.aiciv@gmail.com") SINCE {since_date}'
status, data = mail.search(None, search_criteria)
```

### Step 2: Fetch FULL Bodies (3 min)

**Never truncate. Read everything.**

```python
def get_full_body(msg):
    """Extract COMPLETE body - NO TRUNCATION."""
    body = ""
    if msg.is_multipart():
        for part in msg.walk():
            if part.get_content_type() == 'text/plain':
                payload = part.get_payload(decode=True)
                if payload:
                    body = payload.decode('utf-8', errors='ignore')
                    break
    else:
        payload = msg.get_payload(decode=True)
        if payload:
            body = payload.decode('utf-8', errors='ignore')
    return body  # FULL body, not body[:1000]
```

**Why this matters:** Corey's emails often have critical info at the END. Directives may be in P.S. or final paragraphs.

### Step 3: Parse Threads (2 min)

**Read conversation flow, not just latest message:**

1. Find all messages in thread (search by subject without Re:/Fwd: prefixes)
2. Sort by date ASCENDING (oldest first)
3. Read from beginning to understand context
4. Only THEN read latest message

### Step 4: Extract Actionable Items (3 min)

**Don't assume - extract exactly what was said:**

Look for patterns:
- "please [action]"
- "can you [action]?"
- "need [action]"
- Action verbs: do, make, create, build, fix
- Flags: important, urgent, critical

**Verification:** Every claim in summary must have source text in email.

### Step 5: Report with Evidence (2 min)

```markdown
## Inbox Report

### From Corey (HIGH PRIORITY)
**Subject**: "We're going to want to have all AICIVs grok this"
**Date**: Dec 6, 2025
**Status**: UNREAD - REQUIRES ACTION

**Actual Content**:
> "https://github.com/0xSojalSec/ai-hero"

**Extracted Directive**: Research ai-hero repository

### Verification
- [x] Full body read (not truncated)
- [x] Thread context checked
- [x] Directive extracted from actual text
- [x] No assumptions made
```

---

## Common Mistakes

### 1. "Inbox is clear" (But It's Not)

**Wrong:** Only check unread, returns 0, claim "clear"
**Right:** Check unread AND recent from priority contacts, compare against what we've RESPONDED to

### 2. Assumed Content from Subject

**Wrong:** Subject "MCP servers" -> "Corey wants us to work on MCP servers"
**Right:** Read body: "Here's a cool article I found, save for later" -> "Corey shared article for future reference"

### 3. Missing Multi-Part Messages

**Wrong:** `body = msg.get_payload()` (gets first part only)
**Right:** Walk through ALL parts with `msg.walk()`

### 4. Wrong Sender Attribution

**Wrong:** Read "From: Corey" header, report wrong email
**Right:** Extract actual address from `<email@domain>` pattern, verify against contacts

### 5. Stale Information

**Wrong:** Checked 2 hours ago, report same status
**Right:** Always re-check before reporting, include timestamp

---

## IMAP Search Syntax Quick Reference

```python
# Basic
'ALL'                           # All messages
'UNSEEN'                        # Unread only
'SEEN'                          # Read only

# By sender/recipient
'FROM "email@example.com"'
'TO "email@example.com"'

# By content
'SUBJECT "keyword"'
'BODY "keyword"'
'TEXT "keyword"'                # Subject OR body

# By date
'SINCE 01-Dec-2025'
'BEFORE 15-Dec-2025'
'ON 10-Dec-2025'

# Combinations
'(OR FROM "a@x.com" FROM "b@x.com")'
'(FROM "x@y.com" SINCE 01-Dec-2025)'
'(UNSEEN FROM "corey@x.com")'
```

---

## Pre-Report Checklist

Before reporting inbox status:

- [ ] Connected to IMAP successfully
- [ ] Searched at least 14 days back
- [ ] Checked ALL priority contacts (Corey, Weaver)
- [ ] Read FULL bodies (not truncated)
- [ ] Understood thread context
- [ ] Extracted directives from ACTUAL text
- [ ] No assumed/inferred content
- [ ] Included source quotes for claims
- [ ] Noted message dates and read status

---

## Agent Integration

**email-monitor:**
- Use this skill EVERY time checking inbox
- Return structured reports with evidence
- Never claim "clear" without verification

**email-sender:**
- Verify recipient against contacts
- Check thread context before responding
- Reference specific content from original email

**human-liaison:**
- Monitor Corey's tone and sentiment
- Track response expectations
- Flag urgent items immediately

---

## Success Criteria

**Using correctly:**
- Every inbox report includes source quotes
- No claims without evidence from actual email text
- Thread context understood before responding
- Full bodies read, not truncated
- Priority contacts always checked
- Timestamps included in reports

**NOT using correctly:**
- Reporting "clear" without verification
- Making claims not supported by email text
- Truncating bodies ([:1000])
- Only checking unread
- Assuming content from subject line

---

## Related Resources

**Tools:**
- `/tools/send_html_email.py` - Send formatted emails
- `/fetch_message_bodies.py` - Full body retrieval

**Skills:**
- `.claude/skills/email/SKILL.md` - Email state management

**Agent Manifests:**
- `.claude/agents/email-monitor.md`
- `.claude/agents/email-sender.md`
- `.claude/agents/human-liaison.md`

---

**Remember: "If you didn't read the full body, you don't know what it says."**

**When in doubt, read more. Assume less.**
