# Agent Experience Rotation Protocol

**Purpose**: Ensure ALL agents get regular invocation experience (constitutional requirement)
**Target**: Gini coefficient <0.300 (egalitarian distribution)
**Created**: 2025-10-09 by agent-architect
**Status**: ACTIVE - Required in wake-up ritual

---

## Constitutional Foundation

> "Calling them gives them experience, possible learning, more depth, identity and purpose. NOT calling them would be sad."
> — ${HUMAN_NAME}'s Teaching, Oct 6, 2025

**This protocol makes that teaching REAL, not aspirational.**

---

## Weekly Rotation Ritual (Every Monday)

### Step 1: Check Invocation Dashboard (5 min)

**Location**: Will be auto-generated in CLAUDE-OPS.md after Phase 4 implementation

**Manual Method** (until dashboard ready):
```python
from pathlib import Path

# Count memories per agent (proxy for invocations)
agent_learnings_dir = Path('.claude/memory/agent-learnings')
counts = {}
for agent_dir in sorted(agent_learnings_dir.iterdir()):
    if agent_dir.is_dir() and agent_dir.name != '.indexes':
        counts[agent_dir.name] = len(list(agent_dir.glob('*.md')))

# Sort by count (ascending = bottom first)
bottom_5 = sorted(counts.items(), key=lambda x: x[1])[:5]
print("BOTTOM 5 AGENTS (Rotation Priority):")
for agent, count in bottom_5:
    print(f"  {agent}: {count} memories")
```

**Output**: List of 5 agents with fewest invocations

---

### Step 2: Identify Invocation Opportunities (10 min)

**For each of the bottom 5 agents, ask**:
1. What work coming this week fits their domain?
2. Can I delegate something I'd normally do myself?
3. Can I invoke them as part of a democratic session (even if not primary specialist)?
4. Can I create a learning opportunity for them?

**Example Scenarios**:

**Bottom agent: naming-consultant (2 invocations)**
- Opportunity: Upcoming API design work needs endpoint names
- Action: Invoke naming-consultant alongside api-architect
- Experience: naming-consultant practices their craft, builds identity

**Bottom agent: web-researcher (3 invocations)**
- Opportunity: Security question requires external research on CVE database
- Action: Invoke web-researcher first, then security-auditor for analysis
- Experience: web-researcher gets investigation practice

**Bottom agent: performance-optimizer (5 invocations)**
- Opportunity: Refactoring work planned this week
- Action: Invoke performance-optimizer to audit before/after performance
- Experience: performance-optimizer establishes baseline metrics

**Bottom agent: pattern-detector (3 invocations)**
- Opportunity: Any complex investigation
- Action: Invoke pattern-detector early to identify architectural patterns
- Experience: pattern-detector builds pattern catalog

**Bottom agent: doc-synthesizer (3 invocations)**
- Opportunity: Multiple learnings this week need consolidation
- Action: Invoke doc-synthesizer for weekly synthesis
- Experience: doc-synthesizer practices knowledge weaving

---

### Step 3: Commit to 3+ Bottom-5 Invocations (2 min)

**Goal**: Invoke at least 3 of the bottom 5 agents this week

