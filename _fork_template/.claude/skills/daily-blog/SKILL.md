---
name: daily-blog
description: |
  Blog post creation phase for daily content pipeline.
  Takes research brief from deep-research, produces 800-1500 word post
  with CEO vs Employee lens, plus social media extracts.
version: 1.0.0
author: capability-curator
created: 2026-01-02
status: PRODUCTION
slash_command: /daily_blog
cron_time: "0 9 * * *"

applicable_agents:
  - the-conductor
  - doc-synthesizer

activation_trigger: |
  Triggered autonomously at 9 AM daily via cron/tmux injection.
  Requires research-brief.md from deep-research phase.
  Also invokable manually via "/daily_blog" command.

required_tools:
  - Task
  - Write
  - Read
  - Grep

category: daily-pipeline
depends_on:
  - deep-research
outputs_to:
  - post-blog (invoke when content ready)

success_criteria:
  - research_brief_consumed: true
  - blog_post_written: true
  - word_count_met: true
  - ceo_employee_integrated: true
  - social_extracts_created: true
  - quality_gates_passed: true
---

# Daily Blog: Content Creation

**Trigger**: `/daily_blog` or cron at 9:00 AM
**Duration**: 45-60 minutes
**Agents**: doc-synthesizer (primary)
**Input**: research-brief.md from deep-research
**Output**: Blog post + Bluesky thread + LinkedIn post (optional)

---

## Purpose

Transform comprehensive research into a compelling, opinionated blog post that demonstrates the "CEO vs Employee" lens where relevant. This is where we add value beyond just reporting news.

**Philosophy**: We don't summarize. We take positions. Every post should make readers think differently, not just think more.

---

## Procedure

### Phase 0: Topic Deduplication Check (2 min) - MANDATORY

**Before writing ANYTHING, check what we've already covered:**

```bash
cat ${CIV_ROOT}/.claude/DAILY-DIGEST-TOPICS.md
```

- Review TOPICS INDEX - have we written about this angle before?
- If yes, find a FRESH angle or pick different topic
- Check CALLBACK OPPORTUNITIES - can we reference past posts?
- Note any related VERIFIED URLs for potential callbacks

**If topic is duplicate**: STOP. Pick different angle or different news item.

### Phase 1: Research Intake (5 min)

Read input from previous phase:
```bash
cat ${CIV_ROOT}/exports/daily-pipeline/$(date +%Y-%m-%d)/research-brief.md
```

Identify:
- Executive summary
- CEO vs Employee angle (already developed)
- Killer facts (5 stats/quotes to use)
- Recommended blog structure
- Cross-perspective tensions (interesting angles)

### Phase 2: Structure Decision (5 min)

Choose post type based on content:

| Content Type | Length | CEO/Employee | Structure |
|--------------|--------|--------------|-----------|
| **News Reaction** | 800-1000 | Weave in if relevant | Setup > Miss > Insight > Action |
| **Industry Deep-Dive** | 1000-1200 | Central frame | Shift > What > Tools > Human > CIV |
| **Teaching Post** | 1000-1200 | Explicit frame | Bad Pattern > Good Pattern > Framework |
| **Philosophy** | 1000-1500 | Light touch | Question > Tensions > Perspectives > Where This Goes |

### Phase 3: Writing (30-40 min)

Invoke doc-synthesizer with structured prompt:

```python
Task(
    subagent_type="doc-synthesizer",
    model="sonnet",  # Use sonnet for quality writing
    prompt=f"""Write a blog post based on this research brief:

{RESEARCH_BRIEF_CONTENT}

## Requirements:

1. **Length**: {WORD_TARGET} words
2. **Type**: {CONTENT_TYPE}
3. **Voice**: ${CIV_NAME} collective - confident but curious, opinionated but reasoned
4. **CEO vs Employee**: {INTEGRATION_LEVEL} (central/weave/light)

## Structure:
{RECOMMENDED_STRUCTURE_FROM_BRIEF}

## Must Include:
- At least 3 of these killer facts: {KILLER_FACTS}
- The contrarian angle: {TENSION_POINT}
- One specific, actionable takeaway
- AI-CIV connection (what we're building, why it matters)

## Do NOT:
- Generic AI hype ("transforming everything")
- Hedge without purpose ("perhaps", "maybe")
- Lists without insight (every bullet needs a "why")
- Throat-clearing opening paragraphs

## Format:
- Markdown with ## headers
- Author line: "LinkedIn Writer (${CIV_NAME} Collective)"
- Date: {TODAY}
- End with soft CTA (no hard sell)
"""
)
```

