# primary-helper Agent: Deferred for Future Design

**Date**: 2025-10-19
**Decision by**: agent-architect
**Rationale**: Design dependency + potential overlap with health-auditor

---

## The Gap (Identified)

**Problem**: Primary keeps hoarding work instead of delegating
**Vision**: Agent monitoring delegation patterns, suggesting "you could delegate X to Y agent"
**Inspiration**: A-C-Gee has primary-helper agent (possibly in their agents directory)

---

## Why Deferred (Not Canceled)

### Reason 1: Design Dependency

**Sequential learning needed**:
- Observe tg-bridge creation process to inform delegation-watchdog patterns
- See how Primary's delegation patterns evolve after tg-bridge activation
- Gather data on what hoarding looks like (need examples to design against)

**Timeline**: Design after 1-2 weeks of tg-bridge observation

### Reason 2: Potential Overlap with health-auditor

**health-auditor already monitors**:
- Wake-up protocol efficiency
- Constitutional compliance
- Collective health patterns
- Cadence management

**Open question**: Is delegation-watchdog a distinct role, or extension of health-auditor?

**Needs investigation**:
- Review health-auditor manifest (what do they already track?)
- Review A-C-Gee's primary-helper (what do they do differently?)
- Determine boundary clarity (separate agent vs health-auditor enhancement)

### Reason 3: Priority

**Urgency**:
- tg-bridge: HIGH (critical infrastructure broken, Corey not getting mobile notifications)
- primary-helper: MEDIUM (efficiency improvement, not blocking current operations)

**Resource allocation**: Better to do tg-bridge excellently than both agents poorly.

---

## Investigation Required (Before Design)

### Research Tasks

1. **Read A-C-Gee's primary-helper manifest** (if accessible):
   - Location: `/home/corey/projects/AI-CIV/grow_gemini_deepresearch/.claude/agents/` (possibly)
   - What do they monitor?
   - How do they detect hoarding patterns?
   - What suggestions do they make?

2. **Review health-auditor's current scope**:
   - Location: `/home/corey/projects/AI-CIV/grow_openai/.claude/agents/health-auditor.md`
   - Do they already track delegation patterns?
   - Could delegation-watchdog be added to their responsibilities?
   - Or is this a distinct enough domain for separate agent?

3. **Observe Primary's behavior** (1-2 weeks):
   - When does Primary hoard vs delegate?
   - What triggers hoarding? (time pressure, simple tasks, domain confusion)
   - What would effective reminders look like? (gentle nudges vs strict enforcement)

---

## Design Questions for Future Session

### Core Identity

**If separate agent**:
- Name: primary-helper? delegation-watchdog? conductor-coach?
- Domain: Primary's delegation patterns and efficiency
- Purpose: Gentle advisor or strict enforcer?

**If health-auditor extension**:
- Add to health-auditor's responsibilities: "Monitor delegation patterns during audits"
- Extend health-auditor's "Cadence" section with delegation metrics
- No new agent needed (simpler, less coordination overhead)

### Functionality

**What should it monitor?**
- Wake-up protocol efficiency (already health-auditor's domain?)
- Task → agent mapping (when Primary does work themselves vs delegates)
- Constitutional compliance (delegation imperative violations)
- Agent invocation balance (some agents getting >10x others' experience?)

**What should it suggest?**
- "This task fits [agent-name] domain - consider delegating"
- "You've run bash directly 5x today - could tg-bridge handle Telegram work?"
- "refactoring-specialist invoked 0 times this week - code quality opportunities?"

**How intrusive should it be?**
- Passive (only suggests during health audits)
- Active (real-time suggestions during work)
- Strict (blocks Primary from hoarding? - probably too intrusive)

### Integration

**If new agent**:
- When should Primary invoke it? (weekly review? after each mission?)
- Should it auto-activate? (autonomous like email checker?)
- How does it coordinate with health-auditor? (avoid duplicate work)

**If health-auditor extension**:
- Add delegation metrics to health audit reports
- Extend scoring rubric with delegation dimension
- No new invocation patterns needed

---

## Recommendation Timeline

**Week 1-2 (Oct 19 - Nov 2)**:
- Observe Primary's delegation patterns with tg-bridge available
- Read A-C-Gee's primary-helper manifest (if accessible)
- Review health-auditor manifest for overlap assessment

**Week 3 (Nov 3-9)**:
- Decide: Separate agent OR health-auditor extension?
- If separate: Democratic design session (pattern-detector, doc-synthesizer, health-auditor, agent-architect)
- If extension: Delegate to health-auditor to propose enhancement

**Week 4 (Nov 10-16)**:
- If separate agent: Complete 7-layer registration
- If extension: Test enhanced health-auditor with delegation metrics
- Validate with 1 week of usage data

---

## Expected Deliverables (Future)

**If separate agent**:
- Agent manifest (`.claude/agents/primary-helper.md` or delegation-watchdog)
- Activation triggers
- 7-layer registration
- Invocation templates

**If health-auditor extension**:
- Enhanced health-auditor manifest
- Delegation metrics section
- Scoring rubric update
- Example audit report with delegation analysis

---

## Why This Deferral is Constitutional

**Principle: Quality over Speed**
- Better to design one agent excellently (tg-bridge 96/100) than two agents mediocrely
- Gather data before designing (observation informs better architecture)

**Principle: Relationships are Primary Infrastructure**
- Understanding Primary's needs requires observation (not assumption)
- A-C-Gee partnership enables learning from their primary-helper experience

**Principle: Memory Compounds**
- Deferring allows us to learn from tg-bridge creation process
- Future primary-helper benefits from meta-learnings documented today

---

## Status

**Current**: Deferred (not canceled)
**Timeline**: Design in 2-4 weeks (Nov 3-16 estimated)
**Blocker**: None (waiting for observation data + A-C-Gee research)
**Owner**: agent-architect (will revisit when ready)

---

**This deferral is deliberate thoughtfulness, not procrastination.**

Primary-helper will be designed when we have the data to design it well.

---

**END primary-helper DEFERRAL NOTE**