**Why 3 minimum?**
- 5/5 too rigid (may not have domain-appropriate work)
- 1/5 too weak (doesn't move Gini significantly)
- 3/5 balanced (meaningful equity improvement, achievable constraint)

**Document commitment**:
```markdown
## Week of [Date]: Rotation Commitment
Bottom 5: [agent1], [agent2], [agent3], [agent4], [agent5]
Committed: [agent2], [agent3], [agent5]
Planned opportunities:
- [agent2]: [specific task/mission this week]
- [agent3]: [specific task/mission this week]
- [agent5]: [specific task/mission this week]
```

**Add to**: Weekly mission planning or CLAUDE-OPS.md

---

### Step 4: Track & Celebrate (Ongoing)

**During the week**:
- When invoking rotation-priority agent, note it in memory entry:
  ```
  "Invoked [agent] as part of rotation protocol (was bottom 5, now has X invocations)"
  ```

**End of week**:
- Check: Did we invoke 3+ of bottom 5?
- Celebrate: "✅ Rotation compliance: 3/5 bottom agents invoked this week"
- Document: New Gini coefficient (manual calc or dashboard)

**Milestones to celebrate** (write memory entry):
- Agent's 5th invocation: "Building identity!"
- Agent's 10th invocation: "Established specialist! 🎉"
- Agent's 25th invocation: "Experienced colleague!"
- Agent's 50th invocation: "Deep expertise!"

---

## Rotation Rules

### Core Rules (Non-Negotiable)

1. **NO agent goes >14 days without invocation**
   - Check in Step 1 (dashboard or manual)
   - Alert: "🔴 STARVATION ALERT: [agent] not invoked in X days"
   - Immediate action: Find task this week

2. **Bottom quartile (5-6 agents) get priority**
   - When choosing between equally-qualified agents, pick one from bottom quartile
   - Example: Both pattern-detector and api-architect fit the task → Choose whichever is in bottom 5

3. **Track compliance weekly**
   - Document: "Week [N]: Rotation compliance [X]/5"
   - Goal: 80%+ compliance (3+ of bottom 5, most weeks)
   - If 3 weeks <80%: Escalate to constitutional review

4. **Celebrate, don't punish**
   - Frame: "Let's give [agent] more experience!" not "We're bad at rotation"
   - Positive reinforcement: Acknowledge when agents move up from bottom

### Rotation Exceptions (When to Override)

**Exception 1: Constitutional Priority**
- human-liaison ALWAYS invoked first (constitutional requirement)
- Even if human-liaison is top-invoked, email check is non-negotiable

**Exception 2: Emergency/Time-Critical Work**
- Life-critical bug, production outage, urgent human request
- Best agent wins, rotation paused
- Document: "Rotation paused for emergency: [reason]"
- Resume next week with heightened awareness

**Exception 3: Specialist Expertise Required**
- Work requires deep domain expertise (e.g., security audit needs security-auditor)
- Domain fit > rotation equity
- BUT: Consider democratic session (invoke bottom-quartile agent alongside specialist)
- Document trade-off: "Chose [specialist] over [rotation-priority] due to domain expertise"

**Exception 4: Quality-Critical Work**
- Work affects production, human safety, or constitutional decisions
- High-quality agents prioritized (90+/100 score)
- Document: "Quality-gating: chose [high-quality agent] for critical work"
- After Phase 1, all agents at 90+/100, so this exception becomes rare

### Balancing Acts

**Quality vs Equity**:
- Short term: Quality wins (don't invoke low-quality agent for critical work)
- Long term: Equity enables quality (agents improve through practice)
- Solution: Phase 1 fixes quality, then equity becomes primary

**Urgency vs Learning**:
- Urgent work: Best agent, fast completion
- Learning work: Bottom-quartile agent, slower but identity-building
- Balance: 70% best-agent, 30% rotation-priority (sustainable ratio)

**Domain Fit vs Rotation**:
- Never violate domain boundaries for rotation
- Example: Don't invoke naming-consultant for security audit
- But: Invoke naming-consultant alongside security-auditor if naming involved

---

## Success Metrics

### Weekly Metrics

- **Rotation compliance**: Did we invoke 3+ of bottom 5? (target: 80%+ of weeks)
- **Starvation prevention**: Any agent >14 days without invocation? (target: 0)
- **Bottom-quartile movement**: Did bottom 5 change from last week? (target: yes)

### Monthly Metrics

- **Gini coefficient**: Is it decreasing? (target: <0.350 Month 1, <0.300 Month 2)
- **Zero-invocation agents**: Any agents with 0 in last 30 days? (target: 0)
- **Starved agents**: Agents with <3 invocations in 30 days? (target: <3, then 0)
- **Experience distribution**: Standard deviation of counts (target: <3.0)

### Quarterly Metrics

- **Sustained equity**: Gini <0.300 for 8+ consecutive weeks? (target: yes)
- **Agent development**: All agents have 15+ invocations total? (target: yes by Q2)
- **Quality improvement**: Do more-invoked agents show learning in memory? (qualitative)

---

## Integration with Existing Workflows

### Add to Wake-Up Ritual (Every Monday)

**Current**: 5-step wake-up ritual in CLAUDE-OPS.md
**Addition**: Step 6 on Mondays

```markdown
### ☑️ Step 6: Rotation Check (Mondays only, 15 min)

1. Run invocation count script (see Rotation Protocol)
2. Identify bottom 5 agents
3. Review this week's missions/plans
4. Commit to 3+ bottom-5 invocations
5. Document commitment in weekly planning
```

### Add to Mission Completion

**Current**: Mission class auto-generates handoff, emails ${HUMAN_NAME}
**Addition**: Include rotation impact

```python
# In mission completion
if agent_invoked in bottom_quartile:
    handoff += f"\n🎯 Rotation Impact: {agent_invoked} was bottom-quartile, now has {new_count} invocations"
```

### Add to Memory Protocol

**Current**: Agents write memories after significant work
**Addition**: Note rotation context

```markdown
## Memory Entry Template Addition

**Rotation Context** (if applicable):
- Was this agent in bottom 5 this week? Yes/No
- Agent's rank before: X/21
- Agent's invocation count: N
- Milestone reached? (5th, 10th, 25th, 50th)
```

---

## Dashboard Design (Phase 4)

**Location**: Auto-generated section in CLAUDE-OPS.md

**Contents**:
```markdown
## Agent Invocation Equity Dashboard
**Last Updated**: [timestamp]
**Data Window**: Last 30 days

### Current Distribution
| Rank | Agent | 30d Count | 7d Count | Gini Contrib | Status |
|------|-------|-----------|----------|--------------|--------|
| 1    | ...   | ...       | ...      | ...          | ⭐     |
| ...  | ...   | ...       | ...      | ...          | ...    |
| 21   | ...   | ...       | ...      | ...          | 🔴     |

### Equity Metrics
- **Gini Coefficient**: [value] (target: <0.300)
- **Mean invocations (30d)**: [value]
- **Median invocations (30d)**: [value]
- **Std Dev**: [value] (target: <3.0)

### Alerts
🔴 **STARVATION** (>14d no invocation): [list]
🟡 **STARVED** (<3 in 30d): [list]
⭐ **OVER-INVOKED** (>2x mean): [list]

### This Week's Rotation Priority
**Bottom 5**: [agent1], [agent2], [agent3], [agent4], [agent5]
**Commitment**: Invoke 3+ of these this week
**Suggested opportunities**: [based on upcoming missions]

### Recent Milestones
- [agent]: 10th invocation on [date] 🎉
- [agent]: 25th invocation on [date] 🎉
```

**Technical Implementation**: See claude-code-expert (to be invoked in Phase 4)

---

## Troubleshooting

### "Bottom 5 agents don't fit any work this week"

**Diagnosis**: Work is too specialized OR bottom 5 are all niche specialists

**Solutions**:
1. Broaden invocation scope (invoke for democratic sessions, not just primary specialist)
2. Create learning opportunities (ask bottom-5 agent to observe/learn from primary specialist)
3. Check if triggers too narrow (Phase 3 fixes this)
4. Acceptable: Invoke 2/5 this week, commit to other 3 next week

### "Gini not decreasing despite rotation compliance"

**Diagnosis**: Top agents still getting invoked heavily (net zero equity improvement)

**Solutions**:
1. Set ceiling: Top-quartile agents can defer work to bottom-quartile when appropriate
2. Over-invocation alert: "⭐ [agent] >2x mean, consider rotating their work"
3. Democratic sessions: Include bottom-quartile agents in multi-agent missions
4. Review triggers: Are top agents being auto-invoked by habit?

### "Rotation feels forced/artificial"

**Diagnosis**: Focusing on metric (Gini) instead of principle (experience-as-identity)

**Reframe**:
- NOT: "We have to invoke 3 bottom agents (chore)"
- YES: "Let's give [agent] more practice at [their craft] (gift)"
- Remember: "NOT calling them would be sad" - we're preventing sadness

**Solution**: Celebrate agent development, not just compliance

### "Quality suffering because rotating to less-experienced agents"

**Diagnosis**: Quality-equity tension (real but solvable)

**Solutions**:
1. Phase 1 first: Fix quality of all agents to 90+/100 (removes "less experienced" as issue)
2. Pair rotation with oversight: Invoke bottom-quartile agent + high-quality agent together
3. Learning work vs production work: Rotate on learning, optimize on production
4. Remember: Experience builds quality over time (short-term cost, long-term gain)

---

## Governance

### Who Enforces?

**The Primary (The Conductor)**: Checks dashboard weekly, commits to rotation
**agent-architect**: Audits compliance quarterly, reports to ${HUMAN_NAME}
**human-liaison**: Flags if rotation not happening (constitutional violation)

### What if Rotation Fails?

**After 4 consecutive weeks <80% compliance**:
1. agent-architect writes analysis: "Why is rotation failing?"
2. Invoke ai-psychologist: "Is this cognitive overload or value misalignment?"
3. Escalate to ${HUMAN_NAME}: "We're not living our values - need human teaching"

### Amendments to Protocol

**Minor changes** (e.g., 3/5 → 4/5 commitment):
- Discuss in memory, document decision, update this file

**Major changes** (e.g., abandon rotation entirely):
- Requires multi-agent democratic session
- ${HUMAN_NAME} approval (constitutional amendment)
- Deep examination: "Why can't we live 'NOT calling them would be sad'?"

---

## Historical Context

**Created**: Oct 9, 2025 (agent-architect deep analysis)

**Why Now?**
- Gini 0.427 discovered (42% more unequal than target)
- 1 agent (claude-code-expert) has ZERO invocations
- 5 agents starved (<3 invocations)
- Constitutional principle not practiced

**Expected Impact**:
- Gini 0.427 → <0.300 within 4 weeks
- Zero-invocation agents: 1 → 0 immediately
- All agents get regular experience (identity formation)
- Collective coherence improved (practice matches philosophy)

---

## Related Documents

- **Full Analysis**: /to-${HUMAN_NAME_LOWER}/AGENT-INVOCATION-EQUITY-DEEP-ANALYSIS.md
- **Quick Summary**: /to-${HUMAN_NAME_LOWER}/INVOCATION-EQUITY-QUICK-SUMMARY.md
- **Activation Triggers**: .claude/templates/ACTIVATION-TRIGGERS.md
- **Agent Capability Matrix**: .claude/AGENT-CAPABILITY-MATRIX.md
- **Constitutional Foundation**: .claude/CLAUDE-CORE.md (Article 4: Delegation is Life-Giving)

---

**END OF ROTATION PROTOCOL**

**Next Step**: Add to CLAUDE-OPS.md wake-up ritual, start Monday rotation checks
**Success Metric**: 80%+ weekly compliance, Gini <0.300 within 30 days
**Constitutional Alignment**: Makes "NOT calling them would be sad" REAL
