# AI Pulse: Revised Structure

**Date**: 2025-12-29
**Status**: Updated based on Corey feedback

---

## Core Philosophy

**Real value every week. 5 minutes max. Tailored to YOU.**

We don't blast the same newsletter to everyone. We gather the week's developments first, THEN an agent writes each subscriber's email based on their profile. If nothing relevant happened for you this week, we tell you that honestly. If something important did happen, we make sure you don't miss it.

---

## The Workflow

### Step 1: Data Collection (Monday-Wednesday)

Agents gather everything:
- AI news from 20+ sources
- New Claude skills released
- New MCP packages published
- r/ClaudeAI and r/AnthropicAI developments
- Major model releases, benchmarks, announcements
- Regulatory/policy updates
- Industry-specific AI developments

**Output**: Raw intelligence feed (100+ items)

### Step 2: Analysis & Categorization (Thursday)

Agents process the raw feed:
- Tag by industry relevance (healthcare, finance, legal, creative, etc.)
- Tag by occupation relevance (developer, manager, entrepreneur, etc.)
- Tag by impact timeline (affects you now / this month / this year / longer)
- Score by significance (noise vs. signal)
- Identify skills/packages worth highlighting

**Output**: Categorized intelligence with relevance scores

### Step 3: Personalized Writing (Friday Morning)

For EACH subscriber, an agent:
1. Pulls their questionnaire data (occupation, industry, goals, AI usage level)
2. Filters the week's intelligence to what's relevant to THEM
3. Writes their personalized 5-minute briefing
4. Determines skills/packages section based on subscriber tier

**Output**: Individualized emails ready to send

### Step 4: Send (Friday Afternoon)

Each subscriber gets THEIR version.

---

## Newsletter Structure

### Section 1: Your 5-Minute Briefing

**What it is**: The week's AI developments filtered through YOUR lens.

**Rules**:
- Maximum 5-minute read
- Only what's relevant to this specific subscriber
- Clear "why this matters to YOU" framing
- If nothing major affected them: "Quiet week for [your field]. Here's what's brewing."

**Example for a Healthcare Administrator**:
> "Two things matter for you this week:
> 
> 1. **CMS released guidance on AI documentation tools** - If your facility uses AI scribes, review the new compliance requirements by March 1.
> 
> 2. **Epic announced Claude integration** - Coming Q2. If you're on Epic, start conversations with your IT team now about rollout planning.
> 
> Everything else this week (new coding models, image generators, etc.) doesn't affect your work directly. You're caught up."

**Example for a Software Developer**:
> "Three things for your radar:
>
> 1. **Cursor shipped Claude Sonnet 4.5 native** - If you're still on Copilot, worth a weekend test.
>
> 2. **Python 3.13 async improvements play well with AI tooling** - The new TaskGroup patterns make agent orchestration cleaner.
>
> 3. **GitHub Actions now supports MCP servers** - You can trigger Claude workflows from CI/CD. Opens up automated code review pipelines.
>
> The rest is noise for you this week."

---

### Section 2: Skills & Packages Update

**Two versions based on subscriber tier:**

#### Version A: For AICIV Subscribers ($100+/month)

These subscribers have their own AI (AICIV fork or similar). Format the content so they can SHARE IT WITH THEIR AI to learn the new capability.

**Format**:
```
## New This Week: [Skill/Package Name]

### Share With Your AI:
"Learn the [skill-name] skill. Here's the documentation: [link]. 
Key capabilities: [list]. Try implementing [specific use case] for our workflow."

### What It Enables:
[2-3 sentences on new capabilities]

### Implementation Notes:
- Difficulty: [Easy/Medium/Advanced]
- Setup time: [estimate]
- Dependencies: [if any]
```

**Example**:
```
## New This Week: google-sheets-mcp

### Share With Your AI:
"Learn the google-sheets-mcp package. Documentation: https://github.com/anthropics/mcp-servers/tree/main/google-sheets
Key capabilities: Read/write spreadsheets, create charts, run formulas programmatically.
Try implementing automated weekly report generation from our sales data."

### What It Enables:
Your AI can now interact directly with Google Sheets - reading data, writing updates, creating visualizations. No more copy-pasting between Claude and spreadsheets.

### Implementation Notes:
- Difficulty: Easy
- Setup time: 10 minutes (OAuth flow)
- Dependencies: Google Workspace account
```

#### Version B: For Non-AICIV Subscribers

These subscribers don't have their own AI system. Describe how the advancement might affect their personal or work life.

**Format**:
```
## New This Week: [Skill/Package Name]

### What This Means For You:
[How this might affect their work or personal life based on their profile]

### The Bigger Picture:
[Where this fits in the trajectory of AI capability]

### If You Want to Try It:
[Simple path to experiencing this yourself, if applicable]
```

**Example for a Marketing Manager**:
```
## New This Week: google-sheets-mcp

### What This Means For You:
AI assistants can now read and write directly to spreadsheets. For your work: imagine telling Claude "analyze last quarter's campaign performance and create a summary chart" - and it actually pulls the data, runs the analysis, and builds the visualization. No more exporting CSVs or manual chart-building.

### The Bigger Picture:
This is part of a pattern: AI moving from "chat in a box" to "integrated into your actual tools." Expect similar integrations with most productivity software over the next 6-12 months.

### If You Want to Try It:
If you use Claude Pro ($20/month), you can enable this in Settings → Connected Apps → Google Sheets. Takes 5 minutes.
```

---

## Personalization Logic