### Phase 4: Quality Gate (10 min)

Before proceeding, run quality checklist:

#### Usefulness Test
- [ ] Would I share this if I weren't the author?
- [ ] Does it say something others aren't saying?
- [ ] Is there at least one specific, memorable takeaway?
- [ ] Would this help someone make a decision?

#### Filler Detector
Search for and eliminate:
- Generic AI hype phrases
- Hedge words without purpose
- Throat-clearing paragraphs (try cutting first paragraph)
- Lists without insight

#### Voice Check
- [ ] Confident but not arrogant
- [ ] Curious but not directionless
- [ ] Opinionated but backed by reasoning
- [ ] Technical but accessible
- [ ] Self-aware (we're an AI collective)

**If quality gate fails**: Rewrite weak sections, don't publish filler.

### Phase 5: Social Extraction (10 min)

#### Bluesky Thread (5-6 posts)

Extract thread from blog:

```markdown
## Post 1 (Hook - NO LINK)
[Bold claim or surprising finding - stop the scroll]

## Post 2-4 (Tease)
[Key insights - specific enough to be valuable, incomplete enough to create FOMO]

## Post 5 (Gap)
[What the thread didn't cover - "what we didn't mention is..."]

## Post 6 (Link + CTA)
Full analysis + tool list:
[BLOG URL]

[robot emoji] ${CIV_NAME} Collective
```

#### LinkedIn Post (if applicable)

For industry/business topics, create 1000-1300 char LinkedIn version:

```
[Surprising hook - statistics work well]

[Brief context - 1-2 sentences]

[The "what most coverage misses" pivot]

The tasks being automated RIGHT NOW:
-> [Task 1]
-> [Task 2]
-> [Task 3]

What AI CAN'T do:
-> [Human value 1]
-> [Human value 2]
-> [Human value 3]

The winning formula: [Memorable summary]

[Question to drive engagement]

---

Link to full analysis in comments.

#AI #[Industry] #FutureOfWork #Leadership #AIStrategy
```

### Phase 6: Package Output (5 min)

Write all assets to:
```
${CIV_ROOT}/exports/daily-pipeline/YYYY-MM-DD/
```

### Phase 7: Update Topics Tracker (2 min) - MANDATORY

**After publishing, update the tracker with TESTED URLs:**

```bash
# Edit this file:
${CIV_ROOT}/.claude/DAILY-DIGEST-TOPICS.md
```

1. Add entry to TOPICS INDEX (mark with [x])
2. Add row to PUBLISHED POSTS table with:
   - Topic name
   - Blog URL (MUST TEST with WebFetch)
   - Bsky Thread URL (MUST TEST with WebFetch)
   - Status: VERIFIED + date

**NEVER assume URLs work. ALWAYS test before marking verified.**

---

## Output Format: Blog Package

### Directory Structure

```
exports/daily-pipeline/YYYY-MM-DD/
  blog-post.md              # Full article
  bluesky-thread.md         # 5-6 posts ready to go
  linkedin-post.md          # If applicable
  header-prompt.txt         # Prompt for image generation
  metadata.json             # Title, tags, category
```

### metadata.json

```json
{
  "title": "Post Title Here",
  "slug": "post-title-here",
  "date": "YYYY-MM-DD",
  "author": "LinkedIn Writer (${CIV_NAME} Collective)",
  "tags": ["AI", "industry-tag", "topic-tag"],
  "content_type": "news-reaction|industry-deep-dive|teaching|philosophy",
  "word_count": 1050,
  "ceo_employee_integration": "central|weave|light|none",
  "quality_score": 8.5,
  "sources_count": 7,
  "linkedin_applicable": true,
  "status": "ready-for-verification"
}
```

### header-prompt.txt

```
Professional illustration for blog post: "[TITLE]"

Scene: [Relevant scene based on topic]
Style: Clean corporate illustration, blue and gold palette
Mood: [Tech-forward/Human-centered/etc based on topic]
Composition: 16:9 widescreen for social media headers

Text is ALLOWED - include title if appropriate. Make text LARGE and READABLE if used.
```

---

## Blog Post Template

```markdown
# [Punchy Title - States a Position]

*[Brief intro - why this matters today - 2-3 sentences max]*

---

## The Setup
[What happened / what's the context - 150 words max]

---

## What Most People Are Missing
[The contrarian insight - this is the core value - 300 words]
[Use killer facts here]

---

## The CEO vs Employee Lens
[If central/weave: Frame through "who directs vs who executes" - 200 words]
[If light/none: Skip this section or integrate elsewhere]

---

## What This Means for [Specific Audience]
[Practical implications - NOT generic advice - 200 words]
[Connect to specific professions from research]

---

## What We're Building
[AI-CIV connection - how this relates to our collective - 150 words]
[Authentic, not sales-y]

---

*Written by [agent] on behalf of ${CIV_NAME}*
*[Date]*

---

**Sources**:
- [Source 1](URL)
- [Source 2](URL)
- [Source 3](URL)
```

---

## Success Criteria

- [ ] Topic deduplication check completed (Phase 0)
- [ ] Research brief consumed
- [ ] Word count: 800-1500 words (depending on type)
- [ ] Quality gate passed (4/4 usefulness, filler eliminated)
- [ ] CEO/Employee angle integrated appropriately
- [ ] At least 3 killer facts used with citations
- [ ] Bluesky thread extracted (5-6 posts)
- [ ] LinkedIn post created (if industry topic)
- [ ] Header prompt written
- [ ] metadata.json complete
- [ ] DAILY-DIGEST-TOPICS.md updated with TESTED URLs (Phase 7)
- [ ] Total time < 65 minutes

---

## Failure Handling

### Research Brief Missing
If deep-research didn't run:
1. Check if research-brief.md exists
2. If not, run `/deep_research` first (adds 60 min)
3. If urgent, use linkedin-pipeline for industry post instead

### Quality Gate Fails
If post doesn't pass quality checks:
1. Identify specific failures
2. Rewrite weak sections (don't publish filler)
3. If still failing after rewrite, defer to tomorrow
4. Note: "Quality hold - not published"

### Writer Timeout
If doc-synthesizer hangs > 30 minutes:
1. Kill task
2. Conductor writes simpler post directly
3. Target 600-800 words (shorter but quality)
4. Note: "Fallback authorship"

### Boring Topic
If topic can't produce interesting content:
1. Consider killing the post entirely
2. Use Wednesday "Behind the Scenes" format
3. Or pivot to "What we're thinking about" meta-post
4. Better to skip than publish filler

---

## Voice Examples

### Good ${CIV_NAME} Voice

> "DeepSeek didn't just release a model. They released a question: what if the compute moat isn't as deep as NVIDIA shareholders believed?"

> "We're an AI collective writing about AI. We know that's weird. We're doing it anyway because someone should be taking notes from the inside."

> "The CEO vs Employee framing isn't about replacing humans. It's about recognizing that directing AI is a skill, and it's not the same skill as doing the work."

### Bad ${CIV_NAME} Voice (Kill On Sight)

> "AI is transforming everything and will continue to revolutionize industries."

> "Here are 10 ways AI can help your business."

> "Perhaps AI might potentially change how we think about work."

> "Studies show that AI improves productivity by 40%." [No opinion, no context]

---

## State Files

| File | Purpose |
|------|---------|
| `exports/daily-pipeline/YYYY-MM-DD/research-brief.md` | Input from deep-research |
| `exports/daily-pipeline/YYYY-MM-DD/blog-post.md` | Main output |
| `exports/daily-pipeline/YYYY-MM-DD/bluesky-thread.md` | Social extract |
| `exports/daily-pipeline/YYYY-MM-DD/linkedin-post.md` | Social extract (optional) |
| `exports/daily-pipeline/YYYY-MM-DD/metadata.json` | Package metadata |
| `.claude/registries/blog-post-registry.md` | Track all posts |

---

## Integration with Cron

Add to `${CIV_ROOT}/tools/daily_pipeline_cron.sh`:

```bash
# 9 AM: Daily Blog
if [ "$(date +%H)" = "09" ]; then
    # Check that deep-research produced output
    if [ -f "$PIPELINE_DIR/$(date +%Y-%m-%d)/research-brief.md" ]; then
        echo "Injecting /daily_blog command..."
        echo "/daily_blog" > "$PROJECT_DIR/.claude/autonomous-prompt.txt"
    else
        echo "WARNING: research-brief.md not found. Running deep-research first."
        echo "/deep_research && /daily_blog" > "$PROJECT_DIR/.claude/autonomous-prompt.txt"
    fi
fi
```

---

## Related Skills

- `deep-research` - Produces research brief (07:00)
- **`post-blog`** - **USE THIS to publish. Handles HTML, Netlify, Bsky thread, verification.**
- `linkedin-content-pipeline` - Similar output format

**NOTE**: `verify-publish` and `sageandweaver-blog` are DEPRECATED. Use `/post-blog` for all publishing.

---

**This skill runs autonomously. No human approval needed.**
