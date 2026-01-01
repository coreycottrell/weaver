# Skills Section: Two-Tier Examples

## Same Skill, Two Audiences

---

## This Week's Skill: `slack-search-mcp`

New MCP package that lets AI read and search Slack workspaces.

---

### VERSION A: For AICIV Subscribers
*They have their own AI - format it so they can share it directly*

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📦 NEW SKILL: slack-search-mcp

SHARE WITH YOUR AI:
━━━━━━━━━━━━━━━━━━━
"Learn the slack-search-mcp skill. 

Documentation: https://github.com/anthropics/mcp-servers/tree/main/slack

Key capabilities:
- Search messages across channels
- Read thread conversations
- Access user profiles and presence
- Filter by date, channel, or user

Try implementing: 'Every Monday morning, summarize the key 
discussions from #engineering and #product from last week 
and flag anything that needs my attention.'"

WHAT IT ENABLES:
━━━━━━━━━━━━━━━━
Your AI can now see what's happening in your Slack without 
you copy-pasting. Context from team discussions becomes 
available for any task you're working on together.

IMPLEMENTATION:
━━━━━━━━━━━━━━━
• Difficulty: Medium (OAuth setup required)
• Setup time: 15-20 minutes  
• Requires: Slack workspace admin approval
• Works with: Any Claude-based system with MCP support

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

### VERSION B: For Non-AICIV Subscribers  
*They don't have their own AI - explain how this affects their life/work*

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📦 NEW THIS WEEK: AI Can Now Read Your Slack

WHAT THIS MEANS FOR YOU:
━━━━━━━━━━━━━━━━━━━━━━━━
AI assistants can now search and read Slack messages 
(with permission). Here's what changes:

FOR YOUR WORK:
• "Catch me up on what I missed" becomes real
• AI can find that conversation you half-remember
• Meeting prep can include "what has the team said about X?"
• Less context-switching between Slack and AI tools

THE PRIVACY ANGLE:
This requires explicit permission - AI can only see what 
you authorize. But worth thinking about: what Slack 
channels would you want AI to access? Which ones wouldn't 
you?

THE BIGGER PICTURE:
━━━━━━━━━━━━━━━━━━━
This is part of the "AI leaving the chat box" trend. 
Instead of you copying info TO the AI, the AI reaches 
out to where your info already lives. Expect similar 
integrations for email, docs, calendars - all this year.

IF YOU WANT TO TRY IT:
━━━━━━━━━━━━━━━━━━━━━
Claude Pro ($20/month) now supports Slack integration.
Settings → Connected Apps → Slack → Authorize

Takes 5 minutes. Start with low-stakes channels to 
see how it works before giving access to sensitive ones.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

## Another Example: `pdf-form-filler` Skill

---

### VERSION A: For AICIV Subscribers

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📦 NEW SKILL: pdf-form-filler (built-in)

SHARE WITH YOUR AI:
━━━━━━━━━━━━━━━━━━━
"You now have the pdf-form-filler skill available.

Key capabilities:
- Fill PDF forms programmatically
- Extract form field names and types
- Handle multi-page forms
- Preserve original formatting

Try implementing: 'When I share a PDF form and context 
about what should go in it, fill it out and give me the 
completed version.'"

WHAT IT ENABLES:
━━━━━━━━━━━━━━━━
No more manually typing into PDF forms. Upload the blank 
form, provide context (or let your AI pull from memory), 
get a filled form back.

IMPLEMENTATION:
━━━━━━━━━━━━━━━
• Difficulty: Easy (built into Claude, no setup)
• Works with: Standard PDF forms
• Limitation: Some heavily locked PDFs may not work

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

### VERSION B: For Non-AICIV Subscribers (Legal Professional)

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📦 NEW THIS WEEK: AI Can Fill Out PDF Forms

WHAT THIS MEANS FOR YOU:
━━━━━━━━━━━━━━━━━━━━━━━━
Those court forms, intake documents, and filing 
paperwork you fill out repeatedly? AI can now do that.

FOR YOUR LEGAL WORK:
• Upload a blank form + client info → get filled form
• Standard discovery requests filled in seconds
• Intake questionnaires → client forms automatically
• No more retyping the same address 50 times

TIME SAVINGS ESTIMATE:
If you fill 10+ PDF forms weekly, this could save 
2-3 hours. Not life-changing, but real.

THE CAUTION:
━━━━━━━━━━━━━
• Always review AI-filled forms before filing
• Some jurisdictions have rules about AI-prepared docs
• Keep confidential client info off cloud AI for now
  (wait for on-premise options if this concerns you)

IF YOU WANT TO TRY IT:
━━━━━━━━━━━━━━━━━━━━━
Claude Pro already has this. Upload any PDF form and 
say "fill this out with the following information: [info]"

Start with internal forms (not client-facing) to test.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

## The Pattern

| Subscriber Type | Focus | Tone | Call to Action |
|-----------------|-------|------|----------------|
| **AICIV ($100+)** | Technical implementation | Direct, instructional | "Share this with your AI" |
| **Non-AICIV ($10)** | Personal/work impact | Explanatory, contextual | "Here's what to consider" |

**AICIV subscribers** have a working AI system. They want to know: "Can my AI learn this? How do I teach it?"

**Non-AICIV subscribers** use AI tools but don't have their own system. They want to know: "How does this change things for me? Should I care?"

Same information, different framing.

---

## Detection & Routing

```python
def get_skills_version(subscriber):
    """Determine which skills section format to use."""
    
    # Check if they're an AICIV subscriber
    if subscriber.email in aiciv_subscriber_emails:
        return "VERSION_A"  # Share with your AI
    
    # Check questionnaire response
    if subscriber.has_own_ai_system == True:
        return "VERSION_A"
    
    # Default: they don't have their own AI
    return "VERSION_B"  # What this means for you


def generate_skills_section(skill, subscriber):
    """Generate the appropriate skills content."""
    
    version = get_skills_version(subscriber)
    
    if version == "VERSION_A":
        return generate_share_with_ai_format(
            skill=skill,
            occupation=subscriber.occupation
        )
    else:
        return generate_impact_format(
            skill=skill,
            occupation=subscriber.occupation,
            industry=subscriber.industry,
            goals=subscriber.goals
        )
```

---

## Integration with AICIV Billing

When someone subscribes to AICIV ($100+ tier):
1. Add their email to `aiciv_subscriber_emails` list
2. They automatically get VERSION_A skills content
3. If they also subscribe to AI Pulse, they get the enhanced format

When someone churns from AICIV:
1. Remove from list
2. Downgrade to VERSION_B if they still have AI Pulse subscription

This creates a natural upsell path:
- AI Pulse subscriber reads VERSION_B content
- Thinks "I wish I had an AI I could share this with"
- Explores AICIV subscription
- Gets VERSION_A content + their own AI system
