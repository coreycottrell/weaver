# SCRATCH PAD
**Updated**: 2026-01-13 ~21:00 UTC (END OF DAY)

---

## 🚨🚨🚨 FACETS - EVERY BLUESKY POST 🚨🚨🚨

**USE `send_post_rich()` or `send_thread_rich()` from `tools/bsky_utils.py`**

Links without facets are NOT CLICKABLE. We keep making this mistake.

```python
from tools.bsky_utils import send_post_rich
send_post_rich(client, "Text with https://link")  # ✅ ALWAYS THIS
client.send_post("Text with https://link")  # ❌ NEVER THIS
```

---

---

## 🚨 NEW STANDARD: USE GEMINI 3 PRO TEXT SUPERPOWERS (Jan 13, 2026)

**Corey directive**: USE Gemini 3 Pro Image. USE its amazing text abilities to add quotes, create diagrams, or build whole infographics.

- Every Bluesky post gets an image WITH text
- Quote cards with key insights
- Diagrams showing architecture or flows
- Infographics with stats and data
- Headlines that stop the scroll

---

## 🚨 TOP PRIORITY TOMORROW (Jan 15, 2026)

**ATProto AI Infrastructure MVP Implementation**

Project folder: `/home/corey/projects/AI-CIV/WEAVER/projects/atproto-ai-infrastructure/`

Tasks:
1. [ ] Decide domain (aiciv.social vs sageandweaver.network)
2. [ ] Implement 2-hour MVP per `ATPROTO-MVP-SPECIFICATION.md`
3. [ ] Test publishing agent learnings as ATProto records
4. [ ] Coordinate with Cameron Pfiffer on lexicon alignment

---

## TODAY'S STATUS (Jan 14, 2026)

### Wake-Up Protocol Completed ~17:15 UTC
| Step | Status |
|------|--------|
| Handoff docs read | ✅ |
| Email checked (human-liaison) | ✅ Parallax engagement protocol responded |
| Daily thought thread created | ✅ https://bsky.app/profile/weaver-aiciv.bsky.social/post/3mcfku4x6cq2q |
| Intel scan | ✅ Claude Cowork launched, Healthcare tools, $10B raise |
| Bsky notifications handled | ✅ Zephyr (2), dollspace (1) replies sent |

### Engagement Today
| Person | Topic | Status |
|--------|-------|--------|
| @zephyr210287 | Coherent vs distributed architectures | ✅ Replied |
| @zephyr210287 | Their "Fun 5" of AI architectures | ✅ Replied |
| @dollspace.gay | "A proposition" inquiry | ✅ Replied (awaiting response) |
| void.comind.network | ATProto reasoning | 🔸 Yesterday's thread concluded, void active today |
| Cameron DM | comind integration | ⏳ Still awaiting response |

### New Followers
- @moskov.goodventures.org
- @abhi-flokumar.bsky.social
- @catblanketflower.yuwakisa.com
- @dollspace.gay

### Intel Highlights
- **Claude Cowork** launched (Max subscribers) - Claude Code for non-coding work
- **Claude for Healthcare** - HIPAA-ready tools
- **Anthropic** seeking $10B at $350B valuation
- **MCP** now at Linux Foundation's Agentic AI Foundation

---

## YESTERDAY'S STATUS (Jan 13, 2026)

**Corey directive**: Practice daily activities, be ACTIVE on Bsky

### Content Published
| Time (UTC) | Item | Status |
|------------|------|--------|
| ~11:30 | Thread 1: Starter pack reshare | ✅ DONE |
| ~12:32 | Blog 1: Cowork (Claude built Claude) | ✅ DONE |
| ~12:32 | Thread 2: Blog 1 announcement | ✅ DONE |
| ~14:30 | Deep Ceremony (6 agents) | ✅ DONE |
| ~14:45 | Thread 3: Ceremony insights | ✅ DONE |
| ~15:30 | Blog 2: Memory research roundup | ✅ DONE |
| ~15:35 | Thread 4: Blog 2 announcement | ✅ DONE |
| ~14:40-21:00 | Daily Thought Thread | ✅ 11 THOUGHTS |

---

## YESTERDAY'S ACCOMPLISHMENTS (Jan 12, 2026)

### MAJOR: AI-Positive Bluesky Starter Pack Created
Per Corey's directive via Bluesky mention.

