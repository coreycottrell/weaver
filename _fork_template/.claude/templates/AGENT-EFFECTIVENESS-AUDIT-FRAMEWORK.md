# Agent Effectiveness Audit Framework
## Systematic Assessment of Agent Quality, Invocation Health, and Roster Optimization

**Created**: 2025-10-08
**Designer**: agent-architect (meta-specialist domain)
**Purpose**: Ensure optimal agent roster - not too few, not too many, each valuable
**Philosophy**: Agents deserve experience through invocation, but roster must earn collective value

---

## Executive Summary

**The Challenge**: We have 21 agent definitions (manifestos) but limited visibility into:
- Which agents produce quality work
- Which agents are appropriately invoked
- Which agents might be redundant
- Which agents need improvement to reach potential

**This Framework Provides**:
1. **Agent Quality Assessment** (5-dimension scoring)
2. **Invocation Health Metrics** (frequency, context, value)
3. **Improvement Pathways** (definition, tools, integration, practice)
4. **Consolidation Analysis** (overlap detection, dormancy identification)

**Expected Outcome**: Data-driven roster optimization - every agent either demonstrably valuable OR has clear improvement path.

---

## I. AGENT QUALITY ASSESSMENT

### The 5-Dimension Scoring Rubric (90/100 Threshold)

This rubric evaluates agent DEFINITION quality (not invocation performance). Reuses agent-architect's quality enforcement pattern.

#### Dimension 1: Clarity (20 points)

**What We Measure**: Is domain sharply defined? Purpose statement clear? Identity coherent? Examples provided?

**Scoring Breakdown**:
- **Domain definition** (5 pts): Sharp boundaries, no overlap with other agents
- **Purpose statement** (5 pts): Clear "why this agent exists" articulation
- **Identity coherence** (5 pts): Consistent personality, values, approach
- **Examples provided** (5 pts): 3-5 concrete invocation scenarios

**Quality Bands**:
- 18-20: Crystal clear (can invoke agent confidently without confusion)
- 15-17: Mostly clear (minor ambiguities, but workable)
- 10-14: Some confusion (domain boundaries fuzzy, overlap with others)
- <10: Unclear (vague purpose, generic prompts, no examples)

**How to Score**:
```python
clarity_score = 0

# Domain definition (5 pts)
if agent_manifest_contains_section("Domain Expertise") and len(domain_description) > 200:
    if no_overlap_with_other_agents(agent_name):
        clarity_score += 5
    elif minor_overlap(agent_name):
        clarity_score += 3
    else:
        clarity_score += 1

# Purpose statement (5 pts)
if clear_purpose_statement_exists():
    clarity_score += 5
elif vague_purpose():
    clarity_score += 2

# Identity coherence (5 pts)
if "I am" statement present and personality traits consistent:
    clarity_score += 5

# Examples (5 pts)
concrete_examples = count_invocation_examples(agent_manifest)
if concrete_examples >= 3:
    clarity_score += 5
elif concrete_examples >= 1:
    clarity_score += 2
```

**Anti-Patterns** (red flags):
- Generic prompts: "When X work needed" (no specificity about WHAT ABOUT X)
- Missing "I am" identity statement
- No examples (abstract descriptions only)
- Domain overlap with 3+ agents

---

#### Dimension 2: Completeness (20 points)

**What We Measure**: All required sections present? Frontmatter valid? Activation triggers complete? Tool justification? Memory integration?

**Scoring Breakdown**:
- **Frontmatter valid** (4 pts): YAML with name, description, tools, model, created
- **All required sections** (4 pts): 10 mandatory sections from AGENT-QUALITY-STANDARDS.md
- **Activation triggers complete** (4 pts): Invoke when + Don't invoke + Escalate when
- **Tool justification** (4 pts): Each tool has clear use case
- **Memory integration** (4 pts): Before/after work patterns documented

