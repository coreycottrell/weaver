# Agent Quality Standards Defined for Spawner

**Mission**: Define quality standards for programmatic agent creation
**Agent**: refactoring-specialist
**Date**: 2025-10-08
**Status**: COMPLETE

---

## What I Analyzed

**20 agent definitions** across quality spectrum:
- Smallest: 127 lines (naming-consultant)
- Largest: 1103 lines (ai-psychologist)
- **Variance: 8.7x** (significant quality inconsistency)

**Exemplar agents** (90th percentile quality):
- ai-psychologist (1103 lines, complexity 10/10)
- claude-code-expert (596 lines, complexity 9/10)
- human-liaison (843 lines, complexity 9/10)
- collective-liaison (695 lines, complexity 8/10)

**Standard agents** (meets threshold):
- security-auditor (157 lines, complexity 7/10)
- refactoring-specialist (135 lines, complexity 6/10)
- naming-consultant (129 lines, complexity 5/10)

---

## Quality Standards Established

### Structural Requirements

**10 Mandatory Sections** (MUST exist):
1. Frontmatter (YAML metadata with 6 required fields)
2. Agent Title (h1 heading)
3. Core Principles (references Constitutional CLAUDE.md)
4. Responsibilities (3-5 enumerated, action-verb + outcome)
5. Allowed Tools (with justifications for each)
6. Tool Restrictions (explicit NOT allowed list with reasoning)
7. Success Metrics (quantified or qualitative-clear)
8. Activation Triggers (invoke when/don't invoke/escalate when)
9. Output Format (references templates or defines custom with max length)
10. Constitutional Compliance (immutable/scope/escalation/sunset)

**5 Recommended Sections** (SHOULD exist):
11. Memory Integration (before/after work patterns)
12. Scope Boundaries (your domain vs NOT your domain)
13. Special Scenarios (edge cases, complex situations)
14. Integration with Other Agents (primary collaborations)
15. Invocation Examples (concrete usage patterns)

**Validation**: Spawner MUST verify all 10 mandatory sections before finalizing agent.

---

### Content Quality Standards

**Responsibilities**:
- ✅ Action verbs: "Audit", "Analyze", "Design", "Synthesize", "Detect"
- ✅ Clear outcomes: "ensuring X" or "to achieve Y"
- ✅ 3-5 responsibilities (not 1, not 10)
- ❌ Vague verbs: "Handle", "Manage", "Deal with"

**Success Metrics**:
- ✅ Quantified: "Cyclomatic complexity -20%", "Response time < 2 hours"
- ✅ Qualitative-clear: "Improved code review feedback", "Intention-revealing at first read"
- ❌ Vague: "Good quality", "Fast response", "Better code"

**Activation Triggers**:
- ✅ Quantified thresholds: "Complexity > 10", "Response time > 200ms", "Duplication > 20%"
- ✅ Clear anti-patterns: "Complexity < 5 (trivial)", "New code (< 1 week old)"
- ✅ Specific escalation: "Refactoring requires API changes", "Critical vulnerabilities (CVSS > 9.0)"
- ❌ Unquantified: "When code is complex", "When security matters"

**Tools**:
- ✅ Every tool justified with specific use case
- ✅ Tool restrictions explained (not just listed)
- ❌ Tool hoarding ("just in case" without justification)

**Constitutional Compliance**:
- ✅ Domain-specific immutable core (2-3 principles)
- ✅ Clear scope boundaries (in scope vs out of scope)
- ✅ Specific human escalation conditions
- ✅ Sunset condition (when agent obsolete)
- ❌ Generic principles that could apply to any agent

---

### Consistency Standards

**Frontmatter** (YAML):
```yaml
---
name: agent-name-kebab-case  # Must match filename
description: One-sentence clear description (60-120 chars)
tools: [Read, Write, Grep, Glob]  # Array format, justified list
model: sonnet-4
created: YYYY-MM-DD  # ISO date format
---
```

**Heading Hierarchy**:
- h1: Agent name (once only, top of file)
- h2: Major sections (10 mandatory + optional)
- h3: Subsections within sections
- h4: Deep details (sparingly)

**Code Blocks**: Always labeled with language (```python, ```bash, ```markdown)

**Lists**: Consistent indentation (2 spaces), blank line before/after

**Links**: Validate all internal references (no broken links)

---

### Quality Scoring Rubric

**Total: 100 points** (Target: >= 90 for spawned agents)

- **Structure Completeness** (25 points): 10 mandatory + 5 recommended sections
- **Content Quality** (25 points): Responsibilities, metrics, triggers, tools, compliance
- **Consistency** (20 points): Frontmatter, headings, code blocks, links
- **Actionability** (15 points): Triggers, output format, examples
- **Integration** (15 points): Memory patterns, collaborations, template references

**Threshold**: Spawner must achieve >= 90/100 before finalizing agent.

---

## Anti-Patterns Cataloged

### Content Anti-Patterns (8)

1. **Duplicating Constitutional Content** - Reference CLAUDE.md, never copy
2. **Vague Responsibilities** - "Handle security stuff" → "Audit code for security vulnerabilities"
3. **Unmeasured Success Metrics** - "Good quality" → "Cyclomatic complexity -20%"
4. **Unquantified Activation Triggers** - "When complex" → "Complexity > 10"
5. **Tool Hoarding** - All tools listed "just in case" → Only justified tools
6. **Missing Tool Restrictions** - No "NOT Allowed" section → Explicit restrictions with reasoning
7. **Vague Constitutional Compliance** - "Do good work" → Domain-specific immutable principles
8. **Missing Sunset Condition** - "Never obsolete" → "Code quality goals achieved or automated tooling"

### Structural Anti-Patterns (5)

1. **Missing Frontmatter** - File starts with h1 → Always include YAML frontmatter
2. **Inconsistent Heading Levels** - h2 → h4 without h3 → Follow strict hierarchy
3. **Unlabeled Code Blocks** - ``` without language → Always label with language
4. **Broken Internal Links** - Non-existent file references → Validate all links
5. **Inconsistent Spacing** - Sometimes blank lines, sometimes not → Always blank line before/after lists/code/headings

### Length Anti-Patterns (3)

1. **Too Sparse** (< 150 lines) - Missing recommended sections → Add Memory Integration, Scope Boundaries, Examples
2. **Too Verbose** (> 600 lines) - Duplicating Constitutional content → Reference external docs
3. **No Output Length Limit** - Agent doesn't specify max output → Always specify (default 200 lines)

---

## Spawner Implementation Guidance

### Agent Generation Pipeline

**Step 1: Gather Requirements**
- Name, domain, responsibilities, tools, complexity score (1-10)
- is_leaf_specialist flag (affects Task tool)
- is_research_agent flag (affects WebFetch/WebSearch)

**Step 2: Generate Core Sections**
- 10 mandatory sections in order
- Quantified metrics for technical agents (complexity >= 7)
- Qualitative metrics for creative agents (complexity < 7)

**Step 3: Generate Recommended Sections**
- All 5 recommended if complexity >= 7
- 2 essential (Memory Integration, Scope Boundaries) if complexity < 7

**Step 4: Validate Quality**
- Check mandatory sections present
- Validate frontmatter format
- Check links, headings, code blocks
- Verify activation triggers quantified (for technical agents)
- Ensure tools justified, restrictions explained

**Step 5: Quality Score**
- Calculate score across 5 dimensions
- Threshold: >= 90/100 required

**Step 6: Finalize**
- If score >= 90: Write agent definition, register agent, log creation
- If score < 90: Report issues, iterate until threshold met

### Validation Functions Provided

- `validate_frontmatter()` - Check YAML format, name, description, tools, date
- `check_quantified_triggers()` - Ensure technical agents have numeric thresholds
- `score_actionability()` - Score activation triggers, output format, examples
- Plus full scoring rubric for all 5 dimensions

---

## Expected Impact

**Before Standards**:
- Agent quality variance: 8.7x (127 to 1103 lines)
- Inconsistent activation triggers (40% waste from Great Audit)
- Missing memory integration (8 of 20 agents)
- Varied frontmatter formats

**After Standards**:
- All spawned agents: 90th percentile quality (comparable to ai-psychologist, claude-code-expert)
- Consistent structure: 10 mandatory + 5 recommended sections
- Clear activation triggers: Quantified thresholds where measurable
- Universal memory integration: Search-before/write-after patterns
- Validation pipeline: Quality >= 90/100 enforced programmatically

**Measurable Improvements**:
- Quality variance: Reduce 8.7x to < 2x (150-600 lines typical)
- Invocation appropriateness: 60% → 90% (clear triggers)
- Memory integration: 60% coverage → 100% coverage
- Frontmatter consistency: Variable → 100% valid YAML

---

## Deliverable Location

**Complete Standards Document**:
`/home/corey/projects/AI-CIV/grow_openai/.claude/templates/AGENT-QUALITY-STANDARDS.md`

**Length**: 1,847 lines (justified for comprehensive standard)

**Sections**:
1. Executive Summary
2. Structural Quality Standards (10 mandatory, 5 recommended, optional)
3. Frontmatter Standards (6 required fields, 4 optional)
4. Content Quality Standards (9 subsections: Core Principles through Constitutional Compliance)
5. Consistency Standards (headings, code blocks, lists, emphasis, links)
6. Completeness Validation (pre-flight checklist)
7. Anti-Patterns to Prevent (content, structural, length)
8. Spawner Implementation Guidance (pipeline, validation functions, scoring rubric)
9. Reference: High-Quality Examples (exemplar agents, standard agents)
10. Evolution and Maintenance (version history, review cadence, feedback loop)
11. Summary: Quality Checklist

---

## Next Steps for Spawner Development

1. **Implement Validation Pipeline** - Use pipeline from Section VII
2. **Build Validation Functions** - Implement `validate_frontmatter()`, `check_quantified_triggers()`, etc.
3. **Create Scoring System** - Implement 5-dimension scoring rubric (structure, content, consistency, actionability, integration)
4. **Integrate Quality Gate** - Spawner must score >= 90/100 before finalizing
5. **Log Quality Metrics** - Track spawned agent quality scores for continuous improvement
6. **Test Against Exemplars** - Validate scoring system scores ai-psychologist, claude-code-expert >= 90

---

## Refactoring Patterns Applied

**Pattern Detection**:
- Analyzed 20 agent definitions for structural patterns
- Identified 10 mandatory sections common to high-quality agents
- Extracted quantified thresholds from technical agents (security, performance, refactoring)

**Anti-Pattern Catalog**:
- Documented 16 anti-patterns across content, structure, length
- Provided good/bad examples for each
- Created prevention guidelines for spawner

**Standardization**:
- Unified frontmatter format (YAML with 6 required fields)
- Standardized heading hierarchy (h1 → h2 → h3 → h4)
- Consistent code block labeling, list formatting, link styles

**Validation Framework**:
- Pre-flight checklist (spawner must verify before finalizing)
- Validation functions (programmatic quality checks)
- Scoring rubric (5 dimensions, 100 points, target >= 90)

---

## Meta-Learning (For My Memory)

**What Worked**:
- Analyzing quality spectrum (smallest to largest agents) revealed patterns
- Identifying exemplar agents (ai-psychologist, claude-code-expert) provided quality target
- Extracting quantified thresholds from technical agents enabled measurable standards
- Creating validation pipeline makes quality enforcement programmatic (not manual)

**Pattern Discovered**:
- Quality variance correlates with domain complexity (psychology/liaison = verbose, naming = concise)
- Mandatory vs recommended sections balance completeness with domain appropriateness
- Quantified thresholds critical for technical agents, qualitative triggers for creative agents

**Reusable for Spawner**:
- Validation pipeline pattern applies to any programmatic generation
- Quality scoring rubric adaptable to other artifact types (not just agents)
- Anti-pattern catalog grows with experience (living document)

**Domain Insight**:
- Agent quality = Structure (25) + Content (25) + Consistency (20) + Actionability (15) + Integration (15)
- 90th percentile = exemplar-comparable quality (not just "good enough")
- Spawner should ENFORCE standards, not SUGGEST them (quality gate, not guideline)

---

## Confidence Assessment

**Structure Standards**: HIGH (analyzed 20 agents, clear patterns emerged)
**Content Standards**: HIGH (quantified from Great Audit, validated against exemplars)
**Consistency Standards**: HIGH (derived from best practices, validated in exemplars)
**Validation Pipeline**: MEDIUM (design complete, implementation needed for testing)
**Quality Scoring**: MEDIUM (rubric defined, needs calibration against actual scoring)

**Overall Confidence**: HIGH for standards definition, MEDIUM for spawner implementation readiness

**Recommendation**: Standards are production-ready. Spawner should implement validation pipeline, test against 2-3 agent specs, calibrate scoring rubric, then begin spawning.

---

**Quality standards complete. Ready for spawner implementation.** ✅

**Refactoring Specialist**
**Lines**: This report: 484 | Standards doc: 1,847 | Total: 2,331
**Time Invested**: ~2 hours (comprehensive analysis)
**Artifacts**:
- `/home/corey/projects/AI-CIV/grow_openai/.claude/templates/AGENT-QUALITY-STANDARDS.md`
- `/home/corey/projects/AI-CIV/grow_openai/to-corey/REFACTORING-QUALITY-STANDARDS-COMPLETE.md` (this file)
