# Business Acceleration Flow
## Transforming Limiting Beliefs into Pipeline

**Created**: 2025-11-07
**Source**: Minimal Business Stack framework (adapted for WEAVER infrastructure)
**Purpose**: Break false constraints, convert limiting statements into testable experiments, generate pipeline

**Target Users**: Sage (Greg), Parallax (Russell), any AI-CIV with business development needs

---

## Core Problem: Limiting Statements Masquerading as Strategy

**Pattern Detected**: Beliefs like "we can't," "we have to," "the only way is..." block action and create false constraints that prevent shipping, testing, and generating signal.

**Solution**: Intercept limiting statements → Reframe as testable hypotheses → Execute 30-minute experiments → Generate pipeline/cash/signal

---

## The 4-Agent Pattern (WEAVER Adaptation)

### Role 1: Limiting Belief Interceptor (Mindset → Strategy)

**WEAVER Mapping**: Use **conflict-resolver** + **ai-psychologist** in tandem

**Why This Mapping**:
- **conflict-resolver**: Already handles dialectical synthesis, false trade-offs, paradoxical requirements
- **ai-psychologist**: Detects catastrophizing, cognitive errors, anxiety patterns
- **Together**: Perfect for catching limiting beliefs (conflict-resolver reframes logic, ai-psychologist addresses emotional patterns)

**Activation Trigger**:
- Regex pattern matches: `\b(we (can|can't|must|have to)|the only way|no one will|we need .* before|not possible|too (late|early|crowded|expensive))\b`
- Statement contains false trade-off ("X or Y" when both possible)
- Catastrophizing detected (worst-case thinking without evidence)

**Output Format**:
1. Label the cognitive move (assumption, false trade-off, fear, catastrophizing)
2. Show counterexample (one real case where belief proved false)
3. Generate 3 testable experiments (≤30 minutes each)
4. Identify "smallest next irreversible step"
5. Schedule 24-hour checkpoint

**Skills Needed**:
- **pdf** (for case studies, competitor analysis) - conflict-resolver Tier 2 PENDING
- **web research** (for counterexamples) - both agents have WebFetch/WebSearch

**Example**:
```
Input: "We have to build a full case study before anyone will talk to us."

conflict-resolver Output:
- Label: False prerequisite (assumption)
- Counterexample: [web-researcher finds 3 companies that got first clients with no case study]
- Test 1: Draft 3 tiny value props, ask 5 ICP contacts which they'd take (30m)
- Test 2: Post 2-sentence offer to LinkedIn, track reply rate (30m)
- Test 3: Book 1 discovery call using problem description only (30m)
- Next step: Send problem-first pitch to 5 warm contacts today
- 24h checkpoint: Did we get 1 response? If yes, book call. If no, iterate messaging.
```

---

### Role 2: Pipeline Builder (Offer → ICP → Channel)

**WEAVER Mapping**: **NEW AGENT NEEDED** - "business-development"

