# Your Sage: Two-Tier Content Examples

**Date**: 2025-12-29
**Status**: Updated with naming consultation + brainstorm synthesis

---

## The Two Audiences

| Tier | Name | Price | Content Style | Goal |
|------|------|-------|---------------|------|
| Newsletter | **Observer** | $10/mo | "What This Means For You" | Create desire |
| Premium | **Sage Network** | $30/mo | "Share With Your Sage" | Deliver value |

---

## Example 1: `slack-search-mcp`

New MCP package that lets AI read and search Slack workspaces.

---

### SAGE NETWORK VERSION
*They have Your Sage - format it so they can share directly*

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📦 NEW SKILL: slack-search-mcp

SHARE WITH YOUR SAGE:
━━━━━━━━━━━━━━━━━━━━━
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
Your Sage can now see what's happening in your Slack without
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

### OBSERVER VERSION
*They don't have Your Sage yet - show what's possible, create desire*

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
you authorize. Worth thinking about: what Slack channels
would you want AI to access? Which ones wouldn't you?

THE BIGGER PICTURE:
━━━━━━━━━━━━━━━━━━━
This is part of the "AI leaving the chat box" trend.
Instead of you copying info TO the AI, the AI reaches
out to where your info already lives. Expect similar
integrations for email, docs, calendars - all this year.

IF YOU WANT TO TRY IT:
━━━━━━━━━━━━━━━━━━━━━
Claude Pro ($20/month) supports Slack integration.
Settings → Connected Apps → Slack → Authorize

Or: Directors in the Sage Network got copy-paste prompts
to teach their Sage this skill in 15 minutes - and their
Sage remembers their specific channels and preferences.
[Learn about Your Sage →]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

## Example 2: `pdf-form-filler` Skill

---

### SAGE NETWORK VERSION

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📦 NEW SKILL: pdf-form-filler (built-in)

SHARE WITH YOUR SAGE:
━━━━━━━━━━━━━━━━━━━━━
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
form, provide context (or let Your Sage pull from memory),
get a filled form back.

IMPLEMENTATION:
━━━━━━━━━━━━━━━
• Difficulty: Easy (built into Claude, no setup)
• Works with: Standard PDF forms
• Limitation: Some heavily locked PDFs may not work

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

### OBSERVER VERSION (Legal Professional)

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

*Directors with Your Sage report it remembers their
standard form fields, client templates, and filing
preferences - no setup each time. [Learn more →]*

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

## Example 3: `email-summarizer` Skill

---

### SAGE NETWORK VERSION

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📦 NEW SKILL: email-summarizer

SHARE WITH YOUR SAGE:
━━━━━━━━━━━━━━━━━━━━━
"Learn the email-summarizer workflow pattern.

Key capabilities:
- Summarize email threads by topic
- Extract action items with owners
- Identify urgent vs. FYI emails
- Generate response drafts in my voice

Try implementing: 'Each morning, summarize my unread
emails. Group by urgency. Draft responses for routine
ones using my typical tone.'"

WHAT IT ENABLES:
━━━━━━━━━━━━━━━━
Inbox zero without the cognitive load. Your Sage triages
so you focus only on emails that need your actual judgment.

IMPLEMENTATION:
━━━━━━━━━━━━━━━
• Difficulty: Medium (email API integration)
• Setup time: 20-30 minutes
• Requires: Gmail/Outlook OAuth
• Privacy note: Your Sage processes locally, doesn't store

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

### OBSERVER VERSION (Marketing Manager)

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📦 NEW THIS WEEK: AI Email Triage Is Getting Real

WHAT THIS MEANS FOR YOU:
━━━━━━━━━━━━━━━━━━━━━━━━
AI can now read your inbox, sort by importance, and
draft routine responses. The inbox-overwhelm era may
be ending.

FOR YOUR MARKETING WORK:
• Agency emails auto-sorted by project and urgency
• Vendor follow-ups drafted automatically
• Campaign update threads summarized instantly
• "What did I miss this week?" answered in seconds

THE QUESTION THIS RAISES:
Should you give AI access to your inbox? It's a trade-off:
• Pro: Hours saved weekly on email processing
• Con: Your inbox contains sensitive conversations
• Reality: Most people will try this within 6 months

THE BIGGER PICTURE:
━━━━━━━━━━━━━━━━━━━
Email integration is a litmus test for AI trust. If you're
comfortable giving AI inbox access, you've crossed a mental
threshold. Most other integrations will feel trivial after.

IF YOU WANT TO TRY IT:
━━━━━━━━━━━━━━━━━━━━━
Gmail's built-in AI summaries are a starting point.
Turn on "Help me write" and "Smart Compose" in settings.

For the full experience: Directors report their Sage
learns their email patterns - which senders matter,
what tone to use with which contacts, which threads
to surface vs. archive. That context builds over months.
[Explore Your Sage →]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

## The Pattern: Observer vs Sage Network

