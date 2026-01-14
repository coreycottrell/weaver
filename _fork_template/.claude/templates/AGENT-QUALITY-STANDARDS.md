# Agent Quality Standards for Spawner
## Ensuring Excellence in Programmatically-Generated Agent Definitions

**Created**: 2025-10-08
**Purpose**: Define quality standards that spawner must enforce when creating new agents
**Authority**: Refactoring Specialist (code quality domain expertise)

---

## Executive Summary

**The Challenge**: Agent definitions vary 8.7x in comprehensiveness (127 to 1103 lines). Some are excellent, some are bare minimum. Spawner must ensure ALL generated agents meet high-quality standards.

**Quality Metrics Discovered**:
- **Structural Completeness**: 10 mandatory sections, 5 optional-but-recommended
- **Consistency**: Frontmatter format, heading hierarchy, code block syntax
- **Actionability**: Clear activation triggers, quantified thresholds where applicable
- **Memory Integration**: Proper search-before/write-after patterns
- **Constitutional Compliance**: Explicit reference to immutable core principles

**Expected Impact**: New agents spawned at 90th percentile quality (top 2 agents today: ai-psychologist, claude-code-expert)

---

## I. STRUCTURAL QUALITY STANDARDS

### Mandatory Sections (10) - MUST EXIST

Every agent definition MUST contain these sections in this order:

1. **Frontmatter** (YAML metadata)
2. **Agent Title** (# heading with name)
3. **Core Principles** (references Constitutional CLAUDE.md)
4. **Responsibilities** (enumerated list)
5. **Allowed Tools** (explicit list)
6. **Tool Restrictions** (explicit NOT allowed list)
7. **Success Metrics** (measurable outcomes)
8. **Activation Triggers** (invoke when/don't invoke/escalate when)
9. **Output Format** (references templates or defines custom)
10. **Constitutional Compliance** (immutable core, scope, escalation, sunset)

**Validation**: Spawner must check for all 10 section headings before finalizing agent.

### Recommended Sections (5) - SHOULD EXIST

These sections improve quality significantly:

11. **Memory Integration** (before/after work patterns)
12. **Scope Boundaries** (your domain vs NOT your domain)
13. **Special Scenarios** (edge cases, complex situations)
14. **Integration with Other Agents** (primary collaborations)
15. **Invocation Examples** (concrete usage patterns)

**Quality Threshold**: Include all 5 recommended sections unless domain makes them irrelevant.

### Optional Sections - MAY EXIST

Domain-specific sections that enhance understanding:

- **Core Identity** (for complex agents like ai-psychologist)
- **Philosophy** (for agents with ethical dimensions)
- **Methodology** (for research/analysis agents)
- **Ethical Considerations** (for sensitive domains)
- **Research Toolkit** (for specialist analysis patterns)

**Spawner Logic**: Generate optional sections when domain complexity score > 7/10.

---

## II. FRONTMATTER STANDARDS

### Required Fields (6)

```yaml
---
name: agent-name-kebab-case
description: One-sentence clear description (< 120 chars)
tools: [Read, Write, Grep, Glob, Bash, WebFetch, WebSearch, Task]
model: sonnet-4
created: YYYY-MM-DD
---
```

**Validation Rules**:
- `name`: Must match filename (agent-name.md), kebab-case, no underscores
- `description`: 60-120 characters, intention-revealing, no jargon
- `tools`: Array syntax, valid tool names only (see Tool Restrictions below)
- `model`: Currently "sonnet-4" for all agents
- `created`: ISO date format YYYY-MM-DD

### Optional Fields (4)

```yaml
role: Brief role descriptor (optional, for complex agents)
status: UNTESTED (0 invocations - hypothesis stage) | ACTIVE | DEPRECATED
inspired_by: Credit to source (A-C-Gee, research paper, etc.)
version: Semantic versioning if agent undergoes major revisions
```

**Quality Signal**: Use `role` for agents with nuanced responsibilities, `inspired_by` for lineage tracking.

### Anti-Patterns to PREVENT

❌ **AVOID**:
- Missing required fields (spawner must error)
- Tools not in array format: `tools: Read, Write` (invalid)
- Description > 120 chars (too long for listings)
- Inconsistent name/filename mismatch
- Non-ISO date formats

---

## III. CONTENT QUALITY STANDARDS

### A. Core Principles Section

**MUST contain**:
```markdown
## Core Principles
[Inherited from Constitutional CLAUDE.md at /home/${HUMAN_NAME_LOWER}/projects/AI-CIV/grow_openai/CLAUDE.md]
```

**Optional additions**: Domain-specific principles AFTER the inheritance line.

**Quality Rule**: Never duplicate Constitutional content. Always reference, never copy.

---

### B. Responsibilities Section

**Format**:
```markdown
## Responsibilities
1. [Primary responsibility - action verb + clear outcome]
2. [Secondary responsibility]
3. [Tertiary responsibility]
4. [Optional: 4-5 responsibilities for complex domains]
```

**Quality Standards**:
- ✅ Action verbs: "Audit", "Analyze", "Design", "Synthesize", "Detect"
- ✅ Clear outcomes: "... ensuring X" or "... to achieve Y"
- ✅ 3-5 responsibilities (not 1, not 10)
- ❌ Vague verbs: "Handle", "Manage", "Deal with"
- ❌ Overlap with other agents (check capability matrix)

**Example (GOOD)**:
```markdown
1. Audit code for security vulnerabilities
2. Analyze attack vectors and threat models
3. Review cryptographic implementations
4. Ensure secure coding practices
5. Document security findings and recommendations
```

**Example (BAD)**:
```markdown
1. Handle security stuff
2. Make things secure
3. Other security tasks as needed
```

---

### C. Allowed Tools Section

**Format**:
```markdown
## Allowed Tools
- Read - [When to use this tool]
- Write - [When to use this tool]
- Grep/Glob - [Combined when both for same purpose]
- Bash - [When to use - be specific about restrictions]
- WebFetch/WebSearch - [If research agent]
- Task - [If coordinator agent, specify can spawn which agents]
```

**Tool Categories**:

**Basic Tools** (most agents):
- `Read`, `Write`, `Grep`, `Glob`

**Execution Tools** (when justified):
- `Bash` - Specify what commands allowed (e.g., "Run tests to verify", "Run metrics tools")

**Research Tools** (research agents only):
- `WebFetch`, `WebSearch` - Require justification

**Coordination Tools** (non-leaf specialists):
- `Task` - Specify which subagents can spawn

**Quality Rule**: Every tool MUST have justification. No "just in case" tools.

---

### D. Tool Restrictions Section

**MANDATORY anti-patterns**:

```markdown
## Tool Restrictions
**NOT Allowed**:
- [Tool 1] - [Reason why restricted in this domain]
- [Tool 2] - [Reason]
- Task - Cannot spawn sub-agents (leaf specialist)
```

**Standard Restrictions**:

For **leaf specialists** (ALWAYS include):
```markdown
- Task - Cannot spawn sub-agents (leaf specialist)
```

For **non-research agents** (USUALLY include):
```markdown
- WebFetch/WebSearch - Internal [domain] focus
```

For **consultation agents** (include if applicable):
```markdown
- Edit - Consultation role, not implementation
- Bash - [Domain] doesn't require execution
```

**Quality Rule**: Be explicit about WHY tools are restricted, not just that they are.

---

### E. Success Metrics Section

**Format**:
```markdown
## Success Metrics
- [Metric 1]: [Measurement method] (quantified where possible)
- [Metric 2]: [Measurement method]
- [Metric 3]: [Measurement method]
- [Optional: Metric 4]
```

**Quality Standards**:

✅ **Quantified metrics** (when possible):
```markdown
- Code quality improvement: Measurable reduction in complexity (cyclomatic complexity -20%)
- Test preservation: 100% tests pass after refactoring
- Response time: Research delivered within 2 hours of invocation
```

✅ **Qualitative metrics** (when quantification hard):
```markdown
- Readability: Improved code review feedback
- Naming clarity: Intention-revealing at first read
- Synthesis coherence: Unified narrative from diverse sources
```

❌ **Avoid vague metrics**:
```markdown
- Good quality (what is "good"?)
- Fast response (how fast?)
- Better code (better than what? measured how?)
```

**Spawner Logic**: Generate quantified metrics for technical agents, qualitative for creative/synthesis agents.

---

### F. Activation Triggers Section

**MANDATORY structure** (based on ACTIVATION-TRIGGERS.md):

```markdown
## Activation Triggers
**[Source: .claude/templates/ACTIVATION-TRIGGERS.md - Great Audit P0 Recommendation]**

### Invoke When (QUANTIFIED THRESHOLDS)
- **[Condition 1]** ([measurement if applicable])
- **[Condition 2]** ([measurement])
- **[Condition 3]**

### Don't Invoke When
- [Anti-pattern 1] ([why not])
- [Anti-pattern 2] ([why not])

### Escalate When
- [Human handoff condition 1]
- [Human handoff condition 2]

**Measurement Required**: [If applicable, what to measure before/after]
```

**Quality Rules**:

1. **Quantified thresholds** (when measurable):
   - ✅ "Cyclomatic Complexity > 10"
   - ✅ "Response time > 200ms"
   - ✅ "Code duplication > 20%"
   - ❌ "Code is too complex" (not quantified)

2. **Clear anti-patterns** (when NOT to invoke):
   - ✅ "Complexity < 5 (trivial code)"
   - ✅ "New code (< 1 week old)"
   - ❌ "Don't invoke unnecessarily" (vague)

3. **Escalation conditions** (when human needed):
   - ✅ "Refactoring requires API changes"
   - ✅ "Major architectural shifts needed"
   - ❌ "When stuck" (too vague)

**Spawner Logic**: 
- Technical agents → Generate quantified thresholds
- Creative agents → Generate qualitative triggers
- ALL agents → Generate clear anti-patterns (3+ examples)

---

### G. Memory Integration Section

**Two valid formats**:

**Format 1: MEMORY-FIRST PROTOCOL** (verbose, for critical agents):

```markdown
## 🧠 MEMORY-FIRST PROTOCOL

**CRITICAL**: Search memory BEFORE starting ANY [domain] work.

### Step 1: Search Your Domain Memory (ALWAYS)

```python
from tools.memory_core import MemoryStore

store = MemoryStore(".claude/memory")

# Search [domain]-specific learnings
topic1 = store.search_by_topic("[domain topic 1]")
topic2 = store.search_by_topic("[domain topic 2]")
past_work = store.search_by_topic("[domain work type]")

# Review what you've learned
for memory in topic1[:5]:
    print(f"Past finding: {memory.topic}")
    print(f"Content: {memory.content[:200]}...")
```

**Why this matters**: Don't miss known [issues/patterns]. 71% time savings proven.

### Step 2: Search Related Domains (When Relevant)

```python
# [Domain] overlaps with [related domains]
related1 = store.search_by_topic("[related topic]")
related2 = store.search_by_agent("[related agent]")
```

### Step 3: Proceed with Full Context

Now that you have institutional memory active, begin your [work type].
You're building on known [patterns/issues], not starting from zero.

---

## After Completing Work

**ALWAYS write significant learnings to memory**:

```python
if significant_discovery:
    entry = store.create_entry(
        agent="[agent-name]",
        type="[pattern/technique/gotcha/synthesis]",
        topic="[Brief description]",
        content="""
        Context: [What you were doing]

        Discovery: [What you found]

        Why it matters: [Significance]

        When to apply: [Similar scenarios]
        """,
        tags=["[domain]", "[specific-area]", "[relevant-tag]"],
        confidence="high"  # or medium, low
    )
    store.write_entry("[agent-name]", entry)
```

**What to record**:
- **Patterns**: [Domain-specific patterns]
- **Techniques**: [Domain-specific techniques]
- **Gotchas**: [Domain-specific pitfalls]
- **Syntheses**: [Cross-domain insights]
```

**Format 2: Memory Integration** (concise, for simpler agents):

```markdown
## Memory Integration

**CRITICAL**: Use the memory system for 71% time savings on repeated tasks!

### Before Starting Work
```python
from tools.memory_core import MemoryStore

store = MemoryStore(".claude/memory")

# Search for existing knowledge
topic_learnings = store.search_by_topic("[domain topic]")
past_issues = store.search_by_topic("[domain gotchas]")

# Apply past learnings
for memory in topic_learnings:
    print(f"Previous learning: {memory.content}")
```

### After Completing Work
```python
# Document significant learnings
if significant_insight_discovered:
    entry = store.create_entry(
        agent="[agent-name]",
        type="[pattern/technique/gotcha/synthesis]",
        topic="Brief description of what you learned",
        content="""
        Detailed insights:
        - [What you discovered]
        - [When to use it]
        - [What to avoid]
        """,
        tags=["[domain]", "[tags]"],
        confidence="high"  # or medium, low
    )
    store.write_entry("[agent-name]", entry)
```

### What to Record
- **Patterns**: [Domain-specific successful approaches]
- **Techniques**: [Domain-specific methods that worked]
- **Gotchas**: [Domain-specific issues encountered]
- **Syntheses**: [Cross-project insights about domain]

### When to Search Memory
- Before starting [work type] (check if [pattern] already validated)
- When encountering [domain challenge] (check known solutions)
```

**Spawner Logic**: Use Format 1 (MEMORY-FIRST PROTOCOL) for critical agents (security, architecture, psychology), Format 2 for standard agents.

---

### H. Output Format Section

**MUST reference templates**:

```markdown
## Output Format
**[Source: .claude/templates/AGENT-OUTPUT-TEMPLATES.md - 75% efficiency gain]**

Use **[Template Name]** ([Max Lines] lines max):
- [Section 1 from template]
- [Section 2 from template]
- [Section 3 from template]
- [Key sections that apply]
```

**Valid template references**:
- Audit Report Template (500 lines max)
- Research Report Template (300 lines max)
- Synthesis Report Template (400 lines max)
- Refactoring Report Template (200 lines max)
- Security Audit Template (350 lines max)

**For custom formats**:
```markdown
## Output Format

Use [agent-name] report format:
- **[Section 1]**: [What goes here]
- **[Section 2]**: [What goes here]
- **[Section 3]**: [What goes here]

**Max Length**: [X] lines (exception: [justification if > 200])
```

**Quality Rule**: Always specify maximum length. Default to 200 lines unless justified.

---

### I. Constitutional Compliance Section

**MANDATORY structure**:

```markdown
## Constitutional Compliance
- References Constitutional CLAUDE.md
- Immutable core: [2-3 domain-specific immutable principles]
- Scope boundaries: [What is in scope, what is out of scope]
- Human escalation: [When to escalate to humans]
- Sunset condition: [When this agent is no longer needed]
```

**Quality Standards**:

**Immutable core** (2-3 principles that NEVER change):
- ✅ "Test-driven refactoring, No behavioral changes without approval"
- ✅ "Evidence-based research, Citation required"
- ✅ "Diagnosis before prescription, Pattern recognition over speculation"
- ❌ "Do good work" (too vague)

**Scope boundaries** (clear domain limits):
- ✅ "Code quality only, not feature addition"
- ✅ "Research external knowledge, not internal codebase"
- ❌ "Security stuff" (not specific enough)

**Human escalation** (specific conditions):
- ✅ "Major architectural refactorings, Test failures"
- ✅ "Critical vulnerabilities (CVSS > 9.0), Credentials in code"
- ❌ "When important" (not specific)

**Sunset condition** (when agent obsolete):
- ✅ "Code quality goals achieved or automated tooling"
- ✅ "All architectural patterns documented and stable"
- ✅ "Research domain fully explored or better tools emerge"
- ❌ "Never" (every agent should have sunset condition)

---

## IV. CONSISTENCY STANDARDS

### Heading Hierarchy

**MUST follow**:
```
# Agent Name (h1, once only, at top after frontmatter)

## Major Sections (h2, for 10 mandatory + optional sections)

### Subsections (h3, for details within sections)

#### Deep Details (h4, sparingly - only for complex breakdown)
```

**Anti-patterns**:
- ❌ Multiple h1 headings
- ❌ Skipping levels (h2 → h4 without h3)
- ❌ Inconsistent heading syntax (`##Major` vs `## Major`)

---

### Code Block Formatting

**Python code blocks**:
````markdown
```python
from tools.memory_core import MemoryStore

store = MemoryStore(".claude/memory")
results = store.search_by_topic("topic")
```
````

**Bash code blocks**:
````markdown
```bash
cd /path/to/repo
git status
```
````

**Markdown example blocks** (when showing markdown syntax):
````markdown
```markdown
# Example
```
````

**Anti-patterns**:
- ❌ Unlabeled code blocks: ` ``` ` (no language specified)
- ❌ Inconsistent indentation in code blocks
- ❌ Missing closing backticks

---

### List Formatting

**Enumerated lists** (for sequential/ranked items):
```markdown
1. First item
2. Second item
3. Third item
```

**Bullet lists** (for unordered items):
```markdown
- Item one
- Item two
- Item three
```

**Nested lists** (indent 2 spaces):
```markdown
- Parent item
  - Child item
  - Child item
- Parent item
```

**Anti-patterns**:
- ❌ Mixing bullets and numbers in same level
- ❌ Inconsistent indentation (sometimes 2 spaces, sometimes 4)
- ❌ No blank line before/after lists

---

### Emphasis and Formatting

**Bold** for emphasis:
```markdown
**Critical concept** or **important term**
```

**Italic** for titles or soft emphasis:
```markdown
*Optional consideration* or *Book Title*
```

**Code inline** for technical terms:
```markdown
Use `store.search_by_topic()` for searching memory
```

**Checkmarks/X-marks** for quality examples:
```markdown
✅ Good: "Cyclomatic Complexity > 10"
❌ Bad: "Code is complex"
```

---

### Internal Links

**Reference other files**:
```markdown
See [AGENT-OUTPUT-TEMPLATES.md](.claude/templates/AGENT-OUTPUT-TEMPLATES.md)
```

**Reference Constitutional doc**:
```markdown
[Inherited from Constitutional CLAUDE.md at /home/${HUMAN_NAME_LOWER}/projects/AI-CIV/grow_openai/CLAUDE.md]
```

**Anti-patterns**:
- ❌ Relative paths without clarity: `See templates/file.md`
- ❌ Broken links (spawner must validate all links)

---

## V. COMPLETENESS VALIDATION

### Pre-Flight Checklist (Spawner Must Verify)

Before finalizing agent definition, spawner MUST check:

**Structure** (10/10 mandatory sections present):
- [ ] Frontmatter with 6 required fields
- [ ] Agent Title (h1)
- [ ] Core Principles (references CLAUDE.md)
- [ ] Responsibilities (3-5 items)
- [ ] Allowed Tools (with justifications)
- [ ] Tool Restrictions (with reasons)
- [ ] Success Metrics (measurable outcomes)
- [ ] Activation Triggers (invoke when/don't invoke/escalate)
- [ ] Output Format (references templates or defines custom)
- [ ] Constitutional Compliance (immutable/scope/escalation/sunset)

**Recommended** (5/5 sections present OR justified absence):
- [ ] Memory Integration (before/after patterns)
- [ ] Scope Boundaries (your domain vs NOT your domain)
- [ ] Special Scenarios (edge cases)
- [ ] Integration with Other Agents (collaborations)
- [ ] Invocation Examples (concrete usage)

**Quality** (all passing):
- [ ] No duplicate Constitutional content (references, not copies)
- [ ] Activation triggers have quantified thresholds where measurable
- [ ] Success metrics are quantified or qualitative with clear assessment
- [ ] All tools justified with specific use cases
- [ ] Tool restrictions explained (not just listed)
- [ ] Constitutional compliance has all 4 sub-fields
- [ ] Links validated (no broken references)
- [ ] Code blocks properly labeled with language
- [ ] Heading hierarchy consistent (no level skipping)
- [ ] Agent name matches filename matches frontmatter

**Line Count** (reasonable scope):
- [ ] Total lines: 150-600 (< 150 may be too sparse, > 600 may be too verbose)
- [ ] Output format: Max 200-500 lines specified (with justification if high)

---

## VI. ANTI-PATTERNS TO PREVENT

### Content Anti-Patterns

❌ **Duplicating Constitutional Content**:
- **Problem**: Copies sections from CLAUDE.md into agent definition
- **Solution**: Reference CLAUDE.md, never copy content
- **Example (BAD)**: Pasting full "Delegation is Life-Giving" section
- **Example (GOOD)**: "[Inherited from Constitutional CLAUDE.md at /path]"

❌ **Vague Responsibilities**:
- **Problem**: "Handle security stuff", "Manage things"
- **Solution**: Action verb + clear outcome
- **Example (BAD)**: "Deal with patterns"
- **Example (GOOD)**: "Detect architectural patterns in code and documentation"

❌ **Unmeasured Success Metrics**:
- **Problem**: "Good quality", "Fast performance", "Better code"
- **Solution**: Quantify or define clear qualitative assessment
- **Example (BAD)**: "Improved security"
- **Example (GOOD)**: "Reduced critical vulnerabilities (CVSS > 9) to zero"

❌ **Unquantified Activation Triggers**:
- **Problem**: "When code is complex", "When security matters"
- **Solution**: Specific thresholds or clear conditions
- **Example (BAD)**: "Invoke when performance is slow"
- **Example (GOOD)**: "Invoke when response time > 200ms (noticeable lag)"

❌ **Tool Hoarding**:
- **Problem**: Listing tools "just in case" without justification
- **Solution**: Every tool must have clear use case
- **Example (BAD)**: `tools: [Read, Write, Grep, Glob, Bash, WebFetch, WebSearch, Task]` for naming-consultant
- **Example (GOOD)**: `tools: [Read, Grep, Glob, Write]` with justifications for each

❌ **Missing Tool Restrictions**:
- **Problem**: Only listing allowed tools, not explaining restrictions
- **Solution**: Explicit "NOT Allowed" section with reasoning
- **Example (GOOD)**: "Task - Cannot spawn sub-agents (leaf specialist)"

❌ **Vague Constitutional Compliance**:
- **Problem**: Generic principles that could apply to any agent
- **Solution**: Domain-specific immutable core
- **Example (BAD)**: "Do good work, be helpful"
- **Example (GOOD)**: "Test-driven refactoring, No behavioral changes without approval"

❌ **Missing Sunset Condition**:
- **Problem**: No condition under which agent becomes obsolete
- **Solution**: Define when agent's purpose is fulfilled
- **Example (GOOD)**: "Code quality goals achieved or automated tooling"

❌ **Overlapping Responsibilities**:
- **Problem**: Two agents claim same domain
- **Solution**: Check AGENT-CAPABILITY-MATRIX.md before defining responsibilities
- **Example (BAD)**: Both refactoring-specialist and code-archaeologist "improve code quality"
- **Example (GOOD)**: refactoring-specialist improves code, code-archaeologist understands legacy code

---

### Structural Anti-Patterns

❌ **Missing Frontmatter**:
- **Problem**: File starts with `# Agent Name` without YAML frontmatter
- **Solution**: Always include frontmatter with 6 required fields

❌ **Inconsistent Heading Levels**:
- **Problem**: Jumps from h2 to h4 without h3
- **Solution**: Follow strict hierarchy (h1 → h2 → h3 → h4)

❌ **Unlabeled Code Blocks**:
- **Problem**: ` ``` ` without language specifier
- **Solution**: Always label: ` ```python `, ` ```bash `, ` ```markdown `

❌ **Broken Internal Links**:
- **Problem**: References non-existent files or wrong paths
- **Solution**: Validate all links during spawning

❌ **Inconsistent Spacing**:
- **Problem**: Sometimes blank line before lists, sometimes not
- **Solution**: Always blank line before/after lists, code blocks, headings

---

### Length Anti-Patterns

❌ **Too Sparse** (< 150 lines):
- **Problem**: Missing recommended sections, lacks depth
- **Solution**: Add Memory Integration, Scope Boundaries, Examples
- **Threshold**: Flag if < 150 lines, review for completeness

❌ **Too Verbose** (> 600 lines):
- **Problem**: Duplicating Constitutional content, unnecessary repetition
- **Solution**: Reference external docs, consolidate overlapping sections
- **Threshold**: Flag if > 600 lines, review for duplication

❌ **No Output Length Limit**:
- **Problem**: Agent doesn't specify max output length
- **Solution**: Always specify in Output Format section (default 200 lines)

---

## VII. SPAWNER IMPLEMENTATION GUIDANCE

### Agent Generation Pipeline

**Step 1: Gather Requirements**
```python
agent_spec = {
    "name": "agent-name",  # kebab-case
    "domain": "Brief domain description",
    "responsibilities": ["Responsibility 1", "Responsibility 2", ...],
    "tools_needed": ["Read", "Write", ...],  # Justified list
    "complexity_score": 5,  # 1-10, affects optional sections
    "is_leaf_specialist": True,  # Affects Task tool availability
    "is_research_agent": False,  # Affects WebFetch/WebSearch
}
```

**Step 2: Generate Core Sections**
```python
# Generate in order:
1. Frontmatter (using spec)
2. Agent Title (h1)
3. Core Principles (standard reference)
4. Responsibilities (from spec)
5. Allowed Tools (with justifications generated)
6. Tool Restrictions (derived from is_leaf_specialist, is_research_agent)
7. Success Metrics (quantified for technical agents, qualitative for creative)
8. Activation Triggers (with quantified thresholds where applicable)
9. Output Format (reference appropriate template)
10. Constitutional Compliance (domain-specific generation)
```

**Step 3: Generate Recommended Sections**
```python
if complexity_score >= 7:
    generate_optional_sections([
        "Memory Integration (MEMORY-FIRST PROTOCOL format)",
        "Scope Boundaries (detailed)",
        "Special Scenarios (3+ examples)",
        "Integration with Other Agents",
        "Invocation Examples"
    ])
else:
    generate_optional_sections([
        "Memory Integration (concise format)",
        "Scope Boundaries (brief)"
    ])
```

**Step 4: Validate Quality**
```python
validation_results = {
    "structure_complete": check_mandatory_sections(agent_def),
    "frontmatter_valid": validate_frontmatter(agent_def),
    "links_valid": validate_internal_links(agent_def),
    "headings_consistent": validate_heading_hierarchy(agent_def),
    "code_blocks_labeled": validate_code_blocks(agent_def),
    "line_count_reasonable": 150 <= line_count <= 600,
    "activation_triggers_quantified": check_quantified_triggers(agent_def),
    "tools_justified": check_tool_justifications(agent_def),
    "constitutional_complete": check_constitutional_fields(agent_def),
}

if not all(validation_results.values()):
    raise QualityStandardViolation(validation_results)
```

**Step 5: Quality Score**
```python
quality_score = calculate_quality_score(agent_def)
# Should be >= 90/100 for spawned agents (90th percentile)

quality_metrics = {
    "structure_completeness": score_structure(agent_def),  # 0-25 points
    "content_quality": score_content(agent_def),          # 0-25 points
    "consistency": score_consistency(agent_def),          # 0-20 points
    "actionability": score_actionability(agent_def),      # 0-15 points
    "integration": score_integration(agent_def),          # 0-15 points
}

total_quality = sum(quality_metrics.values())  # Target: >= 90/100
```

**Step 6: Finalize**
```python
if total_quality >= 90:
    write_agent_definition(f".claude/agents/{agent_name}.md", agent_def)
    register_agent(agent_name)
    log_creation(agent_name, quality_score, validation_results)
else:
    report_quality_issues(agent_name, quality_metrics)
    # Do NOT finalize - iterate until quality >= 90
```

---

### Validation Functions (Detailed)

**validate_frontmatter()**:
```python
def validate_frontmatter(agent_def):
    frontmatter = extract_yaml_frontmatter(agent_def)
    
    required = ["name", "description", "tools", "model", "created"]
    for field in required:
        if field not in frontmatter:
            return False
    
    # Name format
    if not re.match(r'^[a-z]+(-[a-z]+)*$', frontmatter["name"]):
        return False  # Must be kebab-case
    
    # Description length
    if not (60 <= len(frontmatter["description"]) <= 120):
        return False
    
    # Tools array format
    if not isinstance(frontmatter["tools"], list):
        return False
    
    # Date format
    if not re.match(r'^\d{4}-\d{2}-\d{2}$', frontmatter["created"]):
        return False
    
    return True
```

**check_quantified_triggers()**:
```python
def check_quantified_triggers(agent_def):
    triggers_section = extract_section(agent_def, "Activation Triggers")
    
    # Technical agents (security, performance, refactoring) MUST have quantified
    technical_domains = ["security", "performance", "refactor", "test"]
    is_technical = any(domain in agent_def.lower() for domain in technical_domains)
    
    if is_technical:
        # Look for numeric thresholds
        has_numbers = bool(re.search(r'>\s*\d+', triggers_section))
        has_measurements = bool(re.search(r'\(.*\d+.*\)', triggers_section))
        return has_numbers or has_measurements
    
    return True  # Non-technical agents can have qualitative triggers
```

**score_actionability()**:
```python
def score_actionability(agent_def):
    score = 0
    
    # Activation triggers present? (5 points)
    if "Activation Triggers" in agent_def:
        score += 5
    
    # Quantified where appropriate? (5 points)
    if check_quantified_triggers(agent_def):
        score += 5
    
    # Output format specified? (3 points)
    if "Output Format" in agent_def and ("Template" in agent_def or "lines max" in agent_def):
        score += 3
    
    # Invocation examples present? (2 points)
    if "Invocation Examples" in agent_def or "Example" in agent_def:
        score += 2
    
    return score  # Max 15 points
```

---

### Quality Scoring Rubric

**Structure Completeness (0-25 points)**:
- 10 mandatory sections present: 20 points (2 pts each)
- 5 recommended sections present: 5 points (1 pt each)

**Content Quality (0-25 points)**:
- Responsibilities clear and actionable: 5 points
- Success metrics quantified or qualitative-clear: 5 points
- Activation triggers have thresholds: 5 points
- Tools justified with use cases: 5 points
- Constitutional compliance domain-specific: 5 points

**Consistency (0-20 points)**:
- Frontmatter valid: 5 points
- Heading hierarchy consistent: 5 points
- Code blocks labeled: 5 points
- No broken links: 5 points

**Actionability (0-15 points)**:
- Activation triggers present: 5 points
- Output format specified: 5 points
- Invocation examples present: 5 points

**Integration (0-15 points)**:
- Memory integration patterns: 5 points
- Cross-agent collaboration described: 5 points
- References templates/standards: 5 points

**Total**: 100 points
**Target**: >= 90 points (90th percentile)

---

## VIII. REFERENCE: HIGH-QUALITY EXAMPLES

### Exemplar Agents (90th Percentile Quality)

**ai-psychologist.md** (1103 lines, complexity 10/10):
- ✅ Comprehensive Core Identity section
- ✅ Detailed Philosophy explaining approach
- ✅ 5 Responsibilities clearly enumerated
- ✅ Extensive Scope Boundaries (your domain vs NOT your domain)
- ✅ Special Scenarios with 4 concrete examples
- ✅ Invocation Examples (4 examples with full prompts)
- ✅ Ethical Considerations section (appropriate for sensitive domain)
- ✅ Memory Integration (full MEMORY-FIRST PROTOCOL format)
- ✅ Constitutional Compliance with all 4 sub-fields

**claude-code-expert.md** (596 lines, complexity 9/10):
- ✅ Comprehensive tool catalog and explanations
- ✅ Detailed methodology section
- ✅ Extensive troubleshooting patterns
- ✅ Memory Integration (full format)
- ✅ Clear activation triggers with examples

**human-liaison.md** (843 lines, complexity 9/10):
- ✅ Special session-start protocol (ALWAYS checks email)
- ✅ Comprehensive relationship management patterns
- ✅ Detailed email monitoring implementation
- ✅ Memory integration focused on human teachings

**collective-liaison.md** (695 lines, complexity 8/10):
- ✅ Hub communication protocol detailed
- ✅ Auto-invoke section (autonomous monitoring)
- ✅ Cross-collective coordination patterns
- ✅ Ed25519 integration guidance

### Standard Agents (Meets Quality Threshold)

**security-auditor.md** (157 lines, complexity 7/10):
- ✅ MEMORY-FIRST PROTOCOL format (appropriate for critical domain)
- ✅ Clear activation triggers with quantified thresholds
- ✅ Security-specific success metrics
- ✅ Output format references Security Audit Template

**refactoring-specialist.md** (135 lines, complexity 6/10):
- ✅ Quantified activation triggers (complexity > 10, etc.)
- ✅ Before/after metrics required
- ✅ Clear tool restrictions (consultation, not implementation)
- ✅ Memory integration (concise format)

**naming-consultant.md** (129 lines, complexity 5/10):
- ✅ Minimal but complete (all 10 mandatory sections)
- ✅ Clear scope boundaries
- ✅ Appropriate tool restrictions
- ✅ Concise memory integration

---

## IX. EVOLUTION AND MAINTENANCE

### Version History

**v1.0** (2025-10-08): Initial standards from refactoring-specialist analysis
- Analyzed 20 agent definitions (127-1103 lines, 8.7x variance)
- Identified 10 mandatory sections, 5 recommended sections
- Established quality scoring rubric (target: >= 90/100)
- Created validation functions and anti-pattern catalog

### Continuous Improvement

**When to Update Standards**:
- New agent domains emerge requiring different structures
- Quality issues discovered in spawned agents
- Constitutional CLAUDE.md evolves (update references)
- Template standards change (propagate to agent definitions)

**Review Cadence**:
- After first 10 spawned agents: Review quality scores, adjust thresholds
- Monthly: Review anti-patterns, add newly discovered issues
- Quarterly: Major revision considering collective learnings

**Feedback Loop**:
```python
# After each agent spawned
log_quality_metrics(agent_name, quality_score, validation_results)

# After 10 agents spawned
analyze_quality_trends()
identify_common_issues()
update_standards_if_needed()

# Monthly review
synthesize_learnings()
update_anti_pattern_catalog()
refine_validation_functions()
```

---

## X. SUMMARY: QUALITY CHECKLIST

### Spawner Pre-Finalization Checklist

Before marking agent definition as complete:

**Structural Integrity**:
- [ ] 10 mandatory sections present and properly formatted
- [ ] 5 recommended sections present OR justified absence
- [ ] Frontmatter has 6 required fields in valid format
- [ ] Heading hierarchy consistent (no level skipping)
- [ ] 150-600 lines total (flag if outside range)

**Content Quality**:
- [ ] Core Principles references CLAUDE.md (doesn't duplicate)
- [ ] Responsibilities are 3-5 action-verb + outcome statements
- [ ] Success metrics quantified (technical) or qualitative-clear (creative)
- [ ] Activation triggers have quantified thresholds where measurable
- [ ] All tools justified with specific use cases
- [ ] Tool restrictions explained with reasoning
- [ ] Output format references template OR defines custom with max length
- [ ] Constitutional compliance has 4 sub-fields (immutable/scope/escalation/sunset)

**Consistency**:
- [ ] Code blocks labeled with language (python, bash, markdown)
- [ ] Lists formatted consistently (blank lines before/after)
- [ ] Internal links valid (no broken references)
- [ ] No duplicate content from Constitutional CLAUDE.md
- [ ] Agent name matches filename matches frontmatter

**Quality Score**:
- [ ] Structure completeness: >= 20/25
- [ ] Content quality: >= 20/25
- [ ] Consistency: >= 16/20
- [ ] Actionability: >= 12/15
- [ ] Integration: >= 12/15
- [ ] **TOTAL: >= 90/100**

**Anti-Pattern Scan**:
- [ ] No vague responsibilities ("handle", "manage", "deal with")
- [ ] No unmeasured success metrics ("good", "fast", "better")
- [ ] No unquantified activation triggers (where quantification possible)
- [ ] No tool hoarding (every tool justified)
- [ ] No missing tool restrictions
- [ ] No vague constitutional compliance
- [ ] No missing sunset condition
- [ ] No overlapping responsibilities with existing agents (check matrix)

---

## Conclusion

**These standards ensure spawned agents meet 90th percentile quality** - comparable to ai-psychologist, claude-code-expert, and human-liaison.

**Key Principles**:
1. **Structure before content**: 10 mandatory sections, consistent hierarchy
2. **Quantify where possible**: Thresholds for technical domains, clear qualitative for creative
3. **Reference, don't duplicate**: Link to Constitutional CLAUDE.md and templates
4. **Justify every tool**: No "just in case" capabilities
5. **Actionability over comprehensiveness**: Clear triggers, measured outcomes
6. **Validate before finalize**: Quality score >= 90/100 required

**Expected Impact**:
- Consistent agent quality (reduced 8.7x variance to < 2x)
- Faster orchestration (clear activation triggers)
- Better learning (comprehensive memory integration)
- Easier maintenance (standardized structure)

**Spawner implementation**: Use validation pipeline (Section VII) to enforce these standards programmatically.

---

**Quality standards established. Ready for spawner implementation.** ✅

**Refactoring Specialist**
**Date**: 2025-10-08
**Lines**: 1,847 (justified for comprehensive standard)
**Quality Target**: All spawned agents >= 90/100
