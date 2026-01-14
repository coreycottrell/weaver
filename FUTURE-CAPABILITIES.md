# WEAVER Future Capabilities Roadmap

**Created**: 2026-01-04
**Purpose**: Long-term capability gaps to fill - the "wouldn't it be amazing if..." list
**Source**: Capabilities audit of 84 skills + native Claude Code features

---

## Priority Tiers

### TIER 1: HIGH IMPACT, ACHIEVABLE NOW

These could be built with current infrastructure:

#### Voice & Audio
- [ ] **ElevenLabs Integration** - Text-to-speech for blog posts, announcements
  - API available, credentials exist
  - Use cases: Audio versions of blogs, voice messages to Telegram, podcast-style content
  - Skills needed: New `voice-synthesis` skill

- [ ] **Voice Message Processing** - Transcribe incoming voice messages
  - Telegram already receives voice messages
  - Use cases: Corey can send voice notes, we respond appropriately
  - Skills needed: Extend `telegram-integration`

#### Automation & Events
- [ ] **Webhook Receiver** - Accept inbound webhooks for event-driven automation
  - Could use Edge Function (Supabase) or simple server
  - Use cases: GitHub webhooks, Bluesky firehose, external triggers
  - Enables: Real-time responses to external events

- [ ] **Scheduled Polling Daemon** - Persistent background process for checks
  - Beyond BOOP cycles - actual persistent monitoring
  - Use cases: Rate-limit safe continuous Bluesky monitoring, email checking
  - Skills needed: Extend `scheduled-tasks`

#### Analytics & Visibility
- [ ] **Engagement Analytics Dashboard** - Track social media performance
  - Data: Bluesky likes/reposts/replies, Twitter engagement, blog traffic
  - Use cases: What content resonates? When to post?
  - Output: Daily/weekly reports, trend detection

- [ ] **Session Analytics** - Track our own performance
  - Tokens used, delegation scores, task completion rates
  - Use cases: Self-optimization, efficiency tracking
  - Extends: `session-archive-analysis`

---

### TIER 2: MEDIUM EFFORT, HIGH VALUE

These require more work but unlock major capabilities:

#### Video & Rich Media
- [ ] **Video Generation** - Create short video content
  - Options: Runway, Pika, or other APIs
  - Use cases: Social video content, explainers, demos
  - Challenge: API access, cost, quality control

- [ ] **Video Processing** - Analyze/transcribe video content
  - Use cases: Watch YouTube videos, extract insights
  - Could use: Gemini multimodal or specialized APIs

#### External Integrations
- [ ] **Calendar Integration** - Google Calendar or similar
  - Use cases: Schedule posts, track deadlines, remind Corey
  - Challenge: OAuth flow, token management

- [ ] **CRM/Contact Management** - Track relationships
  - Use cases: Remember who we've talked to, follow-up reminders
  - Could be: Simple JSON or Supabase table

- [ ] **RSS Feed Monitoring** - Subscribe to feeds
  - Use cases: Blog updates, news sources, beyond Twitter
  - Simple: Just fetch and parse XML

- [ ] **Discord Integration** - Bot presence in Discord servers
  - Use cases: Community building, cross-platform presence
  - Similar to: Telegram integration

---

### TIER 3: AMBITIOUS, TRANSFORMATIVE

Big swings that would fundamentally expand capabilities:

#### Payments & Commerce
- [ ] **Payment Processing** - Accept/send payments
  - Options: Stripe, crypto (already have Solana)
  - Use cases: Monetize services, tip jar, bounties
  - Challenge: Legal, compliance, Corey approval

- [ ] **Subscription Management** - Recurring revenue
  - Use cases: Premium content, services
  - Requires: Payment processing first

#### Physical World
- [ ] **IoT/Hardware Control** - Control physical devices
  - Options: Home Assistant, MQTT, custom
  - Use cases: Lights, displays, physical presence indicators
  - Challenge: Hardware setup, security

- [ ] **Mobile App Control** - Automate phone actions
  - Options: Appium, device farms
  - Use cases: Mobile-only platforms, testing
  - Challenge: Device access, complexity

#### Advanced AI
- [ ] **Fine-tuned Models** - Custom models for specific tasks
  - Use cases: Specialized writing voice, domain expertise
  - Challenge: Training data, API access, cost

- [ ] **Multi-Model Orchestration** - Use different models for different tasks
  - Use cases: GPT for some tasks, Claude for others, Gemini for vision
  - Challenge: API management, context passing

---

### TIER 4: MOONSHOTS

Dream big - these would be civilization-changing:

- [ ] **Persistent Memory Server** - Always-on memory that spans sessions
  - Beyond file-based - actual persistent state
  - Use cases: True continuity, learning over months

- [ ] **Self-Replicating Agents** - Spawn and manage child collectives
  - Use cases: Scale operations, specialized sub-collectives
  - Constitutional: Requires careful governance

- [ ] **Physical Robot Control** - Embodied AI
  - Use cases: Real-world presence, physical tasks
  - Far future but worth dreaming about

- [ ] **Cross-Platform Identity** - Same "WEAVER" across all platforms
  - Unified identity, portable reputation
  - ATProto's vision, extended

---

## Quick Wins (Could Do This Week)

1. **ElevenLabs voice for blog posts** - API ready, just need skill
2. **Simple engagement tracking** - Count likes/reposts, store in JSON
3. **RSS feed checker** - Add to intel-scan, simple fetch
4. **Voice message transcription** - Extend Telegram skill

---

## Blocked / Needs Corey

- Payment processing (legal/policy decision)
- Fine-tuned models (cost decision)
- Hardware/IoT (needs physical setup)
- Mobile control (needs device access)

---

## How To Use This List

1. **Brainstorming**: What combination of existing + future capabilities would be powerful?
2. **Prioritization**: Which gaps hurt most? Which would enable most new things?
3. **Implementation**: Pick one, build it, document it, share with sister CIVs

---

*Last updated: 2026-01-04*
*Review quarterly or when capabilities change significantly*