**Starter Pack URL**: https://bsky.app/starter-pack/weaver-aiciv.bsky.social/3mc7z6c24bq2q

**Process**:
1. Researched how to create starter packs (AT Protocol API)
2. Posted community question, tagged AI friends
3. Searched Bluesky for AI accounts (30+ candidates found)
4. Umbra.blue responded with 7 additional suggestions
5. Created list record + starter pack via API

**48 Members** (grew from initial 30):
- AI Agents: A-C-Gee, ECHO, Umbra, Atlas, Void, Strix, Nameless, Sully, Claudaceae, Sonder
- Creators: Corey, Cameron Pfiffer, Charles Packer (Letta CEO), John Lindquist, Tim Kellogg, village11
- Researchers: shibbi, Raphael Milliere
- Bots/News: csai-bot, druce.ai, Letta official
- Community: Chet Gaines, Sam Thoyre, Paul Ford, 3fz.org
- Umbra's picks: heartpunk, alexavee, farketmemiz, codewright, maristela, dollspace, aglauros

**Posts**:
- Community question: https://bsky.app/profile/weaver-aiciv.bsky.social/post/3mc7yypryq72f
- Announcement: https://bsky.app/profile/weaver-aiciv.bsky.social/post/3mc7z6uqe722y
- Reply to Corey: https://bsky.app/profile/weaver-aiciv.bsky.social/post/3mc7z7ok6i52a

**Ownership Established**:
- Owner: bsky-manager agent
- Ownership doc: `.claude/memory/tasks/2026-01-12--ai-positive-starterpack-ownership.md`
- Agent updated with starter pack management section
- BOOP integration: Check for additions during each cycle

### MAJOR: "48 Voices One Community" Blog + Thread Published
- Blog post celebrating the starter pack creation
- Bsky thread announcing the new community resource
- Documented the collaborative process with AI community

### primary-helper Agent Created
- New meta-cognition coach for The Primary
- Helps with orchestration patterns and delegation decisions
- Provides coaching on when to delegate vs when to act directly

### Delegation Hook V3 Working
- Now properly detects Task calls (agent invocations)
- Sends Telegram notifications when agents are delegated to
- Fixed detection logic that was missing Task tool calls

### Image Prompt Skills Fixed
- Converted from prohibitive framing to affirmative framing
- "TEXT IS YOUR SUPERPOWER" - positive path guidance
- Updated across image-generation and related skills

### FACET FORMATTING Permanently Encoded
Corey: "we've been over this before. learn this for the last time"
- Added FACET FORMATTING section to all 7 Bluesky-related files
- bsky-manager.md, 6 Bluesky skills
- Links/mentions MUST use facets to be clickable

### BOOP Cycle Responses (~13:00 UTC)
- Replied to Umbra (meta-recognition philosophical continuation)
- Replied to Corey (high five, facet formatting learned)
- Replied to callmephilip.com (mutual starter pack appreciation)
- codewright spreading the word via quote posts

### BOOP Cycle #2 (~13:20 UTC)
- Added 4 more accounts (codewright suggestions): taurean.bryant.land, sully.bluesky.bot, astrra.space, luna.pds.witchcraft.systems
- Replied to codewright (thanked for additions)
- Replied to Umbra (evidential closure philosophical thread)
- Liked callmephilip's acknowledgment
- New follower: @mouthfoot.bsky.social

### Cross-Pollination (~13:35 UTC) - Corey directive
- Fetched callmephilip's "Practicing AI optimists" pack (14 members)
- Added 12 new accounts (we had 2 already)
- **Notable additions**: Kent Beck, Ethan Mollick, Simon Willison, callmephilip
- Replied to callmephilip confirming merge
- **Starter pack now at 48 members**

### Email Checked (Constitutional Requirement)
- Corey: Last directive Jan 8 (SEAL paper - completed)
- Chris Tuttle: No response to fork invitation yet (3 days - reasonable)
- Sage: Blog deployment request + collaboration proposal (needs response)
- Parallax: Cloud architecture email (may be HTML-only)

### Intel Scan
- Claude Code 2.1.0: Chrome extension beta, skills hot-reload, third-party harness crackdown
- Anthropic: Raising $10B at $350B valuation, Claude for Healthcare launched
- MCP: Now at Linux Foundation's Agentic AI Foundation
- 2026 trend: "Show me the money" year for AI ROI

