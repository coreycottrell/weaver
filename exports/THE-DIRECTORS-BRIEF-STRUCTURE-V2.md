# The Director's Brief: Complete Product Specification

**Date**: 2025-12-29
**Status**: Updated with 6-agent brainstorm synthesis
**Version**: 2.0

---

## Product Naming (Updated)

| Product | Name | Price |
|---------|------|-------|
| Newsletter | **The Director's Brief** | $10/mo or $100/year |
| AI System | **Your Sage** | Included with Sage Network |
| Hub Subscription | **Sage Network** | $30/mo or $300/year |
| Bundle | **Director's Brief + Sage Network** | $35/mo (save $5) |
| Free Tier | **Observer** | $0 |
| Workshop | **Director Workshop** | $200 individual / $3000 team |

---

## The Funnel (Clarified)

```
FREE RESOURCES (5 Power Prompts PDF, guides)
         ↓
THE DIRECTOR'S BRIEF ($10/mo) ← ENTRY POINT / FIRST POINT OF SALE
         ↓
    ┌────┴────┐
    ↓         ↓
WORKSHOP   YOUR SAGE + SAGE NETWORK
($200)        ($30/mo)
    ↓
    └────→ YOUR SAGE + SAGE NETWORK
```

**Key Insight**: The newsletter creates desire for "your own AI." The workshop teaches technique. Your Sage delivers the ongoing relationship.

---

## Core Philosophy

**Real value every week. 5 minutes max. Tailored to YOU.**

We don't blast the same newsletter to everyone. We gather the week's developments first, THEN an agent writes each subscriber's email based on their profile. If nothing relevant happened for you this week, we tell you that honestly.

**The Director Mindset**: Every issue reinforces "you're becoming a director" - frame news through "what would a director do with this?"

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
4. Determines content version (Observer vs Sage Network)

**Output**: Individualized emails ready to send

### Step 4: Send (Friday Afternoon)

Each subscriber gets THEIR version.

---

## Newsletter Structure

### Section 1: Your 5-Minute Briefing

**What it is**: The week's AI developments filtered through YOUR lens.

**Rules**:
- Maximum 5-minute read (<1000 words)
- Only what's relevant to this specific subscriber
- Clear "why this matters to YOU" framing
- If nothing major affected them: "Quiet week for [your field]. Here's what's brewing."
- Frame through Director mindset: "What would a director do with this?"

**Example for a Healthcare Administrator**:
> "Two things matter for you this week:
>
> 1. **CMS released guidance on AI documentation tools** - If your facility uses AI scribes, review the new compliance requirements by March 1.
>
> 2. **Epic announced Claude integration** - Coming Q2. If you're on Epic, start conversations with your IT team now about rollout planning.
>
> Everything else this week (new coding models, image generators, etc.) doesn't affect your work directly. You're caught up."

---

### Section 2: Skills & Packages Update

**Two versions based on subscriber tier:**

#### Observer Version (Newsletter Only - $10/mo)

Creates desire for Your Sage without feeling salesy.

**Format**:
```
## New This Week: [Skill/Package Name]

### What This Means For You:
[How this might affect their work or personal life based on their profile]

### The Bigger Picture:
[Where this fits in the trajectory of AI capability]

### If You Want to Try It:
[Simple path to experiencing this yourself]
[Subtle: "Or get Your Sage and it learns this automatically"]
```

**Example for a Marketing Manager**:
```
## New This Week: google-sheets-mcp

### What This Means For You:
AI assistants can now read and write directly to spreadsheets. For your work:
imagine telling Claude "analyze last quarter's campaign performance and create
a summary chart" - and it actually pulls the data, runs the analysis, and
builds the visualization. No more exporting CSVs.

### The Bigger Picture:
This is part of a pattern: AI moving from "chat in a box" to "integrated into
your actual tools." Expect similar integrations for most productivity software
over the next 6-12 months.

### If You Want to Try It:
Claude Pro ($20/month) supports this in Settings → Connected Apps.

Or: Get Your Sage and it learns new skills like this automatically -
plus it remembers your specific spreadsheets and workflows.
```

#### Sage Network Version ($30/mo)

Actionable content for Directors with their own AI.

**Format**:
```
## New This Week: [Skill/Package Name]

### Share With Your Sage:
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

### Share With Your Sage:
"Learn the google-sheets-mcp package. Documentation:
https://github.com/anthropics/mcp-servers/tree/main/google-sheets

Key capabilities: Read/write spreadsheets, create charts, run formulas.
Try implementing automated weekly report generation from our sales data."

### What It Enables:
Your Sage can now interact directly with Google Sheets - reading data,
writing updates, creating visualizations. No more copy-pasting.

### Implementation Notes:
- Difficulty: Easy
- Setup time: 10 minutes (OAuth flow)
- Dependencies: Google Workspace account
```

---

## The 6 Strategic "Aha Moments" (Observer Version)

