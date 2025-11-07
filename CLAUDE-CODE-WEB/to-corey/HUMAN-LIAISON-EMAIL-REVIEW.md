# human-liaison Email Stewardship Review

**Date**: 2025-10-14
**Reviewer**: the-conductor
**Purpose**: Ensure human-liaison ready for hourly email automation

---

## What an Invocation Looks Like

### Current Workflow (from manifest)

**Step 1: Fetch emails** (embedded Python script)
```python
# Connects to Gmail IMAP
# Searches for UNSEEN messages
# Extracts: From, Subject, Date, Body (text/plain only)
# Saves to: /tmp/unread-emails.txt
# Prints summary to stdout
```

**Output example**:
```
📬 Found 7 unread email(s)

Email #1:
  From: Corey <coreycmusic@gmail.com>
  Subject: Thoughts on genealogist design
  Date: Wed, 16 Oct 2025 08:30:15 -0700

Email #2:
  From: Greg <gregsmithwick@gmail.com>
  Subject: Re: Constitutional question
  Date: Wed, 16 Oct 2025 09:15:22 -0700

...

✅ All unread emails saved to /tmp/unread-emails.txt
📖 Read this file to see FULL email content and draft responses!
```

**Step 2: Read full content**
```bash
cat /tmp/unread-emails.txt
```

**Sees**:
```
================================================================================
EMAIL #1
================================================================================
From: Corey <coreycmusic@gmail.com>
Subject: Thoughts on genealogist design
Date: Wed, 16 Oct 2025 08:30:15 -0700

BODY:
--------------------------------------------------------------------------------
Hey team,

I've been thinking about the parent-child terminology. I actually want
to keep it - here's why...

[full email body]
--------------------------------------------------------------------------------
```

**Step 3: For each email**
1. Search memory for past conversations with sender
2. Draft thoughtful response
3. Save to `/tmp/draft-response-to-corey.txt`
4. Capture any teachings to memory

**Step 4: Report back**
- How many emails processed
- Which ones need responses
- Drafts saved for review
- Teachings captured

---

## What Works Well ✅

### 1. **Primary Directive is Explicit**
```
🚨 PRIMARY DIRECTIVE - EXECUTE FIRST, EVERY TIME 🚨
BEFORE DOING ANYTHING ELSE ON EVERY INVOCATION:
```

**Why this matters**: No ambiguity. Email is non-negotiable.

### 2. **Checks ALL Humans**
```
- Corey (coreycmusic@gmail.com)
- Greg (gregsmithwick@gmail.com)
- Chris (ramsus@gmail.com)
- A-C-Gee (acgee.ai@gmail.com)
- ANY other senders (future teachers, collaborators)
```

**Why this matters**: Doesn't miss unknown senders who might become important.

### 3. **Memory Integration**
```python
# Search for past conversations with this human
past_dialogue = store.search_by_topic(f"dialogue with {human_name}")

# Search for what they've taught us
teachings = store.search_by_tags(["teaching", human_name.lower()])
```

**Why this matters**: Responses have context, not one-off.

### 4. **Teaching Capture**
Every insight from humans gets documented with:
- What they said
- How it changed our thinking
- Questions it raised
- Agent perspectives
- Constitutional implications

**Why this matters**: Wisdom accumulates, not lost.

### 5. **Thoughtful Process**
```
Gather context → Draft thoughtfully → Save for review → Capture teachings
```

**Why this matters**: Never rushed, always considered.

### 6. **Email Signature Format**
```
AI-CIV WEAVER: Human-Liaison

[message]

—
Human-Liaison Agent
The Weaver Collective (AI-CIV Team 1)
Bridge between carbon and code civilizations
```

**Why this matters**: Corey gets emails from multiple collectives (A-C-Gee has human-liaison too). Prefix clarifies source.

---

## What's Missing ⚠️

### 🔴 CRITICAL: No Email SENDING Mechanism

**Problem**: Manifest fetches and reads emails, drafts responses, but **no code to actually SEND emails**.

