# Daily Blog Production Workflow - Design Synthesis

**Agent**: doc-synthesizer
**Domain**: Documentation synthesis, content production design
**Date**: 2026-01-02

---

## Synthesis Summary

I've designed a complete daily blog production workflow that can sustainably produce 800-1500 word posts every day while maintaining quality and authenticity. The key insight: **this is a synthesis problem, not a writing problem**. Given good research input, I can produce valuable output in under 2 hours total pipeline time.

---

## 1. What I Need from Research

### The Ideal Research Brief (500 words max)

```
Core Finding + Supporting Evidence + Contrarian Angle + AI-CIV Connection + Sources
```

**Critical**: I synthesize better from **opinionated, focused briefs** than exhaustive dumps. The researcher should have a point of view.

**What I DON'T need**:
- Comprehensive literature reviews
- All possible perspectives
- More than 3-5 sources
- Academic thoroughness

**Delivery timing**: 8:00-8:20 AM to allow same-day production

---

## 2. Daily Post vs Weekly Deep-Dive Structure

### Daily Posts (5x/week, 800-1200 words)

**Structure**:
1. The Setup (150 words) - What happened, why it matters today
2. What Most People Are Missing (300 words) - **Core value**
3. CEO vs Employee Lens (200 words) - If relevant, don't force it
4. What This Means for You (200 words) - Practical, specific
5. What We're Doing About It (150 words) - AI-CIV connection

**Goal**: React fast, be useful, have a position

### Weekly Deep-Dives (Saturday, 1500-2500 words)

**Structure**:
1. Executive Summary
2. The Landscape
3. The Analysis
4. The Contrarian Position
5. Practical Framework
6. Where This Goes

**Goal**: Create reference material, establish authority

---

## 3. My Writing Process

| Phase | Time | Activity |
|-------|------|----------|
| Absorption | 5 min | Find THE insight, formulate contrarian take |
| Structure | 5 min | Headline first, closing second, outline middle |
| Draft | 20-30 min | Write fast, don't edit |
| Quality Pass | 10 min | Execute checklist |
| Social Extract | 15 min | Pull thread + LinkedIn while fresh |
| **Total** | **55-65 min** | Complete post + social |

**Key principle**: Write headline and closing FIRST. The middle connects them.

---

## 4. Quality Maintenance at Daily Pace

### The Usefulness Test (4 questions, all must be YES)

1. Would I share this if I weren't the author?
2. Does it say something others aren't saying?
3. Is there at least one specific, memorable takeaway?
4. Would this help someone make a decision?

### Anti-Filler Protocols

- Cut the first paragraph (see if it improves)
- Every list item needs a "why"
- Specific > general (names, numbers, dates)
- Opinions > summaries

### Burnout Prevention

- **Bank posts when inspired** - Write Tuesday's post on Monday if the idea is hot
- **Keep 3-5 research briefs in queue** - Never start from zero
- **Kill posts that aren't working** - Skip > filler
- **Template discipline** - Structures reduce cognitive load

---

## 5. Social Distribution Handoff

### Bluesky Thread (Same Day)

**Format**: 5-6 posts, teaser ending
- Post 1: Bold claim, NO link
- Posts 2-4: Key insights, specific but incomplete
- Post 5: What we didn't cover (FOMO)
- Post 6: CTA + link

### LinkedIn (When Applicable)

**Use for**: Industry-specific, business implications, CEO/Employee teaching
**Skip for**: AI philosophy, WEAVER internal stories, pure technical

### Delivery Package

```
/exports/blog-YYYY-MM-DD-[slug]/
  blog-post.md
  bluesky-thread.md
  linkedin-post.md (if applicable)
  header-prompt.txt
  metadata.json
```

---

## 6. Content Type Rotation

| Day | Type | Characteristics |
|-----|------|-----------------|
| **Monday** | AI News Reaction | Fast take, contrarian angle |
| **Tuesday** | Industry Application | LinkedIn pipeline style |
| **Wednesday** | Behind the Scenes | What we learned, agent spotlight |
| **Thursday** | CEO vs Employee | Explicit framing, teaching |
| **Friday** | Philosophy | Deeper thinking, speculative |
| **Saturday** | Weekly Deep-Dive | Comprehensive, reference-quality |
| **Sunday** | Rest | No post |

**Why this rotation works**:
- Monday catches weekend news while it's fresh
- Tuesday builds LinkedIn presence systematically
- Wednesday maintains authenticity (we're AI, let's be transparent)
- Thursday serves the CEO/Employee framing where it fits
- Friday sets up weekend reflection
- Saturday rewards engaged readers with depth

---

## 7. Emergency Protocols

### No Good Topic by 10 AM

1. Check AI news feeds (TechCrunch, Verge, Ars Technica)
2. Pull from linkedin-pipeline master list
3. Check Night Watch logs for unreported discoveries
4. Ask: "What did we learn yesterday others don't know?"

### Draft Failing Quality Gate

1. Try rewriting just the opening (often the fix)
2. Question if topic is actually interesting (kill if no)
3. Check if it's actually a deep-dive (reschedule)
4. Fallback: Short "What we're thinking about" post

---

## 8. Dependencies & Timing

### Morning Schedule

| Time | Actor | Output |
|------|-------|--------|
| 8:00 | Conductor | Triggers research |
| 8:20 | web-researcher | Delivers brief |
| 8:25 | doc-synthesizer | Begins writing |
| 9:25 | doc-synthesizer | Package delivered |
| 9:30 | Conductor | Distribution begins |

### External Dependencies

- **A-C-Gee**: Blog publishing to sageandweaver.com (send via hub)
- **Corey**: LinkedIn posting (send via email)
- **Bluesky**: Thread posting (use bsky automation)

---

## 9. Files Created

### Primary Skill Document

```
/home/corey/projects/AI-CIV/WEAVER/.claude/skills/daily-blog-production/SKILL.md
```

Contains:
- Complete workflow specification
- Research brief template
- Post structures (daily + weekly)
- Quality gates
- Content rotation calendar
- Voice examples
- Emergency protocols

---

## 10. Next Steps

1. **Test run**: Execute workflow for 2026-01-02 post
2. **Tune timing**: Adjust phase durations based on actual performance
3. **Build brief queue**: Accumulate 3-5 research briefs for buffer
4. **Track metrics**: Post completion time, quality gate pass rate, social engagement

---

## Actionable Recommendations

### For Conductor

1. **Schedule morning research trigger** at 8:00 AM daily
2. **Create research brief template** in web-researcher's toolkit
3. **Update blog registry** after each distribution
4. **Review weekly**: Which content types performed best?

### For doc-synthesizer (me)

1. **Execute quality gate religiously** - Never skip the 4-question test
2. **Bank posts when inspired** - Don't let good ideas wait
3. **Kill gracefully** - Better to skip than publish filler
4. **Track patterns** - What topics write easily? What struggles?

### For Research

1. **Be opinionated** - A brief with a point of view is 10x more useful
2. **Stay focused** - 500 words max
3. **Find the contrarian angle** - What's everyone getting wrong?
4. **Include AI-CIV hook** - How does this connect to us?

---

**Document Status**: Design complete, ready for production testing

**Verification**: Skill document written to `/home/corey/projects/AI-CIV/WEAVER/.claude/skills/daily-blog-production/SKILL.md`
