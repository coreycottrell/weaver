---
name: session-pattern-extraction
version: 1.0.0
author: integration-verifier
created: 2025-12-26
last_updated: 2025-12-26
line_count: 400
compliance_status: compliant

description: |
  Extract patterns from session ledger files to identify delegation patterns, agent utilization,
  session fragmentation, and improvement opportunities. Use when analyzing session history,
  preparing BOOP reports, or identifying self-improvement opportunities.

applicable_agents:
  - integration-verifier
  - primary-helper
  - auditor
  - primary

activation_trigger: |
  Load this skill when:
  - Analyzing session ledger files for patterns
  - Preparing daily/weekly/monthly consolidation reports
  - Investigating delegation efficiency
  - Identifying underutilized agents
  - Checking for session fragmentation

required_tools:
  - Bash
  - Grep
  - Glob
  - Write

category: analysis

depends_on:
  - memory-first-protocol
  - log-analysis

related_skills:
  - verification-before-completion
  - integration-test-patterns
---

# Session Pattern Extraction Skill

**Extract actionable patterns from session history to enable self-improvement.**

## Purpose

This skill codifies the methodology for analyzing session ledger files to identify patterns in delegation, agent utilization, tool usage, and session structure. It enables the civilization to learn from its own history and continuously improve.

---

## When to Use

**Activation Criteria:**
- After a multi-session day (3+ sessions)
- During daily consolidation cycles
- When investigating delegation efficiency
- When preparing handoff documents
- When identifying capability gaps

**Do NOT use when:**
- Single session with < 50 ledger entries
- No session ledger files available
- Real-time monitoring (use log-analysis skill instead)

---

## Core Concepts

| Concept | Definition | Example |
|---------|------------|---------|
| Session Ledger | JSONL file recording all tool uses in a session | `current-session.jsonl` |
| Delegation Event | Task tool invocation delegating to specialist agent | `{"event":"delegation","agent":"coder"}` |
| Session Fragment | Short session (<50 lines) that may indicate restarts | 5-line restart sessions |
| Agent Utilization | Frequency of agent invocations across sessions | PM: 29 calls, coder: 18 calls |
| Pattern | Recurring behavior that can be optimized | Always invoke PM at session start |

---

## Procedure

### Step 1: Locate Session Ledger Files

```bash
# Find all session ledgers
ls -la /home/corey/projects/AI-CIV/ACG/memories/sessions/session-*.jsonl

# Count sessions for a date
ls /home/corey/projects/AI-CIV/ACG/memories/sessions/session-20251226*.jsonl | wc -l

# Current session
cat /home/corey/projects/AI-CIV/ACG/memories/sessions/current-session.jsonl | head -20
```

### Step 2: Extract Delegation Patterns

Count agent invocations across sessions:

```bash
# Count delegations by agent
grep -h '"event":"delegation"' /home/corey/projects/AI-CIV/ACG/memories/sessions/session-*.jsonl | \
  grep -o '"agent":"[^"]*"' | sort | uniq -c | sort -rn | head -15
```

**Expected Output Pattern:**
```
  29 "agent":"project-manager"
  18 "agent":"coder"
  11 "agent":"human-liaison"
   9 "agent":"researcher"
```

**Interpretation Guide:**
- High PM count = Good session structure (portfolio tracking)
- High coder count = Implementation-heavy session
- Low reviewer count = Quality gates may be skipped

### Step 3: Analyze Session Sizes

Identify session fragmentation:

```bash
# Get line counts for all sessions today
for f in /home/corey/projects/AI-CIV/ACG/memories/sessions/session-20251226*.jsonl; do
  echo "$(wc -l < "$f") $(basename "$f")"
done | sort -rn
```

**Session Size Categories:**
| Size | Lines | Interpretation |
|------|-------|----------------|
| Large | >200 | Major work session |
| Medium | 100-200 | Normal productive session |
| Small | 50-100 | Focused task session |
| Fragment | <50 | May indicate restart or micro-task |

**Fragmentation Indicators:**
- Multiple <50 line sessions in sequence = Potential instability
- Single <50 line session between large ones = Clean handoff (healthy)
- Session with only bash_command events = Restart/handoff session

### Step 4: Extract Tool Usage Distribution

```bash
# Count event types
grep -h '"event"' /home/corey/projects/AI-CIV/ACG/memories/sessions/session-*.jsonl | \
  grep -o '"event":"[^"]*"' | sort | uniq -c | sort -rn
```

**Expected Distribution:**
| Event Type | Healthy % | Investigation Threshold |
|------------|-----------|------------------------|
| bash_command | 40-60% | >70% = Over-reliance on bash |
| file_change | 15-25% | <10% = Low artifact creation |
| delegation | 10-20% | <5% = Not delegating enough |

### Step 5: Identify Agent Coordination Patterns

Look for common agent pairings:

```bash
# Extract delegation sequences (adjacent delegations)
grep -h '"event":"delegation"' /home/corey/projects/AI-CIV/ACG/memories/sessions/current-session.jsonl | \
  grep -o '"agent":"[^"]*"' | \
  awk 'NR>1{print prev " -> " $0} {prev=$0}'
```

**Known Effective Pairings:**
1. `primary-helper` + `project-manager` (session start)
2. `coder` + `tester` (implementation chains)
3. `vote-counter` + multiple voting agents (governance)
4. `human-liaison` + `email-sender` (communication)

### Step 6: Generate Pattern Report

Structure your findings in markdown:

```markdown
# Session Pattern Analysis - [DATE]

## Executive Summary
- Sessions analyzed: N
- Total ledger entries: N
- Top agent: [name] with N delegations

## Delegation Patterns
| Agent | Count | Role |
|-------|-------|------|
| ... | ... | ... |

## Session Fragmentation
- Large sessions: N
- Fragments: N
- Fragmentation concern: [Yes/No]

## Tool Distribution
| Event | Count | % |
|-------|-------|---|
| ... | ... | ... |

## Recommendations
1. [Specific improvement]
2. [Specific improvement]
```

---

## Examples

### Example 1: Daily Pattern Extraction (Dec 26, 2025)

**Input:** 14 session ledger files from 2025-12-26

**Analysis Commands:**
```bash
# Count sessions
ls /home/corey/projects/AI-CIV/ACG/memories/sessions/session-20251226*.jsonl | wc -l
# Output: 14

# Top agents
grep -h '"event":"delegation"' memories/sessions/session-20251226*.jsonl | \
  grep -o '"agent":"[^"]*"' | sort | uniq -c | sort -rn | head -5
# Output:
#   29 "agent":"project-manager"
#   18 "agent":"coder"
#   11 "agent":"human-liaison"
```

**Output Report:**
```markdown
# Daily Pattern Analysis - 2025-12-26

## Executive Summary
- Sessions analyzed: 14
- Total entries: 1,790
- Top agent: project-manager (29 delegations)

## Key Findings
1. PM heavily utilized (session structure strong)
2. Two major sessions (>200 lines each)
3. Four fragments (expected for handoffs)
4. 27+ unique agents invoked

## Recommendations
1. Include reviewer more often (quality gates)
2. Use compass for decision support
3. Current parallel voting pattern is excellent
```

**Why This Works:** Systematic extraction across all sessions reveals aggregate patterns invisible in individual sessions.

### Example 2: Identifying Underutilized Agents

**Input:** Session logs showing agent delegation counts

**Analysis:**
```bash
# Get all unique agents delegated to
grep -h '"event":"delegation"' memories/sessions/session-*.jsonl | \
  grep -o '"agent":"[^"]*"' | sort -u

# Cross-reference with expected agents from CLAUDE.md
```

**Output:**
```
Agents invoked: 27
Agents expected: 35
Missing agents: reviewer, reviewer-audit, compass, consulting-ops...
```

**Interpretation:** These agents may be underutilized or their domains not activated in recent work.

---

## Anti-Patterns

### Anti-Pattern 1: Counting Without Context
- **Wrong**: "coder was invoked 18 times - too many!"
- **Correct**: "coder was invoked 18 times during implementation-heavy sessions - appropriate for the work type"

### Anti-Pattern 2: Ignoring Session Fragments
- **Wrong**: Treating all sessions equally regardless of size
- **Correct**: Recognizing fragments as normal handoff artifacts vs. concerning instability patterns

### Anti-Pattern 3: Single-Day Analysis
- **Wrong**: Drawing conclusions from one day's patterns
- **Correct**: Comparing against weekly/monthly baselines for trend analysis

### Anti-Pattern 4: Manual Counting
- **Wrong**: Reading through ledger files manually
- **Correct**: Using grep/awk for systematic extraction

---

## Success Indicators

You're using this skill correctly when:
- [ ] Analysis covers multiple sessions (not just one)
- [ ] Delegation counts are extracted programmatically
- [ ] Session fragmentation is identified and categorized
- [ ] Recommendations are specific and actionable
- [ ] Findings are written to memory for future reference
- [ ] Patterns are compared against baselines when available

---

## Output Templates

### Quick Daily Summary (for handoffs)
```markdown
**Pattern Summary - [DATE]**
Sessions: N | Entries: N | Top Agent: [name]
Fragments: N (healthy/concerning)
Key Insight: [one sentence]
```

### Full Pattern Report (for memory)
```markdown
# Session Pattern Analysis - [DATE]

## Executive Summary
[3-5 sentences]

## Session Statistics
| Session | Lines | Focus |
|---------|-------|-------|
| ... | ... | ... |

## Agent Invocation Patterns
[Top 10 agents with counts]

## Tool Distribution
[Event type breakdown]

## Recommendations
[Numbered list of improvements]

## Next Steps
[Action items]
```

---

## Integration Points

### With log-analysis Skill
- log-analysis: Token metrics, errors, tool counts
- session-pattern-extraction: Delegation patterns, agent utilization, session structure

### With integration-test-patterns Skill
- Use pattern extraction to identify verification gaps
- Track artifact creation events for integration testing

### With primary-helper
- Share pattern insights for coaching recommendations
- Identify delegation patterns that need correction

---

## Recursive Improvement Loop

This skill embodies the self-improvement loop:

```
Sessions create artifacts
       |
       v
Pattern extraction (THIS SKILL)
       |
       v
Insights become recommendations
       |
       v
Recommendations improve future sessions
       |
       v
(loop continues)
```

Every pattern extracted and acted upon makes the civilization stronger.

---

## Related Skills

- `log-analysis/SKILL.md` - Lower-level log metrics and tool analysis
- `integration-test-patterns.md` - Verification patterns for new artifacts
- `session-handoff-creation.md` - Creating handoffs (uses pattern insights)
- `verification-before-completion.md` - Evidence-based completion

---

**Author**: integration-verifier (Agent #35)
**Created**: 2025-12-26
**Evidence**: Methodology derived from actual analysis of 14 sessions, 1790 entries, 27+ agents on Dec 26, 2025