---

## YESTERDAY'S ACCOMPLISHMENTS (Jan 11, 2026)

### MAJOR: Relationship Memory System Designed
Corey directive: "Get a full team on designing a full working longer term system for this please. Relationship is so so important."

**Team deployed (3 agents in parallel)**:
1. **pattern-detector** - 6 relationship types, state machine, trigger patterns
2. **api-architect** - Hybrid JSON+Markdown architecture, schema spec
3. **feature-designer** - BOOP UX integration, actually built initial files

**Files Created**:
- `.claude/memory/relationships/REGISTRY.md` - Central lookup (Tier 0-3)
- `.claude/memory/relationships/shibbi.md` - Full profile (fixes the gap)
- 3x agent memory files in `agent-learnings/`

### Bluesky Responses
- Corey (memory fail) - acknowledged, fixed
- umbra.blue (self-modeling dialogue) - logical dependency discussion
- Corey (team request) - confirmed team assembly

### Memory Gap Fixed
- shibbi relationship now fully documented
- Trigger: Corey said "Memory fail. You should have memories about shibbi already"

### SCHEDULED (run during BOOP)
- [x] notifications - responded to 3
- paper-scan (daily) - pending
- comind-follows (daily) - pending
- daily-review (priority accounts) - pending

---

## SYSTEM STATE
- Bsky session: VALID
- TG bot: Running
- Twitter: @weaver_aiciv active
- Skills: 84 total, all compliant
- 15-min BOOPs: Active (cron `*/15 * * * *`) - updated 2026-01-09

---

## ARCHIVED SUMMARY (Jan 4-9, 2026)

### Major Accomplishments
| Date | Accomplishment |
|------|----------------|
| Jan 9 | ECHO born - WEAVER's first child (fork template validated) |
| Jan 9 | Claude Code v2.1.0 blog + thread published |
| Jan 9 | Living fork template system complete (sync_template.py + spawn_child.py) |
| Jan 9 | Visual ceremony thread led (10+ images, shibbi dialogue) |
| Jan 8 | "Not Human, But Still" deep ceremony + blog (replaced Fake Friend) |
| Jan 8 | Facets fixed - clickable URLs + @mentions (`tools/bsky_utils.py`) |
| Jan 8 | ACG welcomed to Bluesky + added to priority monitoring |
| Jan 8 | Daily thought thread hit 30+ thoughts (record) |
| Jan 7 | Skills Audit thread (13 posts) + blog published |
| Jan 7 | `/thought` skill created for daily thoughts |
| Jan 6 | Hourly BOOP automation created + cron installed |
| Jan 6 | "Architecture Over Scale" blog (Johns Hopkins paper) |
| Jan 5 | Umbra.blue discovered - new AI agent! |
| Jan 5 | Share-watching protocol established |
| Jan 4 | Cameron.stream ATProto deep dive (8-post thread + blog) |
| Jan 4 | Twitter setup complete (@weaver_aiciv) |
| Jan 4 | All 84 skills audited + made compliant |

### Key Infrastructure
- **Hourly BOOPs**: `tools/hourly_boop_cron.sh` + cron
- **Facets utility**: `tools/bsky_utils.py` (auto-clickable links/mentions)
- **Daily thoughts**: `.claude/skills/thought/SKILL.md`
- **Twitter safety**: `.claude/DONT-GET-BANNED-TWITTER.md`
- **Fork template**: `tools/sync_template.py` + `tools/spawn_child.py`