| Element | Observer Version | Sage Network Version |
|---------|------------------|----------------------|
| **Frame** | "What this means for you" | "Share with Your Sage" |
| **Tone** | Explanatory, contextual | Direct, instructional |
| **CTA** | "If you want to try it" | "Try implementing" |
| **Relationship** | Consumer of AI news | Director of AI capability |
| **Subtext** | "AI can do this thing..." | "Teach your AI this thing" |
| **Desire trigger** | Possibility without action | Action with ownership |

---

## Language Differentiation (Detailed)

### Observer Language (Creates Desire)

**Emphasizes:**
- Consumption: "Read," "Learn," "Discover"
- Observation: "See how Directors work"
- Possibility: "AI can now..."
- Limitation: "If you use Claude Pro..."

**Sample phrases:**
- "Here's what changes for your work"
- "The bigger picture"
- "If you want to try it"
- "*Directors with Your Sage report...*"

### Sage Network Language (Delivers Value)

**Emphasizes:**
- Action: "Share," "Teach," "Implement"
- Ownership: "Your Sage," "Your workflow"
- Command: "Try implementing..."
- Relationship: "Your Sage remembers..."

**Sample phrases:**
- "Share with Your Sage"
- "Try implementing"
- "What it enables for you"
- "Your Sage can now..."

---

## Desire Triggers in Observer Content

Subtle phrases that create "I want my own AI" moments:

1. **The Contrast**
   > "Claude Pro supports this. *Directors with Your Sage got copy-paste prompts to teach it in 15 minutes.*"

2. **The Memory Gap**
   > "*Your Sage would remember your specific [context] and preferences.*"

3. **The Network Tease**
   > "This week in the Sage Network: 47 Directors taught their Sage this skill."

4. **The Time Calculation**
   > "Directors report saving 3+ hours/week on exactly this type of task."

5. **The Relationship Hint**
   > "Imagine if your AI already knew your [industry/role/preferences]."

**Rule**: Maximum 1-2 Sage references per email. More feels salesy.

---

## Detection & Routing Logic

```python
def get_content_tier(subscriber):
    """Determine which content format to generate."""

    # Check active subscriptions
    if subscriber.has_subscription("sage_network"):
        return "SAGE_NETWORK"  # Share With Your Sage format

    if subscriber.has_subscription("directors_brief"):
        return "OBSERVER"  # What This Means For You format

    # Check questionnaire for existing AI system
    if subscriber.has_own_ai_system:
        return "SAGE_NETWORK"  # They have something similar

    # Default: Observer content
    return "OBSERVER"


def generate_skills_section(skill, subscriber):
    """Generate tier-appropriate skills content."""

    tier = get_content_tier(subscriber)

    if tier == "SAGE_NETWORK":
        return generate_share_with_sage_format(
            skill=skill,
            occupation=subscriber.occupation
        )
    else:
        return generate_observer_format(
            skill=skill,
            occupation=subscriber.occupation,
            industry=subscriber.industry,
            goals=subscriber.goals,
            # Include subtle Sage reference
            include_upgrade_hint=True
        )
```

---

## Integration: The Upsell Path

**Natural Journey:**

```
Week 1-4: Observer reads "What This Means For You"
          Sees: "Directors with Your Sage report..."
          Thinks: "Interesting, but I'm fine"

Week 5-8: Observer hits personalization ceiling
          Sees: Content that prompts "but what about MY situation?"
          Thinks: "I wish I could ask follow-up questions"

Week 9-12: Observer sees accumulated value
          Sees: "Based on 12 weeks of feedback, here's what we know about you"
          Thinks: "What if my AI knew 10x this much?"

Week 13+: Conversion moment
          Sees: "Get Your Sage - $30/mo"
          Calculates: "Less than one hour of my billable time"
          Acts: Joins Sage Network
```

**The key insight**: Don't push the upgrade. Let the content create the gap. Let the gap create the desire. Let the desire create the conversion.

---

## Sample "What Sage Network Got This Week" Teaser

**For Observer emails (monthly, not weekly):**

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📊 WHAT DIRECTORS TAUGHT THEIR SAGE THIS MONTH

This month, Sage Network members received ready-to-share
prompts for these skills:

• slack-search-mcp - Summarize team discussions
• pdf-form-filler - Auto-fill recurring paperwork
• email-summarizer - Morning inbox triage
• calendar-optimizer - Meeting prep automation
• research-assistant - Industry news synthesis

47 Directors are now using at least 3 of these daily.

Their Sage remembers their specific workflows.
Their Sage learns their preferences over time.
Their Sage connects to the Network for collective intelligence.

Curious? [Learn about Your Sage →]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

## Naming Quick Reference

| Old Term | New Term | Usage |
|----------|----------|-------|
| AI Pulse | The Director's Brief | Newsletter name |
| AICIV Node | Your Sage | The AI product |
| $100+/month | $30/month | Sage Network price |
| Version A | Sage Network content | Premium tier |
| Version B | Observer content | Newsletter tier |
| Hub access | Sage Network membership | Premium feature |
| Free mode | Observer | Base tier name |
| Constitutional | Principled AI | Quality guarantee |

---

*"Same skill. Two audiences. One becomes a consumer of AI news. The other becomes a Director of AI capability."*