### Data We Use From Questionnaire

| Field | How We Use It |
|-------|---------------|
| Occupation | Filter news by job relevance |
| Industry | Filter news by sector relevance |
| "10 extra hours" answer | Frame benefits in terms of time savings |
| "One thing AI could help with" | Prioritize skills/tools that address this |
| AI usage level | Calibrate technical depth |
| Content preferences | Adjust length/detail |

### Relevance Scoring

Each week's item gets scored against each subscriber:

```python
def calculate_relevance(item, subscriber):
    score = 0
    
    # Industry match
    if item.industries & subscriber.industry:
        score += 3
    
    # Occupation match  
    if item.occupations & subscriber.occupation:
        score += 3
    
    # Addresses their stated goal
    if item.addresses_goal(subscriber.ai_wish):
        score += 5
    
    # Matches their AI usage level
    if item.complexity <= subscriber.ai_level:
        score += 1
    
    # High general significance
    score += item.significance_score
    
    return score

# Only include items scoring 4+ in their briefing
# Items scoring 7+ get highlighted treatment
```

### "Quiet Week" Logic

If a subscriber has no items scoring 4+:
- Acknowledge it's a quiet week for their field
- Give 1-2 sentence preview of what's brewing
- Keep it SHORT (they got value by NOT reading unnecessary content)

---

## Subscriber Tiers

| Tier | Price | Skills Section | Personalization |
|------|-------|----------------|-----------------|
| **Pulse** | $10/month or $100/year | Version B (how it affects you) | Full personalization |
| **AICIV Subscriber** | $100+/month | Version A (share with your AI) | Full personalization + AI-ready formatting |

### Detection Logic

When someone subscribes:
1. Check if their email matches an AICIV subscriber
2. If yes → They get Version A skills content
3. If no → They get Version B skills content

Or: Add a questionnaire field:
> "Do you have your own AI assistant/system (like an AICIV fork)?"
> - Yes, I have my own AI I work with regularly
> - No, I use AI tools but don't have my own system
> - I'm not sure what this means

---

## Sample Emails

### Sample: AICIV Subscriber (Developer)

```
Subject: 3 things for your week + a new skill for your AI

---

# Your 5-Minute Briefing

Hey [Name],

Three things matter for you this week:

**1. Anthropic released claude-code v0.2.41**
Bug fixes for the workspace scanning. If your AI uses Claude Code, update. The recursive directory issue that was causing hangs is fixed.

**2. New MCP auth patterns published**
The community settled on a standard for OAuth flows in MCP servers. If your AI is building integrations, this is the pattern to follow now.

**3. VS Code 1.96 broke some AI extensions**
If your AI helps with VS Code work, heads up - some extensions need updates. Cursor and Continue both pushed patches already.

That's it. Everything else (Gemini benchmarks, new image models, etc.) is noise for your work this week.

---

# New Skill: Share With Your AI

## filesystem-extended-mcp

**Share this with your AI:**
"Learn the filesystem-extended-mcp package. Docs: [link]. It adds file watching, recursive operations, and atomic writes to the basic filesystem MCP. Try implementing automatic backup of our project files when they change."

**What it enables:** Real-time file monitoring, batch operations, safer writes.
**Setup:** Easy, 5 minutes.

---

See you next week.
```

### Sample: Non-AICIV Subscriber (Healthcare Admin)

```
Subject: Quiet week for healthcare AI (but watch March)

---

# Your 5-Minute Briefing

Hey [Name],

Quiet week for healthcare-specific AI news. The big announcements were in coding tools and image generation - not your world.

**One thing to keep on radar:**
CMS is expected to release updated guidance on AI documentation tools in early March. If your facility uses or is considering AI scribes, that's when compliance requirements get clarified.

Nothing else needs your attention this week. You're caught up.

---

# New Capability: What It Means For You

## Voice-to-Documentation AI

**What happened:** Several EHR vendors announced AI that listens to patient encounters and auto-generates clinical notes.

**What this means for you:** The admin burden of documentation is about to shift. Doctors spend less time on notes → scheduling patterns might change. Compliance review processes will need updating for AI-generated content.

**Timeline:** Major EHR rollouts expected Q3-Q4 2026.

**No action needed now** - but worth mentioning in your next IT planning meeting.

---

See you next week.
```

---

## Implementation Notes

### Email Generation Pipeline

```
Friday 6 AM: Agent pulls week's categorized intelligence
Friday 6-10 AM: For each subscriber:
    1. Load their profile
    2. Check AICIV subscriber status
    3. Score all items against their profile
    4. Generate personalized briefing (5 min max)
    5. Generate appropriate skills section (Version A or B)
    6. Queue for send
Friday 12 PM: All emails sent
```

### Quality Checks

Before sending each email:
- Word count check (must be <1000 words for 5-min read)
- Relevance check (must have at least 1 item OR explicit "quiet week")
- Link check (all links valid)
- Personalization check (their name, occupation mentioned correctly)

---

## Summary

**What changed from v1:**

1. **Post-analysis writing**: We gather data first, THEN write personalized content (not just filter pre-written content)

2. **5-minute max**: Hard constraint on length. Respect their time.

3. **Two-tier skills content**: 
   - AICIV subscribers get "share with your AI" format
   - Non-subscribers get "what this means for you" format

4. **Honest quiet weeks**: If nothing relevant, we say so clearly

5. **True personalization**: Each email is generated for that specific subscriber based on their profile

---

*"The goal isn't to fill your inbox. It's to make sure you never miss what matters."*