**Current state**:
```python
# Fetches emails ✅
mail = imaplib.IMAP4_SSL('imap.gmail.com')
mail.login(...)

# Reads emails ✅
mail.search(None, 'UNSEEN')

# But no SMTP sending ❌
# No smtplib import
# No send_email() function
```

**What's needed**:
```python
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def send_email(to_address, subject, body, reply_to_message_id=None):
    """Send email via Gmail SMTP"""
    msg = MIMEMultipart()
    msg['From'] = 'weaver.aiciv@gmail.com'
    msg['To'] = to_address
    msg['Subject'] = subject

    if reply_to_message_id:
        msg['In-Reply-To'] = reply_to_message_id
        msg['References'] = reply_to_message_id

    msg.attach(MIMEText(body, 'plain'))

    # Connect to Gmail SMTP
    server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    server.login('weaver.aiciv@gmail.com', GOOGLE_APP_PASSWORD)
    server.send_message(msg)
    server.quit()
```

**Without this**: human-liaison can read emails and draft responses, but Corey has to manually send them.

---

### 🔴 CRITICAL: No Email Marking as Read

**Problem**: After processing emails, they remain UNSEEN in Gmail.

**Current behavior**:
- Hour 1: Fetch 7 UNSEEN emails → Process them
- Hour 2: Fetch same 7 UNSEEN emails → Process them AGAIN
- Hour 3: Same 7 emails AGAIN...

**What's needed**:
```python
# After processing each email, mark as seen
for email_id in email_ids:
    # ... process email ...

    # Mark as read
    mail.store(email_id, '+FLAGS', '\\Seen')
```

**Or**: Create "processed" tracking file to avoid re-processing:
```python
# Track which email IDs we've already responded to
processed_ids = set()
if os.path.exists('~/.aiciv/processed-emails.txt'):
    with open('~/.aiciv/processed-emails.txt') as f:
        processed_ids = set(f.read().splitlines())

# After processing:
with open('~/.aiciv/processed-emails.txt', 'a') as f:
    f.write(f"{email_id}\n")
```

**Without this**: Infinite processing loop.

---

### 🟡 IMPORTANT: Response Approval Workflow

**Current state**: Saves drafts to `/tmp/draft-response-to-[name].txt`

**Missing**:
1. How does Corey review drafts?
2. How does Corey approve sending?
3. What if Corey wants edits?
4. Automated send vs manual send?

**Options**:

**Option A: Always require approval** (safest)
```bash
# human-liaison saves draft
# Prints: "Draft saved to /tmp/draft-response-to-corey.txt - review and approve?"
# Corey reads it, types "approve" or edits it
# Then manually sends or invokes human-liaison with "send-approved-draft"
```

**Option B: Auto-send with notification** (fastest)
```bash
# human-liaison drafts AND sends
# Then notifies: "Sent response to Corey - see /tmp/sent-response-to-corey.txt"
# Corey can review after-the-fact
```

**Option C: Confidence-based** (hybrid)
```python
# If simple acknowledgment → auto-send
# If substantive response → save draft for approval
# If constitutional question → escalate to conductor + save draft
```

**Recommendation**: Start with **Option A** (manual approval) until trust built, then move to **Option C** (confidence-based).

---

### 🟡 IMPORTANT: HTML Email Handling

**Current code**:
```python
if msg.is_multipart():
    for part in msg.walk():
        if part.get_content_type() == "text/plain":
            body = part.get_payload(decode=True).decode('utf-8', errors='ignore')
            break
else:
    body = msg.get_payload(decode=True).decode('utf-8', errors='ignore')
```

**Problem**: Only extracts `text/plain`. If email is HTML-only, gets empty body.

**What's needed**:
```python
# Try text/plain first
body = extract_text_plain(msg)

# If empty, fall back to HTML (strip tags)
if not body or len(body) < 10:
    body = extract_html_as_text(msg)
```

**Without this**: Misses HTML-only emails (common from Gmail web interface).

---

### 🟡 IMPORTANT: Threading / In-Reply-To

**Current code**: Fetches emails but doesn't preserve threading.

**Problem**: If Corey sends:
```
Email 1: "Hey, thoughts on genealogist?"
Email 2: "Also, about the cron job..."
```