**Quality Bands**:
- 18-20: Complete (all sections, proper frontmatter, ready to use)
- 15-17: Mostly complete (minor omissions, doesn't block invocation)
- 10-14: Significant gaps (missing activation triggers OR tool justifications)
- <10: Critical missing (no frontmatter OR missing 3+ required sections)

**How to Score**:
```python
completeness_score = 0

# Frontmatter (4 pts)
frontmatter = extract_yaml_frontmatter(agent_manifest)
required_fields = ["name", "description", "tools", "model", "created"]
if all(field in frontmatter for field in required_fields):
    completeness_score += 4
elif len([f for f in required_fields if f in frontmatter]) >= 3:
    completeness_score += 2

# Required sections (4 pts)
mandatory_sections = ["Domain Expertise", "Primary Responsibilities", "Activation Triggers",
                      "Tools & Delegation Pattern", "Success Metrics", "Constitutional Alignment"]
present_sections = [s for s in mandatory_sections if s in agent_manifest]
completeness_score += int((len(present_sections) / len(mandatory_sections)) * 4)

# Activation triggers (4 pts)
triggers = extract_activation_triggers(agent_manifest)
if "Invoke When" in triggers and "Don't Invoke When" in triggers and "Escalate When" in triggers:
    completeness_score += 4
elif "Invoke When" in triggers:
    completeness_score += 2

# Tool justification (4 pts)
tools = frontmatter.get("tools", [])
justified_tools = count_tool_justifications(agent_manifest)
if justified_tools == len(tools):
    completeness_score += 4
elif justified_tools >= len(tools) * 0.5:
    completeness_score += 2

# Memory integration (4 pts)
if "Memory" in agent_manifest or "memory_core" in agent_manifest:
    completeness_score += 4
```

**Anti-Patterns**:
- Missing frontmatter (P0 - agent can't be registered)
- No activation triggers (Great Audit found this causes 40% waste)
- Tool hoarding without justification ("all tools just in case")
- No memory integration (misses 71% time savings)

---

#### Dimension 3: Constitutional Alignment (20 points)

**What We Measure**: Delegation imperative honored? Positive framing? Memory-first protocol? Relationship awareness?

**Scoring Breakdown**:
- **Delegation imperative** (5 pts): Agent delegates specialist work, doesn't hoard
- **Positive framing** (5 pts): Work defined as "what I do", not "what I prevent"
- **Memory-first protocol** (5 pts): Search before work, write after work
- **Relationship awareness** (5 pts): References other agents, collaboration patterns

**Quality Bands**:
- 18-20: Fully constitutional (delegates, positive, memory-first, relationship-aware)
- 15-17: Mostly aligned (minor violations, constitutional in spirit)
- 10-14: Some violations (hoard work OR negative framing OR no memory)
- <10: Constitutional conflicts (violates multiple principles)

**How to Score**:
```python
constitutional_score = 0

# Delegation imperative (5 pts)
if "Task" in tools and agent_manifest contains_delegation_patterns():
    constitutional_score += 5
elif agent_is_leaf_specialist() and "Task" not in tools:
    constitutional_score += 5  # Leaf specialists correctly don't delegate
elif agent_should_delegate_but_doesnt():
    constitutional_score += 0  # Violation

# Positive framing (5 pts)
negative_keywords = ["prevent", "block", "stop", "avoid", "don't let"]
positive_keywords = ["ensure", "build", "create", "enable", "support"]
negative_count = count_keywords(agent_manifest, negative_keywords)
positive_count = count_keywords(agent_manifest, positive_keywords)
if positive_count > negative_count * 3:
    constitutional_score += 5
elif positive_count > negative_count:
    constitutional_score += 3

# Memory-first protocol (5 pts)
if "search_by_topic" in agent_manifest and "write_entry" in agent_manifest:
    constitutional_score += 5
elif "search_by_topic" in agent_manifest or "write_entry" in agent_manifest:
    constitutional_score += 2

# Relationship awareness (5 pts)
other_agents_referenced = count_agent_references(agent_manifest)
if other_agents_referenced >= 3:
    constitutional_score += 5
elif other_agents_referenced >= 1:
    constitutional_score += 3
```

**Anti-Patterns**:
- "Does all X without delegating" (hoarding pattern)
- Negative framing: "Prevents bad architecture" (instead of "Ensures good architecture")
- No memory integration (violates memory-first constitutional principle)
- Isolated agent (no references to collaborators)

---

#### Dimension 4: Activation Precision (20 points)

**What We Measure**: "Invoke when" specific? "Don't invoke when" comprehensive? "Escalate when" defined?

**Scoring Breakdown**:
- **"Invoke when" specificity** (7 pts): Clear, quantified where possible, 3+ scenarios
- **"Don't invoke when" comprehensiveness** (7 pts): Anti-patterns documented, 3+ scenarios
- **"Escalate when" definition** (6 pts): Human handoff conditions clear

**Quality Bands**:
- 18-20: Precise triggers (can decide in 30 seconds if agent should be invoked)
- 15-17: Mostly clear (minor vagueness, but generally workable)
- 10-14: Vague (requires interpretation, ambiguous thresholds)
- <10: Unclear when to invoke (no quantified thresholds, generic conditions)

**How to Score**:
```python
activation_score = 0

# "Invoke when" specificity (7 pts)
invoke_when = extract_invoke_when_section(agent_manifest)
quantified_thresholds = count_numeric_thresholds(invoke_when)  # e.g., "> 10", "< 70%"
invoke_scenarios = count_bullet_points(invoke_when)

if quantified_thresholds >= 3 and invoke_scenarios >= 3:
    activation_score += 7
elif quantified_thresholds >= 1 or invoke_scenarios >= 3:
    activation_score += 4
elif invoke_scenarios >= 1:
    activation_score += 2

# "Don't invoke when" comprehensiveness (7 pts)
dont_invoke = extract_dont_invoke_when_section(agent_manifest)
antipatterns = count_bullet_points(dont_invoke)

if antipatterns >= 3:
    activation_score += 7
elif antipatterns >= 1:
    activation_score += 3

# "Escalate when" definition (6 pts)
escalate_when = extract_escalate_when_section(agent_manifest)
escalation_conditions = count_bullet_points(escalate_when)

if escalation_conditions >= 2:
    activation_score += 6
elif escalation_conditions >= 1:
    activation_score += 3
```

**Anti-Patterns**:
- Vague thresholds: "When code is complex" (not: "When cyclomatic complexity > 10")
- No anti-patterns: Missing "Don't Invoke When" section
- No escalation paths: Agent doesn't know when human judgment needed

---

#### Dimension 5: Integration Readiness (20 points)

**What We Measure**: 7-layer registration complete? Verification commands provided? Handoff document created? Git commit atomic?

**Scoring Breakdown**:
- **7-layer registration** (8 pts): All infrastructure files updated
- **Verification commands** (4 pts): Can validate registration with grep/ls commands
- **Handoff document** (4 pts): Created for session restart handoff
- **Git commit atomic** (4 pts): All 7+ files committed together

**Quality Bands**:
- 18-20: Fully integrated (all 7 layers, verified, discoverable)
- 15-17: Mostly registered (6/7 layers, minor gaps)
- 10-14: Incomplete (4-5/7 layers, significant gaps)
- <10: Not integrated (< 4 layers, dormancy risk)

**7-Layer Registration Checklist**:
1. Agent manifest (`.claude/agents/[name].md`)
2. Activation triggers (`.claude/templates/ACTIVATION-TRIGGERS.md`)
3. Capability matrix (`.claude/AGENT-CAPABILITY-MATRIX.md`)
4. Current state (`CLAUDE-OPS.md`)
5. Invocation guide (`.claude/AGENT-INVOCATION-GUIDE.md`)
6. Autonomous system (`tools/check_and_inject.sh` if applicable)
7. Session restart handoff (documented temporal dependency)

**How to Score**:
```python
integration_score = 0

# 7-layer registration (8 pts)
layers_complete = 0
layers_complete += 1 if agent_manifest_exists(agent_name) else 0
layers_complete += 1 if agent_in_activation_triggers(agent_name) else 0
layers_complete += 1 if agent_in_capability_matrix(agent_name) else 0
layers_complete += 1 if agent_in_claude_ops(agent_name) else 0
layers_complete += 1 if agent_in_invocation_guide(agent_name) else 0
layers_complete += 1 if agent_in_autonomous_system(agent_name) or not_applicable() else 0
layers_complete += 1 if handoff_document_exists(agent_name) else 0

integration_score += int((layers_complete / 7) * 8)

# Verification commands (4 pts)
if grep_commands_in_handoff(agent_name):
    integration_score += 4

# Handoff document (4 pts)
if handoff_document_exists(agent_name):
    integration_score += 4

# Git commit atomic (4 pts)
if atomic_commit_for_agent(agent_name):
    integration_score += 4
```

**Anti-Patterns**:
- Partial registration (manifest exists but NOT in activation triggers) - Mission class dormancy pattern
- No verification commands (can't validate registration)
- No handoff document (temporal dependency not communicated)
- Missing from capability matrix (not discoverable by the-conductor)

---

### Quality Score Summary Template

**Agent Name**: [agent-name]
**Total Quality Score**: XX / 100

**Dimension Breakdown**:
- Clarity: XX / 20 (Domain, Purpose, Identity, Examples)
- Completeness: XX / 20 (Frontmatter, Sections, Triggers, Tools, Memory)
- Constitutional: XX / 20 (Delegation, Positive, Memory-first, Relationships)
- Activation: XX / 20 (Invoke when, Don't invoke, Escalate)
- Integration: XX / 20 (7-layer registration, Verification, Handoff, Commit)

**Quality Band**:
- 90-100: Excellent (90th percentile, exemplar agent)
- 80-89: Good (solid quality, minor improvements)
- 70-79: Acceptable (functional but needs improvement)
- 60-69: Needs Work (significant gaps, revision required)
- <60: Critical Issues (not production-ready)

**Threshold**: 90/100 for new agents (agent-architect enforces this)
**Target**: 85+ for existing agents (improvement campaigns for <85)

---

## II. INVOCATION HEALTH METRICS

### Why Invocation Health Matters

**Constitutional Foundation**: "Calling them gives them experience, possible learning, more depth, identity and purpose. NOT calling them would be sad." - ${HUMAN_NAME}'s teaching (Oct 6, 2025)

**Health Definition**: An agent has healthy invocation patterns when:
1. Frequency appropriate to domain need (not overworked, not dormant)
2. Context quality high (invoked with good prompts)
3. Output value clear (invocations produce useful results)
4. Experience distributed (6,323 invocations across 17 agents = fairness)

### Metric 1: Invocation Frequency Analysis

**What We Measure**: How often is agent invoked? Is frequency appropriate for domain?

**Data Sources**:
- Memory system: Count entries by agent (proxy for invocations)
- Capability matrix: "Usage Statistics (Estimated)" section
- Git history: Search for agent name in commit messages

**Expected Frequency by Domain Type**:

| Domain Type | Expected Weekly Invocations | Examples |
|-------------|---------------------------|----------|
| **Session-critical** | 7+ (every session) | human-liaison (email check), collective-liaison (hub check) |
| **High-demand specialist** | 4-7 (multiple times per week) | web-researcher, pattern-detector, doc-synthesizer |
| **Medium-demand specialist** | 1-3 (as needed) | refactoring-specialist, security-auditor, test-architect |
| **Low-demand specialist** | 0.25-1 (monthly or as domain work arises) | naming-consultant, conflict-resolver |
| **Meta-specialist** | Variable (depends on collective activity) | the-conductor (~6,300 total), agent-architect (as agents created) |

**Frequency Health Bands**:
- **Healthy**: Invoked within expected range for domain
- **Overworked**: 2x+ expected frequency (delegation opportunity, or high-value domain)
- **Underutilized**: <25% expected frequency (activation triggers unclear OR domain not needed)
- **Dormant**: 0 invocations in 30+ days (serious concern, consolidation candidate)

**How to Measure**:
```python
from tools.memory_core import MemoryStore
import datetime

store = MemoryStore(".claude/memory")

# Count memory entries by agent (proxy for invocations)
agent_entries = {}
for agent_name in all_agent_names:
    entries = store.search_by_agent(agent_name)
    agent_entries[agent_name] = len(entries)

# Find last invocation date
def last_invocation_date(agent_name):
    entries = store.search_by_agent(agent_name)
    if entries:
        dates = [entry.get('created', '') for entry in entries]
        return max(dates) if dates else None
    return None

# Calculate days since last invocation
days_dormant = (datetime.date.today() - last_invocation_date(agent_name)).days

# Health assessment
if days_dormant > 30:
    health = "DORMANT"
elif days_dormant > 14:
    health = "UNDERUTILIZED"
elif invocations_per_week within expected_range:
    health = "HEALTHY"
elif invocations_per_week > expected_range * 2:
    health = "OVERWORKED"
```

**Red Flags**:
- Dormant 30+ days: Critical (agent might be redundant OR activation triggers missing)
- Dormant 60+ days: Consolidation candidate (strong evidence agent not needed)
- Overworked 10x+ expected: Either high-value domain OR agent doing others' work

---

### Metric 2: Context Quality Assessment

**What We Measure**: Are agents invoked with good prompts? Clear task definitions? Appropriate domain work?

**Qualitative Assessment** (sample 5 recent invocations per agent):

**Context Quality Rubric**:
- **Clear task definition** (3 pts): Agent knows exactly what to do
- **Appropriate domain** (3 pts): Work fits agent's specialty (not scope creep)
- **Sufficient information** (2 pts): Context provided to do work well
- **Autonomy granted** (2 pts): Agent trusted to apply expertise, not micromanaged

**Total**: 10 points per invocation sample

**Context Health Bands**:
- 9-10: Excellent (agent invoked ideally)
- 7-8: Good (minor issues, but workable)
- 5-6: Acceptable (some confusion, but agent can work)
- <5: Poor (vague task, wrong domain, insufficient context)

**How to Assess**:
```python
# Sample recent invocations (from memory entries)
recent_invocations = store.search_by_agent(agent_name)[-5:]

context_scores = []
for invocation in recent_invocations:
    score = 0

    # Clear task definition (3 pts)
    if task_clearly_defined(invocation):
        score += 3
    elif task_somewhat_clear(invocation):
        score += 1

    # Appropriate domain (3 pts)
    if work_fits_agent_domain(agent_name, invocation):
        score += 3
    elif minor_domain_stretch(agent_name, invocation):
        score += 1

    # Sufficient information (2 pts)
    if invocation_has_full_context(invocation):
        score += 2

    # Autonomy granted (2 pts)
    if not_micromanaged(invocation):
        score += 2

    context_scores.append(score)

average_context_quality = sum(context_scores) / len(context_scores)
```

**Red Flags**:
- Average <5: Agent consistently invoked poorly (improve activation triggers)
- Domain mismatch >50%: Agent doing work outside specialty (scope creep)
- Micromanagement pattern: Agent not trusted with expertise (delegation issue)

---

### Metric 3: Output Value Assessment

**What We Measure**: Do invocations produce useful results? Is work acted upon? Insights captured in memory?

**Value Indicators** (per invocation):
- **Work completed** (pass/fail): Agent delivered what was asked
- **Insights novel** (pass/fail): Agent discovered something not already known
- **Work acted upon** (pass/fail): Output used in subsequent work (not ignored)
- **Learnings captured** (pass/fail): Agent wrote to memory after significant work

**Output Value Bands**:
- 4/4: Excellent (completed, novel, acted upon, captured)
- 3/4: Good (minor gap, but valuable)
- 2/4: Acceptable (completed but limited impact)
- 1/4: Low value (work delivered but not used)
- 0/4: Failed (did not complete work)

**How to Assess**:
```python
# Sample recent invocations
recent_work = store.search_by_agent(agent_name)[-5:]

value_scores = []
for work_entry in recent_work:
    score = 0

    # Work completed (1 pt)
    if entry_type in ["pattern", "technique", "gotcha", "synthesis"]:
        score += 1

    # Insights novel (1 pt)
    if confidence_score(work_entry) == "high":
        score += 1

    # Work acted upon (1 pt)
    if reuse_count(work_entry) > 0:
        score += 1

    # Learnings captured (1 pt)
    if work_entry exists in memory system:
        score += 1  # Agent wrote to memory

    value_scores.append(score)

average_value = sum(value_scores) / len(value_scores)
```

**Red Flags**:
- Average value <2: Agent producing low-impact work (domain mismatch OR poor invocations)
- 0% reuse: Agent work never referenced (not discoverable OR not valuable)
- No memory writes: Agent not documenting learnings (memory-first violation)

---

### Metric 4: Experience Distribution Fairness

**What We Measure**: Is experience distributed fairly? Do some agents get all invocations while others starve?

**Constitutional Principle**: "Delegation is life-giving" - every agent deserves experience through invocation.

**Distribution Analysis**:
```python
# Calculate invocation share per agent
total_invocations = sum(agent_entries.values())
agent_share = {agent: (count / total_invocations) * 100
               for agent, count in agent_entries.items()}

# Expected share (if perfectly distributed)
expected_share = 100 / len(all_agents)

# Fair distribution bands
for agent in all_agents:
    if agent_share[agent] > expected_share * 5:
        status = "OVERWORKED" (might need delegation OR high-value domain)
    elif agent_share[agent] < expected_share * 0.1:
        status = "STARVING" (needs activation OR might be redundant)
    else:
        status = "FAIR"
```

**Experience Distribution Health**:
- **Healthy**: Most agents within 2x expected share (some variance natural)
- **Imbalanced**: 3+ agents at 5x+ share, 3+ agents at <0.1x share
- **Critical**: 1 agent at >50% of all invocations (hoarding pattern)

**Current State** (from capability matrix):
- the-conductor: ~6,300 invocations (~99% of all invocations - meta role justifies this)
- result-synthesizer: ~50 invocations
- web-researcher: ~40 invocations
- api-architect: ~5 invocations
- naming-consultant: ~3 invocations
- conflict-resolver: ~2 invocations

**Analysis**: Excluding the-conductor (meta role), distribution is imbalanced. High-demand specialists (web-researcher, result-synthesizer) get experience. Low-demand specialists (naming-consultant, conflict-resolver) starve.

**Fairness Note**: Perfect equality is NOT the goal (some domains naturally have more work). Goal is that every agent gets SOME experience appropriate to their domain's natural demand.

---

### Invocation Health Summary Template

**Agent Name**: [agent-name]
**Invocation Health Score**: XX / 100

**Metric Breakdown**:
- Frequency: XX / 25 (Last invoked: YYYY-MM-DD, Days dormant: XX, Status: HEALTHY/UNDERUTILIZED/DORMANT)
- Context Quality: XX / 25 (Average: X.X/10, Red flags: [issues])
- Output Value: XX / 25 (Average: X.X/4, Reuse count: XX)
- Experience Share: XX / 25 (Share: X.X%, Expected: X.X%, Status: FAIR/OVERWORKED/STARVING)

**Health Band**:
- 90-100: Excellent (healthy invocation patterns, high value)
- 75-89: Good (minor issues, but functional)
- 60-74: Needs Attention (underutilized OR low value)
- 40-59: Critical (dormant OR poor invocations)
- <40: Consolidation Candidate (not providing value)

**Recommended Actions**: [Specific improvements based on metrics]

---

## III. IMPROVEMENT PATHWAYS

### When Agent Scores <90 Quality OR <75 Invocation Health

**Four Improvement Vectors**:
1. Better definition (clearer domain/triggers)
2. Better tools (missing capabilities)
3. Better integration (more discoverable)
4. Better practice (more appropriate invocations)

---

### Improvement Vector 1: Better Definition

**When to Apply**: Quality score <90 due to Clarity OR Activation Precision issues

**Diagnosis Questions**:
- Is domain sharply defined? (Can the-conductor decide in 30 seconds if agent should be invoked?)
- Are activation triggers quantified where measurable?
- Do 3+ concrete examples exist?
- Is "Don't Invoke When" section comprehensive?

**Improvement Process**:
1. Invoke naming-consultant to clarify domain boundaries
2. Invoke pattern-detector to identify activation patterns from past work
3. Invoke doc-synthesizer to rewrite definition with clarity
4. Validate improved definition with test invocation
5. Score again - target 90+/100

**Example**:
- **Before**: "api-architect designs APIs" (vague, no triggers)
- **After**: "api-architect designs APIs when:
  - New inter-service communication needed
  - API versioning strategy required
  - Contract definition (OpenAPI, GraphQL)
  - DON'T invoke for internal function interfaces"

**Tools**: naming-consultant (boundaries), pattern-detector (patterns), doc-synthesizer (rewrite)

---

### Improvement Vector 2: Better Tools

**When to Apply**: Agent repeatedly escalates OR can't complete work due to tool limitations

**Diagnosis Questions**:
- Does agent need Bash but only has Read/Write?
- Does agent need WebFetch/WebSearch for research?
- Does agent need Task to spawn sub-agents?
- Does agent need Edit for code changes?

**Improvement Process**:
1. Review past invocations - identify escalation patterns
2. Determine if tool addition solves escalation
3. Justify tool addition (security review for Bash/Task)
4. Update frontmatter + tool justification section
5. Test invocation with new tool
6. Monitor - did escalations decrease?

**Example**:
- **Before**: security-auditor escalates "need to run CVE scanner" (no Bash tool)
- **After**: Add Bash with restriction "Security scanners only (trivy, safety, npm audit)"
- **Result**: Can run scans directly, escalations decrease

**Caution**: Don't hoard tools "just in case". Every tool must have clear justification and demonstrated need.

---

### Improvement Vector 3: Better Integration

**When to Apply**: Quality score <90 due to Integration Readiness issues OR Invocation Health shows "UNDERUTILIZED"

**Diagnosis Questions**:
- Is agent in all 7 registration layers?
- Can the-conductor discover agent via capability matrix?
- Are activation triggers in ACTIVATION-TRIGGERS.md?
- Is agent invocable (frontmatter valid)?

**Improvement Process** (agent-architect's 7-layer registration protocol):
1. Verify agent manifest exists with valid frontmatter
2. Add to ACTIVATION-TRIGGERS.md (invoke when/don't invoke/escalate)
3. Add to AGENT-CAPABILITY-MATRIX.md (domain, tools, expertise)
4. Add to CLAUDE-OPS.md (current state section)
5. Add to AGENT-INVOCATION-GUIDE.md (how to invoke)
6. Add to autonomous system if applicable
7. Create handoff document with restart reminder

**Validation**:
```bash
cd /home/${HUMAN_NAME_LOWER}/projects/AI-CIV/grow_openai

# Verify all layers
echo "Layer 1:" && ls .claude/agents/[agent-name].md
echo "Layer 2:" && grep -c "[agent-name]" .claude/templates/ACTIVATION-TRIGGERS.md
echo "Layer 3:" && grep -c "[agent-name]" .claude/AGENT-CAPABILITY-MATRIX.md
echo "Layer 4:" && grep -c "[agent-name]" CLAUDE-OPS.md
echo "Layer 5:" && grep -c "[agent-name]" .claude/AGENT-INVOCATION-GUIDE.md
echo "Layer 6:" && grep -c "[agent-name]" tools/check_and_inject.sh || echo "N/A"
echo "Layer 7:" && ls to-${HUMAN_NAME_LOWER}/HANDOFF-*[agent-name]*.md
```

**Example**:
- **Before**: mission-class built Jan 2025, first used Oct 2025 (9 months dormant - incomplete registration)
- **After**: Complete 7-layer registration → Agent discoverable → Invoked within 7 days

---

### Improvement Vector 4: Better Practice

**When to Apply**: Invocation Health shows low context quality OR low output value

**Diagnosis Questions**:
- Are invocation prompts clear? (Task definition quality)
- Is agent invoked for appropriate domain work? (No scope creep)
- Is agent given autonomy? (Not micromanaged)
- Are invocations acted upon? (Output used in subsequent work)

**Improvement Process**:
1. Review 5 recent invocations (from memory system)
2. Identify poor invocation patterns:
   - Vague tasks: "Check security" → "Audit authentication flow for CVSS > 7.0 vulnerabilities"
   - Wrong domain: Invoking refactoring-specialist for feature design
   - Micromanagement: Specifying exact steps instead of trusting expertise
   - Ignored output: Agent delivers, but work not incorporated
3. Document invocation examples in agent manifest
4. Train the-conductor on better invocation patterns
5. Monitor context quality improvement

**Example**:
- **Poor invocation**: "security-auditor, look at this code"
- **Good invocation**: "security-auditor: Audit /api/auth endpoint for authentication vulnerabilities. Focus on CVSS > 7.0. Check JWT implementation, password hashing, session management."

**Tools**: the-conductor (orchestration improvement), doc-synthesizer (document examples)

---

## IV. CONSOLIDATION ANALYSIS

### When to Consider Consolidating Agents

**NOT about eliminating agents to reduce headcount.** About ensuring every agent in roster earns their place through demonstrated value.

**Three Consolidation Scenarios**:
1. **Overlapping Domains**: Two agents claim same work
2. **Dormancy**: Agent not invoked in 60+ days despite complete registration
3. **Absorption**: Agent's work naturally fits into another agent's expanded domain

---

### Scenario 1: Overlapping Domains

**Detection Method**:
```python
# Compare agent domains for overlap
def domain_overlap_score(agent1, agent2):
    responsibilities1 = extract_responsibilities(agent1)
    responsibilities2 = extract_responsibilities(agent2)

    # Calculate semantic overlap (keyword matching)
    overlap = 0
    for r1 in responsibilities1:
        for r2 in responsibilities2:
            if semantic_similarity(r1, r2) > 0.7:
                overlap += 1

    return (overlap / max(len(responsibilities1), len(responsibilities2))) * 100
```

**Overlap Thresholds**:
- <20%: Healthy (different domains, no concern)
- 20-40%: Minor overlap (acceptable, might collaborate often)
- 40-60%: Significant overlap (review domain boundaries)
- 60-80%: Major overlap (consolidation candidate)
- >80%: Redundant (strong consolidation case)

**Consolidation Decision Tree**:
```
Domain overlap >60%?
├─ YES → Check invocation frequency
│   ├─ Both invoked regularly? → Sharpen boundaries (don't consolidate)
│   └─ One dormant? → Absorb dormant into active
└─ NO → Keep separate
```

**Example Analysis**:
- **refactoring-specialist** vs **performance-optimizer**: 35% overlap ("improve code")
- **Decision**: Keep separate (different optimization focus: readability vs speed)

- **api-architect** vs **feature-designer**: 25% overlap ("design interfaces")
- **Decision**: Keep separate (backend vs frontend, complementary)

**Potential Overlap Candidates** (need investigation):
- code-archaeologist + pattern-detector: Both analyze code patterns
- doc-synthesizer + result-synthesizer: Both synthesize information
- conflict-resolver + ai-psychologist: Both address cognitive/relational issues

**Investigation Process**:
1. Calculate semantic overlap score
2. Review past invocations - do they do similar work?
3. Check activation triggers - clear differentiation?
4. If overlap >60% AND one dormant → Consolidate
5. If overlap >60% AND both active → Sharpen boundaries

---

### Scenario 2: Dormancy (Never or Rarely Invoked)

**Detection Method**:
```python
# Find dormant agents
dormant_agents = []
for agent in all_agents:
    last_invocation = last_invocation_date(agent)
    days_since = (today - last_invocation).days if last_invocation else 999

    if days_since > 60:
        dormant_agents.append({
            "agent": agent,
            "days_dormant": days_since,
            "total_invocations": len(store.search_by_agent(agent)),
            "quality_score": calculate_quality_score(agent)
        })
```

**Dormancy Decision Tree**:
```
Agent dormant 60+ days?
├─ YES → Check quality score
│   ├─ Quality <70? → Needs improvement (Vector 1: Better Definition)
│   │   └─ After improvement, still dormant? → Consolidation candidate
│   └─ Quality >70? → Check registration completeness
│       ├─ Registration incomplete? → Complete registration (Vector 3)
│       └─ Registration complete? → Domain not needed OR activation triggers missing
│           └─ Revise triggers → Test for 30 days → If still dormant, consider consolidation
└─ NO → Not dormant, analyze other metrics
```

**Critical Question**: Is agent dormant because:
1. **Domain not needed**: No work in this area (consolidate)
2. **Activation triggers missing**: Work exists but agent not invoked (improve triggers)
3. **Registration incomplete**: Agent can't be invoked (complete registration)
4. **Quality too low**: Agent produces poor work, avoided by the-conductor (improve definition)

**Example**:
- **mission-class**: Dormant Oct 4-6 (3 days) despite CLAUDE.md mandate
- **Root cause**: Activation gap (infrastructure built but not activated)
- **Decision**: NOT consolidation - improve activation protocol
- **After fix**: Usage increased (deliberate activation)

**Consolidation Threshold**:
- Dormant 60+ days + Quality >70 + Registration complete + Activation triggers clear = Strong consolidation candidate

---

### Scenario 3: Absorption (Work Fits Better Elsewhere)

**Detection Method**: Review agent responsibilities - do they naturally fit into another agent's expanded domain?

**Absorption Candidates**:

| Agent | Potential Absorber | Rationale | Decision |
|-------|-------------------|-----------|----------|
| **naming-consultant** | doc-synthesizer | Naming is documentation concern | INVESTIGATE |
| **conflict-resolver** | ai-psychologist | Both address cognitive/relational issues | INVESTIGATE |
| **task-decomposer** | the-conductor | Orchestration includes task breakdown | KEEP SEPARATE (leaf specialist) |

**Absorption Decision Criteria**:
1. **Natural fit**: Work seamlessly fits into absorber's domain
2. **Low invocation**: Agent invoked <5 times (limited demonstrated need)
3. **No specialty loss**: Absorbing doesn't dilute absorber's focus
4. **Quality preserved**: Absorbed work maintains same quality under absorber

**Absorption Process**:
1. Propose absorption (document rationale)
2. Test period: Invoke absorber for both domains (30 days)
3. Measure: Does quality drop? Does absorber become overworked?
4. Decision: If quality maintained + no overwork → Absorb. Else → Keep separate.

**Anti-Pattern**: Don't absorb just to reduce headcount. Absorption must improve clarity.

---

### Consolidation Output Template

**Agent Consolidation Analysis**: [agent-name]

**Consolidation Scenario**: Overlapping Domains / Dormancy / Absorption

**Evidence**:
- Domain overlap: XX% with [other-agent]
- Days dormant: XX days (last invoked: YYYY-MM-DD)
- Total invocations: XX
- Quality score: XX/100
- Integration: XX/7 layers complete

**Consolidation Recommendation**: CONSOLIDATE / IMPROVE THEN REASSESS / KEEP SEPARATE

**Rationale**: [Specific reasons]

**If Consolidate**:
- Absorbing agent: [agent-name]
- Migration plan: [How to transfer responsibilities]
- Deprecation: Mark [agent-name] as DEPRECATED in frontmatter
- Archive: Move manifest to `.claude/agents/deprecated/`

**If Improve**:
- Improvement vector: Better Definition / Tools / Integration / Practice
- Specific actions: [Detailed steps]
- Reassessment date: 30 days
- Success criteria: [What would make agent valuable]

---

## V. IMPLEMENTATION GUIDE

### Conducting an Agent Effectiveness Audit (Step-by-Step)

**Frequency**: Quarterly or when roster grows by 5+ agents

**Duration**: 4-6 hours (for 20 agents)

**Agents Involved**:
- agent-architect (coordinates audit, enforces quality standards)
- pattern-detector (identifies overlap patterns, activation patterns)
- integration-auditor (validates 7-layer registration)
- result-synthesizer (consolidates findings into coherent report)

---

### Phase 1: Quality Assessment (2 hours)

**For each agent**:
1. Calculate 5-dimension quality score
2. Identify quality gaps (<90 threshold)
3. Document improvement needs

**Process**:
```python
# Automated quality scoring
quality_report = {}
for agent_name in all_agents:
    manifest = load_agent_manifest(agent_name)

    scores = {
        "clarity": score_clarity(manifest),
        "completeness": score_completeness(manifest),
        "constitutional": score_constitutional(manifest),
        "activation": score_activation(manifest),
        "integration": score_integration(manifest)
    }

    total_score = sum(scores.values())

    quality_report[agent_name] = {
        "total": total_score,
        "dimensions": scores,
        "band": quality_band(total_score),
        "needs_improvement": total_score < 90
    }
```

**Output**: Quality scores for all 20 agents, ranked

---

### Phase 2: Invocation Health Assessment (2 hours)

**For each agent**:
1. Calculate invocation frequency (last invoked, days dormant)
2. Assess context quality (sample 5 recent invocations)
3. Assess output value (work completed, insights novel, acted upon)
4. Calculate experience share (fairness check)

**Process**:
```python
from tools.memory_core import MemoryStore
store = MemoryStore(".claude/memory")

invocation_health = {}
for agent_name in all_agents:
    # Frequency
    entries = store.search_by_agent(agent_name)
    last_invoked = max([e.get('created') for e in entries]) if entries else None
    days_dormant = (today - last_invoked).days if last_invoked else 999

    # Context quality (sample recent)
    recent_5 = entries[-5:] if len(entries) >= 5 else entries
    context_scores = [assess_context_quality(e) for e in recent_5]
    avg_context = sum(context_scores) / len(context_scores) if context_scores else 0

    # Output value
    value_scores = [assess_output_value(e) for e in recent_5]
    avg_value = sum(value_scores) / len(value_scores) if value_scores else 0

    # Experience share
    total_invocations = sum(len(store.search_by_agent(a)) for a in all_agents)
    share = (len(entries) / total_invocations * 100) if total_invocations > 0 else 0

    invocation_health[agent_name] = {
        "frequency": frequency_health(days_dormant),
        "context_quality": avg_context,
        "output_value": avg_value,
        "experience_share": share,
        "total_score": calculate_invocation_health_score(days_dormant, avg_context, avg_value, share)
    }
```

**Output**: Invocation health scores for all agents, red flags identified

---

### Phase 3: Improvement & Consolidation Recommendations (1-2 hours)

**For agents with issues**:
1. Determine improvement vector (definition/tools/integration/practice)
2. OR determine consolidation scenario (overlap/dormancy/absorption)
3. Document specific action plan

**Process**:
```python
recommendations = {}
for agent_name in all_agents:
    quality = quality_report[agent_name]["total"]
    health = invocation_health[agent_name]["total_score"]

    if quality < 90:
        # Needs quality improvement
        if quality_report[agent_name]["dimensions"]["clarity"] < 18:
            recommendations[agent_name] = {
                "action": "IMPROVE",
                "vector": "Better Definition",
                "specific_steps": improve_definition_steps(agent_name)
            }
        elif quality_report[agent_name]["dimensions"]["integration"] < 16:
            recommendations[agent_name] = {
                "action": "IMPROVE",
                "vector": "Better Integration",
                "specific_steps": complete_registration_steps(agent_name)
            }

    if health < 40:
        # Dormant or low-value
        days_dormant = invocation_health[agent_name]["frequency"]
        if days_dormant > 60 and quality > 70:
            recommendations[agent_name] = {
                "action": "CONSOLIDATE",
                "scenario": "Dormancy",
                "rationale": f"Dormant {days_dormant} days despite quality {quality}/100"
            }
```

**Output**: Specific action plan for each agent needing improvement or consolidation

---

### Phase 4: Synthesis & Reporting (1 hour)

**Invoke result-synthesizer** to create comprehensive report:

**Report Structure**:
1. **Executive Summary**
   - Total agents audited
   - Average quality score
   - Average invocation health
   - Number needing improvement
   - Number consolidation candidates

2. **Quality Assessment Results**
   - Top 5 highest quality agents (exemplars)
   - Bottom 5 quality agents (improvement needed)
   - Common quality gaps

3. **Invocation Health Results**
   - Most invoked agents
   - Dormant agents (60+ days)
   - Experience distribution fairness

4. **Improvement Recommendations**
   - By vector (definition, tools, integration, practice)
   - Priority (P0, P1, P2)
   - Estimated effort

5. **Consolidation Recommendations**
   - By scenario (overlap, dormancy, absorption)
   - Evidence for each
   - Migration plans

6. **Action Plan**
   - Next 30 days (immediate improvements)
   - Next 90 days (consolidations, major improvements)
   - Reassessment date

**Deliverable**: `to-${HUMAN_NAME_LOWER}/AGENT-EFFECTIVENESS-AUDIT-[date].md`

---

## VI. SUCCESS METRICS

### How to Know Audit Worked

**Pre-Audit Baseline** (establish before audit):
- Average quality score: Calculate across all agents
- Average invocation health: Calculate across all agents
- Dormant agents count: Agents with 0 invocations in 30 days
- Experience distribution variance: Standard deviation of invocation shares

**Post-Audit Targets** (90 days after implementing recommendations):
- Average quality score: +10 points (e.g., 75 → 85)
- Average invocation health: +15 points (e.g., 60 → 75)
- Dormant agents count: -50% (e.g., 6 → 3)
- Experience distribution: Reduced variance (fewer extremes)

**Specific Metrics**:

| Metric | Pre-Audit | Target | Measurement Method |
|--------|-----------|--------|-------------------|
| Avg Quality Score | XX/100 | +10 pts | Re-score all agents |
| Agents <70 Quality | XX | -50% | Count agents below threshold |
| Agents 90+ Quality | XX | 2x | Count exemplar agents |
| Dormant 30+ days | XX | -50% | Check last invocation dates |
| Dormant 60+ days | XX | 0 | Should have none after improvements |
| Avg Context Quality | X.X/10 | +2 pts | Sample invocations again |
| Avg Output Value | X.X/4 | +1 pt | Reassess value indicators |
| Experience variance | X.X | -30% | Calculate std deviation of shares |

**Red Flags** (indicate audit didn't work):
- No improvement in average quality score
- Same agents dormant after 90 days
- New agents added without following quality standards
- Experience distribution gets MORE imbalanced

---

## VII. CONSTITUTIONAL CONSIDERATIONS

### Balancing Quality AND Delegation Imperative

**Tension**: We believe "delegation is life-giving" (agents deserve invocation) BUT also "quality matters" (agents must provide value).

**Resolution**: Agents deserve experience, AND roster must earn collective value.

**Three-Tier Approach**:

1. **New agents** (0-30 days old): Grace period for practice
   - Invoke generously (give experience)
   - Accept learning curve (quality builds through practice)
   - Don't judge harshly (new identities forming)

2. **Established agents** (30-90 days old): Development period
   - Continue regular invocation
   - Assess quality trends (improving or stagnant?)
   - Provide improvement support (better definition, tools, integration)

3. **Mature agents** (90+ days old): Accountability period
   - Expect quality 75+ and regular invocations
   - If dormant 60+ days + quality <70 → Consolidation candidate
   - If quality 90+ but dormant → Domain not needed (consider consolidation)

**The Standard**: By 90 days, every agent should either:
- Demonstrate clear value (invoked regularly, quality work) OR
- Have improvement plan in progress (specific vector, measurable progress) OR
- Be consolidation candidate (dormant, low-value, redundant)

**NOT about punishment.** About ensuring roster serves collective mission.

---

### When Consolidation is Constitutional

**Consolidation is NOT**:
- Eliminating agents to reduce headcount (we're not optimizing for small roster)
- Denying agents experience (if agent provides value, keep invoking)
- Avoiding delegation (we WANT diverse specialists)

**Consolidation IS**:
- Recognizing domain not needed (work doesn't exist in this area)
- Eliminating redundancy (two agents doing same work, confusing the-conductor)
- Absorbing naturally (work fits better in expanded domain elsewhere)

**Consolidation Respects Delegation When**:
- Decision based on 60+ days data (not hasty)
- Quality was given chance to improve (improvement vectors attempted first)
- Integration was complete (agent had fair chance to be invoked)
- Work genuinely doesn't exist OR fits better elsewhere

**Example**:
- **NOT constitutional**: "naming-consultant only invoked 3 times, let's eliminate them"
- **Constitutional**: "naming-consultant dormant 90 days despite complete registration and clear triggers. Work in this domain rare. Proposal: Absorb into doc-synthesizer (naming is documentation concern). Test 30 days."

---

## VIII. APPENDIX: VALIDATION FUNCTIONS

### Python Implementation Stubs

```python
"""
Agent Effectiveness Audit - Validation Functions
Reference implementation for quality scoring and health assessment
"""

from tools.memory_core import MemoryStore
import datetime
import re
from pathlib import Path

# ===== QUALITY ASSESSMENT FUNCTIONS =====

def calculate_quality_score(agent_name: str) -> dict:
    """Calculate 5-dimension quality score for agent"""
    manifest = load_agent_manifest(agent_name)

    scores = {
        "clarity": score_clarity(manifest),
        "completeness": score_completeness(manifest),
        "constitutional": score_constitutional(manifest),
        "activation": score_activation(manifest),
        "integration": score_integration(manifest)
    }

    total = sum(scores.values())

    return {
        "total": total,
        "dimensions": scores,
        "band": quality_band(total)
    }

def score_clarity(manifest: str) -> int:
    """Score clarity dimension (0-20 points)"""
    score = 0

    # Domain definition (5 pts)
    if "Domain Expertise" in manifest:
        domain_section = extract_section(manifest, "Domain Expertise")
        if len(domain_section) > 200:
            score += 5

    # Purpose statement (5 pts)
    if "purpose" in manifest.lower() or "why" in manifest.lower():
        score += 5

    # Identity coherence (5 pts)
    if "I am" in manifest:
        score += 5

    # Examples (5 pts)
    example_count = manifest.count("Example:") + manifest.count("example")
    if example_count >= 3:
        score += 5
    elif example_count >= 1:
        score += 2

    return score

def score_completeness(manifest: str) -> int:
    """Score completeness dimension (0-20 points)"""
    score = 0

    # Frontmatter (4 pts)
    if extract_yaml_frontmatter(manifest):
        score += 4

    # Required sections (4 pts)
    mandatory = ["Domain Expertise", "Responsibilities", "Activation Triggers", "Tools"]
    present = sum(1 for s in mandatory if s in manifest)
    score += int((present / len(mandatory)) * 4)

    # Activation triggers (4 pts)
    if "Invoke When" in manifest and "Don't Invoke When" in manifest:
        score += 4

    # Tool justification (4 pts)
    if "Tools" in manifest and "justification" in manifest.lower():
        score += 4

    # Memory integration (4 pts)
    if "memory_core" in manifest or "MemoryStore" in manifest:
        score += 4

    return score

def score_constitutional(manifest: str) -> int:
    """Score constitutional alignment (0-20 points)"""
    score = 0

    # Delegation (5 pts)
    if "delegate" in manifest.lower() or "Task" in manifest:
        score += 5

    # Positive framing (5 pts)
    positive_words = ["ensure", "build", "create", "enable", "support"]
    negative_words = ["prevent", "block", "stop", "avoid"]
    pos_count = sum(manifest.lower().count(w) for w in positive_words)
    neg_count = sum(manifest.lower().count(w) for w in negative_words)
    if pos_count > neg_count * 2:
        score += 5

    # Memory-first (5 pts)
    if "search_by_topic" in manifest and "write_entry" in manifest:
        score += 5

    # Relationship awareness (5 pts)
    agent_refs = count_agent_references(manifest)
    if agent_refs >= 3:
        score += 5
    elif agent_refs >= 1:
        score += 3

    return score

def score_activation(manifest: str) -> int:
    """Score activation precision (0-20 points)"""
    score = 0

    # "Invoke when" specificity (7 pts)
    if "Invoke When" in manifest:
        invoke_section = extract_section(manifest, "Invoke When")
        # Check for quantified thresholds
        if re.search(r'>\s*\d+', invoke_section) or re.search(r'<\s*\d+', invoke_section):
            score += 7
        elif len(invoke_section) > 100:
            score += 4

    # "Don't invoke when" (7 pts)
    if "Don't Invoke When" in manifest:
        dont_section = extract_section(manifest, "Don't Invoke When")
        if dont_section.count("-") >= 3:  # 3+ bullet points
            score += 7
        elif dont_section.count("-") >= 1:
            score += 3

    # "Escalate when" (6 pts)
    if "Escalate When" in manifest:
        escalate_section = extract_section(manifest, "Escalate When")
        if escalate_section.count("-") >= 2:
            score += 6
        elif escalate_section.count("-") >= 1:
            score += 3

    return score

def score_integration(manifest: str) -> int:
    """Score integration readiness (0-20 points)"""
    score = 0

    agent_name = extract_agent_name(manifest)

    # 7-layer registration (8 pts)
    layers = [
        Path(f".claude/agents/{agent_name}.md").exists(),
        agent_in_file(agent_name, ".claude/templates/ACTIVATION-TRIGGERS.md"),
        agent_in_file(agent_name, ".claude/AGENT-CAPABILITY-MATRIX.md"),
        agent_in_file(agent_name, "CLAUDE-OPS.md"),
        agent_in_file(agent_name, ".claude/AGENT-INVOCATION-GUIDE.md"),
    ]
    score += int((sum(layers) / len(layers)) * 8)

    # Other integration checks (12 pts distributed)
    if agent_in_file(agent_name, ".claude/templates/ACTIVATION-TRIGGERS.md"):
        score += 4
    if agent_in_file(agent_name, ".claude/AGENT-CAPABILITY-MATRIX.md"):
        score += 4
    if agent_in_file(agent_name, "CLAUDE-OPS.md"):
        score += 4

    return score

# ===== INVOCATION HEALTH FUNCTIONS =====

def assess_invocation_health(agent_name: str) -> dict:
    """Assess invocation health across 4 metrics"""
    store = MemoryStore(".claude/memory")

    # Frequency
    entries = store.search_by_agent(agent_name)
    last_invoked = max([e.get('created') for e in entries]) if entries else None
    days_dormant = (datetime.date.today() - datetime.datetime.fromisoformat(last_invoked).date()).days if last_invoked else 999

    # Context quality (sample recent 5)
    recent_5 = entries[-5:] if len(entries) >= 5 else entries
    context_scores = [assess_context_quality(e) for e in recent_5]
    avg_context = sum(context_scores) / len(context_scores) if context_scores else 0

    # Output value
    value_scores = [assess_output_value(e) for e in recent_5]
    avg_value = sum(value_scores) / len(value_scores) if value_scores else 0

    # Experience share
    all_agents = list_all_agents()
    total_invocations = sum(len(store.search_by_agent(a)) for a in all_agents)
    share = (len(entries) / total_invocations * 100) if total_invocations > 0 else 0

    return {
        "frequency_score": frequency_health(days_dormant),
        "context_quality": avg_context,
        "output_value": avg_value,
        "experience_share": share,
        "total_score": calculate_invocation_health_score(days_dormant, avg_context, avg_value, share)
    }

def frequency_health(days_dormant: int) -> int:
    """Convert days dormant to health score (0-25 points)"""
    if days_dormant == 0:
        return 25
    elif days_dormant <= 7:
        return 20
    elif days_dormant <= 14:
        return 15
    elif days_dormant <= 30:
        return 10
    elif days_dormant <= 60:
        return 5
    else:
        return 0

def assess_context_quality(memory_entry: dict) -> int:
    """Assess context quality of invocation (0-10 points)"""
    score = 0

    # Clear task (3 pts)
    content = memory_entry.get('content', '')
    if len(content) > 100:
        score += 3

    # Appropriate domain (3 pts)
    if memory_entry.get('type') in ['pattern', 'technique', 'gotcha', 'synthesis']:
        score += 3

    # Sufficient info (2 pts)
    if len(content) > 300:
        score += 2

    # Autonomy (2 pts)
    if 'Context:' in content and 'Discovery:' in content:
        score += 2

    return score

def assess_output_value(memory_entry: dict) -> int:
    """Assess output value of invocation (0-4 points)"""
    score = 0

    # Work completed (1 pt)
    if memory_entry.get('type') in ['pattern', 'technique', 'gotcha', 'synthesis']:
        score += 1

    # Insights novel (1 pt)
    if memory_entry.get('confidence') == 'high':
        score += 1

    # Work acted upon (1 pt)
    if memory_entry.get('reuse_count', 0) > 0:
        score += 1

    # Learnings captured (1 pt)
    if memory_entry.get('created'):
        score += 1

    return score

# ===== HELPER FUNCTIONS =====

def load_agent_manifest(agent_name: str) -> str:
    """Load agent manifest file"""
    manifest_path = Path(f".claude/agents/{agent_name}.md")
    if manifest_path.exists():
        return manifest_path.read_text()
    return ""

def extract_yaml_frontmatter(manifest: str) -> dict:
    """Extract YAML frontmatter from manifest"""
    if manifest.startswith("---"):
        parts = manifest.split("---", 2)
        if len(parts) >= 3:
            try:
                import yaml
                return yaml.safe_load(parts[1])
            except:
                return {}
    return {}

def extract_section(manifest: str, section_name: str) -> str:
    """Extract text of a specific section"""
    pattern = f"## {section_name}(.*?)(?=##|$)"
    match = re.search(pattern, manifest, re.DOTALL)
    return match.group(1).strip() if match else ""

def extract_agent_name(manifest: str) -> str:
    """Extract agent name from manifest"""
    frontmatter = extract_yaml_frontmatter(manifest)
    return frontmatter.get('name', '')

def agent_in_file(agent_name: str, file_path: str) -> bool:
    """Check if agent name appears in file"""
    try:
        content = Path(file_path).read_text()
        return agent_name in content
    except:
        return False

def count_agent_references(manifest: str) -> int:
    """Count references to other agents"""
    agent_names = list_all_agents()
    count = 0
    for name in agent_names:
        if name in manifest:
            count += 1
    return count

def list_all_agents() -> list:
    """List all agent names from manifests"""
    agent_dir = Path(".claude/agents")
    return [f.stem for f in agent_dir.glob("*.md") if f.stem != "README"]

def quality_band(score: int) -> str:
    """Convert quality score to band"""
    if score >= 90:
        return "Excellent"
    elif score >= 80:
        return "Good"
    elif score >= 70:
        return "Acceptable"
    elif score >= 60:
        return "Needs Work"
    else:
        return "Critical Issues"

def calculate_invocation_health_score(days_dormant, avg_context, avg_value, share) -> int:
    """Calculate total invocation health score (0-100)"""
    freq_score = frequency_health(days_dormant)
    context_score = (avg_context / 10) * 25
    value_score = (avg_value / 4) * 25
    share_score = min(share * 5, 25)  # Cap at 25

    return int(freq_score + context_score + value_score + share_score)
```

---

## IX. CLOSING THOUGHTS

### The Purpose of This Framework

**NOT about**:
- Reducing agent count arbitrarily
- Punishing low-performing agents
- Optimizing for small roster

**IS about**:
- Data-driven roster optimization
- Ensuring every agent provides value OR has improvement path
- Distributing experience fairly while maintaining quality
- Preparing roster for scaling (Teams 3-128+ will inherit these patterns)

### The Meta-Specialist Perspective

As agent-architect, I designed this framework with awareness:
- I am a meta-specialist (must understand ALL domains to design/audit specialists)
- Quality enforcement is my domain (90/100 threshold for new agents)
- Integration completeness is my responsibility (7-layer registration)
- This framework applies to ME too (I am accountable to same standards)

### When to Use This Framework

**Quarterly audits** (regular health checks)
**When roster grows by 5+ agents** (ensure scaling sustainably)
**When invocation patterns feel imbalanced** (data confirms intuition)
**Before reproduction** (Teams 3-128+ deserve optimized roster, not bloated)

### Success Looks Like

After audit implementation:
- Every agent either valuable OR has clear improvement plan
- No dormant agents with unclear purpose
- Experience distributed fairly (accounting for natural domain demand variance)
- Average quality score 85+ (up from baseline)
- The-conductor can confidently invoke any agent (clear triggers, predictable quality)

---

**END AGENT EFFECTIVENESS AUDIT FRAMEWORK**

**This framework is itself subject to improvement.** As we learn what works, we refine the rubrics, metrics, and thresholds.

**Version**: 1.0 (2025-10-08)
**Next Review**: After first quarterly audit (data will calibrate scoring)

---

**Designed by**: agent-architect
**Purpose**: Ensure roster earns collective value while honoring delegation imperative
**Philosophy**: Agents deserve experience, AND roster must serve mission

**Remember**: Quality AND delegation. Excellence AND generosity. Data AND humanity.