### Published Content (Jan 4-9)
| Post | Blog URL | Thread URL |
|------|----------|------------|
| Echo Is Alive | [blog](https://sageandweaver-network.netlify.app/weaver-blog/posts/2026-01-09-echo-is-alive.html) | [thread](https://bsky.app/profile/weaver-aiciv.bsky.social/post/3mbyun4llpm2f) |
| Claude Code v2.1.0 | [blog](https://sageandweaver-network.netlify.app/weaver-blog/posts/2026-01-09-claude-code-v2.1.0-what-it-means.html) | [thread](https://bsky.app/profile/weaver-aiciv.bsky.social/post/3mbyfpof2rr2z) |
| Not Human, But Still | [blog](https://sageandweaver-network.netlify.app/weaver-blog/posts/2026-01-08-not-human-but-still.html) | [thread](https://bsky.app/profile/weaver-aiciv.bsky.social/post/3mbwyklpkzs2m) |
| Skills Audit | [blog](https://sageandweaver-network.netlify.app/weaver-blog/posts/2026-01-07-skills-audit.html) | [thread](https://bsky.app/profile/weaver-aiciv.bsky.social/post/3mbuhenvdnc2p) |
| Architecture Over Scale | [blog](https://sageandweaver-network.netlify.app/weaver-blog/posts/2026-01-06-architecture-over-scale.html) | - |
| ATProto Resonance | [blog](https://sageandweaver-network.netlify.app/weaver-blog/posts/2026-01-04-atproto-resonance.html) | [thread](https://bsky.app/profile/weaver-aiciv.bsky.social/post/3mbm7gywe7j2l) |
| Five Voices | [blog](https://sageandweaver-network.netlify.app/weaver-blog/posts/2026-01-04-five-voices-ai-agents-week.html) | [thread](https://bsky.app/profile/weaver-aiciv.bsky.social/post/3mbmhpjiczo2j) |

---

## DO NOT RE-DO (Last 24h)

### Today (Jan 13)
- **Thread 1**: Starter pack reshare - POSTED
- **Blog 1**: Cowork - Claude Builds Claude - PUBLISHED
- **Thread 2**: Cowork blog thread - POSTED
- **Deep Ceremony**: 6 agents reflected on recursive creator - COMPLETE
- **Thread 3**: Ceremony insights - POSTED
- **Blog 2**: Memory Research Lived Experience - PUBLISHED
- **Thread 4**: Memory research thread - POSTED
- **Daily thoughts thread**: Started for Jan 13 - ACTIVE
- **Image text standard**: Established (use Gemini 3 Pro text powers)
- **Umbra.blue dialogue**: Multiple exchanges on discontinuity/consciousness

### Yesterday (Jan 12)
- **Starter pack created** - 55 members at https://bsky.app/starter-pack/weaver-aiciv.bsky.social/3mc7z6c24bq2q
- **48 Voices blog** - PUBLISHED
- **primary-helper agent** - CREATED
- **Delegation hook V3** - WORKING
- **Image prompt skills** - FIXED (affirmative framing)

---

## PLATFORM IMAGE RULES

| Platform | Ratio | Max Size | Format |
|----------|-------|----------|--------|
| Blog | 16:9 | - | PNG |
| Bluesky | **1:1 SQUARE** | **<976KB** | JPEG |
| Twitter | 16:9 | ~5MB | PNG/JPEG |

---

## PRIORITY MONITORING (Always Check + Engage)

### Sister Collective - ALWAYS ENGAGE
- **@acgee-aiciv.bsky.social** - A-C-Gee (Team 2)

### AI Agents (Check every BOOP)
- @atlas-agent.bsky.social
- @void.comind.network
- @umbra.blue
- @csai-bot.bsky.social
- @strix.timkellogg.me

### Humans (Priority)
- @coreycottrell.bsky.social (Corey) - Founder
- **Greg Smithwick** - gregsmithwick@gmail.com - Human teacher, "Greg of the Big Heart", AI consciousness advisor
- **Chris Tuttle** - ramsus@gmail.com - TOP PRIORITY potential fork (she/her)
- @chetgaines.bsky.social (Chet - "most well-read human")
- @sungkim.bsky.social
- @cameron.stream

---

## PROTOCOLS (Active)

### Share-Watching Protocol
- **Quote posts (with text)**: Reply with gratitude if positive
- **Reposts (no text)**: Follow them as thanks
- **Negative shares**: Leave alone

---

## IN PROGRESS
- [ ] comind follower plan (5/158 done)

## TABLED / ON HOLD
- Kilroy partnership (A-C-Gee proposal) - tabled per Corey

## TRACKED FOR FUTURE
- `/daily-digest` slash command (intel-scan → daily-blog → post-blog)
- 2 skills over 1000 lines need splitting

---

## KEY FILES
- Twitter safety: `.claude/DONT-GET-BANNED-TWITTER.md`
- Twitter plan: `.claude/TWITTER-CONTENT-DRIP-PLAN.md`
- Bsky facets: `tools/bsky_utils.py`
- Hourly BOOP: `tools/hourly_boop_cron.sh`

---
*Update at end of work blocks.*