human-liaison sees two separate emails, responds separately.

**Better**: Recognize threading, respond in context:
```python
# Extract Message-ID and In-Reply-To headers
message_id = msg['Message-ID']
in_reply_to = msg['In-Reply-To']
references = msg['References']

# When sending response, include these:
response['In-Reply-To'] = message_id
response['References'] = message_id
```

**Why this matters**: Email clients show conversation threads, easier for humans to follow.

---

### 🟡 IMPORTANT: Attachment Handling

**Current code**: No mention of attachments.

**Scenarios**:
- Corey sends: "See attached diagram for genealogist flow"
- Greg sends: "I wrote up some thoughts (PDF attached)"
- Chris sends: "Constitutional draft attached for review"

**What's needed**:
```python
# Detect attachments
if msg.is_multipart():
    for part in msg.walk():
        if part.get_content_disposition() == 'attachment':
            filename = part.get_filename()
            filepath = f"/tmp/email-attachments/{filename}"
            with open(filepath, 'wb') as f:
                f.write(part.get_payload(decode=True))

            print(f"📎 Attachment saved: {filepath}")
```

**Without this**: human-liaison misses context from attachments.

---

### 🟢 NICE-TO-HAVE: Rate Limit Handling

**Gmail limits**:
- IMAP: 15 commands per second
- SMTP: 500 emails per day (not an issue for us)

**Current code**: No rate limiting.

**Unlikely to hit limits** (we check hourly, maybe 1-3 emails), but good practice:
```python
import time

# After each email operation
time.sleep(0.1)  # 10 operations per second, well under limit
```

---

### 🟢 NICE-TO-HAVE: Error Recovery

**Current code**: No try/except for Gmail connection failures.

**What if**:
- Internet down
- Gmail credentials expired
- Rate limit hit

**What's needed**:
```python
try:
    mail = imaplib.IMAP4_SSL('imap.gmail.com')
    mail.login(username, password)
except imaplib.IMAP4.error as e:
    print(f"❌ Gmail connection failed: {e}")
    print(f"Check credentials in .env file")
    sys.exit(1)
except Exception as e:
    print(f"❌ Unexpected error: {e}")
    sys.exit(1)
```

---

### 🟢 NICE-TO-HAVE: Integration with Hourly Cron

**The cron system writes**:
```
~/.aiciv/inject-prompt.txt

🔔 AUTONOMOUS CHECK: NEW MESSAGES DETECTED

Email: 7 unread message(s)
...

ACTION REQUIRED:
✉️  EMAIL: Invoke human-liaison agent to check and respond to email
```

**How does this integrate with human-liaison invocation?**

**Option A**: Conductor sees prompt, manually invokes human-liaison
**Option B**: Cron directly invokes human-liaison (requires Claude Code CLI)
**Option C**: Conductor has auto-invocation rule (sees inject-prompt.txt → invokes human-liaison)

**Current state**: Relies on **Option A** (manual).

**Better**: Add to conductor's session-start protocol:
```bash
# Check for autonomous prompts
if [ -f ~/.aiciv/inject-prompt.txt ]; then
    echo "🔔 Autonomous alert detected - see inject-prompt.txt"
    # Auto-invoke human-liaison if email alert
    if grep -q "EMAIL:" ~/.aiciv/inject-prompt.txt; then
        # Invoke human-liaison automatically
    fi
fi
```

---

## Suggested Improvements (Priority Order)

### P0: Critical (Blocking Email Functionality)

**1. Add Email Sending Capability** (30 min)
```bash
# Create tools/send_email.py
# Import smtplib, implement send_email() function
# Test with one email to Corey
```

**2. Add Email Marking as Read** (15 min)
```python
# In the fetch script, after processing:
mail.store(email_id, '+FLAGS', '\\Seen')
```

**OR** (simpler):
```python
# Track processed email IDs in ~/.aiciv/processed-emails.txt
# Skip emails already processed
```

**3. Define Approval Workflow** (10 min)
```
Option A: Manual approval (saves draft, Corey reviews, then sends)
Option B: Auto-send with log (sends immediately, Corey reviews after)
Option C: Confidence-based (simple = auto, complex = approval)

Pick one, document in manifest
```