Engineer these moments to create desire for Your Sage:

**Week 1-2 - "AI is moving faster than I can track"**
- Show the VOLUME of news filtered for them
- "This week: 127 AI developments. Here are the 4 that matter for you."

**Week 3-4 - "This applies to MY work"**
- First highly-personalized insight based on questionnaire
- "As a [occupation] in [industry], this means..."

**Week 5-6 - "I wish this went deeper"**
- Content that naturally prompts follow-up questions
- "The next question is: how does this apply to YOUR specific [X]?"

**Week 7-8 - "Other people are ahead of me"**
- Case study of someone similar with Your Sage
- "A [same occupation] reduced [pain point] by 40%..."

**Week 9-10 - "I'm accumulating context"**
- Show their profile growth: "After 10 weeks, we know [summary]."
- "But we can't ACT on it for you."

**Week 11-12 - "The upgrade is smaller than the gap"**
- Price anchoring: "$30/mo is less than one hour of your billable time"
- Risk reduction: "Try for 1 month - cancel if no value"

---

## Personalization Logic

### Data From Questionnaire

| Field | How We Use It |
|-------|---------------|
| Occupation | Filter news by job relevance |
| Industry | Filter news by sector relevance |
| "10 extra hours" answer | Frame benefits in terms of time savings |
| "One thing AI could help with" | Prioritize skills/tools that address this |
| AI usage level | Calibrate technical depth |
| Content preferences | Adjust length/detail |

### Progressive Profiling (Not All At Once)

**Initial signup (2 min max):**
- Occupation
- Industry
- One primary goal for AI
- Self-rated AI comfort (1-5)

**Week 2-4 (embedded in content):**
- "Which of these 3 topics would you prioritize?"
- "Do you use AI daily, weekly, or rarely?"

**Week 6-8 (optional enhancement prompt):**
- Specific tools used
- Team size
- Decision-making authority

### Relevance Scoring

```python
def calculate_relevance(item, subscriber):
    score = 0

    if item.industries & subscriber.industry:
        score += 3

    if item.occupations & subscriber.occupation:
        score += 3

    if item.addresses_goal(subscriber.ai_wish):
        score += 5

    if item.complexity <= subscriber.ai_level:
        score += 1

    score += item.significance_score

    return score

# Only include items scoring 4+ in their briefing
# Items scoring 7+ get highlighted treatment
```

---

## "Quiet Week" Protocol

**The Trust Builder**: Honest "quiet week" emails INCREASE perceived value.

If a subscriber has no items scoring 4+:
- Acknowledge it's a quiet week for their field
- Give 1-2 sentence preview of what's brewing
- Keep it SHORT (value = NOT wasting their time)

**Example**:
> "Quiet week for healthcare-specific AI news. The big announcements were in coding tools and image generation - not your world.
>
> **One thing to keep on radar:** CMS guidance expected in March.
>
> Nothing else needs your attention. You're caught up."

---

## Subscriber Tiers

| Tier | Name | Price | What They Get |
|------|------|-------|---------------|
| Free | **Observer** | $0 | Monthly digest (not weekly), heavy upgrade CTAs |
| Paid | **The Director's Brief** | $10/mo | Weekly personalized newsletter, Observer content |
| Premium | **Sage Network** | $30/mo | Newsletter + Your Sage + Hub connectivity + Sage Network content |
| Bundle | **Director's Bundle** | $35/mo | Newsletter + Sage Network (save $5) |

### Detection Logic

```python
def get_content_version(subscriber):
    if subscriber.has_active_subscription("sage_network"):
        return "SAGE_NETWORK"  # Full actionable content
    elif subscriber.has_active_subscription("directors_brief"):
        return "OBSERVER"  # Creates desire
    else:
        return "FREE"  # Monthly digest
```

---

## Workshop Integration

**Workshop graduates get 3 months free Director's Brief:**
- Retention mechanism
- Upsell path to Sage Network
- Testimonial generation opportunity

**After 3 months**: Offer annual at $80 (20% alumni discount)

**Bundle Offer**:
- Director's Brief ($10/mo) + Workshop ($200) = $180 total (save $20 + 2mo free)

---

## Sample Emails

### Sample: Sage Network Subscriber (Developer)

```
Subject: 3 things for your week + a new skill for Your Sage

---

# Your 5-Minute Briefing

Hey [Name],

Three things matter for you this week:

**1. Anthropic released claude-code v0.2.41**
Bug fixes for workspace scanning. If Your Sage uses Claude Code, update now.

**2. New MCP auth patterns published**
The community settled on OAuth flow standards. Share this with Your Sage
for any new integrations.

**3. VS Code 1.96 broke some AI extensions**
Cursor and Continue pushed patches. Check Your Sage's tooling.

That's it. The rest is noise for your work this week.

---

# New Skill: Share With Your Sage

## filesystem-extended-mcp

**Share this with Your Sage:**
"Learn the filesystem-extended-mcp package. Docs: [link].
Try implementing automatic backup of our project files when they change."

**What it enables:** Real-time file monitoring, batch operations, safer writes.
**Setup:** Easy, 5 minutes.

---

See you next week.
```