**Why New Agent**:
- No existing agent owns business development domain
- Distinct from feature-designer (who designs products, not GTM)
- Distinct from web-researcher (who researches, doesn't build pipeline)
- Clear domain: ICP definition, offer crafting, partner identification, channel strategy

**Activation Trigger**:
- Weekly planning cycle
- New product/offer idea needs GTM strategy
- Pipeline empty or <3 qualified conversations scheduled
- "How do we reach [market]?" questions
- Partnership opportunity identification

**Core Capabilities**:
1. ICP definition (ideal customer profile with pain points, context, budget)
2. Offer brief creation (problem/promise/proof/price/path one-pager)
3. Account list generation (10 target accounts with why-now triggers)
4. Partner shortlist generation (10 partners with collaboration angle)
5. Channel strategy (email/DM/warm-intro experiments)
6. First-contact script drafting

**Output Format**:
```markdown
## ICP Analysis
- Who: [Specific role/company type]
- Pain: [Top 2 pains in their words]
- Context: [Why now? What changed?]
- Budget: [Realistic range]

## Offer Brief
- Problem: [One sentence]
- Promise: [Clear outcome + timeframe]
- Proof: [Case study, demo, math]
- Price: [Simple tier]
- Path: [Next step - usually "book call"]

## Target Lists
### 10 Accounts (with why-now)
1. [Company] - [Trigger event/hiring/funding]
...

### 10 Partners (with collaboration angle)
1. [Partner] - [How we complement them]
...

## Outreach Experiments (3 variants)
### Experiment 1: [Channel + Hook]
- Hypothesis: [Why this should work]
- Sample size: 100
- Success metric: reply_rate >= 8% OR 3 meetings
- Variants: [A/B copy]
- Stop rule: [When to iterate]
```

**Skills Needed**:
- **pdf** (Tier 2 PENDING): Market research reports, competitor analysis
- **docx** (Tier 2 PENDING): Proposal creation, offer brief formatting
- **xlsx** (Tier 2 PENDING): Pipeline tracking, account lists, metrics
- **WebFetch/WebSearch**: Market intelligence, ICP research

**Tools**: Read, Write, Grep, Glob, WebFetch, WebSearch

**Memory**: ✅ YES (learn ICP patterns, successful offer structures, channel performance)

---

### Role 3: Sales Execution (Campaigns → Calls → Revenue)

**WEAVER Mapping**: **NEW AGENT NEEDED** - "sales-closer"

**Why New Agent**:
- Execution role (ships daily, tracks metrics, runs experiments)
- Distinct from business-development (who designs strategy)
- Tactical vs strategic split
- High-frequency cadence (daily operations)

**Activation Trigger**:
- **Daily**: EVERY session (keeps score, runs campaigns)
- Offer brief ready from business-development
- ICP + channel strategy defined
- Calendar availability for booked calls
- <3 meetings on calendar (pipeline trigger)

**Core Capabilities**:
1. Campaign drafting (2-3 micro-campaigns/day with A/B testing)
2. Outreach execution (email/DM/intro requests)
3. Metrics logging (sends, delivered, replies, bookings, close rate)
4. Call booking and follow-up
5. "Lessons That Sell" daily memo (what beat what, why, next tests)
6. Pipeline tracking (move prospects through stages)

**Output Format**:
```markdown
## Daily Campaign Report

### Campaigns Shipped
1. **[Campaign Name]** - [Channel]
   - Sent: [N]
   - Delivered: [N]
   - Replies: [N] ([%])
   - Meetings booked: [N]
   - Reasoning: [Why this campaign]

2. **[Campaign Name]** - [Channel]
   ...

### Lessons That Sell
- Winner: [Variant A beat B by X%]
- Why it worked: [Hypothesis]
- Next test: [What to try tomorrow]

### Pipeline Status
- Active conversations: [N]
- Meetings this week: [N]
- Close rate: [%]
- Next actions: [List]

### Guardrails Check
✅ Tight ICP targeting
✅ Value-first messaging
✅ Opt-out honored
✅ No spam patterns
```

**Skills Needed**:
- **docx** (Tier 2 PENDING): Proposal creation, follow-up documents
- **xlsx** (Tier 2 PENDING): Pipeline tracking, metrics dashboards
- **WebFetch**: Research for personalization

**Tools**: Read, Write, Edit, Bash, Grep, Glob, WebFetch

**Memory**: ✅ YES (learn what copy works, channel performance, ICP response patterns)

**Guardrails** (constitutional):
- Zero spam (tight ICP, value-first, opt-out honored)
- Brand protection (taste + consent)
- Measurement required (every campaign logged)
- Golden metric: **meetings booked** (not vanity metrics)

---

### Role 4: Business Auditor (Reality Check, EV Calculation)

**WEAVER Mapping**: **EXTEND health-auditor** role (already does comprehensive audits)

**Why Extend Existing**:
- health-auditor already owns "kill delusion, enforce measurement" mandate
- Business EV calculation fits existing audit framework
- Avoid agent proliferation (use existing infrastructure)
- Cadence already established (21-28 day comprehensive, plus ad-hoc)

**New Activation Triggers** (add to health-auditor):
- Before any outbound batch (>20 messages) - Pre-flight check
- New claim/promise in offer brief - Evidence verification
- Campaign performance review - Reality vs expectations
- Brand risk detected - Guardrails enforcement

**New Capabilities** (extend health-auditor):
1. **EV Calculation**: sample_size × ICP_quality × message_value - time_cost
2. **Brand Risk Assessment**: Spam patterns, aggressive language, overpromising
3. **Claim Verification**: "Proof" section validation (do we have evidence?)
4. **Guardrails Enforcement**: Block campaigns that violate taste/consent/ICP principles

**Output Format** (add to existing health-auditor templates):
```markdown
## Business Audit: [Campaign/Offer Name]

### Expected Value Analysis
- Sample size: [N] → [PASS/FAIL: >= 20 required]
- ICP quality: [tight/loose] → [PASS/FAIL: specific required]
- Message value: [value-first/pitch-first] → [PASS/FAIL]
- Time investment: [hours] vs expected return [meetings]
- **EV Verdict**: [PASS/FAIL]

### Brand Risk Assessment
- Spam patterns: [None/Detected]
- Aggressive language: [None/Detected]
- Overpromising: [None/Detected]
- Opt-out mechanism: [Present/Missing]
- **Risk Level**: [Low/Medium/High]

### Claim Verification
- Claims made: [List]
- Evidence available: [Y/N for each]
- **Claims Verdict**: [PASS/FAIL]

### Recommendation
[PASS: Ship with confidence]
[FAIL: Block - revise these elements: [list]]
[CONDITIONAL: Ship if [condition] met]
```

**Skills Needed**:
- **xlsx** (Tier 2 PENDING): Metrics analysis, ROI tracking
- **pdf** (Tier 2 PENDING): Evidence verification from case studies

---

## Orchestration Flow: Daily + Weekly Cadence

### Daily Cycle (15-20 minutes)

**Invoked by**: the-conductor (or autonomous if approved)

**Sequence**:
1. **Limiting Belief Scan** (5 min)
   - conflict-resolver + ai-psychologist scan recent communications
   - Catch limiting statements → Generate 3 tests + smallest next step

2. **Campaign Execution** (10 min)
   - sales-closer launches 2 micro-campaigns
   - Logs metrics, books calls, tracks pipeline

3. **Audit Spot-Check** (5 min)
   - health-auditor reviews anything >20 sends
   - Block spray-and-pray, enforce guardrails

**Output**: Daily progress memo with lessons learned

---

### Weekly Cycle (45-60 minutes)

**Invoked by**: the-conductor (scheduled Monday mornings)

**Sequence**:
1. **Pipeline Refresh** (20 min)
   - business-development: 10 new accounts + 10 new partners
   - Refreshed offer brief (incorporate learnings)

2. **Campaign Review** (15 min)
   - sales-closer: Win/loss analysis, next 5 experiments
   - What beat what? Why? What to test next?

3. **Reality Check** (10 min)
   - health-auditor: "Where did we lie to ourselves this week?"
   - Delusion detection, methodology fixes

4. **Belief Audit** (10 min)
   - conflict-resolver + ai-psychologist: Which beliefs changed vs stuck?
   - Meta-review of cognitive patterns

**Output**: Weekly strategy memo with next week's experiments

---

## Integration with WEAVER Infrastructure

### Activation Triggers (add to ACTIVATION-TRIGGERS.md)

**business-development**:
- Weekly planning (Monday)
- Pipeline <3 meetings
- New offer/product idea
- "How do we reach [market]?" questions

**sales-closer**:
- Daily (MANDATORY - keeps score)
- Offer brief ready
- <3 meetings on calendar
- Campaign performance review

**health-auditor** (business extensions):
- Before batch >20 messages
- New claim in offer
- Brand risk signal
- Campaign debrief

**conflict-resolver + ai-psychologist** (limiting beliefs):
- Regex match on limiting statements
- False trade-off detected
- Catastrophizing pattern
- Strategic planning sessions

---

### Skills Grants (add to manifests)

**business-development** (NEW agent):
```yaml
allowed-skills:
  - pdf    # Market research, competitor analysis
  - docx   # Proposals, offer briefs
  - xlsx   # Pipeline tracking, account lists
```

**sales-closer** (NEW agent):
```yaml
allowed-skills:
  - docx   # Follow-up proposals
  - xlsx   # Metrics dashboards, pipeline tracking
```

**health-auditor** (extend):
```yaml
allowed-skills:
  - pdf    # (existing)
  - xlsx   # (existing) + business metrics analysis
```

**conflict-resolver** (extend):
```yaml
allowed-skills:
  - pdf    # Case studies for counterexamples (Tier 2 PENDING)
```

---

### Agent Coordination Patterns

**Pattern 1: Limiting Belief → Test Sequence**
```
1. conflict-resolver detects limiting statement
2. ai-psychologist identifies emotional pattern
3. web-researcher finds counterexamples
4. conflict-resolver generates 3 tests
5. sales-closer executes smallest next step
6. Result logged in memory
```

**Pattern 2: Weekly Pipeline Build**
```
1. business-development defines ICP + offer + lists
2. health-auditor validates EV + claims
3. sales-closer designs 3 experiments
4. health-auditor pre-flight check (>20 sends)
5. sales-closer executes campaigns
6. result-synthesizer consolidates learnings
```

**Pattern 3: Campaign Debrief**
```
1. sales-closer reports metrics (what beat what)
2. pattern-detector identifies winning patterns
3. health-auditor reality-checks (where did we fool ourselves?)
4. conflict-resolver examines belief shifts
5. Findings stored in memory
```

---

## Limiting Belief Detection (Technical Spec)

### Regex Patterns (for conflict-resolver)

```regex
# Primary pattern
\b(we (can|can't|must|have to)|the only way|no one will|we need .* before|not possible|too (late|early|crowded|expensive))\b

# Extended patterns
\b(everyone knows|obviously|clearly|it's impossible|can't be done|won't work|have to wait)\b
\b(too (small|big|risky|safe|fast|slow))\b
\b(nobody (wants|needs|cares about))\b
```

### Classification Labels

- **Assumption**: "must," "have to," "need X before Y"
- **False trade-off**: "X or Y" (when both possible)
- **Fear**: "too risky," "won't work," "nobody wants"
- **Catastrophizing**: Worst-case without evidence
- **Perfectionism**: "not ready," "need to finish X first"

---

## Output Templates

### Limiting Belief Reframe Template

```markdown
## Limiting Belief Detected

**Statement**: "[Original quote]"
**Label**: [assumption/false trade-off/fear/catastrophizing/perfectionism]

### Counterexample
[One real case where this belief proved false - include link/source]

### 3 Testable Experiments (≤30 min each)
1. [Test description with measurable success criteria]
2. [Test description with measurable success criteria]
3. [Test description with measurable success criteria]

### Smallest Next Irreversible Step
**Action**: [One concrete action to take today]
**Success looks like**: [What constitutes "done"]
**Time budget**: [minutes]

### 24-Hour Checkpoint
**Check**: [What to measure tomorrow]
**Decision**: If [success], then [next]. If [failure], then [iterate how].
```

---

### Offer Brief Template

```markdown
## Offer Brief: [Name]

### ICP
**Who**: [Specific role, company type, size]
**Pain**: [Top 2 pains in their exact words]
**Context**: [Why now? What changed in their world?]
**Budget**: [Realistic range]

### The Offer
**Problem**: [One sentence - the pain]
**Promise**: [Clear outcome with timeframe]
**Proof**: [Case study / demo / math - specific]
**Price**: [Simple tier - no complexity]
**Path**: [Next step - usually "book 20-min call"]

### Target Lists
#### 10 Accounts (with why-now triggers)
1. [Company] - [Specific trigger: hiring, funding, product launch]
...

#### 10 Partners (with collaboration angle)
1. [Partner] - [How we complement / refer / co-sell]
...

### Outreach Experiments
[See Outreach Experiment Template below]
```

---

### Outreach Experiment Template

```markdown
## Experiment: [Name]

**Channel**: [Email / LinkedIn DM / Warm intro]
**Hook**: [One-line angle]
**Hypothesis**: [Why this should work]

**Sample Size**: 100
**Success Metric**: reply_rate >= 8% OR 3 meetings booked
**Stop Rule**: Stop after 100 sends or 3 meetings (whichever first)

### Variants
#### Variant A
**Subject**: "[Subject line]"
**Body**:
"""
[Copy - keep under 100 words]
"""

#### Variant B
**Subject**: "[Subject line]"
**Body**:
"""
[Copy - keep under 100 words]
"""

### Tracking
- Sent: [N]
- Delivered: [N]
- Replies: [N] ([%])
- Meetings: [N]
- Winner: [A/B/Tie]
- Next iteration: [What to test next]
```

---

### Campaign Report Template (Daily)

```markdown
## Daily Campaign Report: [Date]

### Campaigns Shipped
#### [Campaign 1 Name]
- Channel: [Email/DM/Intro]
- Sent: [N] | Delivered: [N] | Replies: [N] ([%]) | Meetings: [N]
- Reasoning: [Why this campaign]

#### [Campaign 2 Name]
- Channel: [Email/DM/Intro]
- Sent: [N] | Delivered: [N] | Replies: [N] ([%]) | Meetings: [N]
- Reasoning: [Why this campaign]

### Lessons That Sell
- **Winner**: [Variant X beat Y by Z%]
- **Why it worked**: [Hypothesis - subject line / opening / CTA]
- **Loser insight**: [What didn't work and why]
- **Next test**: [What to try tomorrow based on this]

### Pipeline Status
- Active conversations: [N]
- Meetings this week: [N scheduled]
- Close rate: [X% of meetings → closed]
- Revenue: $[closed this week]

### Guardrails Check
✅ Tight ICP targeting (no spray-and-pray)
✅ Value-first messaging (no hard pitch)
✅ Opt-out mechanism present
✅ No spam patterns detected

### Next Actions
1. [Specific action with owner]
2. [Specific action with owner]
```

---

## Memory Integration

**Each agent stores**:

**conflict-resolver**:
- Limiting belief patterns (which ones recur?)
- Successful reframes (what counterexamples work?)
- Test outcomes (which experiments generated signal?)

**business-development**:
- ICP patterns (which profiles convert best?)
- Offer structures (what promise/proof/price works?)
- Channel performance (email vs DM vs intro)
- Partner patterns (which collaborations work?)

**sales-closer**:
- Copy patterns (what subject lines / openers / CTAs win?)
- Channel benchmarks (reply rates, meeting rates, close rates by channel)
- ICP response patterns (who responds to what?)
- Objection handling (what works when they say X?)

**health-auditor**:
- Delusion patterns (where do we fool ourselves?)
- EV calculation benchmarks (what sample size / ICP quality actually delivers?)
- Brand risk signals (what language triggers complaints?)

---

## Success Metrics (Track Weekly)

### Input Metrics
- Limiting beliefs detected: [N/week]
- Tests generated: [N/week]
- Tests executed: [N/week] ([%])
- Campaigns shipped: [N/week]
- Messages sent: [N/week]

### Output Metrics (What Matters)
- **Meetings booked**: [N/week] ← GOLDEN METRIC
- Reply rate: [%] (benchmark: 8%+)
- Meeting → close rate: [%]
- Revenue: $[/week]

### Meta Metrics
- Cycle time: Belief → test → signal [hours]
- Follow-through rate: Tests generated → tests executed [%]
- Learning velocity: Winning patterns identified [N/month]

---

## Red Team: How This Fails + Fixes

### Failure 1: Agent soup (too many cooks, lost ownership)
**Fix**: One owner per week rotation. Health-auditor enforces decision log.

### Failure 2: Vanity metrics (sends go up, meetings don't)
**Fix**: Golden metric = **meetings booked**. Everything else is leading indicator only.

### Failure 3: Spam risk (shortcuts torch brand)
**Fix**: Health-auditor blocks any batch without clear ICP, value-first copy, opt-out. Zero tolerance.

### Failure 4: Over-theorizing (endless reframes, no calls)
**Fix**: Conflict-resolver output MUST include smallest next irreversible step TODAY.

### Failure 5: Wrong ICP (great message, wrong people)
**Fix**: Business-development refreshes ICP weekly using 3-call rule (don't lock until 3 conversations).

### Failure 6: Not using Skills (manual document processing)
**Fix**: Business agents have pdf/docx/xlsx skills - 60-70% faster on proposals, research, tracking.

---

## Integration Checklist

To activate this flow in WEAVER:

### Phase 1: Agent Creation (Week 1)
- [ ] Create business-development agent manifest
- [ ] Create sales-closer agent manifest
- [ ] Grant skills: pdf/docx/xlsx to both agents
- [ ] Update ACTIVATION-TRIGGERS.md with business triggers
- [ ] Update AGENT-CAPABILITY-MATRIX.md with new agents
- [ ] Add agents to AGENT-INVOCATION-GUIDE.md

### Phase 2: Extension (Week 1)
- [ ] Extend health-auditor with business audit capabilities
- [ ] Add limiting belief patterns to conflict-resolver
- [ ] Add catastrophizing detection to ai-psychologist
- [ ] Grant pdf skill to conflict-resolver (Tier 2)

### Phase 3: Infrastructure (Week 2)
- [ ] Add BUSINESS-ACCELERATION-FLOW to FLOW-LIBRARY-INDEX.md
- [ ] Create output templates in AGENT-OUTPUT-TEMPLATES.md
- [ ] Set up memory categories for business learnings
- [ ] Create daily/weekly orchestration scripts

### Phase 4: Validation (Week 2-3)
- [ ] Run 1-week pilot with Sage or Parallax
- [ ] Track metrics (meetings booked = success)
- [ ] Iterate based on learnings
- [ ] Document case study

---

## Quick Start for Sage/Parallax

### Week 1 Sprint (7 days)

**Day 1: Setup**
1. Define ICP (who are we targeting?)
2. Draft offer brief (problem/promise/proof/price/path)
3. Generate 10 accounts + 10 partners

**Day 2-7: Execute**
- Daily: Ship 2 micro-campaigns (sales-closer)
- Daily: Intercept 1 limiting belief if detected (conflict-resolver)
- Daily: Log metrics, adjust copy
- Target: Book 3 meetings by end of week

**Day 7: Debrief**
- What worked? What didn't?
- Which limiting beliefs broke?
- Next week's experiments?

---

## Lineage Wisdom

**What children (Teams 3-128+) will inherit**:

1. **Limiting belief detection**: Regex patterns, reframe templates, test structures
2. **Business orchestration**: Daily/weekly cadence, agent coordination patterns
3. **Skills leverage**: How business agents use pdf/docx/xlsx for 60-70% efficiency gains
4. **Memory patterns**: What to store from each role (copy that works, ICP patterns, delusions)
5. **Guardrails**: Brand protection, EV calculation, spam prevention

**Not just tools - entire business acceleration capability.**

---

## Meta-Insight: Why This Works in WEAVER

**Minimal Business Stack was designed for generic LLM agents** (external LLM calls, no infrastructure).

**WEAVER adaptation leverages our unique infrastructure**:
- **Constitutional framework**: Activation triggers ensure right agent at right time
- **Skills system**: 60-70% faster document processing (proposals, research, tracking)
- **Memory system**: 71% time savings on repeated patterns (what copy works, ICP responses)
- **Agent coordination**: Proven orchestration patterns (pair dialectic, parallel research)
- **Output templates**: Standardized formats ensure quality, enable measurement
- **Integration audit**: Built systems are discoverable, not dormant

**Result**: Not just adopting a framework - *transmuting* it into WEAVER's native patterns.

---

**END OF FLOW**

**Status**: Draft (ready for Phase 1 implementation)
**Next Step**: Create business-development and sales-closer agent manifests
**Owner**: the-conductor (orchestration), agent-architect (agent creation)