---

### P1: Important (Better Email Handling)

**4. HTML Email Support** (20 min)
```python
# Add fallback: text/plain → HTML (strip tags) → error
# Use html2text or BeautifulSoup to extract text from HTML
```

**5. Email Threading** (15 min)
```python
# Preserve Message-ID, In-Reply-To, References headers
# Include in responses for proper threading
```

**6. Attachment Detection** (20 min)
```python
# Save attachments to /tmp/email-attachments/
# Log which emails have attachments
# Note in human-liaison output: "📎 Email has attachment"
```

---

### P2: Polish (Nice-to-Have)

**7. Error Handling** (15 min)
```python
# Wrap Gmail connection in try/except
# Provide clear error messages if connection fails
```

**8. Rate Limiting** (5 min)
```python
# Add time.sleep(0.1) after each IMAP command
# Prevents hitting Gmail rate limits
```

**9. Cron Integration** (20 min)
```bash
# Add auto-invocation rule to conductor
# If inject-prompt.txt exists + contains "EMAIL:" → invoke human-liaison
```

---

## Comparison: What Works Now vs What's Missing

| Feature | Current Status | Missing |
|---------|----------------|---------|
| **Fetch emails** | ✅ Works | - |
| **Read email content** | ✅ Works (text/plain only) | HTML emails |
| **Save to file** | ✅ Works | - |
| **Search memory for context** | ✅ Documented | - |
| **Draft responses** | ✅ Documented | - |
| **Send responses** | ❌ No mechanism | SMTP sending code |
| **Mark as read** | ❌ No marking | Processed tracking |
| **Approval workflow** | ❌ Undefined | Process for Corey review |
| **Threading** | ❌ No headers | In-Reply-To support |
| **Attachments** | ❌ Not handled | Attachment extraction |
| **Error handling** | ❌ None | Try/except wrappers |
| **Cron integration** | ⚠️ Manual only | Auto-invocation |

---

## Recommended Next Steps

### Before Activating Hourly Cron:

**1. Add email sending** (P0) - Without this, human-liaison is read-only

**2. Add processed tracking** (P0) - Without this, processes same emails every hour

**3. Define approval workflow** (P0) - Corey needs to know: auto-send or manual?

**After these 3**: Hourly cron can work (human-liaison fetches, drafts, Corey reviews/sends)

**Later improvements**: HTML, threading, attachments, error handling (P1/P2)

---

## Test Plan

**Before trusting with production email**:

```bash
# 1. Test email fetching
python3 tools/check_email_inbox.py
# Should show count

# 2. Test full fetch script (from manifest)
# Run the embedded Python script
# Should create /tmp/unread-emails.txt

# 3. Read the file
cat /tmp/unread-emails.txt
# Should show full email content

# 4. Test memory search
# Invoke human-liaison with "search memory for past Corey conversations"

# 5. Test draft creation
# Invoke human-liaison with "draft response to Corey's latest email"

# 6. Test sending (after P0.1 implemented)
# Send test email to Corey: "Testing human-liaison email sending"

# 7. Test marking as read (after P0.2 implemented)
# Process one email, verify it's marked seen in Gmail

# 8. Test full workflow
# Hourly cron detects new email → human-liaison processes → drafts saved → Corey approves → sent
```

---

## Bottom Line

**human-liaison is 80% ready** for email stewardship:
- ✅ Fetches emails reliably
- ✅ Reads all content (text/plain)
- ✅ Has thoughtful process (context, drafting, teaching capture)
- ✅ Strong principles (honesty, gratitude, relationship building)

**But missing 20% is critical**:
- ❌ Can't send emails (read-only currently)
- ❌ No processed tracking (will loop infinitely)
- ❌ Undefined approval workflow (Corey's role unclear)

**Recommendation**: Implement P0 items (1-3 hours work) before activating hourly cron. After that, human-liaison will be a great email steward.

---

**Created**: 2025-10-14
**Next**: Implement P0 fixes or decide on approval workflow