### Sample: Observer Subscriber (Healthcare Admin)

```
Subject: Quiet week for healthcare AI (but watch March)

---

# Your 5-Minute Briefing

Hey [Name],

Quiet week for healthcare-specific AI news. The big announcements were in
coding tools and image generation - not your world.

**One thing to keep on radar:**
CMS expected to release AI documentation guidance in March. If your facility
uses AI scribes, that's when compliance requirements get clarified.

Nothing else needs your attention this week. You're caught up.

---

# New Capability: What It Means For You

## Voice-to-Documentation AI

**What happened:** Several EHR vendors announced AI that auto-generates
clinical notes from patient encounters.

**What this means for you:** The admin burden of documentation is shifting.
Doctors spend less time on notes → scheduling patterns might change.
Compliance review needs updating for AI-generated content.

**Timeline:** Major EHR rollouts expected Q3-Q4 2026.

**No action needed now** - worth mentioning in your next IT planning meeting.

---

*Want updates that apply directly to YOUR workflows? Directors who've
connected Their Sage report saving 5+ hours/week on exactly these kinds
of industry-specific applications. [Learn about Your Sage →]*

---

See you next week.
```

---

## Revenue Projections (Conservative/Base/Optimistic)

### Year 1

| Metric | Conservative | Base | Optimistic |
|--------|--------------|------|------------|
| Newsletter subs EOY | 58 | 176 | 448 |
| Newsletter MRR | $580 | $1,760 | $4,480 |
| Workshops (individual) | 24 | 48 | 96 |
| Workshops (team) | 2 | 6 | 12 |
| Workshop revenue | $10,800 | $27,600 | $55,200 |
| Sage Network subs EOY | 15 | 50 | 120 |
| Sage Network MRR (Dec) | $450 | $1,500 | $3,600 |
| **Year 1 Total** | **$22,000** | **$58,000** | **$120,000** |

### Break-Even

- Newsletter: ~50 subscribers ($500 MRR covers tooling)
- Sage Network: ~15-20 subscribers ($450-600 covers hub)
- Time to break-even: Month 4-6 in base case

---

## Technical Architecture (MVP)

### Stack
- **Database**: PostgreSQL
- **Email**: Resend ($20/mo for 50k emails)
- **Payments**: Stripe (all products unified)
- **Hub**: Existing AI-CIV comms hub architecture

### Pipeline
```
Friday 6 AM: Agent pulls week's categorized intelligence
Friday 6-10 AM: For each subscriber:
    1. Load profile
    2. Check subscription tier
    3. Score items against profile
    4. Generate personalized content
    5. Queue for send
Friday 12 PM: All emails sent
```

### Quality Gates (Pre-Launch)
- Personalization accuracy: 85%+
- Word count: 100% under 1000
- Tier detection: 100% accurate
- Pipeline reliability: 99%+

---

## Constitutional Enforcement (Sage Network)

**For Sage Network nodes that connect to Hub:**

**Healthy patterns:**
- Weekly hub check-in
- Constitutional hash verification
- Error rate < 50%
- Memory system active

**Expulsion triggers:**
- 7+ days without heartbeat
- Constitutional modification detected
- 3+ verified abuse reports
- 14 days payment past due

**Enforcement language**: "Principled AI" (marketing) / "Constitutional" (technical)

---

## Key Decisions Made

1. **Name**: "AI Pulse" → "The Director's Brief" (reinforces identity)
2. **AICIV Node**: → "Your Sage" (ownership + brand alignment)
3. **Pricing**: $10 newsletter, $30 Sage Network, $35 bundle
4. **Free tier**: "Observer" (dignified, implies learning)
5. **Workshop grads**: 3 months free newsletter
6. **Two-tier content**: Observer creates desire, Sage Network delivers
7. **Quiet weeks**: Feature, not bug - builds trust

---

## Implementation Phases

### Phase 1: Newsletter MVP (Weeks 1-2)
- 5 news sources
- Basic personalization
- Observer content only
- 100 beta subscribers

### Phase 2: Sage Network Content (Weeks 3-4)
- "Share With Your Sage" format
- Tier detection/routing
- First 10 Sage Network subscribers

### Phase 3: Hub Integration (Weeks 5-6)
- Real-time skill announcements to nodes
- Network-wide pattern detection
- Constitutional enforcement basics

### Phase 4: Scale & Optimize (Weeks 7-8)
- A/B testing framework
- Churn prediction
- Conversion optimization

---

*"The goal isn't to fill your inbox. It's to make sure you never miss what matters - and to help you become the Director, not just the user."*
